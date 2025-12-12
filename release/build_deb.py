#!/usr/bin/env python3
"""
Build script for MetaFinder DEB Package (Ubuntu/Linux Mint)
Creates a .deb package for Debian-based Linux distributions
"""

import PyInstaller.__main__
import os
import shutil
import subprocess
import stat
from pathlib import Path
from build_config_linux import *

def build_deb():
    """Build DEB package for Ubuntu/Linux Mint."""
    
    print("=" * 60)
    print("Building MetaFinder DEB Package (Ubuntu/Linux Mint)")
    print("=" * 60)
    
    # First, build the executable
    print("\nStep 1: Building executable...")
    
    # Use separate folder for deb build
    deb_output = os.path.join(OUTPUT_DIR, "deb_temp")
    
    # Clean previous builds
    if os.path.exists(deb_output):
        shutil.rmtree(deb_output)
    deb_build_dir = os.path.join(BUILD_DIR, "deb")
    if os.path.exists(deb_build_dir):
        shutil.rmtree(deb_build_dir)
    
    # Prepare PyInstaller arguments
    args = [
        MAIN_SCRIPT,
        f"--name={APP_NAME}",
        f"--distpath={deb_output}",
        f"--workpath={deb_build_dir}",
        "--onedir",  # Use folder mode for package
        "--windowed",
        "--clean",
        "--noconfirm",
    ]
    
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
    
    PyInstaller.__main__.run(args)
    
    # Step 2: Create DEB package structure
    print("\nStep 2: Creating DEB package structure...")
    
    package_name = f"{APP_NAME_LOWER}_{VERSION}_{DEB_ARCHITECTURE}"
    package_dir = os.path.join(OUTPUT_DIR, package_name)
    
    # Clean if exists
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    # Create directory structure
    dirs_to_create = [
        os.path.join(package_dir, "DEBIAN"),
        os.path.join(package_dir, "usr", "share", APP_NAME_LOWER),
        os.path.join(package_dir, "usr", "bin"),
        os.path.join(package_dir, "usr", "share", "applications"),
        os.path.join(package_dir, "usr", "share", "pixmaps"),
        os.path.join(package_dir, "usr", "share", "doc", APP_NAME_LOWER),
    ]
    
    for dir_path in dirs_to_create:
        os.makedirs(dir_path, exist_ok=True)
    
    # Copy application files
    print("\nStep 3: Copying application files...")
    app_src = os.path.join(deb_output, APP_NAME)
    app_dst = os.path.join(package_dir, "usr", "share", APP_NAME_LOWER)
    
    # Copy all files from PyInstaller output
    for item in os.listdir(app_src):
        src_path = os.path.join(app_src, item)
        dst_path = os.path.join(app_dst, item)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)
    
    # Create launcher script
    print("\nStep 4: Creating launcher script...")
    launcher_script = os.path.join(package_dir, "usr", "bin", APP_NAME_LOWER)
    with open(launcher_script, 'w') as f:
        f.write(f"""#!/bin/bash
# MetaFinder launcher script
cd /usr/share/{APP_NAME_LOWER}
./{APP_NAME} "$@"
""")
    
    # Make launcher executable
    os.chmod(launcher_script, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    
    # Create desktop entry
    print("\nStep 5: Creating desktop entry...")
    desktop_file = os.path.join(package_dir, "usr", "share", "applications", f"{APP_NAME_LOWER}.desktop")
    with open(desktop_file, 'w') as f:
        f.write(f"""[Desktop Entry]
Version=1.0
Type=Application
Name={APP_NAME}
Comment={DESCRIPTION}
Exec={APP_NAME_LOWER} %f
Icon={APP_NAME_LOWER}
Categories={DESKTOP_CATEGORIES}
Keywords={DESKTOP_KEYWORDS}
Terminal=false
StartupNotify=true
MimeType=inode/directory;
""")
    
    # Copy icon
    if os.path.exists(ICON_PATH):
        shutil.copy2(ICON_PATH, os.path.join(package_dir, "usr", "share", "pixmaps", f"{APP_NAME_LOWER}.png"))
    
    # Copy README
    if os.path.exists("../README.md"):
        shutil.copy2("../README.md", os.path.join(package_dir, "usr", "share", "doc", APP_NAME_LOWER, "README.md"))
    
    # Calculate installed size (in KB)
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(app_dst):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    installed_size = total_size // 1024
    
    # Create control file
    print("\nStep 6: Creating control file...")
    control_file = os.path.join(package_dir, "DEBIAN", "control")
    with open(control_file, 'w') as f:
        f.write(f"""Package: {APP_NAME_LOWER}
Version: {VERSION}
Section: {DEB_SECTION}
Priority: {DEB_PRIORITY}
Architecture: {DEB_ARCHITECTURE}
Depends: {DEB_DEPENDS}
Maintainer: {AUTHOR} <{AUTHOR_EMAIL}>
Homepage: {URL}
Installed-Size: {installed_size}
Description: {DESCRIPTION}
 {LONG_DESCRIPTION}
""")
    
    # Create postinst script
    postinst_file = os.path.join(package_dir, "DEBIAN", "postinst")
    with open(postinst_file, 'w') as f:
        f.write(f"""#!/bin/bash
# Post-installation script
set -e

# Update desktop database
if [ -x /usr/bin/update-desktop-database ]; then
    update-desktop-database -q
fi

# Update icon cache
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    gtk-update-icon-cache -q -t -f /usr/share/pixmaps 2>/dev/null || true
fi

exit 0
""")
    os.chmod(postinst_file, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    
    # Create postrm script
    postrm_file = os.path.join(package_dir, "DEBIAN", "postrm")
    with open(postrm_file, 'w') as f:
        f.write(f"""#!/bin/bash
# Post-removal script
set -e

# Update desktop database
if [ -x /usr/bin/update-desktop-database ]; then
    update-desktop-database -q
fi

exit 0
""")
    os.chmod(postrm_file, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    
    # Build the DEB package
    print("\nStep 7: Building DEB package...")
    deb_filename = f"{package_name}.deb"
    deb_path = os.path.join(OUTPUT_DIR, deb_filename)
    
    try:
        subprocess.run(
            ["dpkg-deb", "--build", "--root-owner-group", package_dir, deb_path],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"\n✓ DEB package created successfully: {deb_filename}")
        print(f"  Location: {os.path.abspath(deb_path)}")
        print(f"\nTo install:")
        print(f"  sudo dpkg -i {deb_filename}")
        print(f"  sudo apt-get install -f  # Install dependencies if needed")
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error building DEB package:")
        print(e.stderr)
        raise
    except FileNotFoundError:
        print("\n✗ Error: dpkg-deb not found. Install it with:")
        print("  sudo apt-get install dpkg-dev")
        raise
    
    print("\n" + "=" * 60)
    print("DEB Build Complete!")
    print("=" * 60)

if __name__ == "__main__":
    build_deb()
