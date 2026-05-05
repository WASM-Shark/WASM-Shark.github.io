#!/bin/bash

set -e

echo "WASMShark Documentation Builder"
echo ""

# Install dependencies
echo "[1/3] Installing Sphinx..."
pip install sphinx sphinx-rtd-theme --break-system-packages -q
echo "      Done."

# Build HTML
echo "[2/3] Building documentation..."
cd "$(dirname "$0")/docs"
sphinx-build -b html . _build/html -q
echo "      Done."

# Report
echo "[3/3] Documentation built successfully."
