"""Video metadata extraction."""
import os
import subprocess
import json
import shutil

try:
    from hachoir.parser import createParser
    from hachoir.metadata import extractMetadata
    HACHOIR_AVAILABLE = True
except ImportError:
    HACHOIR_AVAILABLE = False


def extract(file_path):
    """
    Extract metadata from video files.
    
    Args:
        file_path: Path to video file
        
    Returns:
        dict: Metadata dictionary
    """
    metadata = {}
    
    # Add basic file info
    metadata.update(get_basic_info(file_path))
    
    # Try ffprobe first (most comprehensive for video)
    ffprobe_data = extract_with_ffprobe(file_path)
    if ffprobe_data:
        metadata.update(ffprobe_data)
    
    # Try hachoir as fallback
    if HACHOIR_AVAILABLE:
        metadata.update(extract_with_hachoir(file_path))
    
    return metadata


def get_basic_info(file_path):
    """Get basic file information."""
    stat = os.stat(file_path)
    return {
        'file_name': os.path.basename(file_path),
        'file_size_bytes': stat.st_size,
        'file_size_mb': round(stat.st_size / (1024 * 1024), 2),
    }


def extract_with_ffprobe(file_path):
    """Extract using ffprobe (from FFmpeg)."""
    metadata = {}
    
    try:
        # Find ffprobe in PATH
        ffprobe_path = shutil.which('ffprobe')
        
        if not ffprobe_path:
            # Try common installation paths on Windows
            common_paths = [
                r'C:\ffmpeg\bin\ffprobe.exe',
                r'C:\Program Files\ffmpeg\bin\ffprobe.exe',
                os.path.expanduser(r'~\scoop\apps\ffmpeg\current\bin\ffprobe.exe'),
                os.path.expanduser(r'~\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-full_build\bin\ffprobe.exe'),
            ]
            
            # Also search in WinGet packages folder dynamically
            winget_packages = os.path.expanduser(r'~\AppData\Local\Microsoft\WinGet\Packages')
            if os.path.exists(winget_packages):
                for item in os.listdir(winget_packages):
                    if 'FFmpeg' in item:
                        for root, dirs, files in os.walk(os.path.join(winget_packages, item)):
                            if 'ffprobe.exe' in files:
                                common_paths.insert(0, os.path.join(root, 'ffprobe.exe'))
            
            for path in common_paths:
                if os.path.exists(path):
                    ffprobe_path = path
                    break
        
        if not ffprobe_path:
            metadata['ffprobe_note'] = "ffprobe not found (install FFmpeg for detailed video metadata)"
            return metadata
        
        # Run ffprobe
        cmd = [
            ffprobe_path,
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            file_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            
            # Format info
            if 'format' in data:
                fmt = data['format']
                metadata['format_name'] = fmt.get('format_name', '')
                metadata['format_long_name'] = fmt.get('format_long_name', '')
                metadata['duration'] = fmt.get('duration', '')
                metadata['size'] = fmt.get('size', '')
                metadata['bit_rate'] = fmt.get('bit_rate', '')
                
                # Tags
                if 'tags' in fmt:
                    for key, value in fmt['tags'].items():
                        metadata[f'tag_{key}'] = value
            
            # Stream info
            if 'streams' in data:
                for i, stream in enumerate(data['streams']):
                    prefix = f"stream_{i}_{stream.get('codec_type', 'unknown')}"
                    metadata[f'{prefix}_codec'] = stream.get('codec_name', '')
                    metadata[f'{prefix}_codec_long'] = stream.get('codec_long_name', '')
                    
                    if stream.get('codec_type') == 'video':
                        metadata[f'{prefix}_width'] = stream.get('width', '')
                        metadata[f'{prefix}_height'] = stream.get('height', '')
                        metadata[f'{prefix}_fps'] = stream.get('r_frame_rate', '')
                        metadata[f'{prefix}_aspect_ratio'] = stream.get('display_aspect_ratio', '')
                    elif stream.get('codec_type') == 'audio':
                        metadata[f'{prefix}_sample_rate'] = stream.get('sample_rate', '')
                        metadata[f'{prefix}_channels'] = stream.get('channels', '')
    
    except FileNotFoundError:
        metadata['ffprobe_note'] = "ffprobe not found (install FFmpeg for detailed video metadata)"
    except subprocess.TimeoutExpired:
        metadata['ffprobe_error'] = "Timeout while processing video"
    except Exception as e:
        metadata['ffprobe_error'] = str(e)
    
    return metadata


def extract_with_hachoir(file_path):
    """Extract using hachoir."""
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
