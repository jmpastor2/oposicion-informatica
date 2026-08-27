# Bloque III — Desarrollo de Sistemas (Supuesto Práctico)
## Material de repaso — TAI C1, Administración General del Estado

---

# 1. Casos prácticos resueltos

---

## Caso práctico A — Modelado E/R, paso a tablas y normalización
### Gestión de expedientes administrativos

**Enunciado**

El Ayuntamiento de una localidad de tamaño medio desea informatizar la tramitación de **expedientes administrativos** (licencias de obra, licencias de actividad, subvenciones, etc.). Los requisitos funcionales recogidos son:

1. Cada expediente pertenece a un **tipo de procedimiento** (p. ej. "Licencia de obra menor"), que define un plazo máximo de resolución en días y la normativa aplicable.
2. Un expediente puede ser promovido por **uno o varios ciudadanos** (cotitulares), y un ciudadano puede promover varios expedientes a lo largo del tiempo.
3. Cada expediente tiene asignado un **funcionario tramitador** responsable, y a lo largo de su vida puede reasignarse a otro funcionario (se debe conservar el histórico de asignaciones).
4. Un expediente atraviesa distintos **estados** (Registrado, En subsanación, Informado, Resuelto, Archivado), y es obligatorio conservar la fecha de cada cambio y quién lo realizó.
5. Un expediente puede llevar adjuntos varios **documentos** (instancia, planos, informes técnicos), cada uno con nombre, tipo MIME, tamaño y hash de integridad.
6. Algunos procedimientos generan una **tasa** que el ciudadano debe abonar; de cada tasa se necesita el importe, la fecha de pago y la referencia de la pasarela de pago.

Se pide: (1) modelo entidad-relación, (2) paso al modelo relacional, (3) comprobación de que el resultado está en 3FN, partiendo de una tabla plana inicial sin normalizar.

---

**Resolución**

**1. Modelo E/R**

Entidades y relaciones identificadas:

- `CIUDADANO` (1) —— (N) `EXPEDIENTE_CIUDADANO` (N) —— (1) `EXPEDIENTE`  → relación N:M entre `CIUDADANO` y `EXPEDIENTE` (cotitularidad), resuelta con entidad asociativa.
- `TIPO_PROCEDIMIENTO` (1) —— (N) `EXPEDIENTE`
- `FUNCIONARIO` (1) —— (N) `ASIGNACION` (N) —— (1) `EXPEDIENTE` → histórico de tramitadores, también resuelto como entidad asociativa (no es un simple 1:N porque debe guardar historia).
- `ESTADO` (1) —— (N) `HISTORICO_ESTADO` (N) —— (1) `EXPEDIENTE`
- `EXPEDIENTE` (1) —— (N) `DOCUMENTO`
- `EXPEDIENTE` (1) —— (0..1) `TASA` (no todo expediente genera tasa)

Nótese que **cotitularidad** y **tramitador con historial** son ambas relaciones N:M o 1:N-con-historia que en el diagrama E/R deben modelarse ya como entidades débiles/asociativas (`EXPEDIENTE_CIUDADANO`, `ASIGNACION`), porque llevan atributos propios (fecha de alta como cotitular, fecha de inicio/fin de la asignación).

**2. Paso al modelo relacional**

```
TIPO_PROCEDIMIENTO (id_tipo_proc PK, nombre, plazo_dias, normativa)

CIUDADANO (nif PK, nombre, apellidos, direccion, email, telefono)

FUNCIONARIO (id_funcionario PK, nif, nombre, unidad)

ESTADO (id_estado PK, descripcion)

EXPEDIENTE (
  id_expediente PK,
  id_tipo_proc  FK -> TIPO_PROCEDIMIENTO,
  fecha_registro,
  id_estado_actual FK -> ESTADO      -- desnormalización controlada para acceso rápido
)

EXPEDIENTE_CIUDADANO (
  id_expediente FK -> EXPEDIENTE,
  nif_ciudadano FK -> CIUDADANO,
  fecha_alta_cotitular,
  PK (id_expediente, nif_ciudadano)
)

ASIGNACION (
  id_asignacion PK,
  id_expediente   FK -> EXPEDIENTE,
  id_funcionario  FK -> FUNCIONARIO,
  fecha_inicio,
  fecha_fin NULL
)

HISTORICO_ESTADO (
  id_historico PK,
  id_expediente FK -> EXPEDIENTE,
  id_estado     FK -> ESTADO,
  fecha_cambio,
  id_funcionario FK -> FUNCIONARIO
)

DOCUMENTO (
  id_documento PK,
  id_expediente FK -> EXPEDIENTE,
  nombre_archivo, tipo_mime, tamano_bytes, hash_sha256
)

TASA (
  id_tasa PK,
  id_expediente FK -> EXPEDIENTE UNIQUE,   -- 0..1: FK única
  importe, fecha_pago NULL, referencia_pasarela NULL
)
```

**3. Normalización (partiendo de una tabla plana)**

Si el análisis de partida fuese una única tabla del tipo:

```
EXPEDIENTE_PLANO(
  id_expediente, tipo_proc_nombre, plazo_dias,
  nif_ciudadano1, nombre_ciudadano1, nif_ciudadano2, nombre_ciudadano2,
  funcionario_actual, estado_actual, fecha_cambio_estado,
  doc1_nombre, doc2_nombre, doc3_nombre
)
```

Los problemas y su corrección serían:

- **Viola 1FN**: los grupos repetitivos `nif_ciudadano1/2`, `doc1/2/3` (número variable de cotitulares y documentos). Se corrige extrayendo `EXPEDIENTE_CIUDADANO` y `DOCUMENTO` como tablas hijas con clave que incluye `id_expediente`.
- **Viola 2FN** (si la PK fuese compuesta, p. ej. `(id_expediente, nif_ciudadano)`): atributos como `tipo_proc_nombre` o `plazo_dias` dependen solo de `id_expediente`, no de la clave completa → dependencia parcial. Se corrige separando `TIPO_PROCEDIMIENTO` en su propia tabla.
- **Viola 3FN**: `plazo_dias` depende de `tipo_proc_nombre`, que a su vez depende de `id_expediente` → dependencia transitiva (`id_expediente → tipo_proc_nombre → plazo_dias`). Se corrige igualmente aislando `TIPO_PROCEDIMIENTO(id_tipo_proc, nombre, plazo_dias)` y referenciándola por FK.
- El campo `estado_actual` + `fecha_cambio_estado` sin histórico impide cumplir el requisito 4 (conservar todos los cambios): se sustituye por la tabla `HISTORICO_ESTADO`, y `id_estado_actual` en `EXPEDIENTE` queda como una **desnormalización deliberada y documentada** (no vulnera 3FN porque es redundancia consciente para rendimiento, calculable siempre a partir del histórico).

El resultado final del apartado 2 está en **3FN**: cada atributo no clave depende de la clave, de toda la clave y de nada más que la clave.

---

## Caso práctico B — Consulta SQL con JOIN, GROUP BY y subconsulta
### Base de datos de personal

**Enunciado**

Se dispone del siguiente esquema simplificado de una base de datos de RRHH de un organismo:

```sql
DEPARTAMENTO(id_departamento PK, nombre_departamento)
PUESTO(id_puesto PK, nombre_puesto, complemento_destino)
EMPLEADO(
  id_empleado PK, nombre, id_departamento FK, id_puesto FK,
  salario_base, fecha_alta
)
```

Se pide una única consulta SQL que devuelva, **por cada departamento**, el nombre del departamento, el número de empleados, el salario medio (base + complemento de destino de su puesto) y que **solo incluya los departamentos cuyo salario medio supere la media global de la organización**. El resultado debe ordenarse de mayor a menor salario medio.

---

**Resolución**

```sql
SELECT
    d.nombre_departamento,
    COUNT(e.id_empleado)                              AS num_empleados,
    ROUND(AVG(e.salario_base + p.complemento_destino), 2) AS salario_medio_dpto
FROM DEPARTAMENTO d
INNER JOIN EMPLEADO e ON e.id_departamento = d.id_departamento
INNER JOIN PUESTO   p ON p.id_puesto       = e.id_puesto
GROUP BY d.id_departamento, d.nombre_departamento
HAVING AVG(e.salario_base + p.complemento_destino) > (
    SELECT AVG(e2.salario_base + p2.complemento_destino)
    FROM EMPLEADO e2
    INNER JOIN PUESTO p2 ON p2.id_puesto = e2.id_puesto
)
ORDER BY salario_medio_dpto DESC;
```

**Justificación de cada bloque:**

- `INNER JOIN` doble: se necesita el complemento de destino, que reside en `PUESTO`, no en `EMPLEADO` — un solo JOIN no bastaría.
- `GROUP BY` por `id_departamento` (y no solo por el nombre): buena práctica para evitar agrupar por una columna no clave que en teoría podría repetirse; además es obligatorio incluir en el `GROUP BY` toda columna no agregada del `SELECT`.
- `HAVING` en vez de `WHERE`: el filtro actúa **sobre el resultado agregado** (`AVG(...)`), y `WHERE` no admite funciones de agregación — se ejecuta antes del `GROUP BY`.
- **Subconsulta escalar no correlacionada** en el `HAVING`: calcula la media global una sola vez; al no depender de `d.id_departamento` no es correlacionada, por lo que el optimizador puede resolverla una única vez en lugar de por cada grupo.
- Se usa `AVG` sobre la expresión `salario_base + complemento_destino` para obtener directamente el salario medio total, no la suma de medias por separado (que sería incorrecto).

**Variante con CTE (más legible, SQL:1999 / SQL Server / Oracle / PostgreSQL):**

```sql
WITH salario_global AS (
    SELECT AVG(e.salario_base + p.complemento_destino) AS media
    FROM EMPLEADO e
    INNER JOIN PUESTO p ON p.id_puesto = e.id_puesto
)
SELECT d.nombre_departamento,
       COUNT(*) AS num_empleados,
       ROUND(AVG(e.salario_base + p.complemento_destino), 2) AS salario_medio_dpto
FROM DEPARTAMENTO d
INNER JOIN EMPLEADO e ON e.id_departamento = d.id_departamento
INNER JOIN PUESTO   p ON p.id_puesto       = e.id_puesto
CROSS JOIN salario_global sg
GROUP BY d.id_departamento, d.nombre_departamento, sg.media
HAVING AVG(e.salario_base + p.complemento_destino) > MIN(sg.media)
ORDER BY salario_medio_dpto DESC;
```

---

## Caso práctico C — Diseño de clase Java con herencia y polimorfismo
### Gestión documental

**Enunciado**

Un organismo necesita un módulo de **gestión documental** que trate de forma homogénea distintos tipos de documento (PDF, ofimático, documento firmado electrónicamente), pero que cada tipo calcule de forma distinta su "vista previa" y su validez. Se pide diseñar las clases en Java aplicando herencia, una interfaz para la capacidad de firma, y polimorfismo al procesar una lista heterogénea de documentos.

---

**Resolución**

```java
// Interfaz que aporta la capacidad de "ser firmable" — no todos los documentos lo son
public interface Firmable {
    void firmar(CertificadoDigital certificado);
    boolean isFirmado();
}

// Clase base abstracta: define el contrato común y comportamiento compartido
public abstract class Documento {

    protected final String nombreArchivo;
    protected final long tamanoBytes;
    protected final LocalDateTime fechaCarga;

    protected Documento(String nombreArchivo, long tamanoBytes) {
        this.nombreArchivo = nombreArchivo;
        this.tamanoBytes = tamanoBytes;
        this.fechaCarga = LocalDateTime.now();
    }

    // Método abstracto: cada subtipo decide cómo generar su vista previa
    public abstract String generarVistaPrevia();

    // Método abstracto: cada subtipo define su propia regla de validez
    public abstract boolean esValido();

    // Comportamiento común, no se repite en cada subclase
    public String getNombreArchivo() {
        return nombreArchivo;
    }

    @Override
    public String toString() {
        return String.format("%s [%s, %d bytes]",
                getClass().getSimpleName(), nombreArchivo, tamanoBytes);
    }
}

public class DocumentoPDF extends Documento {

    private final int numeroPaginas;

    public DocumentoPDF(String nombreArchivo, long tamanoBytes, int numeroPaginas) {
        super(nombreArchivo, tamanoBytes);
        this.numeroPaginas = numeroPaginas;
    }

    @Override
    public String generarVistaPrevia() {
        return "Miniatura de la primera página del PDF (" + numeroPaginas + " págs.)";
    }

    @Override
    public boolean esValido() {
        return numeroPaginas > 0 && tamanoBytes > 0;
    }
}

public class DocumentoOfimatico extends Documento {

    private final String aplicacionOrigen; // "Writer", "Word", "Calc"...

    public DocumentoOfimatico(String nombreArchivo, long tamanoBytes, String aplicacionOrigen) {
        super(nombreArchivo, tamanoBytes);
        this.aplicacionOrigen = aplicacionOrigen;
    }

    @Override
    public String generarVistaPrevia() {
        return "Extracto de texto convertido desde " + aplicacionOrigen;
    }

    @Override
    public boolean esValido() {
        return tamanoBytes > 0 && aplicacionOrigen != null;
    }
}

// Documento firmado: hereda de DocumentoPDF (un PDF firmado sigue siendo un PDF)
// e implementa Firmable para añadir la capacidad de firma electrónica
public class DocumentoFirmado extends DocumentoPDF implements Firmable {

    private boolean firmado = false;
    private String huellaFirma;

    public DocumentoFirmado(String nombreArchivo, long tamanoBytes, int numeroPaginas) {
        super(nombreArchivo, tamanoBytes, numeroPaginas);
    }

    @Override
    public void firmar(CertificadoDigital certificado) {
        this.huellaFirma = certificado.firmarHash(this.nombreArchivo);
        this.firmado = true;
    }

    @Override
    public boolean isFirmado() {
        return firmado;
    }

    @Override
    public boolean esValido() {
        // Sobrescribe la validez heredada: además de ser un PDF correcto, debe estar firmado
        return super.esValido() && firmado;
    }
}
```

**Uso polimórfico:**

```java
List<Documento> expediente = new ArrayList<>();
expediente.add(new DocumentoPDF("informe_tecnico.pdf", 204800, 12));
expediente.add(new DocumentoOfimatico("instancia.odt", 34500, "Writer"));

DocumentoFirmado resolucion = new DocumentoFirmado("resolucion.pdf", 51200, 3);
resolucion.firmar(certificadoAlcaldia);
expediente.add(resolucion);

for (Documento doc : expediente) {
    // Enlace dinámico: la JVM decide en tiempo de ejecución qué generarVistaPrevia()
    // y qué esValido() invocar según el tipo real del objeto, no de la variable
    System.out.println(doc + " -> " + doc.generarVistaPrevia());
    if (!doc.esValido()) {
        throw new IllegalStateException("Documento inválido: " + doc.getNombreArchivo());
    }
    if (doc instanceof Firmable f && !f.isFirmado()) {
        System.out.println("Aviso: documento firmable pendiente de firma");
    }
}
```

**Puntos clave para el examen:**
- `Documento` es **abstracta** porque no tiene sentido instanciar un "documento genérico"; obliga a las subclases a implementar el comportamiento variable.
- `Firmable` es una **interfaz**, no una clase base, porque la capacidad de firma es ortogonal a la jerarquía de tipo de documento (Java no permite herencia múltiple de clases, sí de interfaces).
- El bucle `for` demuestra **polimorfismo de inclusión**: la misma línea `doc.generarVistaPrevia()` ejecuta código distinto según el objeto real (ligadura dinámica / *late binding*).
- `DocumentoFirmado.esValido()` ilustra **sobrescritura (override)** con `super.esValido()`, no ocultación.

---

## Caso práctico D — REST vs SOAP para integración entre organismos

**Enunciado**

Dos organismos deben intercambiar información: el Ayuntamiento necesita consultar datos de empadronamiento contra un servicio del Ministerio (similar al Sistema de Verificación de Datos de Residencia) y, por otro lado, exponer un servicio propio para que aplicaciones móviles ciudadanas consulten el estado de sus expedientes. Se pide razonar qué tecnología de integración (REST o SOAP) conviene en cada caso.

---

**Resolución**

**Criterios de comparación:**

| Criterio | SOAP | REST |
|---|---|---|
| Contrato | WSDL, tipado estricto (XSD) | OpenAPI/Swagger, más flexible |
| Transporte | Normalmente HTTP, pero agnóstico (también JMS, SMTP) | HTTP nativo, usa sus verbos y códigos de estado |
| Seguridad | WS-Security (firma y cifrado a nivel de mensaje, extremo a extremo) | TLS a nivel de transporte + OAuth2/JWT a nivel de aplicación |
| Transaccionalidad | WS-AtomicTransaction, soporta operaciones complejas multi-paso | No estandarizada; se gestiona a nivel de aplicación |
| Acoplamiento | Fuerte (contrato rígido, cambios rompen clientes) | Débil, evoluciona mejor |
| Rendimiento/payload | XML más pesado, más *overhead* | JSON ligero, más eficiente |
| Interoperabilidad legacy AAPP | Muy extendido en plataformas históricas de la Administración (SCSP, @firma, muchos servicios de la Red SARA) | Estándar de facto en APIs modernas |

**Caso 1 — Consulta contra el Ministerio (SVDR/SCSP):** se recomienda **SOAP**.
- Estas plataformas ya publican sus servicios como SOAP sobre el **Sistema de Consulta de Datos entre Administraciones (SCSP)**, con seguridad **WS-Security** y firma XML extremo a extremo exigida por la normativa de intercambio entre AAPP; no se controla el extremo remoto, por lo que hay que adaptarse a lo publicado.
- Es una operación puntual de consulta con contrato muy formal y estable — el tipado estricto de WSDL/XSD reduce errores de interpretación entre organismos distintos.
- La transacción puede requerir garantías de no repudio (firma del mensaje), algo que WS-Security resuelve de forma nativa a nivel de mensaje (viaja cifrado/firmado aunque pase por intermediarios), mientras que REST solo protege el transporte (TLS) punto a punto.

**Caso 2 — API para app móvil ciudadana:** se recomienda **REST**.
- Cliente propio y nuevo (app móvil): no hay legado que condicione el protocolo, así que prima ligereza y facilidad de consumo. JSON reduce el consumo de datos y batería frente a XML/SOAP.
- Los verbos HTTP (`GET /expedientes/{id}`, `GET /expedientes/{id}/estado`) mapean de forma natural el modelo de recursos, con caché HTTP estándar (`ETag`, `Cache-Control`) para reducir carga en el servidor.
- Seguridad basada en **OAuth2 / JWT** sobre TLS es el estándar actual para apps móviles (p. ej. integrable con Cl@ve o Cl@ve Móvil como *identity provider*), con mejor soporte en SDKs móviles que WS-Security.
- Menor acoplamiento: la API puede evolucionar añadiendo campos sin romper clientes ya desplegados en tiendas de aplicaciones, algo crítico porque no se puede forzar la actualización inmediata de todas las apps instaladas.

**Conclusión:** la elección no es dogmática sino contextual — SOAP cuando el contrato lo impone un tercero, exige seguridad a nivel de mensaje o transaccionalidad formal (típico en interoperabilidad AAPP-AAPP histórica); REST cuando se diseña un servicio propio orientado a consumo ágil por clientes heterogéneos (web, móvil, terceros).

---

## Caso práctico E — Trigger SQL de auditoría

**Enunciado**

Sobre la tabla `EXPEDIENTE` del caso A, el órgano de control interno exige que quede constancia de **quién modifica o elimina** un expediente, **qué valores tenía antes y después**, y **cuándo**, sin depender de que la aplicación cliente recuerde hacerlo (debe garantizarse a nivel de base de datos).

---

**Resolución**

**Tabla de auditoría:**

```sql
CREATE TABLE AUDITORIA_EXPEDIENTE (
    id_auditoria     INT IDENTITY(1,1) PRIMARY KEY,
    id_expediente    INT           NOT NULL,
    operacion        CHAR(1)       NOT NULL,   -- 'U' = UPDATE, 'D' = DELETE
    id_estado_ant    INT           NULL,
    id_estado_nuevo  INT           NULL,
    usuario_bd       SYSNAME       NOT NULL,
    fecha_operacion  DATETIME2     NOT NULL DEFAULT SYSDATETIME()
);
```

**Trigger (sintaxis T-SQL, SQL Server):**

```sql
CREATE TRIGGER trg_auditoria_expediente
ON EXPEDIENTE
AFTER UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- Caso UPDATE: existen filas tanto en 'deleted' (valor antiguo) como en 'inserted' (valor nuevo)
    IF EXISTS (SELECT 1 FROM inserted)
    BEGIN
        INSERT INTO AUDITORIA_EXPEDIENTE
            (id_expediente, operacion, id_estado_ant, id_estado_nuevo, usuario_bd)
        SELECT
            d.id_expediente,
            'U',
            d.id_estado_actual,
            i.id_estado_actual,
            SUSER_SNAME()
        FROM deleted d
        INNER JOIN inserted i ON i.id_expediente = d.id_expediente;
    END
    ELSE
    BEGIN
        -- Caso DELETE: solo hay filas en 'deleted'
        INSERT INTO AUDITORIA_EXPEDIENTE
            (id_expediente, operacion, id_estado_ant, id_estado_nuevo, usuario_bd)
        SELECT
            d.id_expediente,
            'D',
            d.id_estado_actual,
            NULL,
            SUSER_SNAME()
        FROM deleted d;
    END
END;
```

**Justificación de diseño:**

- Es un **trigger AFTER** (no INSTEAD OF): la operación debe completarse realmente en `EXPEDIENTE` antes de registrar la auditoría; un `INSTEAD OF` sustituiría la operación original y obligaría a reimplementarla manualmente.
- Se combinan `UPDATE` y `DELETE` en un único trigger porque comparten casi toda la lógica; se distinguen por la presencia de filas en `inserted`.
- Se opera **por conjuntos** (`SELECT ... FROM deleted/inserted`), no fila a fila con cursores: los triggers pueden dispararse por sentencias que afectan a múltiples filas (`UPDATE ... WHERE id_departamento = X`), y un trigger mal escrito que asuma una sola fila es un error clásico y grave.
- `SUSER_SNAME()` captura el usuario de conexión a BD; si la aplicación usa un único usuario técnico para todas las conexiones, en un caso real habría que propagar el usuario de aplicación mediante `SESSION_CONTEXT` o un parámetro, dejando constancia de esa limitación.
- No se audita el `INSERT` porque el requisito solo pide modificaciones y eliminaciones (alta ya queda registrada por la propia existencia de la fila y su `fecha_registro`).

**Equivalente conceptual en PL/SQL (Oracle), por si el enunciado especifica ese motor:**

```sql
CREATE OR REPLACE TRIGGER trg_auditoria_expediente
AFTER UPDATE OR DELETE ON EXPEDIENTE
FOR EACH ROW
DECLARE
    v_operacion CHAR(1);
BEGIN
    v_operacion := CASE WHEN UPDATING THEN 'U' ELSE 'D' END;

    INSERT INTO AUDITORIA_EXPEDIENTE
        (id_expediente, operacion, id_estado_ant, id_estado_nuevo, usuario_bd, fecha_operacion)
    VALUES
        (:OLD.id_expediente, v_operacion, :OLD.id_estado_actual,
         CASE WHEN UPDATING THEN :NEW.id_estado_actual ELSE NULL END,
         SYS_CONTEXT('USERENV','SESSION_USER'), SYSTIMESTAMP);
END;
```

(En Oracle el trigger es `FOR EACH ROW` con pseudorregistros `:OLD`/`:NEW`, frente al enfoque por conjuntos de SQL Server con `inserted`/`deleted`; es una diferencia que suele preguntarse en el test.)

---

## Caso práctico F — Arquitectura cliente-servidor / microservicios
### Modernización de una aplicación legacy

**Enunciado**

Un organismo dispone de una aplicación monolítica cliente-servidor de dos capas, desarrollada hace 15 años: un cliente pesado de escritorio (Visual Basic/PowerBuilder) que se conecta **directamente** a una base de datos centralizada, sin capa intermedia. Gestiona expedientes de subvenciones y padece: imposibilidad de acceso desde web o móvil, despliegues que exigen actualizar manualmente cientos de puestos, y fuerte acoplamiento entre lógica de negocio y acceso a datos. Se pide proponer una arquitectura objetivo y una estrategia de migración.

---

**Resolución**

**1. Diagnóstico de la arquitectura actual**

Arquitectura cliente-servidor de **2 capas** (*fat client*): el cliente contiene tanto presentación como parte de la lógica de negocio, y accede a la BD mediante conexión directa (ODBC/driver nativo). Problemas típicos: baja escalabilidad (cada cliente abre su propia conexión persistente a BD), imposibilidad de reutilizar la lógica desde otros canales, despliegue costoso, y seguridad débil (credenciales de BD en el propio cliente).

**2. Arquitectura objetivo propuesta**

Migración a una arquitectura de **N capas orientada a servicios**, evolucionando hacia microservicios de forma incremental:

```
[Web / App móvil / Cliente de escritorio modernizado]
                    │  HTTPS (REST/JSON)
            [API Gateway]
       (autenticación, rate limiting, enrutado)
                    │
   ┌────────────────┼─────────────────┐
[MS Expedientes] [MS Solicitantes] [MS Pagos/Tasas]
   │                 │                  │
[BD Expedientes] [BD Solicitantes]  [BD Pagos]
                    │
         [Bus de eventos / mensajería]
        (notificación de cambios de estado)
```

- **API Gateway**: punto único de entrada, gestiona autenticación (integrable con Cl@ve/OAuth2), *throttling* y enrutado a los microservicios correspondientes — evita que cada cliente conozca la topología interna.
- **Microservicios por dominio funcional** (no por capa técnica): `Expedientes`, `Solicitantes`, `Pagos`, siguiendo el principio de **responsabilidad única** y alineados con *bounded contexts* de DDD.
- **Base de datos por servicio**: cada microservicio es dueño de sus datos, evitando el acoplamiento actual de "todo el mundo consulta la misma BD" — la comunicación entre servicios se hace vía API, no vía BD compartida.
- **Comunicación asíncrona** (cola/bus de eventos, p. ej. cuando `Expedientes` cambia de estado, publica un evento que `Pagos` consume) para desacoplar temporalmente los servicios y mejorar resiliencia.

**3. Estrategia de migración: patrón *Strangler Fig***

No se plantea una reescritura completa "big bang" (alto riesgo, alto coste, sin valor visible hasta el final), sino una sustitución progresiva:

1. Colocar el **API Gateway/proxy** delante del sistema legacy sin tocar el monolito: todo el tráfico sigue yendo al sistema antiguo.
2. Extraer el primer módulo de menor riesgo y mayor valor (p. ej. `Solicitantes`, consulta de datos maestros) como microservicio nuevo, con su propia BD poblada mediante migración/sincronización desde la BD legacy.
3. El Gateway empieza a enrutar las peticiones de ese dominio al nuevo microservicio; el resto sigue en el monolito.
4. Repetir el proceso módulo a módulo (`Expedientes`, luego `Pagos`) hasta que el monolito quede "estrangulado" — sin funcionalidad propia — y pueda retirarse.
5. Durante la transición, mantener ambos sistemas sincronizados (doble escritura o *change data capture*) es el punto más delicado y donde se concentra el mayor riesgo del proyecto.

**4. Justificación frente a alternativas**

- Frente a mantener 2 capas: no resuelve ninguno de los problemas de acoplamiento ni habilita nuevos canales (web/móvil).
- Frente a un monolito modular en 3 capas (presentación-negocio-datos) sin llegar a microservicios: es una alternativa más conservadora, con menor coste y complejidad operativa (no requiere orquestación, *service discovery*, ni resolver transacciones distribuidas); **es la recomendación adecuada si el equipo es pequeño o no existe cultura DevOps**, y debe mencionarse como alternativa válida — microservicios no es la respuesta correcta en todos los supuestos, es una decisión de compromiso entre escalabilidad/autonomía de equipos y complejidad operativa añadida.
- Se elige microservicios en este enunciado porque el objetivo explícito es habilitar múltiples canales de acceso concurrente (web, móvil, escritorio) con evolución independiente de cada dominio, lo que justifica la mayor complejidad operativa asumida.

---

# 2. Test de autoevaluación (25 preguntas)

**1.** En el modelo relacional, una relación está en Segunda Forma Normal (2FN) cuando:

a) No contiene grupos repetitivos.
b) Está en 1FN y todo atributo no clave depende funcionalmente de forma completa de la clave primaria (no hay dependencias parciales).
c) Está en 1FN y no existen dependencias transitivas entre atributos no clave.
d) Todos sus atributos son atómicos.

**2.** Dado el atributo `id_expediente → tipo_proc → plazo_dias`, si estos tres atributos conviven en una misma tabla con `id_expediente` como clave primaria simple, ¿qué se produce?

a) Una violación de la 1FN.
b) Una dependencia transitiva, que se corrige extrayendo `tipo_proc` y `plazo_dias` a una tabla aparte.
c) Una dependencia parcial, propia de tablas con clave compuesta.
d) No hay ningún problema de normalización porque la clave es simple.

**3.** Según la regla de Boyce-Codd (FNBC), una relación está correctamente normalizada cuando:

a) Toda dependencia funcional no trivial tiene como determinante una superclave.
b) Toda clave candidata es también clave foránea de otra tabla.
c) No existen más de dos claves candidatas por relación.
d) Todos los atributos son de tipo numérico o fecha.

**4.** ¿Cuál de las siguientes afirmaciones sobre lenguajes de programación **compilados** frente a **interpretados** es correcta?

a) Un lenguaje compilado siempre es más lento en ejecución que uno interpretado.
b) Java es puramente compilado a código máquina nativo, como C.
c) Un lenguaje compilado traduce el código fuente completo a código objeto/máquina antes de la ejecución; uno interpretado lo traduce y ejecuta instrucción a instrucción en tiempo de ejecución.
d) Python no puede compilarse nunca a bytecode intermedio.

**5.** En el paradigma de programación funcional, ¿qué caracteriza a una función **pura**?

a) Debe estar declarada como `static`.
b) Para las mismas entradas siempre devuelve la misma salida y no produce efectos secundarios observables.
c) Solo puede recibir un único parámetro.
d) No puede invocar a otras funciones.

**6.** Analiza el siguiente fragmento en Java:

```java
public class Contador {
    private static int total = 0;
    private int propio;

    public Contador() {
        propio = ++total;
    }
}
```

¿Qué representa el atributo `total`?

a) Un atributo de instancia, uno distinto por cada objeto `Contador`.
b) Un atributo de clase, compartido por todas las instancias de `Contador`.
c) Una constante que no puede modificarse tras la primera asignación.
d) Un atributo local al constructor, se destruye al finalizar cada llamada.

**7.** Respecto a los tipos de dato en SQL estándar, `DECIMAL(10,2)` es más adecuado que `FLOAT` para almacenar importes monetarios porque:

a) `FLOAT` ocupa más espacio en disco que `DECIMAL`.
b) `DECIMAL` es un tipo de precisión exacta (decimal fijo), mientras que `FLOAT` es de coma flotante binaria y puede introducir errores de redondeo.
c) `FLOAT` no admite números negativos.
d) No hay diferencia real entre ambos tipos en los motores relacionales actuales.

**8.** En SQL, la cláusula `HAVING` se diferencia de `WHERE` en que:

a) `HAVING` filtra filas antes de agrupar y `WHERE` después.
b) `WHERE` filtra filas individuales antes del `GROUP BY`; `HAVING` filtra sobre los resultados ya agregados, y admite funciones de agregación.
c) `HAVING` solo puede usarse con `INNER JOIN`.
d) Son intercambiables en cualquier consulta sin diferencia de comportamiento.

**9.** Un procedimiento almacenado que recibe un parámetro que se usa exclusivamente para **devolver** un valor al invocador debe declararse en PL/SQL (Oracle) como:

a) `IN`
b) `OUT`
c) `IN OUT`
d) `RETURN` (no existe como modo de parámetro)

**10.** Sobre los triggers `BEFORE` frente a `AFTER` en un motor relacional:

a) Un trigger `BEFORE` puede modificar los valores que se van a insertar/actualizar antes de que se graben; un `AFTER` actúa sobre datos ya persistidos, típico para auditoría.
b) `AFTER` siempre se ejecuta antes que `BEFORE` en el ciclo de vida de la sentencia.
c) Solo `BEFORE` puede lanzar excepciones que aborten la transacción.
d) No hay diferencia funcional entre ambos, solo de sintaxis.

**11.** ¿Cuál de los siguientes principios **NO** pertenece a SOLID?

a) Principio de responsabilidad única (SRP).
b) Principio de sustitución de Liskov (LSP).
c) Principio de la máxima cohesión estructurada (PMCE).
d) Principio de inversión de dependencias (DIP).

**12.** En el patrón de diseño **Singleton**, el objetivo principal es:

a) Permitir crear múltiples instancias de una clase de forma controlada.
b) Garantizar que una clase tenga una única instancia y proporcionar un punto de acceso global a ella.
c) Desacoplar la creación de objetos de su uso mediante una fábrica.
d) Notificar automáticamente a varios objetos cuando cambia el estado de otro.

**13.** El patrón **Observer** es el más adecuado para:

a) Definir una interfaz para crear familias de objetos relacionados sin especificar sus clases concretas.
b) Notificar a múltiples objetos suscriptores cuando cambia el estado de un objeto sujeto, sin acoplarlos fuertemente.
c) Encapsular una petición como un objeto, permitiendo parametrizar clientes con distintas peticiones.
d) Proveer una interfaz simplificada a un subsistema complejo.

**14.** En UML, un **diagrama de secuencia** se utiliza principalmente para:

a) Representar la estructura estática de clases y sus relaciones.
b) Mostrar la interacción entre objetos ordenada en el tiempo, mediante el intercambio de mensajes.
c) Modelar los estados posibles de un objeto y las transiciones entre ellos.
d) Representar los casos de uso del sistema y los actores que interactúan con él.

**15.** En un diagrama de clases UML, una línea con un rombo **relleno** (negro) en un extremo representa:

a) Herencia (generalización).
b) Asociación simple.
c) Composición: la parte no puede existir sin el todo, y su ciclo de vida está ligado a él.
d) Dependencia.

**16.** En Java EE / Jakarta EE, la anotación `@Stateless` aplicada a un EJB indica que:

a) El bean mantiene el estado de la conversación de un cliente concreto entre llamadas.
b) El bean no conserva estado conversacional entre invocaciones y el contenedor puede reutilizar sus instancias entre distintos clientes mediante *pooling*.
c) El bean se instancia una única vez para toda la aplicación, como un Singleton.
d) El bean gestiona directamente las transacciones sin intervención del contenedor.

**17.** En el ecosistema .NET, **Entity Framework** se clasifica como:

a) Un servidor de aplicaciones.
b) Un framework de mapeo objeto-relacional (ORM) para acceso a datos.
c) Un motor de plantillas para generación de vistas HTML.
d) Un contenedor de inyección de dependencias.

**18.** Respecto a la arquitectura cliente-servidor de **3 capas** (presentación, negocio, datos):

a) El cliente accede directamente a la base de datos sin intermediarios.
b) La capa de presentación nunca puede ejecutarse en un navegador web.
c) La capa de negocio encapsula las reglas y procesos del dominio, desacoplando la presentación del acceso a datos, lo que facilita reutilizar la lógica desde distintos clientes.
d) Es equivalente en todo a una arquitectura de microservicios.

**19.** ¿Qué diferencia principal existe entre un servicio **REST** y uno **SOAP** respecto al formato de contrato?

a) REST exige siempre un contrato WSDL; SOAP no tiene contrato formal.
b) SOAP describe su contrato mediante WSDL con tipado XSD estricto; REST se describe habitualmente con especificaciones como OpenAPI, de forma más flexible.
c) Ambos usan exclusivamente XML como formato de intercambio, sin excepción.
d) REST no puede exponerse sobre HTTP.

**20.** En el protocolo HTTP, si un cliente envía `PUT /expedientes/45` con un cuerpo JSON completo del recurso, la semántica REST esperada es:

a) Crear un nuevo recurso con un identificador autogenerado por el servidor.
b) Reemplazar por completo el recurso identificado por `45` con los datos enviados (operación idempotente).
c) Eliminar el recurso `45`.
d) Aplicar una modificación parcial únicamente de los campos enviados.

**21.** En HTML5, ¿cuál de las siguientes etiquetas es semánticamente correcta para marcar el contenido principal y único de una página?

a) `<div id="main">`
b) `<main>`
c) `<section class="main">`
d) `<content>`

**22.** En XML, un documento se considera **bien formado** (*well-formed*) cuando:

a) Valida contra un esquema XSD específico.
b) Cumple las reglas sintácticas básicas: un único elemento raíz, etiquetas correctamente anidadas y cerradas, atributos entrecomillados.
c) No contiene espacios de nombres (namespaces).
d) Todos sus elementos son opcionales según el DTD.

**23.** Según las Pautas de Accesibilidad para el Contenido Web (WCAG 2.1), el atributo `alt` de una imagen meramente decorativa debe:

a) Contener una descripción larga y detallada de la imagen.
b) Dejarse vacío (`alt=""`) para que los lectores de pantalla la omitan, en lugar de eliminarlo u omitir el atributo.
c) Omitirse por completo, sin incluir el atributo `alt`.
d) Contener siempre el nombre del archivo de la imagen.

**24.** Frente a una vulnerabilidad de **inyección SQL**, la medida de prevención más eficaz en el código de acceso a datos es:

a) Escapar manualmente las comillas simples en las cadenas recibidas del usuario.
b) Usar siempre `EXEC` de sentencias dinámicas construidas por concatenación de cadenas.
c) Utilizar consultas parametrizadas o procedimientos almacenados con parámetros tipados, de forma que el valor del usuario nunca se interprete como código SQL.
d) Validar únicamente en el cliente (JavaScript) que el campo no contenga la palabra `SELECT`.

**25.** En Git, ¿qué diferencia existe entre `git merge` y `git rebase` al integrar una rama de funcionalidad sobre `main`?

a) Son estrictamente equivalentes y generan el mismo historial de commits.
b) `git merge` crea (normalmente) un commit de fusión y conserva el historial real de ambas ramas; `git rebase` reescribe los commits de la rama de origen aplicándolos secuencialmente sobre el destino, produciendo un historial lineal.
c) `git rebase` nunca debe usarse sobre ramas ya publicadas y compartidas, mientras que `git merge` está prohibido en cualquier circunstancia.
d) `git merge` elimina automáticamente la rama de origen tras la fusión.

---

### Soluciones

**1. b)** — La 2FN exige 1FN + ausencia de dependencias parciales (atributos que dependan solo de una parte de una clave compuesta). Esto solo tiene sentido cuando la clave primaria es compuesta.

**2. b)** — `id_expediente` (clave) determina `tipo_proc`, y `tipo_proc` determina `plazo_dias`: es una dependencia transitiva clásica (X→Y→Z), que viola 3FN aunque la tabla ya esté en 2FN (al ser clave simple, no puede haber dependencias parciales).

**3. a)** — FNBC es una versión más estricta de 3FN: para toda dependencia funcional no trivial `X→Y`, `X` debe ser superclave. Resuelve casos de 3FN con claves candidatas solapadas que 3FN no cubre.

**4. c)** — Es la definición correcta y neutra. (b) es falsa: Java compila a bytecode, que se interpreta/JIT-compila en la JVM, no a código máquina nativo directamente.

**5. b)** — Ausencia de efectos secundarios y determinismo (mismo input → mismo output) son las dos propiedades que definen la pureza funcional.

**6. b)** — `static` en Java asocia el atributo a la clase, no a cada instancia; todas las instancias comparten la misma variable `total`, por eso sirve como contador global de objetos creados.

**7. b)** — `FLOAT`/`REAL` son de coma flotante binaria (IEEE 754) y no pueden representar exactamente muchos decimales (p. ej. 0.1), lo que es inaceptable en importes económicos; `DECIMAL`/`NUMERIC` almacenan el valor exacto con precisión y escala fijas.

**8. b)** — Orden lógico de ejecución en SQL: `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY`. `WHERE` no puede usar funciones agregadas porque en ese punto aún no existen los grupos.

**9. b)** — `OUT` es el modo correcto para un parámetro que solo transporta información de salida; `IN` es solo entrada, `IN OUT` es entrada y salida simultáneamente.

**10. a)** — `BEFORE` permite interceptar/corregir/rechazar los valores antes del cambio físico (p. ej. `:NEW.campo := ...` en Oracle); `AFTER` ve datos ya confirmados en la tabla, apropiado para registrar auditoría (como el caso práctico E, que usa `AFTER UPDATE, DELETE`).

**11. c)** — "Principio de la máxima cohesión estructurada" no es uno de los cinco principios SOLID (SRP, OCP, LSP, ISP, DIP); es un distractor inventado.

**12. b)** — Definición canónica del patrón Singleton (patrón creacional).

**13. b)** — Observer (patrón de comportamiento) desacopla un sujeto observable de sus observadores, que se suscriben/notifican sin conocerse fuertemente entre sí.

**14. b)** — El diagrama de secuencia es un diagrama de **interacción**: eje vertical de tiempo, líneas de vida de los objetos y mensajes intercambiados entre ellos.

**15. c)** — El rombo relleno indica **composición** (agregación fuerte, ciclo de vida compartido); el rombo hueco indica agregación simple (la parte puede sobrevivir al todo).

**16. b)** — `@Stateless` marca un *Session Bean* sin estado de conversación; el contenedor EJB gestiona un *pool* de instancias intercambiables entre clientes, mejorando la escalabilidad frente a `@Stateful`.

**17. b)** — Entity Framework es el ORM oficial de .NET para mapear objetos a tablas relacionales (equivalente conceptual a Hibernate/JPA en Java).

**18. c)** — Es la ventaja central de las 3 capas: aislar las reglas de negocio en una capa intermedia reutilizable desde múltiples clientes (web, escritorio, móvil), frente al acoplamiento directo cliente-BD de 2 capas visto en el caso práctico F.

**19. b)** — SOAP tiene un contrato formal obligatorio (WSDL/XSD); REST no exige un formato de contrato único, aunque en la práctica se documenta con OpenAPI/Swagger de forma más laxa.

**20. b)** — Semántica HTTP estándar: `PUT` reemplaza el recurso completo en la URI indicada y es idempotente (repetir la petición produce el mismo estado final); la modificación parcial correspondería a `PATCH`, y la creación con ID autogenerado a `POST`.

**21. b)** — `<main>` es el elemento semántico de HTML5 destinado exclusivamente al contenido principal y único de la página, mejorando accesibilidad y SEO frente a un `<div>` genérico.

**22. b)** — "Bien formado" es una propiedad puramente sintáctica (independiente de validar contra un esquema): raíz única, anidamiento correcto, atributos entre comillas. "Válido" es un concepto distinto que sí exige conformidad con un DTD/XSD.

**23. b)** — WCAG recomienda `alt=""` (vacío pero presente) en imágenes puramente decorativas, para que la tecnología de asistencia las ignore sin interrumpir la lectura; omitir el atributo por completo es peor porque algunos lectores de pantalla anuncian el nombre del archivo.

**24. c)** — Las consultas parametrizadas/procedimientos con parámetros tipados separan estructuralmente código y datos, de forma que el motor nunca interpreta el valor del usuario como parte de la sentencia SQL — es la defensa recomendada frente a la inyección SQL, consistente con el uso de `?`/parámetros con nombre visto en el caso práctico B.

**25. b)** — Diferencia clave para el examen: `merge` preserva la historia real (incluye un commit de fusión con dos padres); `rebase` reescribe commits (nuevos hashes) para lograr un historial lineal, por lo que no debe aplicarse sobre commits ya compartidos con otros.
