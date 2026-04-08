"""
Edge case tests for MetaFinder.
"""
import os
import stat
import pytest
from extractors import (
    image_extractor,
    audio_extractor,
    video_extractor,
    document_extractor,
    archive_extractor,
    generic_extractor
)
from utils.file_detection import detect_type, get_file_category
from utils.normalize import normalize_metadata
from utils.text_writer import save_metadata


class TestNonExistentFiles:
    """Test handling of non-existent files."""
    
    def test_detect_type_non_existent(self, non_existent_file):
        """Test detect_type with non-existent file."""
        result = detect_type(non_existent_file)
        assert result == "unknown/unknown"
    
    def test_image_extractor_non_existent(self, non_existent_file):
        """Test image extractor with non-existent file."""
        with pytest.raises((FileNotFoundError, OSError)):
            image_extractor.extract(non_existent_file)
    
    def test_generic_extractor_non_existent(self, non_existent_file):
        """Test generic extractor with non-existent file."""
        with pytest.raises((FileNotFoundError, OSError)):
            generic_extractor.extract(non_existent_file)


class TestEmptyFiles:
    """Test handling of empty files."""
    
    def test_empty_file_detection(self, sample_empty_file):
        """Test type detection of empty file."""
        result = detect_type(sample_empty_file)
        assert result is not None
    
    def test_empty_file_extraction(self, sample_empty_file):
        """Test extraction from empty file."""
        result = generic_extractor.extract(sample_empty_file)
        
        assert isinstance(result, dict)
        assert result['file_size_bytes'] == 0
    
    def test_empty_file_hash(self, sample_empty_file):
        """Test hash calculation for empty file."""
        result = generic_extractor.calculate_hashes(sample_empty_file)
        
        # MD5 of empty string is known
        assert result['md5_hash'] == 'd41d8cd98f00b204e9800998ecf8427e'


class TestCorruptedFiles:
    """Test handling of corrupted files."""
    
    def test_corrupted_image_extraction(self, corrupted_file):
        """Test image extraction from corrupted file."""
        result = image_extractor.extract(corrupted_file)
        
        # Should not crash, return dict with basic info
        assert isinstance(result, dict)
        assert 'file_name' in result
    
    def test_corrupted_file_header_inspection(self, corrupted_file):
        """Test header inspection on corrupted file."""
        result = generic_extractor.inspect_header(corrupted_file)
        
        assert isinstance(result, dict)
        assert 'file_header_hex' in result


class TestSpecialCharactersInPaths:
    """Test handling of special characters in file paths."""
    
    def test_unicode_filename(self, temp_dir):
        """Test file with Unicode characters in name."""
        unicode_file = os.path.join(temp_dir, "тест_文件_🎉.txt")
        with open(unicode_file, 'w', encoding='utf-8') as f:
            f.write("Unicode test content")
        
        result = generic_extractor.extract(unicode_file)
        
        assert isinstance(result, dict)
        assert 'file_name' in result
    
    def test_spaces_in_filename(self, temp_dir):
        """Test file with spaces in name."""
        space_file = os.path.join(temp_dir, "file with spaces.txt")
        with open(space_file, 'w') as f:
            f.write("Content")
        
        result = generic_extractor.extract(space_file)
        
        assert isinstance(result, dict)
        assert result['file_name'] == "file with spaces.txt"
    
    def test_special_chars_in_filename(self, temp_dir):
        """Test file with special characters in name."""
        special_file = os.path.join(temp_dir, "file-with_special.chars(1).txt")
        with open(special_file, 'w') as f:
            f.write("Content")
        
        result = generic_extractor.extract(special_file)
        
        assert isinstance(result, dict)


class TestLargeFiles:
    """Test handling of large files."""
    
    def test_large_file_basic_info(self, temp_dir):
        """Test basic info extraction from large file."""
        large_file = os.path.join(temp_dir, "large.bin")
        size = 10 * 1024 * 1024  # 10MB
        
        with open(large_file, 'wb') as f:
            f.write(b'\x00' * size)
        
        result = generic_extractor.get_basic_info(large_file)
        
        assert result['file_size_bytes'] == size
        assert result['file_size_mb'] == 10.0


class TestMetadataEdgeCases:
    """Test edge cases in metadata normalization."""
    
    def test_normalize_with_none_values(self):
        """Test normalization with None values in metadata."""
        metadata = {
            'field1': None,
            'field2': 'value',
            'field3': None,
        }
        
        result = normalize_metadata(metadata, '/path/test.txt', 'text/plain')
        
        assert isinstance(result, str)
        assert 'None' in result
    
    def test_normalize_with_very_long_values(self):
        """Test normalization with very long values."""
        metadata = {
            'long_field': 'x' * 10000,
        }
        
        result = normalize_metadata(metadata, '/path/test.txt', 'text/plain')
        
        assert isinstance(result, str)
        assert 'x' * 100 in result  # At least part of long value
    
    def test_normalize_with_special_key_names(self):
        """Test normalization with unusual key names."""
        metadata = {
            '': 'empty_key_value',
            '  spaces  ': 'value',
            'key:with:colons': 'value',
        }
        
        result = normalize_metadata(metadata, '/path/test.txt', 'text/plain')
        
        assert isinstance(result, str)


class TestOutputWriteEdgeCases:
    """Test edge cases in file writing."""
    
    def test_write_to_invalid_path(self, temp_dir):
        """Test handling of write failure with invalid path."""
        # Use a path with invalid characters on Windows
        import sys
        if sys.platform == 'win32':
            # Windows: use path with invalid characters
            invalid_path = "Z:\\nonexistent_drive_xyz\\file.txt"
        else:
            invalid_path = "/nonexistent/path/to/file.txt"
        
        result = save_metadata("content", invalid_path)
        # On some systems this may succeed if the directory is created
        # Just verify it doesn't crash
        assert isinstance(result, bool)
    
    def test_output_path_with_unicode(self, temp_dir):
        """Test writing to path with Unicode characters."""
        output_path = os.path.join(temp_dir, "выход_输出.txt")
        
        result = save_metadata("Test content", output_path)
        
        assert result is True
        assert os.path.exists(output_path)


class TestExtractorFallbacks:
    """Test extractor fallback behavior when libraries unavailable."""
    
    def test_image_extractor_returns_basic_info_always(self, sample_png_file):
        """Test image extractor always returns basic file info."""
        result = image_extractor.extract(sample_png_file)
        
        # Basic info should always be present
        assert 'file_name' in result
        assert 'file_size_bytes' in result
    
    def test_audio_extractor_returns_basic_info_always(self, sample_mp3_file):
        """Test audio extractor always returns basic file info."""
        result = audio_extractor.extract(sample_mp3_file)
        
        assert 'file_name' in result
        assert 'file_size_bytes' in result
    
    def test_document_extractor_returns_basic_info_always(self, sample_text_file):
        """Test document extractor always returns basic file info."""
        result = document_extractor.extract(sample_text_file)
        
        assert 'file_name' in result
        assert 'file_size_bytes' in result


class TestBoundaryConditions:
    """Test boundary conditions and limits."""
    
    def test_very_small_file(self, temp_dir):
        """Test extraction from 1-byte file."""
        tiny_file = os.path.join(temp_dir, "tiny.bin")
        with open(tiny_file, 'wb') as f:
            f.write(b'X')
        
        result = generic_extractor.extract(tiny_file)
        
        assert result['file_size_bytes'] == 1
    
    def test_file_with_no_extension(self, temp_dir):
        """Test file without extension."""
        no_ext_file = os.path.join(temp_dir, "noextension")
        with open(no_ext_file, 'w') as f:
            f.write("Content")
        
        result = generic_extractor.extract(no_ext_file)
        
        assert result['file_extension'] == ''
    
    def test_hidden_file(self, temp_dir):
        """Test hidden file (starting with dot)."""
        hidden_file = os.path.join(temp_dir, ".hidden")
        with open(hidden_file, 'w') as f:
            f.write("Hidden content")
        
        result = generic_extractor.extract(hidden_file)
        
        assert result['file_name'] == '.hidden'
