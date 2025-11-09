# MetaFinder Build Configuration

VERSION = "1.0.0"
APP_NAME = "MetaFinder"
AUTHOR = "Your Name"
DESCRIPTION = "Universal Metadata Extraction Tool"
ICON_PATH = "../assets/icon.ico"  # You'll need to create this

# PyInstaller settings
ONEFILE = True
CONSOLE = False  # Set to True for debugging
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
