#!/bin/bash
# Palette Toolkit - Package Builder
# Creates shareable ZIP with all current updates

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_NAME="palette-toolkit-v1.0.zip"
OUTPUT_PATH="$SCRIPT_DIR/$PACKAGE_NAME"

echo "🎨 Building Palette Toolkit Package..."
echo ""

# Remove old package if exists
if [ -f "$OUTPUT_PATH" ]; then
    echo "📦 Removing old package..."
    rm "$OUTPUT_PATH"
fi

# Create new package
echo "📦 Creating package..."
cd "$SCRIPT_DIR"
zip -r "$PACKAGE_NAME" palette/ \
    -x "palette/.git/*" \
    -x "palette/garbage_collection/*" \
    -x "palette/kgdrs/*" \
    -q

# Get package size
PACKAGE_SIZE=$(ls -lh "$PACKAGE_NAME" | awk '{print $5}')

echo ""
echo "✅ Package created successfully!"
echo ""
echo "📊 Package Details:"
echo "   File: $PACKAGE_NAME"
echo "   Size: $PACKAGE_SIZE"
echo "   Location: $OUTPUT_PATH"
echo ""
echo "📋 Contents:"
echo "   ✓ 7 agents (Argy, Rex, Theri, Raptor, Yuty, Anky, Para)"
echo "   ✓ Taxonomy v1.2 (104 RIUs)"
echo "   ✓ Knowledge library v1.2 (86 questions)"
echo "   ✓ Three-tier system"
echo "   ✓ Demo guide + Quick start + Install guide"
echo ""
echo "🚀 Ready to share!"
echo ""
echo "To test the package:"
echo "   1. Extract: unzip $PACKAGE_NAME"
echo "   2. Open: cd palette/"
echo "   3. Read: cat INSTALL_PALETTE.md"
echo ""
