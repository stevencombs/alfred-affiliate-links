#!/bin/bash
# Build Affiliate.Links.alfredworkflow from workflow/.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/Affiliate.Links.alfredworkflow"

rm -f "$OUT"
(
  cd "$ROOT/workflow"
  zip -r -X "$OUT" info.plist icon.png search.py -x '*.DS_Store' -x '__MACOSX/*'
)
echo "Wrote $OUT"
