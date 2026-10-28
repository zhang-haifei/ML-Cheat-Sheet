#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ -f /workspace/setup/latex-env.sh ]]; then
  source /workspace/setup/latex-env.sh
fi
target="${1:-main}"
case "$target" in main|batch01|batch02) ;; *) echo 'Usage: scripts/build.sh [main|batch01|batch02]' >&2; exit 2;; esac
mkdir -p build
latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build "$target.tex"
