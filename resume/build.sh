#!/usr/bin/env bash
# Rebuild the resume PDF from resume/sriram.yaml with RenderCV, then check it
# with tools/check_resume_pdf.py.
#
#   ./resume/build.sh                      build and check
#   ./resume/build.sh --jd path/to/jd.md   also report keyword coverage for a job
#
# Environment:
#   PYTHON   Python used for RenderCV and the checker (default: python3).
#            RenderCV needs Python 3.12+.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$HERE")"
PDF_NAME="Damotharan-Sriram-Product-Designer.pdf"
PY="${PYTHON:-python3}"

# 1. Find RenderCV: the CLI, an importable module, or a one-off uvx run.
if command -v rendercv >/dev/null 2>&1; then
  RCV=(rendercv)
elif "$PY" -c "import rendercv" >/dev/null 2>&1; then
  RCV=("$PY" -m rendercv)
elif command -v uvx >/dev/null 2>&1; then
  RCV=(uvx --from "rendercv[full]" rendercv)
else
  echo "RenderCV not found. Install it with one of:" >&2
  echo "  uv tool install 'rendercv[full]'" >&2
  echo "  pipx install 'rendercv[full]'" >&2
  echo "  python3.12 -m pip install 'rendercv[full]'" >&2
  exit 1
fi

# 2. Render. Output paths are set in sriram.yaml; the flags repeat them so the
#    filename never falls back to RenderCV's default.
cd "$HERE"
"${RCV[@]}" render sriram.yaml \
  --pdf-path "$PDF_NAME" \
  --dont-generate-markdown --dont-generate-html --dont-generate-png \
  --quiet
echo "Built resume/$PDF_NAME"

# 3. Check it. A FAIL stops the build; a WARN does not.
if "$PY" -c "import pypdf" >/dev/null 2>&1; then
  CHECK=("$PY")
elif command -v uv >/dev/null 2>&1; then
  CHECK=(uv run --no-project --with pypdf --with pdfplumber python)
else
  echo "pypdf not installed, skipping the check (python3 -m pip install pypdf)." >&2
  exit 0
fi

status=0
"${CHECK[@]}" "$ROOT/tools/check_resume_pdf.py" "$HERE/$PDF_NAME" "$@" || status=$?
if [ "$status" -ge 2 ]; then
  echo "Resume check failed (exit $status)." >&2
  exit "$status"
fi
