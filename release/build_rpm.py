#!/usr/bin/env python3
"""
Build script for MetaFinder RPM Package (Fedora)
Creates an .rpm package for Red Hat-based Linux distributions
"""

import PyInstaller.__main__
import os
import shutil
import subprocess
import stat
from pathlib import Path
from build_config_linux import *

def build_rpm():
    """Build RPM package for Fedora and other RPM-based distributions."""
    
    print("=" * 60)
    print("Building MetaFinder RPM Package (Fedora)")
    print("=" * 60)
    
    # First, build the executable
    print("\nStep 1: Building executable...")
    
    # Use separate folder for rpm build
    rpm_output = os.path.join(OUTPUT_DIR, "rpm_temp")
    
    # Clean previous builds
    if os.path.exists(rpm_output):
        shutil.rmtree(rpm_output)
    rpm_build_dir = os.path.join(BUILD_DIR, "rpm")
    if os.path.exists(rpm_build_dir):
        shutil.rmtree(rpm_build_dir)
    
    # Prepare PyInstaller arguments
    args = [
        MAIN_SCRIPT,
        f"--name={APP_NAME}",
        f"--distpath={rpm_output}",
        f"--workpath={rpm_build_dir}",
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
    
    # Step 2: Create RPM build structure
    print("\nStep 2: Creating RPM build structure...")
    
    rpm_root = os.path.join(OUTPUT_DIR, "rpmbuild")
    rpm_dirs = ["BUILD", "RPMS", "SOURCES", "SPECS", "SRPMS"]
    
    for rpm_dir in rpm_dirs:
        os.makedirs(os.path.join(rpm_root, rpm_dir), exist_ok=True)
    
    # Create buildroot structure
    buildroot = os.path.join(rpm_root, "BUILDROOT")
    package_buildroot = os.path.join(buildroot, f"{APP_NAME_LOWER}-{VERSION}-1.x86_64")
    
    dirs_to_create = [
        os.path.join(package_buildroot, "usr", "share", APP_NAME_LOWER),
        os.path.join(package_buildroot, "usr", "bin"),
        os.path.join(package_buildroot, "usr", "share", "applications"),
        os.path.join(package_buildroot, "usr", "share", "pixmaps"),
        os.path.join(package_buildroot, "usr", "share", "doc", APP_NAME_LOWER),
    ]
    
    for dir_path in dirs_to_create:
        os.makedirs(dir_path, exist_ok=True)
    
    # Copy application files
    print("\nStep 3: Copying application files...")
    app_src = os.path.join(rpm_output, APP_NAME)
    app_dst = os.path.join(package_buildroot, "usr", "share", APP_NAME_LOWER)
    
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
    launcher_script = os.path.join(package_buildroot, "usr", "bin", APP_NAME_LOWER)
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
    desktop_file = os.path.join(package_buildroot, "usr", "share", "applications", f"{APP_NAME_LOWER}.desktop")
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
        shutil.copy2(ICON_PATH, os.path.join(package_buildroot, "usr", "share", "pixmaps", f"{APP_NAME_LOWER}.png"))
    
    # Copy README
    if os.path.exists("../README.md"):
        shutil.copy2("../README.md", os.path.join(package_buildroot, "usr", "share", "doc", APP_NAME_LOWER, "README.md"))
    
    # Create spec file
    print("\nStep 6: Creating RPM spec file...")
    spec_file = os.path.join(rpm_root, "SPECS", f"{APP_NAME_LOWER}.spec")
    
    with open(spec_file, 'w') as f:
        f.write(f"""Name:           {APP_NAME_LOWER}
Version:        {VERSION}
Release:        1%{{?dist}}
Summary:        {DESCRIPTION}
Group:          {RPM_GROUP}
License:        {RPM_LICENSE}
URL:            {URL}
BuildArch:      x86_64
Requires:       {RPM_REQUIRES}

%description
{LONG_DESCRIPTION}

%prep
# No prep needed - using pre-built files

%build
# No build needed - using PyInstaller output

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
cp -r {package_buildroot}/* $RPM_BUILD_ROOT/

%files
%defattr(-,root,root,-)
/usr/share/{APP_NAME_LOWER}/*
/usr/bin/{APP_NAME_LOWER}
/usr/share/applications/{APP_NAME_LOWER}.desktop
/usr/share/pixmaps/{APP_NAME_LOWER}.png
%doc /usr/share/doc/{APP_NAME_LOWER}/README.md

%post
# Update desktop database
if [ -x /usr/bin/update-desktop-database ]; then
    /usr/bin/update-desktop-database &> /dev/null || :
fi

# Update icon cache
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache -q -t -f /usr/share/pixmaps 2>/dev/null || :
fi

%postun
# Update desktop database
if [ $1 -eq 0 ]; then
    if [ -x /usr/bin/update-desktop-database ]; then
        /usr/bin/update-desktop-database &> /dev/null || :
    fi
fi

%changelog
* {subprocess.run(['date', '+%a %b %d %Y'], capture_output=True, text=True).stdout.strip()} {AUTHOR} <{AUTHOR_EMAIL}> - {VERSION}-1
- Initial RPM package release
""")
    
    # Build the RPM package
    print("\nStep 7: Building RPM package...")
    
    try:
        result = subprocess.run(
            ["rpmbuild", "-bb", 
             "--define", f"_topdir {os.path.abspath(rpm_root)}",
             "--buildroot", os.path.abspath(package_buildroot),
             spec_file],
            check=True,
            capture_output=True,
            text=True
        )
        
        # Find the generated RPM
        rpms_dir = os.path.join(rpm_root, "RPMS", "x86_64")
        rpm_files = [f for f in os.listdir(rpms_dir) if f.endswith('.rpm')]
        
        if rpm_files:
            rpm_filename = rpm_files[0]
            rpm_src = os.path.join(rpms_dir, rpm_filename)
            rpm_dst = os.path.join(OUTPUT_DIR, rpm_filename)
            shutil.copy2(rpm_src, rpm_dst)
            
            print(f"\n✓ RPM package created successfully: {rpm_filename}")
            print(f"  Location: {os.path.abspath(rpm_dst)}")
            print(f"\nTo install:")
            print(f"  sudo dnf install {rpm_filename}  # Fedora")
            print(f"  # or")
            print(f"  sudo rpm -ivh {rpm_filename}")
        else:
            print("\n✗ Error: RPM file not found after build")
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error building RPM package:")
        print(e.stderr)
        print("\nStdout:")
        print(e.stdout)
        raise
    except FileNotFoundError:
        print("\n✗ Error: rpmbuild not found. Install it with:")
        print("  sudo dnf install rpm-build rpmdevtools  # Fedora")
        print("  sudo yum install rpm-build rpmdevtools  # RHEL/CentOS")
        raise
    
    print("\n" + "=" * 60)
    print("RPM Build Complete!")
    print("=" * 60)

if __name__ == "__main__":
    build_rpm()
