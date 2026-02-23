# Renders comparison.md to PDF
# Usage: bash chi_ed/reports/render.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/../../outputs/reports"

mkdir -p "$OUTPUT_DIR"

pandoc "$SCRIPT_DIR/comparison.md" \
    --resource-path="$SCRIPT_DIR" \
    -o "$OUTPUT_DIR/comparison.pdf"

echo "Rendered to $OUTPUT_DIR/comparison.pdf"
