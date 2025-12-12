#!/bin/bash

##############################################################################
# MetaFinder - Automated Setup and Launch Script
# This script checks and installs all prerequisites before running MetaFinder
##############################################################################

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Virtual environment directory
VENV_DIR="$SCRIPT_DIR/venv"

# Log functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Display banner
display_banner() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════╗"
    echo "║      MetaFinder Setup & Launch         ║"
    echo "║   Universal Metadata Extraction Tool   ║"
    echo "╚════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python installation
check_python() {
    log_info "Checking Python installation..."
    
    if command_exists python3; then
        PYTHON_CMD="python3"
        PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
        log_success "Python $PYTHON_VERSION found"
        
        # Check if version is 3.7 or higher
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        
        if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
            log_error "Python 3.7 or higher is required. Found: $PYTHON_VERSION"
            exit 1
        fi
    elif command_exists python; then
        PYTHON_CMD="python"
        PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
        
        if [[ $PYTHON_VERSION == 2.* ]]; then
            log_error "Python 3.7+ is required. Found Python 2.x"
            log_info "Please install Python 3: sudo apt install python3 python3-pip"
            exit 1
        fi
        log_success "Python $PYTHON_VERSION found"
    else
        log_error "Python is not installed!"
        log_info "Installing Python..."
        
        if command_exists apt-get; then
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv python3-tk
        elif command_exists yum; then
            sudo yum install -y python3 python3-pip python3-tkinter
        elif command_exists dnf; then
            sudo dnf install -y python3 python3-pip python3-tkinter
        elif command_exists pacman; then
            sudo pacman -S --noconfirm python python-pip tk
        else
            log_error "Could not detect package manager. Please install Python 3.7+ manually"
            exit 1
        fi
        
        PYTHON_CMD="python3"
        log_success "Python installed successfully"
    fi
}

# Check pip installation
check_pip() {
    log_info "Checking pip installation..."
    
    if $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
        log_success "pip is installed"
    else
        log_warning "pip not found. Installing pip..."
        
        if command_exists apt-get; then
            sudo apt-get install -y python3-pip
        elif command_exists yum; then
            sudo yum install -y python3-pip
        elif command_exists dnf; then
            sudo dnf install -y python3-pip
        else
            # Try to install pip using get-pip.py
            log_info "Downloading get-pip.py..."
            curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
            $PYTHON_CMD get-pip.py
            rm get-pip.py
        fi
        
        log_success "pip installed successfully"
    fi
}

# Check tkinter (required for GUI)
check_tkinter() {
    log_info "Checking tkinter installation..."
    
    if $PYTHON_CMD -c "import tkinter" 2>/dev/null; then
        log_success "tkinter is installed"
    else
        log_warning "tkinter not found. Installing tkinter..."
        
        if command_exists apt-get; then
            sudo apt-get install -y python3-tk
        elif command_exists yum; then
            sudo yum install -y python3-tkinter
        elif command_exists dnf; then
            sudo dnf install -y python3-tkinter
        elif command_exists pacman; then
            sudo pacman -S --noconfirm tk
        else
            log_error "Could not install tkinter. Please install it manually"
            exit 1
        fi
        
        log_success "tkinter installed successfully"
    fi
}

# Check system libraries (for python-magic)
check_system_libraries() {
    log_info "Checking system libraries..."
    
    # Check for libmagic (required by python-magic)
    if ldconfig -p | grep -q libmagic; then
        log_success "libmagic is installed"
    else
        log_warning "libmagic not found. Installing file/libmagic..."
        
        if command_exists apt-get; then
            sudo apt-get install -y libmagic1 file
        elif command_exists yum; then
            sudo yum install -y file-libs file
        elif command_exists dnf; then
            sudo dnf install -y file-libs file
        elif command_exists pacman; then
            sudo pacman -S --noconfirm file
        else
            log_warning "Could not install libmagic automatically"
        fi
    fi
}

# Check and setup virtual environment
setup_virtual_environment() {
    log_info "Checking virtual environment..."
    
    # Check if python3-venv is installed
    if ! $PYTHON_CMD -m venv --help >/dev/null 2>&1; then
        log_warning "python3-venv not found. Installing..."
        
        if command_exists apt-get; then
            sudo apt-get install -y python3-venv python3-full
        elif command_exists yum; then
            sudo yum install -y python3-virtualenv
        elif command_exists dnf; then
            sudo dnf install -y python3-virtualenv
        else
            log_error "Could not install python3-venv. Please install it manually"
            exit 1
        fi
    fi
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "$VENV_DIR" ]; then
        log_info "Creating virtual environment..."
        $PYTHON_CMD -m venv "$VENV_DIR"
        log_success "Virtual environment created at: $VENV_DIR"
    else
        log_success "Virtual environment already exists"
    fi
    
    # Update Python command to use venv
    PYTHON_CMD="$VENV_DIR/bin/python"
    PIP_CMD="$VENV_DIR/bin/pip"
    
    log_success "Using virtual environment"
}

# Install Python dependencies
install_dependencies() {
    log_info "Checking Python dependencies..."
    
    if [ ! -f "requirements.txt" ]; then
        log_error "requirements.txt not found!"
        exit 1
    fi
    
    # Create a temporary requirements file for Linux
    TEMP_REQ="$SCRIPT_DIR/.requirements_temp.txt"
    
    # Check if all packages are installed
    log_info "Verifying installed packages..."
    MISSING_PACKAGES=false
    
    # Prepare requirements for Linux (replace python-magic-bin with python-magic)
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        log_info "Detected Linux - using python-magic instead of python-magic-bin..."
        sed 's/python-magic-bin.*/python-magic/' requirements.txt > "$TEMP_REQ"
    else
        cp requirements.txt "$TEMP_REQ"
    fi
    
    while IFS= read -r package || [ -n "$package" ]; do
        # Skip empty lines and comments
        [[ -z "$package" || "$package" =~ ^#.* ]] && continue
        
        # Extract package name (before == or >=)
        pkg_name=$(echo "$package" | sed 's/[>=<]=.*//' | sed 's/\[.*\]//')
        
        if ! $PYTHON_CMD -m pip show "$pkg_name" >/dev/null 2>&1; then
            MISSING_PACKAGES=true
            break
        fi
    done < "$TEMP_REQ"
    
    if [ "$MISSING_PACKAGES" = true ]; then
        log_warning "Some dependencies are missing. Installing..."
        
        # Upgrade pip first
        log_info "Upgrading pip in virtual environment..."
        $PYTHON_CMD -m pip install --upgrade pip --quiet
        
        # Install requirements
        log_info "Installing dependencies from modified requirements..."
        $PYTHON_CMD -m pip install -r "$TEMP_REQ"
        
        log_success "All dependencies installed successfully"
    else
        log_success "All dependencies are already installed"
    fi
    
    # Clean up temp file
    rm -f "$TEMP_REQ"
}

# Verify installation
verify_installation() {
    log_info "Verifying installation..."
    
    # Test imports
    if $PYTHON_CMD -c "
import sys
try:
    import magic
    import exifread
    import mutagen
    import hachoir
    import PyPDF2
    import docx
    import tinytag
    import PIL
    from tkinter import Tk
    print('OK')
except ImportError as e:
    print(f'FAIL: {e}')
    sys.exit(1)
" 2>&1 | grep -q "OK"; then
        log_success "All modules verified successfully"
    else
        log_error "Some modules failed to import"
        log_info "Attempting to reinstall dependencies..."
        $PYTHON_CMD -m pip install --force-reinstall -r requirements.txt
    fi
}

# Launch MetaFinder
launch_metafinder() {
    log_info "Launching MetaFinder..."
    echo ""
    
    if [ ! -f "main.py" ]; then
        log_error "main.py not found!"
        exit 1
    fi
    
    # Run the application
    $PYTHON_CMD main.py
}

# Main execution flow
main() {
    display_banner
    
    log_info "Starting automated setup..."
    echo ""
    
    # Check and install prerequisites
    check_python
    check_pip
    check_tkinter
    check_system_libraries
    
    echo ""
    
    # Setup virtual environment
    setup_virtual_environment
    
    echo ""
    
    # Install Python dependencies
    install_dependencies
    
    echo ""
    
    # Verify everything works
    verify_installation
    
    echo ""
    log_success "Setup completed successfully!"
    echo ""
    
    # Launch the application
    launch_metafinder
}

# Run main function
main
