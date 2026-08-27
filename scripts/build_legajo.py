"""
Genera legajo.html a partir de legajo_template.html + el temario en teoria/**/*.md.

Uso: python scripts/build_legajo.py
Requiere: pandoc en PATH.

Vuelve a ejecutar esto cada vez que se edite un fichero de teoria/ (nuevo tema,
correccion, temario actualizado tras nueva convocatoria) para regenerar el HTML.
"""
import re
import subprocess
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "teoria")
TEMPLATE = os.path.join(ROOT, "legajo_template.html")
OUT = os.path.join(ROOT, "index.html")

FILES = [
    ("TAI", "b1", "Bloque I — Organización del Estado y Administración electrónica", os.path.join(BASE, "TAI", "bloque1_organizacion_estado.md")),
    ("TAI", "b2", "Bloque II — Tecnología básica", os.path.join(BASE, "TAI", "bloque2_tecnologia_basica.md")),
    ("TAI", "b3", "Bloque III — Desarrollo de sistemas", os.path.join(BASE, "TAI", "bloque3_desarrollo_sistemas.md")),
    ("TAI", "b4", "Bloque IV — Sistemas y comunicaciones", os.path.join(BASE, "TAI", "bloque4_sistemas_comunicaciones.md")),
    ("MUR", "comunes", "Materias comunes", os.path.join(BASE, "Murcia", "materias_comunes.md")),
    ("MUR", "esp1", "Materias específicas (1-15)", os.path.join(BASE, "Murcia", "materias_especificas_1_15.md")),
    ("MUR", "esp2", "Materias específicas (16-29)", os.path.join(BASE, "Murcia", "materias_especificas_16_29.md")),
]


def split_temas(md_text):
    """Divide un fichero markdown en temas usando '# Tema N.' o '## Tema N.' como separador."""
    pattern = re.compile(r'^#{1,2}\s+Tema\s+(\d+)\.\s*(.*)$', re.MULTILINE)
    matches = list(pattern.finditer(md_text))
    temas = []
    for i, m in enumerate(matches):
        num = int(m.group(1))
        title = m.group(2).strip()
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md_text)
        body = md_text[start:end]
        body_wo_heading = body[m.end() - m.start():].strip()
        temas.append((num, title, body_wo_heading))
    return temas


def md_to_html(md_text):
    p = subprocess.run(
        ["pandoc", "-f", "gfm", "-t", "html", "--wrap=none"],
        input=md_text, capture_output=True, text=True, encoding="utf-8"
    )
    if p.returncode != 0:
        print("PANDOC ERROR:", p.stderr, file=sys.stderr)
        raise SystemExit(1)
    return p.stdout


def main():
    result = {"TAI": [], "MUR": []}
    counts = {}

    for group, key, title, path in FILES:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        temas = split_temas(text)
        rendered_temas = []
        for num, tema_title, body_md in temas:
            html = md_to_html(body_md)
            rendered_temas.append({"num": num, "title": tema_title, "html": html})
        counts[key] = len(rendered_temas)
        result[group].append({"key": key, "title": title, "temas": rendered_temas})

    total = sum(counts.values())
    print("Temas por bloque:", counts, file=sys.stderr)
    print("Total:", total, file=sys.stderr)

    data_text = json.dumps(result, ensure_ascii=False)
    data_text_safe = data_text.replace("</script", "<\\/script")

    with open(TEMPLATE, encoding="utf-8") as f:
        tpl = f.read()

    out = tpl.replace("__DATA_JSON__", data_text_safe)

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(out)

    print("Escrito:", OUT, "(", len(out.encode("utf-8")), "bytes )", file=sys.stderr)


if __name__ == "__main__":
    main()
