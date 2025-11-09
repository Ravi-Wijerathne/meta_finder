# MetaFinder Release Build Scripts

This folder contains scripts to build distributable versions of MetaFinder.

## Release Contents

### 1. Setup Version (Installer)
- Full installer for Windows
- Includes all dependencies
- Creates desktop shortcut
- Adds to Start Menu

### 2. Portable Version
- No installation required
- Runs from any folder
- All dependencies bundled
- USB-friendly

## Building the Release

### Prerequisites
```powershell
pip install pyinstaller
```

### Build Commands

**Build Installer Version:**
```powershell
cd release
.\build_installer.ps1
```

**Build Portable Version:**
```powershell
cd release
.\build_portable.ps1
```

**Build Both:**
```powershell
cd release
.\build_all.ps1
```

## Output Structure

```
release/
├── dist/
│   ├── MetaFinder-Setup-v1.0.0.exe     # Installer
│   └── MetaFinder-Portable-v1.0.0.zip  # Portable
├── build/                               # Temporary build files
└── builds/                              # Archive of previous builds
```

## Release Checklist

- [ ] Update version number in `build_config.py`
- [ ] Test both installer and portable versions
- [ ] Verify FFmpeg integration
- [ ] Check all file types work
- [ ] Create GitHub release
- [ ] Upload both versions
- [ ] Update README with download links

## Version History

- v1.0.0 - Initial release
