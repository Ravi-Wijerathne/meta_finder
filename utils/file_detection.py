"""File type detection utilities."""
import os
import mimetypes

try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False
    print("⚠️  python-magic not available, falling back to mimetypes")


def detect_type(file_path):
    """
    Detect the MIME type of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        str: MIME type (e.g., 'image/jpeg', 'audio/mpeg')
    """
    if not os.path.exists(file_path):
        return "unknown/unknown"
    
    # Try python-magic first (most reliable)
    if MAGIC_AVAILABLE:
        try:
            mime = magic.Magic(mime=True)
            return mime.from_file(file_path)
        except Exception as e:
            print(f"⚠️  Magic detection failed: {e}")
    
    # Fallback to mimetypes (extension-based)
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        return mime_type
    
    # Last resort
    return "application/octet-stream"


def get_file_category(mime_type):
    """
    Categorize a MIME type into broad categories.
    
    Args:
        mime_type: MIME type string
        
    Returns:
        str: Category ('image', 'audio', 'video', 'document', 'archive', 'other')
    """
    if not mime_type:
        return 'other'
    
    mime_lower = mime_type.lower()
    
    if mime_lower.startswith('image/'):
        return 'image'
    elif mime_lower.startswith('audio/'):
        return 'audio'
    elif mime_lower.startswith('video/'):
        return 'video'
    elif any(x in mime_lower for x in ['pdf', 'word', 'document', 'text', 'officedocument']):
        return 'document'
    elif any(x in mime_lower for x in ['zip', 'rar', '7z', 'tar', 'gzip', 'compress']):
        return 'archive'
    else:
        return 'other'
