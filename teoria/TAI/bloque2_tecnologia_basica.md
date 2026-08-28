# TAI — Bloque II: Tecnología básica

## Tema 1. Informática básica. Representación y comunicación de la información: elementos constitutivos de un sistema de información. Características y funciones. Arquitectura de ordenadores. Componentes internos de los equipos microinformáticos.

### Representación de la información

Los sistemas digitales representan cualquier tipo de información mediante dígitos binarios (bits), agrupados en bytes (8 bits). La codificación numérica emplea sistemas posicionales: binario (base 2), octal (base 8) y hexadecimal (base 16), este último muy utilizado para representar direcciones de memoria y valores de color por su correspondencia directa con grupos de 4 bits (nibbles). Para números con signo se emplea habitualmente el complemento a 2, que permite realizar restas mediante sumas y evita la ambigüedad del cero con signo: en n bits el rango va de -2^(n-1) a 2^(n-1)-1 (en 8 bits, de -128 a +127). Los números reales se representan en coma flotante según el estándar IEEE 754, que distingue signo, exponente y mantisa: precisión simple (32 bits: 1 de signo + 8 de exponente + 23 de mantisa) y precisión doble (64 bits: 1 + 11 + 52).

La representación de caracteres ha evolucionado desde ASCII (7 bits, 128 caracteres) hasta Unicode, que asigna un punto de código único a cada carácter de cualquier alfabeto; su codificación más extendida en transmisión y almacenamiento es UTF-8, de longitud variable (1 a 4 bytes) y compatible con ASCII. Otros códigos relevantes: EBCDIC (mainframes IBM), BCD (decimal codificado en binario) y mecanismos de detección de errores (bit de paridad, checksum, CRC).

**Unidades de medida.** En informática se emplean potencias de 2: 1 KiB = 1024 bytes (convención JEDEC: KB, MB, GB), mientras que el sistema SI usa potencias de 10 (1 kB = 1000 bytes). La RAM se mide en base 2 y los discos comerciales anuncian capacidad en base 10, lo que explica la discrepancia de capacidad "real" (un disco de 500 GB muestra ~465 GiB).

### Elementos constitutivos de un sistema de información

Un sistema de información se compone de: hardware (soporte físico), software (programas de sistema y de aplicación), datos, procedimientos y personas. Sus funciones básicas son entrada, proceso, almacenamiento, salida y comunicación de la información, articuladas para dar soporte a los procesos de una organización, garantizando integridad, disponibilidad y confidencialidad.

### Arquitectura de ordenadores: Von Neumann y Harvard

La mayoría de los ordenadores actuales siguen el modelo de Von Neumann, caracterizado por almacenar programa y datos en la misma memoria y ejecutar instrucciones secuencialmente mediante el ciclo de instrucción: captación (fetch), decodificación (decode), ejecución (execute) y escritura del resultado (writeback). Este modelo presenta la limitación conocida como "cuello de botella de Von Neumann", pues la CPU y la memoria comparten un único bus, limitando el paralelismo. Frente a ella, la arquitectura Harvard emplea memorias y buses separados para instrucciones y datos, habitual en microcontroladores y DSP.

**CISC vs RISC.** CISC (x86) ofrece muchas instrucciones complejas ejecutadas mediante microcódigo; RISC (ARM, MIPS, RISC-V) usa un conjunto reducido de instrucciones simples, de ejecución en un ciclo, con más registros y segmentación eficiente.

**CPU.** Integra la ALU (unidad aritmético-lógica), la unidad de control (UC, que decodifica y secuencia las instrucciones) y los registros: PC/IP (contador de programa), IR (registro de instrucción), MAR (dirección de memoria), MBR (datos de memoria) y acumulador. Los procesadores actuales incorporan varios núcleos, memoria caché (L1, L2, L3), segmentación (pipelining) y ejecución fuera de orden (out-of-order) para mejorar el rendimiento.

### Buses del sistema

El bus es el conjunto de líneas físicas que permiten la comunicación entre componentes. Se distinguen tres tipos funcionales: bus de direcciones (unidireccional, indica la posición de memoria o dispositivo a acceder; el número de líneas determina la memoria direccionable: 2^n posiciones), bus de datos (bidireccional, transporta la información) y bus de control (señales de sincronización, lectura/escritura, interrupciones). A nivel de expansión, los sistemas actuales usan buses serie de alta velocidad como PCI Express (organizado en lanes x1/x4/x8/x16), sustituyendo a los antiguos buses paralelos ISA y PCI.

### Memoria

**Jerarquía de memoria:** se organiza en niveles según velocidad y coste: registros, caché (L1, L2, L3), memoria principal (RAM), memoria secundaria (SSD/HDD) y almacenamiento externo, aplicando el principio de localidad temporal y espacial para optimizar el acceso.

**RAM (volátil):** la DRAM necesita refresco periódico y es más barata (memoria principal); la SRAM es más rápida y cara, sin refresco, usada en caché. Predominan los módulos DDR SDRAM (DDR3, DDR4, DDR5), con doble transferencia de datos por ciclo.

**ROM y variantes (no volátiles):** ROM (grabada en fabricación), PROM (programable una vez), EPROM (borrable por luz ultravioleta), EEPROM (borrable eléctricamente) y memoria flash (SSD, pendrives, firmware). Almacenan el firmware, incluida la BIOS/UEFI, encargada del arranque (POST, Power-On Self-Test) y la inicialización del hardware.

### Componentes internos de los equipos microinformáticos

**Placa base:** integra el chipset (puente norte y puente sur, o su equivalente unificado en procesadores modernos), los zócalos de CPU y memoria (DIMM), y los conectores de expansión y almacenamiento (SATA, M.2/NVMe).

**Fuente de alimentación:** convierte corriente alterna en las tensiones continuas requeridas por los componentes (norma ATX: 3,3 V, 5 V y 12 V).

**Otros componentes:** tarjeta gráfica (GPU, con memoria dedicada VRAM), tarjeta de red, sistema de refrigeración (disipadores, ventiladores, refrigeración líquida) y chasis.

### Trampas habituales de examen

- **Complemento a 2**: en n bits el rango va de -2^(n-1) a 2^(n-1)-1; en 8 bits, de -128 a +127 (no -127 a +127). Existe un solo cero.
- **IEEE 754 simple**: 1+8+23 bits (no 1+8+24); doble: 1+11+52.
- **ASCII = 7 bits / 128 caracteres** (no 8 bits/256, eso es el ASCII extendido o Latin-1).
- **Unidades**: KiB (1024) vs kB (1000) — la RAM se mide en base 2, los discos en base 10.
- **Bus de direcciones unidireccional vs bus de datos bidireccional**: el examen invierte con frecuencia la dirección de los buses.
- **Von Neumann**: programa y datos en la misma memoria y un único bus (cuello de botella); Harvard: memorias y buses separados.
- **CISC vs RISC**: ARM es RISC (no CISC); x86 es CISC. RISC = instrucciones simples en un ciclo.
- **SRAM vs DRAM**: SRAM en caché (rápida, cara, sin refresco); DRAM en memoria principal (requiere refresco periódico).

## Tema 2. Periféricos: conectividad y administración. Elementos de impresión. Elementos de almacenamiento. Elementos de visualización y digitalización.

### Concepto y clasificación de periféricos

Los periféricos son dispositivos que permiten la comunicación entre el ordenador y el exterior. Se clasifican en periféricos de entrada (teclado, ratón, escáner, lector biométrico, lector de código de barras), de salida (monitor, impresora, altavoces), de entrada/salida (pantallas táctiles, módems, unidades de almacenamiento) y de almacenamiento (discos, unidades flash).

### Conectividad

La conexión de periféricos se realiza mediante interfaces estandarizadas.

**USB (Universal Serial Bus)** es la más extendida, con versiones que evolucionan en velocidad: USB 2.0 (hasta 480 Mbps), USB 3.0/3.1 Gen1 (5 Gbps), USB 3.1 Gen2/3.2 Gen2 (10 Gbps), USB 3.2 Gen2x2 (20 Gbps) y USB4 (hasta 40 Gbps, convergiendo con Thunderbolt 3/4). El conector Tipo C es reversible y admite suministro de energía mediante USB Power Delivery.

**Almacenamiento interno:** SATA (Serial ATA; SATA III hasta 6 Gbps) y, con mayor ancho de banda, NVMe sobre bus PCIe (con colas de comandos masivas); en el ámbito empresarial, SAS (Serial Attached SCSI, full-duplex).

**Inalámbrico:** Bluetooth (comunicación de corto alcance entre dispositivos personales) y Wi-Fi (conectividad de red local).

**Vídeo:** HDMI (audio y vídeo digital, estándar doméstico) y DisplayPort (mayor ancho de banda, soporte multi-stream), que sustituyen a interfaces analógicas como VGA; Thunderbolt combina datos, vídeo y energía sobre USB-C.

**Administración de periféricos.** El sistema operativo gestiona los dispositivos mediante controladores (drivers), programas que traducen las órdenes genéricas del sistema a las instrucciones específicas del dispositivo. El sistema Plug and Play (PnP) permite la detección y configuración automática; el gestor de dispositivos (Windows) o los subsistemas udev/sysfs (Linux) permiten consultar el estado, actualizar drivers y resolver conflictos de recursos (IRQ, direcciones de E/S, canales DMA).

### Elementos de impresión

Las impresoras se clasifican según su tecnología:
- **Inyección de tinta**: proyectan gotas mediante cabezales térmicos o piezoeléctricos; adecuadas para color y bajo volumen.
- **Láser**: emplean un tambor fotosensible cargado electrostáticamente que fija el tóner mediante calor y presión (fusor); mayor velocidad y coste por copia inferior en grandes volúmenes.
- **Matriciales o de impacto**: agujas que golpean una cinta entintada; aún usadas para impresión multicopia (formularios).
- **Térmicas**: por transferencia o sublimación térmica, típicas de tickets y etiquetas.

Las impresoras 3D (FDM, SLA) constituyen una categoría creciente (fabricación aditiva capa a capa). Los lenguajes de descripción de página como PostScript o PCL, y el protocolo IPP (Internet Printing Protocol), gestionan la comunicación entre el sistema y el dispositivo en entornos de red.

### Elementos de almacenamiento

- **Magnético (HDD):** platos giratorios y cabezales de lectura/escritura; velocidad de giro 5.400/7.200/10.000/15.000 RPM; tiempo de acceso = tiempo de búsqueda (seek) + latencia rotacional; menor coste por GB.
- **Óptico:** CD, DVD, Blu-ray, que codifican información mediante variaciones reflectantes leídas por láser.
- **Estado sólido (SSD):** memoria flash NAND, sin partes móviles, menor latencia y mayor velocidad de acceso aleatorio; requieren TRIM para mantener el rendimiento; mayor coste por GB.

Los parámetros técnicos relevantes incluyen capacidad, tiempo de acceso, velocidad de transferencia y fiabilidad (MTBF). Para configuraciones redundantes se emplean sistemas RAID:
- **RAID 0 (striping):** datos repartidos en bloques; solo rendimiento, sin redundancia (un fallo pierde todo).
- **RAID 1 (mirroring):** copia íntegra en dos discos; tolera 1 fallo; la mitad de la capacidad útil.
- **RAID 5:** paridad distribuida; tolera 1 fallo; mínimo 3 discos.
- **RAID 6:** doble paridad; tolera 2 fallos; mínimo 4 discos.
- **RAID 10 (1+0):** espejo de bandas; rendimiento y tolerancia; mínimo 4 discos.

### Elementos de visualización y digitalización

Los monitores actuales utilizan mayoritariamente tecnología LCD/LED (cristal líquido con retroiluminación), con variantes IPS (mejor fidelidad de color y ángulo de visión) y OLED (píxeles autoemisivos, mayor contraste y negros puros, sin retroiluminación). Los parámetros clave son resolución, tasa de refresco (Hz), tiempo de respuesta y relación de aspecto.

En digitalización, los escáneres (de sobremesa, de rodillo o de mano) capturan imágenes mediante sensores CCD o CIS, convirtiendo la señal analógica en una matriz de píxeles digital, cuya calidad depende de la resolución (ppp, puntos por pulgada) y la profundidad de color. Las cámaras de documentos y los sistemas OCR (reconocimiento óptico de caracteres) complementan la digitalización, transformando imágenes de texto en texto editable, funcionalidad clave en la gestión documental de la Administración.

### Trampas habituales de examen

- **USB 2.0 = 480 Mbps** (no 480 MB/s); USB 3.0 = 5 Gbps; USB 3.1 Gen2 = 10 Gbps; USB4 = 40 Gbps (converge con Thunderbolt).
- **RAID**: RAID 0 no da redundancia (solo rendimiento); RAID 1 tolera 1 fallo; RAID 5 tolera 1 fallo (mínimo 3 discos); RAID 6 tolera 2 (mínimo 4); RAID 10 = espejo de bandas (mínimo 4).
- **HDD vs SSD**: HDD tiene partes móviles (platos y cabezales); SSD no. TRIM es una operación de SSD, no de HDD.
- **HDMI vs DisplayPort**: DisplayPort tiene mayor ancho de banda y multi-stream; HDMI es el estándar doméstico (audio+vídeo).
- **SATA III = 6 Gbps**; NVMe va sobre PCIe (mucho mayor ancho de banda y profundidad de cola que SATA).
- **Monitor OLED**: píxeles autoemisivos, sin retroiluminación; el LCD/LED la necesita.
- **Impresora láser**: tambor + tóner + fusor (calor y presión); la matricial es de impacto (impresión multicopia).

## Tema 3. Tipos abstractos y Estructuras de datos. Organizaciones de ficheros. Algoritmos. Formatos de información y ficheros.

### Tipos abstractos de datos (TAD)

Un tipo abstracto de datos define un conjunto de valores y las operaciones aplicables sobre ellos, independientemente de su implementación concreta. Esta separación entre interfaz (especificación) y representación interna constituye la base de la abstracción y el encapsulamiento en programación. Ejemplos clásicos de TAD son pila, cola, lista, conjunto y diccionario (o mapa clave-valor).

### Estructuras de datos lineales

**Pila (stack):** estructura LIFO (Last In, First Out) con operaciones push (inserción) y pop (extracción) restringidas a un extremo (la cima). Se emplea en la gestión de llamadas a funciones (pila de ejecución), evaluación de expresiones, algoritmos de recorrido en profundidad (DFS) y deshacer/rehacer (undo/redo).

**Cola (queue):** estructura FIFO (First In, First Out), con inserción por un extremo (encolar/enqueue) y extracción por el opuesto (desencolar/dequeue). Variantes destacadas: la cola de prioridad, donde cada elemento se extrae según una prioridad asociada (implementada típicamente con un heap), y la cola circular, que reutiliza el espacio del array de forma eficiente.

**Listas enlazadas:** secuencias de nodos donde cada uno contiene un dato y un puntero al siguiente (y al anterior en las doblemente enlazadas; circulares si el último apunta al primero). Frente a los arrays, permiten inserción y borrado en tiempo constante O(1) sin desplazamiento de elementos, a costa de un acceso secuencial (sin indexación directa).

### Estructuras de datos no lineales

**Árboles:** estructuras jerárquicas compuestas por nodos y aristas, con un nodo raíz y ausencia de ciclos. El árbol binario de búsqueda (ABB) mantiene la propiedad de que el subárbol izquierdo contiene valores menores y el derecho mayores, permitiendo búsquedas en tiempo logarítmico O(log n) en el caso medio; los árboles equilibrados (AVL, rojo-negro) garantizan esta complejidad en el peor caso mediante rebalanceo. Los árboles B y B+ (multivía) son ampliamente usados en índices de bases de datos y sistemas de ficheros por optimizar el acceso a almacenamiento secundario; en el B+ los datos residen solo en las hojas, enlazadas entre sí, lo que optimiza los recorridos en rango.

**Grafos:** conjuntos de vértices y aristas (dirigidos o no, con o sin peso) que modelan relaciones complejas. Se representan con listas o matrices de adyacencia y se recorren en anchura (BFS, con cola) o en profundidad (DFS, con pila o recursión). Problemas clásicos: camino mínimo (algoritmo de Dijkstra para pesos no negativos) y árbol de recubrimiento mínimo (Kruskal, Prim).

**Tablas hash:** estructuras que aplican una función hash para mapear claves a posiciones de un array, ofreciendo acceso en tiempo medio constante O(1); requieren estrategias de resolución de colisiones (encadenamiento separado o direccionamiento abierto: sondeo lineal, cuadrático, doble hash). No soportan búsqueda por rango de forma eficiente.

### Organización de ficheros

La organización secuencial almacena los registros en orden físico consecutivo, adecuada para procesamiento por lotes. La organización indexada mantiene una estructura auxiliar (habitualmente un árbol B+) que relaciona claves con posiciones físicas, permitiendo acceso directo eficiente. La organización directa o relativa (hash) calcula la dirección física a partir de la clave mediante una función de dispersión. La organización indexada-secuencial (ISAM) combina ambos enfoques, permitiendo tanto recorrido ordenado como acceso directo.

### Algoritmos y complejidad

Un algoritmo es una secuencia finita y no ambigua de pasos que resuelve un problema. Su eficiencia se mide mediante la notación asintótica: **O** (cota superior, peor caso), **Ω** (cota inferior, mejor caso) y **Θ** (cota ajustada). Complejidades habituales ordenadas: O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ).

**Ordenación:** los algoritmos simples (burbuja, inserción, selección) son O(n²); los eficientes alcanzan O(n log n): quicksort (peor caso O(n²) con un pivote desfavorable; in-place), mergesort (estable, O(n log n) garantizado, con O(n) de espacio extra) y heapsort (in-place, O(1) de espacio extra, no estable). La búsqueda binaria sobre datos ordenados requiere O(log n) frente a la búsqueda lineal O(n).

**Recursividad:** toda función recursiva consta de caso base y caso recursivo, y es transformable a iterativa mediante una pila explícita (relación directa con el TAD pila).

### Formatos de información y ficheros

Los formatos de texto estructurado como XML, JSON y YAML permiten el intercambio de información entre sistemas heterogéneos, con distinto grado de verbosidad y capacidad de tipado (XML muy verboso, JSON ligero y estándar en APIs, YAML legible y habitual en configuración). Los formatos binarios (imágenes, audio, vídeo, documentos ofimáticos) incluyen cabeceras con metadatos y, frecuentemente, compresión: sin pérdida (ZIP, PNG) o con pérdida (JPEG, MP3), en función del compromiso entre tamaño y fidelidad admisible.

### Trampas habituales de examen

- **Pila LIFO vs cola FIFO**: push/pop vs encolar/desencolar — el examen suele intercambiar las operaciones y el orden de extracción.
- **Ordenación**: quicksort es O(n log n) en el caso medio pero O(n²) en el peor; mergesort garantiza O(n log n) con O(n) de espacio; heapsort es in-place (O(1) espacio) pero no estable.
- **Búsqueda binaria**: exige datos ordenados; si no lo están, la búsqueda es lineal O(n).
- **Notación**: O es cota superior (peor caso), Ω cota inferior (mejor caso), Θ cota ajustada.
- **Árbol B+**: los datos están solo en las hojas (enlazadas entre sí); en el B clásico están en todos los nodos.
- **Hash**: O(1) medio para igualdad exacta; no sirve para búsquedas por rango.
- **Cola de prioridad**: se implementa típicamente con un heap, no con una cola normal.
- **UTF-8**: longitud variable (1-4 bytes) y compatible con ASCII (los primeros 128 puntos de código ocupan 1 byte).

## Tema 4. Sistemas operativos. Características y elementos constitutivos. Sistemas Windows. Sistemas Unix y Linux. Sistemas operativos para dispositivos móviles.

### Concepto y funciones del sistema operativo

El sistema operativo es el software que gestiona los recursos hardware y ofrece una interfaz uniforme a las aplicaciones y al usuario. Sus funciones principales son la gestión de procesos, de memoria, del sistema de archivos, de dispositivos de entrada/salida y la seguridad, además de actuar como máquina virtual que abstrae la complejidad del hardware subyacente.

**Estructuras de los SO:** monolítico (todo el núcleo en espacio de kernel, rápido pero acoplado — Linux), microkernel (mínimo en el núcleo, servicios en espacio de usuario — Minix, QNX) e híbrido (combina ambos — Windows NT, macOS/XNU).

### Gestión de procesos

Un proceso es un programa en ejecución, con su propio espacio de direcciones, estado y recursos asignados. Puede encontrarse en estados de nuevo, preparado (listo), en ejecución, bloqueado o terminado, transiciones gestionadas por el planificador (scheduler). Los hilos (threads) son unidades de ejecución dentro de un proceso que comparten memoria, permitiendo concurrencia con menor sobrecarga que procesos independientes.

**Algoritmos de planificación:** FCFS (orden de llegada, no apropiativo), SJF (trabajo más corto primero, óptimo en tiempo medio de espera pero con riesgo de inanición), Round Robin (quantum fijo, apropiativo, adecuado para sistemas interactivos) y por prioridades (con riesgo de inanición, mitigado con aging — aumento gradual de la prioridad con el tiempo). También existen las colas multinivel.

**Concurrencia y sincronización:** exclusión mutua, semáforos (contador con operaciones wait/signal), mutex (semáforo binario) y monitores. El interbloqueo (deadlock) requiere las cuatro condiciones de Coffman simultáneas: exclusión mutua, retención y espera, no apropiación y espera circular.

### Gestión de memoria

Los sistemas actuales emplean memoria virtual, que independiza el espacio de direcciones lógico del físico mediante paginación (bloques de tamaño fijo: páginas y marcos; evita la fragmentación externa pero genera interna) o segmentación (bloques de tamaño variable con significado lógico). La MMU (unidad de gestión de memoria) traduce direcciones virtuales a físicas con ayuda de la tabla de páginas y el buffer TLB (Translation Lookaside Buffer). Cuando la memoria física es insuficiente, se recurre al intercambio (swapping) con el área de paginación en disco. Algoritmos de reemplazo de página: FIFO, LRU (menos usada recientemente, la mejor aproximación práctica) y el óptimo (teórico, usado como referencia de comparación).

### Sistemas de archivos

El sistema de archivos organiza el almacenamiento persistente en una estructura jerárquica de directorios y ficheros, gestionando metadatos (permisos, fechas, propietario) e implementando mecanismos de asignación de espacio (contigua, enlazada o indexada) y de recuperación ante fallos mediante journaling, que registra las operaciones antes de aplicarlas para garantizar la consistencia. Sistemas representativos: **FAT32** (límite de 4 GB por archivo, sin journaling, máxima compatibilidad), **exFAT** (sin límite práctico de tamaño de archivo, para dispositivos extraíbles), **NTFS** (Windows: permisos ACL, compresión, cifrado EFS y journaling) y **ext4** (Linux: journaling, extents, soporte de volúmenes grandes).

### Sistemas Windows

Windows es un sistema operativo propietario de Microsoft con arquitectura híbrida (núcleo con componentes en espacio de kernel y de usuario). Su sistema de archivos principal es NTFS, que soporta permisos ACL, compresión, cifrado (EFS) y journaling. La gestión de usuarios y equipos en entornos corporativos se realiza mediante Active Directory (AD), que centraliza la autenticación (protocolo Kerberos) y las políticas de grupo (GPO, Group Policy Objects). El registro de Windows (registry) almacena la configuración del sistema y las aplicaciones en una base de datos jerárquica. Herramientas administrativas: Administrador de tareas, visor de eventos, administrador de dispositivos, administración de discos y PowerShell.

### Sistemas Unix y Linux

Unix, desarrollado en Bell Labs en los años setenta, estableció principios como "todo es un fichero", la composición de utilidades simples mediante tuberías (pipes) y un sistema de permisos basado en propietario, grupo y otros (rwx). Linux es un núcleo de código abierto inspirado en Unix (creado por Linus Torvalds en 1991), sobre el que se construyen distribuciones (Debian/Ubuntu, Red Hat/Fedora, openSUSE) que integran gestores de paquetes (APT con paquetes .deb, DNF/YUM con .rpm), sistemas de ficheros como ext4, XFS o Btrfs, y el sistema de inicio systemd, que gestiona servicios y dependencias de arranque (systemctl). La administración remota se realiza habitualmente mediante SSH, y la shell (bash u otras) permite la automatización mediante scripts.

### Sistemas operativos para dispositivos móviles

Android, basado en el núcleo Linux, emplea la máquina virtual ART (Android Runtime) para ejecutar aplicaciones y organiza los componentes en actividades, servicios y proveedores de contenido, con un modelo de permisos granular y ciclo de vida de aplicación gestionado por el propio sistema para optimizar batería y memoria. iOS, de Apple, se basa en un núcleo derivado de Unix (Darwin/XNU) y aplica un modelo de aislamiento estricto entre aplicaciones (sandboxing), distribución controlada mediante App Store y una gestión de memoria basada en conteo automático de referencias (ARC). Ambos sistemas comparten características frente a los de escritorio: mayor restricción de recursos, gestión activa del consumo energético y modelos de permisos orientados a la privacidad del usuario.

### Trampas habituales de examen

- **Proceso vs hilo**: el proceso tiene espacio de memoria propio; los hilos lo comparten (cambio de contexto más barato).
- **Estados del proceso**: nuevo → preparado → ejecución → bloqueado → terminado. El estado "bloqueado" espera un evento (p. ej. E/S), no es por agotamiento del quantum.
- **Round Robin**: apropiativo con quantum fijo, bueno para interactivos; SJF es óptimo en tiempo medio de espera pero causa inanición en su forma pura.
- **Deadlock**: las 4 condiciones de Coffman deben darse a la vez (exclusión mutua, retención y espera, no apropiación, espera circular).
- **Paginación vs segmentación**: paginación = bloques fijos (fragmentación interna); segmentación = bloques lógicos variables (fragmentación externa).
- **Reemplazo de página**: LRU es la mejor aproximación práctica; el óptimo es teórico (requiere conocer el futuro).
- **FAT32**: límite de 4 GB por archivo y sin journaling; NTFS con ACL y EFS; exFAT para extraíbles sin límite práctico.
- **Active Directory**: autenticación Kerberos y GPO; no confundir con el registro de Windows (configuración local del sistema).
- **Android vs iOS**: Android usa ART sobre el kernel Linux; iOS usa XNU/Darwin (Unix) con sandboxing y ARC.

## Tema 5. Sistemas de gestión de bases de datos relacionales, orientados a objetos y NoSQL: características y componentes.

### Concepto y componentes de un SGBD

Un sistema de gestión de bases de datos (SGBD) es el software que permite definir, crear, mantener y controlar el acceso a una base de datos. Sus componentes principales son el motor de almacenamiento, el procesador de consultas (parser, optimizador y ejecutor), el gestor de transacciones, el catálogo o diccionario de datos (metadatos) y los módulos de seguridad y control de concurrencia. Ofrece independencia entre los datos y las aplicaciones que los utilizan, evitando la redundancia y garantizando su integridad. Funciones: definición de datos (DDL), manipulación (DML), control de acceso (DCL), gestión de transacciones, copias de seguridad y recuperación.

### Modelo relacional

Propuesto por E.F. Codd (1970), organiza los datos en relaciones (tablas), formadas por tuplas (filas) y atributos (columnas), cada uno definido sobre un dominio de valores válidos. La integridad se garantiza mediante claves primarias (identificación única de cada tupla, no nulas), claves ajenas o foráneas (referencias entre tablas, que materializan la integridad referencial) y restricciones de dominio.

**Álgebra relacional:** operaciones fundamentales: selección (σ, filtra filas), proyección (π, filtra columnas), unión, intersección, diferencia, producto cartesiano y join (combinación de tablas: inner, left/right/full outer, natural).

**Normalización:** el proceso, a través de las formas normales, elimina redundancias y anomalías de actualización, inserción y borrado, descomponiendo las relaciones según las dependencias funcionales: 1FN (atributos atómicos, sin grupos repetidos), 2FN (sin dependencias parciales de la clave), 3FN (sin dependencias transitivas) y FNBC (toda determinante es clave candidata).

**SQL:** el lenguaje estándar, con sentencias DDL (CREATE, ALTER, DROP), DML (SELECT, INSERT, UPDATE, DELETE), DCL (GRANT, REVOKE) y TCL (COMMIT, ROLLBACK, SAVEPOINT).

**Índices:** estructuras que aceleran el acceso a los datos: B-tree/B+tree (búsqueda por rango y por orden, uso general) e índices hash (igualdad exacta, O(1) medio, no sirven para rangos).

### Propiedades ACID

Las transacciones en un SGBD relacional cumplen las propiedades ACID: Atomicidad (una transacción se ejecuta completa o no se ejecuta — todo o nada), Consistencia (las restricciones de integridad se mantienen antes y después), Aislamiento (las transacciones concurrentes no interfieren entre sí, con niveles como read uncommitted, read committed, repeatable read y serializable) y Durabilidad (los cambios confirmados persisten ante fallos, típicamente mediante un log de transacciones — WAL). Ejemplos de SGBD relacionales: Oracle, SQL Server, PostgreSQL y MySQL/MariaDB.

### Modelo orientado a objetos

Los SGBD orientados a objetos almacenan directamente objetos, con su estado (atributos) y comportamiento (métodos), soportando herencia, encapsulamiento y polimorfismo, evitando el desajuste de impedancia (impedance mismatch) que se produce al mapear objetos de un lenguaje de programación a tablas relacionales. Existe también el enfoque objeto-relacional, que extiende el modelo relacional con tipos de datos complejos, herencia de tablas y métodos almacenados, adoptado parcialmente por motores como PostgreSQL u Oracle.

### Bases de datos NoSQL

Surgen para dar respuesta a requisitos de escalabilidad horizontal, esquemas flexibles y grandes volúmenes de datos no necesariamente estructurados (Big Data), habitualmente relajando las garantías ACID a favor del modelo BASE (Basically Available, Soft state, Eventually consistent), que prioriza la disponibilidad y la consistencia eventual frente a la consistencia inmediata, conforme describe el teorema CAP (Consistencia, Disponibilidad y tolerancia a Particiones): un sistema distribuido solo puede garantizar plenamente dos de esas tres propiedades simultáneamente, de modo que ante una partición de red debe elegirse entre consistencia fuerte (CP) o disponibilidad (AP).

Se distinguen cuatro categorías principales:

**Clave-valor:** la estructura más simple, almacena pares identificador-valor sin esquema fijo, con acceso muy eficiente por clave (Redis, DynamoDB), habitual en caché y sesiones.

**Documentales:** almacenan documentos semiestructurados, típicamente en formato JSON o BSON, permitiendo estructuras anidadas y esquemas variables entre documentos de una misma colección (MongoDB, CouchDB).

**Orientadas a columnas (columnares):** organizan los datos por familias de columnas en lugar de por filas, optimizando la lectura de grandes volúmenes analíticos y la escalabilidad distribuida de escritura (Cassandra, HBase).

**De grafos:** modelan explícitamente entidades (nodos) y sus relaciones (aristas), optimizadas para consultas de recorrido y de relaciones complejas, como redes sociales o sistemas de recomendación (Neo4j).

### Consideraciones de selección

La elección entre modelo relacional y NoSQL depende de los requisitos del sistema: el modelo relacional resulta idóneo cuando se requiere integridad transaccional estricta y relaciones complejas bien definidas (ACID), mientras que las soluciones NoSQL se orientan a escenarios de alta escalabilidad horizontal, esquemas cambiantes o grandes volúmenes de datos semiestructurados (BASE). Es frecuente en arquitecturas actuales la coexistencia de ambos paradigmas (polyglot persistence) según la naturaleza de cada componente del sistema de información.

### Trampas habituales de examen

- **ACID vs BASE**: relacional = ACID (consistencia inmediata); NoSQL = BASE (consistencia eventual).
- **CAP**: solo 2 de 3 (Consistencia, Disponibilidad, tolerancia a Particiones); ante una partición de red se elige CP o AP — ningún sistema garantiza las tres a la vez.
- **Formas normales**: 1FN atributos atómicos; 2FN sin dependencias parciales (requiere clave compuesta); 3FN sin dependencias transitivas; FNBC toda determinante es clave candidata.
- **Join**: inner (solo coincidencias), left/right outer (conserva todos los de un lado), full outer (todos).
- **Índices**: B-tree/B+ para rangos y orden; hash solo para igualdad exacta.
- **SQL**: DDL (definición), DML (manipulación), DCL (control de acceso: GRANT/REVOKE), TCL (transacciones: COMMIT/ROLLBACK) — no confundir GRANT/REVOKE con COMMIT/ROLLBACK.
- **NoSQL por categoría**: MongoDB = documental; Redis/DynamoDB = clave-valor; Cassandra/HBase = columnar; Neo4j = grafos.
- **Niveles de aislamiento** (de menor a mayor garantía): read uncommitted, read committed, repeatable read, serializable.
