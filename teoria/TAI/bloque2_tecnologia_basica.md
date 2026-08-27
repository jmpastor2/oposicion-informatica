# TAI — Bloque II: Tecnología básica

## Tema 1. Informática básica. Representación y comunicación de la información: elementos constitutivos de un sistema de información. Características y funciones. Arquitectura de ordenadores. Componentes internos de los equipos microinformáticos.

### Representación de la información

Los sistemas digitales representan cualquier tipo de información mediante dígitos binarios (bits), agrupados en bytes (8 bits). La codificación numérica emplea sistemas posicionales: binario (base 2), octal (base 8) y hexadecimal (base 16), este último muy utilizado para representar direcciones de memoria y valores de color por su correspondencia directa con grupos de 4 bits (nibbles). Para números con signo se emplea habitualmente el complemento a 2, que permite realizar restas mediante sumas y evita la ambigüedad del cero con signo. Los números reales se representan en coma flotante según el estándar IEEE 754, que distingue signo, exponente y mantisa, en precisión simple (32 bits) o doble (64 bits).

La representación de caracteres ha evolucionado desde ASCII (7 bits, 128 caracteres) hasta Unicode, que asigna un punto de código único a cada carácter de cualquier alfabeto; su codificación más extendida en transmisión y almacenamiento es UTF-8, de longitud variable y compatible con ASCII.

### Elementos constitutivos de un sistema de información

Un sistema de información se compone de: hardware (soporte físico), software (programas de sistema y de aplicación), datos, procedimientos y personas. Sus funciones básicas son entrada, proceso, almacenamiento, salida y comunicación de la información, articuladas para dar soporte a los procesos de una organización, garantizando integridad, disponibilidad y confidencialidad.

### Arquitectura de Von Neumann

La mayoría de los ordenadores actuales siguen el modelo de Von Neumann, caracterizado por almacenar programa y datos en la misma memoria y ejecutar instrucciones secuencialmente mediante el ciclo de instrucción: captación (fetch), decodificación (decode), ejecución (execute) y, en su caso, escritura del resultado. Este modelo presenta la limitación conocida como "cuello de botella de Von Neumann", pues la CPU y la memoria comparten un único bus, limitando el paralelismo. Frente a ella, la arquitectura Harvard emplea memorias y buses separados para instrucciones y datos, habitual en microcontroladores y DSP.

### Buses del sistema

El bus es el conjunto de líneas físicas que permiten la comunicación entre componentes. Se distinguen tres tipos funcionales: bus de direcciones (unidireccional, indica la posición de memoria o dispositivo a acceder), bus de datos (bidireccional, transporta la información) y bus de control (señales de sincronización, lectura/escritura, interrupciones). A nivel de expansión, los sistemas actuales usan buses serie de alta velocidad como PCI Express, sustituyendo a los antiguos buses paralelos ISA y PCI.

### Componentes internos de los equipos microinformáticos

**CPU (unidad central de proceso):** integra la ALU (unidad aritmético-lógica), la unidad de control y los registros. Los procesadores actuales incorporan varios núcleos, memoria caché (L1, L2, L3) y técnicas de segmentación (pipelining) y ejecución fuera de orden para mejorar el rendimiento.

**Memoria principal:** la RAM (volátil) almacena programas y datos en ejecución; predominan los módulos DDR (Double Data Rate) SDRAM. La ROM y sus variantes (EEPROM, memoria flash) almacenan el firmware, incluida la BIOS/UEFI, encargada del arranque (POST) y la inicialización del hardware.

**Placa base:** integra el chipset (puentes norte y sur o su equivalente unificado en procesadores modernos), los zócalos de CPU y memoria, y los conectores de expansión y almacenamiento (SATA, M.2/NVMe).

**Fuente de alimentación:** convierte corriente alterna en las tensiones continuas requeridas por los componentes (norma ATX).

**Jerarquía de memoria:** se organiza en niveles según velocidad y coste: registros, caché, memoria principal, memoria secundaria (SSD/HDD) y almacenamiento externo, aplicando el principio de localidad temporal y espacial para optimizar el acceso.

## Tema 2. Periféricos: conectividad y administración. Elementos de impresión. Elementos de almacenamiento. Elementos de visualización y digitalización.

### Concepto y clasificación de periféricos

Los periféricos son dispositivos que permiten la comunicación entre el ordenador y el exterior. Se clasifican en periféricos de entrada (teclado, ratón, escáner), de salida (monitor, impresora), de entrada/salida (pantallas táctiles, módems) y de almacenamiento (discos, unidades flash).

### Conectividad

La conexión de periféricos se realiza mediante interfaces estandarizadas. USB (Universal Serial Bus) es la más extendida, con versiones que evolucionan en velocidad (USB 2.0 hasta 480 Mbps, USB 3.x por encima de 5 Gbps, USB4 convergiendo con Thunderbolt) y en conector físico (Tipo A, Tipo C, reversible y con capacidad de suministro de energía mediante USB Power Delivery). Para almacenamiento interno se emplean SATA (Serial ATA) y, con mayor ancho de banda, NVMe sobre bus PCIe. En el ámbito inalámbrico destacan Bluetooth (comunicación de corto alcance entre dispositivos personales) y Wi-Fi (conectividad de red local). Para vídeo se usan HDMI y DisplayPort, que integran audio y vídeo digital, sustituyendo a interfaces analógicas como VGA.

La administración de periféricos en el sistema operativo se realiza mediante controladores (drivers), programas que traducen las órdenes genéricas del sistema a las instrucciones específicas del dispositivo. El sistema Plug and Play permite la detección y configuración automática, y el gestor de dispositivos (Windows) o los subsistemas udev/sysfs (Linux) permiten consultar el estado, actualizar drivers y resolver conflictos de recursos (IRQ, direcciones de E/S).

### Elementos de impresión

Las impresoras se clasifican según su tecnología: de inyección de tinta (proyectan gotas mediante cabezales térmicos o piezoeléctricos, adecuadas para color y bajo volumen), láser (emplean un tambor fotosensible cargado electrostáticamente que fija el tóner mediante calor y presión, con mayor velocidad y coste por copia inferior en grandes volúmenes) y matriciales o de impacto (aún usadas para impresión multicopia). Las impresoras 3D, por adición de material capa a capa (FDM, SLA), constituyen una categoría creciente. Los lenguajes de descripción de página como PostScript o PCL, y el protocolo IPP (Internet Printing Protocol), gestionan la comunicación entre el sistema y el dispositivo en entornos de red.

### Elementos de almacenamiento

Se distingue entre almacenamiento magnético (discos duros HDD, con platos giratorios y cabezales de lectura/escritura), óptico (CD, DVD, Blu-ray, que codifican información mediante variaciones reflectantes leídas por láser) y de estado sólido (SSD, basado en memoria flash NAND, sin partes móviles, con mayor velocidad de acceso aleatorio y menor latencia). Los parámetros técnicos relevantes incluyen capacidad, tiempo de acceso, velocidad de transferencia y tasa de fallos (MTBF). Para configuraciones redundantes se emplean sistemas RAID (0, 1, 5, 6, 10), que combinan discos para mejorar rendimiento, tolerancia a fallos o ambos.

### Elementos de visualización y digitalización

Los monitores actuales utilizan mayoritariamente tecnología LCD/LED, con variantes IPS (mejor fidelidad de color y ángulo de visión) y OLED (píxeles autoemisivos, mayor contraste). Los parámetros clave son resolución, tasa de refresco, tiempo de respuesta y relación de aspecto. En digitalización, los escáneres (de sobremesa, de rodillo o de mano) capturan imágenes mediante sensores CCD o CIS, convirtiendo la señal analógica en una matriz de píxeles digital, cuya calidad depende de la resolución (ppp) y la profundidad de color. Las cámaras de documentos y los sistemas OCR (reconocimiento óptico de caracteres) complementan la digitalización, transformando imágenes de texto en texto editable, funcionalidad clave en la gestión documental de la Administración.

## Tema 3. Tipos abstractos y Estructuras de datos. Organizaciones de ficheros. Algoritmos. Formatos de información y ficheros.

### Tipos abstractos de datos (TAD)

Un tipo abstracto de datos define un conjunto de valores y las operaciones aplicables sobre ellos, independientemente de su implementación concreta. Esta separación entre interfaz y representación interna constituye la base de la abstracción y el encapsulamiento en programación. Ejemplos clásicos de TAD son pila, cola, lista, conjunto y diccionario (o mapa clave-valor).

### Estructuras de datos lineales

**Pila (stack):** estructura LIFO (Last In, First Out) con operaciones push (inserción) y pop (extracción) restringidas a un extremo. Se emplea en la gestión de llamadas a funciones (pila de ejecución), evaluación de expresiones y algoritmos de recorrido en profundidad.

**Cola (queue):** estructura FIFO (First In, First Out), con inserción por un extremo (encolar) y extracción por el opuesto (desencolar). Variantes destacadas son la cola de prioridad, donde cada elemento se extrae según un valor de prioridad asociado, y la cola circular, que reutiliza el espacio del array de forma eficiente.

**Listas enlazadas:** secuencias de nodos donde cada uno contiene un dato y un puntero al siguiente (y, en listas doblemente enlazadas, al anterior). Frente a los arrays, permiten inserción y borrado en tiempo constante sin desplazamiento de elementos, a costa de un acceso secuencial (no indexado directo).

### Estructuras de datos no lineales

**Árboles:** estructuras jerárquicas compuestas por nodos y aristas, con un nodo raíz y ausencia de ciclos. El árbol binario de búsqueda (ABB) mantiene la propiedad de que el subárbol izquierdo contiene valores menores y el derecho valores mayores, permitiendo búsquedas en tiempo logarítmico en el caso medio; los árboles equilibrados (AVL, rojo-negro) garantizan esta complejidad en el peor caso mediante rebalanceo. Los árboles B y B+ son ampliamente usados en índices de bases de datos y sistemas de ficheros por optimizar el acceso a almacenamiento secundario.

**Grafos:** conjuntos de vértices y aristas (dirigidas o no, con o sin peso) que modelan relaciones complejas, recorridos en anchura (BFS) y en profundidad (DFS), y problemas de camino mínimo (algoritmo de Dijkstra).

**Tablas hash:** estructuras que aplican una función hash para mapear claves a posiciones de un array, ofreciendo acceso en tiempo medio constante; requieren estrategias de resolución de colisiones (encadenamiento o direccionamiento abierto).

### Organización de ficheros

La organización secuencial almacena los registros en orden físico consecutivo, adecuada para procesamiento por lotes. La organización indexada mantiene una estructura auxiliar (habitualmente un árbol B+) que relaciona claves con posiciones físicas, permitiendo acceso directo eficiente. La organización directa o relativa (hash) calcula la dirección física a partir de la clave mediante una función de dispersión. La organización indexada-secuencial (ISAM) combina ambos enfoques, permitiendo tanto recorrido ordenado como acceso directo.

### Algoritmos y complejidad

Un algoritmo es una secuencia finita y no ambigua de pasos que resuelve un problema. Su eficiencia se mide mediante la notación asintótica O(n), que expresa el crecimiento del tiempo o espacio en función del tamaño de la entrada. Los algoritmos de ordenación clásicos presentan complejidades características: burbuja e inserción O(n²); mientras que quicksort y mergesort alcanzan O(n log n) en el caso medio. La búsqueda binaria sobre datos ordenados requiere O(log n) frente a la búsqueda lineal O(n).

### Formatos de información y ficheros

Los formatos de texto estructurado como XML, JSON y YAML permiten el intercambio de información entre sistemas heterogéneos, con distinto grado de verbosidad y capacidad de tipado. Los formatos binarios (imágenes, audio, vídeo, documentos ofimáticos) incluyen cabeceras con metadatos y, frecuentemente, compresión, que puede ser sin pérdida (ZIP, PNG) o con pérdida (JPEG, MP3), en función del compromiso entre tamaño y fidelidad admisible.

## Tema 4. Sistemas operativos. Características y elementos constitutivos. Sistemas Windows. Sistemas Unix y Linux. Sistemas operativos para dispositivos móviles.

### Concepto y funciones del sistema operativo

El sistema operativo es el software que gestiona los recursos hardware y ofrece una interfaz uniforme a las aplicaciones y al usuario. Sus funciones principales son la gestión de procesos, de memoria, del sistema de archivos, de dispositivos de entrada/salida y la seguridad, además de actuar como máquina virtual que abstrae la complejidad del hardware subyacente.

### Gestión de procesos

Un proceso es un programa en ejecución, con su propio espacio de direcciones, estado y recursos asignados. Puede encontrarse en estados de nuevo, preparado, en ejecución, bloqueado o terminado, transiciones gestionadas por el planificador (scheduler). Los hilos (threads) son unidades de ejecución dentro de un proceso que comparten memoria, permitiendo concurrencia con menor sobrecarga que procesos independientes. Los algoritmos de planificación (round-robin, prioridades, colas multinivel) determinan el orden de acceso a la CPU, buscando equilibrio entre tiempo de respuesta y rendimiento global.

### Gestión de memoria

Los sistemas actuales emplean memoria virtual, que independiza el espacio de direcciones lógico del físico mediante paginación (división en bloques de tamaño fijo, páginas y marcos) o segmentación (bloques de tamaño variable con significado lógico). La MMU (unidad de gestión de memoria) traduce direcciones virtuales a físicas con ayuda de la tabla de páginas y el buffer TLB. Cuando la memoria física es insuficiente, se recurre al intercambio (swapping) con el área de paginación en disco.

### Sistemas de archivos

El sistema de archivos organiza el almacenamiento persistente en una estructura jerárquica de directorios y ficheros, gestionando metadatos (permisos, fechas, propietario) e implementando mecanismos de asignación de espacio (contigua, enlazada o indexada) y de recuperación ante fallos mediante journaling, que registra las operaciones antes de aplicarlas para garantizar la consistencia.

### Sistemas Windows

Windows es un sistema operativo propietario de Microsoft con arquitectura híbrida (núcleo con componentes en espacio de kernel y de usuario). Su sistema de archivos principal es NTFS, que soporta permisos ACL, compresión, cifrado (EFS) y journaling. La gestión de usuarios y equipos en entornos corporativos se realiza mediante Active Directory, que centraliza autenticación (Kerberos) y políticas de grupo (GPO). El registro de Windows almacena la configuración del sistema y las aplicaciones en una base de datos jerárquica.

### Sistemas Unix y Linux

Unix, desarrollado en los años setenta, estableció principios como "todo es un fichero", la composición de utilidades simples mediante tuberías (pipes) y un sistema de permisos basado en propietario, grupo y otros (rwx). Linux es un núcleo de código abierto inspirado en Unix, sobre el que se construyen distribuciones (Debian, Red Hat, Ubuntu) que integran gestores de paquetes (APT, DNF/YUM), sistemas de ficheros como ext4, XFS o Btrfs, y el sistema de inicio systemd, que gestiona servicios y dependencias de arranque. La administración remota se realiza habitualmente mediante SSH, y la shell (bash u otras) permite la automatización mediante scripts.

### Sistemas operativos para dispositivos móviles

Android, basado en el núcleo Linux, emplea la máquina virtual ART para ejecutar aplicaciones y organiza los componentes en actividades, servicios y proveedores de contenido, con un modelo de permisos granular y ciclo de vida de aplicación gestionado por el propio sistema para optimizar batería y memoria. iOS, de Apple, se basa en un núcleo derivado de Unix (Darwin/XNU) y aplica un modelo de aislamiento estricto entre aplicaciones (sandboxing), distribución controlada mediante App Store y una gestión de memoria sin recolector de basura tradicional, basada en conteo automático de referencias (ARC). Ambos sistemas comparten características frente a los de escritorio: mayor restricción de recursos, gestión activa del consumo energético y modelos de permisos orientados a la privacidad del usuario.

## Tema 5. Sistemas de gestión de bases de datos relacionales, orientados a objetos y NoSQL: características y componentes.

### Concepto y componentes de un SGBD

Un sistema de gestión de bases de datos (SGBD) es el software que permite definir, crear, mantener y controlar el acceso a una base de datos. Sus componentes principales son el motor de almacenamiento, el procesador de consultas (parser, optimizador y ejecutor), el gestor de transacciones, el catálogo o diccionario de datos (metadatos) y los módulos de seguridad y control de concurrencia. Ofrece independencia entre los datos y las aplicaciones que los utilizan, evitando la redundancia y garantizando su integridad.

### Modelo relacional

Propuesto por E.F. Codd, organiza los datos en relaciones (tablas), formadas por tuplas (filas) y atributos (columnas), cada uno definido sobre un dominio de valores válidos. La integridad se garantiza mediante claves primarias (identificación única de cada tupla), claves ajenas (referencias entre tablas) y restricciones de dominio. El proceso de normalización, a través de las formas normales (1FN, 2FN, 3FN, entre otras), elimina redundancias y anomalías de actualización, inserción y borrado, descomponiendo las relaciones según las dependencias funcionales existentes entre atributos. El lenguaje estándar de manipulación y definición es SQL, con sentencias DDL (CREATE, ALTER), DML (SELECT, INSERT, UPDATE, DELETE) y DCL (GRANT, REVOKE).

### Propiedades ACID

Las transacciones en un SGBD relacional cumplen las propiedades ACID: Atomicidad (una transacción se ejecuta completa o no se ejecuta), Consistencia (las restricciones de integridad se mantienen antes y después), Aislamiento (las transacciones concurrentes no interfieren entre sí, con distintos niveles como read committed o serializable) y Durabilidad (los cambios confirmados persisten ante fallos, típicamente mediante un log de transacciones). Ejemplos de SGBD relacionales son Oracle, SQL Server, PostgreSQL y MySQL.

### Modelo orientado a objetos

Los SGBD orientados a objetos almacenan directamente objetos, con su estado (atributos) y comportamiento (métodos), soportando herencia, encapsulamiento y polimorfismo, evitando el desajuste de impedancia (impedance mismatch) que se produce al mapear objetos de un lenguaje de programación a tablas relacionales. Existe también el enfoque objeto-relacional, que extiende el modelo relacional con tipos de datos complejos, herencia de tablas y métodos almacenados, adoptado parcialmente por motores como PostgreSQL u Oracle.

### Bases de datos NoSQL

Surgen para dar respuesta a requisitos de escalabilidad horizontal, esquemas flexibles y grandes volúmenes de datos no necesariamente estructurados (Big Data), habitualmente relajando las garantías ACID a favor del modelo BASE (Basically Available, Soft state, Eventually consistent), que prioriza la disponibilidad y la consistencia eventual frente a la consistencia inmediata, conforme describe el teorema CAP (Consistencia, Disponibilidad y tolerancia a Particiones), según el cual un sistema distribuido solo puede garantizar plenamente dos de esas tres propiedades simultáneamente.

Se distinguen cuatro categorías principales:

**Clave-valor:** la estructura más simple, almacena pares identificador-valor sin esquema fijo, con acceso muy eficiente por clave (Redis, DynamoDB), habitual en caché y sesiones.

**Documentales:** almacenan documentos semiestructurados, típicamente en formato JSON o BSON, permitiendo estructuras anidadas y esquemas variables entre documentos de una misma colección (MongoDB, CouchDB).

**Orientadas a columnas (columnares):** organizan los datos por familias de columnas en lugar de por filas, optimizando la lectura de grandes volúmenes analíticos y la escalabilidad distribuida (Cassandra, HBase).

**De grafos:** modelan explícitamente entidades (nodos) y sus relaciones (aristas), optimizadas para consultas de recorrido y de relaciones complejas, como redes sociales o sistemas de recomendación (Neo4j).

### Consideraciones de selección

La elección entre modelo relacional y NoSQL depende de los requisitos del sistema: el modelo relacional resulta idóneo cuando se requiere integridad transaccional estricta y relaciones complejas bien definidas, mientras que las soluciones NoSQL se orientan a escenarios de alta escalabilidad horizontal, esquemas cambiantes o grandes volúmenes de datos semiestructurados, siendo frecuente en arquitecturas actuales la coexistencia de ambos paradigmas (polyglot persistence) según la naturaleza de cada componente del sistema de información.
