#!/usr/bin/env python3
"""Строит индекс страниц справочника REST из зеркала документации.

Использование: python3 -I scripts/build-methods-index.py <каталог-зеркала> <выходной-файл>

Для каждого .md в api-reference/ берёт заголовок первого уровня и путь.
Страницы-обзоры (index.md) отмечены жирным. Группировка — по разделам.
"""
import os
import re
import sys

mirror, out = sys.argv[1], sys.argv[2]
api = os.path.join(mirror, "api-reference")

sections = {}
for root, _dirs, files in os.walk(api):
    for name in files:
        if not name.endswith(".md"):
            continue
        path = os.path.join(root, name)
        rel = os.path.relpath(path, api)
        top = rel.split(os.sep)[0] if os.sep in rel else "(корень)"
        title = name
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if line.startswith("# "):
                    title = line[2:].strip()
                    break
        sections.setdefault(top, []).append((rel, title))

os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", encoding="utf-8") as fh:
    fh.write("# Индекс страниц справочника REST API\n\n")
    fh.write("Генерируется скриптом `scripts/build-methods-index.py` из зеркала "
             "`docs/knowledge/rest-docs/api-reference/`. Не править вручную.\n\n")
    total = sum(len(v) for v in sections.values())
    fh.write(f"Всего страниц: {total}. Пути — относительно `docs/knowledge/rest-docs/api-reference/`.\n\n")
    fh.write("Поиск нужного метода: `grep -i 'crm.deal' docs/knowledge/reference/methods-index.md`\n\n")
    for top in sorted(sections):
        items = sorted(sections[top], key=lambda x: (not x[0].endswith("index.md"), x[0]))
        fh.write(f"## {top} ({len(items)})\n\n")
        for rel, title in items:
            mark = "**" if rel.endswith("index.md") else ""
            fh.write(f"- {mark}{title}{mark} — `{rel}`\n")
        fh.write("\n")
print(f"Индекс: {total} страниц -> {out}")
