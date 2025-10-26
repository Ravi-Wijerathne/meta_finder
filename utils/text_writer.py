"""Text file writing utilities."""
import os


def save_metadata(text_content, output_path):
    """
    Save metadata text to a file.
    
    Args:
        text_content: String content to write
        output_path: Output file path
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Write with UTF-8 encoding to handle special characters
        with open(output_path, 'w', encoding='utf-8', errors='replace') as f:
            f.write(text_content)
        
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False


def generate_output_filename(input_path):
    """
    Generate an appropriate output filename based on input.
    
    Args:
        input_path: Path to input file
        
    Returns:
        str: Output path with .txt extension
    """
    base = os.path.splitext(input_path)[0]
    return f"{base}_metadata.txt"
