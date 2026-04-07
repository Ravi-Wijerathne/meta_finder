# MetaFinder Release Build Scripts

This folder contains scripts to build distributable versions of MetaFinder for Windows and Linux.

## Platform Support

### Windows
- **Installer** - Full installer with Inno Setup
- **Portable** - Standalone executable

### Linux
- **DEB Package** - Ubuntu, Linux Mint, Debian
- **RPM Package** - Fedora, RHEL, CentOS
- **Portable** - Universal tarball for any Linux distribution

---

## Quick Start Commands

### Windows
```powershell
# Build all Windows versions
cd release
.\build_all.ps1

# Build specific version
.\build_installer.ps1   # Installer only
.\build_portable.ps1    # Portable only
```

### Linux - One-Command Builds
```bash
# Build everything for all Linux distributions
./build_all_linux.sh --all

# Build for Ubuntu/Linux Mint only
./build_all_linux.sh --deb

# Build for Fedora only
./build_all_linux.sh --rpm

# Build portable version only
./build_all_linux.sh --portable

# Build DEB and portable (skip RPM)
./build_all_linux.sh --deb --portable
```

### Linux - Advanced Build Options
```bash
# Build specific package directly
python3 build_deb.py              # DEB package
python3 build_rpm.py              # RPM package
python3 build_portable_linux.py   # Portable version

# Build with Python directly
python3 build_all_linux.py --deb
python3 build_all_linux.py --rpm
python3 build_all_linux.py --portable
python3 build_all_linux.py --all
```

---

## Prerequisites

### Windows
```powershell
# Install PyInstaller
pip install pyinstaller
```

For installer version: Install [Inno Setup](https://jrsoftware.org/isdl.php)

### Linux

#### All Builds
```bash
# Install Python 3 and pip
sudo apt-get install python3 python3-pip  # Ubuntu/Mint/Debian
sudo dnf install python3 python3-pip      # Fedora/RHEL

# Install PyInstaller
pip3 install pyinstaller

# Install required Python packages
pip3 install -r ../requirements.txt
```

#### For DEB Packages (Ubuntu/Mint/Debian)
```bash
sudo apt-get install dpkg-dev
```

#### For RPM Packages (Fedora/RHEL/CentOS)
```bash
sudo dnf install rpm-build rpmdevtools
```

#### First Time Setup
```bash
# Make the build script executable
chmod +x build_all_linux.sh
```

---

## Installation

### Windows Installer
```powershell
# Run the installer
MetaFinder-Setup-v1.0.0.exe
```

### Windows Portable
```powershell
# Extract and run
# Double-click MetaFinder.exe
```

### Ubuntu / Linux Mint / Debian
```bash
# Install the DEB package
sudo dpkg -i metafinder_1.0.0_amd64.deb

# Install dependencies if needed
sudo apt-get install -f

# Run the application
metafinder
```

### Fedora / RHEL / CentOS
```bash
# Install the RPM package
sudo dnf install metafinder-1.0.0-1.fc39.x86_64.rpm
# or
sudo rpm -ivh metafinder-1.0.0-1.fc39.x86_64.rpm

# Run the application
metafinder
```

### Linux Portable (Any Distribution)
```bash
# Extract the archive
tar -xzf MetaFinder-Portable-v1.0.0-linux.tar.gz

# Change to the directory
cd MetaFinder-Portable-v1.0.0-linux

# Run the launcher
./scripts/run_metafinder.sh
```

---

## Output Structure

```
release/
├── dist/
│   ├── MetaFinder-Setup-v1.0.0.exe              # Windows Installer
│   ├── MetaFinder-Portable-v1.0.0.zip           # Windows Portable
│   ├── metafinder_1.0.0_amd64.deb               # DEB Package
│   ├── metafinder-1.0.0-1.fc39.x86_64.rpm      # RPM Package
│   └── MetaFinder-Portable-v1.0.0-linux.tar.gz # Linux Portable
├── build/                                        # Temporary build files (can be deleted)
└── builds/                                       # Archive of previous builds
```

---

## Configuration

### Windows Configuration
Edit `build_config.py` to customize Windows builds.

### Linux Configuration
Edit `build_config_linux.py` to customize:
- Application name and version
- Package metadata (author, description, URL)
- Dependencies
- Hidden imports for PyInstaller
- Desktop entry settings

---

## Package Details

### Windows Installer
- Full installer for Windows
- Includes all dependencies
- Creates desktop shortcut
- Adds to Start Menu
- Uninstaller included

### Windows Portable
- No installation required
- Runs from any folder
- All dependencies bundled
- USB-friendly
- Single executable file

### Linux DEB Package
- Standard package for Debian-based systems
- **Location**: `/usr/share/metafinder/`
- **Launcher**: `/usr/bin/metafinder`
- **Desktop Entry**: `/usr/share/applications/metafinder.desktop`
- **Icon**: `/usr/share/pixmaps/metafinder.png`
- **Documentation**: `/usr/share/doc/metafinder/`
- Installs to system directories
- Adds to application menu
- Desktop integration

### Linux RPM Package
- Standard package for Red Hat-based systems
- **Location**: `/usr/share/metafinder/`
- **Launcher**: `/usr/bin/metafinder`
- **Desktop Entry**: `/usr/share/applications/metafinder.desktop`
- **Icon**: `/usr/share/pixmaps/metafinder.png`
- **Documentation**: `/usr/share/doc/metafinder/`
- Installs to system directories
- Adds to application menu
- Desktop integration

### Linux Portable
- No installation required
- Self-contained in a single directory
- Can run from USB drive
- Includes all dependencies
- Works on any Linux distribution

---

## Testing Packages

### Quick Test on Current System (Linux)
```bash
# After building, test the executable directly
cd dist/portable_temp/MetaFinder
./MetaFinder
```

### Test in Docker (Ubuntu)
```bash
docker run -it --rm \
  -v $(pwd)/dist:/packages \
  ubuntu:latest bash -c "
    apt-get update && \
    apt-get install -y /packages/metafinder_1.0.0_amd64.deb && \
    metafinder --version
  "
```

### Test in Docker (Fedora)
```bash
docker run -it --rm \
  -v $(pwd)/dist:/packages \
  fedora:latest bash -c "
    dnf install -y /packages/metafinder-1.0.0-1.fc39.x86_64.rpm && \
    metafinder --version
  "
```

---

## Troubleshooting

### Linux Build Issues

#### PyInstaller not found
```bash
pip3 install pyinstaller
```

#### DEB build fails
```bash
sudo apt-get install dpkg-dev debhelper

# Check for errors in the control file
cat dist/deb_temp/DEBIAN/control
```

#### RPM build fails
```bash
sudo dnf install rpm-build rpmdevtools

# Check spec file
cat dist/rpmbuild/SPECS/metafinder.spec
```

#### Import errors during build
```bash
pip3 install -r ../requirements.txt
```

#### Missing Dependencies
```bash
# Ubuntu/Mint/Debian
sudo apt-get install python3-tk libmagic1

# Fedora/RHEL
sudo dnf install python3-tkinter file-libs
```

#### Permission Errors
```bash
# Make scripts executable
chmod +x build_all_linux.sh
chmod +x build_deb.py
chmod +x build_rpm.py
chmod +x build_portable_linux.py
```

### Clean Build
```bash
# Remove all build artifacts
rm -rf dist/ build/

# Start fresh build
./build_all_linux.sh --all
```

---

## File Locations

### Build Scripts
- **Windows**: `build_all.ps1`, `build_installer.ps1`, `build_portable.ps1`
- **Linux**: `build_all_linux.sh`, `build_all_linux.py`
- **Linux Individual**: `build_deb.py`, `build_rpm.py`, `build_portable_linux.py`

### Configuration
- **Windows**: `build_config.py`
- **Linux**: `build_config_linux.py`

### Desktop Integration
- `metafinder.desktop` - Linux desktop entry file

### Output
- `dist/` - All built packages
- `build/` - Temporary build files (can be deleted)

---

## Release Checklist

- [ ] Update version in `build_config.py` (Windows)
- [ ] Update version in `build_config_linux.py` (Linux)
- [ ] Create/update icons (`assets/icon.ico` for Windows, `assets/icon.png` for Linux)
- [ ] Test all package types on their respective platforms
- [ ] Verify all file type metadata extraction works
- [ ] Build all packages:
  - [ ] Windows Installer
  - [ ] Windows Portable
  - [ ] Linux DEB (Ubuntu/Mint)
  - [ ] Linux RPM (Fedora)
  - [ ] Linux Portable
- [ ] Test installations on clean systems
- [ ] Create GitHub release
- [ ] Upload all packages to GitHub releases
- [ ] Update main README.md with download links
- [ ] Tag the release in Git

---

## Additional Resources

- [PyInstaller Documentation](https://pyinstaller.org/)
- [Inno Setup Documentation](https://jrsoftware.org/ishelp/)
- [Debian Package Guide](https://www.debian.org/doc/manuals/maint-guide/)
- [RPM Packaging Guide](https://rpm-packaging-guide.github.io/)

---

## Support

For issues or questions:
- **GitHub**: https://github.com/Ravi-Wijerathne/meta_finder
- Open an issue on the repository

---

## Version History

- **v1.0.0** - Initial release
  - Windows installer and portable versions
  - Linux DEB, RPM, and portable versions
  - Support for Ubuntu, Linux Mint, Fedora, and universal Linux
  - Complete desktop integration for Linux
  - Comprehensive build system for both platforms

