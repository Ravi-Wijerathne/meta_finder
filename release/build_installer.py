"""
Build script for MetaFinder Installer Version
Creates an installer using Inno Setup
"""

import PyInstaller.__main__
import os
import shutil
import subprocess
from build_config import *

def build_installer():
    """Build installer version of MetaFinder."""
    
    print("=" * 60)
    print("Building MetaFinder Installer Version")
    print("=" * 60)
    
    # First, build the executable
    print("\nStep 1: Building executable...")
    
    # Use separate folder for installer build
    installer_output = os.path.join(OUTPUT_DIR, "installer_temp")
    
    # Clean previous builds
    if os.path.exists(installer_output):
        shutil.rmtree(installer_output)
    installer_build_dir = os.path.join(BUILD_DIR, "installer")
    if os.path.exists(installer_build_dir):
        shutil.rmtree(installer_build_dir)
    
    # Prepare PyInstaller arguments
    args = [
        MAIN_SCRIPT,
        f"--name={APP_NAME}",
        f"--distpath={installer_output}",
        f"--workpath={installer_build_dir}",
        "--onedir",  # Use folder mode for installer
        "--windowed",
        "--clean",
        "--noconfirm",
    ]
    
    # Add icon
    if os.path.exists(ICON_PATH):
        args.append(f"--icon={ICON_PATH}")
    
    # Add data files
    for src, dst in ADDITIONAL_DATA:
        if os.path.exists(src):
            args.append(f"--add-data={src};{dst}")
    
    # Add hidden imports
    for imp in HIDDEN_IMPORTS:
        args.append(f"--hidden-import={imp}")
    
    PyInstaller.__main__.run(args)
    
    # Step 2: Create Inno Setup script
    print("\nStep 2: Creating installer script...")
    
    inno_script = f"""
; MetaFinder Installer Script
; Generated automatically

#define MyAppName "{APP_NAME}"
#define MyAppVersion "{VERSION}"
#define MyAppPublisher "{AUTHOR}"
#define MyAppURL "https://github.com/Ravi-Wijerathne/meta_finder"
#define MyAppExeName "{APP_NAME}.exe"

[Setup]
AppId={{{{YOUR-GUID-HERE}}}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={{#MyAppURL}}
AppSupportURL={{#MyAppURL}}
AppUpdatesURL={{#MyAppURL}}
DefaultDirName={{autopf}}\\{{#MyAppName}}
DefaultGroupName={{#MyAppName}}
AllowNoIcons=yes
LicenseFile=..\\README.md
OutputDir={OUTPUT_DIR}
OutputBaseFilename={APP_NAME}-Setup-v{VERSION}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked

[Files]
Source: "{installer_output}\\{APP_NAME}\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{group}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"
Name: "{{autodesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: desktopicon

[Run]
Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(MyAppName, '&', '&&')}}}}"; Flags: nowait postinstall skipifsilent
"""
    
    inno_script_path = os.path.join(".", "installer.iss")
    with open(inno_script_path, "w") as f:
        f.write(inno_script)
    
    print(f"✅ Installer script created: {inno_script_path}")
    
    # Step 3: Try to compile with Inno Setup if available
    print("\nStep 3: Checking for Inno Setup...")
    
    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
    ]
    
    inno_found = False
    for inno_path in inno_paths:
        if os.path.exists(inno_path):
            print(f"✅ Found Inno Setup: {inno_path}")
            print("Compiling installer...")
            
            try:
                result = subprocess.run(
                    [inno_path, inno_script_path],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print("\n" + "=" * 60)
                    print("✅ Installer build complete!")
                    print(f"📦 Output: {OUTPUT_DIR}/{APP_NAME}-Setup-v{VERSION}.exe")
                    print("=" * 60)
                    inno_found = True
                else:
                    print("❌ Inno Setup compilation failed:")
                    print(result.stderr)
            except Exception as e:
                print(f"❌ Error running Inno Setup: {e}")
            
            break
    
    if not inno_found:
        print("\n⚠️  Inno Setup not found!")
        print("To create the installer:")
        print("1. Download Inno Setup from: https://jrsoftware.org/isdl.php")
        print("2. Install Inno Setup")
        print(f"3. Open {inno_script_path} in Inno Setup")
        print("4. Click 'Compile' to create the installer")
        print("\n" + "=" * 60)
        print("✅ Executable build complete!")
        print(f"📁 Files ready in: {installer_output}/{APP_NAME}/")
        print(f"📄 Installer script: {inno_script_path}")
        print("=" * 60)
    
    # Clean up temporary build folder
    if os.path.exists(installer_build_dir):
        shutil.rmtree(installer_build_dir, ignore_errors=True)

if __name__ == "__main__":
    build_installer()
