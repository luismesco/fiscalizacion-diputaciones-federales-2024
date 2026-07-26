#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
CHROME_BIN="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUTPUT_PDF="$REPO_DIR/reporte_observaciones_pef_2023_2024.pdf"

"$CHROME_BIN" \
  --headless \
  --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf="$OUTPUT_PDF" \
  "file://$REPO_DIR/index.html"

printf '%s\n' "PDF generado: $OUTPUT_PDF"
