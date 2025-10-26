"""Archive metadata extraction."""
import os
import zipfile
import tarfile

try:
    import py7zr
    PY7ZR_AVAILABLE = True
except ImportError:
    PY7ZR_AVAILABLE = False


def extract(file_path):
    """
    Extract metadata from archive files.
    
    Args:
        file_path: Path to archive file
        
    Returns:
        dict: Metadata dictionary
    """
    metadata = {}
    
    # Add basic file info
    metadata.update(get_basic_info(file_path))
    
    # Determine archive type
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.zip':
        metadata.update(extract_zip(file_path))
    elif ext in ['.tar', '.gz', '.bz2', '.xz']:
        metadata.update(extract_tar(file_path))
    elif ext == '.7z' and PY7ZR_AVAILABLE:
        metadata.update(extract_7z(file_path))
    else:
        metadata['note'] = f"No specific extractor for {ext} archives"
    
    return metadata


def get_basic_info(file_path):
    """Get basic file information."""
    stat = os.stat(file_path)
    return {
        'file_name': os.path.basename(file_path),
        'file_size_bytes': stat.st_size,
        'file_size_mb': round(stat.st_size / (1024 * 1024), 2),
    }


def extract_zip(file_path):
    """Extract ZIP metadata."""
    metadata = {}
    
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            info_list = zf.infolist()
            metadata['num_files'] = len(info_list)
            metadata['compression_type'] = 'ZIP'
            
            # Calculate total uncompressed size
            total_uncompressed = sum(info.file_size for info in info_list)
            metadata['total_uncompressed_size_mb'] = round(total_uncompressed / (1024 * 1024), 2)
            
            # Compression ratio
            if total_uncompressed > 0:
                stat = os.stat(file_path)
                ratio = (1 - stat.st_size / total_uncompressed) * 100
                metadata['compression_ratio_percent'] = round(ratio, 2)
            
            # List files (limit to first 50)
            file_list = [info.filename for info in info_list[:50]]
            metadata['file_list'] = ", ".join(file_list)
            
            if len(info_list) > 50:
                metadata['file_list_note'] = f"... and {len(info_list) - 50} more files"
    
    except Exception as e:
        metadata['zip_error'] = str(e)
    
    return metadata


def extract_tar(file_path):
    """Extract TAR metadata."""
    metadata = {}
    
    try:
        # Determine compression
        if file_path.endswith('.tar.gz') or file_path.endswith('.tgz'):
            mode = 'r:gz'
        elif file_path.endswith('.tar.bz2'):
            mode = 'r:bz2'
        elif file_path.endswith('.tar.xz'):
            mode = 'r:xz'
        else:
            mode = 'r'
        
        with tarfile.open(file_path, mode) as tf:
            members = tf.getmembers()
            metadata['num_files'] = len(members)
            metadata['compression_type'] = 'TAR'
            
            # Calculate total uncompressed size
            total_uncompressed = sum(m.size for m in members)
            metadata['total_uncompressed_size_mb'] = round(total_uncompressed / (1024 * 1024), 2)
            
            # List files (limit to first 50)
            file_list = [m.name for m in members[:50]]
            metadata['file_list'] = ", ".join(file_list)
            
            if len(members) > 50:
                metadata['file_list_note'] = f"... and {len(members) - 50} more files"
    
    except Exception as e:
        metadata['tar_error'] = str(e)
    
    return metadata


def extract_7z(file_path):
    """Extract 7Z metadata."""
    metadata = {}
    
    try:
        with py7zr.SevenZipFile(file_path, 'r') as zf:
            file_list = zf.getnames()
            metadata['num_files'] = len(file_list)
            metadata['compression_type'] = '7Z'
            
            # List files (limit to first 50)
            metadata['file_list'] = ", ".join(file_list[:50])
            
            if len(file_list) > 50:
                metadata['file_list_note'] = f"... and {len(file_list) - 50} more files"
    
    except Exception as e:
        metadata['7z_error'] = str(e)
    
    return metadata
