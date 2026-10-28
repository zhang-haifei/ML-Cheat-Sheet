#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ -f /workspace/setup/latex-env.sh ]]; then
  source /workspace/setup/latex-env.sh
fi
target="${1:-main}"
case "$target" in main|batch[0-9][0-9]) ;; *) echo 'Usage: scripts/build.sh [main|batchNN]' >&2; exit 2;; esac
[[ -f "$target.tex" ]] || { echo "Missing entry: $target.tex" >&2; exit 2; }
mkdir -p build
latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build "$target.tex"
