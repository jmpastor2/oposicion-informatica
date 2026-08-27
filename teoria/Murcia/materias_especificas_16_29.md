# Murcia (CARM) — Materias específicas, Opción Informática (Temas 16-29)

## Tema 16. Gestión de servicios de TI. ISO/IEC 20000. Conceptos. Procesos de control, entrega y soporte de servicios TI.

ISO/IEC 20000 es la norma internacional de gestión de servicios de TI (SMS, Service Management System), publicada originalmente en 2005 a partir de las mejores prácticas de ITIL v2, y revisada en 2011 y 2018 (ISO/IEC 20000-1:2018) para alinearse con la estructura de alto nivel (Anexo SL) común a ISO 9001, ISO 27001 e ISO 22301. Se compone de varias partes: **ISO/IEC 20000-1** (requisitos, la única certificable), **20000-2** (código de buenas prácticas), **20000-3** (guía de aplicabilidad y alcance), **20000-5** (guía de implantación exemplar) y **20000-10** (conceptos y terminología).

**Conceptos clave.** Un servicio de TI aporta valor al cliente facilitando resultados sin que este asuma costes ni riesgos específicos de los recursos empleados. El SMS integra política, objetivos, planes, procesos, documentación y recursos necesarios para diseñar, transicionar, entregar y mejorar servicios cumpliendo los requisitos del cliente. La norma se estructura sobre el ciclo **PHVA (Plan-Do-Check-Act)** de Deming, aplicado tanto al SMS global como a cada proceso individual.

**Estructura de la norma (edición 2018).** Consta de 10 cláusulas: 1-3 introductorias, 4 (contexto de la organización), 5 (liderazgo), 6 (planificación), 7 (soporte: recursos, competencia, concienciación, comunicación, documentación), 8 (operación de servicios, el bloque más extenso), 9 (evaluación del desempeño) y 10 (mejora).

**Procesos de control**, agrupados dentro de la cláusula de operación:
- **Gestión de la configuración**: mantiene una CMDB (Configuration Management Database) con los CI (Configuration Items) y sus relaciones, controlando integridad y trazabilidad.
- **Gestión de cambios**: evalúa, aprueba (mediante un CAB, Change Advisory Board), implementa y revisa cambios en los servicios minimizando el impacto adverso, distinguiendo cambios estándar, normales y de emergencia.

**Procesos de entrega (Service Delivery)**:
- **Gestión del nivel de servicio (SLM)**: negocia, documenta y monitoriza SLA (Service Level Agreements) con clientes, y OLA (Operational Level Agreements) internos, con indicadores como disponibilidad (%), tiempo medio de reparación (MTTR) y tiempo medio entre fallos (MTBF).
- **Gestión de la capacidad**: garantiza recursos suficientes con coste eficiente, mediante planes de capacidad y modelado de tendencias.
- **Gestión de la continuidad y disponibilidad del servicio (SCDM)**: BIA (Business Impact Analysis), RTO (Recovery Time Objective) y RPO (Recovery Point Objective).
- **Gestión financiera de servicios**: presupuestación, contabilidad y facturación de TI (chargeback).
- **Gestión de la seguridad de la información**: controles alineados con ISO/IEC 27001, gestión de incidentes de seguridad diferenciados de incidentes de servicio.
- **Gestión de relaciones de negocio y de proveedores (SUPPM)**: contratos, UC (Underpinning Contracts) con terceros.

**Procesos de soporte (Service Support)**:
- **Gestión de incidentes**: restaurar el servicio lo antes posible; clasificación por prioridad = impacto × urgencia; workaround como solución temporal.
- **Gestión de peticiones de servicio**: canaliza solicitudes estándar (altas de usuario, permisos) normalmente vía catálogo de servicios.
- **Gestión de problemas**: análisis de causa raíz (RCA) para evitar recurrencia de incidentes; genera KEDB (Known Error Database).
- **Gestión de despliegue y entrega (Release Management)**: paso a producción controlado de nuevas versiones, con entornos DEV/TEST/PRE/PRO diferenciados.

**Certificación.** La otorgan organismos acreditados (en España, AENOR) tras una auditoría de tercera parte que valida que el SMS cumple los requisitos "SHALL" de la cláusula 4-10. La certificación tiene alcance definido (qué servicios, qué ubicaciones) y vigencia trienal con auditorías de seguimiento anuales.

**Diferencia con ITIL**: ITIL es un marco de buenas prácticas no certificable por organizaciones (solo las personas se certifican, ITIL Foundation/Practitioner/Managing Professional); ISO/IEC 20000 es una norma certificable que puede implementarse apoyándose en procesos ITIL como referencia práctica, pero define *qué* debe cumplirse, no *cómo*.

**Ejemplo de métrica de SLA en un informe mensual:**
```
Servicio: ERP-Producción
Disponibilidad comprometida: 99,5%
Disponibilidad real: 99,72%
Incidentes prioridad 1: 2 (SLA cumplido en ambos, resolución < 4h)
MTTR medio: 2h 15min
```

En la Administración Pública, la adopción de ISO/IEC 20000 suele vincularse a pliegos de contratación de servicios TIC externalizados, exigiendo certificación al proveedor como garantía de madurez del proceso.

## Tema 17. Gestión de servicios de TI. ITIL: Conceptos. Ciclo de vida del servicio. Transición, operación y mejora continua del servicio.

ITIL (Information Technology Infrastructure Library) es el marco de referencia de gestión de servicios de TI más extendido, desarrollado originalmente por la CCTA británica (hoy AXELOS, y desde 2021 propiedad de PeopleCert). Existen varias versiones: ITIL v2 (procesos agrupados en Service Support y Service Delivery), **ITIL v3/2011** (ciclo de vida del servicio en 5 fases, la base tradicional del temario de oposición) e **ITIL 4** (2019), que introduce el Sistema de Valor del Servicio (SVS) y las 34 prácticas.

**Conceptos fundamentales (ITIL v3).** Servicio: medio de entregar valor mediante la facilitación de resultados sin que el cliente asuma costes ni riesgos específicos. Valor = utilidad (fit for purpose, "¿qué hace?") + garantía (fit for use, "¿cómo se entrega?": disponibilidad, capacidad, continuidad, seguridad). Los 4 elementos que componen un servicio siguen el modelo de las 4 P: Personas, Procesos, Productos (tecnología) y Partners (proveedores/socios).

**El ciclo de vida del servicio** se articula en 5 fases, cada una con procesos y funciones propios:

**1. Estrategia del servicio (Service Strategy).** Define qué servicios ofrecer y a quién. Procesos: gestión de la estrategia, gestión del portfolio de servicios (pipeline, catálogo, servicios retirados), gestión financiera, gestión de la demanda (PBA, Patterns of Business Activity) y gestión de relaciones de negocio.

**2. Diseño del servicio (Service Design).** Diseña servicios nuevos o modificados y sus procesos de soporte. Procesos: gestión del catálogo de servicios, gestión del nivel de servicio (SLA/OLA/UC), gestión de la disponibilidad, gestión de la capacidad, gestión de la continuidad del servicio TI (ITSCM), gestión de la seguridad de la información, gestión de proveedores. Entregable clave: el paquete de diseño del servicio (SDP).

**3. Transición del servicio (Service Transition).** Introduce cambios en producción de forma controlada, gestionando el riesgo. Procesos principales:
- **Gestión de cambios**: evalúa mediante el CAB tipos de cambio (estándar, normal, emergencia — usando ECAB), con los "7 R" para valorar una RFC (Request for Change): quién lo solicita, razón, resultado esperado, riesgos, recursos necesarios, responsables de construcción/prueba/implementación, y relación con otros cambios.
- **Gestión de la configuración y activos del servicio (SACM)**: CMDB/CMS (Configuration Management System) con CI y sus relaciones.
- **Gestión de entregas y despliegues (Release and Deployment)**: unidades de entrega (release units), opciones de despliegue big bang vs. fases.
- **Validación y pruebas del servicio**: modelo en V, entornos de prueba.
- **Evaluación del cambio** y **gestión del conocimiento** (SKMS, Service Knowledge Management System).

**4. Operación del servicio (Service Operation).** Fase de ejecución diaria, donde se entrega y soporta el valor. Procesos:
- **Gestión de eventos**: monitorización, clasificación (informativo, advertencia, excepción).
- **Gestión de incidentes**: restauración rápida del servicio; prioridad = impacto × urgencia; escalado funcional (a especialistas) vs. jerárquico (a gestión).
- **Cumplimiento de peticiones**: vía catálogo de servicios.
- **Gestión de problemas**: reactiva (tras incidentes) y proactiva (análisis de tendencias); RCA con técnicas como los 5 porqués o Ishikawa; genera errores conocidos (KEDB) y workarounds.
- **Gestión de accesos**: provisión de derechos según políticas de seguridad.
Funciones: **Service Desk** (único punto de contacto, SPOC), gestión técnica, gestión de operaciones TI, gestión de aplicaciones.

**5. Mejora continua del servicio (CSI, Continual Service Improvement).** Transversal a todo el ciclo, basada en el ciclo PHVA. Modelo CSI en 7 pasos: identificar la estrategia de mejora → definir qué se medirá → recopilar datos → procesarlos → analizarlos → presentarlos y usarlos → implementar la mejora. Utiliza el **enfoque de las 7 R** y el **Registro de Mejoras del Servicio (SIP, CSI Register)**. Métricas: KPI, factores críticos de éxito (CSF) y métricas de tecnología/proceso/servicio.

**ITIL 4** sustituye el ciclo de vida por el SVS, con la **cadena de valor del servicio** (Plan, Improve, Engage, Design & Transition, Obtain/Build, Deliver & Support) y añade prácticas nuevas como gestión de relaciones o gestión de riesgos, manteniendo compatibilidad conceptual con v3.

## Tema 18. Gestión de proyectos. PRINCE2.

PRINCE2 (PRojects IN Controlled Environments) es un método de gestión de proyectos desarrollado por la CCTA británica en 1996 y hoy gestionado por AXELOS/PeopleCert. Es un método estructurado, basado en procesos, orientado a producto y aplicable a cualquier tipo de proyecto independientemente del sector. La última edición relevante es PRINCE2 6th Edition (2017) y PRINCE2 7 (2023).

**Los 7 principios** (obligatorios, no adaptables):
1. Justificación comercial continua (Business Case vivo durante todo el proyecto).
2. Aprender de la experiencia (lecciones aprendidas al inicio, durante y al cierre).
3. Roles y responsabilidades definidos.
4. Gestión por fases (Stages), con puntos de decisión (Stage Boundaries).
5. Gestión por excepción: cada nivel de dirección delega tolerancias (tiempo, coste, calidad, alcance, riesgo, beneficios) al nivel inferior; solo se escala si se superan.
6. Enfoque en los productos (Product-Based Planning), no en las actividades.
7. Adaptación al entorno del proyecto (tailoring).

**Los 7 temas** (aspectos que deben gestionarse continuamente): Business Case, Organización, Calidad, Planes, Riesgo, Cambio (control de configuración e incidencias) y Progreso (control de avance mediante tolerancias).

**Estructura organizativa (los 4 niveles):**
- **Junta de Proyecto (Project Board)**: máxima autoridad, formada por Ejecutivo (Executive, representa el negocio y toma decisiones finales), Usuario Senior (representa a quienes usarán el producto) y Proveedor Senior (representa a quienes lo construyen).
- **Gestión (Project Manager)**: gestión diaria del proyecto.
- **Entrega (Team Manager)**: gestión de equipos de trabajo especializados.
- **Dirección corporativa/de programa**: por encima de la Junta, encarga el proyecto (Project Mandate).
Roles de apoyo: Project Assurance (auditoría independiente) y Project Support (asistencia administrativa, gestión de configuración).

**Los 7 procesos:**
1. **SU – Puesta en marcha (Starting Up a Project)**: valida la idea, nombra al Ejecutivo y PM, elabora el Project Brief.
2. **IP – Iniciación (Initiating a Project)**: produce el **Documento de Inicio del Proyecto (PID)**, con Business Case detallado, plan de proyecto, estrategias (calidad, riesgos, comunicación, configuración).
3. **DP – Dirección (Directing a Project)**: la Junta autoriza inicio, fases y cierre; gestiona por excepción.
4. **CS – Control de una fase (Controlling a Stage)**: asignación de paquetes de trabajo (Work Packages), seguimiento de progreso, gestión de incidencias (Issues) mediante el registro de incidencias.
5. **MP – Gestión de la entrega de producto (Managing Product Delivery)**: el Team Manager ejecuta y reporta sobre los Work Packages (Checkpoint Reports).
6. **SB – Gestión de los límites de fase (Managing a Stage Boundary)**: reporta a la Junta al final de cada fase (End Stage Report) y planifica la siguiente.
7. **CP – Cierre de proyecto (Closing a Project)**: entrega productos, lecciones aprendidas, plan de revisión de beneficios post-proyecto.

**Los 26 productos de gestión** documentan el método; los más relevantes: Business Case, PID, Plan de Proyecto/Fase/Equipo, Registro de Riesgos, Registro de Incidencias (Issue Register), Registro de Calidad, Registro de Lecciones, Informe de Progreso (Highlight Report), Informe de Excepción (Exception Report) y Registro de Configuración.

**Planificación basada en productos:** se elabora una Estructura de Descomposición de Productos (PBS), Descripciones de Producto (con criterios de calidad y método de verificación), un diagrama de secuencia de productos y finalmente el plan de actividades derivado.

**PRINCE2 Agile** combina el marco con prácticas ágiles (Scrum, Kanban), manteniendo la gobernanza PRINCE2 (Business Case, tolerancias, roles) mientras el equipo de entrega trabaja en sprints, útil cuando la Administración exige control formal de contratos pero el desarrollo se organiza de forma ágil.

**Certificaciones:** Foundation (conceptos) y Practitioner (aplicación adaptativa a un contexto real, examen basado en escenario).

## Tema 19. Gestión de proyectos con metodologías ágiles. Scrum.

Las metodologías ágiles surgen formalmente con el **Manifiesto Ágil (2001)**, firmado por 17 desarrolladores, que establece 4 valores: individuos e interacciones sobre procesos y herramientas; software funcionando sobre documentación exhaustiva; colaboración con el cliente sobre negociación contractual; respuesta al cambio sobre seguimiento de un plan. Se apoya en 12 principios (entrega temprana y continua, aceptar cambios incluso tardíos, entregas frecuentes, colaboración diaria negocio-desarrollo, equipos motivados y autoorganizados, comunicación cara a cara, software funcionando como medida de progreso, ritmo sostenible, excelencia técnica, simplicidad, retrospectivas regulares).

**Scrum** (Schwaber y Sutherland) es el framework ágil más adoptado, definido formalmente en la **Guía Scrum** (última revisión 2020). No es una metodología prescriptiva completa sino un marco ligero basado en control de procesos empírico: transparencia, inspección y adaptación.

**Roles (2020: los "3 responsabilidades" del Scrum Team, equipo único auto-gestionado ≤10 personas):**
- **Product Owner (PO)**: maximiza el valor del producto, gestiona y prioriza el **Product Backlog**, único responsable de definir qué se construye.
- **Scrum Master**: garante del marco Scrum, elimina impedimentos, facilita eventos, sirve tanto al equipo como a la organización (coaching).
- **Developers**: equipo multidisciplinar que construye el Incremento cada Sprint.

**Artefactos y sus compromisos (commitments):**
- **Product Backlog** (compromiso: **Product Goal**): lista ordenada y viva de todo lo pendiente (historias de usuario, bugs, deuda técnica), refinada continuamente (Backlog Refinement).
- **Sprint Backlog** (compromiso: **Sprint Goal**): elementos seleccionados para el Sprint más el plan para entregarlos.
- **Incremento** (compromiso: **Definición de Terminado, DoD**): suma de todos los elementos completados, debe ser utilizable e inspeccionable.

**Eventos, dentro de un Sprint (bloque de tiempo fijo, típicamente 2-4 semanas):**
1. **Sprint Planning** (máx. 8h para sprint de 1 mes): responde qué se hará (selección de Product Backlog Items) y cómo (descomposición en tareas), fijando el Sprint Goal.
2. **Daily Scrum** (15 min diarios): sincronización del equipo, inspección de progreso hacia el Sprint Goal.
3. **Sprint Review**: inspección del Incremento con stakeholders, retroalimentación que alimenta el Product Backlog.
4. **Sprint Retrospective**: el equipo identifica mejoras de proceso, personas, herramientas para el siguiente Sprint.

**Historias de usuario**, técnica habitual (no formalmente parte de Scrum) para expresar el backlog: formato *"Como [rol], quiero [funcionalidad] para [beneficio]"*, con criterios INVEST (Independiente, Negociable, Valiosa, Estimable, Small/pequeña, Testeable) y criterios de aceptación tipo Gherkin (Given/When/Then).

**Estimación:** puntos de historia (Story Points, escala Fibonacci: 1,2,3,5,8,13...) mediante Planning Poker, midiendo esfuerzo/complejidad relativa, no tiempo absoluto. La **velocidad** (puntos completados por sprint) permite proyectar entregas.

**Ejemplo de tablero Kanban de sprint:**
```
To Do          | In Progress    | In Review   | Done
---------------|----------------|-------------|-------
US-102 (5pts)  | US-098 (3pts)  | US-095 (2pts)| US-090
US-103 (3pts)  |                |             | US-091
```

**Otros frameworks ágiles relacionados:** Kanban (flujo continuo, WIP limits, sin sprints), XP/Extreme Programming (TDD, pair programming, integración continua), Lean, y a escala **SAFe** (Scaled Agile Framework) o **LeSS**, relevantes cuando varios equipos Scrum coordinan un mismo producto grande, algo habitual en proyectos TIC de gran envergadura en la Administración.

**Diferencias clave frente a metodologías predictivas (cascada):** planificación adaptativa e iterativa frente a planificación exhaustiva inicial; entregas incrementales frecuentes frente a entrega única al final; el alcance es la variable flexible (frente a tiempo/coste fijos), mientras tiempo y coste tienden a fijarse por el timebox del Sprint.

## Tema 20. Programación orientada a objetos (clases, objetos, herencia, métodos). Lenguaje Unificado de Modelado (UML).

**Programación orientada a objetos (POO).** Paradigma que organiza el software en torno a objetos, instancias de clases que encapsulan estado (atributos) y comportamiento (métodos). Los 4 pilares son:

**1. Encapsulación**: oculta el estado interno tras una interfaz pública, controlando el acceso mediante modificadores de visibilidad (`private`, `protected`, `public`, `package/default`).

```java
public class CuentaBancaria {
    private double saldo; // oculto al exterior
    public void ingresar(double importe) {
        if (importe > 0) this.saldo += importe;
    }
    public double getSaldo() { return saldo; }
}
```

**2. Herencia**: una clase (subclase) reutiliza y extiende atributos/métodos de otra (superclase), modelando relaciones "es-un".

```java
public class CuentaAhorro extends CuentaBancaria {
    private double tipoInteres;
    public void aplicarInteres() {
        ingresar(getSaldo() * tipoInteres); // reutiliza método heredado
    }
}
```

**3. Polimorfismo**: un mismo mensaje produce comportamientos distintos según el objeto receptor. Polimorfismo de sobreescritura (*overriding*, en tiempo de ejecución mediante enlace dinámico) frente a sobrecarga (*overloading*, en tiempo de compilación).

```java
class Figura { double area() { return 0; } }
class Circulo extends Figura {
    double radio;
    @Override double area() { return Math.PI * radio * radio; }
}
```

**4. Abstracción**: modelar solo los aspectos relevantes del dominio, mediante clases abstractas (`abstract class`, pueden tener implementación parcial) e interfaces (contrato puro, en Java desde v8 con métodos `default`).

**Otros conceptos**: composición vs. herencia ("favorecer composición sobre herencia" — principio de diseño para evitar jerarquías rígidas); clases y métodos `static` (pertenecen a la clase, no a la instancia); constructores y sobrecarga de constructores; principio SOLID (Responsabilidad Única, Abierto/Cerrado, Sustitución de Liskov, Segregación de Interfaces, Inversión de Dependencias), base del diseño orientado a objetos de calidad.

**UML (Unified Modeling Language).** Lenguaje gráfico estándar (gestionado por OMG, Object Management Group) para especificar, visualizar, construir y documentar sistemas software. No es un método sino una notación. Versión de referencia: UML 2.5.

**Diagramas estructurales:**
- **Clases**: el más usado, representa clases con 3 compartimentos (nombre, atributos, métodos) y relaciones — asociación (línea simple, con multiplicidad 1, 0..1, *, 1..*), agregación (rombo hueco, "tiene un", ciclo de vida independiente), composición (rombo relleno, ciclo de vida dependiente), generalización/herencia (flecha triangular hueca), dependencia (línea discontinua) y realización de interfaz (línea discontinua con triángulo).
- **Objetos**: instantánea de instancias concretas en un momento dado.
- **Componentes** y **Despliegue** (nodos físicos, servidores, dispositivos y su interconexión).
- **Paquetes**: agrupación lógica de elementos.

**Diagramas de comportamiento:**
- **Casos de uso**: actores (externos al sistema) y casos de uso (funcionalidades), con relaciones `<<include>>` (obligatoria) y `<<extend>>` (opcional/condicional).
- **Secuencia**: interacción entre objetos ordenada temporalmente (eje vertical = tiempo), con líneas de vida, mensajes síncronos/asíncronos y fragmentos combinados (`alt`, `loop`, `opt`).
- **Actividades**: flujo de control/datos, similar a diagramas de flujo pero con carriles (swimlanes), bifurcaciones y uniones.
- **Estados (máquina de estados)**: estados, transiciones, eventos y guardas de un objeto a lo largo de su ciclo de vida.
- **Comunicación**, **Temporización** y **Vista general de interacción**, menos usados en la práctica.

**Ejemplo textual de relación en diagrama de clases:**
```
Cliente "1" --- "0..*" Pedido : realiza
Pedido *-- LineaPedido : contiene (composición)
Empleado ..|> IAutenticable : implementa
```

UML se emplea típicamente en fases de análisis y diseño (metodologías como el Proceso Unificado, RUP) y sigue siendo referencia en documentación de arquitectura de sistemas de información en proyectos públicos, aunque en desarrollo ágil su uso se simplifica a diagramas puntuales de apoyo (whiteboard UML) en lugar de especificación exhaustiva.

## Tema 21. Oracle. Objetos del esquema: tablas, vistas, secuencias, sinónimos, índices, paquetes, procedimientos, funciones, triggers, etcétera. Dependencias entre objetos. El diccionario de datos. Tipos de datos e integridad.

Un **esquema** en Oracle es la colección de objetos de base de datos asociados a un usuario, que comparten el mismo namespace.

**Objetos del esquema:**
- **Tablas**: estructura básica de almacenamiento en filas y columnas. Pueden ser tablas normales, particionadas (`PARTITION BY RANGE/LIST/HASH`), organizadas por índice (IOT) o temporales (`GLOBAL TEMPORARY`).
- **Vistas**: consultas almacenadas que presentan datos de una o varias tablas; pueden ser actualizables si cumplen ciertas condiciones (`CREATE OR REPLACE VIEW`). Las vistas materializadas (`CREATE MATERIALIZED VIEW`) almacenan físicamente el resultado y se refrescan (`ON COMMIT` o `ON DEMAND`), útiles en data warehousing.
- **Secuencias**: generadores de números únicos, típicamente para claves primarias: `CREATE SEQUENCE seq_pedido START WITH 1 INCREMENT BY 1 NOCACHE;` — se invocan con `seq_pedido.NEXTVAL` y `.CURRVAL`.
- **Sinónimos**: alias de otros objetos, privados o públicos (`CREATE PUBLIC SYNONYM emp_syn FOR hr.empleados;`), facilitan la transparencia de ubicación (útil junto a `DBLINK` para acceso remoto).
- **Índices**: estructuras para acelerar accesos. B-tree (por defecto), bitmap (baja cardinalidad, DW), únicos, compuestos, basados en función (`CREATE INDEX idx_upper ON empleados(UPPER(apellido));`).
- **Paquetes (packages)**: agrupan procedimientos, funciones, variables, cursores y tipos relacionados, con especificación (interfaz pública) y cuerpo (implementación, puede ocultar lógica privada).
- **Procedimientos y funciones**: subprogramas PL/SQL almacenados; la función siempre retorna un valor (`RETURN`) y puede usarse en expresiones SQL; el procedimiento no retorna valor por `RETURN` pero puede usar parámetros `OUT`/`IN OUT`.
- **Triggers**: código que se ejecuta automáticamente ante eventos DML (`INSERT`/`UPDATE`/`DELETE`), DDL o del sistema (`LOGON`, `SERVERERROR`). Pueden ser `BEFORE`/`AFTER`, a nivel de fila (`FOR EACH ROW`) o de sentencia.
- Otros: **tipos de objeto** (UDT, `CREATE TYPE`), **clusters** (agrupan físicamente tablas relacionadas), **dimensiones** (metadatos jerárquicos para OLAP), **enlaces de base de datos (DB LINK)**.

**Ejemplo de trigger de auditoría:**
```sql
CREATE OR REPLACE TRIGGER trg_aud_salario
BEFORE UPDATE OF salario ON empleados
FOR EACH ROW
BEGIN
  INSERT INTO aud_salarios(id_emp, salario_ant, salario_nue, fecha)
  VALUES (:OLD.id_emp, :OLD.salario, :NEW.salario, SYSDATE);
END;
/
```

**Dependencias entre objetos.** Oracle mantiene un grafo de dependencias (visible en `USER_DEPENDENCIES`) entre objetos que referencian a otros: una vista depende de sus tablas base, un procedimiento de los objetos que invoca. Si un objeto base cambia de estructura, los dependientes pueden quedar `INVALID` y se recompilan automáticamente en el siguiente acceso (recompilación diferida) o manualmente con `ALTER ... COMPILE`. La vista `USER_OBJECTS` muestra el `STATUS` (VALID/INVALID) de cada objeto.

**El diccionario de datos.** Conjunto de tablas y vistas de solo lectura, propiedad del usuario `SYS`, que almacena metadatos de toda la base de datos. Tres niveles de vistas según ámbito: `USER_*` (objetos propios del usuario conectado), `ALL_*` (objetos propios más aquellos sobre los que se tiene privilegio), `DBA_*` (todos los objetos de la BD, requiere privilegio DBA). Ejemplos: `USER_TABLES`, `USER_TAB_COLUMNS`, `USER_CONSTRAINTS`, `USER_INDEXES`, `DBA_USERS`, `DBA_ROLE_PRIVS`. También existen las vistas dinámicas de rendimiento `V$` (p. ej. `V$SESSION`, `V$SQL`), que reflejan el estado en memoria de la instancia.

**Tipos de datos**: `VARCHAR2`/`CHAR` (texto), `NUMBER(p,s)` (precisión/escala), `DATE` (con hora, segundos), `TIMESTAMP` (con fracciones de segundo y zona horaria mediante `TIMESTAMP WITH TIME ZONE`), `CLOB`/`BLOB`/`NCLOB` (objetos grandes), `RAW`, `ROWID`.

**Integridad de datos**, mediante restricciones (`CONSTRAINT`):
```sql
CREATE TABLE pedidos (
  id_pedido   NUMBER PRIMARY KEY,
  id_cliente  NUMBER NOT NULL REFERENCES clientes(id_cliente),
  estado      VARCHAR2(10) CHECK (estado IN ('PEND','ENV','ENT')),
  importe     NUMBER(10,2) DEFAULT 0
);
```
Tipos: `PRIMARY KEY`, `FOREIGN KEY` (con `ON DELETE CASCADE`/`SET NULL`), `UNIQUE`, `CHECK`, `NOT NULL`. Pueden definirse `DEFERRABLE` para comprobarse al `COMMIT` en lugar de en cada sentencia, útil en cargas masivas con dependencias circulares.

## Tema 22. Oracle. Lenguajes de programación SQL y PL/SQL.

**SQL en Oracle.** Lenguaje declarativo estándar (ISO/ANSI, con extensiones propietarias) dividido en subconjuntos: **DDL** (`CREATE`, `ALTER`, `DROP`, `TRUNCATE`), **DML** (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `MERGE`), **DCL** (`GRANT`, `REVOKE`) y **TCL** (`COMMIT`, `ROLLBACK`, `SAVEPOINT`).

**Particularidades de Oracle SQL**: `DUAL` (tabla ficticia de una fila para evaluar expresiones: `SELECT SYSDATE FROM DUAL;`), operador de concatenación `||`, cláusula `ROWNUM`/`ROW_NUMBER()` para paginación (`FETCH FIRST n ROWS ONLY` desde 12c), funciones analíticas (`OVER (PARTITION BY ... ORDER BY ...)`: `RANK()`, `DENSE_RANK()`, `LAG()`, `LEAD()`), consultas jerárquicas (`CONNECT BY PRIOR ... START WITH`), y `MERGE` para upsert:

```sql
MERGE INTO stock s
USING (SELECT id_prod, cantidad FROM entradas) e
ON (s.id_prod = e.id_prod)
WHEN MATCHED THEN UPDATE SET s.cantidad = s.cantidad + e.cantidad
WHEN NOT MATCHED THEN INSERT (id_prod, cantidad) VALUES (e.id_prod, e.cantidad);
```

**PL/SQL (Procedural Language/SQL)** es la extensión procedimental propietaria de Oracle que embebe SQL dentro de estructuras de control tipo Ada. Un bloque tiene la estructura:

```sql
DECLARE
  v_salario empleados.salario%TYPE;
  v_nombre  empleados.nombre%TYPE;
  ex_sin_datos EXCEPTION;
BEGIN
  SELECT salario, nombre INTO v_salario, v_nombre
  FROM empleados WHERE id_emp = 100;

  IF v_salario < 1200 THEN
    UPDATE empleados SET salario = salario * 1.05 WHERE id_emp = 100;
  ELSIF v_salario > 5000 THEN
    RAISE ex_sin_datos;
  END IF;

  COMMIT;
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    DBMS_OUTPUT.PUT_LINE('Empleado no encontrado');
  WHEN OTHERS THEN
    ROLLBACK;
    RAISE;
END;
/
```

**Elementos clave**: variables con `%TYPE` (ancla al tipo de una columna) y `%ROWTYPE` (ancla a la fila completa); estructuras de control `IF/ELSIF`, `LOOP`/`WHILE LOOP`/`FOR LOOP`; **cursores** explícitos (`CURSOR c IS SELECT ...; OPEN/FETCH/CLOSE`) e implícitos; **cursores FOR** (abren y cierran automáticamente); registros (`TYPE ... IS RECORD`) y colecciones (`TABLE`, `VARRAY`, `ASSOCIATIVE ARRAY`/`INDEX BY`).

**Manejo de excepciones**: predefinidas (`NO_DATA_FOUND`, `TOO_MANY_ROWS`, `DUP_VAL_ON_INDEX`, `ZERO_DIVIDE`), definidas por el usuario (`EXCEPTION` + `RAISE`) y `PRAGMA EXCEPTION_INIT` para asociar un código Oracle (`SQLCODE`) a una excepción con nombre.

**Bulk operations** para rendimiento en procesamiento masivo, evitando el context switch SQL↔PL/SQL fila a fila:
```sql
DECLARE
  TYPE t_ids IS TABLE OF NUMBER;
  v_ids t_ids;
BEGIN
  SELECT id_emp BULK COLLECT INTO v_ids FROM empleados WHERE activo = 'S';
  FORALL i IN v_ids.FIRST..v_ids.LAST
    UPDATE empleados SET revisado = 'S' WHERE id_emp = v_ids(i);
END;
/
```

**Funciones y procedimientos almacenados:**
```sql
CREATE OR REPLACE FUNCTION calcular_iva(p_base IN NUMBER, p_tipo IN NUMBER DEFAULT 21)
RETURN NUMBER IS
BEGIN
  RETURN ROUND(p_base * p_tipo / 100, 2);
END;
/
```

**Paquetes**, con estado persistente durante la sesión (variables globales de paquete) y sobrecarga de subprogramas:
```sql
CREATE OR REPLACE PACKAGE pkg_rrhh AS
  FUNCTION antiguedad(p_id NUMBER) RETURN NUMBER;
  PROCEDURE subir_salario(p_id NUMBER, p_pct NUMBER);
END pkg_rrhh;
/
```

**Triggers PL/SQL compuestos** (`COMPOUND TRIGGER`, desde 11g) resuelven el error de mutating table permitiendo secciones `BEFORE STATEMENT`, `BEFORE EACH ROW`, `AFTER EACH ROW`, `AFTER STATEMENT` en un único trigger.

**Optimización**: uso de bind variables (`:variable`) para favorecer el *cursor sharing* y evitar hard parses; `EXPLAIN PLAN`/`AUTOTRACE` para analizar el plan de ejecución; paquetes de utilidad `DBMS_OUTPUT`, `UTL_FILE`, `DBMS_SCHEDULER`, `DBMS_XPLAN`.

## Tema 23. Oracle. Oracle Developer (Oracle Forms, Oracle Reports).

**Oracle Developer Suite** (Oracle Developer/2000 en sus orígenes) es el conjunto de herramientas RAD (Rapid Application Development) de Oracle para construir aplicaciones cliente/servidor y, desde la versión 6i en adelante, aplicaciones desplegadas en tres capas mediante **Oracle Application Server (Forms Services)**. Incluye principalmente Oracle Forms y Oracle Reports, junto a Oracle Designer y Oracle Discoverer (herramientas complementarias hoy en desuso).

**Oracle Forms.** Herramienta para construir formularios de entrada/consulta de datos altamente ligados a la base de datos (data-bound), muy usada históricamente en aplicaciones corporativas y de Administración Pública sobre Oracle.

**Arquitectura de ejecución**: en modo web, el cliente ejecuta un **applet Java (Forms Applet)** o, desde versiones modernas, el **Forms Web client** vía Java Web Start/JNLP, que se comunica con el **Forms Listener Servlet** en el servidor de aplicaciones, el cual delega en un **Forms Runtime Engine (frmweb)** que mantiene la sesión y ejecuta la lógica, conectando a la base de datos Oracle.

**Componentes de un módulo Forms (.fmb, compilado a .fmx):**
- **Bloques de datos (Data Blocks)**: vinculados a tablas/vistas o procedimientos (bloques no basados en tabla), gestionan automáticamente `SELECT`, `INSERT`, `UPDATE`, `DELETE` mediante el motor de Forms.
- **Ítems (Items)**: campos de texto, listas, casillas, botones de radio, dentro de un canvas (lienzo visual).
- **Canvas y Ventanas**: superficies de presentación.
- **LOV (List of Values)** y **Record Groups**: listas de selección basadas en consultas SQL.
- **Triggers de Forms**: código PL/SQL asociado a eventos, con nomenclatura por nivel:
  - Nivel formulario: `WHEN-NEW-FORM-INSTANCE`, `KEY-EXIT`.
  - Nivel bloque: `PRE-QUERY`, `POST-QUERY`.
  - Nivel ítem: `WHEN-VALIDATE-ITEM`, `WHEN-BUTTON-PRESSED`, `KEY-NEXT-ITEM`.

**Ejemplo de trigger `WHEN-VALIDATE-ITEM`:**
```sql
DECLARE
  v_existe NUMBER;
BEGIN
  SELECT COUNT(*) INTO v_existe
  FROM clientes WHERE nif = :bloque_clientes.nif;

  IF v_existe = 0 THEN
    MESSAGE('NIF no encontrado en el sistema');
    RAISE FORM_TRIGGER_FAILURE;
  END IF;
END;
```

**Program Units**: procedimientos/funciones PL/SQL reutilizables dentro del módulo, o en **librerías (.pll)** compartidas entre varios formularios (`ATTACH LIBRARY`).

**Estados de registro**: `NEW`, `QUERY`, `CHANGED`, `INSERT` — controlan qué operación DML se ejecutará al hacer commit (`COMMIT_FORM`, tecla F10 por defecto).

**Menús** (.mmb): módulos de menú personalizados que sustituyen el menú por defecto de Forms, con roles de seguridad asociados.

**Oracle Reports.** Herramienta de generación de informes (.rdf) con salida en múltiples formatos: pantalla, PDF, HTML, PostScript, hoja de cálculo, XML.

**Modelo de un informe:**
- **Data Model**: consultas SQL (Q_1, Q_2...) organizadas jerárquicamente mediante enlaces de datos (grupos padre-hijo, `master-detail`), fórmulas y columnas resumen (`%COUNT`, `%SUM`).
- **Layout Model**: disposición visual mediante *frames*, *repeating frames* (que iteran sobre los grupos de datos), campos y boilerplate (texto fijo).
- **PL/SQL asociado**: triggers de formato (`Format Trigger`, oculta/muestra elementos condicionalmente), y triggers del informe (`Before Report`, `After Report`, `Between Pages`).

**Ejemplo de consulta jerárquica en el Data Model:**
```sql
-- Q_1 (maestro)
SELECT id_dpto, nombre_dpto FROM departamentos;
-- Q_2 (detalle, enlazado por id_dpto)
SELECT nombre, salario FROM empleados WHERE id_dpto = :id_dpto;
```

**Despliegue**: en modo servidor, **Reports Server** encola y ejecuta peticiones (batch o interactivo), invocable desde Forms mediante `RUN_PRODUCT` o el paquete `RUN_REPORT_OBJECT`. En entornos actuales, Oracle Forms/Reports 12c se ejecuta sobre **WebLogic Server**, y Oracle mantiene la tecnología en modo de soporte extendido, recomendando migraciones hacia **APEX (Application Express)** o arquitecturas web modernas, migración habitual en la modernización de sistemas legados de la Administración.

## Tema 24. Diseño de páginas web. HTML. JavaScript. Intercambio de datos en Internet: formatos XML y JSON.

**HTML (HyperText Markup Language)**, estandarizado por el W3C/WHATWG, actualmente **HTML5** (Living Standard). Define la estructura semántica de una página mediante etiquetas.

**Estructura básica y semántica HTML5:**
```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Portal de trámites</title>
</head>
<body>
  <header><nav>...</nav></header>
  <main>
    <article>
      <h1>Solicitud de cita</h1>
      <section>...</section>
    </article>
  </main>
  <footer>...</footer>
</body>
</html>
```
Elementos semánticos clave: `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`, `<figure>`, mejoran accesibilidad (WAI-ARIA, atributos `role`, `aria-label`) y SEO frente al uso indiscriminado de `<div>`. **Formularios**: `<form>`, `<input type="email|date|number">`, validación nativa (`required`, `pattern`, `min`/`max`). APIs HTML5 relevantes: Canvas, LocalStorage/SessionStorage, Geolocation, WebSockets, Fetch API.

**JavaScript**, lenguaje interpretado, dinámico, basado en prototipos, con estándar **ECMAScript** (ES6/ES2015 en adelante marca la modernización: `let`/`const`, arrow functions, clases, `Promise`, módulos, plantillas literales).

**Manipulación del DOM:**
```javascript
document.getElementById('btnEnviar').addEventListener('click', async () => {
  const nombre = document.querySelector('#nombre').value;
  if (!nombre) {
    alert('Campo obligatorio');
    return;
  }
  const respuesta = await fetch('/api/solicitudes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre })
  });
  const datos = await respuesta.json();
  console.log(datos);
});
```

**Conceptos clave de JS moderno**: closures, hoisting, event loop (asincronía mediante *callback queue* y *microtask queue*), `this` y su enlace dinámico (`bind`/`call`/`apply`), programación funcional (`map`, `filter`, `reduce`), clases ES6 con `class`/`extends`, módulos (`import`/`export`), y manejo de promesas con `async`/`await` para evitar el *callback hell*.

**JavaScript en el navegador vs. Node.js**: en el cliente interactúa con el DOM/BOM; Node.js (motor V8) permite ejecución en servidor, con `npm` como gestor de paquetes.

**Intercambio de datos: XML.** Lenguaje de marcado extensible (W3C, 1998), jerárquico, autodescriptivo, con validación mediante DTD o **XSD (XML Schema Definition)**, transformable con **XSLT**.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<solicitudes>
  <solicitud id="1001">
    <ciudadano nif="12345678A">Juan Pérez</ciudadano>
    <fecha>2026-08-27</fecha>
    <estado>PENDIENTE</estado>
  </solicitud>
</solicitudes>
```
Usos típicos: SOAP (envoltura `<Envelope>`/`<Header>`/`<Body>`), configuraciones, intercambio en la interoperabilidad administrativa (esquemas SICRES, facturación electrónica Facturae).

**JSON (JavaScript Object Notation)**, formato más ligero (RFC 8259), notación de objetos/arrays nativa de JS, hoy predominante en APIs REST por su menor verbosidad y parseo directo.

```json
{
  "solicitud": {
    "id": 1001,
    "ciudadano": { "nif": "12345678A", "nombre": "Juan Pérez" },
    "fecha": "2026-08-27",
    "estado": "PENDIENTE",
    "documentos": ["dni.pdf", "empadronamiento.pdf"]
  }
}
```

**Comparativa XML vs. JSON**: XML admite atributos, namespaces, validación de esquema robusta y transformación declarativa (XSLT), preferible en contextos que exigen contratos estrictos e interoperabilidad formal (Administración, SOAP). JSON es más compacto, de parseo nativo en JS (`JSON.parse()`/`JSON.stringify()`) y dominante en APIs REST modernas y aplicaciones SPA. Ambos se validan: XML con XSD, JSON con **JSON Schema**.

## Tema 25. El lenguaje de programación Java: sintaxis, tipos de datos, operadores, estructuras de control.

Java es un lenguaje de programación orientado a objetos, fuertemente tipado, compilado a bytecode y ejecutado sobre la **JVM (Java Virtual Machine)**, lo que le confiere portabilidad ("write once, run anywhere"). Desarrollado originalmente por Sun Microsystems (1995), hoy propiedad de Oracle, con ciclo de versiones semestral desde Java 9 y versiones LTS (8, 11, 17, 21).

**Estructura básica de un programa:**
```java
package com.carm.app;

import java.util.List;
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        System.out.println("Inicio de la aplicación");
    }
}
```

**Tipos de datos primitivos** (8 tipos, almacenados por valor):
| Tipo | Tamaño | Rango/uso |
|---|---|---|
| `byte` | 8 bits | -128 a 127 |
| `short` | 16 bits | enteros pequeños |
| `int` | 32 bits | entero por defecto |
| `long` | 64 bits | requiere sufijo `L` |
| `float` | 32 bits | coma flotante, sufijo `f` |
| `double` | 64 bits | coma flotante por defecto |
| `char` | 16 bits | carácter Unicode (UTF-16) |
| `boolean` | 1 bit lógico | `true`/`false` |

**Tipos de referencia**: clases, interfaces, arrays, enums. Cada primitivo tiene su **wrapper class** (`Integer`, `Double`, `Boolean`...) para uso en colecciones genéricas, con *autoboxing/unboxing* automático desde Java 5.

**Operadores**: aritméticos (`+ - * / %`), de asignación (`= += -= *=`), relacionales (`== != > < >= <=`), lógicos (`&& || !`, con cortocircuito), a nivel de bit (`& | ^ ~ << >> >>>`), condicional ternario (`cond ? a : b`), `instanceof` (comprobación de tipo, con *pattern matching* desde Java 16: `if (obj instanceof String s)`). Importante distinguir `==` (compara referencias en objetos, valor en primitivos) de `.equals()` (compara contenido lógico).

**Estructuras de control:**

Condicionales:
```java
if (edad >= 18) {
    System.out.println("Mayor de edad");
} else if (edad >= 14) {
    System.out.println("Adolescente");
} else {
    System.out.println("Menor");
}

// switch expression (Java 14+)
String categoria = switch (mes) {
    case 12, 1, 2 -> "Invierno";
    case 3, 4, 5 -> "Primavera";
    default -> "Otra estación";
};
```

Bucles:
```java
for (int i = 0; i < 10; i++) { /* ... */ }

for (String nombre : listaNombres) { /* for-each */ }

int i = 0;
while (i < 10) { i++; }

do {
    i--;
} while (i > 0);
```

**Arrays**:
```java
int[] numeros = {1, 2, 3, 4, 5};
int[][] matriz = new int[3][3];
```

**Manejo de excepciones** (checked vs. unchecked):
```java
try {
    int resultado = 10 / divisor;
} catch (ArithmeticException e) {
    System.err.println("Error: " + e.getMessage());
} finally {
    System.out.println("Bloque finally siempre se ejecuta");
}
```
Excepciones *checked* (`IOException`, `SQLException`) deben declararse con `throws` o capturarse obligatoriamente; *unchecked* (`RuntimeException` y subclases como `NullPointerException`, `ArrayIndexOutOfBoundsException`) no lo exigen. Desde Java 7, *try-with-resources* cierra automáticamente recursos `AutoCloseable`:
```java
try (Connection con = DriverManager.getConnection(url, user, pass)) {
    // uso de con
} catch (SQLException e) {
    e.printStackTrace();
}
```

**Genéricos y colecciones**:
```java
List<String> nombres = new ArrayList<>();
Map<String, Integer> edades = new HashMap<>();
```

**Elementos modernos**: *records* (Java 16, clases inmutables concisas: `record Punto(int x, int y) {}`), *streams* para procesamiento funcional (`lista.stream().filter(n -> n > 10).collect(Collectors.toList())`), expresiones lambda (`(a, b) -> a + b`) e interfaces funcionales (`Runnable`, `Comparator`, `Function<T,R>`).

## Tema 26. Reglamento (UE) 2016/679 del Parlamento Europeo y del Consejo de 27 de abril de 2016 relativo a la protección de las personas físicas en lo que respecta al tratamiento de datos personales y a la libre circulación de estos datos (RGPD).

El **RGPD** (Reglamento General de Protección de Datos, Reglamento UE 2016/679), aplicable desde el 25 de mayo de 2018, es de aplicación directa en todos los Estados miembros sin necesidad de transposición, sustituyendo a la Directiva 95/46/CE. En España se completa con la **LOPDGDD** (Ley Orgánica 3/2018, de Protección de Datos Personales y garantía de los derechos digitales).

**Ámbito de aplicación**: material (tratamiento total o parcialmente automatizado de datos personales, o tratamiento no automatizado incluido en un fichero) y territorial (responsables/encargados establecidos en la UE, y también fuera de la UE si ofrecen bienes/servicios o monitorizan el comportamiento de interesados en la UE — criterio de extraterritorialidad, art. 3).

**Principios (art. 5)**: licitud, lealtad y transparencia; limitación de la finalidad; minimización de datos; exactitud; limitación del plazo de conservación; integridad y confidencialidad; y **responsabilidad proactiva (accountability)**, principio transversal que obliga al responsable a poder demostrar el cumplimiento.

**Bases de legitimación (art. 6)**: consentimiento (debe ser libre, específico, informado, inequívoco y revocable, art. 4.11 y 7), ejecución de un contrato, cumplimiento de una obligación legal, protección de intereses vitales, cumplimiento de una misión de interés público o ejercicio de poderes públicos (base típica de la Administración), e interés legítimo.

**Categorías especiales de datos (art. 9)**: origen étnico/racial, opiniones políticas, convicciones religiosas/filosóficas, afiliación sindical, datos genéticos, biométricos, de salud, vida u orientación sexual — tratamiento prohibido salvo excepciones tasadas (consentimiento explícito, interés público esencial, obligación en el ámbito laboral/social).

**Derechos de los interesados (arts. 15-22, "ARSULOP")**: Acceso, Rectificación, Supresión ("derecho al olvido"), Limitación del tratamiento, Portabilidad (obtener los datos en formato estructurado, de uso común y lectura mecánica), Oposición, y decisiones no basadas únicamente en tratamiento automatizado (incluida la elaboración de perfiles). Plazo general de respuesta: **1 mes**, prorrogable 2 meses más si es complejo.

**Obligaciones del responsable/encargado**:
- **Registro de actividades de tratamiento (RAT, art. 30)**: obligatorio (con umbral de exención para organizaciones <250 empleados salvo ciertos supuestos).
- **Evaluación de Impacto relativa a la Protección de Datos (EIPD/DPIA, art. 35)**: obligatoria cuando el tratamiento entrañe alto riesgo (evaluación sistemática, tratamiento a gran escala de categorías especiales, observación sistemática a gran escala).
- **Delegado de Protección de Datos (DPO, art. 37)**: obligatorio en autoridades/organismos públicos (salvo tribunales en ejercicio de función jurisdiccional), en tratamientos de observación sistemática a gran escala, o categorías especiales a gran escala.
- **Privacidad desde el diseño y por defecto (art. 25)**: incorporar medidas técnicas/organizativas desde la concepción del sistema y configurar por defecto solo el tratamiento necesario.
- **Notificación de violaciones de seguridad (arts. 33-34)**: a la autoridad de control (AEPD en España) en un plazo máximo de **72 horas** desde que se tenga conocimiento; comunicación al interesado si supone alto riesgo.
- **Medidas de seguridad (art. 32)**: pseudonimización, cifrado, garantía de confidencialidad/integridad/disponibilidad/resiliencia, capacidad de restauración tras incidente, verificación periódica.

**Encargado del tratamiento**: debe existir un contrato o acto jurídico (art. 28) que regule objeto, duración, naturaleza, finalidad, tipo de datos, obligaciones y derechos.

**Transferencias internacionales (Capítulo V)**: solo a terceros países con decisión de adecuación de la Comisión, o mediante garantías adecuadas (Cláusulas Contractuales Tipo, normas corporativas vinculantes - BCR).

**Sanciones (art. 83)**: dos niveles — hasta 10 millones € o 2% del volumen de negocio global (infracciones "menos graves": deberes del encargado, EIPD, DPO) y hasta 20 millones € o 4% (infracciones "graves": principios, consentimiento, derechos de los interesados, transferencias internacionales). La AEPD es la autoridad de control en España, con potestad sancionadora e inspectora.

## Tema 27. Seguridad en redes de ordenadores. Tipos de ataques y defensas. Políticas de seguridad para redes corporativas.

**Fundamentos de seguridad**: la tríada CIA — Confidencialidad, Integridad, Disponibilidad —, ampliada con Autenticidad y No Repudio (modelo CIDAN/AAA extendido).

**Tipos de ataques:**

*Ataques de reconocimiento*: sniffing (captura de tráfico, herramientas Wireshark/tcpdump), escaneo de puertos (Nmap), footprinting.

*Ataques de acceso/intrusión*:
- **Spoofing**: IP spoofing (suplantación de dirección origen), ARP spoofing/poisoning (envenenamiento de tablas ARP para interceptar tráfico en LAN), DNS spoofing/cache poisoning.
- **Man-in-the-Middle (MitM)**: interceptación activa entre dos partes, frecuentemente combinado con ARP spoofing o portales wifi falsos (evil twin).
- **Ataques de fuerza bruta y diccionario** contra credenciales.
- **Explotación de vulnerabilidades**: buffer overflow, inyección SQL, RCE (Remote Code Execution) sobre servicios expuestos.

*Ataques de denegación de servicio*:
- **DoS/DDoS**: SYN flood (agotamiento de la pila TCP mediante conexiones semiabiertas), UDP flood, ICMP flood (ping flood), ataques de amplificación (DNS/NTP amplification), y a nivel de aplicación (HTTP flood, Slowloris).

*Malware*: virus, gusanos (autopropagación en red sin intervención humana), troyanos, ransomware (cifrado extorsivo, vector habitual: phishing/RDP expuesto), rootkits (persistencia oculta a nivel de kernel), botnets (redes de equipos zombi controladas para DDoS/spam).

*Ingeniería social*: phishing, spear phishing (dirigido), whaling (a directivos), vishing/smishing (voz/SMS), pretexting.

*Ataques a nivel de aplicación web*: XSS (Cross-Site Scripting, inyección de script en páginas confiadas), CSRF (Cross-Site Request Forgery), inyección SQL, path traversal, referenciados en el **OWASP Top 10**.

**Defensas y controles:**

**Perimetrales**: **Firewall** (filtrado por reglas, capas 3-4; de nueva generación NGFW añade inspección de capa 7 y control de aplicaciones), **IDS/IPS** (Snort, Suricata — detección vs. prevención activa mediante firmas y análisis de anomalías), **DMZ** (zona desmilitarizada para servicios expuestos, aislada de la red interna con doble firewall o firewall de tres interfaces), **proxy** (control de salida, filtrado de contenido) y **reverse proxy** (protección de servidores internos).

**Segmentación**: VLAN (aislamiento lógico de capa 2), microsegmentación en entornos virtualizados, arquitectura **Zero Trust** (verificación continua, "nunca confiar, siempre verificar", independiente de la ubicación en red).

**Cifrado**: VPN (IPSec en modo túnel/transporte, con IKE para negociación de claves; SSL/TLS VPN), TLS 1.2/1.3 para tráfico web, cifrado en reposo de datos sensibles.

**Autenticación**: **802.1X** (control de acceso a red basado en puertos, con servidor RADIUS), **MFA** (autenticación multifactor), políticas de contraseñas robustas, gestión de identidades (IAM).

**Monitorización**: **SIEM** (correlación de logs y eventos de seguridad, alertas), **NAC** (Network Access Control, verifica cumplimiento del endpoint antes de conceder acceso), honeypots (señuelos para detectar/estudiar atacantes), análisis de tráfico con NetFlow/sFlow.

**Protección de infraestructura**: hardening de sistemas (deshabilitar servicios innecesarios, parcheo regular), segregación de redes de gestión (out-of-band), listas de control de acceso (ACL) en routers/switches, port security (limitación de MAC por puerto), protección contra spoofing con DHCP snooping y Dynamic ARP Inspection.

**Políticas de seguridad corporativas**: deben incluir política de uso aceptable (PUA), gestión de activos, control de acceso basado en el principio de mínimo privilegio, clasificación de la información, gestión de parches, plan de respuesta a incidentes (con roles CSIRT/CERT), plan de continuidad de negocio (BCP) y de recuperación ante desastres (DRP), formación y concienciación periódica del personal (el eslabón humano es el vector más explotado), auditorías periódicas y pentesting, y cumplimiento normativo (ENS en el caso de la Administración Pública española, ISO/IEC 27001 como marco de gestión).

## Tema 28. Certificados digitales.

Un **certificado digital** es un documento electrónico firmado por una Autoridad de Certificación (CA) que vincula una clave pública a la identidad de su titular (persona física, jurídica, dispositivo o sede electrónica), garantizando autenticidad, integridad y no repudio en las comunicaciones y transacciones electrónicas. Se basa en criptografía asimétrica: un par de claves, pública (contenida en el certificado, distribuible) y privada (custodiada de forma segura por el titular, en tarjeta criptográfica, HSM o almacén software).

**Estándar X.509 (v3)**, campos principales: número de serie, algoritmo de firma (típicamente `SHA256withRSA` o ECDSA), emisor (Issuer/DN de la CA), periodo de validez (`Not Before`/`Not After`), sujeto (Subject/DN del titular), clave pública, extensiones (Key Usage, Extended Key Usage, Subject Alternative Name — SAN, CRL Distribution Point, Authority Information Access/OCSP), y la firma digital de la CA sobre todo lo anterior.

**Infraestructura de Clave Pública (PKI)**, componentes:
- **Autoridad de Certificación (CA)**: emite y firma certificados; puede haber jerarquía (CA raíz, autofirmada, y CAs subordinadas/intermedias) formando una **cadena de confianza** que se valida hasta un certificado raíz de confianza instalado en el almacén del sistema/navegador.
- **Autoridad de Registro (RA)**: verifica la identidad del solicitante antes de la emisión (en España, oficinas de registro presenciales para persona física con FNMT).
- **Repositorio/Directorio**: publica certificados emitidos y listas de revocación.
- **Autoridad de Validación**: comprueba el estado de un certificado mediante **CRL** (Certificate Revocation List, lista periódica de números de serie revocados) u **OCSP** (Online Certificate Status Protocol, consulta en tiempo real punto a punto, más eficiente y con menor latencia de propagación).

**Ciclo de vida**: solicitud → verificación de identidad (RA) → generación de par de claves → emisión y firma (CA) → distribución → uso → renovación → revocación (por compromiso de clave, cese, cambio de datos) o expiración.

**Tipos de certificados en España**: certificado de persona física (FNMT, DNIe — este último embebido en el chip del documento de identidad), de representante (persona jurídica/entidad sin personalidad), de sede electrónica (identifica un sitio web de una Administración), de sello electrónico (actuación administrativa automatizada, sin intervención de una persona física concreta), de empleado público, y certificados de componente/servidor (TLS).

**Prestadores de servicios de confianza cualificados** en España, según el **Reglamento eIDAS (UE 910/2014)**: FNMT-RCM (CERES), DNIe, y otros prestadores privados (Camerfirma, Firmaprofesional, ANF AC, etc.), listados en la TSL (Trusted List) nacional.

**Firma electrónica**, niveles según eIDAS: simple, avanzada (vinculada de manera única al firmante, permite su identificación, creada con medios bajo su control exclusivo y detecta modificaciones posteriores) y **cualificada** (avanzada + certificado cualificado + dispositivo cualificado de creación de firma, DCCF — equivalente jurídico a la firma manuscrita, con presunción de validez).

**Formatos de firma electrónica avanzada**: **XAdES** (XML Advanced Electronic Signatures), **CAdES** (basado en CMS/PKCS#7, para cualquier tipo de documento binario), **PAdES** (específico para PDF, compatible con el estándar ISO 32000). Cada uno define niveles de firma (BES, T con sello de tiempo, LT con información de validación a largo plazo, LTA con archivo a largo plazo).

**Sello de tiempo (timestamp, RFC 3161)**: emitido por una TSA (Time Stamping Authority), garantiza que un documento existía en un instante determinado, esencial para la validez a largo plazo de la firma tras la expiración del certificado.

**Aplicación práctica en la Administración**: plataformas @firma (validación de certificados y firma del Estado), Cl@ve (identificación electrónica ciudadana, combina Cl@ve PIN/Permanente con certificado/DNIe), Autofirma (cliente de firma de escritorio del Gobierno de España), Port@firmas (tramitación de firmas en flujos de trabajo administrativos).

## Tema 29. Real Decreto 3/2010, de 8 de enero, por el que se regula el Esquema Nacional de Seguridad en el ámbito de la Administración Electrónica (ENS).

El **Esquema Nacional de Seguridad (ENS)** fue creado por el **RD 3/2010**, de 8 de enero, en desarrollo del artículo 42 de la entonces Ley 11/2007 de acceso electrónico de los ciudadanos, con el objetivo de establecer los principios y requisitos de una política de seguridad en la utilización de medios electrónicos que permitiera la protección adecuada de la información. **Este Real Decreto fue derogado y sustituido por el RD 311/2022, de 3 de mayo**, que actualiza el ENS adaptándolo al RGPD, a la Ley 40/2015 de Régimen Jurídico del Sector Público, al Reglamento eIDAS y a la evolución de las ciberamenazas, reforzando además la coordinación con el Esquema Nacional de Interoperabilidad (ENI) y con el CCN-CERT.

**Ámbito de aplicación (RD 311/2022)**: sector público (Administración General del Estado, CCAA, Entidades Locales, entidades de derecho público vinculadas) y, cuando presten servicios a las Administraciones o ejerzan potestades administrativas, también a entidades del sector privado.

**Principios básicos**: seguridad como proceso integral, gestión de la seguridad basada en riesgos, prevención/detección/respuesta/conservación (nuevo enfoque frente al RD 3/2010, que hablaba de prevención-reacción-recuperación), existencia de líneas de defensa, vigilancia continua, y reevaluación periódica.

**Requisitos mínimos**: organización e implantación del proceso de seguridad, análisis y gestión de riesgos, gestión de personal, profesionalidad, autorización y control de accesos, protección de instalaciones, adquisición de productos, seguridad por defecto, integridad y actualización del sistema, protección de la información almacenada y en tránsito, prevención frente a otros sistemas interconectados, registro de actividad y detección de código dañino, incidentes de seguridad, continuidad de la actividad, y mejora continua del proceso de seguridad.

**Categorización de sistemas**: se determina en función del impacto que tendría un incidente sobre las dimensiones de seguridad, en tres niveles — **BÁSICA, MEDIA, ALTA**. Las **dimensiones de seguridad (ADATC/CIDAT)** son: Confidencialidad, Integridad, Disponibilidad, Autenticidad y Trazabilidad (el RD 311/2022 añade "Conservación" como propiedad adicional). La categoría del sistema es la más alta entre las alcanzadas por cada dimensión, siguiendo la metodología de valoración recogida en el Anexo I.

**Medidas de seguridad (Anexo II)**, organizadas en tres grupos:
- **Marco organizativo**: política de seguridad, normativa de seguridad, procedimientos de seguridad, proceso de autorización.
- **Marco operacional**: planificación, control de acceso, explotación, servicios externos, continuidad del servicio, monitorización del sistema.
- **Medidas de protección**: protección de instalaciones e infraestructuras, gestión del personal, protección de equipos, protección de comunicaciones, protección de soportes de información, protección de aplicaciones informáticas, protección de la información, protección de servicios.

El número de medidas aplicables aumenta con la categoría del sistema (aplicación gradual/graduada); además existen **refuerzos** y medidas compensatorias cuando una medida no puede implantarse íntegramente.

**Auditoría de seguridad**: obligatoria al menos cada dos años (y siempre que haya cambios sustanciales) para sistemas de categoría MEDIA o ALTA; para categoría BÁSICA basta con autoevaluación. El informe de auditoría se remite al responsable de seguridad y a los órganos competentes.

**Declaración y certificación de conformidad**: el RD 311/2022 introduce la **Declaración de Conformidad** con el ENS y refuerza el régimen de **certificación** por entidades de certificación acreditadas por ENAC, otorgando mayor peso a la verificación independiente frente al modelo de autoevaluación predominante bajo el RD 3/2010.

**Estructura de gobernanza de la seguridad**: responsable de la información, **responsable de la seguridad** (distinto del responsable del sistema, garantiza la coordinación), **responsable del sistema**, y el **Comité o Comisión de Seguridad TIC**, roles que deben quedar diferenciados para evitar conflictos de interés.

**Actualización de guías CCN-STIC**: el Centro Criptológico Nacional (CCN) desarrolla la serie de guías CCN-STIC (destaca la CCN-STIC-800, "Glosario y Abreviaturas del ENS", y la CCN-STIC-804 sobre medidas de implantación) que operativizan los requisitos del ENS, herramienta de referencia obligada para cualquier técnico de sistemas de una Administración Pública española, incluida la CARM.
