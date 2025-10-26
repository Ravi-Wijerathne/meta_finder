"""Audio metadata extraction."""
import os

try:
    from mutagen import File as MutagenFile
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False

try:
    from tinytag import TinyTag
    TINYTAG_AVAILABLE = True
except ImportError:
    TINYTAG_AVAILABLE = False


def extract(file_path):
    """
    Extract metadata from audio files.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        dict: Metadata dictionary
    """
    metadata = {}
    
    # Add basic file info
    metadata.update(get_basic_info(file_path))
    
    # Try mutagen (more comprehensive)
    if MUTAGEN_AVAILABLE:
        metadata.update(extract_with_mutagen(file_path))
    
    # Try tinytag as supplement or fallback
    if TINYTAG_AVAILABLE:
        metadata.update(extract_with_tinytag(file_path))
    
    return metadata


def get_basic_info(file_path):
    """Get basic file information."""
    stat = os.stat(file_path)
    return {
        'file_name': os.path.basename(file_path),
        'file_size_bytes': stat.st_size,
        'file_size_mb': round(stat.st_size / (1024 * 1024), 2),
    }


def extract_with_mutagen(file_path):
    """Extract using mutagen."""
    metadata = {}
    
    try:
        audio = MutagenFile(file_path)
        
        if audio is None:
            metadata['mutagen_error'] = "Unable to read file"
            return metadata
        
        # Audio properties
        if hasattr(audio, 'info'):
            info = audio.info
            metadata['duration_seconds'] = round(info.length, 2) if hasattr(info, 'length') else None
            metadata['bitrate'] = info.bitrate if hasattr(info, 'bitrate') else None
            metadata['sample_rate'] = info.sample_rate if hasattr(info, 'sample_rate') else None
            metadata['channels'] = info.channels if hasattr(info, 'channels') else None
            
            # Format-specific info
            for attr in dir(info):
                if not attr.startswith('_'):
                    try:
                        value = getattr(info, attr)
                        if not callable(value) and value is not None:
                            metadata[f'audio_{attr}'] = str(value)
                    except:
                        pass
        
        # Tags/Metadata
        if audio.tags:
            for key, value in audio.tags.items():
                # Handle different tag formats
                if isinstance(value, list):
                    value_str = ", ".join(str(v) for v in value)
                else:
                    value_str = str(value)
                
                metadata[f'tag_{key}'] = value_str
    
    except Exception as e:
        metadata['mutagen_error'] = str(e)
    
    return metadata


def extract_with_tinytag(file_path):
    """Extract using tinytag."""
    metadata = {}
    
    try:
        tag = TinyTag.get(file_path)
        
        # Map common fields
        fields = {
            'artist': tag.artist,
            'album': tag.album,
            'title': tag.title,
            'track': tag.track,
            'year': tag.year,
            'genre': tag.genre,
            'comment': tag.comment,
            'albumartist': tag.albumartist,
            'composer': tag.composer,
            'disc': tag.disc,
            'duration': tag.duration,
            'bitrate': tag.bitrate,
            'samplerate': tag.samplerate,
            'channels': tag.channels,
        }
        
        for key, value in fields.items():
            if value is not None:
                metadata[f'tinytag_{key}'] = str(value)
    
    except Exception as e:
        metadata['tinytag_error'] = str(e)
    
    return metadata
