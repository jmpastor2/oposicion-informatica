# TAI — Bloque III: Desarrollo de sistemas

> Bloque de alto peso en el examen: entra en el test general Y es uno de los dos supuestos prácticos posibles (junto al Bloque IV).

## Tema 1. Modelado de datos, metodologías y reglas. Entidades, atributos y relaciones. Diseño de bases de datos. Diseño lógico y físico. El modelo lógico relacional. Normalización.

El modelado de datos es el proceso de representar la información de un dominio de forma abstracta para su posterior implementación en un sistema de bases de datos. Se desarrolla habitualmente en tres niveles: **conceptual**, **lógico** y **físico**.

**Nivel conceptual.** Se emplea el modelo Entidad-Relación (E/R) de Chen, ampliado posteriormente con notación Peter Chen o Crow's Foot. Sus elementos básicos son:

- **Entidad**: objeto del mundo real con existencia independiente (EMPLEADO, DEPARTAMENTO).
- **Atributo**: propiedad de una entidad (simple, compuesto, monovaluado, multivaluado, derivado).
- **Relación**: asociación entre entidades, con cardinalidad (1:1, 1:N, N:M) y grado (binaria, ternaria).
- **Clave primaria**: atributo o conjunto de atributos que identifica de forma única cada instancia.

**Diseño lógico.** Se transforma el modelo E/R en un esquema relacional siguiendo reglas de paso:
- Entidad fuerte → tabla con su clave primaria.
- Relación 1:N → la clave primaria del lado "1" se propaga como clave ajena en el lado "N".
- Relación N:M → se crea una tabla intermedia con ambas claves ajenas, que normalmente forman la clave primaria compuesta.
- Atributo multivaluado → tabla independiente relacionada por clave ajena.

**Diseño físico.** Consiste en decidir la implementación concreta: tipos de datos del SGBD, índices, particionado, espacios de tablas, estrategias de almacenamiento y parámetros de rendimiento (tablespaces en Oracle, filegroups en SQL Server).

### El modelo relacional

Propuesto por E.F. Codd (1970), se basa en el álgebra relacional y la lógica de predicados. Una **relación** (tabla) es un conjunto de tuplas (filas) sobre un conjunto de atributos (columnas), cada uno con un dominio. Reglas fundamentales:

- Cada tabla tiene una clave primaria (PK) que garantiza la integridad de entidad (no nulos, no duplicados).
- Las claves ajenas (FK) garantizan la integridad referencial.
- Las restricciones de dominio (CHECK, NOT NULL) garantizan la integridad de dominio.

```sql
CREATE TABLE DEPARTAMENTO (
    id_dept     INT PRIMARY KEY,
    nombre      VARCHAR(50) NOT NULL
);

CREATE TABLE EMPLEADO (
    id_emp      INT PRIMARY KEY,
    nombre      VARCHAR(50) NOT NULL,
    salario     DECIMAL(10,2) CHECK (salario > 0),
    id_dept     INT,
    CONSTRAINT fk_dept FOREIGN KEY (id_dept)
        REFERENCES DEPARTAMENTO(id_dept)
);
```

### Normalización

La normalización es un proceso de descomposición de tablas para eliminar redundancias y anomalías de inserción, actualización y borrado, basado en dependencias funcionales.

**Primera Forma Normal (1FN):** todos los atributos deben ser atómicos (indivisibles) y no debe haber grupos repetitivos.

```
NO 1FN:  Pedido(id, cliente, productos="lápiz,goma,folio")
1FN:     PedidoLinea(id_pedido, producto)
```

**Segunda Forma Normal (2FN):** debe estar en 1FN y todo atributo no clave debe depender funcionalmente de la clave primaria **completa** (elimina dependencias parciales, aplicable con claves compuestas).

```
NO 2FN: LineaPedido(id_pedido, id_producto, cant, nombre_producto)
        -- nombre_producto depende solo de id_producto, no de la clave completa
2FN:    LineaPedido(id_pedido, id_producto, cant)
        Producto(id_producto, nombre_producto)
```

**Tercera Forma Normal (3FN):** debe estar en 2FN y ningún atributo no clave debe depender de otro atributo no clave (elimina dependencias transitivas).

```
NO 3FN: Empleado(id_emp, id_dept, nombre_dept)
        -- nombre_dept depende de id_dept, no de id_emp
3FN:    Empleado(id_emp, id_dept)
        Departamento(id_dept, nombre_dept)
```

Existen formas superiores (FNBC, 4FN, 5FN) que resuelven dependencias multivaluadas y de proyección-unión, aunque en la práctica profesional la 3FN o FNBC suele ser suficiente. En sistemas de alto rendimiento se aplica en ocasiones **desnormalización** controlada para reducir joins costosos, a cambio de asumir cierta redundancia gestionada.

### Metodologías de modelado

Las metodologías estructuradas (Métrica v3, en la Administración española) definen fases: Estudio de Viabilidad, Análisis, Diseño, Construcción, Implantación y Mantenimiento, con el modelo E/R como artefacto central del subproceso de Diseño de Datos. Métrica v3 distingue el **Diseño Lógico de Datos** (paso a tablas, normalización) del **Diseño Físico de Datos** (elección de estructuras de almacenamiento, índices).

## Tema 2. Lenguajes de programación. Representación de tipos de datos. Operadores. Instrucciones condicionales. Bucles y recursividad. Procedimientos, funciones y parámetros. Vectores y registros. Estructura de un programa.

### Clasificación de lenguajes

Los lenguajes de programación se clasifican por su nivel de abstracción (máquina, ensamblador, alto nivel), por su paradigma (imperativo, orientado a objetos, funcional, declarativo/lógico) y por su forma de ejecución (compilados: C, C++; interpretados: Python, JavaScript; híbridos con máquina virtual: Java, C#). Un **compilador** traduce todo el código fuente a código máquina antes de ejecutarlo; un **intérprete** traduce y ejecuta instrucción a instrucción; los lenguajes como Java compilan a bytecode intermedio ejecutado por una JVM.

### Tipos de datos

- **Primitivos/simples**: enteros (`int`, `long`), reales (`float`, `double`), carácter (`char`), booleano (`bool`), en coma flotante representados según IEEE 754.
- **Compuestos/estructurados**: cadenas, vectores (arrays), registros (struct), uniones, punteros/referencias.
- **Abstractos (TDA)**: pilas, colas, listas, árboles, definidos por su comportamiento, no por su representación interna.

### Operadores

- **Aritméticos**: `+ - * / % (módulo)`.
- **Relacionales**: `== != < > <= >=`.
- **Lógicos**: `AND OR NOT` (evaluación cortocircuito `&&`, `||`).
- **Asignación**: `= += -= *=`.
- **Bit a bit**: `& | ^ ~ << >>`.

### Estructuras de control

```
SI (edad >= 18) ENTONCES
    ESCRIBIR "Mayor de edad"
SINO
    ESCRIBIR "Menor de edad"
FIN SI

MIENTRAS (i < 10) HACER
    ESCRIBIR i
    i <- i + 1
FIN MIENTRAS

REPETIR
    ESCRIBIR i
    i <- i + 1
HASTA (i >= 10)

PARA i <- 1 HASTA 10 HACER
    ESCRIBIR i
FIN PARA
```

### Recursividad

Una función recursiva se llama a sí misma, requiriendo siempre un **caso base** (condición de parada) y un **caso recursivo**.

```java
int factorial(int n) {
    if (n <= 1) return 1;          // caso base
    return n * factorial(n - 1);   // caso recursivo
}
```

### Procedimientos, funciones y parámetros

Un **procedimiento** ejecuta una acción sin devolver valor; una **función** devuelve un valor. Los parámetros pueden pasarse **por valor** (se copia, no se modifica el original) o **por referencia** (se pasa la dirección de memoria, permitiendo modificar el original).

### Vectores y registros

```c
int notas[5] = {7, 8, 5, 9, 6};   // vector: homogéneo, indexado
struct Empleado {                  // registro: heterogéneo
    int id;
    char nombre[50];
    float salario;
};
```

### Estructura de un programa

Cabecera/importación de librerías, declaración de constantes y tipos, variables globales, subprogramas, bloque principal, organizado en paquetes/módulos para favorecer la modularidad.

## Tema 3. Lenguajes de interrogación de bases de datos. Estándar ANSI SQL. Procedimientos almacenados. Eventos y disparadores.

SQL (Structured Query Language) es el lenguaje estándar (ISO/IEC 9075, originalmente ANSI SQL-86) para la gestión de bases de datos relacionales, subdividido en:

**DDL** (define estructura): `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`, `CREATE INDEX`.

**DML** (manipula datos): `INSERT`, `UPDATE`, `DELETE`, `SELECT` con `JOIN` (INNER, LEFT, RIGHT, FULL), `GROUP BY`/`HAVING`, subconsultas y funciones de ventana (`OVER (PARTITION BY ...)`).

**DCL** (permisos y transacciones): `GRANT`, `REVOKE`, `BEGIN TRANSACTION` / `COMMIT` / `ROLLBACK`.

```sql
BEGIN TRANSACTION;
UPDATE CUENTA SET saldo = saldo - 100 WHERE id = 1;
UPDATE CUENTA SET saldo = saldo + 100 WHERE id = 2;
COMMIT;
```

Las transacciones cumplen ACID, con niveles de aislamiento (READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE).

**Procedimientos almacenados**: bloques compilados en el servidor (PL/SQL en Oracle, T-SQL en SQL Server) que encapsulan lógica de negocio.

```sql
CREATE PROCEDURE ActualizarSalario @id_emp INT, @porcentaje DECIMAL(5,2)
AS
BEGIN
    UPDATE EMPLEADO SET salario = salario * (1 + @porcentaje/100) WHERE id_emp = @id_emp;
END;
```

**Triggers**: se ejecutan automáticamente ante un evento DML/DDL, sin invocación explícita.

```sql
CREATE TRIGGER trg_AuditoriaSalario ON EMPLEADO AFTER UPDATE
AS
BEGIN
    IF UPDATE(salario)
        INSERT INTO AUDITORIA_SALARIO (id_emp, salario_anterior, fecha)
        SELECT d.id_emp, d.salario, GETDATE() FROM deleted d;
END;
```

Se clasifican por momento (`BEFORE`/`AFTER`/`INSTEAD OF`) y ámbito (por fila o por sentencia). Uso típico: auditoría, validación de reglas complejas, integridad referencial personalizada.

## Tema 4. Diseño y programación orientada a objetos. Elementos y componentes software: objetos, clases, herencia, métodos, sobrecarga. Ventajas e inconvenientes. Patrones de diseño y lenguaje de modelado unificado (UML).

### Fundamentos de la POO

La POO organiza el software en **objetos**, instancias de **clases**. Sus cuatro pilares: **encapsulamiento**, **abstracción**, **herencia** y **polimorfismo**.

```java
public abstract class Vehiculo {
    protected String matricula;
    protected int velocidad;
    public Vehiculo(String matricula) { this.matricula = matricula; }
    public abstract void acelerar();
    public void frenar() { velocidad = 0; }
}

public class Coche extends Vehiculo {          // herencia
    public Coche(String matricula) { super(matricula); }
    @Override
    public void acelerar() { velocidad += 20; }   // polimorfismo/sobreescritura
    public void acelerar(int incremento) { velocidad += incremento; }  // sobrecarga
}
```

La **sobrecarga (overloading)** define varios métodos con el mismo nombre y distinta firma, resuelta en compilación. La **sobreescritura (overriding)** redefine un método heredado, resuelta en ejecución.

**Ventajas**: reutilización, mantenibilidad, modelado natural, extensión sin modificar código existente. **Inconvenientes**: curva de aprendizaje, sobrecarga en tiempo de ejecución, riesgo de jerarquías mal diseñadas.

**Principios SOLID**: Responsabilidad única, Abierto/cerrado, Sustitución de Liskov, Segregación de interfaces, Inversión de dependencias.

**Patrones de diseño** (Gang of Four, 1994): creacionales (Singleton, Factory Method, Builder), estructurales (Adapter, Decorator, Facade), de comportamiento (Observer, Strategy, Command).

**UML**: diagrama de clases (atributos, métodos, relaciones: asociación, agregación ◇, composición ◆, herencia △), diagrama de casos de uso (actores, `<<include>>`/`<<extend>>`), diagrama de secuencia (interacción temporal entre objetos).

## Tema 5. Arquitectura Java EE/Jakarta EE y plataforma .NET: componentes, persistencia y seguridad. Características, elementos, lenguajes y funciones en ambos entornos. Desarrollo de interfaces.

### Jakarta EE (antes Java EE)

Conjunto de especificaciones sobre la JVM, ejecutado sobre servidor de aplicaciones (WildFly, GlassFish, WebSphere Liberty). Componentes: **Servlets**, **JSP/JSF**, **EJB** (lógica de negocio con soporte transaccional), **CDI** (inyección de dependencias), **JPA** (ORM, implementado por Hibernate), **JAX-RS/JAX-WS** (REST/SOAP).

```java
@Entity
public class Empleado {
    @Id @GeneratedValue private Long id;
    private String nombre;
}

@Path("/empleados")
public class EmpleadoResource {
    @GET @Path("/{id}")
    public Empleado obtener(@PathParam("id") Long id) { return entityManager.find(Empleado.class, id); }
}
```

Seguridad: Jakarta Security (`@RolesAllowed`), realms del servidor de aplicaciones.

### Plataforma .NET

Multiplataforma desde .NET 5. Lenguajes: C#, F#, VB.NET, compilados a CIL/MSIL ejecutado por el CLR (garbage collector, JIT). Componentes: **ASP.NET Core** (MVC, Web API), **Entity Framework Core** (ORM), **ASP.NET Core Identity** (autenticación).

```csharp
[ApiController][Route("api/[controller]")]
public class EmpleadosController : ControllerBase {
    [HttpGet("{id}")][Authorize(Roles = "Administrador")]
    public async Task<ActionResult<Empleado>> Obtener(int id) {
        var emp = await _context.Empleados.FindAsync(id);
        return emp is null ? NotFound() : Ok(emp);
    }
}
```

### Comparativa

| Aspecto | Java EE/Jakarta EE | .NET |
|---|---|---|
| ORM | JPA (Hibernate) | Entity Framework Core |
| DI | CDI | Contenedor DI integrado |
| Servidor | Externo (WildFly, Tomcat) | Kestrel embebido |

### Desarrollo de interfaces

Ambos entornos desacoplan presentación de backend: Java EE con JSF/PrimeFaces o frontend SPA (Angular/React) consumiendo REST; .NET con Razor Pages/Blazor o igualmente un frontend SPA independiente. Convergen en la arquitectura desacoplada backend-API / frontend-SPA.

## Tema 6. Arquitectura de sistemas cliente/servidor y multicapas: componentes y operación. Arquitecturas de servicios web y protocolos asociados.

### Cliente/servidor

- **2 capas**: cliente con presentación+negocio, acceso directo a BD. Acoplamiento fuerte.
- **3 capas**: separa presentación, lógica de negocio y datos.
- **N capas**: añade capas adicionales (servicios, integración, caché).

```
[Cliente/Navegador] --HTTP--> [Servidor de Aplicaciones] --SQL--> [Servidor de BD]
```

**SOA**: servicios débilmente acoplados coordinados por un bus (ESB). **Microservicios**: servicios pequeños y autónomos con BD propia, desplegados en contenedores (Docker/Kubernetes), comunicados vía REST o mensajería asíncrona (Kafka, RabbitMQ).

### Servicios web

**SOAP**: basado en XML, contrato formal en WSDL, catalogado en UDDI, soporta WS-Security y transacciones — usado en banca y Administración Pública.

```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
  <soap:Body><ObtenerEmpleado><id>5</id></ObtenerEmpleado></soap:Body>
</soap:Envelope>
```

**REST**: estilo arquitectónico (Roy Fielding), recursos por URI, verbos HTTP, sin estado, JSON.

```http
GET /api/empleados/5 HTTP/1.1
Accept: application/json
```

| Aspecto | SOAP | REST |
|---|---|---|
| Formato | XML estricto | JSON típico |
| Contrato | WSDL formal | OpenAPI/Swagger opcional |
| Estado | Puede ser stateful | Stateless |

Otros: GraphQL (consultas flexibles), gRPC (RPC sobre HTTP/2 con Protocol Buffers), AMQP/MQTT (mensajería asíncrona).

## Tema 7. Aplicaciones web. Desarrollo web front-end y en servidor, multiplataforma y multidispositivo. Lenguajes: HTML, XML y sus derivaciones. Navegadores y lenguajes de programación web. Lenguajes de script.

### Arquitectura de una aplicación web

**Front-end**: HTML, CSS, JavaScript ejecutados en el navegador. **Back-end/server-side**: Java, C#, PHP, Node.js, Python, responsable de lógica de negocio. Renderizado: SSR, CSR (SPA React/Angular/Vue), o híbrido (Next.js).

### HTML5

Etiquetas semánticas (`<header>`, `<nav>`, `<article>`), APIs nativas (Canvas, geolocalización, WebSockets), multimedia sin plugins (`<video>`, `<audio>`).

### XML y derivaciones

Metalenguaje jerárquico autodescriptivo. Tecnologías asociadas: **XSD** (esquemas), **XSLT** (transformación), **XPath** (navegación), **DTD**. Frente a XML, **JSON** es más ligero y de mapeo directo a estructuras de programación, aunque XML se mantiene donde se requiere validación estricta (SOAP, facturación electrónica, interoperabilidad Administración).

### Navegadores

Motores de renderizado: Blink (Chrome/Edge), Gecko (Firefox), WebKit (Safari). Motores JavaScript: V8, SpiderMonkey.

### Lenguajes de script y CSS

**JavaScript**: dinámico, débilmente tipado, basado en prototipos, bucle de eventos (`Promise`, `async/await`).

```javascript
async function obtenerEmpleado(id) {
    const respuesta = await fetch(`/api/empleados/${id}`);
    const datos = await respuesta.json();
}
```

**TypeScript**: tipado estático opcional sobre JavaScript. **CSS3**: Flexbox, Grid, media queries, base del diseño responsive.

### Multiplataforma y multidispositivo

Responsive design (mobile first) + frameworks CSS (Bootstrap, Tailwind). Para nativas/híbridas: React Native, Flutter, Ionic.

## Tema 8. Accesibilidad, diseño universal y usabilidad. Acceso y usabilidad de las tecnologías, productos y servicios relacionados con la sociedad de la información. Confidencialidad y disponibilidad de la información en puestos de usuario final. Conceptos de seguridad en el desarrollo de los sistemas.

### Accesibilidad y diseño universal

Garantiza que personas con discapacidad puedan percibir, entender, navegar e interactuar con un sistema. Normativa española: RDLeg 1/2013 y RD 1112/2018 (accesibilidad web y apps móviles del sector público).

### WCAG (POUR)

**Perceptible, Operable, Comprensible, Robusto.** Niveles A, AA (exigido por normativa), AAA.

```html
<img src="grafico.png" alt="Gráfico de ventas trimestrales 2025">
<label for="dni">DNI:</label>
<input type="text" id="dni" aria-required="true">
```

### Usabilidad

ISO 9241-11: eficacia, eficiencia y satisfacción. Heurísticas de Nielsen: visibilidad del estado, coherencia, prevención de errores.

### Confidencialidad y disponibilidad en el puesto de usuario final

Tríada **CID**: confidencialidad (cifrado de disco, bloqueo de sesión, MFA), integridad (firmas digitales, hash), disponibilidad (backups, SAI, redundancia). Marco normativo: **ENS** (RD 311/2022).

### Seguridad en el desarrollo (OWASP Top 10)

```sql
-- Vulnerable a inyección SQL
"SELECT * FROM usuarios WHERE nombre = '" + nombreUsuario + "'"
-- Correcto: parametrizada
SELECT * FROM usuarios WHERE nombre = @nombreUsuario;
```

Mitigaciones: consultas parametrizadas (SQLi), codificación de salida + CSP (XSS), tokens anti-CSRF, hash con sal bcrypt/PBKDF2 (contraseñas), JWT firmados con expiración, cookies `HttpOnly`/`Secure`/`SameSite`.

## Tema 9. Repositorios: estructura y actualización. Generación de código y documentación. Metodologías de desarrollo. Pruebas. Programas para control de versiones. Plataformas de desarrollo colaborativo de software.

### Control de versiones

**Centralizados** (SVN, CVS) vs **distribuidos** (Git). Git: commit, branch, merge, remote, pull/merge request.

```bash
git init
git add archivo.java
git commit -m "Añade validación de entrada"
git branch feature/login
git push origin feature/login
git merge feature/login
```

Estrategias: Git Flow (`main`/`develop`/`feature`/`release`/`hotfix`), GitHub Flow, Trunk-Based Development.

### Plataformas colaborativas

GitHub, GitLab, Bitbucket: issues, pull/merge requests, CI/CD (`.gitlab-ci.yml`, GitHub Actions), wikis, tableros Kanban.

### Generación de código y documentación

Herramientas CASE, scaffolding. Documentación desde comentarios estructurados: Javadoc, Doxygen, Swagger/OpenAPI.

### Metodologías de desarrollo

**Cascada**: fases secuenciales estrictas, sin retroceso. **Ágiles** (Manifiesto Ágil 2001): iterativo e incremental.
- **Scrum**: sprints, roles (Product Owner, Scrum Master, equipo), Product/Sprint Backlog, Daily/Planning/Review/Retrospectiva.
- **Kanban**: flujo continuo, límites WIP.
- **XP**: programación en parejas, integración continua, TDD.

### Pruebas de software

Pirámide de testing: unitarias (JUnit), integración, sistema, aceptación.

```java
@Test
void debeCalcularSalarioNetoCorrectamente() {
    Empleado emp = new Empleado(2000.0);
    assertEquals(1600.0, emp.calcularNeto(), 0.01);
}
```

**TDD**: ciclo red-green-refactor. **CI/CD**: integración y despliegue continuo automatizados en cada cambio.
