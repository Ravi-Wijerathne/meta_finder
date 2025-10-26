"""Generic metadata extraction for unknown file types."""
import os
import hashlib

try:
    from hachoir.parser import createParser
    from hachoir.metadata import extractMetadata
    HACHOIR_AVAILABLE = True
except ImportError:
    HACHOIR_AVAILABLE = False


def extract(file_path):
    """
    Extract generic metadata from any file.
    
    Args:
        file_path: Path to file
        
    Returns:
        dict: Metadata dictionary
    """
    metadata = {}
    
    # Basic file info
    metadata.update(get_basic_info(file_path))
    
    # File hashes
    metadata.update(calculate_hashes(file_path))
    
    # Try hachoir for binary inspection
    if HACHOIR_AVAILABLE:
        metadata.update(extract_with_hachoir(file_path))
    
    # File header inspection
    metadata.update(inspect_header(file_path))
    
    return metadata


def get_basic_info(file_path):
    """Get basic file information."""
    stat = os.stat(file_path)
    
    metadata = {
        'file_name': os.path.basename(file_path),
        'file_extension': os.path.splitext(file_path)[1],
        'file_size_bytes': stat.st_size,
        'file_size_kb': round(stat.st_size / 1024, 2),
        'file_size_mb': round(stat.st_size / (1024 * 1024), 2),
        'creation_time': str(stat.st_ctime),
        'modification_time': str(stat.st_mtime),
        'access_time': str(stat.st_atime),
    }
    
    return metadata


def calculate_hashes(file_path, max_size=100 * 1024 * 1024):
    """Calculate file hashes (skip for very large files)."""
    metadata = {}
    
    try:
        file_size = os.path.getsize(file_path)
        
        if file_size > max_size:
            metadata['hash_note'] = f"File too large ({file_size} bytes), skipping hash calculation"
            return metadata
        
        # Calculate MD5 and SHA256
        md5_hash = hashlib.md5()
        sha256_hash = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
                sha256_hash.update(chunk)
        
        metadata['md5_hash'] = md5_hash.hexdigest()
        metadata['sha256_hash'] = sha256_hash.hexdigest()
    
    except Exception as e:
        metadata['hash_error'] = str(e)
    
    return metadata


def extract_with_hachoir(file_path):
    """Extract using hachoir parser."""
    metadata = {}
    
    try:
        parser = createParser(file_path)
        if parser:
            meta = extractMetadata(parser)
            if meta:
                for line in meta.exportPlaintext():
                    if ': ' in line:
                        key, value = line.split(': ', 1)
                        metadata[f'hachoir_{key.strip()}'] = value.strip()
            parser.stream._input.close()
    
    except Exception as e:
        metadata['hachoir_error'] = str(e)
    
    return metadata


def inspect_header(file_path, header_size=16):
    """Inspect file header/magic bytes."""
    metadata = {}
    
    try:
        with open(file_path, 'rb') as f:
            header = f.read(header_size)
        
        # Hex representation
        hex_header = ' '.join(f'{b:02x}' for b in header)
        metadata['file_header_hex'] = hex_header
        
        # ASCII representation (printable only)
        ascii_header = ''.join(chr(b) if 32 <= b < 127 else '.' for b in header)
        metadata['file_header_ascii'] = ascii_header
        
        # Identify common formats by magic bytes
        magic_signatures = {
            b'\xFF\xD8\xFF': 'JPEG image',
            b'\x89PNG': 'PNG image',
            b'GIF8': 'GIF image',
            b'%PDF': 'PDF document',
            b'PK\x03\x04': 'ZIP archive',
            b'\x1f\x8b': 'GZIP compressed',
            b'Rar!': 'RAR archive',
            b'7z\xbc\xaf': '7-Zip archive',
            b'ID3': 'MP3 audio',
            b'\x00\x00\x00\x18ftypmp42': 'MP4 video',
        }
        
        for signature, description in magic_signatures.items():
            if header.startswith(signature):
                metadata['identified_format'] = description
                break
    
    except Exception as e:
        metadata['header_error'] = str(e)
    
    return metadata
