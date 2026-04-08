"""
Pytest configuration and shared fixtures for MetaFinder tests.
"""
import os
import sys
import tempfile
import shutil
import zipfile
import tarfile
import struct
import pytest

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    tmp = tempfile.mkdtemp(prefix="metafinder_test_")
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture
def sample_text_file(temp_dir):
    """Create a sample text file."""
    file_path = os.path.join(temp_dir, "sample.txt")
    content = "Hello, World!\nThis is a test file.\nLine 3 here."
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return file_path


@pytest.fixture
def sample_empty_file(temp_dir):
    """Create an empty file."""
    file_path = os.path.join(temp_dir, "empty.txt")
    with open(file_path, 'w') as f:
        pass
    return file_path


@pytest.fixture
def sample_binary_file(temp_dir):
    """Create a sample binary file."""
    file_path = os.path.join(temp_dir, "sample.bin")
    with open(file_path, 'wb') as f:
        f.write(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09')
    return file_path


@pytest.fixture
def sample_png_file(temp_dir):
    """Create a minimal valid PNG file (1x1 red pixel)."""
    file_path = os.path.join(temp_dir, "sample.png")
    # Minimal valid PNG: 1x1 red pixel
    png_data = (
        b'\x89PNG\r\n\x1a\n'  # PNG signature
        b'\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde'  # IHDR
        b'\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf\xc0\x00\x00\x00\x03\x00\x01\x00\x05\xfe\xd4'  # IDAT
        b'\x00\x00\x00\x00IEND\xaeB`\x82'  # IEND
    )
    with open(file_path, 'wb') as f:
        f.write(png_data)
    return file_path


@pytest.fixture
def sample_jpeg_file(temp_dir):
    """Create a minimal valid JPEG file."""
    file_path = os.path.join(temp_dir, "sample.jpg")
    # Minimal valid JPEG (1x1 pixel, no EXIF)
    jpeg_data = bytes([
        0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46, 0x00, 0x01,
        0x01, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0xFF, 0xDB, 0x00, 0x43,
        0x00, 0x08, 0x06, 0x06, 0x07, 0x06, 0x05, 0x08, 0x07, 0x07, 0x07, 0x09,
        0x09, 0x08, 0x0A, 0x0C, 0x14, 0x0D, 0x0C, 0x0B, 0x0B, 0x0C, 0x19, 0x12,
        0x13, 0x0F, 0x14, 0x1D, 0x1A, 0x1F, 0x1E, 0x1D, 0x1A, 0x1C, 0x1C, 0x20,
        0x24, 0x2E, 0x27, 0x20, 0x22, 0x2C, 0x23, 0x1C, 0x1C, 0x28, 0x37, 0x29,
        0x2C, 0x30, 0x31, 0x34, 0x34, 0x34, 0x1F, 0x27, 0x39, 0x3D, 0x38, 0x32,
        0x3C, 0x2E, 0x33, 0x34, 0x32, 0xFF, 0xC0, 0x00, 0x0B, 0x08, 0x00, 0x01,
        0x00, 0x01, 0x01, 0x01, 0x11, 0x00, 0xFF, 0xC4, 0x00, 0x1F, 0x00, 0x00,
        0x01, 0x05, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
        0x09, 0x0A, 0x0B, 0xFF, 0xC4, 0x00, 0xB5, 0x10, 0x00, 0x02, 0x01, 0x03,
        0x03, 0x02, 0x04, 0x03, 0x05, 0x05, 0x04, 0x04, 0x00, 0x00, 0x01, 0x7D,
        0x01, 0x02, 0x03, 0x00, 0x04, 0x11, 0x05, 0x12, 0x21, 0x31, 0x41, 0x06,
        0x13, 0x51, 0x61, 0x07, 0x22, 0x71, 0x14, 0x32, 0x81, 0x91, 0xA1, 0x08,
        0x23, 0x42, 0xB1, 0xC1, 0x15, 0x52, 0xD1, 0xF0, 0x24, 0x33, 0x62, 0x72,
        0x82, 0x09, 0x0A, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x25, 0x26, 0x27, 0x28,
        0x29, 0x2A, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x43, 0x44, 0x45,
        0x46, 0x47, 0x48, 0x49, 0x4A, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59,
        0x5A, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x73, 0x74, 0x75,
        0x76, 0x77, 0x78, 0x79, 0x7A, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89,
        0x8A, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9A, 0xA2, 0xA3,
        0xA4, 0xA5, 0xA6, 0xA7, 0xA8, 0xA9, 0xAA, 0xB2, 0xB3, 0xB4, 0xB5, 0xB6,
        0xB7, 0xB8, 0xB9, 0xBA, 0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8, 0xC9,
        0xCA, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9, 0xDA, 0xE1, 0xE2,
        0xE3, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8, 0xE9, 0xEA, 0xF1, 0xF2, 0xF3, 0xF4,
        0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA, 0xFF, 0xDA, 0x00, 0x08, 0x01, 0x01,
        0x00, 0x00, 0x3F, 0x00, 0xFB, 0xD5, 0xDB, 0x20, 0xA8, 0xF1, 0x85, 0xE3,
        0xE9, 0x40, 0xA5, 0x3D, 0xE3, 0xAB, 0x7F, 0xFF, 0xD9
    ])
    with open(file_path, 'wb') as f:
        f.write(jpeg_data)
    return file_path


@pytest.fixture
def sample_zip_file(temp_dir):
    """Create a sample ZIP file."""
    zip_path = os.path.join(temp_dir, "sample.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("file1.txt", "Content of file 1")
        zf.writestr("file2.txt", "Content of file 2")
        zf.writestr("subdir/file3.txt", "Content of file 3")
    return zip_path


@pytest.fixture
def sample_tar_file(temp_dir):
    """Create a sample TAR file."""
    tar_path = os.path.join(temp_dir, "sample.tar")
    txt_file = os.path.join(temp_dir, "tartest.txt")
    with open(txt_file, 'w') as f:
        f.write("Content for tar")
    with tarfile.open(tar_path, 'w') as tf:
        tf.add(txt_file, arcname="tartest.txt")
    return tar_path


@pytest.fixture
def sample_pdf_file(temp_dir):
    """Create a minimal valid PDF file."""
    file_path = os.path.join(temp_dir, "sample.pdf")
    # Minimal valid PDF
    pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT
/F1 12 Tf
100 700 Td
(Hello World) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000206 00000 n 
trailer
<< /Size 5 /Root 1 0 R >>
startxref
300
%%EOF"""
    with open(file_path, 'wb') as f:
        f.write(pdf_content)
    return file_path


@pytest.fixture
def non_existent_file(temp_dir):
    """Return a path to a file that doesn't exist."""
    return os.path.join(temp_dir, "does_not_exist.txt")


@pytest.fixture
def sample_mp3_file(temp_dir):
    """Create a minimal valid MP3 file with ID3 tags."""
    file_path = os.path.join(temp_dir, "sample.mp3")
    # Minimal MP3 with ID3v2 header and one frame
    # ID3v2.3 header
    id3_header = b'ID3\x03\x00\x00\x00\x00\x00\x00'
    # Minimal MP3 frame (silence)
    mp3_frame = bytes([
        0xFF, 0xFB, 0x90, 0x00,  # MP3 frame header
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ])
    # Repeat frame for valid duration
    mp3_data = id3_header + (mp3_frame * 100)
    with open(file_path, 'wb') as f:
        f.write(mp3_data)
    return file_path


@pytest.fixture
def corrupted_file(temp_dir):
    """Create a file with corrupted/random data."""
    file_path = os.path.join(temp_dir, "corrupted.jpg")
    # Start with JPEG magic bytes but corrupt the rest
    with open(file_path, 'wb') as f:
        f.write(b'\xFF\xD8\xFF' + b'\x00' * 100)
    return file_path


@pytest.fixture
def sample_metadata():
    """Return a sample metadata dictionary for testing."""
    return {
        'file_name': 'test.jpg',
        'file_size_bytes': 12345,
        'image_width': 1920,
        'image_height': 1080,
        'exif_Make': 'Canon',
        'exif_Model': 'EOS 5D',
    }


@pytest.fixture
def nested_metadata():
    """Return metadata with nested dictionary for testing."""
    return {
        'file_name': 'test.jpg',
        'gps_info': {
            'GPSLatitude': '51.5074',
            'GPSLongitude': '-0.1278',
        },
        'binary_data': b'\x00\x01\x02\x03',
        'list_data': ['item1', 'item2', 'item3'],
    }
