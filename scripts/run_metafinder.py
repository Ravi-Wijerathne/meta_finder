#!/usr/bin/env python3
"""
MetaFinder - Automated Setup and Launch Script
This script checks and installs all prerequisites before running MetaFinder
Cross-platform compatible (Windows, Linux, macOS)
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

# Directories
SCRIPTS_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPTS_DIR.parent
os.chdir(PROJECT_ROOT)

# Virtual environment directory
VENV_DIR = PROJECT_ROOT / "venv"

# Color codes for output (ANSI escape codes)
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

    @classmethod
    def disable(cls):
        """Disable colors for Windows CMD that doesn't support ANSI"""
        cls.RED = ''
        cls.GREEN = ''
        cls.YELLOW = ''
        cls.BLUE = ''
        cls.NC = ''


# Enable ANSI colors on Windows 10+
def enable_windows_ansi():
    """Enable ANSI escape sequences on Windows"""
    if platform.system() == 'Windows':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            # Enable ANSI escape sequences
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            Colors.disable()


# Log functions
def log_info(message):
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {message}")


def log_success(message):
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {message}")


def log_warning(message):
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {message}")


def log_error(message):
    print(f"{Colors.RED}[ERROR]{Colors.NC} {message}")


def display_banner():
    """Display application banner"""
    print(f"{Colors.BLUE}")
    print("╔════════════════════════════════════════╗")
    print("║      MetaFinder Setup & Launch         ║")
    print("║   Universal Metadata Extraction Tool   ║")
    print("╚════════════════════════════════════════╝")
    print(f"{Colors.NC}")


def command_exists(cmd):
    """Check if a command exists in the system"""
    return shutil.which(cmd) is not None


def run_command(cmd, capture_output=True, check=False):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            cmd,
            shell=isinstance(cmd, str),
            capture_output=capture_output,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        return e
    except Exception as e:
        return None


def get_python_cmd():
    """Get the appropriate Python command for the system"""
    # Try python3 first, then python
    for cmd in ['python3', 'python']:
        if command_exists(cmd):
            result = run_command([cmd, '--version'])
            if result and result.returncode == 0:
                version = result.stdout.strip().split()[-1]
                major, minor = map(int, version.split('.')[:2])
                if major >= 3 and minor >= 7:
                    return cmd, version
    return None, None


def check_python():
    """Check Python installation"""
    log_info("Checking Python installation...")
    
    python_cmd, version = get_python_cmd()
    
    if python_cmd:
        log_success(f"Python {version} found")
        return python_cmd
    
    log_error("Python 3.7+ is not installed!")
    
    system = platform.system()
    if system == 'Windows':
        log_info("Please install Python from https://www.python.org/downloads/")
        log_info("Make sure to check 'Add Python to PATH' during installation")
    elif system == 'Linux':
        log_info("Install Python using your package manager:")
        log_info("  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv python3-tk")
        log_info("  Fedora: sudo dnf install python3 python3-pip python3-tkinter")
        log_info("  Arch: sudo pacman -S python python-pip tk")
    elif system == 'Darwin':
        log_info("Install Python using Homebrew: brew install python3 python-tk")
    
    sys.exit(1)


def check_pip(python_cmd):
    """Check pip installation"""
    log_info("Checking pip installation...")
    
    result = run_command([python_cmd, '-m', 'pip', '--version'])
    
    if result and result.returncode == 0:
        log_success("pip is installed")
        return True
    
    log_warning("pip not found. Attempting to install...")
    
    # Try to install pip using ensurepip
    result = run_command([python_cmd, '-m', 'ensurepip', '--upgrade'])
    if result and result.returncode == 0:
        log_success("pip installed successfully")
        return True
    
    log_error("Could not install pip. Please install it manually.")
    sys.exit(1)


def check_tkinter(python_cmd):
    """Check tkinter installation"""
    log_info("Checking tkinter installation...")
    
    result = run_command([python_cmd, '-c', 'import tkinter'])
    
    if result and result.returncode == 0:
        log_success("tkinter is installed")
        return True
    
    log_error("tkinter is not installed!")
    
    system = platform.system()
    if system == 'Windows':
        log_info("tkinter should be included with Python on Windows.")
        log_info("Try reinstalling Python with the 'tcl/tk and IDLE' option checked.")
    elif system == 'Linux':
        log_info("Install tkinter using your package manager:")
        log_info("  Ubuntu/Debian: sudo apt install python3-tk")
        log_info("  Fedora: sudo dnf install python3-tkinter")
        log_info("  Arch: sudo pacman -S tk")
    elif system == 'Darwin':
        log_info("Install tkinter using Homebrew: brew install python-tk")
    
    sys.exit(1)


def check_system_libraries():
    """Check system libraries (for python-magic)"""
    log_info("Checking system libraries...")
    
    system = platform.system()
    
    if system == 'Windows':
        # On Windows, python-magic-bin includes the DLL
        log_success("Using python-magic-bin for Windows (includes libmagic)")
    elif system == 'Linux':
        # Check for libmagic
        result = run_command(['ldconfig', '-p'])
        if result and 'libmagic' in result.stdout:
            log_success("libmagic is installed")
        else:
            log_warning("libmagic may not be installed.")
            log_info("If you encounter issues, install it:")
            log_info("  Ubuntu/Debian: sudo apt install libmagic1 file")
            log_info("  Fedora: sudo dnf install file-libs file")
            log_info("  Arch: sudo pacman -S file")
    elif system == 'Darwin':
        # Check for libmagic on macOS
        if Path('/usr/local/lib/libmagic.dylib').exists() or Path('/opt/homebrew/lib/libmagic.dylib').exists():
            log_success("libmagic is installed")
        else:
            log_warning("libmagic may not be installed.")
            log_info("Install using: brew install libmagic")


def setup_virtual_environment(python_cmd):
    """Check and setup virtual environment"""
    log_info("Checking virtual environment...")
    
    # Check if venv module is available
    result = run_command([python_cmd, '-m', 'venv', '--help'])
    if not result or result.returncode != 0:
        log_error("python venv module is not available!")
        system = platform.system()
        if system == 'Linux':
            log_info("Install python3-venv:")
            log_info("  Ubuntu/Debian: sudo apt install python3-venv python3-full")
            log_info("  Fedora: sudo dnf install python3-virtualenv")
        sys.exit(1)
    
    # Determine paths based on OS
    system = platform.system()
    if system == 'Windows':
        venv_python = VENV_DIR / 'Scripts' / 'python.exe'
        venv_pip = VENV_DIR / 'Scripts' / 'pip.exe'
    else:
        venv_python = VENV_DIR / 'bin' / 'python'
        venv_pip = VENV_DIR / 'bin' / 'pip'

    # Create or repair virtual environment when missing or incomplete
    if not VENV_DIR.exists():
        log_info("Creating virtual environment...")
        result = run_command([python_cmd, '-m', 'venv', str(VENV_DIR)])
        if result and result.returncode == 0:
            log_success(f"Virtual environment created at: {VENV_DIR}")
        else:
            log_error("Failed to create virtual environment!")
            sys.exit(1)
    elif not venv_python.exists():
        log_warning("Virtual environment exists but looks incomplete. Rebuilding...")
        result = run_command([python_cmd, '-m', 'venv', '--clear', str(VENV_DIR)])
        if result and result.returncode == 0:
            log_success("Virtual environment rebuilt successfully")
        else:
            log_error("Failed to rebuild virtual environment!")
            sys.exit(1)
    else:
        log_success("Virtual environment already exists")

    if not venv_python.exists():
        log_error("Virtual environment Python executable not found after setup")
        sys.exit(1)
    
    log_success("Using virtual environment")
    return str(venv_python), str(venv_pip)


def install_dependencies(python_cmd, pip_cmd):
    """Install Python dependencies"""
    log_info("Checking Python dependencies...")
    
    requirements_file = PROJECT_ROOT / 'requirements.txt'
    
    if not requirements_file.exists():
        log_error("requirements.txt not found!")
        sys.exit(1)
    
    # Read requirements
    with open(requirements_file, 'r') as f:
        requirements = f.read()
    
    # Modify requirements based on OS
    system = platform.system()
    temp_req_file = PROJECT_ROOT / '.requirements_temp.txt'
    
    if system == 'Linux' or system == 'Darwin':
        log_info(f"Detected {system} - using python-magic instead of python-magic-bin...")
        # Replace python-magic-bin with python-magic for Linux/macOS
        modified_requirements = []
        for line in requirements.splitlines():
            if line.strip().startswith('python-magic-bin'):
                modified_requirements.append('python-magic')
            else:
                modified_requirements.append(line)
        requirements_content = '\n'.join(modified_requirements)
    else:
        requirements_content = requirements
    
    # Write temporary requirements file
    with open(temp_req_file, 'w') as f:
        f.write(requirements_content)
    
    # Check if packages are missing
    log_info("Verifying installed packages...")
    missing_packages = False
    
    for line in requirements_content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Extract package name
        pkg_name = line.split('==')[0].split('>=')[0].split('<=')[0].split('[')[0].strip()
        
        result = run_command([python_cmd, '-m', 'pip', 'show', pkg_name])
        if not result or result.returncode != 0:
            missing_packages = True
            break
    
    if missing_packages:
        log_warning("Some dependencies are missing. Installing...")
        
        # Upgrade pip first
        log_info("Upgrading pip in virtual environment...")
        run_command([python_cmd, '-m', 'pip', 'install', '--upgrade', 'pip', '--quiet'])
        
        # Install requirements
        log_info("Installing dependencies...")
        result = run_command([python_cmd, '-m', 'pip', 'install', '-r', str(temp_req_file)], capture_output=False)
        
        if result and result.returncode == 0:
            log_success("All dependencies installed successfully")
        else:
            log_error("Failed to install some dependencies")
    else:
        log_success("All dependencies are already installed")
    
    # Clean up temp file
    if temp_req_file.exists():
        temp_req_file.unlink()


def verify_installation(python_cmd):
    """Verify installation by testing imports"""
    log_info("Verifying installation...")
    
    test_code = """
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
"""
    
    result = run_command([python_cmd, '-c', test_code])
    
    if result and result.returncode == 0 and 'OK' in result.stdout:
        log_success("All modules verified successfully")
        return True
    else:
        log_error("Some modules failed to import")
        if result:
            log_error(result.stdout + result.stderr)
        log_info("Attempting to reinstall dependencies...")
        
        requirements_file = PROJECT_ROOT / 'requirements.txt'
        run_command([python_cmd, '-m', 'pip', 'install', '--force-reinstall', '-r', str(requirements_file)], capture_output=False)
        return False


def launch_metafinder(python_cmd):
    """Launch MetaFinder"""
    log_info("Launching MetaFinder...")
    print()
    
    main_file = PROJECT_ROOT / 'main.py'
    
    if not main_file.exists():
        log_error("main.py not found!")
        sys.exit(1)
    
    # Run the application (don't capture output, let it display to user)
    try:
        subprocess.run([python_cmd, str(main_file)], check=True)
    except subprocess.CalledProcessError as e:
        log_error(f"MetaFinder exited with error code: {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        log_info("MetaFinder terminated by user")


def main():
    """Main execution flow"""
    enable_windows_ansi()
    display_banner()
    
    log_info("Starting automated setup...")
    print()
    
    # Check and install prerequisites
    python_cmd = check_python()
    check_pip(python_cmd)
    check_tkinter(python_cmd)
    check_system_libraries()
    
    print()
    
    # Setup virtual environment
    venv_python, venv_pip = setup_virtual_environment(python_cmd)
    
    print()
    
    # Install Python dependencies
    install_dependencies(venv_python, venv_pip)
    
    print()
    
    # Verify everything works
    verify_installation(venv_python)
    
    print()
    log_success("Setup completed successfully!")
    print()
    
    # Launch the application
    launch_metafinder(venv_python)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        log_info("Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        log_error(f"Unexpected error: {e}")
        sys.exit(1)
