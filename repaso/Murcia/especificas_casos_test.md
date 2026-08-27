# Murcia (CARM) — Materias específicas: casos prácticos + test (30 preguntas)

## 1. Casos prácticos resueltos

### Caso práctico 1 — Reorganización departamental en Active Directory

**Enunciado.** Un organismo de la CARM fusiona los departamentos "Contabilidad" y "Tesorería" en uno nuevo, "Financiero" (8 usuarios, actualmente repartidos en las OU `Contabilidad` y `Tesoreria`). Se pide: reestructurar las OU, mover los usuarios, crear el grupo de seguridad para acceso a `\\SRV-DATOS\Financiero` (permiso de modificación), delegar en el técnico `jmartinez` la gestión de usuarios de esa OU sin hacerlo administrador de dominio, y mapear la unidad automáticamente por GPO solo a los miembros del nuevo grupo.

**Resolución.**

1. **Crear la OU destino:**
```powershell
New-ADOrganizationalUnit -Name "Financiero" `
  -Path "OU=Departamentos,DC=carm,DC=local" `
  -ProtectedFromAccidentalDeletion $true
```

2. **Mover los usuarios** desde las OU antiguas:
```powershell
Get-ADUser -Filter * -SearchBase "OU=Contabilidad,OU=Departamentos,DC=carm,DC=local" |
    Move-ADObject -TargetPath "OU=Financiero,OU=Departamentos,DC=carm,DC=local"

Get-ADUser -Filter * -SearchBase "OU=Tesoreria,OU=Departamentos,DC=carm,DC=local" |
    Move-ADObject -TargetPath "OU=Financiero,OU=Departamentos,DC=carm,DC=local"
```
Tras verificar que quedan vacías, se desprotegen (`Set-ADOrganizationalUnit ... -ProtectedFromAccidentalDeletion $false`) y se eliminan.

3. **Modelo AGDLP** (cuentA → Grupo Global → grupo Domain Local → Permiso), buena práctica frente a asignar permisos directamente a usuarios:
```powershell
New-ADGroup -Name "GG_Financiero" -GroupScope Global -GroupCategory Security `
  -Path "OU=Financiero,OU=Departamentos,DC=carm,DC=local"

Get-ADUser -Filter * -SearchBase "OU=Financiero,OU=Departamentos,DC=carm,DC=local" |
    Add-ADGroupMember -Identity "GG_Financiero"

New-ADGroup -Name "DL_Financiero_Modificar" -GroupScope DomainLocal -GroupCategory Security `
  -Path "OU=Grupos_Recursos,DC=carm,DC=local"

Add-ADGroupMember -Identity "DL_Financiero_Modificar" -Members "GG_Financiero"
```

4. **Permisos sobre el recurso**: a nivel de recurso compartido se concede "Cambiar" solo a `DL_Financiero_Modificar`; a nivel NTFS:
```powershell
$acl = Get-Acl "D:\Datos\Financiero"
$regla = New-Object System.Security.AccessControl.FileSystemAccessRule(
  "CARM\DL_Financiero_Modificar","Modify","ContainerInherit,ObjectInherit","None","Allow")
$acl.AddAccessRule($regla)
Set-Acl "D:\Datos\Financiero" $acl
```
El permiso efectivo resultante es la **intersección** (el más restrictivo) entre el permiso de recurso compartido y el NTFS.

5. **Delegación de control** (principio de mínimo privilegio: ni Domain Admins ni Account Operators):
Con el Asistente de delegación de control sobre la OU `Financiero`, se marcan únicamente las tareas "Restablecer contraseñas de usuario y forzar cambio en el siguiente inicio de sesión" y "Crear, eliminar y administrar cuentas de usuario" para `jmartinez`. Equivalente en `dsacls`:
```
dsacls "OU=Financiero,OU=Departamentos,DC=carm,DC=local" /I:S /G "CARM\jmartinez:CA;Reset Password;user"
```

6. **GPO de mapeo de unidad**: nueva GPO vinculada a la OU `Financiero`, con una Preferencia de asignación de unidad (`\\SRV-DATOS\Financiero` → `F:`). En **Filtrado de seguridad** se retira "Usuarios autenticados" y se añade `GG_Financiero`, de modo que solo esos usuarios reciban la política. Verificación en cliente con `gpupdate /force` y `gpresult /r`.

---

### Caso práctico 2 — Script bash de monitorización de un servidor Linux

**Enunciado.** Un servidor CentOS/RHEL (systemd) del CPD aloja una aplicación web servida por `nginx`. Se pide un script, ejecutado por `cron` cada 5 minutos, que compruebe uso de CPU, memoria, espacio en `/var` y estado del servicio `nginx`; si se supera un umbral o el servicio cae, debe registrar el evento y avisar por correo, evitando alertas repetidas ("antiflood") en menos de 30 minutos, e intentar el reinicio automático del servicio.

**Resolución.**

```bash
#!/usr/bin/env bash
# monitor_sistema.sh — Monitorización CPU/MEM/disco/servicio nginx
set -euo pipefail

UMBRAL_CPU=85
UMBRAL_MEM=90
UMBRAL_DISCO=85
SERVICIO="nginx"
DESTINATARIO="sistemas@carm.es"
LOCKFILE="/var/run/monitor_alerta.lock"
LOCK_MINUTOS=30
LOGFILE="/var/log/monitor_sistema.log"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1" >> "$LOGFILE"
    logger -t monitor_sistema "$1"
}

alerta_permitida() {
    if [[ -f "$LOCKFILE" ]]; then
        local diff=$(( ( $(date +%s) - $(stat -c %Y "$LOCKFILE") ) / 60 ))
        [[ $diff -ge $LOCK_MINUTOS ]]
    else
        true
    fi
}

enviar_alerta() {
    local asunto="$1" cuerpo="$2"
    if alerta_permitida; then
        echo "$cuerpo" | mail -s "[ALERTA CPD] $asunto" "$DESTINATARIO"
        touch "$LOCKFILE"
        log "ALERTA enviada: $asunto"
    else
        log "Alerta suprimida (antiflood): $asunto"
    fi
}

cpu_uso=$(top -bn1 | awk -F'[,: ]+' '/Cpu\(s\)/ {print 100 - $8}' | cut -d. -f1)
[[ "$cpu_uso" -ge "$UMBRAL_CPU" ]] && enviar_alerta "CPU alta (${cpu_uso}%)" "Uso de CPU ${cpu_uso}%, umbral ${UMBRAL_CPU}%."

mem_uso=$(free | awk '/Mem:/ {printf "%d", $3/$2*100}')
[[ "$mem_uso" -ge "$UMBRAL_MEM" ]] && enviar_alerta "Memoria alta (${mem_uso}%)" "Uso de memoria ${mem_uso}%, umbral ${UMBRAL_MEM}%."

disco_uso=$(df -h /var | awk 'NR==2 {gsub("%","",$5); print $5}')
[[ "$disco_uso" -ge "$UMBRAL_DISCO" ]] && enviar_alerta "Disco /var alto (${disco_uso}%)" "Uso de /var ${disco_uso}%, umbral ${UMBRAL_DISCO}%."

if ! systemctl is-active --quiet "$SERVICIO"; then
    enviar_alerta "Servicio $SERVICIO caído" "systemctl indica que $SERVICIO no está activo. Reintentando..."
    systemctl restart "$SERVICIO" && log "Servicio $SERVICIO reiniciado" || log "ERROR: fallo al reiniciar $SERVICIO"
fi

log "Comprobación OK. CPU=${cpu_uso}% MEM=${mem_uso}% DISCO=${disco_uso}%"
```

Entrada en `crontab -e`: `*/5 * * * * /usr/local/bin/monitor_sistema.sh`

Puntos clave: `set -euo pipefail` para fallo temprano; `stat -c %Y` obtiene el timestamp del lockfile para el control antiflood; `systemctl is-active --quiet` como comprobación silenciosa apta para scripting; separación entre `logger` (syslog/journald) y fichero propio para trazabilidad doble.

---

### Caso práctico 3 — PL/SQL con cursor explícito y manejo de excepciones (proceso batch)

**Enunciado.** Cada noche debe ejecutarse un proceso batch que recorra `facturas_pendientes` (estado `'P'`) y aplique el cobro descontando saldo del cliente. Si un cliente no tiene saldo suficiente, no existe, o se produce cualquier otro error, **no debe abortarse el proceso completo**: se registra el fallo en `log_errores_batch` y se continúa con la siguiente factura. Al final, commit único y resumen de resultados.

**Resolución.**

```sql
DECLARE
  CURSOR c_facturas IS
      SELECT id_factura, importe, id_cliente
      FROM   facturas_pendientes
      WHERE  estado = 'P'
      FOR UPDATE OF estado;

  v_saldo       clientes.saldo%TYPE;
  v_ok          PLS_INTEGER := 0;
  v_error       PLS_INTEGER := 0;
  e_saldo_insuf EXCEPTION;

BEGIN
  FOR r_fact IN c_facturas LOOP
    BEGIN
      SAVEPOINT sp_factura;

      SELECT saldo INTO v_saldo
      FROM   clientes
      WHERE  id_cliente = r_fact.id_cliente
      FOR UPDATE;

      IF v_saldo < r_fact.importe THEN
        RAISE e_saldo_insuf;
      END IF;

      UPDATE clientes SET saldo = saldo - r_fact.importe
      WHERE  id_cliente = r_fact.id_cliente;

      UPDATE facturas_pendientes
      SET    estado = 'C', fecha_cobro = SYSDATE
      WHERE  CURRENT OF c_facturas;

      v_ok := v_ok + 1;

    EXCEPTION
      WHEN e_saldo_insuf THEN
        ROLLBACK TO sp_factura;
        INSERT INTO log_errores_batch (id_factura, fecha, descripcion)
        VALUES (r_fact.id_factura, SYSDATE, 'Saldo insuficiente');
        v_error := v_error + 1;

      WHEN NO_DATA_FOUND THEN
        ROLLBACK TO sp_factura;
        INSERT INTO log_errores_batch (id_factura, fecha, descripcion)
        VALUES (r_fact.id_factura, SYSDATE, 'Cliente no encontrado');
        v_error := v_error + 1;

      WHEN OTHERS THEN
        ROLLBACK TO sp_factura;
        INSERT INTO log_errores_batch (id_factura, fecha, descripcion)
        VALUES (r_fact.id_factura, SYSDATE, 'Error inesperado: ' || SQLERRM);
        v_error := v_error + 1;
    END;
  END LOOP;

  COMMIT;
  DBMS_OUTPUT.PUT_LINE('Procesadas OK: ' || v_ok || '  Con error: ' || v_error);
END;
/
```

Claves: cursor **explícito** con `FOR UPDATE` para bloquear las filas leídas; bloque `BEGIN...EXCEPTION...END` **anidado dentro del bucle** para aislar el fallo de una fila sin romper el `LOOP`; `SAVEPOINT`/`ROLLBACK TO` deshace solo los cambios de esa factura (el `INSERT` en el log se ejecuta *después* del rollback al savepoint, por lo que sobrevive); excepción con nombre (`e_saldo_insuf`) para el caso de negocio, más `NO_DATA_FOUND` y `WHEN OTHERS` con `SQLERRM` como red de seguridad; **un único `COMMIT`** al final para no fragmentar la transacción.

---

### Caso práctico 4 — Cálculo de capacidad y elección de nivel RAID

**Enunciado.** Se dispone de 8 discos de 2 TB (16 TB brutos) para un servidor de base de datos transaccional que requiere tolerancia a fallos y buen rendimiento de escritura, con un mínimo de 6 TB útiles.

**Resolución.**

| RAID | Capacidad útil | Discos que tolera fallar | Penalización de escritura* |
|---|---|---|---|
| RAID 5 (n−1) | (8−1)×2 = **14 TB** | 1 disco | ×4 (lectura dato+paridad, escritura dato+paridad) |
| RAID 6 (n−2) | (8−2)×2 = **12 TB** | 2 discos | ×6 |
| RAID 10 (n/2) | (8/2)×2 = **8 TB** | hasta 4, si es uno por cada pareja espejada | ×2 |

*Penalización: nº de operaciones de E/S físicas por cada escritura lógica.

Cálculo de IOPS efectivas (ejemplo, discos de 150 IOPS aleatorias c/u, 8 discos → 1.200 IOPS brutas):
- RAID 10: 1.200 / 2 = **600 IOPS** efectivas de escritura.
- RAID 5: 1.200 / 4 = 300 IOPS.
- RAID 6: 1.200 / 6 = 200 IOPS.

**Recomendación:** aunque RAID 5 y RAID 6 ofrecen más capacidad útil, ambas superan holgadamente el mínimo de 6 TB solo con RAID 10 (8 TB), que además da el doble/triple de IOPS efectivas para escritura y una reconstrucción tras fallo mucho más rápida y menos arriesgada (sin necesidad de recalcular paridad sobre discos grandes, donde el riesgo de URE durante el rebuild de RAID 5 es significativo). Para una BD transaccional se elige **RAID 10**.

---

### Caso práctico 5 — Diseño de subnetting IPv4 (VLSM) para una sede CARM

**Enunciado.** Se asigna a una sede el bloque `10.50.0.0/24`. Departamentos y hosts necesarios: Atención al público/Registro (110), Administración (60), Informática/Servidores (25), Wifi invitados (14).

**Resolución (VLSM, de mayor a menor tamaño):**

| Departamento | Hosts necesarios | Máscara | Red | Rango utilizable | Broadcast |
|---|---|---|---|---|---|
| Atención al público | 110 | /25 (126 hosts) | 10.50.0.0/25 | 10.50.0.1 – 10.50.0.126 | 10.50.0.127 |
| Administración | 60 | /26 (62 hosts) | 10.50.0.128/26 | 10.50.0.129 – 10.50.0.190 | 10.50.0.191 |
| Informática | 25 | /27 (30 hosts) | 10.50.0.192/27 | 10.50.0.193 – 10.50.0.222 | 10.50.0.223 |
| Wifi invitados | 14 | /28 (14 hosts) | 10.50.0.224/28 | 10.50.0.225 – 10.50.0.238 | 10.50.0.239 |
| *Reserva/enlaces* | — | /28 libre | 10.50.0.240/28 | — | — |

Método: se ordenan los requisitos de mayor a menor; para cada uno se calcula la máscara más ajustada tal que `2^h − 2 ≥ hosts_necesarios`; cada bloque arranca donde termina el anterior. El bloque `10.50.0.240/28` queda libre para crecimiento o enlaces punto a punto (p. ej. /30 hacia el router).

---

### Caso práctico 6 — RGPD ante una brecha de seguridad en un organismo público

**Enunciado.** Un ransomware compromete un servidor de un organismo de la CARM con expedientes de dependencia (nombre, DNI y **datos de salud**, categoría especial del art. 9 RGPD). ¿Qué obligaciones y plazos aplican?

**Resolución.**

1. **Calificación del hecho**: es una "violación de la seguridad de los datos personales" (art. 4.12 RGPD) que compromete confidencialidad e integridad; al incluir datos de salud, el riesgo para los derechos y libertades de los afectados se presume **alto**.
2. **Notificación a la autoridad de control** (AEPD, al no existir agencia autonómica propia en la Región de Murcia): sin dilación indebida y, a más tardar, en **72 horas** desde que se tuvo constancia (art. 33 RGPD), salvo que sea improbable que exista riesgo. Si no se dispone de toda la información puede notificarse **por fases** (art. 33.4). Si se supera el plazo, debe justificarse el retraso.
   Contenido mínimo (art. 33.3): naturaleza de la brecha, categorías y nº aproximado de afectados/registros, datos de contacto del DPO, consecuencias probables, medidas adoptadas o propuestas.
3. **Comunicación a los interesados** (art. 34): obligatoria porque hay alto riesgo (datos de salud), en lenguaje claro y sencillo, salvo que concurra alguna excepción: datos protegidos con medidas técnicas que los hagan ininteligibles (p. ej. cifrados), medidas posteriores que eliminen el alto riesgo, o esfuerzo desproporcionado (en cuyo caso, comunicación pública equivalente).
4. **Registro interno** de la brecha (art. 33.5), obligatorio exista o no notificación externa, documentando hechos, efectos y medidas correctoras.
5. **Doble canal por tratarse de AAPP sujeta al ENS** (RD 311/2022): además del cauce RGPD, debe notificarse el incidente de seguridad conforme a la Instrucción Técnica de Seguridad de Notificación de Incidentes, a través de la red de CSIRT de referencia (CCN-CERT/INCIBE-CERT), según su nivel de criticidad.
6. **Papel del DPO**: asesora al responsable, es el punto de contacto con la AEPD y los interesados, y supervisa el cumplimiento del plazo.
7. **Medidas técnicas posteriores**: aislamiento del sistema afectado, análisis forense, rotación de credenciales, restauración desde copia de seguridad verificada, parcheo de la vulnerabilidad explotada, revisión del plan de continuidad.
8. **Régimen sancionador**: al ser Administración Pública, conforme al art. 77 LOPDGDD, la AEPD no impone multa económica, sino que dicta resolución proponiendo medidas correctoras a adoptar en un plazo determinado (sin perjuicio de la posible responsabilidad disciplinaria del personal implicado).

---

### Caso práctico 7 — Fragmento HTML + JavaScript consumiendo una API JSON

**Enunciado.** Página que, al cargar, consume `GET https://api.ejemplo.carm.es/expedientes` (devuelve un array `[{id, titulo, estado}, ...]`) y vuelca el resultado en una tabla, controlando errores de red o de formato.

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Listado de expedientes</title>
</head>
<body>
  <h1>Expedientes</h1>
  <table id="tablaExpedientes" border="1">
    <thead><tr><th>ID</th><th>Título</th><th>Estado</th></tr></thead>
    <tbody></tbody>
  </table>
  <p id="mensajeError" style="color:red;"></p>

  <script>
    async function cargarExpedientes() {
      try {
        const respuesta = await fetch('https://api.ejemplo.carm.es/expedientes');
        if (!respuesta.ok) {
          throw new Error(`Error HTTP: ${respuesta.status}`);
        }
        const expedientes = await respuesta.json();
        const cuerpoTabla = document.querySelector('#tablaExpedientes tbody');
        expedientes.forEach(exp => {
          const fila = document.createElement('tr');
          fila.innerHTML = `<td>${exp.id}</td><td>${exp.titulo}</td><td>${exp.estado}</td>`;
          cuerpoTabla.appendChild(fila);
        });
      } catch (error) {
        document.getElementById('mensajeError').textContent =
          'No se pudieron cargar los expedientes: ' + error.message;
      }
    }
    document.addEventListener('DOMContentLoaded', cargarExpedientes);
  </script>
</body>
</html>
```

**Explicación línea a línea (bloque script):**
- `async function cargarExpedientes()`: función asíncrona; permite usar `await` para esperar promesas sin bloquear el hilo principal.
- `await fetch(...)`: lanza la petición HTTP GET; `fetch` **no** rechaza la promesa ante códigos de error HTTP (4xx/5xx), solo ante fallos de red — por eso se comprueba `respuesta.ok` a mano.
- `if (!respuesta.ok) throw new Error(...)`: `respuesta.ok` es `true` solo si el status está en el rango 200-299; en caso contrario se fuerza el salto al `catch`.
- `await respuesta.json()`: parsea el cuerpo como JSON; si el cuerpo no es JSON válido, esta promesa se rechaza y el control pasa igualmente al `catch`.
- `document.querySelector('#tablaExpedientes tbody')`: referencia al `<tbody>` donde se insertarán las filas.
- `expedientes.forEach(...)`: recorre el array; por cada elemento crea una fila `<tr>` y la rellena mediante *template literals*.
- `cuerpoTabla.appendChild(fila)`: inserta la fila en el DOM.
- `catch (error)`: captura tanto errores de red (fetch rechazada) como el `Error` lanzado manualmente o el fallo de `json()`, y muestra el mensaje en el párrafo de error.
- `document.addEventListener('DOMContentLoaded', cargarExpedientes)`: garantiza que el DOM esté construido antes de manipularlo, sin depender de dónde se cargue el `<script>`.

---

## 2. Test de autoevaluación (30 preguntas)

**1.** En un servidor Linux con systemd se ejecuta `journalctl -u nginx.service --since "1 hour ago" -p err`. ¿Qué muestra?
a) Todas las unidades systemd relacionadas con nginx en la última hora
b) Los mensajes de log de nginx.service con prioridad error o superior, de la última hora
c) El estado actual (activo/inactivo) del servicio con su PID
d) Reinicia nginx si lleva más de una hora sin responder

**2.** En Windows Server, dos servidores DHCP se configuran en modo Failover "Load balance" 50-50. Si el primario deja de responder:
a) Los clientes quedan sin IP hasta reconfiguración manual
b) El secundario asume el 100% de las peticiones sobre el mismo ámbito replicado, protegido por el MCLT frente a duplicados
c) El secundario solo puede renovar concesiones existentes
d) Hay que reiniciar el servicio DHCP en el secundario manualmente

**3.** ¿Qué rol FSMO es único a nivel de bosque, no de dominio?
a) RID Master
b) PDC Emulator
c) Infrastructure Master
d) Schema Master

**4.** Un cliente de correo usa IMAP4 sobre el puerto 993. ¿Qué lo diferencia fundamentalmente de POP3?
a) IMAP cifra siempre de extremo a extremo y POP3 nunca
b) IMAP mantiene los mensajes sincronizados y organizados en carpetas en el servidor (accesible desde varios dispositivos); POP3 está pensado para descargarlos, habitualmente eliminándolos del servidor
c) POP3 exige autenticación e IMAP no
d) IMAP solo admite TLS y POP3 nunca lo admite

**5.** Un portátil con Windows 10 Pro no dispone de TPM. ¿Qué se requiere para activar BitLocker?
a) No es posible sin TPM
b) Habilitar por GPO "Permitir BitLocker sin un TPM compatible" y usar una unidad USB como clave de inicio
c) Actualizar a Windows 10 Enterprise
d) Usar EFS en su lugar

**6.** En la arquitectura de una instancia Oracle, ¿qué componente cachea los bloques de datos leídos de disco?
a) PGA
b) Redo Log Buffer
c) Database Buffer Cache (dentro de la SGA)
d) Shared Pool

**7.** Sobre InnoDB frente a MyISAM en MySQL:
a) InnoDB no soporta transacciones ni claves foráneas
b) InnoDB soporta transacciones ACID, integridad referencial y bloqueo a nivel de fila; MyISAM no soporta transacciones y bloquea a nivel de tabla
c) MyISAM es el motor recomendado desde MySQL 5.5
d) InnoDB no soporta recuperación ante caídas

**8.** En PostgreSQL, ¿qué recupera el espacio de las tuplas muertas generadas por MVCC?
a) REINDEX
b) VACUUM (y el proceso automático autovacuum)
c) ANALYZE
d) CHECKPOINT

**9.** Dado:
```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN TRAN;
UPDATE Cuentas SET Saldo = Saldo - 100 WHERE IdCuenta = 1;
UPDATE Cuentas SET Saldo = Saldo + 100 WHERE IdCuenta = 2;
COMMIT TRAN;
```
¿Qué garantiza READ COMMITTED frente a otras transacciones?
a) Evita siempre lecturas fantasma
b) Impide leer datos modificados y no confirmados (dirty reads), pero no garantiza lecturas repetibles
c) Bloquea la tabla completa hasta el COMMIT
d) Equivale a SNAPSHOT con versionado de filas

**10.** Diferencia principal entre hipervisor Tipo 1 y Tipo 2:
a) El Tipo 1 se ejecuta directamente sobre el hardware sin SO anfitrión; el Tipo 2 se ejecuta como aplicación sobre un SO ya instalado
b) El Tipo 2 siempre rinde más
c) El Tipo 1 no permite migración en caliente
d) No hay diferencia funcional

**11.** Diferencia fundamental entre un NAS (NFS/SMB) y una SAN (iSCSI/FC):
a) El NAS opera a nivel de bloque y la SAN a nivel de fichero
b) El NAS da acceso a nivel de fichero; la SAN da acceso a nivel de bloque, como un disco local para el servidor
c) Son idénticos, solo cambia el cableado
d) El NAS requiere fabric dedicado igual que Fibre Channel

**12.** Según TIA/EIA-568, longitud máxima recomendada de un canal de cobre UTP horizontal:
a) 100 metros (90 m de cable + hasta 10 m de latiguillos)
b) 500 metros
c) 1000 metros
d) 185 metros

**13.** El estándar IEEE 802.1Q define:
a) La agregación de enlaces (LACP)
b) El etiquetado de tramas Ethernet para VLANs sobre un enlace troncal
c) La autenticación basada en puertos (802.1X)
d) El Wi-Fi 6

**14.** Dada la red 172.20.64.0/20, ¿cuántas subredes /24 se obtienen y cuántos hosts utilizables tiene cada una?
a) 16 subredes /24, 254 hosts cada una
b) 8 subredes /24, 510 hosts cada una
c) 256 subredes /24, 254 hosts cada una
d) 4 subredes /24, 1022 hosts cada una

**15.** ¿Qué representa `fe80::1a2b:3c4d:5e6f:7a8b`?
a) Una dirección multicast
b) Una dirección link-local (fe80::/10), no enrutable fuera del segmento, autogenerada en cada interfaz
c) El equivalente a 127.0.0.1
d) Una dirección global unicast asignada por el ISP

**16.** Un navegador solicita `http://www.carm.es` y recibe HTTP 301. ¿Qué indica?
a) El recurso no existe
b) Redirección permanente a otra URL indicada en la cabecera Location
c) Error interno del servidor
d) Acceso prohibido

**17.** Según ITIL, diferencia esencial entre Gestión de Incidencias y Gestión de Problemas:
a) Son el mismo proceso
b) Incidencias busca restaurar el servicio cuanto antes; Problemas busca la causa raíz para evitar que se repitan
c) Problemas se ocupa de incidencias de bajo impacto
d) Incidencias solo aplica a hardware

**18.** ISO/IEC 20000 está orientada a:
a) La seguridad de la información exclusivamente
b) Certificar un Sistema de Gestión del Servicio de TI, alineado con las buenas prácticas de ITIL
c) La gestión de proyectos software, alternativa a PRINCE2
d) Sustituir a ISO 9001 en calidad de desarrollo

**19.** En PRINCE2, el órgano ante el que responde el Jefe de Proyecto y que toma las decisiones clave es:
a) El Comité de Dirección del Proyecto (Project Board)
b) El equipo de aseguramiento de calidad
c) El Product Owner
d) La PMO

**20.** En Scrum, ¿qué evento inspecciona el Incremento y adapta el Product Backlog con los interesados?
a) Daily Scrum
b) Sprint Planning
c) Sprint Review
d) Sprint Retrospective

**21.** Dado el pseudocódigo:
```
class Vehiculo { method arrancar() { imprimir("motor genérico") } }
class Coche extends Vehiculo { method arrancar() { imprimir("motor de coche") } }
Vehiculo v = new Coche();
v.arrancar();
```
¿Qué se imprime y qué principio se aplica?
a) "motor genérico"; encapsulación
b) "motor de coche"; polimorfismo (sobrescritura y enlace dinámico)
c) Error de compilación
d) Ambas líneas se imprimen

**22.** ¿Qué diagrama UML muestra la interacción entre objetos a lo largo del tiempo y el orden de los mensajes?
a) Diagrama de clases
b) Diagrama de casos de uso
c) Diagrama de secuencia
d) Diagrama de despliegue

**23.** Analice:
```sql
BEGIN
  FOR r IN (SELECT id, saldo FROM cuentas WHERE saldo < 0) LOOP
    UPDATE cuentas SET saldo = 0 WHERE id = r.id;
  END LOOP;
  COMMIT;
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    RAISE;
END;
```
¿Qué tipo de cursor es y qué ocurre ante una excepción no controlada específicamente?
a) Cursor explícito con DECLARE CURSOR; si falla, continúa con la siguiente fila
b) Cursor implícito de un "cursor FOR loop" (Oracle lo abre/recorre/cierra); ante cualquier excepción se deshace toda la transacción y se relanza
c) Es una colección VARRAY, no un cursor
d) Es un REF CURSOR para devolver resultados a una app externa

**24.** En Oracle Forms, ¿cuándo se dispara WHEN-VALIDATE-ITEM?
a) Antes de abrir el formulario por primera vez
b) Cuando el cursor sale de un ítem y Forms va a validar su contenido
c) Solo al pulsar el botón de guardar
d) Cuando se produce un error de BD no controlado

**25.** Dado:
```javascript
fetch('/api/expedientes')
  .then(response => response.json())
  .then(data => console.log(data.length))
  .catch(error => console.error('Error:', error));
```
¿Qué asume y qué pasa si el servidor devuelve JSON mal formado?
a) Asume un array (o length); si el JSON es inválido, `response.json()` rechaza su promesa y se ejecuta `.catch()`
b) fetch lanza una excepción síncrona que detiene el script
c) `data.length` será siempre undefined sin error
d) fetch valida el JSON contra un esquema antes de resolver

**26.** Dado:
```java
try {
  int[] datos = {1, 2, 3};
  System.out.println(datos[5]);
} catch (ArithmeticException e) {
  System.out.println("Error aritmético");
} finally {
  System.out.println("Fin");
}
```
¿Qué ocurre?
a) Se imprime "Error aritmético" y "Fin"
b) Se imprime solo "Fin"
c) Se lanza ArrayIndexOutOfBoundsException, no capturada por ese catch; se ejecuta "Fin" en el finally y luego la excepción se propaga
d) No compila por falta de catch genérico

**27.** Según el art. 33 RGPD, ante una violación de seguridad de datos personales, la notificación a la autoridad de control debe hacerse:
a) En 30 días naturales desde que se tuvo constancia
b) Sin dilación indebida y, a más tardar, en 72 horas, salvo que sea improbable el riesgo para los derechos y libertades
c) Solo si afecta a más de 1.000 interesados
d) Solo si los interesados lo solicitan

**28.** Un firewall "stateful inspection" se diferencia de uno de filtrado simple (stateless) en que:
a) Solo filtra en capa de aplicación
b) Mantiene una tabla de estados de conexiones activas, permitiendo automáticamente el tráfico de retorno de una conexión legítima ya establecida
c) No filtra por puertos ni IPs
d) Es siempre software, nunca hardware dedicado

**29.** En una PKI, ¿qué papel desempeña la Autoridad de Certificación (CA)?
a) Almacena las claves privadas de todos los usuarios para recuperarlas
b) Emite y firma certificados digitales, vinculando clave pública e identidad, y gestiona su ciclo de vida (emisión, renovación, revocación por CRL/OCSP)
c) Cifra todo el correo de la organización
d) Sustituye a la firma electrónica cualificada

**30.** Según el ENS (RD 311/2022), un sistema categorizado como ALTA implica:
a) No requiere medidas adicionales frente a BÁSICA
b) Las consecuencias de un incidente tendrían un efecto muy grave, exigiéndose el conjunto de medidas más exigente del Anexo II
c) Solo aplica a sistemas de defensa nacional
d) Implica automáticamente certificación ISO 27001

### Soluciones

1. **b** — `-p err` filtra por prioridad; `--since` acota el intervalo temporal; `-u` selecciona la unidad.
2. **b** — El MCLT (Maximum Client Lead Time) evita que ambos servidores asignen la misma IP durante el failover.
3. **d** — Schema Master y Domain Naming Master son de bosque; los otros tres son por dominio.
4. **b** — IMAP sincroniza estado/carpetas en servidor; POP3 es orientado a descarga.
5. **b** — Requiere la directiva de GPO específica más una unidad USB de arranque.
6. **c** — El Database Buffer Cache forma parte de la SGA y cachea bloques de datos.
7. **b** — Es la diferencia estándar entre ambos motores.
8. **b** — VACUUM/autovacuum limpian las tuplas obsoletas de MVCC.
9. **b** — READ COMMITTED evita dirty reads pero permite non-repeatable reads y phantom reads.
10. **a** — Definición estándar de hipervisor bare-metal frente a hosted.
11. **b** — NAS = nivel fichero; SAN = nivel bloque.
12. **a** — Canal máximo de 100 m según TIA/EIA-568.
13. **b** — 802.1Q = VLAN tagging; 802.1X = autenticación; 802.3ad = LACP; 802.11 = Wi-Fi.
14. **a** — 2^(24-20)=16 subredes; 2^8-2=254 hosts utilizables cada una.
15. **b** — Prefijo fe80::/10 reservado para direcciones link-local.
16. **b** — 301 = Moved Permanently.
17. **b** — Incidencias = restauración rápida del servicio; Problemas = causa raíz.
18. **b** — ISO/IEC 20000 certifica el SGS de TI, alineada con ITIL.
19. **a** — El Project Board es el órgano de decisión ante el que responde el Project Manager.
20. **c** — Sprint Review implica a los stakeholders e inspecciona el incremento; la Retrospectiva es interna del equipo.
21. **b** — Enlace dinámico: se invoca el método sobrescrito en la clase real del objeto (Coche), no el de la referencia declarada (Vehiculo).
22. **c** — El diagrama de secuencia representa el orden temporal de mensajes entre objetos.
23. **b** — Es un cursor FOR loop implícito; cualquier excepción no capturada específicamente provoca el ROLLBACK global y el RAISE la repropaga.
24. **b** — Se dispara al validar el contenido de un ítem, típicamente al perder el foco.
25. **a** — `response.json()` puede rechazar la promesa si el cuerpo no es JSON válido, cayendo en `.catch`.
26. **c** — El catch solo captura ArithmeticException; el finally siempre se ejecuta antes de que la excepción no capturada se propague.
27. **b** — Plazo de 72 horas desde el art. 33.1 RGPD, con la salvedad de riesgo improbable.
28. **b** — El seguimiento de estado de conexión es la característica distintiva de "stateful inspection".
29. **b** — La CA emite, firma y gestiona el ciclo de vida de los certificados digitales.
30. **b** — La categoría ALTA del ENS exige el nivel más exigente de medidas de seguridad del Anexo II ante un impacto muy grave.
