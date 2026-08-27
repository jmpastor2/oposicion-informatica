# TAI — Bloque II: ficha resumen + casos prácticos + test (20 preguntas)

## 1. Ficha resumen

### Tema 1. Informática básica y arquitectura de ordenadores
- Arquitectura **Von Neumann**: memoria única para datos e instrucciones (cuello de botella de Von Neumann) vs **Harvard**: buses y memorias separados para datos/instrucciones (típico en DSP y microcontroladores).
- CPU = **UC** (unidad de control, decodifica y secuencia) + **ALU** (aritmético-lógica) + **registros** (PC/IP, IR, MAR, MBR, acumulador).
- Ciclo de instrucción: **fetch → decode → execute → writeback** (captación, decodificación, ejecución, escritura de resultado).
- **CISC** (x86: muchas instrucciones complejas, microcódigo) vs **RISC** (ARM, MIPS, RISC-V: instrucciones simples, un ciclo, más registros, segmentación eficiente).
- Jerarquía de memoria (de más rápida/cara a más lenta/barata): **registros → caché L1 → L2 → L3 → RAM → SSD/HDD**. Localidad temporal y espacial justifica la caché.
- Memorias: **RAM** volátil (DRAM necesita refresco, SRAM no, más rápida y cara, usada en caché); **ROM/PROM/EPROM/EEPROM/Flash** no volátiles.
- Buses: **datos** (bidireccional), **direcciones** (unidireccional, determina memoria direccionable = 2^n), **control**. Buses de expansión: PCI → PCIe (por *lanes*, x1/x4/x8/x16).
- Representación: **complemento a 2** para enteros con signo; **IEEE 754** para coma flotante (simple: 1+8+23 bits; doble: 1+11+52 bits); **ASCII** (7 bits) vs **Unicode/UTF-8** (longitud variable, compatible con ASCII).
- Unidades: 1 KB = 1024 B (potencias de 2, JEDEC) vs 1 kB = 1000 B (SI); discos comerciales usan base 10, la RAM base 2 (de ahí la discrepancia de capacidad "real").

### Tema 2. Periféricos
- Clasificación: **entrada** (teclado, ratón, escáner, lector biométrico, código de barras), **salida** (monitor, impresora, altavoces), **entrada/salida** (pantalla táctil, módem, unidades de almacenamiento).
- Monitores: **LCD** (cristal líquido + retroiluminación), **LED** (LCD con retroiluminación LED), **OLED** (píxeles autoemisivos, negros puros, sin retroiluminación).
- Impresoras: **láser** (tambor fotosensible + tóner + fusor), **inyección de tinta** (cartuchos, cabezal), **matricial/de impacto** (agujas, tinta duplicada), **térmica** (tickets).
- **HDD**: platos magnéticos + cabezal, RPM (5400/7200/10000/15000), tiempo de acceso = búsqueda + latencia rotacional; **SSD**: memoria NAND Flash + controlador, sin partes móviles, menor latencia, TRIM para mantener rendimiento.
- Interfaces de almacenamiento: **SATA III** (6 Gbps), **SAS** (uso empresarial, full-duplex), **NVMe** (sobre PCIe, mucho mayor ancho de banda que SATA, cola de comandos masiva).
- **USB**: 2.0 (480 Mbps), 3.0/3.1 Gen1 (5 Gbps), 3.1 Gen2/3.2 Gen2 (10 Gbps), 3.2 Gen2x2 (20 Gbps), USB4 (hasta 40 Gbps, converge con Thunderbolt 3/4).
- Vídeo: **HDMI** (audio+vídeo, uso doméstico), **DisplayPort** (mayor ancho de banda, *multi-stream*), **Thunderbolt** (datos+vídeo+energía sobre USB-C).
- RAID (a caballo con almacenamiento): RAID 0 (*striping*, sin redundancia), RAID 1 (*mirroring*), RAID 5 (paridad distribuida, tolera 1 fallo), RAID 6 (doble paridad), RAID 10 (1+0).

### Tema 3. Tipos abstractos de datos, estructuras de datos y algoritmos
- **TAD**: define un tipo por su comportamiento (operaciones y propiedades), independiente de la implementación — separa especificación de representación interna.
- Lineales: **pila** (LIFO: push/pop), **cola** (FIFO: encolar/desencolar), **cola de prioridad** (heap), **lista enlazada** (simple, doble, circular; inserción O(1) vs array O(n)).
- No lineales: **árbol binario de búsqueda** (izq<nodo<der), **AVL/rojo-negro** (autobalanceados, altura O(log n) garantizada), **árboles B/B+** (SGBD e índices, multi-vía, minimizan accesos a disco), **grafos** (dirigidos/no dirigidos, listas o matrices de adyacencia).
- **Tablas hash**: acceso medio O(1) mediante función de dispersión; colisiones resueltas por encadenamiento o direccionamiento abierto.
- Notación asintótica: **O** (cota superior, peor caso), **Ω** (cota inferior, mejor caso), **Θ** (cota ajustada). Complejidades habituales: O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ).
- Ordenación simple O(n²): burbuja, inserción, selección. Ordenación eficiente O(n log n): **quicksort** (peor caso O(n²), pivote), **mergesort** (estable, O(n) en espacio), **heapsort** (in-place, O(1) espacio extra).
- Búsqueda: lineal O(n) sin requisitos; **binaria** O(log n) exige colección **ordenada**.
- Recursividad: caso base + caso recursivo; toda función recursiva es transformable a iterativa mediante pila explícita (relevante en TAD pila).

### Tema 4. Sistemas operativos
- Funciones del SO: gestión de **procesos**, **memoria**, **E/S** y **sistema de archivos**; provee la máquina virtual/abstracción sobre el hardware.
- Estructuras: **monolítico** (todo en espacio de núcleo, rápido pero acoplado — Linux), **microkernel** (mínimo en núcleo, servicios en espacio de usuario — Minix, QNX), **híbrido** (Windows NT, macOS/XNU).
- Proceso vs hilo: el proceso tiene espacio de memoria propio; los **hilos** comparten memoria del proceso (más ligeros, cambio de contexto más barato). Estados de proceso: **nuevo → listo → ejecución → bloqueado → terminado**.
- Planificación de CPU: **FCFS** (orden de llegada), **SJF** (trabajo más corto primero), **Round Robin** (*quantum* fijo, apropiativo, bueno para interactivos), por **prioridades** (riesgo de inanición, mitigado con *aging*).
- Gestión de memoria: **paginación** (bloques fijos, evita fragmentación externa pero genera interna), **segmentación** (bloques lógicos de tamaño variable), **memoria virtual** + *swap* (extiende RAM con disco vía tabla de páginas).
- Algoritmos de reemplazo de página: **FIFO**, **LRU** (menos usada recientemente), **óptimo** (teórico, referencia de comparación).
- Sistemas de archivos: **FAT32** (límite 4 GB/archivo, sin journaling), **NTFS** (Windows, ACL, journaling), **ext4** (Linux, journaling, extents), **exFAT** (extraíble, sin límite de tamaño de archivo).
- Concurrencia: **exclusión mutua**, **semáforos** (contador, `wait`/`signal`), **mutex** (binario), **interbloqueo (deadlock)** — 4 condiciones de Coffman: exclusión mutua, retención y espera, no apropiación, espera circular.

### Tema 5. SGBD relacionales y NoSQL
- Modelo relacional (Codd): **tabla/relación**, **tupla/fila**, **atributo/columna**; **clave primaria** (única, no nula) y **clave foránea** (integridad referencial).
- Álgebra relacional: selección (σ, filtra filas), proyección (π, filtra columnas), unión/intersección/diferencia, producto cartesiano, **join** (interno, externo izq/der/completo).
- Normalización: **1FN** (atómicos, sin repetición de grupos), **2FN** (sin dependencias parciales de la clave), **3FN** (sin dependencias transitivas), **FNBC** (Boyce-Codd, toda determinante es candidata).
- SQL por subtipo: **DDL** (CREATE/ALTER/DROP), **DML** (SELECT/INSERT/UPDATE/DELETE), **DCL** (GRANT/REVOKE), **TCL** (COMMIT/ROLLBACK/SAVEPOINT).
- **ACID**: Atomicidad (todo o nada), Consistencia (invariantes), Aislamiento (niveles: *read uncommitted, read committed, repeatable read, serializable*), Durabilidad (persiste tras commit).
- Índices: **B-tree/B+tree** (rango y orden, uso general), **hash** (igualdad exacta, O(1) medio, no sirve para rangos).
- NoSQL por modelo: **documental** (MongoDB, JSON/BSON), **clave-valor** (Redis, DynamoDB), **columnar/ancho de columna** (Cassandra, HBase, alta escritura), **grafos** (Neo4j, relaciones como ciudadanos de primera clase).
- **Teorema CAP**: en un sistema distribuido, ante partición de red solo se garantizan 2 de 3 (Consistencia, Disponibilidad, tolerancia a Partición); NoSQL suele priorizar **AP** con consistencia eventual (**BASE**: Basically Available, Soft state, Eventually consistent) frente al **ACID** relacional.

---

## 2. Casos prácticos resueltos

### Caso 1 — Diseño de estructura de datos
**Enunciado.** Diseña la estructura de datos más adecuada para implementar las funciones "Atrás" y "Adelante" del historial de navegación de un navegador web. Al visitar una página nueva tras haber pulsado "Atrás", debe descartarse el historial de "Adelante" acumulado.

**Solución.**
1. Identificar el patrón de acceso: solo se opera sobre el extremo más reciente (última página visitada / última deshecha) → acceso **LIFO**, no es necesario acceso aleatorio.
2. Usar **dos pilas**: `pilaAtras` (páginas visitadas antes de la actual) y `pilaAdelante` (páginas deshechas).
3. Operaciones:
   - `visitar(nuevaPagina)`: `push(pilaAtras, actual)`; `actual = nuevaPagina`; **vaciar `pilaAdelante`** (se pierde el "rehacer" al abrir una ruta nueva, igual que en un editor de texto).
   - `atras()`: `push(pilaAdelante, actual)`; `actual = pop(pilaAtras)`.
   - `adelante()`: `push(pilaAtras, actual)`; `actual = pop(pilaAdelante)`.
4. Complejidad: las tres operaciones son **O(1)** amortizado (push/pop de pila con array dinámico o lista enlazada).
5. Justificación frente a alternativas: una lista enlazada simple con puntero de "posición actual" también funciona, pero dos pilas modelan el comportamiento semántico (deshacer/rehacer) de forma más directa y es el patrón estándar usado en editores (undo/redo) y navegadores.

### Caso 2 — Cálculo de complejidad algorítmica
**Enunciado.** Calcula la complejidad temporal (notación O) del siguiente pseudocódigo, que busca pares de elementos iguales en una lista de `n` elementos:

```
para i desde 0 hasta n-1:
    para j desde i+1 hasta n-1:
        si lista[i] == lista[j]:
            imprimir "par encontrado"
```

**Solución.**
1. El bucle exterior ejecuta `n` iteraciones. Para cada valor de `i`, el bucle interior ejecuta `n-1-i` iteraciones.
2. Número total de comparaciones: (n-1) + (n-2) + ... + 1 + 0 = **n(n-1)/2**, que es una progresión aritmética.
3. n(n-1)/2 = (n² - n)/2 → el término dominante es n² → **complejidad O(n²)** (cuadrática).
4. Optimización: si el objetivo es solo detectar si existe algún par repetido (no todos los pares), se puede bajar a **O(n)** en tiempo (con **O(n)** en espacio) usando una tabla hash/conjunto: recorrer una vez, comprobando en O(1) medio si el elemento ya está en el conjunto antes de insertarlo. Alternativa intermedia: ordenar primero (O(n log n)) y comparar elementos adyacentes (O(n)), total O(n log n), sin espacio extra significativo.

### Caso 3 — SGBD relacional vs NoSQL
**Enunciado.** Un ayuntamiento debe implementar dos sistemas: (A) gestión del padrón de contribuyentes y liquidación/cobro de tributos, con relaciones complejas entre padrón, tributos, recibos y pagos, y necesidad de cuadrar cada céntimo; (B) recolección de lecturas de una red de sensores de calidad del aire distribuidos por la ciudad, que genera millones de registros diarios con un esquema que cambia según el modelo de sensor. Justifica el tipo de SGBD para cada caso.

**Solución.**
- **Caso A (padrón/tributación) → SGBD relacional** (p. ej. PostgreSQL/Oracle):
  - Requiere **ACID** estricto: una liquidación y su cobro deben ser atómicos y consistentes (no puede quedar un pago sin su recibo asociado).
  - El dominio es altamente **relacional**: contribuyente–inmueble–tributo–recibo–pago, con integridad referencial mediante claves foráneas.
  - Se necesitan consultas complejas con **joins** y agregaciones (cuadres contables, informes de recaudación) que el modelo relacional resuelve de forma natural y auditable.
  - El volumen de escritura es moderado, no justifica sacrificar consistencia.
- **Caso B (sensores IoT) → NoSQL** (columnar/orientado a series temporales, p. ej. Cassandra o InfluxDB):
  - Volumen de escritura muy alto y sostenido (millones de filas/día) → prioriza **escalabilidad horizontal**, que el modelo columnar resuelve mejor que un relacional monolítico.
  - **Esquema flexible**: cada modelo de sensor puede aportar campos distintos, sin necesidad de `ALTER TABLE` ni migraciones.
  - No se requiere ACID transaccional entre lecturas; basta **consistencia eventual (BASE)** — perder o retrasar la propagación de una lectura puntual no es crítico.
  - Según el teorema **CAP**, se prioriza **disponibilidad y tolerancia a particiones (AP)** frente a consistencia fuerte, adecuado para ingesta distribuida geográficamente.
  - Conclusión: **coexistencia poliglota** — no es una decisión excluyente; cada subsistema usa el modelo de datos alineado con sus requisitos (consistencia vs escala/flexibilidad).

### Caso 4 — Diagnóstico de fallo hardware
**Enunciado.** Un ordenador de sobremesa, al encenderlo, emite una serie de pitidos por el altavoz de la placa base, no muestra imagen en el monitor y no llega a arrancar el sistema operativo. Al abrir la caja, retirar y reinsertar uno de los módulos internos, el equipo arranca con normalidad, pero el fallo reaparece a los pocos días. ¿Qué componente es el más probable causante y cómo se diagnosticaría con precisión?

**Solución.**
1. **Descartar por fase de arranque**: el fallo ocurre durante la **POST** (Power-On Self-Test) de la BIOS/UEFI, antes de que se inicialice la salida de vídeo y antes de cargar el SO → el problema está en el hardware básico verificado por la POST (CPU, RAM, tarjeta gráfica), no en el software ni en el disco.
2. **Los pitidos son un código de error de la POST**: cada fabricante de BIOS (AMI, Award/Phoenix) codifica el componente fallido en un patrón de pitidos (p. ej. en AMI BIOS, un pitido largo repetido continuo suele indicar fallo de **memoria RAM**).
3. **El síntoma "reinsertar el módulo lo arregla temporalmente"** es característico de un **mal contacto en los conectores** — típico de módulos de RAM (oxidación de contactos dorados, asentamiento incompleto en el zócalo DIMM) más que de la CPU (soldada o con menos puntos de fallo por reinserción) o de la GPU (el síntoma sería ausencia de vídeo, pero normalmente sin impedir el arranque del SO).
4. **Diagnóstico preciso**:
   - Anotar el patrón exacto de pitidos y contrastarlo con la tabla de códigos del fabricante de la BIOS/placa.
   - Probar los módulos de RAM **de uno en uno** en distintos zócalos (aísla si el módulo o el zócalo son la causa).
   - Limpiar los contactos dorados con un paño/goma específica y reasentar firmemente.
   - Ejecutar **MemTest86** (arranque desde USB) durante varias pasadas para confirmar errores de bit persistentes.
   - Si el fallo persiste con el módulo aislado en varios zócalos → módulo de RAM defectuoso, sustituir. Si solo falla en un zócalo concreto → zócalo/placa base defectuosa.
5. **Conclusión**: componente más probable, **módulo de memoria RAM** (o su zócalo), diagnosticado por código de pitidos POST + prueba de aislamiento + MemTest86.

---

## 3. Test de autoevaluación

**1.** ¿Cuál es la representación en complemento a 2 de −5 en 8 bits?
a) 11111010
b) 11111011
c) 10000101
d) 11111100

**2.** En IEEE 754 de precisión simple (32 bits), ¿cuántos bits se destinan a la mantisa?
a) 8
b) 23
c) 24
d) 52

**3.** ¿Qué característica distingue a la arquitectura Harvard de la Von Neumann?
a) Usa buses separados para datos e instrucciones
b) Solo tiene una ALU
c) Utiliza microcódigo obligatoriamente
d) No permite memoria caché

**4.** ¿Cuál de las siguientes memorias es volátil?
a) ROM
b) EEPROM
c) DRAM
d) Flash NAND

**5.** ¿Qué tecnología de almacenamiento no tiene partes mecánicas móviles?
a) HDD
b) SSD
c) Unidad de cinta (LTO)
d) Disquete

**6.** ¿Cuál es la velocidad máxima teórica de USB 3.2 Gen 2x2?
a) 5 Gbps
b) 10 Gbps
c) 20 Gbps
d) 40 Gbps

**7.** ¿Qué tipo de impresora utiliza un tambor fotosensible y tóner?
a) Inyección de tinta
b) Láser
c) Matricial
d) Térmica directa

**8.** Interfaz de almacenamiento diseñada específicamente para aprovechar unidades SSD conectadas por PCIe:
a) SATA III
b) SAS
c) NVMe
d) IDE

**9.** ¿Qué estructura de datos sigue la política FIFO (First In First Out)?
a) Pila
b) Cola
c) Árbol binario
d) Lista doblemente enlazada

**10.** La complejidad temporal en el peor caso del algoritmo Quicksort es:
a) O(n log n)
b) O(n)
c) O(n²)
d) O(log n)

**11.** Para poder aplicar búsqueda binaria sobre un array, este debe estar:
a) Indexado desde 0
b) Ordenado
c) Implementado como lista enlazada
d) De tamaño par

**12.** ¿Qué estructura garantiza que un árbol binario de búsqueda mantenga una altura O(log n) tras inserciones y borrados?
a) Árbol binario simple
b) Árbol AVL (autobalanceado)
c) Lista enlazada circular
d) Montículo binario desordenado

**13.** ¿Cuál de las siguientes NO es una de las cuatro condiciones de Coffman necesarias para que se produzca un interbloqueo?
a) Exclusión mutua
b) Retención y espera
c) Apropiación (preemption)
d) Espera circular

**14.** El algoritmo de sustitución de páginas que reemplaza la página que lleva más tiempo sin usarse se llama:
a) FIFO
b) Óptimo
c) LRU
d) Round Robin

**15.** ¿Qué técnica de gestión de memoria divide la memoria física en bloques de tamaño fijo?
a) Segmentación
b) Paginación
c) Particionamiento dinámico
d) Fragmentación externa

**16.** En Linux, ¿qué sistema de archivos con journaling es el sucesor directo de ext3 y el más usado por defecto en muchas distribuciones?
a) XFS
b) Btrfs
c) ext4
d) ReiserFS

**17.** Según el teorema CAP, un sistema distribuido no puede garantizar simultáneamente más de dos de estas tres propiedades:
a) Atomicidad, Consistencia, Aislamiento
b) Consistencia, Disponibilidad, Tolerancia a particiones
c) Durabilidad, Disponibilidad, Aislamiento
d) Atomicidad, Durabilidad, Consistencia

**18.** ¿Qué forma normal exige que no existan dependencias transitivas entre atributos no clave?
a) Primera forma normal (1FN)
b) Segunda forma normal (2FN)
c) Tercera forma normal (3FN)
d) Forma normal de Boyce-Codd (FNBC)

**19.** ¿Cuál de las siguientes bases de datos NoSQL es del tipo "clave-valor"?
a) MongoDB
b) Redis
c) Cassandra
d) Neo4j

**20.** La propiedad ACID que garantiza que, tras confirmarse (commit) una transacción, sus cambios persistan incluso ante un fallo del sistema, es:
a) Atomicidad
b) Consistencia
c) Aislamiento
d) Durabilidad

### Soluciones

1. **b)** 5 = 00000101; invertir bits → 11111010; sumar 1 → 11111011.
2. **b)** Precisión simple: 1 bit de signo + 8 de exponente + 23 de mantisa = 32 bits.
3. **a)** Harvard separa físicamente los buses/memorias de datos e instrucciones; Von Neumann los comparte.
4. **c)** DRAM pierde su contenido sin alimentación y necesita refresco constante; ROM/EEPROM/Flash son no volátiles.
5. **b)** El SSD usa memoria NAND Flash de estado sólido, sin cabezales ni platos mecánicos.
6. **c)** USB 3.2 Gen 2x2 alcanza 20 Gbps (dos líneas de 10 Gbps en paralelo).
7. **b)** La láser usa un tambor fotosensible cargado electrostáticamente que atrae el tóner, fijado después por el fusor.
8. **c)** NVMe se diseñó para explotar el paralelismo y baja latencia de las SSD sobre el bus PCIe, superando el límite de SATA III.
9. **b)** La cola atiende en el mismo orden de llegada (FIFO); la pila es LIFO.
10. **c)** El peor caso de Quicksort (pivote siempre mal elegido, p. ej. lista ya ordenada con pivote extremo) degenera a O(n²); el caso promedio es O(n log n).
11. **b)** La búsqueda binaria descarta mitades del espacio comparando con el elemento central, lo que solo es válido si la colección está ordenada.
12. **b)** El AVL rebalancea tras cada inserción/borrado mediante rotaciones, manteniendo la propiedad de altura logarítmica; un ABB simple puede degenerar en una lista O(n).
13. **c)** La condición real de Coffman es "no apropiación" (no preemption): un recurso no puede ser arrebatado a un proceso, no lo contrario.
14. **c)** LRU (Least Recently Used) sustituye la página con mayor tiempo sin ser referenciada.
15. **b)** La paginación usa marcos/páginas de tamaño fijo; la segmentación usa bloques lógicos de tamaño variable.
16. **c)** ext4 es la evolución directa de ext2/ext3 con journaling, extents y mayor rendimiento, y sigue siendo el predeterminado en numerosas distribuciones.
17. **b)** CAP = Consistency, Availability, Partition tolerance; ante una partición de red solo se pueden garantizar dos de las tres.
18. **c)** La 3FN elimina dependencias transitivas (atributo no clave que depende de otro atributo no clave, no directamente de la clave).
19. **b)** Redis es la base de datos clave-valor en memoria por excelencia; MongoDB es documental, Cassandra columnar, Neo4j de grafos.
20. **d)** La durabilidad garantiza persistencia permanente de los cambios confirmados, típicamente mediante escritura en el log de transacciones antes del commit (write-ahead logging).
