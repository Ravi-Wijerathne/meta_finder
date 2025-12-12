#!/usr/bin/env python3
"""
Build script for MetaFinder Portable Version (Linux)
Creates a standalone portable package for any Linux distribution
"""

import PyInstaller.__main__
import os
import shutil
import stat
from pathlib import Path
from build_config_linux import *

def build_portable():
    """Build portable version of MetaFinder for Linux."""
    
    print("=" * 60)
    print("Building MetaFinder Portable Version (Linux)")
    print("=" * 60)
    
    # Use separate folder for portable build
    portable_output = os.path.join(OUTPUT_DIR, "portable_temp")
    
    # Clean previous builds
    if os.path.exists(portable_output):
        print("Cleaning previous builds...")
        shutil.rmtree(portable_output)
    portable_build_dir = os.path.join(BUILD_DIR, "portable")
    if os.path.exists(portable_build_dir):
        shutil.rmtree(portable_build_dir)
    
    # Prepare PyInstaller arguments
    args = [
        MAIN_SCRIPT,
        f"--name={APP_NAME}",
        f"--distpath={portable_output}",
        f"--workpath={portable_build_dir}",
        "--clean",
    ]
    
    # Add one-file or one-folder mode
    if ONEFILE:
        args.append("--onefile")
    else:
        args.append("--onedir")
    
    # Window mode
    if WINDOWED and not CONSOLE:
        args.append("--windowed")
    elif CONSOLE:
        args.append("--console")
    
    # Add icon if exists
    if os.path.exists(ICON_PATH):
        args.append(f"--icon={ICON_PATH}")
    
    # Add data files
    for src, dst in ADDITIONAL_DATA:
        if os.path.exists(src):
            args.append(f"--add-data={src}:{dst}")
    
    # Add hidden imports
    for imp in HIDDEN_IMPORTS:
        args.append(f"--hidden-import={imp}")
    
    # Additional options
    args.extend([
        "--noconfirm",
        "--log-level=INFO",
    ])
    
    print("\nBuilding executable...")
    print(f"Command: pyinstaller {' '.join(args)}")
    print()
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)
    
    # Create portable package
    print("\nCreating portable package...")
    
    portable_name = f"{APP_NAME}-Portable-v{VERSION}-linux"
    portable_dir = os.path.join(OUTPUT_DIR, portable_name)
    
    # Create portable directory structure
    os.makedirs(portable_dir, exist_ok=True)
    
    # Copy executable
    if ONEFILE:
        exe_name = APP_NAME
        shutil.copy2(
            os.path.join(portable_output, exe_name),
            os.path.join(portable_dir, exe_name)
        )
        # Make sure it's executable
        exe_path = os.path.join(portable_dir, exe_name)
        os.chmod(exe_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    else:
        # Copy entire folder
        app_folder = os.path.join(portable_output, APP_NAME)
        dest_folder = os.path.join(portable_dir, APP_NAME)
        shutil.copytree(app_folder, dest_folder)
        # Make main executable executable
        main_exe = os.path.join(dest_folder, APP_NAME)
        if os.path.exists(main_exe):
            os.chmod(main_exe, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    
    # Create launcher script
    launcher_script = os.path.join(portable_dir, f"run_{APP_NAME_LOWER}.sh")
    if ONEFILE:
        launcher_content = f"""#!/bin/bash
# MetaFinder Portable Launcher
DIR="$( cd "$( dirname "${{BASH_SOURCE[0]}}" )" && pwd )"
cd "$DIR"
./{APP_NAME} "$@"
"""
    else:
        launcher_content = f"""#!/bin/bash
# MetaFinder Portable Launcher
DIR="$( cd "$( dirname "${{BASH_SOURCE[0]}}" )" && pwd )"
cd "$DIR/{APP_NAME}"
./{APP_NAME} "$@"
"""
    
    with open(launcher_script, 'w') as f:
        f.write(launcher_content)
    
    # Make launcher executable
    os.chmod(launcher_script, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    
    # Copy README
    if os.path.exists("../README.md"):
        shutil.copy2("../README.md", os.path.join(portable_dir, "README.md"))
    
    # Create portable README
    portable_readme = os.path.join(portable_dir, "PORTABLE_README.txt")
    with open(portable_readme, 'w') as f:
        f.write(f"""{APP_NAME} v{VERSION} - Portable Edition for Linux
{'=' * 60}

This is a portable version that doesn't require installation.

RUNNING THE APPLICATION:
------------------------
Option 1: Use the launcher script (recommended)
    ./run_{APP_NAME_LOWER}.sh

Option 2: Run directly
""")
        if ONEFILE:
            f.write(f"""    ./{APP_NAME}
""")
        else:
            f.write(f"""    cd {APP_NAME}
    ./{APP_NAME}
""")
        
        f.write(f"""
REQUIREMENTS:
-------------
- Linux with X11 or Wayland
- Python 3 libraries (bundled, no installation needed)
- Tkinter support (usually pre-installed)

FEATURES:
---------
- No installation required
- No admin/root privileges needed
- Self-contained with all dependencies
- Can run from USB drive or any directory
- All extracted metadata saved to text files

TROUBLESHOOTING:
----------------
If the application doesn't start:

1. Make sure the script is executable:
   chmod +x run_{APP_NAME_LOWER}.sh
""")
        if ONEFILE:
            f.write(f"""   chmod +x {APP_NAME}
""")
        else:
            f.write(f"""   chmod +x {APP_NAME}/{APP_NAME}
""")
        
        f.write(f"""
2. Check if required libraries are installed:
   - For Ubuntu/Mint: sudo apt-get install python3-tk libmagic1
   - For Fedora: sudo dnf install python3-tkinter file-libs

3. Try running from terminal to see error messages:
   ./run_{APP_NAME_LOWER}.sh

PROJECT HOMEPAGE:
-----------------
{URL}

{'=' * 60}
""")
    
    # Create tarball
    print("\nCreating tarball...")
    tar_filename = f"{portable_name}.tar.gz"
    tar_path = os.path.join(OUTPUT_DIR, tar_filename)
    
    import tarfile
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(portable_dir, arcname=portable_name)
    
    print(f"\n✓ Portable package created successfully!")
    print(f"  Directory: {os.path.abspath(portable_dir)}")
    print(f"  Archive: {tar_filename}")
    print(f"\nTo use:")
    print(f"  tar -xzf {tar_filename}")
    print(f"  cd {portable_name}")
    print(f"  ./run_{APP_NAME_LOWER}.sh")
    
    print("\n" + "=" * 60)
    print("Portable Build Complete!")
    print("=" * 60)

if __name__ == "__main__":
    build_portable()
