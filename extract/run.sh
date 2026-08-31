#!/usr/bin/env bash
# Render a PDF to per-page PNGs inside Docker.
#
# Usage:
#   bash run.sh PDF OUTPUT_DIR [extract_pages.py options...]
#
# Examples:
#   bash run.sh ../tong-lecture_notes.pdf ./pages
#   bash run.sh "../Dyson - Advanced QM.pdf" ./dyson_pages --pages 1-12
#   bash run.sh notes.pdf ./out --dpi 250 --force

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="${EXTRACT_IMAGE:-qft-extract-pages}"

usage() {
  cat <<EOF
Usage: $(basename "$0") PDF OUTPUT_DIR [extract_pages.py options...]

Render a PDF to per-page PNG images using Docker.
Dependencies are installed in the image; nothing is installed on the host
beyond Docker itself.

Arguments:
  PDF          Path to the PDF on the host
  OUTPUT_DIR   Folder for page images (created if missing)
  options      Passed through to extract_pages.py
               (--pages, --dpi, --force)

Examples:
  bash $(basename "$0") ../tong-lecture_notes.pdf ./pages
  bash $(basename "$0") "../Dyson - Advanced QM.pdf" ./dyson_pages --pages 1-12
  bash $(basename "$0") notes.pdf ./out --dpi 250 --force
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -lt 2 ]]; then
  usage >&2
  exit 1
fi

PDF="$1"
OUT="$2"
shift 2

if ! command -v docker >/dev/null 2>&1; then
  echo "error: docker is not installed or not on PATH" >&2
  exit 1
fi

if [[ ! -f "$PDF" ]]; then
  echo "error: PDF not found: $PDF" >&2
  exit 1
fi

resolve_file() {
  local dir base
  dir="$(cd "$(dirname -- "$1")" && pwd)"
  base="$(basename -- "$1")"
  printf '%s/%s\n' "$dir" "$base"
}

PDF_ABS="$(resolve_file "$PDF")"
mkdir -p -- "$OUT"
OUT_ABS="$(cd -- "$OUT" && pwd)"

echo "building image ${IMAGE_NAME} (cached if unchanged)..."
docker build -t "$IMAGE_NAME" "$SCRIPT_DIR"

run_args=(--rm)
if [[ -t 1 ]]; then
  run_args+=(-t)
fi

# Write files as the invoking user so the host output dir is not root-owned.
run_args+=(-u "$(id -u):$(id -g)")

docker run "${run_args[@]}" \
  -v "$PDF_ABS:/input/document.pdf:ro" \
  -v "$OUT_ABS:/output" \
  "$IMAGE_NAME" \
  /input/document.pdf -o /output "$@"
