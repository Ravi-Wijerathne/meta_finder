"""Image metadata extraction."""
import os

try:
    import exifread
    EXIFREAD_AVAILABLE = True
except ImportError:
    EXIFREAD_AVAILABLE = False

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def extract(file_path):
    """
    Extract metadata from image files.
    
    Args:
        file_path: Path to image file
        
    Returns:
        dict: Metadata dictionary
    """
    metadata = {}
    
    # Add basic file info
    metadata.update(get_basic_info(file_path))
    
    # Try PIL/Pillow first (more comprehensive)
    if PIL_AVAILABLE:
        metadata.update(extract_with_pil(file_path))
    
    # Try exifread as supplement or fallback
    if EXIFREAD_AVAILABLE:
        metadata.update(extract_with_exifread(file_path))
    
    return metadata


def get_basic_info(file_path):
    """Get basic file information."""
    stat = os.stat(file_path)
    return {
        'file_name': os.path.basename(file_path),
        'file_size_bytes': stat.st_size,
        'file_size_mb': round(stat.st_size / (1024 * 1024), 2),
    }


def extract_with_pil(file_path):
    """Extract using PIL/Pillow."""
    metadata = {}
    
    try:
        with Image.open(file_path) as img:
            # Basic image info
            metadata['image_format'] = img.format
            metadata['image_mode'] = img.mode
            metadata['image_width'] = img.width
            metadata['image_height'] = img.height
            metadata['image_size'] = f"{img.width}x{img.height}"
            
            # EXIF data
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    
                    # Handle GPS info specially
                    if tag_name == "GPSInfo":
                        gps_data = {}
                        for gps_tag_id, gps_value in value.items():
                            gps_tag_name = GPSTAGS.get(gps_tag_id, gps_tag_id)
                            gps_data[gps_tag_name] = str(gps_value)
                        metadata['gps_info'] = gps_data
                    else:
                        # Convert bytes to string
                        if isinstance(value, bytes):
                            try:
                                value = value.decode('utf-8', errors='ignore')
                            except:
                                value = str(value)
                        
                        metadata[f'exif_{tag_name}'] = str(value)
            
            # Additional info
            if hasattr(img, 'info'):
                for key, value in img.info.items():
                    if key not in ['exif', 'icc_profile']:  # Skip raw binary
                        metadata[f'info_{key}'] = str(value)
    
    except Exception as e:
        metadata['pil_error'] = str(e)
    
    return metadata


def extract_with_exifread(file_path):
    """Extract using exifread."""
    metadata = {}
    
    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
            
            for tag, value in tags.items():
                # Skip thumbnail data
                if 'thumbnail' not in tag.lower():
                    metadata[f'exifread_{tag}'] = str(value)
    
    except Exception as e:
        metadata['exifread_error'] = str(e)
    
    return metadata
