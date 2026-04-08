"""
Tests for utils/text_writer.py
"""
import os
import pytest
from utils.text_writer import save_metadata, generate_output_filename


class TestSaveMetadata:
    """Tests for save_metadata function."""
    
    def test_save_basic_content(self, temp_dir):
        """Test saving basic text content."""
        output_path = os.path.join(temp_dir, "output.txt")
        content = "Test metadata content"
        
        result = save_metadata(content, output_path)
        
        assert result is True
        assert os.path.exists(output_path)
        
        with open(output_path, 'r', encoding='utf-8') as f:
            saved_content = f.read()
        assert saved_content == content
    
    def test_save_unicode_content(self, temp_dir):
        """Test saving Unicode content."""
        output_path = os.path.join(temp_dir, "unicode_output.txt")
        content = "Unicode: 日本語 Ünïcödé 中文"
        
        result = save_metadata(content, output_path)
        
        assert result is True
        with open(output_path, 'r', encoding='utf-8') as f:
            saved_content = f.read()
        assert saved_content == content
    
    def test_save_empty_content(self, temp_dir):
        """Test saving empty content."""
        output_path = os.path.join(temp_dir, "empty_output.txt")
        
        result = save_metadata("", output_path)
        
        assert result is True
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) == 0
    
    def test_save_multiline_content(self, temp_dir):
        """Test saving multiline content."""
        output_path = os.path.join(temp_dir, "multiline.txt")
        content = "Line 1\nLine 2\nLine 3\n"
        
        result = save_metadata(content, output_path)
        
        assert result is True
        with open(output_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        assert len(lines) == 3  # 3 lines (trailing newline doesn't create extra line)
    
    def test_save_creates_parent_directory(self, temp_dir):
        """Test that parent directories are created if needed."""
        output_path = os.path.join(temp_dir, "subdir", "nested", "output.txt")
        content = "Content in nested directory"
        
        result = save_metadata(content, output_path)
        
        assert result is True
        assert os.path.exists(output_path)
    
    def test_save_overwrites_existing_file(self, temp_dir):
        """Test that existing files are overwritten."""
        output_path = os.path.join(temp_dir, "existing.txt")
        
        # Create initial file
        with open(output_path, 'w') as f:
            f.write("Original content")
        
        # Overwrite with new content
        new_content = "New content"
        result = save_metadata(new_content, output_path)
        
        assert result is True
        with open(output_path, 'r', encoding='utf-8') as f:
            saved_content = f.read()
        assert saved_content == new_content
    
    def test_save_special_characters(self, temp_dir):
        """Test saving content with special characters."""
        output_path = os.path.join(temp_dir, "special.txt")
        content = "Special chars: <>&'\"\t\n"
        
        result = save_metadata(content, output_path)
        
        assert result is True
        with open(output_path, 'r', encoding='utf-8') as f:
            saved_content = f.read()
        # Compare without carriage return issues on Windows
        assert saved_content.strip() == content.strip()
    
    def test_save_large_content(self, temp_dir):
        """Test saving large content."""
        output_path = os.path.join(temp_dir, "large.txt")
        content = "x" * 1000000  # 1MB of content
        
        result = save_metadata(content, output_path)
        
        assert result is True
        assert os.path.getsize(output_path) == 1000000


class TestGenerateOutputFilename:
    """Tests for generate_output_filename function."""
    
    def test_basic_filename_generation(self):
        """Test basic output filename generation."""
        result = generate_output_filename("/path/to/image.jpg")
        assert result == "/path/to/image_metadata.txt"
    
    def test_filename_with_multiple_dots(self):
        """Test filename with multiple dots."""
        result = generate_output_filename("/path/to/my.photo.2023.jpg")
        assert result == "/path/to/my.photo.2023_metadata.txt"
    
    def test_filename_without_extension(self):
        """Test filename without extension."""
        result = generate_output_filename("/path/to/file")
        assert result == "/path/to/file_metadata.txt"
    
    def test_filename_with_spaces(self):
        """Test filename with spaces."""
        result = generate_output_filename("/path/to/my file.jpg")
        assert result == "/path/to/my file_metadata.txt"
    
    def test_windows_path(self):
        """Test Windows-style path."""
        result = generate_output_filename("C:\\Users\\test\\image.jpg")
        assert result == "C:\\Users\\test\\image_metadata.txt"
    
    def test_relative_path(self):
        """Test relative path."""
        result = generate_output_filename("./images/photo.png")
        assert result == "./images/photo_metadata.txt"
    
    def test_filename_only(self):
        """Test filename without directory."""
        result = generate_output_filename("document.pdf")
        assert result == "document_metadata.txt"
    
    def test_hidden_file(self):
        """Test hidden file (starting with dot)."""
        result = generate_output_filename("/path/to/.hidden.txt")
        assert result == "/path/to/.hidden_metadata.txt"
