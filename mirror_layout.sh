#!/usr/bin/env bash
# Mirror an input directory tree into an output directory, turning every
# leaf file into a directory of the same name (including extension).
#
# Intermediate folders are recreated as folders. Empty folders are kept.
# Regular files become empty directories.
#
# Usage:
#   bash mirror_layout.sh INPUT_DIR OUTPUT_DIR
#
# Example:
#   bash mirror_layout.sh books extracted
#

set -euo pipefail

usage() {
  cat <<EOF
Usage: $(basename "$0") INPUT_DIR OUTPUT_DIR

Traverse INPUT_DIR and recreate the same folder tree under OUTPUT_DIR,
except that every leaf file becomes a directory of the same name.

Arguments:
  INPUT_DIR    Source tree to walk
  OUTPUT_DIR   Destination tree (created if missing)

Example:
  $(basename "$0") books extracted
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -ne 2 ]]; then
  usage >&2
  exit 1
fi

INPUT=$1
OUTPUT=$2

if [[ ! -d "$INPUT" ]]; then
  echo "error: input is not a directory: $INPUT" >&2
  exit 1
fi

# Resolve to absolute paths so we can cd freely.
INPUT_ABS=$(cd -- "$INPUT" && pwd)
mkdir -p -- "$OUTPUT"
OUTPUT_ABS=$(cd -- "$OUTPUT" && pwd)

if [[ "$INPUT_ABS" == "$OUTPUT_ABS" ]]; then
  echo "error: input and output directories must be different" >&2
  exit 1
fi

case "$OUTPUT_ABS" in
  "$INPUT_ABS"/*)
    echo "error: output directory must not be inside the input directory" >&2
    exit 1
    ;;
esac

# Snapshot paths first so a later mkdir cannot affect the walk.
tmp=$(mktemp)
trap 'rm -f -- "$tmp"' EXIT

# macOS / POSIX find: no -printf. Null-delimited for names with spaces/newlines.
(cd -- "$INPUT_ABS" && find . \( -type d -o -type f \) -print0) >"$tmp"

created=0
while IFS= read -r -d '' rel; do
  # Skip the input root itself; OUTPUT_ABS already exists.
  if [[ "$rel" == "." ]]; then
    continue
  fi
  dest="$OUTPUT_ABS/$rel"
  if [[ ! -d "$dest" ]]; then
    mkdir -p -- "$dest"
    created=$((created + 1))
  fi
done <"$tmp"

echo "mirrored $INPUT_ABS -> $OUTPUT_ABS"
echo "created $created directories"
