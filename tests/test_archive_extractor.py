"""
Tests for extractors/archive_extractor.py
"""
import os
import zipfile
import tarfile
import pytest
from extractors import archive_extractor


class TestArchiveExtractor:
    """Tests for archive_extractor module."""
    
    def test_extract_zip(self, sample_zip_file):
        """Test extraction from ZIP file."""
        result = archive_extractor.extract(sample_zip_file)
        
        assert isinstance(result, dict)
        assert 'file_name' in result
        assert 'num_files' in result
        assert result['num_files'] == 3
        assert 'compression_type' in result
        assert result['compression_type'] == 'ZIP'
    
    def test_extract_zip_file_list(self, sample_zip_file):
        """Test that file list is included."""
        result = archive_extractor.extract(sample_zip_file)
        
        assert 'file_list' in result
        assert 'file1.txt' in result['file_list']
        assert 'file2.txt' in result['file_list']
    
    def test_extract_tar(self, sample_tar_file):
        """Test extraction from TAR file."""
        result = archive_extractor.extract(sample_tar_file)
        
        assert isinstance(result, dict)
        assert 'file_name' in result
        assert 'num_files' in result
        assert 'compression_type' in result
        assert result['compression_type'] == 'TAR'
    
    def test_basic_info_extraction(self, sample_zip_file):
        """Test get_basic_info function."""
        result = archive_extractor.get_basic_info(sample_zip_file)
        
        assert 'file_name' in result
        assert 'file_size_bytes' in result
        assert 'file_size_mb' in result
    
    def test_extract_zip_function(self, sample_zip_file):
        """Test extract_zip function directly."""
        result = archive_extractor.extract_zip(sample_zip_file)
        
        assert 'num_files' in result
        assert 'compression_type' in result
        assert 'file_list' in result
    
    def test_extract_tar_function(self, sample_tar_file):
        """Test extract_tar function directly."""
        result = archive_extractor.extract_tar(sample_tar_file)
        
        assert 'num_files' in result
        assert 'compression_type' in result
    
    def test_extract_zip_compression_ratio(self, sample_zip_file):
        """Test compression ratio calculation."""
        result = archive_extractor.extract(sample_zip_file)
        
        assert 'total_uncompressed_size_mb' in result
        # Compression ratio may or may not be present depending on content
    
    def test_extract_unknown_archive_type(self, temp_dir):
        """Test extraction from unknown archive type."""
        unknown_file = os.path.join(temp_dir, "archive.rar")
        with open(unknown_file, 'wb') as f:
            f.write(b'Rar!\x1a\x07\x00')  # RAR magic bytes
        
        result = archive_extractor.extract(unknown_file)
        
        assert isinstance(result, dict)
        assert 'note' in result or 'file_name' in result
    
    def test_extract_non_archive_file(self, sample_text_file):
        """Test extraction from non-archive file."""
        result = archive_extractor.extract(sample_text_file)
        
        # Should handle gracefully
        assert isinstance(result, dict)
        assert 'file_name' in result


class TestZipExtraction:
    """Specific tests for ZIP extraction."""
    
    def test_large_zip_file_list_truncation(self, temp_dir):
        """Test that large file lists are truncated."""
        large_zip = os.path.join(temp_dir, "large.zip")
        
        with zipfile.ZipFile(large_zip, 'w') as zf:
            for i in range(100):
                zf.writestr(f"file_{i:03d}.txt", f"Content {i}")
        
        result = archive_extractor.extract_zip(large_zip)
        
        # File list should be limited
        assert 'file_list_note' in result
        assert '50 more files' in result['file_list_note']
    
    def test_empty_zip(self, temp_dir):
        """Test extraction from empty ZIP."""
        empty_zip = os.path.join(temp_dir, "empty.zip")
        with zipfile.ZipFile(empty_zip, 'w') as zf:
            pass
        
        result = archive_extractor.extract_zip(empty_zip)
        
        assert result['num_files'] == 0
    
    def test_nested_directory_zip(self, temp_dir):
        """Test ZIP with nested directories."""
        nested_zip = os.path.join(temp_dir, "nested.zip")
        with zipfile.ZipFile(nested_zip, 'w') as zf:
            zf.writestr("a/b/c/deep.txt", "Deep content")
        
        result = archive_extractor.extract_zip(nested_zip)
        
        assert 'a/b/c/deep.txt' in result['file_list']


class TestTarExtraction:
    """Specific tests for TAR extraction."""
    
    def test_tar_gz_extraction(self, temp_dir):
        """Test extraction from .tar.gz file."""
        txt_file = os.path.join(temp_dir, "content.txt")
        with open(txt_file, 'w') as f:
            f.write("Gzip content")
        
        tar_gz = os.path.join(temp_dir, "archive.tar.gz")
        with tarfile.open(tar_gz, 'w:gz') as tf:
            tf.add(txt_file, arcname="content.txt")
        
        result = archive_extractor.extract_tar(tar_gz)
        
        assert isinstance(result, dict)
        assert 'num_files' in result
    
    def test_empty_tar(self, temp_dir):
        """Test extraction from empty TAR."""
        empty_tar = os.path.join(temp_dir, "empty.tar")
        with tarfile.open(empty_tar, 'w') as tf:
            pass
        
        result = archive_extractor.extract_tar(empty_tar)
        
        assert result['num_files'] == 0


class TestArchiveExtractorLibraryAvailability:
    """Tests for library availability flags."""
    
    def test_py7zr_availability_flag_exists(self):
        """Test PY7ZR_AVAILABLE flag exists."""
        assert hasattr(archive_extractor, 'PY7ZR_AVAILABLE')
        assert isinstance(archive_extractor.PY7ZR_AVAILABLE, bool)
