"""
Build script for MetaFinder Portable Version
Creates a standalone executable with all dependencies
"""

import PyInstaller.__main__
import os
import shutil
from build_config import *

def build_portable():
    """Build portable version of MetaFinder."""
    
    print("=" * 60)
    print("Building MetaFinder Portable Version")
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
            args.append(f"--add-data={src};{dst}")
    
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
    
    portable_name = f"{APP_NAME}-Portable-v{VERSION}"
    portable_dir = os.path.join(portable_output, portable_name)
    
    # Create portable directory structure
    os.makedirs(portable_dir, exist_ok=True)
    
    # Copy executable
    if ONEFILE:
        exe_name = f"{APP_NAME}.exe"
        shutil.copy(
            os.path.join(portable_output, exe_name),
            os.path.join(portable_dir, exe_name)
        )
    else:
        # Copy entire folder
        app_folder = os.path.join(portable_output, APP_NAME)
        shutil.copytree(app_folder, os.path.join(portable_dir, APP_NAME))
    
    # Copy README
    if os.path.exists("../README.md"):
        shutil.copy("../README.md", portable_dir)
    
    # Create portable instructions
    with open(os.path.join(portable_dir, "HOW_TO_USE.txt"), "w") as f:
        f.write(f"""{APP_NAME} - Portable Version v{VERSION}

QUICK START:
1. Double-click {APP_NAME}.exe to launch
2. Click "Browse" to select any file
3. Click "Extract Metadata" to extract metadata
4. View results and save to .txt file

FEATURES:
- Extract metadata from ANY file type
- Support for images, audio, video, documents, archives
- No installation required
- Run from USB drive or any folder

SYSTEM REQUIREMENTS:
- Windows 7 or later
- No additional software needed (all dependencies included)

OPTIONAL:
- For advanced video metadata, install FFmpeg:
  https://ffmpeg.org/download.html

SUPPORT:
- GitHub: https://github.com/Ravi-Wijerathne/meta_finder
- Issues: https://github.com/Ravi-Wijerathne/meta_finder/issues

Enjoy using {APP_NAME}!
""")
    
    # Create zip file
    print(f"Creating ZIP archive: {portable_name}.zip")
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    shutil.make_archive(
        os.path.join(OUTPUT_DIR, portable_name),
        'zip',
        portable_output,
        portable_name
    )
    
    # Clean up temporary folders
    shutil.rmtree(portable_output)
    shutil.rmtree(portable_build_dir, ignore_errors=True)
    
    print("\n" + "=" * 60)
    print("✅ Portable build complete!")
    print(f"📦 Output: {OUTPUT_DIR}/{portable_name}.zip")
    print("=" * 60)

if __name__ == "__main__":
    build_portable()
