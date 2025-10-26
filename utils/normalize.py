"""Metadata normalization utilities."""
from datetime import datetime


def normalize_metadata(metadata_dict, file_path, mime_type):
    """
    Convert metadata dictionary to readable text format.
    
    Args:
        metadata_dict: Dictionary containing metadata
        file_path: Original file path
        mime_type: MIME type of the file
        
    Returns:
        str: Formatted text representation
    """
    lines = []
    lines.append("=" * 80)
    lines.append("METADATA EXTRACTION REPORT")
    lines.append("=" * 80)
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"File: {file_path}")
    lines.append(f"MIME Type: {mime_type}")
    lines.append("=" * 80)
    lines.append("")
    
    if not metadata_dict:
        lines.append("⚠️  No metadata found or unable to extract metadata.")
        return "\n".join(lines)
    
    # Sort keys for consistent output
    for key in sorted(metadata_dict.keys()):
        value = metadata_dict[key]
        
        # Format the value
        if isinstance(value, (list, tuple)):
            value_str = ", ".join(str(v) for v in value)
        elif isinstance(value, dict):
            value_str = format_nested_dict(value)
        elif isinstance(value, bytes):
            value_str = f"<binary data: {len(value)} bytes>"
        else:
            value_str = str(value)
        
        # Clean up key names
        key_formatted = key.replace('_', ' ').title()
        
        lines.append(f"{key_formatted}: {value_str}")
    
    lines.append("")
    lines.append("=" * 80)
    lines.append(f"Total metadata fields: {len(metadata_dict)}")
    lines.append("=" * 80)
    
    return "\n".join(lines)


def format_nested_dict(d, indent=2):
    """Format nested dictionary for display."""
    lines = []
    for key, value in d.items():
        if isinstance(value, dict):
            lines.append(f"\n{' ' * indent}{key}:")
            lines.append(format_nested_dict(value, indent + 2))
        else:
            lines.append(f"\n{' ' * indent}{key}: {value}")
    return "".join(lines)
