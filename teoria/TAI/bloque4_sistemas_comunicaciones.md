# TAI — Bloque IV: Sistemas y comunicaciones (versión ampliada)

> Bloque de máximo peso en el examen: entra en el test general Y es uno de los dos supuestos prácticos posibles (junto al Bloque III). Desarrollo exhaustivo por tema.

## Tema 1. Administración del Sistema operativo y software de base. Actualización, mantenimiento y reparación del sistema operativo.

La administración del sistema operativo constituye la base operativa sobre la que se sustentan los servicios de cualquier organización. En el contexto de la Administración General del Estado, esta labor está condicionada por el Esquema Nacional de Seguridad (ENS, Real Decreto 311/2022), que exige gestión de vulnerabilidades, trazabilidad de cambios y disponibilidad de los sistemas críticos.

### Administración de sistemas Linux: gestores de paquetes

Cada familia de distribuciones implementa su propio sistema de gestión de paquetes, con una capa de bajo nivel (instala/desinstala paquetes individuales) y una capa de alto nivel (resuelve dependencias y repositorios).

**Debian/Ubuntu — dpkg y APT.** `dpkg` es la herramienta de bajo nivel que instala ficheros `.deb`:

```bash
dpkg -i paquete.deb
dpkg -l | grep openssh
dpkg -L openssh-server        # lista ficheros instalados por el paquete
```

APT resuelve dependencias y repositorios (`/etc/apt/sources.list` y `/etc/apt/sources.list.d/`):

```bash
apt update && apt list --upgradable
apt full-upgrade -y
apt install nginx=1.18.0-6ubuntu14.4
apt-mark hold nginx            # evita que se actualice en upgrades futuros
apt autoremove --purge
```

**RedHat/CentOS/Fedora — RPM y DNF/YUM.** `rpm` es el equivalente de bajo nivel a dpkg; `dnf` (sucesor de `yum` desde RHEL 8) resuelve dependencias:

```bash
rpm -qa | grep httpd
rpm -qi kernel
dnf check-update
dnf update --security          # solo parches de seguridad
dnf history                    # traza transacciones, permite dnf history undo <id>
dnf versionlock add nginx
```

**SUSE — zypper.** Similar filosofía, con gestión de patrones y "patches" diferenciados de paquetes normales:

```bash
zypper refresh
zypper list-updates
zypper patch                   # instala solo los parches oficiales del vendor
zypper install -t pattern kvm_server
```

**Arch — pacman.** Modelo rolling release, sincronización y caché local:

```bash
pacman -Syu
pacman -Qdt                    # paquetes huérfanos (dependencias no reclamadas)
pacman -Sc                     # limpia caché de paquetes descargados
```

### systemd: unidades, systemctl y journalctl

`systemd` es el sistema de inicio (init) y gestor de servicios de la práctica totalidad de distribuciones modernas (sustituye a SysVinit/Upstart). Organiza el sistema en **unidades**, ficheros de texto ubicados en `/etc/systemd/system/` (administrador), `/usr/lib/systemd/system/` (paquetes) y `/run/systemd/system/` (runtime), con precedencia decreciente en ese orden.

- **`.service`**: define un proceso demonio. Secciones típicas `[Unit]` (metadatos, dependencias `Requires=`, `After=`), `[Service]` (`ExecStart=`, `Restart=on-failure`, `Type=notify|simple|forking`) y `[Install]` (`WantedBy=multi-user.target`).
- **`.timer`**: sustituye a cron para tareas programadas, con `OnCalendar=` o `OnBootSec=`; siempre va emparejado a un `.service` homónimo.
- **`.mount`** / **`.automount`**: puntos de montaje gestionados declarativamente (alternativa a `/etc/fstab`).
- **`.socket`**: activación por socket (systemd escucha el puerto y arranca el servicio bajo demanda, patrón usado por `sshd.socket` o `cups.socket`).

Comandos habituales:

```bash
systemctl status sshd
systemctl enable --now nginx.service
systemctl daemon-reload                  # tras editar un unit file
systemctl mask bluetooth.service         # bloquea el arranque incluso manual
systemctl list-units --type=timer --all
systemctl edit nginx.service             # crea un "drop-in" en /etc/systemd/system/nginx.service.d/
```

`journalctl` consulta el diario binario de systemd (`journald`):

```bash
journalctl -u nginx.service --since "2026-08-27 08:00" --until now
journalctl -k -b -1              # mensajes de kernel del arranque anterior
journalctl -f                    # seguimiento en tiempo real, equivalente a tail -f
journalctl --disk-usage
journalctl --vacuum-time=7d      # purga entradas de más de 7 días
```

### Gestión de logs: logrotate, rsyslog y journald

Existen dos modelos convivientes en Linux. **journald** almacena logs en formato binario indexado (`/var/log/journal/` si es persistente, configurable en `/etc/systemd/journald.conf` con `Storage=persistent`), con retención controlada por `SystemMaxUse=`. **rsyslog** (o syslog-ng) es el demonio syslog clásico, que escribe texto plano en `/var/log/` según reglas de `/etc/rsyslog.conf` (facility.priority → destino, p. ej. `mail.* /var/log/maillog`) y puede reenviar logs a un colector centralizado (SIEM) vía TCP/UDP 514 o RELP.

`logrotate` (ejecutado vía `.timer`/cron diario) rota los ficheros de texto plano que genera rsyslog para evitar que crezcan indefinidamente, según reglas en `/etc/logrotate.d/`:

```
/var/log/nginx/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    sharedscripts
    postrotate
        systemctl reload nginx > /dev/null 2>&1 || true
    endscript
}
```

journald no necesita logrotate porque autogestiona su propio espacio, pero en entornos regulados por el ENS suele configurarse forwarding a rsyslog (`ForwardToSyslog=yes`) para centralizar la trazabilidad exigida en auditoría.

### Administración de Windows Server

**Windows Update y WSUS.** Windows Server Update Services permite desplegar un punto central que descarga actualizaciones de Microsoft Update y las distribuye internamente, con aprobación manual por grupos de equipos (evita que un parche defectuoso se despliegue sin control). Se gestiona vía consola WSUS o PowerShell (`Get-WsusUpdate`, `Approve-WsusUpdate`). El cliente se apunta mediante GPO (`Configurar el servicio de Windows Update`, ruta del servidor de intranet).

**PowerShell DSC (Desired State Configuration).** Modelo declarativo idempotente para forzar el estado de un servidor (roles instalados, ficheros, servicios en ejecución):

```powershell
Configuration WebServerConfig {
    Node "SRV-WEB01" {
        WindowsFeature IIS {
            Ensure = "Present"
            Name   = "Web-Server"
        }
        Service W3SVC {
            Name  = "W3SVC"
            State = "Running"
            DependsOn = "[WindowsFeature]IIS"
        }
    }
}
WebServerConfig -OutputPath ".\DSC"
Start-DscConfiguration -Path ".\DSC" -Wait -Verbose
```

**Server Manager** centraliza la instalación de roles y características (Add Roles and Features Wizard), equivalente por PowerShell a:

```powershell
Install-WindowsFeature -Name AD-Domain-Services, DNS -IncludeManagementTools
Get-WindowsFeature | Where-Object Installed
```

### Automatización de infraestructura

La gestión manual de flotas de servidores no escala; las herramientas de configuration management aplican el principio de infraestructura como código (IaC).

```yaml
---
- hosts: webservers
  become: yes
  tasks:
    - name: Instalar nginx
      apt:
        name: nginx
        state: latest
        update_cache: yes
    - name: Copiar configuración
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: reload nginx
  handlers:
    - name: reload nginx
      service:
        name: nginx
        state: reloaded
```

| Característica | Ansible | Puppet | Chef |
|---|---|---|---|
| Arquitectura | Sin agente (SSH/WinRM) | Agente-maestro (o agentless con Bolt) | Agente-servidor |
| Lenguaje | YAML declarativo | DSL propio (Puppet Manifest) | Ruby (DSL interno) |
| Modelo | Push | Pull (agente consulta periódicamente) | Pull |
| Curva de aprendizaje | Baja | Media | Alta |
| Idempotencia | Sí (módulos) | Sí (nativa, motor de convergencia) | Sí (recursos) |
| Caso de uso típico | Despliegues puntuales, orquestación | Gestión continua de flotas grandes | Entornos DevOps complejos, Cloud-native |

### Ciclo de gestión de parches

El ciclo formal comprende: **1) Inventario** de activos (SO, versión, paquetes instalados) mediante CMDB o herramientas como Lansweeper/OCS Inventory; **2) Identificación de vulnerabilidades** contra bases CVE (Common Vulnerabilities and Exposures) mediante escáneres (Nessus, OpenVAS); **3) Priorización** con CVSS (Common Vulnerability Scoring System), que asigna una puntuación de 0.0 a 10.0 según vectores de ataque, complejidad, privilegios requeridos e impacto en confidencialidad/integridad/disponibilidad — rangos: 0.1–3.9 Bajo, 4.0–6.9 Medio, 7.0–8.9 Alto, 9.0–10.0 Crítico; **4) Ventana de mantenimiento**, franja horaria planificada y comunicada (habitualmente fuera de horario productivo) para minimizar el impacto; **5) Despliegue** controlado, primero en entorno de pre-producción; **6) Verificación** post-parcheo; **7) Rollback** si el parche introduce regresiones, mediante snapshots de VM, puntos de restauración, o desinstalación dirigida (`dnf history undo`, `apt remove <paquete>=<versión_anterior>`, o `wusa /uninstall /kb:XXXXXXX` en Windows).

### Proceso de arranque

El arranque tradicional BIOS/MBR ejecuta el **POST** (Power-On Self-Test), localiza el dispositivo de arranque, lee el **MBR** (512 bytes, primer sector del disco: 446 bytes de código de arranque, tabla de particiones de 64 bytes con máximo 4 particiones primarias, firma 0x55AA) y ejecuta el bootloader de primera etapa. El esquema moderno **UEFI/GPT** sustituye la BIOS por un firmware con su propio entorno de ejecución, lee la **ESP** (EFI System Partition, FAT32) y ejecuta directamente el gestor de arranque (`.efi`), sin límite práctico de particiones (GPT usa GUID y tabla replicada al final del disco para redundancia).

En Linux, **GRUB2** es el bootloader dominante, configurado en `/etc/default/grub` y generado en `/boot/grub2/grub.cfg` (BIOS) o `/boot/efi/EFI/<distro>/grub.cfg` (UEFI) mediante `grub2-mkconfig` / `update-grub`. **systemd-boot** (antes gummiboot) es una alternativa minimalista solo-UEFI, sin scripting, con entradas en `/boot/loader/entries/*.conf`.

En Windows, el **Windows Boot Manager** (`bootmgr`/`bootmgfw.efi`) lee la **BCD** (Boot Configuration Data, sustituye a `boot.ini` desde Vista), gestionable con `bcdedit`:

```powershell
bcdedit /enum
bcdedit /set {default} bootstatuspolicy ignoreallfailures
bcdedit /timeout 10
```

### Reparación de arranque

**Linux**: si GRUB o el kernel fallan, se accede a **modo rescate** (single-user, `systemd.unit=rescue.target` como parámetro de arranque) o se arranca desde un live-USB para hacer **chroot** al sistema instalado:

```bash
mount /dev/sda2 /mnt
mount /dev/sda1 /mnt/boot/efi
for d in proc sys dev; do mount --bind /$d /mnt/$d; done
chroot /mnt /bin/bash
grub2-install /dev/sda
grub2-mkconfig -o /boot/grub2/grub.cfg
dracut --force --regenerate-all   # reconstruye el initramfs si falta un módulo/driver
```

El **initramfs**, generado por `dracut` (RHEL/SUSE) o `update-initramfs` (Debian), es un sistema de ficheros temporal cargado en RAM que monta el root real y carga los módulos necesarios (LVM, RAID, cifrado) antes del `pivot_root`.

**Windows**: el **WinRE** (Windows Recovery Environment) se invoca con tres fallos de arranque consecutivos o `shutdown /r /o`. Desde el símbolo del sistema de WinRE:

```powershell
bootrec /fixmbr
bootrec /fixboot
bootrec /scanos
bootrec /rebuildbcd
sfc /scannow                       # verifica y repara ficheros de sistema protegidos
DISM /Online /Cleanup-Image /RestoreHealth   # repara la imagen WIM subyacente que usa sfc
```

`DISM` repara el almacén de componentes (`WinSxS`) del que depende `sfc`; si `sfc` falla por corrupción de la imagen base, hay que ejecutar primero `DISM /RestoreHealth`.

### Firmware, drivers, imágenes doradas y Packer

La actualización de **firmware** (BIOS/UEFI, controladoras RAID, BMC/iLO/iDRAC) y **drivers** debe gestionarse con el mismo rigor que el SO: versión certificada por el fabricante, ventana de mantenimiento y plan de rollback (firmware dual-bank en servidores empresariales). Las **imágenes doradas** (golden images) son plantillas de VM/contenedor pre-configuradas, parcheadas y hardenizadas que sirven de base estándar para despliegues, reduciendo drift de configuración. **Packer** (HashiCorp) automatiza la construcción reproducible de estas imágenes a partir de una plantilla declarativa (HCL/JSON) que define el builder (VMware, AWS AMI, Azure, QEMU) y los provisioners (scripts shell, Ansible) que instalan el software base.

### EOL/EOSL y su relación con el ENS

**EOL** (End of Life) marca el fin del desarrollo de nuevas funcionalidades; **EOSL** (End of Service Life / soporte extendido) marca el fin de los parches de seguridad. Mantener sistemas EOSL en producción constituye un incumplimiento directo del ENS, cuya medida `op.exp.4` (mantenimiento) exige aplicar actualizaciones de seguridad y `op.exp.2` exige gestión de configuración segura; un sistema sin soporte no puede parchearse frente a CVE nuevos, lo que en la categorización del ENS (Básica/Media/Alta) obliga a planes de migración documentados y, frecuentemente, a medidas compensatorias (segmentación de red, WAF) mientras se ejecuta la migración.

### Monitorización proactiva

**Nagios** (y su fork Icinga) usa un modelo de *checks* activos/pasivos con plugins que devuelven estados OK/WARNING/CRITICAL/UNKNOWN, orientado a alertar sobre disponibilidad. **Zabbix** añade recolección de métricas históricas, triggers con expresiones complejas y descubrimiento automático de red. **Prometheus** usa un modelo de *pull* sobre HTTP, con **Node Exporter** exponiendo métricas del SO en `:9100/metrics`:

```
node_filesystem_avail_bytes{device="/dev/sda1",mountpoint="/"} 8.4e+09
node_load1 0.42
node_memory_MemAvailable_bytes 3.1e+09
```

Estas métricas se consultan con PromQL (`rate(node_cpu_seconds_total[5m])`) y se visualizan típicamente en Grafana, con alertas gestionadas por Alertmanager.

### Trampas habituales de examen

- **`apt` vs `dpkg`** y **`dnf`/`yum` vs `rpm`**: dpkg/rpm operan sobre un paquete individual sin resolver dependencias; apt/dnf gestionan repositorios y dependencias. Confundir cuál "resuelve dependencias" es el error más frecuente.
- **journald vs rsyslog**: journald es binario, indexado y propio de systemd; rsyslog es texto plano y syslog clásico. `logrotate` rota ficheros de texto (rsyslog), **no** el journal, que se autogestiona con `--vacuum-*`.
- **sfc /scannow vs DISM**: sfc repara ficheros de sistema contra la caché local (`WinSxS`); si esa caché está corrupta, sfc no puede repararse a sí mismo y hace falta `DISM /RestoreHealth` primero. El examen suele plantear el orden correcto.
- **MBR/BIOS vs GPT/UEFI**: MBR limita a 4 particiones primarias y discos de 2 TiB; GPT no tiene esa limitación y requiere partición ESP FAT32. `bootrec /fixmbr` no tiene sentido en un sistema UEFI puro.
- **EOL vs EOSL**: EOL es fin de desarrollo funcional; EOSL es fin de soporte de seguridad. Un producto puede estar en EOL pero seguir recibiendo parches críticos durante su fase EOSL extendida — el examen explota esta distinción temporal.
- **CVSS**: puntuación de severidad de una vulnerabilidad (0–10), no debe confundirse con CVE, que es solo el identificador/catálogo de la vulnerabilidad en sí.

## Tema 2. Administración de bases de datos. Sistemas de almacenamiento y su virtualización. Políticas, sistemas y procedimientos de backup y su recuperación. Backup de sistemas físicos y virtuales. Virtualización de sistemas y virtualización de puestos de usuario.

### Administración de bases de datos: tuning y planes de ejecución

El ajuste de rendimiento (tuning) actúa sobre tres capas: parámetros del motor (memoria de buffer, work_mem, checkpoints), estadísticas del optimizador y diseño físico (índices, particionado). Sin estadísticas actualizadas (ANALYZE en PostgreSQL, UPDATE STATISTICS en SQL Server, DBMS_STATS en Oracle) el optimizador basado en costes (CBO) estima cardinalidades erróneas y elige planes subóptimos, típicamente un escaneo completo (Seq Scan/Table Scan) donde cabría un acceso por índice.

El plan de ejecución es la herramienta de diagnóstico principal. EXPLAIN muestra el plan estimado; EXPLAIN ANALYZE lo ejecuta y añade tiempos y filas reales, permitiendo detectar desviaciones de estimación:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT c.nombre, SUM(f.importe)
FROM facturas f JOIN clientes c ON c.id = f.cliente_id
WHERE f.fecha >= '2026-01-01'
GROUP BY c.nombre;

-- Salida relevante:
-- Hash Join (cost=120.5..980.2 rows=3200 width=48)
--   (actual time=1.2..15.8 rows=3150 loops=1)
--   Buffers: shared hit=210 read=45
--   -> Seq Scan on facturas f (cost=0.00..820.0 rows=3200 ...)
```

En Oracle el equivalente es `EXPLAIN PLAN FOR <sql>; SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);`; en SQL Server, `SET STATISTICS PROFILE ON` o el plan de ejecución real gráfico (Actual Execution Plan). Un plan con "rows estimadas" muy alejadas de "rows reales" indica estadísticas obsoletas o falta de histogramas.

### Gestión de índices y particionado de tablas

Los índices B-tree son el tipo por defecto para igualdad y rangos; los bitmap son eficientes en columnas de baja cardinalidad con consultas OLAP; los hash solo sirven para igualdad exacta. Un índice cubriente (covering index) incluye en sus columnas todo lo que necesita la consulta, evitando el acceso a la tabla (index-only scan). La fragmentación de índices por escrituras intensivas se corrige con REBUILD (reconstrucción completa, bloqueante u online según motor) o REORGANIZE (desfragmentación incremental).

El particionado divide una tabla grande en segmentos físicos manteniendo una interfaz lógica única, habilitando el "partition pruning": el optimizador descarta particiones que no pueden contener filas relevantes.

```sql
CREATE TABLE facturas (
  id BIGINT, cliente_id INT, fecha DATE, importe NUMERIC
) PARTITION BY RANGE (fecha);

CREATE TABLE facturas_2025 PARTITION OF facturas
  FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
CREATE TABLE facturas_2026 PARTITION OF facturas
  FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');
```

Existen también particionado por lista (valores discretos, ej. país) y por hash (distribución uniforme sin criterio natural de rango).

### Replicación de bases de datos

En maestro-esclavo (master-slave) las escrituras solo se aceptan en el nodo maestro y se propagan de forma asíncrona a réplicas de solo lectura, útil para escalar lecturas y como base de un failover manual. En maestro-maestro (multi-master) varios nodos aceptan escrituras simultáneas, lo que exige resolución de conflictos (last-write-wins, vectores de versión) y complica la consistencia.

Always On Availability Groups (SQL Server) agrupa bases de datos en un grupo de disponibilidad sobre un clúster de failover de Windows (WSFC), con réplicas en modo síncrono (compromiso garantizado, cero pérdida, mayor latencia) o asíncrono (menor latencia, posible pérdida de las últimas transacciones); el quórum del clúster decide el failover automático.

La streaming replication de PostgreSQL envía continuamente el WAL (Write-Ahead Log) del primario a los standbys:

```ini
# postgresql.conf en el primario
wal_level = replica
max_wal_senders = 10
wal_keep_size = 1GB

# pg_hba.conf en el primario
host replication replicador 10.0.0.0/24 scram-sha-256

# En el standby: standby.signal presente y postgresql.conf:
primary_conninfo = 'host=10.0.0.1 port=5432 user=replicador password=***'
```

Los replication slots evitan que el primario purgue WAL que un standby aún no ha consumido.

### Niveles de aislamiento transaccional

- **Read Uncommitted**: permite dirty read. T1 actualiza el saldo de una cuenta sin confirmar; T2 lee ese saldo modificado; T1 hace ROLLBACK; T2 ha basado su decisión en un dato que nunca existió realmente.
- **Read Committed**: evita dirty read pero permite non-repeatable read. T1 lee el precio de un producto (10 €); T2 lo actualiza a 12 € y confirma; T1 vuelve a leer el mismo producto dentro de su misma transacción y obtiene 12 €.
- **Repeatable Read**: fija los valores ya leídos pero permite phantom read. T1 ejecuta `SELECT COUNT(*) FROM pedidos WHERE cliente_id=5` y obtiene 3; T2 inserta un nuevo pedido de ese cliente y confirma; T1 repite la misma consulta y obtiene 4 filas "fantasma".
- **Serializable**: equivale a ejecutar las transacciones en serie mediante bloqueo de rango o detección de conflictos; evita las tres anomalías al coste de más abortos por serialización y menor concurrencia.

### Sistemas de almacenamiento: DAS, NAS y SAN

| Característica | DAS | NAS | SAN |
|---|---|---|---|
| Conexión | Directa al servidor (SATA/SAS/USB) | Red Ethernet, IP | Red dedicada (Fibre Channel o Ethernet iSCSI) |
| Protocolo | Bus de almacenamiento local | NFS, SMB/CIFS | FC (FCP), iSCSI |
| Nivel de acceso | Bloque | Archivo | Bloque |
| Compartición entre hosts | No (o muy limitada) | Sí, nativa | Sí, mediante LUNs |
| Latencia | Muy baja | Media (depende de red IP) | Baja (FC dedicada) |
| Escalabilidad | Baja | Alta | Muy alta |
| Coste | Bajo | Medio | Alto |
| Caso de uso típico | Servidor único, BD local de alto I/O | Ficheros compartidos, perfiles, backups | Clústeres, VMs, bases de datos críticas |

Una LUN (Logical Unit Number) es el volumen lógico que la cabina SAN presenta a un host como si fuera un disco físico. El zoning segmenta la red FC restringiendo qué HBA (iniciador) puede ver qué puerto de la cabina (destino): zoning por puerto (hard zoning, más seguro, ligado físicamente) o por WWN (soft zoning, más flexible). El multipathing (MPIO) mantiene varias rutas físicas redundantes entre host y cabina, aportando tolerancia a fallos de cable/HBA/switch y balanceo de carga de I/O.

### RAID

| Nivel | Mecanismo | Discos mín. | Capacidad útil | Tolerancia a fallos | Ejemplo (discos de 1 TB) |
|---|---|---|---|---|---|
| RAID 0 | Striping | 2 | n × T | Ninguna | 4 discos → 4 TB, sin redundancia |
| RAID 1 | Mirroring | 2 | (n/2) × T | 1 disco por par | 2 discos → 1 TB útil |
| RAID 5 | Striping + paridad distribuida | 3 | (n−1) × T | 1 disco | 4 discos → 3 TB |
| RAID 6 | Striping + doble paridad | 4 | (n−2) × T | 2 discos | 6 discos → 4 TB |
| RAID 10 | Mirror + stripe | 4 | (n/2) × T | 1 por cada par espejado | 4 discos → 2 TB |
| RAID 50 | RAID 5 en stripe | 6 | (n−g) × T (g = nº grupos) | 1 disco por grupo | 2 grupos de 4 discos (8 total) → 6 TB |
| RAID 60 | RAID 6 en stripe | 8 | (n−2g) × T | 2 discos por grupo | 2 grupos de 6 discos (12 total) → 8 TB |

RAID 5/6 penalizan la escritura por el cálculo de paridad (write penalty) y sufren mayor riesgo durante el rebuild con discos grandes (posibilidad de segundo fallo antes de terminar); RAID 10 evita ese problema a costa de aprovechamiento del 50%.

### Virtualización del almacenamiento

El thin provisioning asigna espacio bajo demanda: el volumen se presenta con capacidad "X" pero solo consume físicamente lo escrito, con riesgo de sobreaprovisionamiento (overcommit) del pool si no se monitoriza. El thick provisioning reserva toda la capacidad desde la creación, eager zeroed (cero-rellenado inmediato, mejor rendimiento inicial) o lazy zeroed (cero-rellenado bajo demanda en la primera escritura).

Un storage pool agrupa discos físicos heterogéneos en un espacio lógico del que se reparten LUNs o volúmenes virtuales. En Linux, LVM (Logical Volume Manager) implementa esta capa:

```bash
pvcreate /dev/sdb /dev/sdc
vgcreate vg_datos /dev/sdb /dev/sdc
lvcreate -L 500G -n lv_bbdd vg_datos
mkfs.xfs /dev/vg_datos/lv_bbdd
lvextend -L +200G /dev/vg_datos/lv_bbdd && xfs_growfs /dev/vg_datos/lv_bbdd
```

### Backup: RPO, RTO y tipos de copia

RPO (Recovery Point Objective) es la cantidad máxima de datos, medida en tiempo, que la organización asume perder. RTO (Recovery Time Objective) es el tiempo máximo aceptable de indisponibilidad tras el desastre. Ejemplo: backup completo diario a las 02:00; el fallo ocurre a las 14:00 → se pierden 12 horas de transacciones (RPO real = 12 h). Si el SLA exige RPO ≤ 1 h, un backup diario no basta: se requiere replicación continua o backups de log cada hora. Para el RTO, restaurar 2 TB a 100 MB/s tarda ≈ 5,5 horas; si el SLA exige RTO ≤ 1 h, se necesita un sitio en caliente o failover automático, no solo restauración desde cinta/backup.

Con una base de datos de 500 GB que cambia un 5 %/día (25 GB):
- **Completo diario**: 500 GB/día × 7 = 3,5 TB/semana; restauración = leer 500 GB (rápida, un único set).
- **Incremental** (respecto al último backup, sea completo o incremental): domingo 500 GB + 6 × 25 GB = 650 GB/semana; restaurar el viernes exige el completo + 5 incrementales encadenados (mayor tiempo y riesgo: si un incremental intermedio está corrupto, se pierde la cadena).
- **Diferencial** (respecto al último completo): domingo 500 GB + (25+50+75+100+125+150) = 1.025 GB/semana; restaurar el viernes exige solo completo + último diferencial (500+150 GB), más rápido que el incremental aunque ocupa más espacio en disco.

### Regla 3-2-1 y protección frente a ransomware

La regla 3-2-1 exige 3 copias de los datos (el original + 2 backups), en 2 soportes distintos, con 1 copia fuera de las instalaciones (offsite). La extensión 3-2-1-1-0 añade 1 copia offline o inmutable y 0 errores, es decir, verificación periódica mediante pruebas de restauración reales. La inmutabilidad WORM (Write Once Read Many, ej. S3 Object Lock, retención en cintas o snapshots inmutables) impide modificar o eliminar el backup durante el periodo de retención aunque un atacante obtenga credenciales de administrador, siendo la defensa clave frente a ransomware que cifra o borra deliberadamente las copias de seguridad accesibles en red.

### Backup de sistemas virtuales

Un snapshot captura el estado del disco virtual en un instante mediante ficheros delta que registran los cambios posteriores; no constituye backup por sí solo porque reside en el mismo almacenamiento físico que el original. CBT (Changed Block Tracking) es una funcionalidad del hipervisor (VMware) que mantiene un mapa de bloques modificados desde el último backup, permitiendo backups incrementales sin escanear el disco completo. VADP (vStorage APIs for Data Protection) permite a soluciones de terceros (Veeam, Commvault) acceder directamente a los snapshots a nivel de imagen sin agente dentro de la VM.

La consistencia de aplicación se logra mediante VSS (Volume Shadow Copy Service) en Windows, que coordina con SQL Server/Exchange el volcado de buffers y truncado de logs antes de capturar el snapshot, garantizando una copia restaurable sin corrupción. La consistencia de crash captura el disco "tal cual", equivalente a un corte de energía; la aplicación debe recuperarse por sus propios mecanismos (redo logs, journaling) al arrancar, con mayor riesgo de pérdida de transacciones en vuelo.

### Virtualización de sistemas

| | Tipo 1 (bare-metal) | Tipo 2 (hosted) |
|---|---|---|
| Ejecución | Directa sobre el hardware | Sobre un SO anfitrión |
| Ejemplos | ESXi, Hyper-V, KVM, Xen | VMware Workstation, VirtualBox |
| Rendimiento | Alto, baja sobrecarga | Menor, doble capa de abstracción |
| Uso típico | Producción, datacenter | Escritorio, desarrollo, pruebas |

vMotion / Live Migration traslada una VM en ejecución entre hosts físicos sin interrupción de servicio, copiando iterativamente la memoria RAM mientras la VM sigue activa y conmutando en milisegundos; requiere almacenamiento compartido (o Storage vMotion si también se mueve el disco). El overcommit asigna a las VMs más vCPU/vRAM de los físicamente disponibles asumiendo que no todas alcanzan pico simultáneo (ratios típicos de CPU 4:1 a 8:1); en memoria se gestiona con ballooning, compresión de páginas y swap a disco cuando el overcommit es agresivo. Las reglas de afinidad fuerzan a que ciertas VMs corran siempre en el mismo host (ej. por latencia entre nodos de un mismo clúster de aplicación); las de anti-afinidad las separan siempre en hosts distintos (ej. nodos de un clúster de alta disponibilidad, para evitar un punto único de fallo).

### VDI: virtualización de puestos de usuario

Los protocolos de escritorio remoto difieren en su gestión de banda ancha y compresión: RDP (Microsoft, estándar, buena compresión con codificación H.264/AVC en versiones recientes), PCoIP (Teradici/VMware Horizon, orientado a compresión de imagen, robusto en WAN de banda limitada), Blast Extreme (VMware, adaptativo H.264, mejor aprovechamiento de CPU cliente y ancho de banda variable) e ICA/HDX (Citrix, alta eficiencia de compresión y canales virtuales para USB/audio/impresión).

El "boot storm" ocurre cuando un gran número de escritorios virtuales arrancan simultáneamente (ej. al inicio de la jornada laboral), generando un pico masivo de IOPS de lectura sobre el almacenamiento compartido que puede saturar la SAN/NAS y degradar el servicio. Se mitiga con imágenes doradas (golden image) más clones enlazados o instant clones que comparten una base de solo lectura reduciendo I/O redundante, caché de lectura en el host (View Storage Accelerator/CBRC), almacenamiento todo-flash y escalonando los arranques fuera de la hora punta.

### Trampas habituales de examen

1. **RPO vs RTO**: RPO mide cuántos datos se pueden perder (mirando hacia atrás, desde el último punto recuperable); RTO mide cuánto se tarda en volver a estar operativo (mirando hacia delante, el tiempo de parada).
2. **Incremental vs diferencial**: el incremental copia cambios desde el último backup de cualquier tipo (cadena larga en restauración); el diferencial copia cambios desde el último completo (restauración con solo dos backups, más rápida pero mayor volumen por copia).
3. **Snapshot no es backup**: comparte el mismo almacenamiento físico que el original; si falla el datastore, se pierden ambos a la vez.
4. **RAID no sustituye al backup**: protege frente a fallo físico de disco, no frente a borrado accidental, corrupción lógica o ransomware, que se replican igualmente en todos los discos del array.
5. **NAS vs SAN**: NAS trabaja a nivel de archivo (NFS/SMB) y SAN a nivel de bloque (el host ve un disco crudo que debe formatear), independientemente de que ambos puedan viajar sobre red Ethernet (NAS siempre, SAN solo si es iSCSI).

## Tema 3. Administración de servidores de correo electrónico y sus protocolos. Administración de contenedores y microservicios.

### 1. Arquitectura del correo electrónico

El sistema de correo electrónico se basa en cuatro roles funcionales, no siempre coincidentes con software distinto:

- **MUA (Mail User Agent)**: cliente que usa el usuario (Outlook, Thunderbird, webmail). Compone y lee mensajes.
- **MSA (Mail Submission Agent)**: recibe el mensaje del MUA, típicamente en el puerto 587 con autenticación obligatoria, y valida que el remitente esté autorizado a enviar.
- **MTA (Mail Transfer Agent)**: transporta el mensaje entre servidores mediante SMTP (Postfix, Exim, Sendmail). Puede actuar como relay.
- **MDA (Mail Delivery Agent)**: entrega el mensaje al buzón final del destinatario (Dovecot, Procmail), donde queda accesible vía POP3/IMAP.

Flujo completo de un mensaje:

```
[Emisor MUA] --SMTP:587(auth)--> [MSA]
                                   |
                                   v  SMTP:25
                             [MTA origen] --DNS MX lookup--> [MTA destino]
                                   |                              |
                                   v (relay si aplica)            v
                             [MTA intermedio] -------------> [MDA destino]
                                                                    |
                                                                    v
                                                            [Buzón / Maildir]
                                                                    |
                                                       POP3:110/995 o IMAP:143/993
                                                                    |
                                                                    v
                                                          [Receptor MUA]
```

El MTA origen resuelve el dominio del destinatario consultando los registros **MX** en el DNS, ordenados por prioridad (a menor número, mayor prioridad), y establece conexión SMTP saliente contra el MTA de mayor prioridad disponible.

### 2. El protocolo SMTP en detalle

SMTP (Simple Mail Transfer Protocol, RFC 5321) es un protocolo de texto plano orientado a línea, con diálogo cliente-servidor por comandos y códigos de respuesta numéricos.

**Puertos:**
- **25**: MTA-a-MTA (relay entre servidores). Muchos ISP lo bloquean en salida para evitar spam desde equipos comprometidos.
- **587 (submission)**: MUA-a-MSA, con STARTTLS y autenticación (SMTP AUTH) obligatoria.
- **465 (SMTPS)**: submission con TLS implícito desde el inicio de la conexión (no STARTTLS), reintroducido formalmente en RFC 8314.

**Sesión SMTP típica:**

```
S: 220 mail.dominio.es ESMTP Postfix
C: EHLO cliente.dominio.es
S: 250-mail.dominio.es
S: 250-PIPELINING
S: 250-SIZE 10485760
S: 250-STARTTLS
S: 250 AUTH LOGIN PLAIN
C: MAIL FROM:<emisor@dominio.es>
S: 250 2.1.0 Ok
C: RCPT TO:<destino@otrodominio.es>
S: 250 2.1.5 Ok
C: DATA
S: 354 End data with <CR><LF>.<CR><LF>
C: Subject: Prueba
C: 
C: Cuerpo del mensaje.
C: .
S: 250 2.0.0 Ok: queued as A1B2C3D4
C: QUIT
S: 221 2.0.0 Bye
```

`HELO` es el saludo básico (RFC 821); `EHLO` es su extensión (ESMTP) que anuncia capacidades del servidor (STARTTLS, AUTH, tamaño máximo, pipelining).

**Códigos de respuesta:**
- **2xx (éxito)**: `250` operación aceptada; `220` servidor listo; `221` cierre de conexión.
- **3xx (información intermedia)**: `354` esperando el cuerpo tras `DATA`.
- **4xx (error transitorio)**: `421` servicio no disponible, `450` buzón temporalmente no accesible (p. ej. locked), `451` error de procesamiento local; el mensaje queda en cola para reintento.
- **5xx (error permanente)**: `550` buzón inexistente o rechazado por política, `552` excede cuota, `554` transacción fallida (frecuentemente por filtros antispam); el mensaje se devuelve como rebote (bounce, NDR).

### 3. POP3 frente a IMAP

Ambos son protocolos de acceso al buzón, radicalmente distintos en filosofía.

**POP3** (puerto 110 / 995 con SSL) descarga los mensajes al cliente y, por defecto, los elimina del servidor. Comandos básicos: `USER`, `PASS`, `STAT` (número y tamaño de mensajes), `LIST`, `RETR n` (recuperar mensaje n), `DELE n` (marcar borrado), `QUIT` (confirma borrados).

**IMAP** (puerto 143 / 993 con SSL) mantiene el estado en el servidor, permite gestionar carpetas y sincronizar múltiples dispositivos. Tiene tres estados definidos por RFC 3501:

1. **No autenticado**: conexión establecida, pendiente `LOGIN`/`AUTHENTICATE`.
2. **Autenticado**: credenciales válidas, aún sin carpeta seleccionada; permite `LIST`, `CREATE`, `SELECT`.
3. **Seleccionado**: tras `SELECT INBOX`, permite operar sobre mensajes: `FETCH`, `STORE`, `SEARCH`, `EXPUNGE`.

Flags de mensaje IMAP (definidos, gestionables con `STORE`): `\Seen`, `\Answered`, `\Flagged`, `\Deleted` (marcado, se elimina físicamente con `EXPUNGE`), `\Draft`, `\Recent`.

| Aspecto | POP3 | IMAP |
|---|---|---|
| Ubicación del mensaje | Se descarga y borra del servidor | Permanece en servidor |
| Multidispositivo | No sincroniza | Sincroniza estado (leído, carpetas) |
| Estructura de carpetas | No soporta | Sí, jerárquica |
| Consumo de red | Bajo tras descarga | Requiere conexión frecuente |
| Puerto sin cifrar / cifrado | 110 / 995 | 143 / 993 |

### 4. Autenticación de dominio anti-phishing: SPF, DKIM y DMARC

**SPF (Sender Policy Framework)**: registro TXT en el DNS del dominio que enumera qué servidores están autorizados a enviar correo en su nombre. El MTA receptor comprueba la IP del emisor contra esta lista.

```
dominio.es. IN TXT "v=spf1 ip4:203.0.113.10 include:spf.protection.outlook.com -all"
```

`-all` (fail estricto) rechaza cualquier IP no listada; `~all` (softfail) la marca como sospechosa sin rechazar.

**DKIM (DomainKeys Identified Mail)**: firma criptográfica del mensaje. El MTA emisor firma con una **clave privada** ciertas cabeceras y el cuerpo (hash), y publica la **clave pública** en un registro TXT bajo `selector._domainkey.dominio.es`. El receptor recalcula el hash y lo valida con la clave pública.

```
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=dominio.es;
 s=selector1; t=1735000000;
 h=from:to:subject:date;
 bh=47DEQpj8HBSa+/TImW+5JCeuQeR...=;
 b=T5jK8mQpL2n9xR4vC1sD7fH3gA6wE...=
```

**DMARC (Domain-based Message Authentication, Reporting and Conformance)**: define qué hacer cuando SPF y/o DKIM fallan, y exige **alineación**: el dominio del `From:` visible debe coincidir (exacta o parcialmente, según `aspf`/`adkim`) con el dominio autenticado por SPF/DKIM.

```
_dmarc.dominio.es. IN TXT "v=DMARC1; p=quarantine; rua=mailto:dmarc-reports@dominio.es; pct=100; adkim=s; aspf=r"
```

Políticas: `p=none` (solo monitoriza, no actúa), `p=quarantine` (marca como sospechoso/spam), `p=reject` (rechaza directamente). La progresión recomendada es `none` → `quarantine` → `reject`, tras analizar los informes agregados (`rua`) para evitar falsos positivos.

### 5. Administración operativa del servidor

**Colas de correo** (Postfix): los mensajes pendientes de entrega (por diferimiento, error temporal o congestión) residen en `/var/spool/postfix`. Comandos clave:

```bash
mailq                    # lista mensajes en cola (alias de postqueue -p)
postqueue -p             # equivalente
postqueue -f             # fuerza el reenvío inmediato de toda la cola
postsuper -d ID          # elimina un mensaje concreto de la cola
postsuper -d ALL deferred  # purga todos los diferidos
```

**DNSBL (DNS Blackhole Lists)**: listas negras consultadas en tiempo real (Spamhaus, SORBS) contra la IP emisora; Postfix las integra mediante `smtpd_recipient_restrictions` con `reject_rbl_client zen.spamhaus.org`.

**Filtrado antispam — SpamAssassin**: analiza cada mensaje asignando una puntuación mediante reglas heurísticas (cabeceras sospechosas, palabras clave, DNSBL) combinadas con un **filtro bayesiano** entrenado por el usuario (`sa-learn --spam`/`--ham`), que ajusta probabilísticamente la puntuación según el histórico de correo clasificado. Se define un umbral (`required_score`, típicamente 5.0) por encima del cual el mensaje se marca o rechaza.

**Antivirus — ClamAV**: se integra en el flujo SMTP mediante `amavisd-new` o `clamav-milter`, escaneando adjuntos antes de la entrega y rechazando o poniendo en cuarentena mensajes infectados.

### 6. Alta disponibilidad de correo

Se publican varios registros **MX** con distinta **prioridad** (número menor = mayor preferencia):

```
dominio.es. IN MX 10 mx1.dominio.es.
dominio.es. IN MX 20 mx2.dominio.es.
```

Si `mx1` no responde, el MTA emisor reintenta contra `mx2` (MX secundario), que puede aceptar el correo en cola (backup MX) o simplemente balancear carga si ambos tienen igual prioridad.

---

### 7. Contenedores: namespaces y cgroups de Linux

Un contenedor no es una máquina virtual: es un proceso Linux normal al que el kernel aísla mediante dos mecanismos independientes.

**Namespaces** (aíslan la *visibilidad*, "qué ve" el proceso):
- **pid**: el proceso ve su propio árbol de PIDs; dentro del contenedor es PID 1, aunque en el host tenga otro PID real.
- **net**: pila de red propia (interfaces, tablas de rutas, puertos); permite que dos contenedores usen el mismo puerto 80 sin colisión.
- **mnt**: árbol de puntos de montaje propio; el contenedor ve su propio filesystem raíz.
- **uts**: hostname y dominio NIS independientes del host.
- **ipc**: colas de mensajes, semáforos y memoria compartida System V aisladas.
- **user**: mapea UIDs/GIDs del contenedor a un rango distinto en el host (p. ej. root dentro del contenedor = UID 100000 fuera), reduciendo el impacto de un escape.

**cgroups** (limitan y contabilizan *recursos*, "cuánto" puede consumir):
- **cgroups v1**: jerarquías independientes por controlador (cpu, memory, blkio...), cada una montada por separado; más flexible pero más complejo de gestionar coherentemente.
- **cgroups v2**: jerarquía unificada única, todos los controladores bajo el mismo árbol; modelo más simple, adoptado por defecto en distribuciones modernas (systemd, Docker reciente, Kubernetes).

Ejemplo: limitar memoria de un contenedor a 512 MB usa el controlador `memory` de cgroups; aislar que no vea los procesos de otros contenedores usa el namespace `pid`. Son ortogonales: se puede limitar CPU sin aislar red, y viceversa.

### 8. Docker en profundidad

**Dockerfile comentado:**

```dockerfile
FROM node:20-alpine            # imagen base minimalista (Alpine ~5MB)
WORKDIR /app                   # directorio de trabajo dentro del contenedor
COPY package*.json ./          # copia solo manifiestos primero (cachea la capa)
RUN npm ci --omit=dev          # instala dependencias en capa separada y cacheable
COPY . .                       # copia el resto del código (invalida caché si cambia)
RUN addgroup -S app && adduser -S app -G app   # usuario no privilegiado
USER app                       # evita ejecutar el proceso como root
EXPOSE 3000                    # documenta el puerto (no lo publica)
HEALTHCHECK --interval=30s CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "server.js"]      # proceso principal (PID 1 del contenedor)
```

Cada instrucción genera una **capa** (layer) inmutable superpuesta mediante un filesystem **copy-on-write** (overlay2 en Docker moderno): las capas se comparten entre imágenes que las tienen en común, ahorrando espacio, y solo se copia (y modifica) un bloque cuando un proceso escribe sobre él. El orden de las instrucciones importa: colocar lo que cambia con menos frecuencia (dependencias) antes que el código fuente maximiza el aprovechamiento de la caché de build.

**docker-compose.yml** (orquestación local multicontenedor):

```yaml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=db
    depends_on:
      - db
  db:
    image: postgres:16-alpine
    volumes:
      - dbdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    secrets:
      - db_password
volumes:
  dbdata:
secrets:
  db_password:
    file: ./db_password.txt
```

**Registros de imágenes**: Docker Hub (público, por defecto), o registros privados como **Harbor** (self-hosted, con escaneo de vulnerabilidades integrado, control de acceso RBAC y replicación entre instancias), útiles en entornos corporativos donde no se puede depender de un registro externo.

### 9. Kubernetes en profundidad

**Control plane:**
- **kube-apiserver**: punto de entrada único; expone la API REST, valida y persiste peticiones.
- **etcd**: base de datos clave-valor distribuida que almacena todo el estado del clúster.
- **kube-scheduler**: decide en qué nodo se ejecuta cada Pod nuevo según recursos disponibles y afinidades.
- **kube-controller-manager**: ejecuta bucles de control (ReplicaSet, Node, Endpoints) que reconcilian el estado real con el deseado.

**Nodos (worker):**
- **kubelet**: agente que garantiza que los contenedores descritos en los Pods asignados a ese nodo estén ejecutándose.
- **kube-proxy**: gestiona reglas de red (iptables/IPVS) para el enrutamiento de Services.
- **container runtime**: containerd o CRI-O, motor que efectivamente crea y ejecuta los contenedores vía la interfaz CRI.

**Objetos principales**: **Pod** (unidad mínima desplegable, uno o más contenedores que comparten red y almacenamiento), **Deployment** (gestiona ReplicaSets, despliegues rolling update), **Service** (IP virtual estable que balancea tráfico hacia Pods mediante selector de labels), **Ingress** (enrutamiento HTTP/HTTPS externo hacia Services), **ConfigMap** (configuración no sensible desacoplada de la imagen), **Secret** (datos sensibles, codificados en base64, montables como volumen o variable de entorno), **PersistentVolume/PersistentVolumeClaim** (abstracción de almacenamiento persistente independiente del ciclo de vida del Pod).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api
          image: registro.interno/api:1.4.2
          ports:
            - containerPort: 8080
          resources:
            requests: { cpu: "100m", memory: "128Mi" }
            limits: { cpu: "500m", memory: "256Mi" }
---
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  selector:
    app: api
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
```

### 10. VM vs contenedor, y seguridad

| Aspecto | Máquina virtual | Contenedor |
|---|---|---|
| Aislamiento | Hipervisor, kernel propio por VM | Namespaces/cgroups, kernel compartido con el host |
| Arranque | Minutos (boot de SO completo) | Segundos o milisegundos |
| Tamaño | GB (SO completo) | MB (solo dependencias de la app) |
| Densidad por host | Baja-media | Alta |
| Seguridad de aislamiento | Fuerte (frontera de hardware) | Más débil (comparte kernel) |
| Caso de uso típico | Cargas heterogéneas, multi-SO | Microservicios, despliegue rápido |

**Seguridad de contenedores**: escaneo de imágenes en el pipeline CI/CD (Trivy, Clair, o el escáner integrado de Harbor) para detectar CVEs en las capas antes de publicar; ejecución con **usuario no root** dentro del contenedor (como en el Dockerfile anterior) para limitar el impacto de un escape; **Network Policies** en Kubernetes, que restringen mediante selectores de labels qué Pods pueden comunicarse entre sí (deny-by-default más reglas explícitas de permiso), evitando movimiento lateral tras un compromiso.

### Trampas habituales de examen

- No confundir **MSA** (puerto 587, con autenticación, entre MUA y servidor) con **MTA** (puerto 25, entre servidores, sin autenticación de usuario).
- El código SMTP `550` es un rechazo **permanente** (no se reintenta); `450`/`451` son **transitorios** (Postfix reintenta según su política de colas). Confundirlos en un supuesto práctico es error típico.
- SPF valida el dominio del sobre (`MAIL FROM`, envelope sender), no necesariamente el `From:` visible; DMARC es quien exige la **alineación** entre ambos, de ahí que un mensaje pueda pasar SPF y aun así fallar DMARC.
- Un **namespace** aísla visibilidad (qué recursos "ve" el proceso); un **cgroup** limita y contabiliza consumo de recursos. No son intercambiables ni resuelven el mismo problema.
- En Kubernetes, un **Service** no es un balanceador físico: es una regla de red gestionada por kube-proxy que redirige hacia Pods vivos según `selector`; el **Ingress** opera en capa HTTP y necesita un controlador (nginx-ingress, Traefik) que sí implemente el objeto.

## Tema 4. Administración de redes de área local. Gestión de usuarios. Gestión de dispositivos. Monitorización y control de tráfico.

### 1. Diseño jerárquico de la red

El modelo jerárquico clásico divide la LAN en tres capas funcionales que evitan mezclar en un mismo equipo tareas de conmutación masiva, enrutamiento entre VLAN y conectividad de usuario final:

- **Núcleo (core):** backbone de alta velocidad, baja latencia y máxima disponibilidad. No realiza filtrado ni políticas complejas; su única misión es conmutar tráfico entre bloques de distribución lo más rápido posible. Se diseña redundante (doble enlace, doble switch) para tolerar fallos sin punto único de fallo.
- **Distribución:** frontera entre capas de acceso y núcleo. Aquí se realiza el enrutamiento inter-VLAN, la agregación de enlaces de los switches de acceso, la aplicación de ACL y políticas de QoS, y la sumarización de rutas hacia el núcleo. Es el punto natural para implementar redundancia con HSRP/VRRP.
- **Acceso:** capa de conexión directa con el usuario final (PC, teléfono IP, impresora, punto de acceso Wi-Fi). Aplica seguridad de puerto (port-security, 802.1X), asignación de VLAN por puerto y PoE.

En redes pequeñas, distribución y núcleo pueden colapsarse en un único par de switches ("collapsed core"), pero el razonamiento por capas sigue siendo la base para justificar decisiones de diseño en el supuesto práctico.

### 2. Segmentación lógica: VLAN y 802.1Q

Una VLAN (Virtual LAN) segmenta un dominio de broadcast a nivel de capa 2 sin necesidad de segmentación física. El estándar **IEEE 802.1Q** define el etiquetado de trama que permite a un enlace transportar tráfico de varias VLAN.

El tag 802.1Q ocupa **4 bytes** insertados entre la dirección MAC origen y el campo EtherType/Longitud original:

| Campo | Tamaño | Contenido |
|---|---|---|
| TPID (Tag Protocol Identifier) | 2 bytes | Valor fijo `0x8100`, indica que sigue una etiqueta 802.1Q |
| PCP (Priority Code Point) | 3 bits | Prioridad 802.1p (0-7), usada para QoS en capa 2 |
| DEI/CFI (Drop Eligible Indicator) | 1 bit | Elegibilidad de descarte en congestión |
| VLAN ID | 12 bits | Identificador de VLAN (0 y 4095 reservados; rango útil 1-4094) |

Un **puerto access** pertenece a una única VLAN y entrega tramas sin etiquetar al host; un **puerto trunk** transporta múltiples VLAN etiquetadas entre switches (o hacia un router/firewall para enrutamiento inter-VLAN, "router-on-a-stick"). La **VLAN nativa** de un trunk es la única que circula sin etiquetar; si no coincide en ambos extremos se produce un salto de VLAN (VLAN hopping) o pérdida de conectividad, por lo que buenas prácticas recomiendan moverla a una VLAN no usada distinta de la VLAN 1.

```
vlan 10
 name VENTAS
vlan 20
 name IT
!
interface GigabitEthernet0/1
 switchport mode access
 switchport access vlan 10
!
interface GigabitEthernet0/24
 switchport mode trunk
 switchport trunk allowed vlan 10,20
 switchport trunk native vlan 99
```

### 3. Asignación dinámica de direcciones: DHCP

DHCP (Dynamic Host Configuration Protocol, RFC 2131) automatiza la asignación de IP, máscara, puerta de enlace y demás parámetros. El proceso de arranque se conoce como **DORA**:

```
Cliente                                   Servidor DHCP
   |---- DISCOVER (broadcast, UDP 68->67) ---->|
   |<--- OFFER (propone IP + parámetros) ------|
   |---- REQUEST (broadcast, confirma oferta) ->|
   |<--- ACK (concede la IP, envía opciones) ---|
```

Opciones DHCP relevantes: **opción 1** (máscara de subred), **opción 3** (router/puerta de enlace), **opción 6** (servidores DNS), **opción 51** (tiempo de concesión o lease time), **opción 53** (tipo de mensaje DHCP) y **opción 82** (información del agente de retransmisión).

Como DHCP se basa en broadcast de capa 2, un cliente en una subred sin servidor local necesita un **DHCP relay / IP helper**: el router de esa subred convierte el broadcast en unicast hacia el servidor real.

```
interface GigabitEthernet0/0
 ip helper-address 192.168.1.10
```

Para alta disponibilidad existe el **DHCP failover** entre dos servidores: modo **load balance** (ambos activos, se reparten las peticiones según un ratio configurado por hash) y modo **hot standby** (uno activo, otro pasivo que solo responde si el principal cae). El parámetro clave es el **MCLT (Maximum Client Lead Time)**: margen de seguridad que un servidor debe esperar antes de poder extender unilateralmente una concesión cuando pierde contacto con su pareja, evitando que ambos asignen la misma IP.

### 4. Resolución de nombres: DNS

DNS es una base de datos distribuida y jerárquica. La jerarquía consta de **servidores raíz** (root, identificados lógicamente de la A a la M), **servidores de dominio de nivel superior (TLD)** (.com, .es, .org) y **servidores autoritativos** de cada dominio, que contienen los registros reales.

Tipos de registro principales: **A** (nombre a IPv4), **AAAA** (nombre a IPv6), **CNAME** (alias hacia otro nombre canónico), **MX** (servidor de correo, con prioridad numérica), **PTR** (resolución inversa, zona `in-addr.arpa`), **NS** (delegación de servidores de nombres), **SOA** (autoridad de la zona: serie, refresh, retry, expire, TTL mínimo) y **TXT** (texto libre, usado para SPF/DKIM/verificaciones).

```
$TTL 3600
@       IN  SOA  ns1.ejemplo.es. admin.ejemplo.es. (
                 2026082701 ; serial
                 3600       ; refresh
                 900        ; retry
                 604800     ; expire
                 3600 )     ; minimo
        IN  NS   ns1.ejemplo.es.
        IN  MX   10 mail.ejemplo.es.
www     IN  A    192.168.10.10
mail    IN  A    192.168.10.20
ftp     IN  CNAME www
        IN  TXT  "v=spf1 mx -all"
```

La **resolución recursiva** ocurre cuando el cliente delega todo el trabajo en su resolver (normalmente el del proveedor o un servidor caché interno), que a su vez realiza consultas **iterativas** contra raíz, TLD y autoritativo hasta obtener la respuesta final. Cada registro se **cachea** durante su **TTL**; existe también caché negativa (RFC 2308) basada en el campo mínimo del SOA, para respuestas de tipo "no existe".

### 5. Gestión de usuarios: Active Directory, LDAP y Kerberos

Active Directory organiza los objetos en **bosque** (frontera de seguridad máxima, comparte esquema y catálogo global), **dominio** (frontera administrativa y de replicación) y **unidad organizativa (OU)** (contenedor para delegar administración y aplicar directivas de grupo).

La autenticación se basa en **Kerberos**. El **KDC (Key Distribution Center)**, que reside en cada controlador de dominio, integra dos servicios: **AS (Authentication Server)** y **TGS (Ticket Granting Service)**.

1. El cliente se autentica ante el AS con una clave derivada de su contraseña y recibe un **TGT (Ticket Granting Ticket)** cifrado con la clave de la cuenta `krbtgt`.
2. Cuando necesita acceder a un servicio concreto (SPN), presenta el TGT al TGS, que lo valida y emite un **ticket de servicio** cifrado con la clave de la cuenta del servicio destino.
3. El cliente presenta ese ticket de servicio directamente al servidor de recursos, que lo descifra con su propia clave y autentica al usuario sin que la contraseña viaje por la red.

Las **GPO (Group Policy Objects)** se aplican en el orden **LSDOU**: **L**ocal, **S**itio, **D**ominio, **O**U. La última en aplicarse (la OU más específica) prevalece en caso de conflicto, salvo que una directiva superior esté marcada como **Enforced/No invalidar**, en cuyo caso gana siempre sobre las inferiores.

### 6. Integración de Linux en el directorio

En entornos Linux, **OpenLDAP** (demonio `slapd`) implementa un servidor de directorio propio compatible con el protocolo LDAP. **SSSD (System Security Services Daemon)** unifica el acceso a backends de autenticación (LDAP, Kerberos, AD), cachea credenciales para uso offline y centraliza NSS/PAM. La integración directa con Active Directory se realiza mediante **Winbind** (componente de Samba que mapea SID de Windows a UID/GID Unix) o, de forma simplificada, con **realmd**:

```
realm discover dominio.ejemplo.local
realm join --user=administrador dominio.ejemplo.local
```

### 7. Modelos de control de acceso: DAC, MAC y RBAC

| Modelo | Quién decide el acceso | Ejemplo típico | Flexibilidad |
|---|---|---|---|
| **DAC** (Discrecional) | El propietario del recurso | Permisos NTFS/Unix (rwx) | Alta, pero propensa a errores de propagación |
| **MAC** (Obligatorio) | Política central del sistema, etiquetas de clasificación | SELinux, niveles confidencial/secreto | Baja, máxima seguridad |
| **RBAC** (Basado en roles) | Rol asignado al usuario, no el usuario directamente | Grupos de AD, roles de Azure/IAM | Media-alta, escala bien en organizaciones grandes |

En DAC el propio usuario puede ceder sus permisos a otro; en MAC ni siquiera el propietario puede saltarse la política (el kernel la impone); en RBAC la gestión se centra en mantener actualizada la pertenencia a roles en lugar de permisos individuales por recurso.

### 8. Gestión de dispositivos

El **MDM/UEM** (Mobile Device Management / Unified Endpoint Management) permite inscribir, configurar y proteger de forma centralizada equipos y móviles. Con **Microsoft Intune**, por ejemplo, se definen perfiles de configuración, directivas de cumplimiento (cifrado, PIN, versión de SO) integradas con acceso condicional, y capacidad de borrado remoto. En escenarios **BYOD** se recurre a directivas de protección de aplicaciones (MAM) sin inscripción completa del dispositivo, separando datos corporativos y personales mediante contenedores cifrados.

La **CMDB (Configuration Management Database)**, dentro del marco ITIL, almacena los **CI (Configuration Items)** y sus relaciones (qué servidor depende de qué switch, qué aplicación corre sobre qué VM). El **ITAM (IT Asset Management)** gestiona el ciclo de vida completo del activo —adquisición, asignación, mantenimiento y baja—, normalmente alimentando o alimentándose de la CMDB.

### 9. Monitorización de red

**SNMP** (Simple Network Management Protocol) sigue un modelo gestor-agente: la estación de gestión (NMS) consulta agentes residentes en los dispositivos. Operaciones básicas: **GET** (lee un OID concreto), **GETNEXT** (recorre el árbol MIB), **SET** (modifica un valor si es escribible) y **TRAP** (notificación asíncrona no solicitada del agente al gestor ante un evento; en v2c/v3 existe además **INFORM**, que sí se confirma).

La **MIB (Management Information Base)** es un árbol jerárquico de objetos identificados por **OID**; por ejemplo `1.3.6.1.2.1.1.3.0` corresponde a `sysUpTime` (iso.org.dod.internet.mgmt.mib-2.system.sysUpTime.0).

| Versión | Autenticación | Cifrado | Riesgo |
|---|---|---|---|
| SNMPv1 | Community string en texto claro | No | Alto |
| SNMPv2c | Community string en texto claro | No | Alto |
| SNMPv3 | USM: usuario + MD5/SHA | Sí, DES/AES | Bajo, apto para producción |

Para análisis de tráfico a nivel de flujo se usan tres tecnologías: **NetFlow** (propietario de Cisco, exporta registros unidireccionales por 5-tupla; v5 con campos fijos, v9 basado en plantillas), **sFlow** (basado en muestreo de paquetes, menor sobrecarga en el dispositivo, neutral respecto al fabricante) e **IPFIX** (estándar IETF derivado de NetFlow v9, extensible mediante plantillas).

### 10. Control de tráfico: QoS y ACL

QoS clasifica y marca el tráfico mediante **DSCP** (6 bits del campo DS de la cabecera IP): **EF (Expedited Forwarding, DSCP 46)** para tráfico sensible a latencia como VoIP, y las clases **AF (Assured Forwarding, AF11-AF43)** con distinta precedencia de descarte para tráfico con garantías relativas. El **shaping** retiene el tráfico excedente en un buffer y lo retransmite ajustado a la tasa contratada, suavizando ráfagas sin descartar paquetes salvo saturación del buffer; el **policing** actúa en tiempo real descartando o remarcando el exceso sin almacenarlo, imponiendo un límite estricto de tasa.

Las **ACL** filtran tráfico en routers/firewalls. Las **estándar** (numeradas 1-99 y 1300-1999 en Cisco) solo filtran por IP origen; las **extendidas** (100-199, 2000-2699) permiten filtrar por IP origen y destino, protocolo y puerto:

```
access-list 101 deny tcp any host 192.168.10.20 eq 23
access-list 101 permit ip any any
```

### Trampas habituales de examen

- Confundir la **VLAN nativa** de un trunk (la que viaja sin etiquetar) con la VLAN de gestión del switch; son conceptos independientes aunque por defecto coincidan en la VLAN 1.
- Invertir el orden **DORA**: recordar que Discover y Request son broadcast del cliente, mientras que Offer y Ack los envía el servidor.
- Intercambiar **shaping** y **policing**: shaping retrasa y encola (no suele perder paquetes salvo desbordamiento), policing descarta o remarca de inmediato.
- Confundir el **TGT** (emitido por el AS, cifrado con la clave de `krbtgt`) con el **ticket de servicio** (emitido por el TGS, cifrado con la clave de la cuenta del servicio de destino).
- Aplicar mal la prioridad **LSDOU**: la OU más cercana al objeto gana normalmente, pero una directiva marcada como "Enforced" en un nivel superior siempre prevalece sobre las inferiores.

## Tema 5. Conceptos de seguridad de los sistemas de información. Seguridad física. Seguridad lógica. Amenazas y vulnerabilidades. Técnicas criptográficas y protocolos seguros. Mecanismos de firma digital. Infraestructura física de un CPD: acondicionamiento y equipamiento. Sistemas de gestión de incidencias. Control remoto de puestos de usuario.

### 1. Conceptos fundamentales de seguridad de la información

La seguridad de la información se sustenta clásicamente en la tríada **CIA**: **Confidencialidad** (la información solo es accesible a quien está autorizado), **Integridad** (la información no se altera de forma no autorizada, ni accidental ni intencionadamente) y **Disponibilidad** (los sistemas y datos son accesibles cuando se necesitan). A estos tres pilares se añaden habitualmente dos propiedades complementarias: la **autenticidad**, que garantiza que el origen de la información o la identidad de un sujeto es quien dice ser, y la **trazabilidad** (o no repudio), que permite reconstruir quién hizo qué y cuándo, e impide que un actor niegue una acción realizada.

El **Esquema Nacional de Seguridad** (RD 311/2022) formaliza estas cinco propiedades como **dimensiones de seguridad**, resumidas en el acrónimo **D-A-I-C-T**: Disponibilidad, Autenticidad, Integridad, Confidencialidad y Trazabilidad. Cada activo de información del sistema se valora en una escala (Bajo/Medio/Alto/Muy Alto, o "no aplica") para cada una de estas cinco dimensiones, y el nivel más alto obtenido determina la **categoría del sistema** (Básica, Media o Alta), que a su vez condiciona el conjunto de medidas de seguridad exigibles del Anexo II. Esta correspondencia directa entre la tríada CIA ampliada y las dimensiones ENS es un punto que el examen suele preguntar de forma literal.

### 2. Seguridad física

La seguridad física protege el soporte tangible de la información: instalaciones, equipos y personas.

**Control de acceso.** Se articula en capas: perimetral (vallas, torniquetes), de edificio (recepción, tarjetas de proximidad RFID) y de sala técnica (doble factor). Las **tarjetas** (contacto o proximidad) identifican por posesión; la **biometría** identifica por características del propio individuo:
- **Huella dactilar**: barata, madura, pero degradable por suciedad o heridas; tasa de falso rechazo (FRR) relativamente alta en entornos industriales.
- **Iris**: muy alta precisión (patrón único e inmutable), coste elevado, requiere buena iluminación y cooperación del usuario.
- **Facial**: cómoda y sin contacto, pero más vulnerable a spoofing (fotos, mascarillas 3D) si no incorpora detección de vida (*liveness detection*).

El acceso a los CPD suele combinar tarjeta + biometría (dos factores) y emplear una **esclusa de seguridad o mantrap**: una cámara con dos puertas enclavadas eléctricamente de forma que nunca puedan estar ambas abiertas a la vez, evitando el *tailgating* (colarse tras una persona autorizada).

**Videovigilancia (CCTV).** Cámaras IP con grabación en NVR, retención mínima habitual de 30-90 días, y cobertura obligatoria de puntos críticos: accesos, pasillos de CPD y zona de SAI/generador.

**Sistemas de extinción de incendios.** En salas técnicas se descarta el agua y la espuma porque dañan irreversiblemente el hardware energizado y no son eléctricamente seguras; se emplean **agentes gaseosos limpios**:
- **FM-200 (HFC-227ea)**: extingue por absorción química del calor, no deja residuo, actúa en segundos, pero es un gas de efecto invernadero con vida atmosférica relativamente larga.
- **Novec 1230**: fluorocetona con impacto ambiental mucho menor (GWP casi nulo) y margen de seguridad amplio para ocupación humana; alternativa "verde" a FM-200.
- **IG-541 (y gases inertes similares, IG-55, IG-100)**: mezcla de nitrógeno, argón y CO₂ que extingue por dilución de oxígeno (lo reduce hasta ~12,5%, insuficiente para la combustión pero aún respirable); requiere más volumen de almacenamiento que los agentes químicos pero es totalmente inocuo ambientalmente.

Todos estos sistemas son no conductores, no dejan residuo corrosivo sobre placas y componentes, y se activan con preaviso audible/visual para permitir evacuación antes de la descarga.

### 3. Seguridad lógica

La seguridad lógica protege el acceso a datos y sistemas mediante software y configuración.

**Autenticación multifactor (MFA).** Combina al menos dos de tres factores: **algo que se sabe** (contraseña, PIN), **algo que se tiene** (token físico, móvil, tarjeta) y **algo que se es** (biometría). Los estándares más usados para el segundo factor son:
- **HOTP** (HMAC-based One-Time Password, RFC 4226): código derivado de un contador que se incrementa en cada uso.
- **TOTP** (Time-based One-Time Password, RFC 6238): variante de HOTP que sustituye el contador por la marca de tiempo actual (ventanas típicas de 30 segundos), es la base de apps como Google Authenticator o Microsoft Authenticator.

**Listas de control de acceso (ACL).** Estructuras asociadas a un recurso (fichero, carpeta, objeto de red) que enumeran sujetos y los permisos concretos que tienen sobre él (lectura, escritura, ejecución, borrado), complementando o sustituyendo a los modelos de permisos más simples tipo Unix (propietario/grupo/otros).

**Cifrado en reposo vs. en tránsito.** El cifrado **en reposo** protege los datos almacenados (disco, base de datos, backup) frente a acceso físico o robo del soporte, típicamente con AES a nivel de volumen (BitLocker, LUKS) o de campo en BD (*Transparent Data Encryption*). El cifrado **en tránsito** protege los datos mientras viajan por la red (TLS, IPsec, SSH), evitando su captura o alteración en el camino. Ambos son complementarios: cifrar solo en tránsito deja expuesto el dato en el disco del servidor destino, y viceversa.

### 4. Amenazas y vulnerabilidades

**Malware.** Taxonomía por comportamiento:
- **Virus**: código que se adjunta a un programa anfitrión y necesita ejecución de ese anfitrión para propagarse.
- **Gusano (worm)**: se propaga de forma autónoma por la red explotando vulnerabilidades, sin necesitar anfitrión ni intervención del usuario.
- **Troyano**: se presenta como software legítimo pero oculta funcionalidad maliciosa; no se autorreplica.
- **Ransomware**: cifra los datos de la víctima y exige rescate para la clave de descifrado; combina a menudo exfiltración previa (doble extorsión).
- **Spyware**: recopila información del usuario (pulsaciones, navegación, credenciales) sin consentimiento.
- **Rootkit**: se instala con privilegios de sistema para ocultar su propia presencia y la de otro malware, manipulando el propio kernel o las herramientas de administración.

**Ingeniería social.** Explota factores humanos en lugar de fallos técnicos:
- **Phishing**: correo masivo fraudulento que suplanta una entidad de confianza.
- **Spear-phishing**: phishing dirigido a una persona u organización concreta, con información contextual que aumenta la credibilidad.
- **Whaling**: spear-phishing dirigido a directivos o altos cargos.
- **Vishing**: ingeniería social por voz/teléfono.
- **Smishing**: ingeniería social por SMS.

**Ataques de red.**
- **MITM (Man in the Middle)**: el atacante se interpone entre dos partes y puede leer o alterar el tráfico sin que ninguna lo perciba.
- **DoS/DDoS**: agotamiento de recursos (ancho de banda, conexiones, CPU) para impedir el servicio legítimo; distribuido cuando procede de múltiples orígenes coordinados (botnet).
- **ARP spoofing**: el atacante envía respuestas ARP falsas para asociar su MAC a la IP de la puerta de enlace u otro host, desviando tráfico hacia sí (habilita MITM en redes locales).
- **DNS spoofing**: envenena la resolución de nombres para redirigir a un dominio legítimo hacia una IP maliciosa.

**Gestión de vulnerabilidades.** Cada vulnerabilidad pública se identifica con un **CVE** (Common Vulnerabilities and Exposures), un identificador único que referencia el fallo de forma estandarizada. Su gravedad se mide con **CVSS** (Common Vulnerability Scoring System), calculado a partir de un vector de métricas base:

| Métrica | Significado | Valores típicos |
|---|---|---|
| AV (Attack Vector) | Vía de explotación | Network / Adjacent / Local / Physical |
| AC (Attack Complexity) | Dificultad técnica | Low / High |
| PR (Privileges Required) | Privilegios previos necesarios | None / Low / High |
| UI (User Interaction) | Requiere acción del usuario | None / Required |
| S (Scope) | Si afecta a componentes fuera del vulnerable | Unchanged / Changed |
| C / I / A | Impacto en Confidencialidad / Integridad / Disponibilidad | None / Low / High |

La puntuación resultante va de **0 a 10**:

| Rango | Severidad |
|---|---|
| 0.0 | Ninguna |
| 0.1 – 3.9 | Baja |
| 4.0 – 6.9 | Media |
| 7.0 – 8.9 | Alta |
| 9.0 – 10.0 | Crítica |

Los escáneres de vulnerabilidades más habituales en administración pública son **Nessus** (comercial, muy extendido, con plugins actualizados diariamente) y **OpenVAS/Greenbone** (open source), que auditan sistemas contra bases de CVE conocidas y generan informes priorizados por CVSS.

### 5. Criptografía simétrica y asimétrica

**Simétrica.** Usa la misma clave para cifrar y descifrar. **DES** (clave de 56 bits efectivos) quedó obsoleto por fuerza bruta; **3DES** lo mitigó aplicando DES tres veces (clave efectiva ~112 bits) pero es lento y también en retirada. El estándar actual es **AES** (Advanced Encryption Standard), con claves de 128, 192 o 256 bits. El **modo de operación** es tan importante como el algoritmo:
- **ECB** (Electronic Codebook): cifra cada bloque de forma independiente e idéntica; es **inseguro** porque bloques de texto plano iguales producen bloques cifrados iguales, revelando patrones estructurales (el ejemplo clásico es una imagen cuyo contorno sigue siendo reconocible tras cifrarla en ECB).
- **CBC** (Cipher Block Chaining): cada bloque se combina (XOR) con el cifrado del bloque anterior antes de cifrarse, eliminando el patrón, pero requiere IV aleatorio y no ofrece autenticación por sí mismo.
- **GCM** (Galois/Counter Mode): modo autenticado (AEAD) que cifra y genera simultáneamente una etiqueta de integridad, es el preferido en TLS moderno por combinar rendimiento (paralelizable) y protección frente a manipulación.

**Asimétrica.** Usa un par de claves matemáticamente relacionadas: una pública (distribuible) y una privada (secreta). **RSA** se basa en la dificultad computacional de factorizar el producto de dos números primos muy grandes: es fácil multiplicarlos para obtener la clave pública, pero inviable en tiempo razonable recuperar los factores originales a partir del producto. **ECC** (criptografía de curva elíptica) se basa en el problema del logaritmo discreto sobre curvas elípticas y ofrece el mismo nivel de seguridad que RSA con claves mucho más cortas (una clave ECC de 256 bits equivale aproximadamente a una RSA de 3072 bits), lo que la hace más eficiente en CPU y ancho de banda, muy usada en dispositivos móviles y TLS moderno. **Diffie-Hellman** no cifra datos: es un protocolo de **intercambio de claves** que permite a dos partes acordar un secreto compartido a través de un canal inseguro sin haberlo transmitido nunca, combinando valores públicos y privados de forma que ambos lados llegan al mismo resultado por separado.

**Funciones hash.** Generan una huella de longitud fija a partir de una entrada de longitud variable, de forma determinista y (idealmente) sin colisiones prácticas. **MD5** (128 bits) está roto: se han demostrado colisiones prácticas en segundos, no debe usarse para integridad ni firma. **SHA-1** (160 bits) también se considera roto tras demostrarse colisiones prácticas (ataque SHAttered, 2017); navegadores y CA lo han retirado. El estándar actual es **SHA-256** (familia SHA-2) o **SHA-3** (familia con diseño interno distinto, esponja Keccak, como alternativa estructural independiente por si apareciera un fallo en SHA-2). **HMAC** combina una función hash con una clave secreta para producir un código de autenticación de mensaje que verifica simultáneamente integridad y autenticidad del origen.

### 6. Firma digital y PKI

La firma digital garantiza integridad, autenticidad y no repudio de un documento. El proceso es:
1. Se calcula el **hash** del documento original.
2. Ese hash se **cifra con la clave privada** del firmante (esta operación es la firma propiamente dicha).
3. El destinatario recalcula el hash del documento recibido y lo compara con el que resulta de **descifrar la firma con la clave pública** del firmante.
4. Si ambos hashes coinciden, se confirma que el documento no se alteró y que fue firmado por el poseedor de esa clave privada.

Esto requiere confiar en que la clave pública pertenece realmente a quien dice ser, lo que resuelve la **PKI** (Infraestructura de Clave Pública) mediante certificados. Una **CA raíz** (autoridad de certificación) firma certificados de **CA subordinadas**, que a su vez emiten certificados de usuario/servidor, formando una **cadena de confianza**: el verificador confía en la CA raíz (preinstalada en el sistema operativo o navegador) y de ahí desciende la confianza hasta el certificado final. Un **certificado X.509** contiene, entre otros campos: sujeto (*subject*), emisor (*issuer*), clave pública, período de validez, número de serie, algoritmo de firma y extensiones (uso de clave, nombres alternativos). La revocación de certificados comprometidos se comprueba con **CRL** (Certificate Revocation List, lista completa descargable y periódica) u **OCSP** (Online Certificate Status Protocol, consulta puntual en tiempo real sobre un certificado concreto, más ágil y con menor huella).

### 7. Protocolos seguros

**TLS** (Transport Layer Security) sustituyó a **SSL**, obsoleto por vulnerabilidades estructurales (POODLE en SSLv3, cifrados débiles); las versiones vigentes son TLS 1.2 y TLS 1.3, esta última simplifica el *handshake*, elimina algoritmos débiles y reduce la latencia de negociación. **SSH** (Secure Shell) permite administración remota cifrada y soporta **autenticación por clave pública** (el cliente demuestra posesión de la clave privada sin transmitirla, más segura que contraseña) además de **port forwarding**, que permite tunelizar tráfico de otro servicio a través de la conexión SSH cifrada (local, remoto o dinámico/SOCKS). **IPsec** protege tráfico IP a nivel de red mediante dos cabeceras: **AH** (Authentication Header) garantiza integridad y autenticidad pero no confidencialidad; **ESP** (Encapsulating Security Payload) añade cifrado además de integridad, por lo que es la opción mayoritaria en VPN. Puede operar en **modo transporte** (cifra solo el payload, extremos son los propios hosts, típico en comunicaciones host-a-host) o **modo túnel** (encapsula el paquete IP completo dentro de otro, típico en VPN sitio-a-sitio entre pasarelas).

### 8. Infraestructura física de un CPD

La clasificación de referencia del Uptime Institute define cuatro **niveles TIER**:

| Nivel | Disponibilidad | Downtime/año aprox. | Redundancia | Mantenimiento concurrente |
|---|---|---|---|---|
| TIER I | 99,671% | ~28,8 h | Ninguna (ruta única) | No |
| TIER II | 99,741% | ~22,0 h | Componentes N+1 | No |
| TIER III | 99,982% | ~1,6 h | N+1, múltiples rutas (una activa) | Sí |
| TIER IV | 99,995% | ~0,4 h | 2N o 2(N+1), tolerante a fallos | Sí, y tolera fallo simultáneo |

El **PUE** (Power Usage Effectiveness) mide la eficiencia energética: PUE = Energía total de la instalación / Energía consumida por el equipamiento TI. Un PUE de **1,5** significa que por cada vatio consumido por los servidores se gastan 0,5 W adicionales en refrigeración, distribución eléctrica y pérdidas; un PUE de **2,0** indica que el consumo auxiliar iguala al de TI, señal de baja eficiencia. El valor ideal teórico es 1,0.

La distribución en **pasillos fríos/calientes** (*hot aisle/cold aisle*) alterna filas de racks enfrentando sus tomas de aire frío entre sí (pasillo frío, alimentado por el suelo técnico o unidades CRAC) y sus salidas de aire caliente entre sí (pasillo caliente, evacuado hacia el retorno de climatización), evitando la recirculación de aire caliente y mejorando la eficiencia frente a una disposición uniforme.

Los **SAI/UPS** protegen frente a cortes y fluctuaciones eléctricas en tres arquitecturas: **standby** (el equipo funciona con red normalmente y conmuta a batería solo ante fallo, con un breve corte de transferencia), **línea interactiva** (regula la tensión sin pasar siempre por el inversor, mejor respuesta que standby), y **online (doble conversión)**: la corriente pasa siempre por rectificador-batería-inversor, de forma que la salida es permanentemente generada desde la batería sin ningún tiempo de conmutación ante un corte, es el estándar en CPD por su protección total frente a variaciones. Los **generadores diésel** cubren cortes prolongados que exceden la autonomía del SAI (minutos), arrancando automáticamente y asumiendo la carga en segundos mientras el SAI cubre el hueco de arranque.

### 9. Sistemas de gestión de incidencias (ITIL)

ITIL distingue con precisión tres conceptos que el examen suele confundir deliberadamente: un **incidente** es una interrupción no planificada o degradación de un servicio; un **problema** es la causa raíz subyacente a uno o varios incidentes (puede no tener aún solución conocida); una **petición de servicio** es una solicitud estándar y planificada (alta de usuario, instalación de software) que no implica que algo esté fallando. El **SLA** (Service Level Agreement) es el compromiso de nivel de servicio pactado con el cliente/usuario final; el **OLA** (Operational Level Agreement) es el acuerdo interno entre equipos de la propia organización que sustenta el cumplimiento de ese SLA. El **ciclo de vida de un ticket** típico recorre: registro → clasificación y priorización → asignación → diagnóstico → resolución → cierre, con escalados funcional (a un nivel técnico superior) o jerárquico (a un responsable) cuando se incumplen los tiempos. La **CMDB** (Configuration Management Database) almacena los elementos de configuración (CI) del sistema y sus relaciones, permitiendo analizar el impacto de un cambio o incidencia sobre el resto de la infraestructura.

### 10. Control remoto de puestos de usuario

**RDP** (Remote Desktop Protocol) es el protocolo propietario de Microsoft, funciona sobre el puerto TCP 3389, cifra la sesión (TLS o cifrado propio RDP) y desde Windows Server 2012/8 incorpora **NLA** (Network Level Authentication), que obliga a autenticarse antes de establecer la sesión gráfica completa, reduciendo la superficie de ataque frente a exploits que antes se lanzaban contra la pantalla de login sin autenticar. **VNC** (Virtual Network Computing) se basa en el protocolo **RFB** (Remote Framebuffer), de diseño más simple y multiplataforma: transmite directamente las actualizaciones del framebuffer del servidor y los eventos de teclado/ratón del cliente; históricamente no cifra por defecto (depende de la implementación) y suele requerir tunelizarse sobre SSH o VPN para uso seguro. En ambos casos, las buenas prácticas de seguridad exigen: restringir el acceso por IP o VPN, exigir MFA, registrar y auditar cada sesión (quién, cuándo, qué máquina), limitar los privilegios de la cuenta remota y cerrar sesiones inactivas automáticamente.

### Trampas habituales de examen

- Confundir **AH** (solo integridad/autenticidad) con **ESP** (integridad + cifrado) en IPsec, y **modo transporte** (extremos son los hosts) con **modo túnel** (encapsula el paquete completo, típico de VPN sitio-a-sitio).
- Asignar mal las dimensiones ENS: el acrónimo correcto es **D-A-I-C-T**, y la categoría del sistema la marca la dimensión con el **valor más alto**, no una media.
- Creer que **CRL** y **OCSP** son intercambiables: CRL es una lista completa descargada periódicamente, OCSP es una consulta puntual en tiempo real; OCSP es más ágil pero depende de disponibilidad del respondedor.
- Invertir la definición TIER: TIER III es "concurrentemente mantenible" (se puede intervenir sin parar servicio), TIER IV añade además **tolerancia a fallos** (soporta un fallo no planificado simultáneo a una intervención).
- Confundir **PUE bajo con mala eficiencia**: cuanto más cercano a 1,0, mejor; un PUE de 2,0 es peor (más ineficiente) que uno de 1,5, no al revés.
- Mezclar **incidente, problema y petición de servicio** en ITIL, o pensar que un SLA es lo mismo que un OLA (el SLA es externo/con el cliente, el OLA es interno entre equipos).

## Tema 6. Comunicaciones. Medios de transmisión. Modos de comunicación. Equipos terminales y equipos de interconexión y conmutación. Redes de comunicaciones. Redes de conmutación y redes de difusión. Comunicaciones móviles e inalámbricas.

### 1. Medios de transmisión guiados

El par trenzado transporta señales eléctricas por conductores de cobre trenzados entre sí para reducir la diafonía (crosstalk) inducida entre pares adyacentes. Existe en variantes UTP (sin blindaje), STP (blindaje por par) y S/FTP (blindaje por par más pantalla global), siendo el blindaje imprescindible a partir de categoría 7 para alcanzar sus frecuencias de trabajo sin interferencia.

| Categoría | Frecuencia máx. | Velocidad soportada | Distancia máx. | Observaciones |
|---|---|---|---|---|
| Cat 5e | 100 MHz | 1 Gbps (1000BASE-T) | 100 m | Aún desplegada en LAN heredadas |
| Cat 6 | 250 MHz | 1 Gbps (10 Gbps a ≤55 m) | 100 m | Limitación de 10GBASE-T por alien crosstalk |
| Cat 6a | 500 MHz | 10 Gbps | 100 m | UTP o STP, elimina el alien crosstalk |
| Cat 7 | 600 MHz | 10 Gbps | 100 m | S/FTP obligatorio, conectores GG45/TERA |
| Cat 8 | 2000 MHz | 25/40 Gbps | 30 m | Uso en racks de datacenter, no en horizontal de campus |

La fibra óptica transmite pulsos de luz por un núcleo de vidrio o plástico, siendo inmune a interferencias electromagnéticas y, a diferencia del cobre, **no sufre diafonía**: no existe acoplamiento eléctrico entre fibras porque no circula corriente ni campo eléctrico fuera del núcleo, solo confinamiento óptico por reflexión total interna. Se distinguen dos familias: la **multimodo (MMF)**, con núcleo ancho (50 o 62,5 micras) que permite múltiples modos de propagación, fuente LED o VCSEL, longitudes de onda de 850 y 1300 nm, y alcance limitado por dispersión modal (OM1 ≈33 m a 10 Gbps, OM2 ≈82 m, OM3 optimizada a láser ≈300 m, OM4 ≈550 m, OM5 orientada a WDM de banda ancha con varias longitudes de onda simultáneas sobre la misma fibra); y la **monomodo (SMF, OS1/OS2)**, con núcleo estrecho (~9 micras) que fuerza un único modo de propagación, fuente láser, longitudes de onda de 1310 y 1550 nm, y alcances de decenas de kilómetros gracias a su baja atenuación (~0,3-0,4 dB/km frente a 2-3 dB/km de la multimodo). Los conectores más habituales son SC (push-pull, cuadrado), LC (formato reducido, estándar en transceptores SFP), ST (bayoneta, en desuso) y MPO/MTP (multifibra, 12 o 24 hilos en un único conector, propio de troncales de datacenter).

### 2. Medios de transmisión no guiados

La radiofrecuencia se propaga por el aire sin confinamiento físico, es omnidireccional o direccional según la antena, y base de Wi-Fi, redes móviles y radioenlaces. Las microondas terrestres exigen visión directa (line of sight) y se emplean en enlaces punto a punto entre repetidores separados por la curvatura terrestre (típicamente cada 40-50 km). Las microondas por satélite dependen de la órbita: **GEO** (36 000 km, sincronizada con la rotación terrestre, latencia de ida de ~120-140 ms, ~240-280 ms de ida y vuelta, usada en televisión y banda ancha rural con pocos satélites); **MEO** (2000-35 786 km, ejemplo GPS a ~20 200 km, latencia ~50-150 ms); **LEO** (160-2000 km, ejemplo constelaciones tipo Starlink a ~550 km, latencia ~20-40 ms, pero requiere gran número de satélites porque cada uno es visible poco tiempo desde un punto fijo). El infrarrojo exige también visión directa, no atraviesa paredes y se usa en mandos a distancia y antiguos puertos IrDA. El láser ofrece enlaces de muy alto ancho de banda entre edificios, pero se degrada con niebla, lluvia o polvo en suspensión.

### 3. Modos de comunicación

Según el sentido del flujo de datos: **símplex** (una sola dirección, ej. difusión de radio o TV, teclado hacia el ordenador), **semidúplex** (ambas direcciones pero no simultáneas, ej. walkie-talkie, Ethernet en modo half-duplex sobre hub con CSMA/CD) y **dúplex completo** (ambas direcciones simultáneas, ej. llamada telefónica, Ethernet conmutado full-duplex).

En cuanto a la temporización, la transmisión **asíncrona** envía cada carácter enmarcado con un bit de inicio (start), los bits de datos, bit de paridad opcional y uno o dos bits de parada (stop); el receptor resincroniza su reloj en cada flanco de bajada del start bit, lo que añade overhead pero simplifica el hardware (UART, RS-232). La transmisión **síncrona** envía un flujo continuo de bits sin marcas por carácter, compartiendo temporización mediante una señal de reloj dedicada o embebida en la propia codificación de línea; es más eficiente en ancho de banda y se usa en HDLC, SDH/SONET o enlaces de alta velocidad.

Respecto al número de líneas físicas, la transmisión **paralela** envía varios bits simultáneamente por hilos independientes (antiguos puertos de impresora, buses IDE/ATA), pero a alta frecuencia sufre **skew**: pequeñas diferencias de longitud o de retardo entre hilos hacen que los bits no lleguen perfectamente alineados, corrompiendo la palabra recibida. La transmisión **serie** envía un único bit tras otro por un solo canal, evitando el problema de skew y permitiendo frecuencias de reloj mucho más altas; por eso interfaces que originalmente eran paralelas (ATA→SATA, puerto paralelo→USB, PCI→PCIe) migraron a serie para lograr mayor throughput neto pese a transmitir un bit cada vez.

### 4. Equipos terminales

El **DTE** (Data Terminal Equipment) es el equipo que genera o consume la información —un ordenador o terminal—, mientras que el **DCE** (Data Circuit-terminating Equipment) es el que establece, mantiene y termina el enlace de comunicaciones —clásicamente un módem—. La interfaz **RS-232/V.24** define la conexión serie entre ambos, con señales como TD (transmisión de datos), RD (recepción de datos), RTS/CTS (petición/autorización de envío, control de flujo por hardware), DTR/DSR (terminal y equipo de datos listos), DCD (detección de portadora) y RI (indicador de llamada), además de la referencia de masa GND.

### 5. Equipos de interconexión y conmutación

| Equipo | Capa OSI | Función |
|---|---|---|
| Repetidor | 1 (Física) | Regenera y amplifica la señal eléctrica u óptica para extender la distancia, sin interpretar contenido |
| Hub | 1 (Física) | Repetidor multipuerto; retransmite a todos los puertos; un único dominio de colisión |
| Puente (bridge) | 2 (Enlace) | Segmenta dominios de colisión aprendiendo direcciones MAC y filtrando tráfico entre segmentos |
| Switch (conmutador) | 2 (Enlace) | Puente multipuerto; cada puerto es su propio dominio de colisión; conmutación full-duplex por tabla MAC |
| Router (encaminador) | 3 (Red) | Encamina paquetes entre redes distintas según direcciones IP y tabla de rutas; separa dominios de difusión |
| Gateway (pasarela) | 7 (Aplicación) | Traduce entre arquitecturas de protocolos distintas de extremo a extremo (ej. pasarela de correo entre sistemas heterogéneos) |

### 6. Conmutación de circuitos frente a conmutación de paquetes

La **conmutación de circuitos** reserva un camino físico o lógico dedicado de extremo a extremo antes de transmitir, en tres fases: **establecimiento** (señalización que reserva recursos en cada nodo intermedio), **transferencia** (los datos fluyen con ancho de banda garantizado y constante) y **liberación** (se liberan los recursos reservados). Su ejemplo clásico es la telefonía conmutada tradicional (RTC) e ISDN. Ventaja: latencia constante y ancho de banda garantizado, ideal para tráfico isócrono como la voz; inconveniente: uso ineficiente del enlace si no hay datos que transmitir, y tiempo de establecimiento previo a cualquier envío.

La **conmutación de paquetes** fragmenta la información en unidades independientes que comparten estadísticamente el medio, bien como datagramas encaminados individualmente (IP) o mediante circuito virtual (Frame Relay, ATM, MPLS). Ventaja: aprovechamiento eficiente del ancho de banda mediante multiplexación estadística y resiliencia ante fallos de un nodo al poder recalcular rutas; inconveniente: latencia y jitter variables, y posible desorden o pérdida de paquetes salvo mecanismos adicionales de calidad de servicio. Ejemplo real de uso: Internet, basada íntegramente en conmutación de paquetes IP.

### 7. Redes de difusión

En una red de difusión (broadcast) todas las estaciones comparten un único canal de comunicación y toda transmisión llega, en principio, a todas ellas, por lo que cada trama debe incluir una dirección que identifique al destinatario real. Esta naturaleza compartida obliga a definir un **protocolo de control de acceso al medio (MAC)** que arbitre quién puede transmitir en cada instante para evitar colisiones o interferencias: CSMA/CD en Ethernet clásico, CSMA/CA en Wi-Fi, paso de testigo en Token Ring/FDDI, o TDMA/FDMA/CDMA en redes celulares. Se contraponen así a las redes de conmutación, donde la información atraviesa nodos intermedios que la encaminan de forma punto a punto sin que el resto de estaciones la reciban.

### 8. Comunicaciones móviles: evolución generacional

La **1G** fue analógica (AMPS, TACS), solo voz, con acceso FDMA. La **2G/GSM** digitalizó la voz con acceso TDMA combinado con FDMA, incorporando SMS y conmutación de circuitos. La **2.5G** añadió conmutación de paquetes sobre la red GSM: GPRS (hasta ~114 kbps teóricos) y su evolución EDGE, con modulación 8-PSK, hasta ~384 kbps ("2.75G"). La **3G/UMTS** introdujo acceso WCDMA con velocidades de 384 kbps a 2 Mbps, mejoradas por HSPA (HSDPA/HSUPA) hasta decenas de Mbps ("3.5G"). La **4G/LTE** es una red totalmente IP con OFDMA en enlace descendente y SC-FDMA en el ascendente, sustentada en el núcleo **EPC (Evolved Packet Core)**: el **eNodeB** es la estación base que integra funciones de radio y parte del control antes centralizado; el **MME** (Mobility Management Entity) gestiona señalización, autenticación y movilidad del terminal; el **SGW** (Serving Gateway) encamina y reenvía los paquetes de datos de usuario durante los traspasos entre estaciones; el **PGW** (PDN Gateway) es el punto de anclaje hacia redes externas como Internet, asignando la dirección IP al terminal.

La **5G NR** adopta una **arquitectura basada en servicios (SBA)**, donde las funciones del núcleo (AMF, SMF, UPF, entre otras) se implementan como microservicios modulares que se comunican mediante APIs, facilitando el **network slicing**: la creación de redes virtuales extremo a extremo, aisladas lógicamente sobre la misma infraestructura física, cada una dimensionada para un tipo de servicio. Los tres casos de uso definidos por el 3GPP son: **eMBB** (banda ancha móvil mejorada, ej. streaming de vídeo 4K/8K o realidad aumentada), **URLLC** (comunicaciones ultrafiables de baja latencia, por debajo de 1 ms, ej. cirugía remota o control de vehículos autónomos) y **mMTC** (comunicaciones masivas tipo máquina, ej. redes de sensores de ciudad inteligente con densidades de cientos de miles de dispositivos por km²). Trabaja en bandas **sub-6 GHz (FR1)**, con buena cobertura y penetración en interiores, y **mmWave (FR2, 24-100 GHz)**, con anchos de banda muy elevados pero alcance corto y fácil bloqueo por obstáculos.

### 9. Redes inalámbricas Wi-Fi

| Estándar | Nombre comercial | Banda | Velocidad máx. teórica | Técnica |
|---|---|---|---|---|
| 802.11a | — | 5 GHz | 54 Mbps | OFDM |
| 802.11b | — | 2,4 GHz | 11 Mbps | DSSS |
| 802.11g | — | 2,4 GHz | 54 Mbps | OFDM |
| 802.11n | Wi-Fi 4 | 2,4/5 GHz | 600 Mbps | OFDM + MIMO |
| 802.11ac | Wi-Fi 5 | 5 GHz | ~6,9 Gbps | OFDM + MU-MIMO (solo bajada) |
| 802.11ax | Wi-Fi 6/6E | 2,4/5/6 GHz | ~9,6 Gbps | OFDMA + MU-MIMO bidireccional |
| 802.11be | Wi-Fi 7 | 2,4/5/6 GHz | ~46 Gbps | OFDMA + Multi-Link Operation, canales de 320 MHz |

### 10. Comunicaciones inalámbricas de corto alcance

**Bluetooth** define tres clases de potencia: Clase 1 (100 mW, ~100 m), Clase 2 (2,5 mW, ~10 m, la más habitual en periféricos) y Clase 3 (1 mW, ~1 m). Su variante **BLE (Bluetooth Low Energy)** reduce drásticamente el consumo mediante ciclos de trabajo cortos, orientándose a wearables y balizas (beacons). **Zigbee**, basado en IEEE 802.15.4, forma redes en topología **malla (mesh)** autorreparable con roles de coordinador, router y dispositivo final, priorizando bajo consumo y baja tasa de datos frente a IoT doméstico e industrial. **NFC** opera a 13,56 MHz con un alcance de apenas ~4 cm, empleado en pago sin contacto, identificación y control de acceso, y en el emparejamiento inicial de otros enlaces inalámbricos.

### Trampas habituales de examen

- Confundir switch (capa 2, filtra por MAC) con router (capa 3, filtra y encamina por IP): el switch no separa dominios de difusión, el router sí.
- Afirmar que la fibra óptica sufre diafonía: es falso, al transmitir luz no hay acoplamiento electromagnético entre fibras.
- Invertir la relación altitud-latencia en satélites: a mayor altitud (GEO) mayor latencia y menor número de satélites necesarios; a menor altitud (LEO) menor latencia pero se requiere una constelación numerosa.
- Mezclar el orden GPRS→EDGE dentro de la 2.5G, o confundir el acceso TDMA de GSM con el CDMA de UMTS.
- Olvidar que la transmisión asíncrona lleva bits de inicio y parada por carácter, mientras que la síncrona transmite un flujo continuo sincronizado por reloj compartido, sin dichas marcas.

## Tema 7. El modelo TCP/IP y el modelo de referencia de interconexión de sistemas abiertos (OSI) de ISO. Protocolos TCP/IP.

### 1. El modelo OSI

El modelo OSI (Open Systems Interconnection), publicado por ISO en 1984 (ISO/IEC 7498), es un modelo de referencia **teórico y normativo** que descompone la comunicación entre sistemas en 7 capas, cada una con una función bien delimitada y una interfaz definida con las capas adyacentes. El principio rector es la **encapsulación**: cada capa añade su propia cabecera (y a veces cola) a los datos recibidos de la capa superior, formando la PDU (Protocol Data Unit) característica de ese nivel.

| Capa | Nombre | Función principal | PDU | Ejemplos de protocolos/dispositivos |
|---|---|---|---|---|
| 7 | Aplicación | Provee servicios de red directamente al usuario/proceso: correo, transferencia de ficheros, resolución de nombres. | Datos (Data) | HTTP, FTP, SMTP, DNS, SSH, Telnet |
| 6 | Presentación | Traduce, cifra/descifra y comprime la sintaxis de los datos entre formato de red y formato de aplicación. | Datos | TLS/SSL, JPEG, ASCII/EBCDIC, MPEG |
| 5 | Sesión | Establece, gestiona y finaliza el diálogo (sesión) entre aplicaciones, con control de turno y puntos de sincronización. | Datos | NetBIOS, RPC, sockets SSL (fase handshake) |
| 4 | Transporte | Comunicación extremo a extremo, fiable o no, segmentación, control de flujo y de errores entre procesos (puertos). | Segmento (TCP) / Datagrama (UDP) | TCP, UDP, SPX |
| 3 | Red | Direccionamiento lógico y encaminamiento (routing) entre redes distintas, fragmentación si procede. | Paquete | IP, ICMP, IPsec, routers |
| 2 | Enlace de datos | Direccionamiento físico (MAC), detección/corrección de errores, control de acceso al medio, entrega dentro de la misma red local. | Trama (Frame) | Ethernet, PPP, switches, bridges |
| 1 | Física | Transmisión de bits en bruto por el medio: voltajes, conectores, modulación, topología física. | Bit | Cable UTP, fibra óptica, hubs, repetidores |

**Capa física**: define características eléctricas, mecánicas, funcionales y de procedimiento del medio (RS-232, 10BASE-T, especificaciones de fibra). No interpreta el significado de los bits, solo su transmisión sincronizada. Trabajan aquí repetidores y hubs, que no distinguen tramas.

**Capa de enlace**: se subdivide en dos subcapas definidas por IEEE 802: **LLC** (Logical Link Control, 802.2), que multiplexa protocolos de capa superior y ofrece control de errores opcional, y **MAC** (Media Access Control), que gestiona el acceso al medio compartido (CSMA/CD en Ethernet clásica, CSMA/CA en Wi-Fi) y añade la dirección física de 48 bits. Los switches operan aquí, conmutando tramas según tabla de direcciones MAC.

**Capa de red**: responsable del direccionamiento lógico jerárquico (IP) y del cálculo de la mejor ruta entre redes mediante algoritmos de encaminamiento (RIP, OSPF, BGP como protocolos de routing, no de esta capa en sí sino que operan sobre ella). Realiza fragmentación de paquetes cuando el MTU del siguiente salto es menor.

**Capa de transporte**: primera capa realmente extremo a extremo (host a host), identifica procesos mediante puertos, y ofrece dos filosofías: orientada a conexión y fiable (TCP) o no orientada a conexión y de mejor esfuerzo (UDP).

**Capa de sesión**: coordina el diálogo entre aplicaciones, gestiona el modo (símplex, semidúplex, dúplex completo) y establece checkpoints de recuperación. En la práctica muy diluida en TCP/IP.

**Capa de presentación**: encargada de la sintaxis y semántica de la información: cifrado (TLS suele situarse conceptualmente aquí, aunque en la práctica se implementa entre transporte y aplicación), compresión y conversión de codificación de caracteres.

**Capa de aplicación**: interfaz directa con el usuario o proceso final; no es la aplicación en sí, sino el conjunto de protocolos que dan servicio a ella (correo, web, transferencia de ficheros, terminal remoto).

### 2. El modelo TCP/IP

El modelo TCP/IP, anterior en el tiempo (ARPANET, años 70, RFC 791/793 en 1981), es **descriptivo y práctico**: nace de una implementación real, no de una norma previa. Consta oficialmente de 4 capas, aunque a efectos didácticos suele desdoblarse la capa de acceso a la red en física + enlace, resultando 5.

| Capa TCP/IP (4 niveles) | Capa TCP/IP (5 niveles, didáctica) | Capas OSI equivalentes | Protocolos típicos |
|---|---|---|---|
| Aplicación | Aplicación | 7 Aplicación, 6 Presentación, 5 Sesión | HTTP, FTP, SMTP, DNS, SSH, Telnet, SNMP |
| Transporte | Transporte | 4 Transporte | TCP, UDP |
| Internet | Red | 3 Red | IP, ICMP, ARP*, IGMP |
| Acceso a la red | Enlace de datos | 2 Enlace | Ethernet, PPP, Wi-Fi (802.11) |
| Acceso a la red | Física | 1 Física | Medios físicos, señalización |

\* ARP se sitúa en la frontera 2/3: encapsula en trama de enlace pero resuelve direcciones de capa de red; muchos textos de examen lo ubican en Internet por convención RFC.

### 3. Diferencias filosóficas OSI vs TCP/IP

OSI es un modelo **normativo, diseñado antes que la implementación**, con 7 capas estrictamente separadas y pensado como estándar universal de interoperabilidad; en la práctica resultó excesivamente complejo y nunca triunfó como pila de protocolos real (sí como referencia pedagógica). TCP/IP es **descriptivo, la implementación precedió al modelo**, con menos capas, fusión de funciones (sesión/presentación diluidas en aplicación) y ha sido el estándar de facto de Internet desde los 80. OSI separa estrictamente servicio, interfaz y protocolo en cada capa; TCP/IP es más pragmático y permite que protocolos "salten" capas conceptualmente.

### 4. IPv4 en profundidad

Cabecera IPv4 (mínimo 20 bytes, máximo 60 con opciones):

| Campo | Tamaño | Descripción |
|---|---|---|
| Versión | 4 bits | Valor 4 |
| IHL (Internet Header Length) | 4 bits | Longitud de cabecera en palabras de 32 bits (mínimo 5) |
| ToS/DSCP | 8 bits | Tipo de servicio, hoy reinterpretado como DSCP para QoS |
| Longitud total | 16 bits | Tamaño del paquete completo (cabecera + datos), máx. 65535 bytes |
| Identificación | 16 bits | Identifica los fragmentos de un mismo datagrama origen |
| Flags | 3 bits | DF (Don't Fragment), MF (More Fragments), bit reservado |
| Fragment Offset | 13 bits | Posición del fragmento respecto al datagrama original |
| TTL | 8 bits | Salto máximo, decrementado por cada router; evita bucles infinitos |
| Protocolo | 8 bits | Protocolo de capa superior (6=TCP, 17=UDP, 1=ICMP) |
| Checksum de cabecera | 16 bits | Verificación de integridad solo de la cabecera |
| IP origen / IP destino | 32+32 bits | Direcciones de 4 octetos |

**Clases históricas**: A (1.0.0.0–126.x, máscara /8, primer bit 0), B (128.0.0.0–191.x, /16, bits 10), C (192.0.0.0–223.x, /24, bits 110), D (224–239, multicast), E (240–255, experimental/reservado). El esquema classful quedó obsoleto con CIDR (Classless Inter-Domain Routing, RFC 4632), que permite máscaras de longitud arbitraria (notación /n) desligadas de la clase, facilitando el agregado de rutas (route summarization).

**Direccionamiento privado (RFC 1918)**: 10.0.0.0/8, 172.16.0.0/12 y 192.168.0.0/16, no enrutables en Internet pública, traducidas mediante NAT.

**Fragmentación**: cuando un paquete supera el MTU del enlace de salida (típicamente 1500 bytes en Ethernet), el router lo fragmenta usando Identificación, Flags y Fragment Offset; el destino final reensambla los fragmentos. Si DF=1 y el paquete no cabe, se descarta y se devuelve ICMP tipo 3 código 4 (Fragmentation Needed).

### 5. IPv6 en profundidad

Direcciones de **128 bits**, notación hexadecimal en 8 grupos de 16 bits separados por dos puntos (ej. `2001:0db8:0000:0000:0000:ff00:0042:8329`), comprimibles eliminando ceros a la izquierda de cada grupo y sustituyendo una única secuencia de grupos completos a cero por `::`.

**Tipos de dirección**: unicast global (equivalente a las públicas IPv4, prefijo 2000::/3), link-local (`fe80::/10`, uso obligatorio en cada interfaz, no enrutable), multicast (`ff00::/8`, sustituye por completo al broadcast, que **no existe en IPv6**), y anycast (misma dirección asignada a varios nodos, responde el más cercano).

**Cabecera fija de 40 bytes**, sensiblemente simplificada respecto a IPv4: Version (4 bits), Traffic Class (8), Flow Label (20), Payload Length (16), Next Header (8, sustituye al campo Protocolo e indica cabecera de extensión o protocolo superior), Hop Limit (8, equivalente al TTL), Source Address (128) y Destination Address (128). No hay checksum de cabecera (delegado en capas superiores) ni fragmentación por routers intermedios (solo el origen fragmenta, mediante extension header Fragment).

**Extension headers**: cadena encadenada mediante Next Header (Hop-by-Hop Options, Routing, Fragment, Authentication Header, ESP, Destination Options), que mantiene la cabecera base ligera y extensible.

**Autoconfiguración**: SLAAC (Stateless Address Autoconfiguration) permite que el host genere su propia dirección combinando el prefijo anunciado por el router (Router Advertisement) con un identificador de interfaz (EUI-64 o aleatorio por privacidad), sin servidor central; DHCPv6 es la alternativa stateful, con servidor que asigna y controla direcciones y opciones (equivalente funcional a DHCP en IPv4). **NDP** (Neighbor Discovery Protocol, sobre ICMPv6) sustituye a ARP: mediante mensajes Neighbor Solicitation/Advertisement resuelve direcciones MAC, y mediante Router Solicitation/Advertisement descubre routers y prefijos.

### 6. TCP en profundidad

Cabecera TCP (20 bytes mínimo): Puerto origen (16 bits), Puerto destino (16), Número de secuencia (32), Número de ACK (32), Data Offset (4 bits), Flags (URG, ACK, PSH, RST, SYN, FIN), Ventana (16), Checksum (16), Puntero urgente (16).

**Three-way handshake** (establecimiento de conexión):
```
Cliente                          Servidor
  |------ SYN (seq=x) --------->|
  |<--- SYN-ACK (seq=y,ack=x+1)-|
  |------ ACK (ack=y+1) ------->|
```

**Cierre de conexión** (cuatro pasos, semicierre independiente por sentido):
```
Cliente                          Servidor
  |------ FIN (seq=a) --------->|
  |<------- ACK (ack=a+1) ------|
  |<------ FIN (seq=b) ---------|
  |------- ACK (ack=b+1) ------>|
```

**Control de flujo**: ventana deslizante (sliding window), el receptor anuncia en el campo Ventana el espacio disponible en su buffer; el emisor no puede enviar más bytes no confirmados que ese valor, evitando desbordar al receptor.

**Control de congestión** (evita saturar la red, no al receptor): 
- *Slow start*: la ventana de congestión (cwnd) arranca pequeña (típicamente 1-10 MSS) y crece exponencialmente (se duplica por cada RTT confirmado) hasta alcanzar el umbral ssthresh.
- *Congestion avoidance*: superado ssthresh, cwnd crece linealmente (+1 MSS por RTT) para evitar saturación.
- *Fast retransmit*: al recibir 3 ACKs duplicados (indicio de pérdida de un segmento sin esperar al timeout), se retransmite inmediatamente el segmento perdido.
- *Fast recovery*: tras fast retransmit, ssthresh se reduce a la mitad de cwnd y esta no vuelve a slow start desde cero, sino que continúa en congestion avoidance desde el nuevo ssthresh, evitando la penalización total de un timeout.

### 7. UDP

Cabecera mínima de **8 bytes**: Puerto origen (16), Puerto destino (16), Longitud (16), Checksum (16, opcional en IPv4). No hay conexión, ni confirmación, ni reordenación, ni control de flujo/congestión. Se usa cuando la velocidad y baja latencia importan más que la fiabilidad, o cuando la propia aplicación gestiona la fiabilidad: streaming, VoIP, DNS (consultas simples), DHCP, SNMP, juegos en red, NTP.

### 8. ARP y RARP

**ARP** (Address Resolution Protocol) resuelve una IP conocida a su dirección MAC dentro de la misma red local: el host emisor envía una trama **broadcast** (`ARP Request`, MAC destino `FF:FF:FF:FF:FF:FF`) preguntando "¿quién tiene la IP X?"; el propietario responde en **unicast** (`ARP Reply`) con su MAC. El resultado se almacena en la **tabla ARP** (caché) con un tiempo de vida limitado, evitando repetir la resolución en cada envío. **RARP** (Reverse ARP), en desuso, hacía lo inverso: a partir de una MAC conocida obtenía la IP asignada, útil para estaciones sin disco que arrancaban por red (sustituido por BOOTP y después DHCP).

### 9. ICMP

Protocolo de capa de red (encapsulado en IP, protocolo 1) para diagnóstico y control de errores, sin fiabilidad ni conexión.

| Tipo | Código relevante | Mensaje |
|---|---|---|
| 0 | 0 | Echo Reply (respuesta ping) |
| 3 | 0/1/3/4 | Destination Unreachable (red/host/puerto inalcanzable, fragmentación necesaria) |
| 5 | 0-3 | Redirect (ruta mejor disponible) |
| 8 | 0 | Echo Request (petición ping) |
| 11 | 0 | Time Exceeded (TTL agotado) |

**Ping** envía Echo Request (tipo 8) y espera Echo Reply (tipo 0), midiendo RTT y comprobando alcanzabilidad. **Traceroute** explota el TTL: envía paquetes con TTL=1, 2, 3... incrementalmente; cada router que descarta el paquete por TTL agotado responde con ICMP Time Exceeded (tipo 11), revelando la IP de cada salto hasta llegar al destino, que responde con Echo Reply o Port Unreachable según implementación (ICMP en Windows, UDP en Unix tradicional).

### 10. DNS

Protocolo de aplicación (puerto 53, UDP para consultas simples, TCP para transferencias de zona o respuestas >512 bytes) que traduce nombres de dominio a direcciones IP mediante una jerarquía distribuida: raíz (`.`) → dominios de nivel superior (TLD: `.es`, `.com`) → dominios de segundo nivel → subdominios. Una consulta incluye nombre, tipo de registro y clase; principales tipos de registro: **A** (IPv4), **AAAA** (IPv6), **CNAME** (alias), **MX** (servidor de correo), **NS** (servidor de nombres autoritativo), **PTR** (resolución inversa), **SOA** (autoridad de zona), **TXT** (texto libre, usado en SPF/DKIM).

### 11. DHCP

Asigna configuración IP dinámica mediante el proceso **DORA**:
1. **Discover**: el cliente, sin IP, difunde broadcast buscando servidores DHCP.
2. **Offer**: cada servidor disponible ofrece una IP y parámetros (máscara, gateway, DNS).
3. **Request**: el cliente solicita formalmente (broadcast) una de las ofertas recibidas.
4. **Acknowledge (ACK)**: el servidor elegido confirma la concesión (lease) de la dirección.

Usa los puertos UDP 67 (servidor) y 68 (cliente).

### 12. Protocolos de aplicación y puertos

| Protocolo | Puerto | Transporte | Uso |
|---|---|---|---|
| FTP (control/datos) | 21 / 20 | TCP | Transferencia de ficheros |
| SSH | 22 | TCP | Acceso remoto seguro |
| Telnet | 23 | TCP | Terminal remoto en claro (obsoleto: sin cifrado, credenciales expuestas, sustituido por SSH) |
| SMTP | 25 | TCP | Envío de correo |
| DNS | 53 | UDP/TCP | Resolución de nombres |
| DHCP | 67/68 | UDP | Configuración dinámica de red |
| HTTP | 80 | TCP | Web |
| POP3 | 110 | TCP | Descarga de correo |
| NTP | 123 | UDP | Sincronización horaria |
| IMAP | 143 | TCP | Gestión de correo en servidor |
| SNMP (agente/trap) | 161 / 162 | UDP | Gestión de red |
| HTTPS | 443 | TCP | Web cifrada (TLS) |

### Trampas habituales de examen

- ARP **no es un protocolo de capa 3 puro**: encapsula en trama de enlace pero resuelve direcciones IP; el examen suele situarlo entre capa 2 y 3 según el modelo TCP/IP (Internet) frente a OSI (frontera enlace/red).
- No confundir el **Data Offset** de TCP (longitud de cabecera) con el **IHL** de IPv4: son campos análogos pero de protocolos distintos, ambos en unidades de palabras de 32 bits.
- El **broadcast no existe en IPv6**: su función la cubre el multicast (`ff02::1` para todos los nodos del enlace); es un error muy repetido asumir que IPv6 conserva broadcast.
- Diferenciar bien **TTL** (IPv4, salto de router) del **Hop Limit** (IPv6): funcionalmente idénticos, nombre distinto.
- Cuidado con los **puertos de FTP**: 21 es control, 20 es datos (modo activo); confundirlos es error clásico.
- Recordar que **UDP no tiene control de flujo ni de congestión ni de errores más allá del checksum opcional**: no reordena ni retransmite, a diferencia de TCP.
- La **capa de sesión y presentación de OSI no tienen equivalente estructural propio en TCP/IP**: quedan absorbidas en la capa de Aplicación, lo que suele preguntarse como "¿qué capas OSI corresponden a la capa de Aplicación TCP/IP?" (respuesta: 5, 6 y 7).

## Tema 8. Internet: arquitectura de red. Origen, evolución y estado actual. Principales servicios. Protocolos HTTP, HTTPS y SSL/TLS.

### 1. Origen histórico

Internet nace de **ARPANET**, red experimental financiada por la agencia DARPA (entonces ARPA) del Departamento de Defensa de EE. UU. El primer enlace operativo se estableció el 29 de octubre de 1969 entre la Universidad de California en Los Ángeles (UCLA) y el Stanford Research Institute (SRI); poco después se sumaron UC Santa Bárbara y la Universidad de Utah, formando los cuatro nodos iniciales.

Conviene matizar un mito muy extendido en temarios de divulgación: **ARPANET no se diseñó como una red capaz de sobrevivir a un ataque nuclear**. Esa idea procede de trabajos previos de Paul Baran sobre conmutación de paquetes y redes distribuidas, pero el motivo real y documentado del proyecto ARPANET fue **compartir recursos computacionales muy caros** (los grandes ordenadores centrales de las universidades) entre centros de investigación, evitando que cada institución tuviera que duplicar hardware costoso. La resiliencia frente a fallos es una propiedad emergente de la conmutación de paquetes, no el objetivo fundacional.

El protocolo original de ARPANET fue el **NCP (Network Control Protocol)**, con limitaciones serias de direccionamiento y control de flujo. En 1974, **Vint Cerf y Robert Kahn** publicaron el diseño de **TCP/IP**, una arquitectura en capas que separaba el transporte fiable (TCP) del encaminamiento de paquetes (IP). La transición definitiva de NCP a TCP/IP se produjo el **1 de enero de 1983**, fecha conocida como el **"flag day"**, en la que todos los hosts de ARPANET migraron simultáneamente al nuevo protocolo, hito que marca el nacimiento técnico de Internet tal como se entiende hoy.

Casi una década después, entre **1989 y 1991**, **Tim Berners-Lee**, trabajando en el CERN, propuso y desarrolló la **World Wide Web**: un sistema de hipertexto distribuido que definió tres piezas fundamentales que siguen vigentes: el protocolo **HTTP**, el lenguaje de marcado **HTML** y el sistema de identificación de recursos **URI**. Es crucial distinguir con precisión **Internet** (la infraestructura física y lógica de redes interconectadas mediante TCP/IP) de la **Web** (un servicio concreto, basado en HTTP, que se ejecuta sobre esa infraestructura, al mismo nivel que el correo electrónico, la transferencia de ficheros o la videoconferencia).

### 2. Evolución y estado actual

Durante los años 90 se produjo la **explosión comercial** de Internet: la privatización del backbone NSFNET en 1995, la aparición de navegadores gráficos (Mosaic, Netscape) y la burbuja de las empresas ".com" popularizaron el acceso doméstico, inicialmente por módem telefónico y después mediante **banda ancha** (ADSL, cable, fibra óptica), que multiplicó exponencialmente el volumen de tráfico.

El crecimiento del número de dispositivos conectados llevó al **agotamiento de IPv4 (IPv4 exhaustion)**: el espacio de direcciones de 32 bits ofrece unos 4300 millones de combinaciones, insuficientes para la demanda global. IANA agotó su reserva libre en 2011, y los RIR regionales fueron agotando la suya en los años siguientes. Esto motivó el desarrollo de **IPv6**, con direcciones de 128 bits, que elimina la necesidad estructural de NAT masivo, incorpora autoconfiguración de direcciones (SLAAC) y soporte nativo de IPsec. Su despliegue, aunque avanza, convive todavía con IPv4 mediante mecanismos de doble pila y traducción.

El estado actual de Internet está definido por el **Internet de las Cosas (IoT)**: miles de millones de sensores, electrodomésticos, vehículos e infraestructuras industriales conectados permanentemente, apoyados en redes móviles 5G y en el **edge computing**, que procesa datos cerca del origen para reducir latencia.

### 3. Arquitectura jerárquica de la red

Internet no es una red plana, sino una jerarquía de operadores (ISP) organizada en niveles:

- **Tier 1**: operadores con alcance global que tienen acuerdos de **peering sin coste (settlement-free)** con el resto de Tier 1, de modo que ven la totalidad de la tabla de rutas de Internet sin necesidad de comprar tránsito a nadie. Por eso forman la llamada **"default-free zone" (DFZ)**: no necesitan una ruta por defecto porque conocen explícitamente el camino a cualquier prefijo. Ejemplos: Lumen, NTT, GTT, Telia, Tata Communications.
- **Tier 2**: operadores regionales o nacionales que combinan peering con algunas redes y compra de **tránsito** a uno o varios Tier 1 para alcanzar el resto de Internet.
- **Tier 3**: proveedores de acceso locales que únicamente compran tránsito, sin acuerdos de peering propios.

La diferencia entre **tránsito** y **peering** es un punto clásico de examen: el tránsito es un servicio de pago mediante el cual un operador entrega a otro acceso a toda la tabla de rutas de Internet; el peering es un intercambio bilateral (o multilateral) y habitualmente gratuito de tráfico limitado exclusivamente a los prefijos propios de cada red y de sus clientes directos.

Los **IXP (Internet Exchange Point, puntos neutros)** son infraestructuras físicas —conmutadores de alto rendimiento— donde múltiples redes independientes establecen peering entre sí sin necesidad de enlaces punto a punto individuales, reduciendo costes y latencia. En España destacan **ESPANIX** (Madrid), **CATNIX** (Cataluña) y **DE-CIX Madrid**.

### 4. Sistema de numeración: los RIR

La asignación de bloques de direcciones IP y de números de **Sistema Autónomo (AS)** sigue una jerarquía descendente desde IANA hacia cinco **Registros Regionales de Internet (RIR)**, cada uno responsable de una zona geográfica:

- **RIPE NCC**: Europa, Oriente Medio y Asia Central.
- **ARIN**: Norteamérica.
- **APNIC**: Asia-Pacífico.
- **LACNIC**: Latinoamérica y Caribe.
- **AFRINIC**: África.

Cada RIR asigna a los ISP y grandes organizaciones de su región tanto bloques de direcciones IP como números de AS, y mantiene los registros públicos (WHOIS) que permiten identificar al titular de cada recurso.

### 5. BGP: el protocolo que sostiene Internet

Un **Sistema Autónomo (AS)** es un conjunto de redes IP bajo una única política de administración, identificado por un número (ASN) asignado por su RIR. **BGP (Border Gateway Protocol)** es el protocolo de **encaminamiento exterior (EGP)** estándar que permite a los distintos AS intercambiar información sobre qué prefijos IP alcanzan y por qué camino.

BGP es un protocolo de **vector de ruta (path vector)**: a diferencia de un vector distancia clásico, no solo propaga una métrica, sino la lista completa de AS atravesados, el atributo **AS-PATH**. Este atributo cumple dos funciones: evitar bucles de encaminamiento (un AS descarta cualquier anuncio en el que ya aparezca su propio ASN) y servir como uno de los criterios —no el único, ya que también intervienen políticas locales de preferencia— para seleccionar la mejor ruta entre varias posibles.

BGP se describe habitualmente como el **"pegamento" de Internet** porque es el único mecanismo que permite que decenas de miles de redes completamente independientes, cada una con su propia política comercial y técnica, cooperen para ofrecer alcanzabilidad global sin ninguna autoridad centralizada que imponga las rutas.

### 6. Principales servicios de Internet

| Servicio | Protocolo(s) | Puerto típico | Función |
|---|---|---|---|
| WWW | HTTP / HTTPS | 80 / 443 | Acceso a contenido hipertexto |
| Correo electrónico | SMTP / POP3 / IMAP | 587 / 995 / 993 | Envío y recepción de mensajes |
| Transferencia de ficheros | FTP / SFTP | 21 / 22 | FTP sin cifrar; SFTP cifrado sobre SSH |
| Acceso remoto | SSH | 22 | Shell remota segura |
| Resolución de nombres | DNS | 53 | Traducción nombre ↔ IP |
| Voz sobre IP | SIP / RTP | 5060-5061 / dinámico UDP | SIP señaliza la llamada; RTP transporta audio/vídeo |
| Streaming | HLS / DASH (sobre HTTP) | 443 | Entrega adaptativa de vídeo/audio |
| Cloud computing | HTTPS/API REST | 443 | IaaS, PaaS, SaaS |

En **cloud computing**, el modelo de responsabilidad se estratifica en tres niveles: **IaaS** (infraestructura, el proveedor entrega máquinas virtuales, red y almacenamiento; ejemplo: AWS EC2), **PaaS** (plataforma, el proveedor gestiona el sistema operativo y el entorno de ejecución, y el cliente solo despliega su aplicación; ejemplo: Azure App Service) y **SaaS** (software completo entregado como servicio, sin gestión de infraestructura por parte del cliente; ejemplo: Microsoft 365).

### 7. El protocolo HTTP

Un mensaje HTTP se compone siempre de tres partes: una **línea de inicio** (en la petición, método + URI + versión; en la respuesta, versión + código de estado + frase explicativa), un bloque de **cabeceras** en formato clave-valor, y opcionalmente un **cuerpo**, separado de las cabeceras por una línea en blanco.

| Método | Idempotente | Seguro (safe) | Uso típico |
|---|---|---|---|
| GET | Sí | Sí | Obtener un recurso |
| HEAD | Sí | Sí | Como GET, sin cuerpo de respuesta |
| OPTIONS | Sí | Sí | Consultar capacidades (p. ej. preflight CORS) |
| PUT | Sí | No | Reemplazar un recurso completo |
| DELETE | Sí | No | Eliminar un recurso |
| PATCH | No (en general) | No | Modificación parcial de un recurso |
| POST | No | No | Crear un recurso o ejecutar una acción |

Es habitual confundir idempotencia con seguridad: **idempotente** significa que repetir la operación N veces produce el mismo estado final que ejecutarla una vez; **seguro** significa que la operación no modifica el estado del servidor. GET y HEAD son las únicas verdaderamente seguras e idempotentes a la vez; PUT y DELETE son idempotentes pero no seguras.

Los **códigos de estado** se agrupan por familia según su primer dígito:

- **1xx (informativo)**: 100 Continue.
- **2xx (éxito)**: 200 OK, 201 Created (recurso creado, típico tras POST), 204 No Content (éxito sin cuerpo de respuesta).
- **3xx (redirección)**: 301 Moved Permanently (redirección permanente, cacheable), 302 Found (redirección temporal), 304 Not Modified (el recurso en caché sigue siendo válido, respuesta a una petición condicional con ETag/If-Modified-Since).
- **4xx (error del cliente)**: 400 Bad Request, 401 Unauthorized (falta o falla la autenticación), 403 Forbidden (autenticado pero sin permiso), 404 Not Found, 405 Method Not Allowed, 409 Conflict (choque de estado, p. ej. edición concurrente), 429 Too Many Requests (límite de tasa superado).
- **5xx (error del servidor)**: 500 Internal Server Error, 502 Bad Gateway (respuesta inválida de un servidor upstream), 503 Service Unavailable (servicio sobrecargado o en mantenimiento).

Entre las cabeceras más relevantes: **Content-Type** (tipo MIME del cuerpo), **Cache-Control** (directivas de cacheo, como `max-age` o `no-cache`), **ETag** (identificador de versión del recurso usado en validación condicional de caché) y **Authorization** (credenciales de acceso, típicamente un esquema `Bearer` con un token).

### 8. Evolución de las versiones de HTTP

| Versión | Año | Características clave |
|---|---|---|
| HTTP/0.9 | 1991 | Solo método GET, sin cabeceras, respuesta limitada a HTML |
| HTTP/1.0 | 1996 | Cabeceras, códigos de estado, Content-Type; nueva conexión TCP por petición |
| HTTP/1.1 | 1997 | Conexiones persistentes (keep-alive) por defecto, pipelining (poco usado por head-of-line blocking), cabecera Host obligatoria (virtual hosting) |
| HTTP/2 | 2015 | Basado en SPDY; multiplexación de streams sobre una única conexión TCP, compresión de cabeceras (HPACK), server push, formato binario |
| HTTP/3 | 2022 | Transporte sobre QUIC/UDP en lugar de TCP; elimina el head-of-line blocking a nivel de transporte porque cada stream se recupera de pérdidas de forma independiente; integra TLS 1.3 en el establecimiento de la conexión |

### 9. HTTPS y TLS

**SSL** (Secure Sockets Layer), desarrollado originalmente por Netscape, quedó obsoleto tras la publicación en 2014 del ataque **POODLE**, que explotaba una debilidad del relleno (padding) en el modo CBC de SSLv3 para forzar una degradación (downgrade) y descifrar tráfico. Desde entonces SSL en todas sus versiones, y posteriormente también TLS 1.0 y 1.1 (deprecados formalmente por la RFC 8996 en 2021), se consideran inseguros.

**TLS 1.3** (2018) mejora a **TLS 1.2** (2008) en varios aspectos: reduce el establecimiento de la conexión a **1-RTT** (o **0-RTT** con reanudación de sesión, frente a los 2-RTT típicos de TLS 1.2), elimina algoritmos y modos débiles (RC4, cifrado estático RSA, renegociación insegura) y **obliga a usar intercambio de claves efímero** (ECDHE/DHE), garantizando siempre *forward secrecy*.

El **handshake completo de TLS 1.2** sigue estos pasos:

1. **ClientHello**: el cliente envía las versiones de TLS soportadas, la lista de *cipher suites*, un valor aleatorio (`random_client`) y extensiones como SNI.
2. **ServerHello**: el servidor elige versión y cipher suite, y envía su propio aleatorio (`random_server`).
3. **Certificate**: el servidor envía su certificado X.509 y la cadena intermedia.
4. **ServerKeyExchange** (en modos DHE/ECDHE): parámetros efímeros de intercambio de claves, firmados con la clave privada del certificado.
5. **ServerHelloDone**.
6. El cliente **verifica la cadena de confianza**: firma de cada certificado, vigencia temporal, coincidencia del dominio con el CN/SAN, y opcionalmente estado de revocación (CRL/OCSP), hasta llegar a una CA raíz preinstalada en su almacén de confianza.
7. **ClientKeyExchange**: el cliente aporta su parte del intercambio DHE/ECDHE.
8. Ambas partes derivan de forma independiente el mismo *master secret* y, de él, las claves de sesión simétricas.
9. **ChangeCipherSpec + Finished** (cliente): primer mensaje ya cifrado, con un resumen de todo el handshake para detectar manipulaciones.
10. **ChangeCipherSpec + Finished** (servidor): confirmación equivalente.
11. Comienza el tráfico de aplicación cifrado simétricamente (típicamente AES-GCM).

Cada elemento aporta una propiedad de seguridad distinta: el **cifrado simétrico de sesión** aporta confidencialidad; el **MAC/AEAD** integrado en cada registro aporta integridad; el **certificado X.509 y la firma del ServerKeyExchange** aportan autenticación del servidor; y el uso de claves **efímeras (DHE/ECDHE)** aporta *forward secrecy*: aunque en el futuro se comprometa la clave privada del servidor, las sesiones pasadas no pueden descifrarse retroactivamente porque las claves de sesión se descartan tras el uso.

Un **certificado X.509** contiene, entre otros campos, el **CN** (Common Name, hoy en desuso como criterio de validación), el **SAN** (Subject Alternative Name, lista de dominios válidos que sí se valida realmente), el periodo de validez (notBefore/notAfter) y forma parte de una **cadena de confianza**: certificado hoja firmado por una CA intermedia, que a su vez está firmada por una CA raíz de confianza.

### 10. Cookies, sesión y JWT

HTTP es un protocolo **sin estado (stateless)**: cada petición se procesa de forma independiente, sin memoria de peticiones anteriores. Las **cookies** (cabeceras `Set-Cookie` / `Cookie`) permiten simular estado asociando al cliente un identificador de sesión que el servidor almacena y consulta en cada petición; atributos como `Secure`, `HttpOnly` y `SameSite` mitigan robo de cookies y ataques CSRF/XSS.

El **JWT (JSON Web Token)** es una alternativa moderna: un token autocontenido y firmado, con estructura `header.payload.signature`, que el servidor puede validar criptográficamente sin necesidad de mantener estado ni consultar una base de datos de sesiones, lo que lo hace especialmente adecuado en arquitecturas distribuidas y microservicios, a costa de una revocación anticipada más compleja que con sesiones tradicionales.

### Trampas habituales de examen

1. Confundir **Internet** (infraestructura TCP/IP) con la **Web** (servicio HTTP): el correo o el FTP son servicios de Internet, no de la Web.
2. Dar por cierto que ARPANET se diseñó para resistir un ataque nuclear: el motivo documentado fue compartir recursos computacionales caros entre instituciones.
3. Confundir **peering** (gratuito, bilateral) con **tránsito** (de pago, acceso a toda la tabla de rutas): un Tier 1 se define por no pagar tránsito a nadie, no simplemente por su tamaño.
4. Igualar **idempotencia** con **seguridad (safe)** en los métodos HTTP: PUT y DELETE son idempotentes pero no seguras; solo GET/HEAD son ambas cosas.
5. Asumir que "HTTPS" implica SSL vigente: SSL está obsoleto desde POODLE y HTTPS actual se basa en TLS (idealmente 1.3).

## Tema 9. Seguridad y protección en redes de comunicaciones. Seguridad perimetral. Acceso remoto seguro a redes. Redes privadas virtuales (VPN). Seguridad en el puesto del usuario.

### 1. Introducción

La seguridad en redes de comunicaciones se articula en capas: defensa perimetral (frontera entre red confiable y no confiable), segmentación interna, acceso remoto controlado y protección del endpoint. Ningún control aislado es suficiente; el paradigma actual es la **defensa en profundidad**, reforzado por el modelo **Zero Trust**, que asume que la amenaza puede originarse también dentro del perímetro.

### 2. Amenazas de red

**Sniffing (captura pasiva de paquetes).** Un atacante con acceso al segmento de red (interfaz en modo promiscuo, puerto SPAN mal configurado, o hub en vez de switch) captura tráfico en claro. Herramientas como Wireshark o tcpdump permiten extraer credenciales, cookies de sesión o datos sensibles si no hay cifrado extremo a extremo. Es pasivo: no altera el tráfico, por lo que es difícil de detectar.

**Spoofing.** Suplantación de identidad a distintos niveles:
- *IP spoofing*: se falsifica la dirección IP origen de los paquetes para ocultar el origen real o para explotar confianza basada en IP (ataques de reflexión/amplificación).
- *MAC spoofing*: se cambia la dirección MAC de la interfaz para eludir filtrados por MAC o suplantar un host autorizado en la red local.
- *ARP spoofing (ARP poisoning)*: el atacante envía respuestas ARP falsas asociando su propia MAC a la IP de la puerta de enlace u otro host, de modo que el tráfico de la víctima pasa por el atacante. Es la base técnica más habitual para montar un MITM en redes locales, ya que ARP no autentica sus respuestas.

**DoS vs DDoS.** Un ataque de Denegación de Servicio (DoS) busca agotar un recurso (ancho de banda, CPU, memoria, conexiones) para que el servicio deje de responder. Si el ataque se distribuye desde múltiples orígenes (habitualmente una botnet), se denomina DDoS. Se clasifican en:
- *Volumétricos*: saturan el ancho de banda disponible. Ejemplo: **UDP flood**, envío masivo de datagramas UDP a puertos aleatorios que fuerza al host a responder con ICMP "puerto inalcanzable", agotando recursos y enlace.
- *De protocolo*: explotan el comportamiento de un protocolo para agotar recursos de estado en dispositivos intermedios (firewalls, balanceadores). Ejemplo: **SYN flood**, el atacante envía múltiples segmentos TCP SYN con IP origen falsificada y nunca completa el three-way handshake; el servidor mantiene entradas en la cola de conexiones semiabiertas hasta agotar la tabla.
- *De aplicación (capa 7)*: consumen recursos del propio servicio con peticiones aparentemente legítimas. Ejemplo: **Slowloris**, mantiene abiertas múltiples conexiones HTTP enviando cabeceras muy lentamente y de forma incompleta, agotando el pool de workers del servidor web sin apenas consumir ancho de banda.

**Man-in-the-middle (MITM).** El atacante se sitúa entre dos partes que creen comunicarse directamente, pudiendo leer y/o modificar el tráfico. Vectores típicos: ARP spoofing en LAN, rogue AP en Wi-Fi, DNS spoofing, o downgrade de TLS. La mitigación pasa por cifrado y autenticación mutua (TLS con validación de certificado, HSTS, DNSSEC).

### 3. Seguridad perimetral: el firewall

**Filtrado de paquetes sin estado (stateless).** Evalúa cada paquete de forma aislada contra una tabla de reglas basada en IP origen/destino, puerto y protocolo, sin recordar el contexto de la conexión. Ejemplo de tabla de reglas:

| # | Origen | Destino | Protocolo | Puerto | Acción |
|---|--------|---------|-----------|--------|--------|
| 1 | any | 10.0.0.10 | TCP | 443 | ALLOW |
| 2 | any | 10.0.0.10 | TCP | 22 | DENY |
| 3 | 10.0.0.0/24 | any | TCP | any | ALLOW |
| 4 | any | any | any | any | DENY |

El problema: para permitir el tráfico de respuesta hay que abrir reglas simétricas manualmente, ampliando innecesariamente la superficie de exposición.

**Stateful inspection.** Mantiene una tabla de estados de conexión (IP/puerto origen-destino, protocolo, número de secuencia, estado TCP) y solo permite el tráfico de retorno que corresponde a una conexión previamente iniciada y autorizada, sin necesidad de reglas explícitas de vuelta. Es superior porque reduce drásticamente la superficie de reglas, entiende el ciclo de vida de la conexión (SYN, ESTABLISHED, FIN) y detecta paquetes anómalos fuera de contexto (por ejemplo, un ACK sin SYN previo).

**Proxy de aplicación / WAF.** Opera en capa 7, terminando la conexión del cliente e iniciando una nueva hacia el servidor real, inspeccionando el contenido de la aplicación (cabeceras HTTP, payload, patrones de inyección SQL o XSS). Un WAF protege específicamente aplicaciones web frente a ataques de la capa de aplicación que un firewall de capas 3-4 no puede detectar.

**NGFW (Next-Generation Firewall).** Integra stateful inspection con IPS embebido, control de aplicaciones (identificación del tráfico por aplicación real, no solo por puerto), inspección SSL/TLS (descifrado mediante posición man-in-the-middle controlada, con certificado propio de confianza en los clientes) y, a menudo, filtrado por identidad de usuario y reputación de amenazas.

### 4. DMZ (zona desmilitarizada)

La DMZ es un segmento de red intermedio donde se ubican los servicios que deben ser accesibles desde Internet (servidor web, correo, DNS público, proxy inverso), aislándolos tanto de Internet como de la red interna. Si un servidor de la DMZ es comprometido, el atacante no obtiene acceso directo a la LAN.

**Arquitectura con dos firewalls (back-to-back / screened subnet):**

```
Internet --- [FW externo] --- DMZ (web, mail, DNS) --- [FW interno] --- LAN interna
```

El firewall externo filtra tráfico de Internet hacia la DMZ; el firewall interno filtra el tráfico DMZ→LAN, mucho más restrictivo, permitiendo solo los flujos estrictamente necesarios (p. ej. el servidor web consultando una BD interna por un puerto concreto).

**Arquitectura de tres patas (three-legged / single firewall):** un único firewall con tres interfaces (externa, DMZ, interna), cada una con su propio conjunto de reglas. Es más económica pero concentra el punto de fallo: un fallo de configuración en el firewall único compromete todos los segmentos a la vez, mientras que el modelo de dos firewalls permite incluso emplear fabricantes distintos para evitar que una misma vulnerabilidad afecte a ambos.

### 5. IDS vs IPS

| Aspecto | IDS | IPS |
|---|---|---|
| Posición | Fuera de banda (analiza copia del tráfico, p. ej. vía SPAN/TAP) | En línea (el tráfico atraviesa el dispositivo) |
| Capacidad de bloqueo | No; solo alerta | Sí; puede descartar el paquete o cerrar la conexión |
| Impacto en latencia | Ninguno | Introduce latencia y es punto único de fallo |
| Falso positivo | Genera alerta innecesaria (molesto, no interrumpe servicio) | Puede bloquear tráfico legítimo (impacto directo en disponibilidad) |
| Falso negativo | Amenaza real no detectada | Amenaza real no detectada, sin ninguna capa que la frene |

Ambos pueden basar la detección en **firmas** (patrones conocidos de ataque, muy precisos pero ciegos ante amenazas nuevas/0-day) o en **anomalías** (modelan comportamiento "normal" y alertan sobre desviaciones, capaces de detectar ataques desconocidos pero con mayor tasa de falsos positivos).

### 6. Segmentación de red y Zero Trust

**VLAN.** Segmentación lógica a nivel 2 que agrupa puertos de switch en dominios de difusión independientes, aunque compartan la misma infraestructura física. El tráfico entre VLAN requiere enrutamiento (router-on-a-stick o capa 3 en el propio switch).

**ACL entre segmentos.** Listas de control de acceso aplicadas en el punto de enrutamiento entre VLAN o subredes, que restringen qué flujos concretos pueden cruzar de un segmento a otro, aplicando el principio de mínimo privilegio también a nivel de red.

**Zero Trust vs modelo perimetral clásico.** El modelo perimetral clásico asume que todo lo que está dentro de la red es confiable ("castillo con foso"): una vez dentro, el movimiento lateral es prácticamente libre. Zero Trust invierte el principio: *"never trust, always verify"*. Cada petición de acceso se autentica y autoriza individualmente, con independencia de si el origen está dentro o fuera del perímetro, aplicando **microsegmentación** (políticas granulares por carga de trabajo o aplicación, no por segmento de red completo) y verificación continua del contexto (identidad, estado del dispositivo, ubicación, comportamiento).

### 7. Acceso remoto seguro

**SSH.** Autenticación por par de claves pública/privada: el cliente genera un par de claves; la clave pública se instala en `authorized_keys` del servidor. En la conexión, el servidor envía un reto cifrado con la clave pública, y el cliente demuestra posesión de la privada firmando/descifrando dicho reto sin transmitirla nunca. Funcionalidades avanzadas:
- *Agent forwarding*: permite usar el par de claves cargado en el agente SSH local para autenticarse en un tercer host saltando desde el servidor intermedio, sin copiar la clave privada a este.
- *Port forwarding local* (`-L`): expone un puerto remoto como si fuera local, túnel cliente→servidor→destino.
- *Port forwarding remoto* (`-R`): expone un puerto local en el servidor remoto, túnel inverso.
- *Port forwarding dinámico* (`-D`): levanta un proxy SOCKS local que enruta el tráfico a través del túnel SSH.

**RDP con Network Level Authentication (NLA).** Obliga a autenticar al usuario antes de establecer la sesión gráfica completa, reduciendo la superficie expuesta a ataques de fuerza bruta y explotación previa a autenticación.

**MFA.** Actualmente es requisito estándar para cualquier acceso remoto, combinando algo que se sabe (contraseña), algo que se tiene (token/app OTP) o algo que se es (biometría), mitigando el riesgo de credenciales comprometidas.

### 8. ZTNA vs VPN tradicional

Una VPN tradicional concede acceso a nivel de red: una vez conectado, el usuario obtiene una IP dentro de la red corporativa y, salvo segmentación adicional, visibilidad de gran parte de ella. **ZTNA (Zero Trust Network Access)** concede acceso granular por aplicación: el usuario nunca se conecta "a la red", sino a un broker que, tras verificar continuamente identidad, dispositivo y contexto, media el acceso únicamente al recurso concreto autorizado, sin exponer el resto de la infraestructura ni asignar una IP interna visible.

### 9. Redes privadas virtuales (VPN)

**Acceso remoto (host-to-site).** Un usuario individual se conecta desde un cliente VPN hasta una pasarela corporativa, obteniendo acceso a los recursos internos como si estuviera en la LAN.

```
[Portátil usuario] === túnel cifrado === [Gateway VPN] --- LAN corporativa
```

**Sitio a sitio (site-to-site).** Une dos redes completas (p. ej. sede central y delegación) a través de un túnel permanente entre dos gateways, transparente para los equipos de cada extremo.

```
LAN Sede A --- [Gateway A] === túnel cifrado (Internet) === [Gateway B] --- LAN Sede B
```

### 10. IPsec en profundidad

IPsec es un conjunto de protocolos de capa de red que proporciona confidencialidad, integridad y autenticación.

**AH (Authentication Header).** Protege la integridad y autentica el origen de todo el paquete IP (incluida la cabecera, salvo campos mutables), pero **no cifra el contenido**: los datos viajan en claro, solo garantizados frente a manipulación.

**ESP (Encapsulating Security Payload).** Proporciona confidencialidad (cifrado del payload), integridad y autenticación del origen. Es el protocolo más usado en la práctica porque, a diferencia de AH, sí cifra los datos.

| Aspecto | AH | ESP |
|---|---|---|
| Confidencialidad (cifrado) | No | Sí |
| Integridad y autenticación | Sí | Sí |
| Protege cabecera IP externa | Sí (excepto campos mutables) | No en modo transporte |
| Compatibilidad con NAT | Problemática (NAT modifica la cabecera que AH firma) | Mejor (con NAT-T) |
| Uso típico actual | Residual | Estándar de facto |

**SA (Security Association).** Es el contrato unidireccional que define los parámetros de seguridad (algoritmo, clave, protocolo) entre dos extremos; una comunicación bidireccional requiere dos SA, una por sentido.

**IKE (Internet Key Exchange).** Negocia las SA de forma automática y segura, en dos fases:
- *Fase 1*: establece un canal seguro autenticado entre los gateways (la propia IKE SA), negociando algoritmo de cifrado/hash, método de autenticación y realizando el intercambio Diffie-Hellman. Puede operar en modo *main* (6 mensajes, protege la identidad) o *aggressive* (3 mensajes, más rápido pero expone identidad).
- *Fase 2* (modo *quick*): usando el canal seguro de la fase 1, negocia las SA de IPsec propiamente dichas (las que protegerán el tráfico de datos).

IKEv2, frente a IKEv1, simplifica el intercambio de mensajes, integra soporte nativo de NAT-T y MOBIKE (continuidad de sesión ante cambio de IP, clave para dispositivos móviles), y mejora la resistencia frente a ataques DoS durante la negociación.

**Modo túnel vs modo transporte.**

```
Modo transporte (host a host, protege solo el payload):
[IP original][AH/ESP][TCP][Datos]

Modo túnel (red a red o acceso remoto, protege el paquete IP completo):
[IP nueva][AH/ESP][IP original][TCP][Datos]
```

En modo transporte se conserva la cabecera IP original y solo se protege el payload de nivel superior; se usa típicamente en comunicación extremo a extremo entre dos hosts. En modo túnel, el paquete IP original completo se encapsula dentro de uno nuevo con nueva cabecera IP (la de los gateways), ocultando las direcciones internas reales; es el modo empleado en VPN sitio a sitio y acceso remoto.

### 11. VPN SSL/TLS y OpenVPN

Las VPN basadas en SSL/TLS operan típicamente sobre el puerto 443/TCP, lo que les permite atravesar con facilidad NAT, proxies y firewalls restrictivos que ya permiten tráfico HTTPS saliente, evitando los problemas de NAT traversal propios de IPsec/AH y facilitando el despliegue sin abrir puertos adicionales. **OpenVPN** es la implementación de referencia: usa la librería OpenSSL para cifrado y autenticación (certificados X.509 o clave precompartida), puede transportarse sobre TCP o UDP, y es altamente configurable en cuanto a enrutamiento y políticas de acceso.

### 12. WireGuard

WireGuard representa la siguiente generación de VPN, diseñada para simplicidad y rendimiento:
- **Código reducido**: su base de código (unas pocas miles de líneas frente a las decenas de miles de IPsec/OpenVPN) reduce drásticamente la superficie de auditoría y de vulnerabilidades.
- **Criptografía fija**: no negocia suites de cifrado (a diferencia de IPsec/TLS); usa un conjunto moderno predefinido (ChaCha20 para cifrado simétrico, Curve25519 para intercambio de claves, BLAKE2 para hash), eliminando la complejidad y los riesgos de negociaciones débiles.
- **Rendimiento**: al integrarse a nivel de kernel con un diseño minimalista, ofrece latencia y throughput superiores a IPsec y OpenVPN en la mayoría de escenarios.

### 13. Seguridad en el puesto del usuario

**EDR vs antivirus tradicional.** El antivirus clásico detecta basándose en firmas de malware conocido, siendo ciego ante amenazas nuevas o polimórficas. **EDR (Endpoint Detection and Response)** monitoriza continuamente el comportamiento del endpoint (procesos, conexiones, cambios en el sistema), correlaciona eventos para detectar patrones sospechosos aunque no exista firma previa, y permite respuesta activa (aislar el equipo, matar procesos, retroceder cambios).

**Cifrado de disco.** BitLocker (Windows) se apoya en el chip **TPM** para almacenar la clave de cifrado de forma segura y verificar la integridad del arranque, impidiendo el acceso a los datos si el disco se extrae. LUKS cumple la función equivalente en Linux.

**Gestión de parches del endpoint.** Actualización sistemática y auditada del sistema operativo y aplicaciones para cerrar vulnerabilidades conocidas antes de que sean explotadas, habitualmente mediante WSUS, SCCM o soluciones de gestión centralizada.

**DLP (Data Loss Prevention).** Conjunto de controles que detectan y bloquean la fuga de información sensible. Ejemplo de política: bloquear la copia a USB o el adjunto en correo saliente de cualquier fichero que contenga patrones de DNI/NIF o números de tarjeta de crédito.

**Mínimo privilegio.** El usuario opera con el menor nivel de permisos necesario para su función, limitando el impacto si su cuenta o equipo es comprometido.

**Control de dispositivos USB.** Restricción o bloqueo de almacenamiento extraíble no autorizado, frente a fuga de datos e introducción de malware.

**Firewall personal.** Filtrado de tráfico a nivel de host, complementario al perimetral, relevante especialmente cuando el equipo sale de la red corporativa.

**Concienciación anti-phishing.** El factor humano es el vector de entrada más explotado; la formación continua constituye una capa de defensa tan crítica como los controles técnicos.

### Trampas habituales de examen

1. Confundir AH y ESP: **AH no cifra**, solo autentica e integra; el examen suele plantear un escenario que exige confidencialidad, donde AH sería incorrecto.
2. Creer que IDS puede bloquear tráfico: el IDS solo alerta (fuera de banda); el bloqueo en línea es exclusivo del IPS.
3. Confundir modo túnel y modo transporte: túnel encapsula el paquete IP completo (nueva cabecera IP), transporte protege solo el payload conservando la IP original.
4. Asumir que VPN y ZTNA son equivalentes: la VPN da acceso a la red; ZTNA da acceso granular por aplicación con verificación continua, sin exponer el resto de la red.
5. Situar el firewall interno de la DMZ con las mismas reglas permisivas que el externo: el firewall entre DMZ y LAN debe ser el más restrictivo de toda la arquitectura, precisamente porque protege el activo de mayor valor.

## Tema 10. Redes locales. Tipología. Técnicas de transmisión. Métodos de acceso. Dispositivos de interconexión.

### 1. LAN, MAN y WAN: criterios de distinción

Una **LAN** (Local Area Network) interconecta equipos en un área geográfica reducida (un edificio, un campus), bajo **propiedad y administración privada** de una única organización, con **alta velocidad** (típicamente de 100 Mbps a 100 Gbps) y **tasa de error muy baja** gracias a la corta longitud del cableado y al medio controlado.

Una **MAN** (Metropolitan Area Network) cubre una ciudad o área metropolitana (decenas de km), suele apoyarse en infraestructura de operadores (fibra oscura, anillos SDH/Carrier Ethernet) y puede tener administración mixta (pública o de un operador que presta servicio a varias organizaciones). Velocidad intermedia-alta y tasa de error algo mayor que la LAN por la mayor distancia y número de segmentos intermedios.

Una **WAN** (Wide Area Network) enlaza LANs y MANs a escala nacional o internacional, atraviesa infraestructura de **terceros** (operadores de telecomunicaciones), su administración es distribuida entre múltiples organismos, la velocidad por enlace es tradicionalmente menor que en LAN (aunque los backbones actuales alcanzan cientos de Gbps) y la **tasa de error y latencia son mayores** por la distancia, el número de saltos y la heterogeneidad de medios (satélite, fibra submarina, radioenlaces).

El criterio distintivo clave no es solo la distancia sino la **combinación** extensión + propiedad + velocidad + fiabilidad: una LAN puede ser un campus universitario de varios km si toda la infraestructura pertenece a la misma entidad.

### 2. Topologías de red

**Bus.** Todos los nodos comparten un único cable troncal con terminadores en los extremos que evitan reflexiones de señal.

```
──┬────┬────┬────┬──
  A    B    C    D
```
Ventajas: cableado mínimo, económica, fácil de extender. Inconvenientes: un corte en el troncal deja la red inoperativa, difícil diagnóstico de fallos, degradación del rendimiento al crecer el número de nodos (medio compartido, más colisiones).

**Anillo.** Cada nodo se conecta a sus dos vecinos formando un bucle cerrado; la información circula en una dirección (o dos, si es doble anillo).

```
   A───B
   │   │
   D───C
```
Ventajas: no hay colisiones si se usa paso de testigo, rendimiento predecible. Inconvenientes: el fallo de un nodo o enlace puede romper el anillo completo (mitigado con anillo doble). **FDDI** usa **doble anillo contrarrotatorio**: un anillo primario para datos y uno secundario de respaldo que gira en sentido opuesto; ante la rotura de un enlace, las estaciones adyacentes al corte "envuelven" (*wrap*) el tráfico reconectando primario y secundario, reconstruyendo un anillo lógico único y manteniendo la conectividad sin intervención manual.

**Estrella.** Todos los nodos se conectan a un elemento central (hub o switch).

```
       A
       │
   B───H───C
       │
       D
```
Ventajas: el fallo de un enlace o nodo periférico no afecta al resto, gestión y diagnóstico centralizados, es la topología física dominante actual. Inconvenientes: el nodo central es punto único de fallo (SPOF) y limita el cableado total requerido.

**Malla.** Cada nodo se conecta directamente con varios (malla parcial) o todos (malla completa) los demás.

```
Malla completa:      Malla parcial:
A───B                A───B
│╲ ╱│                │    
│ ╳ │                C───D
│╱ ╲│
C───D
```
Ventajas: máxima redundancia y tolerancia a fallos, múltiples caminos alternativos. Inconvenientes: coste de cableado que crece con n(n-1)/2 en malla completa, complejidad de gestión; se usa típicamente en backbones y WAN, no en LAN de usuario final.

**Árbol/jerárquica.** Combinación de estrellas enlazadas en una estructura jerárquica con un nodo raíz.

```
          Raíz
        /      \
      N1        N2
     /  \          \
    H1   H2         H3
```
Ventajas: escalabilidad, segmentación natural del tráfico por niveles (acceso-distribución-núcleo), facilita la administración jerárquica. Inconvenientes: el fallo de un nodo intermedio aísla a toda su rama; requiere protocolos de redundancia (STP) si se añaden enlaces cruzados para evitar bucles.

### 3. Topología física vs topología lógica

La **topología física** describe el cableado real y la disposición de los dispositivos; la **topología lógica** describe cómo circulan realmente las señales y se comparte el medio, independientemente del cableado. El ejemplo clásico es **Ethernet 10BASE-T**: físicamente los equipos se cablean en **estrella** hacia un hub, pero lógicamente el hub se comporta como un **bus compartido**, ya que repite eléctricamente cualquier señal recibida a todos los puertos, de modo que todas las estaciones compiten por el mismo dominio de colisión como si estuvieran en un único cable. Con la sustitución del hub por un switch, la topología lógica pasa a ser de **enlace punto a punto conmutado**, aunque la topología física de estrella no cambia.

### 4. Técnicas de transmisión

**Transmisión en banda base (baseband).** Usa todo el ancho de banda del medio para una única señal digital que ocupa el cable completo en un momento dado; es bidireccional (half o full-duplex) pero no permite multiplexar varias señales simultáneas por división de frecuencia. Es el modelo usado por Ethernet (10BASE-T, 100BASE-TX, etc.).

Como la señal es puramente digital (secuencia de unos y ceros), es necesaria una **codificación de línea** para: (1) proporcionar **sincronización de reloj** entre emisor y receptor sin necesitar un canal de reloj separado —evitando largas secuencias sin transición que impiden al receptor recuperar el "tic" de bit—, (2) eliminar la componente de continua (DC) que degradaría la señal en transformadores/acopladores, y (3) permitir detección de errores básica.

- **Manchester** (Ethernet 10 Mbps): cada bit se codifica mediante una transición a mitad del intervalo de bit; en el convenio IEEE 802.3 una transición ascendente representa un "1" y una descendente un "0" (el Ethernet DIX original usa el convenio inverso).

```
Bit:        1        0        1        0
Nivel:    __|‾‾    ‾‾|__    __|‾‾    ‾‾|__
Transición:  ↑ (subida)  ↓ (bajada)  ↑          ↓
```
Garantiza siempre una transición por bit (autosincronización) a costa de duplicar la tasa de baudios respecto a la tasa de bits (ineficiencia espectral del 50%).

- **4B/5B** (usado en FDDI y como base de 100BASE-TX): agrupa 4 bits de datos y los codifica en un símbolo de 5 bits de un conjunto que garantiza un máximo de transiciones nulas consecutivas, mejorando la eficiencia frente a Manchester (80% de eficiencia frente al 50%).
- **8B/10B** (Gigabit Ethernet 1000BASE-X sobre fibra, y otros buses serie de alta velocidad): codifica 8 bits en 10, garantizando balance DC y densidad mínima de transiciones; eficiencia del 80%, con mejor control de disparidad que 4B/5B.

**Transmisión en banda ancha (broadband).** Divide el ancho de banda del medio en múltiples canales de frecuencia independientes mediante **FDM** (Frequency Division Multiplexing), permitiendo transmitir varias señales analógicas o digitales moduladas simultáneamente por el mismo cable, cada una en su propia sub-banda separada por bandas de guarda. Es la técnica empleada en redes de **CATV/HFC** (Hybrid Fiber-Coaxial), donde en un mismo cable coaxial conviven canales de televisión, telefonía y datos (DOCSIS), cada servicio ocupando un rango de frecuencias reservado.

### 5. Evolución de Ethernet

| Estándar | Velocidad | Medio | Distancia máxima |
|---|---|---|---|
| 10BASE-T | 10 Mbps | Par trenzado UTP Cat3/Cat5 | 100 m |
| 100BASE-TX (Fast Ethernet) | 100 Mbps | UTP Cat5 (2 pares) | 100 m |
| 1000BASE-T (Gigabit Ethernet) | 1000 Mbps | UTP Cat5e/Cat6 (4 pares) | 100 m |
| 1000BASE-SX/LX | 1000 Mbps | Fibra multimodo/monomodo | 550 m / 5 km |
| 10GBASE-T | 10 Gbps | UTP Cat6a/Cat7 | 100 m (55 m en Cat6) |
| 40GBASE-T / 40GbE fibra | 40 Gbps | Cat8 / fibra OM4 | 30 m / 100–400 m |
| 100GBASE-SR4/LR4 | 100 Gbps | Fibra multimodo/monomodo | 100 m / 10 km |

La tendencia constante es que cada salto de velocidad exige medios de mayor calidad (más pares aprovechados, categorías superiores de cable o migración a fibra) al acortarse el margen de ruido disponible por bit.

### 6. Formato de la trama Ethernet (IEEE 802.3)

| Campo | Tamaño |
|---|---|
| Preámbulo | 7 bytes (patrón 10101010… para sincronización) |
| SFD (Start Frame Delimiter) | 1 byte (10101011, marca el inicio real de la trama) |
| MAC destino | 6 bytes |
| MAC origen | 6 bytes |
| EtherType / Longitud | 2 bytes (valor ≥ 1536 = EtherType; valor ≤ 1500 = longitud de datos, IEEE 802.3 clásico) |
| Datos (payload) | 46–1500 bytes (se rellena con *padding* si es menor de 46) |
| FCS (Frame Check Sequence) | 4 bytes (CRC-32 para detección de errores) |

La trama mínima es de 64 bytes (sin contar preámbulo+SFD) y la máxima estándar de 1518 bytes; las tramas *jumbo* (hasta 9000 bytes de payload) son una extensión no estandarizada universalmente pero muy usada en redes de almacenamiento y datacenter.

### 7. Direccionamiento MAC

Una dirección MAC tiene **48 bits** (6 bytes), representada habitualmente en notación hexadecimal separada por dos puntos o guiones (p. ej. `00:1A:2B:3C:4D:5E`). Los 24 bits más significativos constituyen el **OUI** (Organizationally Unique Identifier), asignado por el IEEE a cada fabricante, y los 24 bits restantes son un número de serie asignado libremente por el fabricante, garantizando (en teoría) unicidad global.

El bit menos significativo del primer byte (bit I/G) distingue **unicast** (0, dirige a una única interfaz) de **multicast** (1, dirige a un grupo de interfaces); la dirección **broadcast** es el caso especial de todos los bits a 1 (`FF:FF:FF:FF:FF:FF`), dirigida a todas las estaciones del dominio de difusión. El segundo bit del primer byte (bit U/L) indica si la dirección es universal (asignada de fábrica) o administrada localmente (modificada por software).

### 8. Métodos de acceso al medio

**CSMA/CD** (Carrier Sense Multiple Access with Collision Detection), usado en Ethernet clásico half-duplex sobre medio compartido:
1. **Escuchar** el medio (*carrier sense*); si está ocupado, esperar.
2. Si el medio está libre, **transmitir**.
3. Mientras se transmite, seguir escuchando para **detectar colisión** (superposición de señales, nivel eléctrico anómalo).
4. Si se detecta colisión, emitir una **señal de jam** (32-48 bits) para asegurar que todas las estaciones implicadas la perciban.
5. Aplicar **backoff exponencial binario**: cada estación espera un número aleatorio de intervalos de tiempo (*slot time*) entre 0 y 2ⁿ−1, donde n es el número de colisiones consecutivas sufridas (con tope, típicamente n≤10, tras el cual se informa de error de exceso de colisiones).
6. Reintentar desde el paso 1.

En redes **full-duplex modernas conmutadas** (switch a switch o switch a NIC) cada enlace es punto a punto con canales de transmisión y recepción independientes, por lo que **no puede haber colisiones** y CSMA/CD queda deshabilitado, conservándose únicamente por compatibilidad histórica del estándar.

**CSMA/CA** (Collision Avoidance), usado en redes inalámbricas (802.11) donde no es viable detectar colisiones de forma fiable (una estación no puede escuchar mientras transmite con la misma antena, y la atenuación hace que colisiones lejanas no se perciban localmente). Su principal reto es el **problema del nodo oculto**: dos estaciones fuera de alcance radioeléctrico mutuo, pero ambas dentro del alcance de un tercer nodo (p. ej. el punto de acceso), no se detectan entre sí y pueden transmitir simultáneamente provocando colisión en el receptor común.

```
Alcance de A:  [=====A=====B]
Alcance de C:        [=====B=====C]
      A ............. B ............. C
      (A y C no se oyen entre sí; ambos oyen a B)
```

Para mitigarlo se emplea el mecanismo **RTS/CTS** (Request To Send / Clear To Send): antes de transmitir datos, el emisor envía una trama corta RTS; el receptor responde con CTS, audible por todos los nodos en su radio (incluidos los ocultos al emisor), que reservan el medio (*Network Allocation Vector*) durante el tiempo indicado, evitando así que un nodo oculto interfiera. Además, CSMA/CA usa **espacios entre tramas (IFS)** de distinta duración para priorizar el acceso: **SIFS** (Short IFS, el más corto, usado para ACK, CTS y fragmentos de una misma transmisión) tiene prioridad máxima; **DIFS** (Distributed IFS, mayor que SIFS) es el tiempo que debe esperar libre el medio antes de iniciar una transmisión de datos ordinaria. Tras el DIFS, si el medio sigue libre, cada estación elige un valor aleatorio dentro de la **ventana de contención** (*contention window*) y cuenta atrás mientras el medio permanece libre, transmitiendo al llegar a cero (si otra estación transmite antes, se congela el contador).

**Paso de testigo (Token Passing)**, usado en Token Ring y FDDI: una trama especial (el *testigo* o *token*) circula por el anillo; solo la estación que posee el testigo tiene derecho a transmitir, tras lo cual libera un nuevo testigo. Es un método **determinista**: el tiempo máximo de espera de cualquier estación para transmitir es acotado y calculable, cualidad valorada en entornos industriales o de tiempo real, a diferencia del acceso probabilístico de CSMA/CD. Ante la pérdida del testigo (por fallo de una estación o error de transmisión), se emplea una estación monitora que detecta la ausencia mediante temporizadores y **regenera un nuevo testigo**, evitando el bloqueo permanente del anillo.

### 9. Dispositivos de interconexión

| Dispositivo | Capa OSI | Dominio de colisión | Dominio de difusión |
|---|---|---|---|
| Repetidor | 1 (Física) | No segmenta (uno único) | No segmenta |
| Hub | 1 (Física) | No segmenta (uno único) | No segmenta |
| Puente (bridge) | 2 (Enlace) | Segmenta (uno por puerto) | No segmenta |
| Switch | 2 (Enlace) | Segmenta (uno por puerto) | No segmenta (salvo VLANs) |
| Router | 3 (Red) | Segmenta | Segmenta |
| Gateway | 4–7 (Transporte a Aplicación) | Segmenta | Segmenta |
| Punto de acceso inalámbrico | 1–2 | Segmenta el medio radio del cableado | No segmenta (actúa como puente) |

El **repetidor** regenera la señal eléctrica para extender la distancia física sin interpretar direcciones. El **hub** es un repetidor multipuerto: retransmite por todos los puertos lo recibido por uno, manteniendo un único dominio de colisión para todo el segmento.

El **puente** aprende dinámicamente qué direcciones MAC se encuentran tras cada puerto observando las tramas entrantes (*algoritmo de aprendizaje*): al recibir una trama, registra en su **tabla de reenvío** (MAC origen → puerto de entrada); para decidir el reenvío, si la MAC destino ya está en la tabla la envía solo por ese puerto (segmentando el dominio de colisión), y si no la conoce la inunda (*flooding*) por todos los puertos salvo el de entrada. El **switch** es esencialmente un puente multipuerto con conmutación por hardware (ASIC), y admite tres modos de reenvío: **store-and-forward** (recibe la trama completa, verifica el FCS y solo entonces la reenvía; máxima fiabilidad, mayor latencia), **cut-through** (reenvía en cuanto lee la MAC destino en la cabecera, sin esperar el resto de la trama ni comprobar el CRC; mínima latencia, puede propagar tramas erróneas) y **fragment-free** (variante intermedia que espera a leer los primeros 64 bytes —donde se concentran la mayoría de colisiones— antes de reenviar, equilibrando latencia y fiabilidad).

El **router** opera en la capa de red, toma decisiones de encaminamiento basadas en direcciones IP y tablas de rutas, y **segmenta tanto dominios de colisión como de difusión**, siendo el elemento natural para interconectar redes IP distintas. El **gateway** traduce entre protocolos o pilas de comunicación heterogéneas en capas superiores (p. ej. pasarelas de correo entre distintos formatos, o pasarelas VoIP-RTC). El **punto de acceso (AP)** inalámbrico actúa como un puente entre el medio radio (compartido, half-duplex por naturaleza) y la red cableada.

### 10. Spanning Tree Protocol (STP, IEEE 802.1D)

En topologías con redundancia física a nivel de enlace (necesaria para tolerancia a fallos), los switches pueden generar **bucles de capa 2**: al no existir un campo TTL en las tramas Ethernet, una trama de difusión reenviada por *flooding* puede circular indefinidamente por el bucle, multiplicándose exponencialmente con cada retransmisión y provocando una **tormenta de broadcast** que satura la red y agota los recursos de los switches.

STP resuelve esto construyendo lógicamente un **árbol libre de bucles** sobre la topología física redundante: primero se elige un **puente raíz** (*root bridge*) comparando el **Bridge ID** de cada switch (prioridad configurable + dirección MAC como desempate; gana el valor numérico más bajo); después cada switch calcula el camino de menor coste hacia la raíz y determina qué puertos permanecen activos y cuáles se bloquean para eliminar bucles. Cada puerto atraviesa los estados: **blocking** (no reenvía tramas de datos, solo escucha BPDU), **listening** (participa en la elección de topología, sin aprender MACs ni reenviar), **learning** (aprende direcciones MAC pero aún no reenvía) y **forwarding** (reenvía tráfico normalmente); las transiciones entre estados están temporizadas (por defecto ~30-50 segundos en total), lo que constituye la principal crítica a 802.1D: convergencia lenta ante cambios de topología.

**RSTP** (Rapid STP, IEEE 802.1w) mejora la convergencia a orden de segundos (o milisegundos en el mejor caso) mediante mecanismos de propuesta/acuerdo (*proposal/agreement*) entre puertos vecinos, la introducción de roles de puerto adicionales (*alternate* y *backup*) que permiten una transición casi inmediata sin esperar los temporizadores clásicos, y la reducción efectiva de los estados de puerto a discarding/learning/forwarding.

### 11. Agregación de enlaces: LACP (IEEE 802.3ad)

**LACP** (Link Aggregation Control Protocol) permite agrupar varios enlaces físicos entre dos dispositivos en un único enlace lógico (*port-channel*/*EtherChannel*), negociando dinámicamente qué puertos participan en el grupo mediante el intercambio de PDUs LACP, y detectando automáticamente configuraciones erróneas o caídas de enlace para excluir puertos del grupo sin intervención manual. Aporta dos beneficios: **mayor ancho de banda agregado** (suma nominal de la capacidad de los enlaces miembro) y **tolerancia a fallos** (si un enlace cae, el tráfico se redistribuye automáticamente entre los restantes). El **balanceo de carga** entre los enlaces físicos se realiza mediante algoritmos hash sobre campos de la trama/paquete (MAC origen-destino, IP origen-destino, puertos L4), de modo que un mismo flujo se mantiene siempre en el mismo enlace físico (evitando reordenamiento de tramas), mientras que flujos distintos pueden repartirse entre los distintos enlaces del grupo.

### Trampas habituales de examen

1. Confundir **dominio de colisión** con **dominio de difusión**: el switch segmenta colisión por puerto pero **no** segmenta broadcast (salvo VLANs); solo el router segmenta ambos.
2. Asignar la codificación **Manchester** a Fast Ethernet o Gigabit: Manchester es exclusiva de Ethernet a 10 Mbps; 100BASE-TX usa 4B/5B+MLT-3 y 1000BASE-T usa PAM-5.
3. Pensar que CSMA/CD sigue activo en redes full-duplex modernas: en enlaces punto a punto conmutados full-duplex no hay colisiones posibles y el mecanismo se desactiva.
4. Confundir topología **física** con **lógica** en Ethernet 10BASE-T: cableado físico en estrella, comportamiento lógico de bus compartido (a través del hub).
5. Olvidar que el **EtherType** y la **longitud** comparten el mismo campo de 2 bytes en la trama Ethernet: valores ≤1500 se interpretan como longitud (IEEE 802.3 original) y valores ≥1536 como tipo de protocolo superior (Ethernet II/DIX), existiendo una zona no usada (1501-1535) precisamente para evitar ambigüedad.
