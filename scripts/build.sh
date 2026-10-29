#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ -f /workspace/setup/latex-env.sh ]]; then
  source /workspace/setup/latex-env.sh
fi
target="${1:-main}"
[[ "$target" == main ]] || { echo 'Usage: scripts/build.sh [main]' >&2; exit 2; }
[[ -f "$target.tex" ]] || { echo "Missing entry: $target.tex" >&2; exit 2; }
mkdir -p build
latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build "$target.tex"
