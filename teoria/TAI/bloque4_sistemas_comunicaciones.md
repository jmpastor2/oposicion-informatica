# TAI — Bloque IV: Sistemas y comunicaciones

> Bloque de alto peso en el examen: entra en el test general Y es uno de los dos supuestos prácticos posibles (junto al Bloque III).

## Tema 1. Administración del Sistema operativo y software de base. Actualización, mantenimiento y reparación del sistema operativo.

La administración del sistema operativo (SO) comprende la gestión del núcleo, los servicios, los controladores y el software de base que sustenta las aplicaciones. En entornos GNU/Linux, la administración se apoya en gestores de paquetes que resuelven dependencias y mantienen un registro del software instalado. Los principales son APT (Debian/Ubuntu, con `apt-get`, `apt`, ficheros `.deb` y repositorios definidos en `/etc/apt/sources.list`), YUM y su sucesor DNF (Red Hat/CentOS/Fedora, paquetes `.rpm`, con resolución de dependencias mediante metadatos `repodata`), y Zypper (openSUSE). Todos ellos permiten actualizaciones de seguridad (`apt upgrade`, `dnf update`), instalación transaccional y rollback en sistemas con Btrfs o LVM mediante snapshots. En Windows Server, la gestión equivalente se realiza con Windows Update, WSUS (Windows Server Update Services) para centralizar la distribución de parches en la red corporativa, y PowerShell DSC (Desired State Configuration) para garantizar la configuración declarativa de los servidores.

El mantenimiento del SO implica varias tareas periódicas: gestión de logs (rotación con `logrotate`, revisión de `/var/log/syslog`, `journalctl` en sistemas con systemd), gestión de procesos y recursos (monitorización de carga con `top`, `htop`, `vmstat`, `iostat`), gestión de servicios (systemd como gestor de arranque en Linux moderno, sustituyendo a SysVinit y Upstart; unidades `.service`, `.timer`, `.mount`), y gestión del sistema de ficheros (comprobación de integridad con `fsck`, gestión de particiones con `fdisk`/`parted`, cuotas de disco con `quota`). La actualización del SO debe seguir un ciclo de gestión de parches (patch management) que incluya: inventario de activos, clasificación de vulnerabilidades (CVE, puntuación CVSS), pruebas en entorno de preproducción, ventana de mantenimiento planificada y plan de rollback ante fallos.

La reparación del sistema operativo ante fallos de arranque requiere conocer el proceso de arranque: en BIOS/MBR, el bootloader (GRUB2) carga el kernel desde `/boot`; en UEFI, se emplea la partición EFI (ESP, FAT32) con `grub-efi` o el gestor propio de Windows (Boot Manager, BCD). Ante corrupción del sistema, se recurre a modo de recuperación (`init=/bin/bash`, single user mode), live CD/USB de rescate, `chroot` para reparar el sistema desde un entorno externo, y reconstrucción de `initramfs`. En Windows, las herramientas de reparación incluyen el Entorno de recuperación (WinRE), `sfc /scannow` (System File Checker), `DISM` (Deployment Image Servicing and Management) para reparar la imagen del componente store, y `bootrec` para reconstruir el registro de arranque maestro.

El software de base incluye también los controladores de dispositivo (drivers), firmware (actualizable vía UEFI/BIOS o herramientas del fabricante como iDRAC/iLO en servidores), y el middleware que conecta el SO con las aplicaciones (bibliotecas de tiempo de ejecución como .NET Runtime, JVM). La gestión de la configuración a escala se realiza mediante herramientas de automatización como Ansible (agentless, YAML playbooks, idempotencia), Puppet o Chef (modelo agente-servidor, DSL declarativo), que garantizan que múltiples servidores mantengan un estado consistente y auditable.

Un aspecto crítico es la gestión del ciclo de vida del software: los fabricantes definen fechas de fin de soporte (EOL) y fin de vida útil de seguridad (EOSL), tras las cuales dejan de publicarse parches; mantener sistemas fuera de soporte constituye un riesgo grave de seguridad y suele estar prohibido por normativa como el Esquema Nacional de Seguridad (ENS). La virtualización de la gestión (imágenes doradas o "golden images", plantillas preconfiguradas y despliegue mediante herramientas como Packer) permite estandarizar y acelerar el despliegue de sistemas actualizados.

Finalmente, la monitorización proactiva del estado del SO (uso de CPU, memoria, disco, número de procesos zombis, actualizaciones pendientes) mediante agentes como Nagios, Zabbix o Prometheus con Node Exporter permite anticipar fallos antes de que afecten al servicio, cerrando el ciclo de administración: instalar, configurar, monitorizar, parchear y, cuando es necesario, reparar.

## Tema 2. Administración de bases de datos. Sistemas de almacenamiento y su virtualización. Políticas, sistemas y procedimientos de backup y su recuperación. Backup de sistemas físicos y virtuales. Virtualización de sistemas y virtualización de puestos de usuario.

La administración de bases de datos (DBA) abarca la instalación, configuración, ajuste de rendimiento (tuning), seguridad y disponibilidad de sistemas gestores como SQL Server, Oracle, MySQL/MariaDB y PostgreSQL. Las tareas habituales incluyen la gestión de índices, la planificación de consultas (query execution plans), el control de bloqueos y transacciones (ACID), la gestión de tablespaces/filegroups, y la replicación (maestro-esclavo, maestro-maestro, Always On Availability Groups en SQL Server, streaming replication en PostgreSQL). El aislamiento transaccional se regula mediante niveles como Read Committed, Repeatable Read o Serializable, equilibrando consistencia y concurrencia.

Los sistemas de almacenamiento se clasifican en DAS (Direct Attached Storage), NAS (Network Attached Storage, almacenamiento de archivos por red mediante NFS o SMB/CIFS) y SAN (Storage Area Network, red dedicada de bloques mediante Fibre Channel o iSCSI, que presenta LUNs a los servidores como discos locales). El nivel de redundancia física se implementa mediante RAID: RAID 0 (striping, sin redundancia), RAID 1 (mirroring), RAID 5 (striping con paridad distribuida, tolera un fallo), RAID 6 (doble paridad, tolera dos fallos) y RAID 10 (mirroring + striping). La virtualización del almacenamiento añade una capa de abstracción (storage pools, thin provisioning) mediante VMware vSAN, Storage Spaces Direct (Windows) o LVM en Linux.

Las políticas de backup se rigen por dos métricas clave: **RPO** (Recovery Point Objective, cantidad máxima de datos que se puede perder) y **RTO** (Recovery Time Objective, tiempo máximo admisible para restaurar el servicio). Tipos de copia: **completa** (íntegra), **incremental** (cambios desde la última copia de cualquier tipo, minimiza tiempo/espacio pero complica la restauración) y **diferencial** (cambios desde la última copia completa, restauración más simple a costa de mayor tamaño progresivo). La **regla 3-2-1** es el estándar de referencia: 3 copias, en 2 soportes distintos, 1 copia offsite, con la variante 3-2-1-1-0 que añade una copia inmutable/air-gapped frente al ransomware.

El backup de sistemas físicos se apoya en agentes que copian a nivel de bloque o fichero (Veeam, Bacula, `mysqldump`/`pg_dump`), mientras que el backup de sistemas virtuales aprovecha snapshots del hipervisor y APIs específicas como VMware VADP, con Changed Block Tracking (CBT) para copiar solo bloques modificados. La recuperación debe probarse periódicamente (restore testing), documentada en un Plan de Recuperación ante Desastres (DRP) integrado en el Plan de Continuidad de Negocio (BCP).

La virtualización de sistemas se sustenta en hipervisores de **Tipo 1** (bare-metal: VMware ESXi, Hyper-V, KVM, Xen), usados en producción, y **Tipo 2** (hosted: VirtualBox, VMware Workstation), orientados a desarrollo. Cada VM encapsula un SO completo con recursos virtuales (vCPU, vRAM, vNIC, vDisk), con sobreaprovisionamiento (overcommit) y migración en caliente (vMotion/Live Migration).

La **virtualización de puestos de usuario (VDI)** centraliza los escritorios en el centro de datos, entregados mediante RDP, PCoIP/Blast Extreme (VMware Horizon), Citrix HDX o Azure Virtual Desktop. Facilita la gestión centralizada y la seguridad (los datos no residen en el endpoint), pero exige dimensionamiento cuidadoso frente al "boot storm".

## Tema 3. Administración de servidores de correo electrónico y sus protocolos. Administración de contenedores y microservicios.

El correo electrónico se sustenta en varios protocolos complementarios. **SMTP** (puerto 25 relay, 587 con STARTTLS, 465 SMTPS) gestiona envío y transporte entre MTA (Postfix, Exim, Exchange Transport). La recepción se realiza mediante **POP3** (110/995, descarga y suele eliminar mensajes, un solo cliente) o **IMAP** (143/993, mantiene mensajes sincronizados en servidor, acceso concurrente multi-dispositivo).

Autenticación de dominio contra suplantación: **SPF** (registro DNS TXT, servidores autorizados a enviar), **DKIM** (firma criptográfica de cabeceras, clave publicada en DNS) y **DMARC** (combina SPF+DKIM, política none/quarantine/reject). Administración: colas de correo, listas negras/blancas (RBL, DNSBL), antispam (SpamAssassin), antivirus (ClamAV), cuotas de buzón y retención conforme al RGPD.

**Contenedores**: virtualizan a nivel de SO, comparten el kernel del host mediante namespaces (aislamiento) y cgroups (control de recursos), mucho más ligeros que las VM. Docker: imagen inmutable (`Dockerfile`), registros (Docker Hub, Harbor), Docker Engine.

**Microservicios**: aplicaciones descompuestas en servicios pequeños e independientes, comunicados vía REST/gRPC o mensajería asíncrona (Kafka, RabbitMQ). **Kubernetes**: Pods (unidad mínima), Deployments (réplicas, rolling updates), Services (IP virtual estable), Ingress (enrutamiento HTTP), ConfigMaps/Secrets, PersistentVolumes, autoescalado (HPA), autorreparación.

Diferencia VM vs contenedores: VM = aislamiento fuerte, más recursos, arranque en minutos; contenedores = más eficientes/portables, comparten kernel, exigen escaneo de vulnerabilidades (Trivy, Clair) y ejecución sin privilegios. Integración con CI/CD (Jenkins, GitLab CI) automatiza build, test y despliegue.

## Tema 4. Administración de redes de área local. Gestión de usuarios. Gestión de dispositivos. Monitorización y control de tráfico.

Una LAN se estructura jerárquicamente: núcleo (core), distribución (VLAN, políticas de enrutamiento) y acceso. **VLAN** (802.1Q) segmenta dominios de difusión; el etiquetado marca las tramas en enlaces troncales. Direccionamiento: **DHCP** (IP, máscara, gateway, DNS con leases) y **DNS** (zonas primarias/secundarias, registros A, AAAA, CNAME, MX, PTR).

**Gestión de usuarios**: Active Directory (LDAP + Kerberos), unidades organizativas (OU), GPO (políticas centralizadas). En Linux: OpenLDAP, FreeIPA, SSSD/Winbind. Modelo **RBAC** (permisos por rol, mínimo privilegio).

**Gestión de dispositivos**: switches gestionables, routers, APs (WPA3/802.1X). MDM/UEM (Microsoft Intune) para políticas de seguridad, cifrado, borrado remoto en dispositivos móviles (BYOD). CMDB para inventario de activos TI.

**Monitorización**: **SNMP** (GET/SET sobre MIB, traps asíncronos; SNMPv3 añade cifrado). Herramientas: Zabbix, PRTG, Nagios, LibreNMS. **NetFlow/sFlow** analizan tráfico a nivel de flujo.

**Control de tráfico**: **QoS** (colas de prioridad, marcado DSCP, traffic shaping/policing). NGFW e IDS/IPS con Deep Packet Inspection. Wireshark/tcpdump para análisis de capturas y forense de incidentes.

## Tema 5. Conceptos de seguridad de los sistemas de información. Seguridad física. Seguridad lógica. Amenazas y vulnerabilidades. Técnicas criptográficas y protocolos seguros. Mecanismos de firma digital. Infraestructura física de un CPD: acondicionamiento y equipamiento. Sistemas de gestión de incidencias. Control remoto de puestos de usuario.

Tríada **CIA**: Confidencialidad, Integridad, Disponibilidad, más Autenticidad y Trazabilidad (recogidas en el ENS, RD 311/2022).

**Seguridad física**: control de acceso (tarjetas, biometría, mantrap), CCTV, extinción de incendios con gas inerte (FM-200, Novec 1230, no daña equipos). **Seguridad lógica**: autenticación (MFA), ACL, cifrado en reposo/tránsito, segmentación de redes.

**Amenazas y vulnerabilidades**: clasificación por origen (naturales, humanas intencionadas/no intencionadas). Riesgo = f(probabilidad, impacto). Gestión de vulnerabilidades: escaneo (Nessus, OpenVAS), CVSS, parcheo priorizado. Malware relevante: ransomware, troyanos, phishing/spear-phishing.

**Criptografía simétrica**: clave única compartida (AES 128/192/256), rápida, problema de distribución. **Asimétrica**: par de claves pública/privada (RSA, ECC), resuelve la distribución a costa de rendimiento; en la práctica se combina (cifrado híbrido). **Hash** (SHA-256, SHA-3): huella irreversible, verifica integridad. Protocolos: **TLS** (handshake, autentica servidor con certificado), **SSH**, **IPsec** (base de VPN).

**Firma digital**: hash cifrado con clave privada del emisor; el receptor descifra con la clave pública y compara. Sustentada en **PKI**: Autoridad de Certificación (CA) emite certificados X.509, cadenas de confianza, CRL/OCSP. En España: FNMT, DNI electrónico.

**Infraestructura física de un CPD**: clasificación **TIER** del Uptime Institute (I sin redundancia, ~99,671%; II redundancia parcial; III mantenimiento concurrente, N+1; IV tolerancia a fallos, doble ruta activa-activa, ~99,995%). Climatización de precisión (CRAC/CRAH), pasillos fríos/calientes, PUE (eficiencia energética), SAI/UPS, generadores diésel, extinción específica para equipamiento eléctrico.

**Gestión de incidencias** (ITIL): incidente (interrupción, restaurar servicio) vs problema (causa raíz, evitar recurrencia). Ciclo de ticket: registro, clasificación, priorización (impacto/urgencia), asignación, resolución, cierre. Herramientas ITSM: ServiceNow, Jira Service Management, GLPI. SLA.

**Control remoto de puestos de usuario**: RDP (cifrado TLS), VNC (protocolo RFB), TeamViewer/AnyDesk. Debe quedar auditado, con consentimiento del usuario y bajo cifrado/autenticación robusta.

## Tema 6. Comunicaciones. Medios de transmisión. Modos de comunicación. Equipos terminales y equipos de interconexión y conmutación. Redes de comunicaciones. Redes de conmutación y redes de difusión. Comunicaciones móviles e inalámbricas.

### Medios de transmisión

**Cable de pares trenzados**: Cat5e (1 Gbps/100m), Cat6 (1-10 Gbps), Cat6a (10 Gbps/100m), Cat8 (25/40 Gbps/30m, centros de datos). UTP sin apantallar, STP apantalla cada par, FTP apantalla el conjunto. **Fibra óptica**: monomodo (SMF, alcances de decenas de km, backbone) y multimodo (MMF, OM3/OM4/OM5, centros de datos), inmune a interferencias. **Medios no guiados**: radiofrecuencia, infrarrojos, láser.

### Modos de comunicación

**Símplex** (unidireccional), **semidúplex/half-duplex** (bidireccional alternado), **dúplex/full-duplex** (bidireccional simultáneo). Síncrona (reloj compartido) vs asíncrona (bits inicio/parada). Serie (estándar actual) vs paralelo (en desuso por skew).

### Equipos y dispositivos de interconexión

DTE (origen/destino de datos) y DCE (adaptan señal al medio). Dispositivos por capa: **repetidor** (física, regenera), **hub** (física, un dominio de colisión), **puente/bridge** (enlace, tabla MAC, STP), **switch** (enlace, multipuerto, VLAN, LACP), **router** (red, tablas de encaminamiento), **gateway** (traduce protocolos hasta capa 7).

### Redes de conmutación y de difusión

**Conmutación de circuitos**: camino dedicado (telefonía RTC/RDSI). **Conmutación de paquetes**: orientada a conexión (Frame Relay, ATM) o no orientada (IP/datagramas). **Redes de difusión**: canal compartido, requieren protocolos MAC de acceso.

### Comunicaciones móviles e inalámbricas

Evolución: 1G (analógica) → 2G/GSM (digital, GPRS/EDGE 2.5G) → 3G/UMTS (HSPA) → **4G/LTE** (all-IP, EPC) → **5G NR** (eMBB, URLLC, mMTC; sub-6GHz y mmWave; network slicing). Wi-Fi: 802.11b/g → 802.11ac/Wi-Fi 5 (MU-MIMO) → 802.11ax/Wi-Fi 6-6E (OFDMA, banda 6GHz). Corto alcance: Bluetooth (802.15.1), Zigbee (802.15.4), NFC.

## Tema 7. El modelo TCP/IP y el modelo de referencia de interconexión de sistemas abiertos (OSI) de ISO. Protocolos TCP/IP.

### Modelo OSI (ISO/IEC 7498, 1984) — 7 capas

1. **Física**: bits en bruto, conectores, codificación de línea.
2. **Enlace**: tramas, CRC, control de flujo, MAC/LLC, direccionamiento MAC.
3. **Red**: encaminamiento, direccionamiento lógico (IP).
4. **Transporte**: extremo a extremo, multiplexación por puertos (TCP, UDP).
5. **Sesión**: establecimiento/sincronización de diálogos.
6. **Presentación**: representación de datos, cifrado, compresión.
7. **Aplicación**: interfaz con procesos de usuario (HTTP, FTP, SMTP, DNS).

### Modelo TCP/IP — 4 capas

Acceso a la red (capas 1-2 OSI) → Internet (capa 3, IP) → Transporte (capa 4, TCP/UDP) → Aplicación (capas 5-7 OSI). Diferencia clave: OSI es teórico-normativo previo a implementación; TCP/IP surgió de la práctica.

### Protocolos principales

**IP**: no orientado a conexión, best-effort. IPv4 (32 bits), IPv6 (128 bits, cabecera fija 40 bytes, sin fragmentación en routers, IPsec nativo, SLAAC). **TCP**: orientado a conexión, fiable, three-way handshake (SYN/SYN-ACK/ACK), control de flujo (ventana deslizante) y congestión. **UDP**: sin conexión, sin garantías, cabecera mínima — DNS, streaming, VoIP, DHCP. **ARP**: IP→MAC en el mismo segmento. **ICMP**: control/diagnóstico (`ping`, `traceroute`). **DNS**: UDP/TCP 53, jerárquico, registros A/AAAA/MX/CNAME/NS/PTR/TXT/SOA. **DHCP**: proceso DORA (Discover/Offer/Request/Acknowledge), UDP 67/68.

## Tema 8. Internet: arquitectura de red. Origen, evolución y estado actual. Principales servicios. Protocolos HTTP, HTTPS y SSL/TLS.

### Origen y evolución

**ARPANET** (1969, DARPA). **TCP/IP** (Cerf y Kahn, 1974; adoptado 1983). **HTTP/HTML/URI** (Tim Berners-Lee, CERN, 1990) → World Wide Web (servicio sobre Internet, no confundir con la infraestructura). Transición IPv4→IPv6 en curso por agotamiento de direcciones.

### Arquitectura

Jerarquía de operadoras: **Tier 1** (troncales, peering mutuo sin coste), **Tier 2** (regionales), **Tier 3** (ISP de acceso). **IXP** (puntos neutros: ESPANIX, CATNIX). **RIR** (RIPE NCC, ARIN, APNIC...) asignan bloques IP y AS. **BGP** interconecta sistemas autónomos.

### Principales servicios

WWW, correo (SMTP/POP3/IMAP), FTP/SFTP, SSH/RDP, SIP/RTP (VoIP), DNS/DHCP, IaaS/PaaS/SaaS.

### HTTP

Sin estado, petición-respuesta sobre TCP/80. Métodos: GET, POST, PUT, DELETE, PATCH. Códigos: 2xx éxito, 3xx redirección, 4xx error cliente, 5xx error servidor. **HTTP/1.1**: keep-alive. **HTTP/2**: multiplexado, HPACK. **HTTP/3**: sobre QUIC/UDP, sin head-of-line blocking.

### HTTPS y TLS

Puerto 443. **TLS 1.2/1.3** (SSL obsoleto). Handshake: ClientHello → ServerHello + certificado X.509 → validación de cadena de confianza → intercambio de claves (DHE/ECDHE, forward secrecy) → Finished → tráfico cifrado simétrico (AES-GCM). TLS 1.3 reduce a 1-RTT (0-RTT en reconexión).

## Tema 9. Seguridad y protección en redes de comunicaciones. Seguridad perimetral. Acceso remoto seguro a redes. Redes privadas virtuales (VPN). Seguridad en el puesto del usuario.

### Seguridad perimetral

**Firewall**: filtrado de paquetes (capa 3/4, sin estado), stateful (tabla de conexiones), de aplicación/proxy (capa 7). **NGFW** integra IPS y control de aplicaciones. **DMZ**: segmento aislado para servicios expuestos. **IDS** (pasivo) vs **IPS** (activo), por firmas o anomalías. Segmentación: VLAN, ACL, Zero Trust.

### Acceso remoto seguro

MFA, SSH (clave pública/privada), RDP con NLA sobre VPN, VPN SSL, **ZTNA** (acceso granular por aplicación, verificación continua).

### VPN

**IPsec**: capa 3. **AH** (integridad/autenticación, sin cifrar), **ESP** (cifrado+integridad+autenticación), **IKE** (negociación de claves, IKEv1/IKEv2). Modos: transporte (extremo a extremo) y túnel (sitio a sitio). **VPN SSL/TLS**: capa de aplicación, atraviesa NAT/firewalls con facilidad (OpenVPN). **WireGuard**: base de código reducida, ChaCha20/Curve25519.

### Seguridad en el puesto del usuario

Antivirus/EDR, cifrado de disco (BitLocker, LUKS), gestión de parches, control de USB/DLP, mínimo privilegio, MFA, formación anti-phishing, firewall personal.

## Tema 10. Redes locales. Tipología. Técnicas de transmisión. Métodos de acceso. Dispositivos de interconexión.

### Topologías

**Bus** (medio compartido lineal, un fallo colapsa todo), **anillo** (Token Ring, FDDI), **estrella** (dominante hoy, físicamente hacia switches), **malla** (redundancia alta, backbones), **árbol** (estrellas jerárquicas).

### Técnicas de transmisión

**Banda base**: señal digital sin modular, todo el canal (Ethernet); codificación Manchester, 4B/5B, 8B/10B. **Banda ancha**: FDM, múltiples canales de frecuencia (CATV, HFC).

### Métodos de acceso al medio

**CSMA/CD**: Ethernet half-duplex clásico, detecta colisiones, backoff exponencial binario (inoperante en Ethernet full-duplex moderno con switch). **CSMA/CA**: redes inalámbricas 802.11, evita colisiones (no puede detectarlas), RTS/CTS para nodo oculto, ACK explícito por trama. **Paso de testigo**: Token Ring/FDDI, sin colisiones por diseño.

### Dispositivos de interconexión

Repetidor (física), hub (física, dominio de colisión único), puente/bridge (enlace, STP/802.1D), switch (enlace, VLAN 802.1Q, LACP/802.3ad, RSTP), router (red, OSPF/RIP/EIGRP), gateway (traduce protocolos), AP inalámbrico (puente radio-Ethernet).
