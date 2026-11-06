#!/usr/bin/env bash
# Обновляет локальное зеркало официальной REST-документации Битрикс24
# (репозиторий https://github.com/bitrix-tools/b24-rest-docs, лицензия MIT).
#
# Зачем: искать по документации через grep офлайн, а ссылки в
# docs/knowledge/*.md ведут на файлы зеркала.
#
# Что делает:
#   1. Клонирует репозиторий (depth 1) в НОВУЮ временную папку — скачанное
#      считается недоверенными данными, в проекте ничего оттуда не запускается.
#   2. Копирует в docs/knowledge/rest-docs/ только .md и toc/yaml (без картинок).
#   3. Пишет docs/knowledge/rest-docs/_SOURCE.txt (коммит и дата).
#   4. Пересобирает docs/knowledge/reference/methods-index.md.
#
# Зеркало (~40 МБ) НЕ коммитится: оно в .gitignore, восстанавливается этим скриптом.
#
# Использование: bash scripts/sync-rest-docs.sh
set -euo pipefail
cd "$(dirname "$0")/.."

DEST="docs/knowledge/rest-docs"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Клонирую b24-rest-docs во временную папку…"
git clone --depth 1 --quiet https://github.com/bitrix-tools/b24-rest-docs "$TMP/src"

COMMIT="$(git -C "$TMP/src" log -1 --format='%H')"
COMMIT_DATE="$(git -C "$TMP/src" log -1 --format='%cI')"

echo "Копирую .md и toc в $DEST …"
rm -rf "$DEST"
mkdir -p "$DEST"
( cd "$TMP/src" && find . -path ./.git -prune -o -type f \( -name '*.md' -o -name 'toc.yaml' -o -name 'b24-toc.yaml' -o -name 'index.yaml' \) -print0 \
    | tar --null -T - -cf - ) | tar -xf - -C "$DEST"
cp "$TMP/src/LICENSE" "$DEST/LICENSE"

cat > "$DEST/_SOURCE.txt" <<EOF
Источник: https://github.com/bitrix-tools/b24-rest-docs (MIT, © Bitrix)
Коммит:   $COMMIT
Дата коммита: $COMMIT_DATE
Синхронизировано: $(date -Is)
Картинки и ассеты не копируются — только текст.
EOF

echo "Файлов .md: $(find "$DEST" -name '*.md' | wc -l), размер: $(du -sh "$DEST" | cut -f1)"

if [ -f scripts/build-methods-index.py ]; then
  python3 -I scripts/build-methods-index.py "$DEST" docs/knowledge/reference/methods-index.md
fi
echo "Готово."
