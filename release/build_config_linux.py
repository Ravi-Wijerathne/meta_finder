# MetaFinder Linux Build Configuration

VERSION = "1.0.0"
APP_NAME = "MetaFinder"
APP_NAME_LOWER = "metafinder"
AUTHOR = "Your Name"
AUTHOR_EMAIL = "your.email@example.com"
DESCRIPTION = "Universal Metadata Extraction Tool"
LONG_DESCRIPTION = """MetaFinder is a universal metadata extraction tool that can extract 
metadata from various file types including images, audio, video, documents, and archives."""
URL = "https://github.com/Ravi-Wijerathne/meta_finder"
ICON_PATH = "../assets/icon.png"  # Linux uses PNG for icons

# PyInstaller settings
ONEFILE = True
CONSOLE = False
WINDOWED = True

# Paths
MAIN_SCRIPT = "../main.py"
OUTPUT_DIR = "dist"
BUILD_DIR = "build"

# Files to include
ADDITIONAL_DATA = [
    ("../extractors", "extractors"),
    ("../utils", "utils"),
    ("../README.md", "."),
]

# Hidden imports (libraries that PyInstaller might miss)
HIDDEN_IMPORTS = [
    "PIL._tkinter_finder",
    "exifread",
    "mutagen",
    "hachoir",
    "hachoir.parser",
    "hachoir.metadata",
    "PyPDF2",
    "docx",
    "tinytag",
    "magic",
]

# DEB package settings
DEB_SECTION = "utils"
DEB_PRIORITY = "optional"
DEB_ARCHITECTURE = "amd64"
DEB_DEPENDS = "python3, python3-tk, libmagic1"

# RPM package settings
RPM_GROUP = "Applications/File"
RPM_LICENSE = "MIT"
RPM_REQUIRES = "python3, python3-tkinter, file-libs"

# Desktop entry
DESKTOP_CATEGORIES = "Utility;FileTools;"
DESKTOP_KEYWORDS = "metadata;extractor;exif;tags;"
