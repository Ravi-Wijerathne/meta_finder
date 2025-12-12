#!/bin/bash
# Build script for MetaFinder Linux packages
# Convenience wrapper for build_all_linux.py

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}MetaFinder Linux Build Script${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo -e "${YELLOW}PyInstaller not found. Installing...${NC}"
    pip3 install pyinstaller
fi

# Change to the release directory
cd "$(dirname "$0")"

# Run the Python build script with all arguments
python3 build_all_linux.py "$@"
