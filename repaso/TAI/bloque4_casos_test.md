# Bloque IV — Sistemas y comunicaciones (TAI, C1) — Supuesto práctico: casos resueltos y test

## 1. Casos prácticos resueltos

### Caso 1 (a). Direccionamiento IP con subnetting (VLSM) para una sede con varios departamentos

**Enunciado.** El organismo dispone de una nueva sede con los siguientes departamentos y necesidades de direccionamiento, a partir del bloque asignado **172.20.0.0/24**:

| Departamento | Hosts necesarios |
|---|---|
| Atención al ciudadano | 100 |
| Administración/Gestión | 60 |
| Informática (CPD) | 25 |
| Dirección/Secretaría | 12 |
| Enlace punto a punto con sede central (WAN) | 2 |

**Resolución (VLSM, de mayor a menor tamaño de subred).**

Se calcula el tamaño de bloque mínimo (potencia de 2) que cubre *hosts + 2* (red y broadcast) para cada departamento, y se asignan de forma contigua empezando por el requisito más grande:

| Subred | Hosts requeridos | Prefijo | Máscara | Dirección de red | Rango de hosts útiles | Broadcast | Hosts útiles |
|---|---|---|---|---|---|---|---|
| Atención al ciudadano | 100 | /25 | 255.255.255.128 | 172.20.0.0 | 172.20.0.1 – 172.20.0.126 | 172.20.0.127 | 126 |
| Administración | 60 | /26 | 255.255.255.192 | 172.20.0.128 | 172.20.0.129 – 172.20.0.190 | 172.20.0.191 | 62 |
| Informática/CPD | 25 | /27 | 255.255.255.224 | 172.20.0.192 | 172.20.0.193 – 172.20.0.222 | 172.20.0.223 | 30 |
| Dirección | 12 | /28 | 255.255.255.240 | 172.20.0.224 | 172.20.0.225 – 172.20.0.238 | 172.20.0.239 | 14 |
| Enlace WAN (p2p) | 2 | /30 | 255.255.255.252 | 172.20.0.240 | 172.20.0.241 – 172.20.0.242 | 172.20.0.243 | 2 |

Quedan libres las direcciones **172.20.0.244 – 172.20.0.255** (12 direcciones, subdivisibles en un /29 y un /30) reservadas para crecimiento futuro (p. ej., una VLAN de invitados o un nuevo enlace).

**Criterio de asignación de gateway:** primera IP útil de cada subred para el router/L3 switch (p. ej., 172.20.0.1, 172.20.0.129, 172.20.0.193…). Cada departamento se implementa como una VLAN independiente con su interfaz L3 (SVI) correspondiente, aplicando ACLs entre VLANs según necesidad (p. ej., Informática con acceso a todas, Atención al ciudadano solo a los servicios publicados).

---

### Caso 2 (b). Política de backup 3-2-1 con cálculo de RPO/RTO

**Enunciado.** El organismo tiene una base de datos de gestión de expedientes de **500 GB**, con una tasa de cambio diaria del **5%**. El área de negocio exige poder asumir como máximo **4 horas** de pérdida de datos (RPO) y una interrupción máxima de **2 horas** (RTO) ante un desastre.

**Resolución.**

**a) Diseño conforme a la regla 3-2-1:**
- **3 copias**: el dato original en producción (cabina/NAS) + 1 copia local en disco (appliance de backup) + 1 copia adicional.
- **2 soportes distintos**: disco local (rápido, para restauración operativa) y cinta o almacenamiento cloud (para retención a largo plazo).
- **1 copia fuera de la sede (offsite)**: réplica cifrada hacia un CPD secundario o proveedor cloud, para cubrir desastres que afecten a la sede completa (incendio, inundación).

**b) Planificación de copias en función del RPO (4 h):**
- Copia **completa**: semanal, domingo 02:00.
- Copia **diferencial**: diaria, 23:00 (acumula cambios desde la última completa).
- Copia de **log transaccional**: cada 4 horas (o inferior, p. ej. 15 min, si el motor de BD lo soporta), para no perder más de 4 h de transacciones → esto es lo que fija el RPO real.

**c) Cálculo de ventana de backup** (suponiendo un throughput de red/disco de backup de 200 MB/s):
- Completa: 500 GB ÷ 200 MB/s ≈ 2 500 s ≈ **42 minutos** → cabe en la ventana nocturna.
- Diferencial (peor caso, día 6, ~30% acumulado ≈ 150 GB): 150 000 MB ÷ 200 MB/s = 750 s ≈ **12,5 minutos**.
- Log cada 4 h: tamaño reducido (MB), impacto despreciable en la ventana.

**d) Retención:** diaria 30 días, semanal 3 meses, mensual 1 año (alineado con la categorización ENS del sistema — nivel medio/alto).

**e) Justificación del RTO (2 h):** la recuperación implica restaurar la última completa (42 min) + última diferencial (≤13 min) + logs desde entonces (minutos) + validación de integridad y arranque de servicios. El procedimiento debe **probarse trimestralmente** mediante simulacro de restauración documentado (runbook), ya que un RTO no verificado no es un RTO real. Si la prueba supera las 2 h, hay que rediseñar (p. ej., pasar a snapshot de cabina + replicación síncrona a un nodo caliente en lugar de restauración desde backup).

---

### Caso 3 (c). Cálculo de capacidad útil en RAID 5

**Enunciado.** Se dispone de **5 discos de 2 TB** para configurar un array RAID 5. Calcular la capacidad útil, la tolerancia a fallos y comparar con RAID 6 y RAID 10 usando los mismos discos.

**Resolución.**

**RAID 5** distribuye la paridad entre todos los discos; la capacidad útil equivale a *(n-1)* discos:

- Capacidad bruta: 5 × 2 TB = 10 TB
- Capacidad útil: (5-1) × 2 TB = **8 TB**
- Eficiencia: (n-1)/n = 4/5 = **80%**
- Tolerancia a fallos: **1 disco**
- Penalización de escritura (write penalty): 4 (leer dato antiguo, leer paridad antigua, escribir dato nuevo, escribir paridad nueva)

**Nota sobre unidades (trampa habitual de examen):** los fabricantes miden en TB decimales (10¹²), pero el sistema operativo muestra TiB binarios (2⁴⁰). 2 TB reales ≈ 1,818 TiB, por lo que la capacidad "8 TB" que ve el administrador en el SO será realmente ≈ **7,27 TiB**.

**Comparativa con los mismos 5 discos de 2 TB:**

| RAID | Fórmula capacidad útil | Capacidad útil | Eficiencia | Tolerancia a fallos |
|---|---|---|---|---|
| RAID 5 | (n-1) × disco | 8 TB | 80% | 1 disco |
| RAID 6 | (n-2) × disco | 6 TB | 60% | 2 discos (simultáneos) |
| RAID 10* | (n/2) × disco | 5 TB (requiere n par; con 5 discos no es aplicable directamente, se usaría con 4 ó 6) | 50% | 1 disco por par espejado (hasta 2-3 según cuáles fallen) |

*RAID 10 requiere número par de discos; con 5 discos no puede implementarse de forma pura (habría que usar 4 y dejar 1 de repuesto, o pasar a 6 discos).

**Conclusión para el caso:** si prima la capacidad, RAID 5 es la opción más eficiente; si el volumen es crítico y se quiere tolerar el fallo de 2 discos durante el rebuild (proceso especialmente sensible en discos grandes, donde el tiempo de reconstrucción aumenta el riesgo de una segunda fallo), se recomienda **RAID 6**.

---

### Caso 4 (d). Arquitectura de seguridad perimetral (firewall + DMZ + VPN) para teletrabajadores

**Enunciado.** El organismo necesita publicar un portal web para ciudadanos y permitir el acceso remoto seguro de 80 empleados en teletrabajo a las aplicaciones internas.

**Resolución.**

**Arquitectura lógica (defensa en profundidad):**

```
                    INTERNET
                       |
        [ Firewall perimetral / Router borde ]
           (filtrado anti-spoofing, IDS/IPS)
                       |
        ---------------+---------------
        |            DMZ              |
        |  Servidor Web (HTTPS/443)    |
        |  Relay de correo             |
        |  Concentrador VPN            |
        ---------------+---------------
                       |
           [ Firewall interno ]
        (solo tráfico estrictamente necesario)
                       |
              LAN corporativa
     (VLANs: Administración, Dirección, Informática...)
```

**Elementos de la solución:**

1. **Firewall perimetral** (stateful): filtra el tráfico de Internet, solo permite entrada a los puertos publicados en DMZ (443 al portal web, puerto VPN). Anti-spoofing e IDS/IPS en línea.
2. **DMZ**: aloja los servicios expuestos a Internet (portal web, relay de correo, concentrador VPN). Segmentada en VLANs propias por tipo de servicio.
3. **Firewall interno**: entre DMZ y LAN, con reglas de mínimo privilegio — ni el servidor web ni el concentrador VPN tienen acceso irrestricto a la LAN, solo a los puertos/servicios concretos que necesiten (p. ej., el servidor web solo accede al servidor de BBDD por el puerto de su motor, nunca al resto de la red).
4. **Acceso remoto (VPN):** se recomienda **SSL/TLS VPN** (o IPsec IKEv2) con:
   - Autenticación de **doble factor**: certificado digital de equipo corporativo + usuario/contraseña + OTP.
   - **NAC** (Network Access Control): antes de conceder el túnel, se verifica la postura del endpoint (antivirus actualizado, parches al día, disco cifrado).
   - El túnel da acceso **solo** a los recursos autorizados (segmentación por ACL/grupo de usuario), no a toda la LAN — principio de mínimo privilegio.
5. **Monitorización**: los logs del concentrador VPN y del firewall se envían a un SIEM para detectar patrones anómalos (conexiones fuera de horario, múltiples fallos de autenticación, geolocalización inusual).
6. **Por qué el servidor de BBDD nunca va en la DMZ**: si el servidor web (más expuesto) es comprometido, el atacante no debe poder saltar directamente a los datos; la BBDD queda protegida tras el firewall interno.

---

### Caso 5 (e). Resolución de un incidente de seguridad (ransomware) según ITIL

**Enunciado.** Un usuario del departamento de Administración reporta que no puede abrir sus documentos, que aparecen con extensión `.locked`. El equipo de seguridad debe actuar siguiendo el proceso de gestión de incidentes.

**Resolución (fases ITIL adaptadas a un incidente de seguridad):**

1. **Detección:** alerta del EDR/antivirus o aviso del usuario; se correlaciona con el SIEM (picos de cifrado de ficheros vía SMB, tráfico anómalo hacia una IP externa — posible C2). Se clasifica la prioridad (crítica, por posible propagación a recursos compartidos).

2. **Contención (inmediata):**
   - Aislar el equipo afectado de la red (deshabilitar el puerto del switch o mover a VLAN de cuarentena) **sin apagarlo** (se perdería la memoria RAM, útil para el análisis forense).
   - Deshabilitar/bloquear la cuenta de usuario comprometida.
   - Bloquear en el firewall los IoC conocidos (IP/dominio de C2).
   - Revisar y, si procede, bloquear temporalmente los recursos compartidos SMB afectados para frenar la propagación lateral.
   - Realizar una copia forense (imagen de disco/memoria) antes de cualquier limpieza, para preservar evidencias.

3. **Erradicación:**
   - Identificar el vector de entrada (típicamente phishing con adjunto/macro).
   - Eliminar el malware del equipo (reinstalación limpia recomendada frente a "limpieza" con antivirus, dado el riesgo de restos).
   - Aplicar los parches pendientes y actualizar firmas.
   - Forzar cambio de credenciales de las cuentas potencialmente expuestas.
   - Buscar los mismos IoC en el resto del parque (barrido con el EDR) para descartar propagación silenciosa.

4. **Recuperación:**
   - Restaurar los ficheros cifrados desde el **último backup limpio anterior a la infección** (verificando primero que ese backup no esté también afectado).
   - Reincorporar el equipo a la red de forma progresiva, con monitorización reforzada durante unos días.
   - Confirmar con el usuario la integridad y disponibilidad de los datos restaurados (RPO real del incidente).

5. **Cierre y lecciones aprendidas (Post-Incident Review):**
   - Informe de incidente: cronología, causa raíz, impacto, coste.
   - Notificación obligatoria si aplica el Esquema Nacional de Seguridad (comunicación a **CCN-CERT/INCIBE-CERT** según la categoría del sistema y el tipo de incidente).
   - Actualización de políticas: formación anti-phishing, revisión de la segmentación SMB, ajuste de reglas de detección.

---

### Caso 6 (f). Elección justificada de nivel TIER de CPD

**Enunciado.** El organismo necesita modernizar su CPD. El requisito de negocio es: disponibilidad objetivo ≥ 99,98% anual, capacidad de realizar mantenimiento de UPS y climatización **sin interrumpir el servicio**, con un presupuesto que no permite duplicar toda la infraestructura activa-activa (2N).

**Resolución.**

Referencia (estándar Uptime Institute):

| Nivel | Disponibilidad | Downtime/año aprox. | Redundancia | Mantenimiento sin corte |
|---|---|---|---|---|
| TIER I | 99,671% | ~28,8 h | Ninguna, camino único | No |
| TIER II | 99,741% | ~22,0 h | Componentes N+1 | No (un único camino de distribución) |
| TIER III | 99,982% | ~1,6 h | N+1, múltiples caminos de distribución (uno activo) | Sí (concurrently maintainable) |
| TIER IV | 99,995% | ~0,4 h (~26 min) | 2N / 2N+1, todos los caminos activos | Sí, y tolerante a fallo (fault tolerant) |

**Decisión:** **TIER III.**

- Cumple el requisito de disponibilidad (99,982% ≥ 99,98% exigido).
- Aporta redundancia N+1 y **mantenimiento concurrente** (se puede sacar de servicio un componente —p. ej. una UPS— para mantenimiento sin afectar a la carga), que es el requisito explícito del enunciado.
- **No** se justifica TIER IV: exigiría doble infraestructura activa simultánea (2N, fault tolerant ante fallo no planificado, no solo ante mantenimiento planificado), con un coste de inversión y operación muy superior que el presupuesto del organismo no contempla, y el requisito de negocio no pide tolerancia a fallo no planificado, sino disponibilidad y mantenimiento sin corte.

---

### Caso 7 (g). Troubleshooting de conectividad por capas OSI

**Enunciado.** Un usuario del departamento de Administración no puede acceder a `https://expedientes.organismo.local` (intranet), mientras que otros usuarios de otros departamentos sí pueden.

**Resolución (comprobación sistemática de abajo arriba, capa a capa):**

| Capa OSI | Qué comprobar | Comandos/acciones típicas |
|---|---|---|
| **1 — Física** | Cable conectado, LED del puerto del switch encendido, patch panel correcto, sin daño en el cable | Inspección visual, comprobar luces del switch, sustituir cable/patch |
| **2 — Enlace** | Puerto del switch activo (no en shutdown/err-disabled), VLAN correcta asignada al puerto, ausencia de bucles (STP no bloqueando el puerto), tabla ARP correcta | `show interface status`, `show mac address-table`, `arp -a` |
| **3 — Red** | IP, máscara y gateway correctos en el equipo; ping al gateway; tabla de rutas; posible bloqueo por ACL en el router/firewall (p. ej., si el equipo cayó en una VLAN/subred con ACL más restrictiva) | `ipconfig`/`ifconfig`, `ping <gateway>`, `tracert`/`traceroute` |
| **4 — Transporte** | El puerto TCP del servicio (443) está abierto y accesible desde el cliente; no bloqueado por firewall intermedio | `Test-NetConnection -Port 443`, `telnet <host> 443`, `nc -zv <host> 443` |
| **5-6 — Sesión/Presentación** | Negociación TLS correcta, certificado válido y de confianza para el cliente, fecha/hora del equipo correcta (afecta a validación de certificado) | `curl -v https://expedientes...`, revisar almacén de certificados, hora del sistema |
| **7 — Aplicación** | Resolución DNS del nombre `expedientes.organismo.local`, servicio de aplicación arriba, logs de la aplicación/IIS/Apache, credenciales de la aplicación | `nslookup`/`Resolve-DnsName`, revisar logs del servicio, probar con la IP directa |

**Diagnóstico dirigido para este caso concreto:** dado que solo falla un departamento, el foco debe ir primero a la **capa 2-3** (VLAN incorrecta en el puerto del switch de Administración tras un cambio reciente, o una ACL que en esa subred bloquea el destino) antes que a capa 7 (poco probable si el resto de departamentos accede sin problema al mismo servicio). Se confirma con: `ping` al gateway (capa 3, ¿responde?), `arp -a` (capa 2, ¿resuelve el MAC del gateway?), y comparación de la VLAN asignada al puerto de ese usuario frente a la de un puerto que sí funciona.

---

## 2. Test de autoevaluación (25 preguntas)

**1.** Sobre la gestión de procesos en un sistema tipo UNIX/Linux, ¿qué ocurre al ejecutar `kill -9 <pid>`?

A) Envía SIGTERM, permitiendo que el proceso libere recursos antes de terminar.
B) Envía SIGKILL, señal que el proceso no puede capturar ni ignorar, terminándolo de forma inmediata.
C) Envía SIGSTOP, suspendiendo el proceso hasta recibir SIGCONT.
D) Envía SIGHUP, provocando que el proceso recargue su configuración.

**2.** Al acceder a una carpeta compartida en red sobre un volumen NTFS, con permisos NTFS y permisos de recurso compartido configurados de forma distinta, ¿qué permiso efectivo se aplica?

A) Prevalecen siempre los permisos NTFS.
B) Prevalecen siempre los permisos de recurso compartido.
C) Se aplica el más restrictivo de ambos conjuntos.
D) Se suman ambos, aplicando el menos restrictivo.

**3.** Un servidor tiene 8 discos de 2 TB en RAID 5. ¿Cuál es su capacidad útil aproximada?

A) 16 TB
B) 14 TB
C) 12 TB
D) 8 TB

**4.** ¿Qué caracteriza a la replicación síncrona de bases de datos frente a la asíncrona?

A) La transacción se confirma en origen sin esperar al destino, minimizando latencia pero arriesgando pérdida de datos.
B) La transacción no se confirma en origen hasta que el destino confirma haberla aplicado, garantizando cero pérdida de datos a costa de mayor latencia.
C) Solo puede usarse entre nodos del mismo CPD.
D) Es funcionalmente idéntica a un backup diferencial por hora.

**5.** ¿Qué diferencia principal hay entre un hipervisor tipo 1 y uno tipo 2?

A) El tipo 1 corre directamente sobre el hardware sin SO anfitrión; el tipo 2 se ejecuta como aplicación sobre un SO anfitrión.
B) El tipo 1 solo admite una máquina virtual.
C) El tipo 2 ofrece mejor rendimiento por acceso directo al hardware.
D) No hay diferencia funcional, solo de licencia.

**6.** ¿Qué función cumple el registro SPF en el DNS de un dominio de correo?

A) Cifra el contenido del mensaje de extremo a extremo.
B) Publica qué servidores están autorizados a enviar correo en nombre del dominio, ayudando a detectar suplantación.
C) Firma digitalmente las cabeceras con clave privada.
D) Limita el tamaño máximo de buzón por usuario.

**7.** ¿Qué diferencia fundamental hay entre un contenedor (p. ej. Docker) y una máquina virtual tradicional?

A) El contenedor virtualiza hardware completo con kernel propio.
B) El contenedor comparte el kernel del SO anfitrión, aislando procesos mediante namespaces y cgroups, resultando más ligero que una VM.
C) Ambos requieren obligatoriamente un hipervisor tipo 1.
D) Un contenedor no puede desplegarse en la nube.

**8.** En Active Directory, ¿qué protocolo se usa principalmente para autenticar usuarios del dominio en versiones modernas de Windows?

A) NTLM exclusivamente.
B) Kerberos, mediante tickets emitidos por el KDC.
C) RADIUS integrado de forma nativa en el controlador de dominio.
D) TACACS+.

**9.** ¿Cuál es la finalidad de una política de bloqueo de cuenta (account lockout policy) en una GPO?

A) Cifrar las contraseñas almacenadas en el controlador de dominio.
B) Bloquear temporalmente una cuenta tras varios intentos fallidos de inicio de sesión, mitigando ataques de fuerza bruta.
C) Forzar el cambio de contraseña cada 24 horas.
D) Impedir el acceso a recursos fuera del horario laboral.

**10.** En firma digital con criptografía asimétrica, ¿con qué clave firma el emisor y con cuál se verifica?

A) Firma con su clave pública; se verifica con su clave privada.
B) Firma con su clave privada; se verifica con su clave pública.
C) Firma y verifica con la misma clave simétrica compartida.
D) Firma con la clave pública del receptor.

**11.** ¿Qué propiedad garantiza principalmente el uso de una función hash (p. ej. SHA-256) en el proceso de firma electrónica?

A) La confidencialidad, pues el documento queda cifrado.
B) La integridad: cualquier alteración posterior produce un resumen distinto, detectable al verificar.
C) El no repudio, sin relación con la integridad.
D) La disponibilidad del servicio de firma.

**12.** Según la clasificación Uptime Institute, ¿qué nivel TIER exige N+1 y mantenimiento sin interrupción, pero no tolerancia completa a fallo no planificado (2N)?

A) TIER I
B) TIER II
C) TIER III
D) TIER IV

**13.** ¿Qué medio de transmisión guiado es inmune a interferencias electromagnéticas y permite mayores distancias sin repetidores?

A) Par trenzado UTP categoría 6.
B) Cable coaxial RG-58.
C) Fibra óptica monomodo.
D) Par trenzado STP categoría 5e.

**14.** ¿Qué caracteriza a la transmisión en banda ancha frente a la banda base?

A) Usa toda la capacidad del medio para una única señal digital sin modular.
B) Permite multiplexar varias señales moduladas en distintas frecuencias sobre el mismo medio físico simultáneamente.
C) Solo se aplica a redes inalámbricas.
D) No requiere módem ni modulación.

**15.** Un centro dispone de 192.168.10.0/24 y necesita crear 6 subredes con al menos 25 hosts útiles cada una. ¿Qué máscara mínima debe emplear?

A) /26 (255.255.255.192)
B) /27 (255.255.255.224)
C) /28 (255.255.255.240)
D) /25 (255.255.255.128)

**16.** ¿En qué capa OSI opera un conmutador (switch) que reenvía tramas según direcciones MAC?

A) Capa 1 — Física
B) Capa 2 — Enlace de datos
C) Capa 3 — Red
D) Capa 4 — Transporte

**17.** ¿Qué mecanismos emplea TCP para garantizar entrega ordenada y fiable?

A) Best-effort sin confirmación, igual que UDP.
B) Números de secuencia, ACK, ventana deslizante y retransmisión ante pérdida.
C) Broadcast de cada segmento hasta confirmación.
D) Cifrado TLS obligatorio integrado en la cabecera TCP.

**18.** En HTTP, ¿qué código indica que el recurso se ha movido de forma permanente?

A) 302 Found
B) 404 Not Found
C) 301 Moved Permanently
D) 500 Internal Server Error

**19.** Durante el handshake TLS, ¿qué finalidad tiene el certificado digital del servidor?

A) Cifrar simétricamente todo el tráfico posterior sin negociación previa de claves.
B) Permitir al cliente verificar la identidad del servidor mediante la cadena de confianza y obtener su clave pública para el intercambio de claves.
C) Autenticar obligatoriamente al cliente ante el servidor en todos los casos.
D) Sustituir la resolución DNS del dominio.

**20.** ¿Qué diferencia principal aporta HTTP/2 respecto a HTTP/1.1 en el uso de la conexión TCP?

A) Multiplexa varias peticiones/respuestas sobre una misma conexión TCP, evitando el bloqueo de cabecera de línea.
B) Elimina TCP y usa solo UDP.
C) HTTP/1.1 ya multiplexaba de forma nativa igual que HTTP/2.
D) HTTP/2 no admite cifrado TLS.

**21.** En una VPN IPsec, ¿qué diferencia hay entre modo túnel y modo transporte?

A) El transporte cifra el paquete IP completo encapsulándolo en uno nuevo; el túnel solo la carga útil.
B) El túnel cifra el paquete IP completo (cabecera incluida) encapsulándolo en uno nuevo, habitual entre pasarelas o acceso remoto; el transporte solo protege la carga útil manteniendo la cabecera original, típico extremo a extremo.
C) Ambos modos son idénticos, solo cambia el algoritmo de cifrado.
D) El transporte requiere obligatoriamente un concentrador VPN dedicado.

**22.** ¿Qué diferencia hay entre un IDS y un IPS?

A) El IDS bloquea activamente el tráfico en línea; el IPS solo genera alertas.
B) El IDS monitoriza y alerta sin bloquear (normalmente fuera de banda); el IPS se sitúa en línea y puede bloquear el tráfico automáticamente.
C) Son sinónimos con la misma función.
D) El IDS solo opera a nivel de aplicación.

**23.** ¿Por qué no se debe ubicar el servidor de bases de datos corporativo en la misma DMZ que el servidor web público?

A) Porque la DMZ no admite servidores con más de un interfaz de red.
B) Porque si el servidor web (más expuesto) es comprometido, un atacante tendría acceso directo a la BBDD sin cruzar el firewall interno.
C) Porque los servidores de BBDD no soportan direccionamiento privado.
D) Porque la DMZ solo permite tráfico UDP.

**24.** ¿Qué topología física implica que todos los equipos se conectan a un dispositivo central, de forma que el fallo de un enlace individual no afecta al resto?

A) Bus
B) Anillo
C) Estrella
D) Malla completa

**25.** ¿Cuál es la finalidad principal de Spanning Tree (STP, IEEE 802.1D) en una LAN conmutada con enlaces redundantes?

A) Sumar el ancho de banda de todos los enlaces redundantes simultáneamente.
B) Evitar bucles de capa 2 bloqueando lógicamente los puertos redundantes, activando un puerto alternativo si el enlace principal falla.
C) Cifrar el tráfico entre switches.
D) Asignar direcciones IP automáticamente a los switches.

---

### Soluciones

1. **B** — SIGKILL (señal 9) no puede capturarse ni ignorarse; el proceso termina de inmediato sin posibilidad de liberar recursos limpiamente (a diferencia de SIGTERM, señal 15).
2. **C** — Cuando coexisten permisos NTFS y de recurso compartido, el resultado efectivo es siempre el más restrictivo de los dos.
3. **B** — (8-1) × 2 TB = 14 TB.
4. **B** — La replicación síncrona espera confirmación del destino antes de dar por válida la transacción en origen: cero pérdida de datos, mayor latencia.
5. **A** — Tipo 1 (bare-metal): ESXi, Hyper-V, KVM. Tipo 2 (hosted): VirtualBox, VMware Workstation, sobre un SO anfitrión.
6. **B** — SPF (Sender Policy Framework) publica los servidores autorizados a enviar en nombre del dominio; es un control anti-spoofing, no de cifrado ni de firma.
7. **B** — Los contenedores comparten el kernel del host y se aíslan con namespaces/cgroups; no llevan SO completo propio, de ahí su ligereza frente a una VM.
8. **B** — Kerberos es el protocolo de autenticación por defecto en dominios AD modernos, basado en tickets emitidos por el KDC (el DC hace de KDC).
9. **B** — El bloqueo de cuenta tras N intentos fallidos es la contramedida estándar frente a ataques de fuerza bruta/diccionario.
10. **B** — Se firma con la clave privada del emisor (solo él la posee) y se verifica con su clave pública (de conocimiento público), lo que aporta autenticidad y no repudio.
11. **B** — El hash garantiza integridad: cualquier cambio en el documento altera el resumen y la verificación de la firma falla.
12. **C** — TIER III: N+1, concurrently maintainable (mantenimiento sin corte), pero un único camino activo de distribución (no 2N como TIER IV).
13. **C** — La fibra óptica monomodo no se ve afectada por EMI (no es conductora, transmite luz) y alcanza mucha mayor distancia sin repetidores que el cobre.
14. **B** — La banda ancha (broadband) multiplexa varias señales moduladas en distintas frecuencias sobre el mismo medio (FDM); la banda base usa toda la capacidad para una única señal sin modular.
15. **B** — /27 da bloques de 32 direcciones (30 hosts útiles, cubre los 25 requeridos) y permite 8 subredes dentro del /24, suficientes para las 6 requeridas; /26 solo permite 4 subredes, insuficiente.
16. **B** — El switch tradicional (sin funciones L3) reenvía por dirección MAC, propio de la capa 2 (Enlace de datos).
17. **B** — TCP es orientado a conexión: numeración de secuencia, ACK, ventana deslizante para control de flujo y retransmisión ante pérdida de segmentos.
18. **C** — 301 Moved Permanently indica redirección permanente (302 es temporal).
19. **B** — El certificado permite validar la identidad del servidor contra una cadena de confianza (CA) y aporta la clave pública usada en el intercambio de claves del handshake.
20. **A** — HTTP/2 introduce multiplexación de streams sobre una única conexión TCP, resolviendo el head-of-line blocking a nivel de aplicación que sufría HTTP/1.1 con conexiones no persistentes/pipelining limitado.
21. **B** — Modo túnel: cifra el paquete IP completo y lo reencapsula (uso típico en VPN sitio-a-sitio o acceso remoto). Modo transporte: solo cifra la carga útil, mantiene la cabecera IP original (comunicación extremo a extremo entre dos hosts).
22. **B** — IDS = detección/alerta (pasivo); IPS = detección + bloqueo activo en línea.
23. **B** — La DMZ asume mayor exposición al ser accesible desde Internet; si contuviera la BBDD y el servidor web fuera comprometido, el atacante saltaría directamente a los datos sin atravesar el firewall interno que protege la LAN.
24. **C** — En topología en estrella, cada nodo tiene un enlace dedicado al dispositivo central; el fallo de un enlace solo aísla a ese nodo, no al resto.
25. **B** — STP calcula un árbol libre de bucles bloqueando lógicamente los puertos redundantes y activa un puerto alternativo (reconvergencia) si el enlace en uso falla.
