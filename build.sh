#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 scripts/build_demo.py
python3 scripts/verify_demo.py

chromium --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=demo/redacted.pdf \
  "file://$PWD/out/redacted.html" 2>/dev/null

mkdir -p out/preview

MARP="marp"
if ! command -v marp >/dev/null 2>&1; then
  MARP="npx marp"
fi

"$MARP" deck.md --html --theme-set theme.css --pdf -o out/verixcel.pdf
"$MARP" deck.md --html --theme-set theme.css --pptx -o out/verixcel.pptx
"$MARP" deck.md --html --theme-set theme.css --images png --image-scale 1 -o out/preview/verixcel.png

echo "OK: out/verixcel.pdf, out/verixcel.pptx, demo/*"