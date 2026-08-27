# Oposición Informática — Plan y seguimiento

Repositorio de trabajo para preparar oposiciones de informática al sector público, con foco en dos procesos compatibles con titulación de **Grado Superior (FP)**:

- **TAI** — Cuerpo de Técnicos Auxiliares de Informática de la Administración del Estado (AGE, grupo C1)
- **Técnico Especialista, Opción Informática** — Comunidad Autónoma de la Región de Murcia (CARM, grupo C1)

## 📖 Página de estudio

**https://jmpastor2.github.io/oposicion-informatica/**

Los 74 temas completos (TAI + Murcia) en una sola página: índice lateral, buscador, progreso por tema guardado en el navegador, tema claro/oscuro. Se genera con [scripts/build_legajo.py](scripts/build_legajo.py) a partir de `teoria/` — si editas el temario, vuelve a ejecutar el script y haz push de `index.html`.

## Contenido

| Archivo | Qué contiene |
|---|---|
| [temario_TAI.md](temario_TAI.md) | Temario oficial TAI (33 temas, 4 bloques) + referencia BOE |
| [temario_murcia.md](temario_murcia.md) | Temario Técnico Especialista Informática CARM + referencia BORM |
| [plan_estudio.md](plan_estudio.md) | Plan de estudio semanal, sin depender de fecha de examen |
| [examenes_y_plantillas.md](examenes_y_plantillas.md) | Exámenes oficiales de convocatorias anteriores y plantillas de respuestas (INAP) |
| [enlaces_oficiales.md](enlaces_oficiales.md) | Todos los enlaces oficiales de vigilancia (BOE, INAP, CARM, BORM) |
| [inscripcion_checklist.md](inscripcion_checklist.md) | Qué tener listo (Cl@ve, documentación, tasa) para inscribirse en cuanto salga la convocatoria |

### Teoría desarrollada (temario completo, no solo índice)

| Carpeta | Contenido |
|---|---|
| [teoria/TAI/bloque1_organizacion_estado.md](teoria/TAI/bloque1_organizacion_estado.md) | 9 temas: Constitución, Cortes, Gobierno, TREBEP, igualdad, administración electrónica |
| [teoria/TAI/bloque2_tecnologia_basica.md](teoria/TAI/bloque2_tecnologia_basica.md) | 5 temas: arquitectura de ordenadores, periféricos, estructuras de datos, SO, SGBD |
| [teoria/TAI/bloque3_desarrollo_sistemas.md](teoria/TAI/bloque3_desarrollo_sistemas.md) | 9 temas: modelado de datos, programación, SQL, POO, Java EE/.NET, web, UML, Git |
| [teoria/TAI/bloque4_sistemas_comunicaciones.md](teoria/TAI/bloque4_sistemas_comunicaciones.md) | 10 temas: administración de sistemas, backup, redes, TCP/IP, seguridad, CPD |
| [teoria/Murcia/materias_comunes.md](teoria/Murcia/materias_comunes.md) | 12 temas comunes a todos los Técnicos Especialistas de la CARM |
| [teoria/Murcia/materias_especificas_1_15.md](teoria/Murcia/materias_especificas_1_15.md) | Temas 1-15: Linux, Windows Server, correo, Windows 10, redes |
| [teoria/Murcia/materias_especificas_16_29.md](teoria/Murcia/materias_especificas_16_29.md) | Temas 16-29: ITIL/PRINCE2/Scrum, POO/UML, Oracle/PL-SQL, web, RGPD, ENS |

Contenido original redactado a partir de los programas oficiales (BOE/BORM) y normativa vigente citada por artículo — no copiado de apuntes de academias. Bloques III y IV de TAI llevan ejemplos de código (SQL, Java, C#) porque son los que entran en el supuesto práctico del examen.

## Situación de partida (agosto 2026)

**TAI (AGE)**: última convocatoria resuelta (Resolución 18-dic-2025, BOE-A-2025-26262, 1.030 plazas libre + 340 promoción interna, examen 23-mayo-2026) ya en fase de corrección/resultados — nada que solicitar ahí.

**Próxima convocatoria TAI**: la OEP 2026 (RD 387/2026, BOE 7-mayo-2026) ya aprobó **1.120 plazas específicas para TAI** (1.000 libre = 920 general + 80 discapacidad, más 120 promoción interna), dentro del total de ~1.700 plazas TIC (A1+A2+C1) de esa oferta. La convocatoria concreta (bases, plazos, examen) **todavía no se ha publicado** — por ley debe salir en el BOE antes del 31-dic-2026, con examen probable en 2027. **No hay nada que solicitar ahora**: toca vigilar BOE/INAP en los próximos meses, previsiblemente Q4 2026.

**Murcia**: última convocatoria BORM 13-feb-2024, solo 2 plazas, proceso resuelto en noviembre 2024. Sin convocatoria abierta ni anunciada actualmente — se vigila igual que TAI.

## Vigilancia automática

Hay una rutina cloud programada que revisa semanalmente (lunes 9:00 Madrid) el estado de ambas oposiciones contra las páginas oficiales de INAP, BOE, administracion.gob.es y CARM, y reporta si hay novedades (publicación de convocatoria, cambio de fase, resultados). Panel: https://claude.ai/code/routines/trig_01UsApC89BaLdEJibeqrjNZc

Si la rutina desaparece del panel (ha pasado ya una vez sin explicación clara), avisa para recrearla — el script de creación está documentado en esta conversación.

## Requisito de titulación (ya cumplido)

Grado Superior de FP cumple el requisito de acceso en ambos procesos (piden Bachillerato/FP2/Técnico Superior o equivalente, grupo C1). **No** cumple el requisito de GSI (A2) ni Cuerpo Superior TIC (A1) en la AGE, que exigen titulación universitaria — esos quedan descartados salvo promoción interna futura tras años como funcionario C1.

