"""
Tests for extractors/generic_extractor.py
"""
import os
import hashlib
import pytest
from extractors import generic_extractor


class TestGenericExtractor:
    """Tests for generic_extractor module."""
    
    def test_extract_text_file(self, sample_text_file):
        """Test extraction from text file."""
        result = generic_extractor.extract(sample_text_file)
        
        assert isinstance(result, dict)
        assert 'file_name' in result
        assert 'file_extension' in result
        assert 'file_size_bytes' in result
    
    def test_extract_binary_file(self, sample_binary_file):
        """Test extraction from binary file."""
        result = generic_extractor.extract(sample_binary_file)
        
        assert isinstance(result, dict)
        assert 'file_name' in result
        assert 'md5_hash' in result
        assert 'sha256_hash' in result
    
    def test_basic_info_extraction(self, sample_text_file):
        """Test get_basic_info function."""
        result = generic_extractor.get_basic_info(sample_text_file)
        
        assert 'file_name' in result
        assert 'file_extension' in result
        assert 'file_size_bytes' in result
        assert 'file_size_kb' in result
        assert 'file_size_mb' in result
        assert 'creation_time' in result
        assert 'modification_time' in result
        assert 'access_time' in result
    
    def test_hash_calculation(self, sample_text_file):
        """Test calculate_hashes function."""
        result = generic_extractor.calculate_hashes(sample_text_file)
        
        assert 'md5_hash' in result
        assert 'sha256_hash' in result
        
        # Verify hashes are correct format
        assert len(result['md5_hash']) == 32
        assert len(result['sha256_hash']) == 64
    
    def test_hash_calculation_correct_values(self, temp_dir):
        """Test that hash values are correct."""
        test_file = os.path.join(temp_dir, "hash_test.txt")
        content = b"Test content for hashing"
        with open(test_file, 'wb') as f:
            f.write(content)
        
        result = generic_extractor.calculate_hashes(test_file)
        
        expected_md5 = hashlib.md5(content).hexdigest()
        expected_sha256 = hashlib.sha256(content).hexdigest()
        
        assert result['md5_hash'] == expected_md5
        assert result['sha256_hash'] == expected_sha256
    
    def test_hash_skip_large_files(self, temp_dir):
        """Test that hash calculation skips very large files."""
        large_file = os.path.join(temp_dir, "large.bin")
        # Create a file larger than max_size (100MB)
        # We'll mock this by using a smaller max_size
        with open(large_file, 'wb') as f:
            f.write(b'x' * 1000)
        
        # Call with small max_size to trigger skip
        result = generic_extractor.calculate_hashes(large_file, max_size=500)
        
        assert 'hash_note' in result
        assert 'too large' in result['hash_note'].lower()
    
    def test_header_inspection(self, sample_binary_file):
        """Test inspect_header function."""
        result = generic_extractor.inspect_header(sample_binary_file)
        
        assert 'file_header_hex' in result
        assert 'file_header_ascii' in result
    
    def test_header_hex_format(self, temp_dir):
        """Test that header hex is correctly formatted."""
        test_file = os.path.join(temp_dir, "header_test.bin")
        with open(test_file, 'wb') as f:
            f.write(b'\x00\x01\x02\x03\x04\x05\x06\x07')
        
        result = generic_extractor.inspect_header(test_file, header_size=8)
        
        assert result['file_header_hex'] == '00 01 02 03 04 05 06 07'
    
    def test_magic_bytes_detection(self, sample_png_file):
        """Test magic bytes format identification."""
        result = generic_extractor.inspect_header(sample_png_file)
        
        assert 'identified_format' in result
        assert 'PNG' in result['identified_format']
    
    def test_magic_bytes_detection_jpeg(self, sample_jpeg_file):
        """Test magic bytes detection for JPEG."""
        result = generic_extractor.inspect_header(sample_jpeg_file)
        
        assert 'identified_format' in result
        assert 'JPEG' in result['identified_format']
    
    def test_magic_bytes_detection_pdf(self, sample_pdf_file):
        """Test magic bytes detection for PDF."""
        result = generic_extractor.inspect_header(sample_pdf_file)
        
        assert 'identified_format' in result
        assert 'PDF' in result['identified_format']
    
    def test_magic_bytes_detection_zip(self, sample_zip_file):
        """Test magic bytes detection for ZIP."""
        result = generic_extractor.inspect_header(sample_zip_file)
        
        assert 'identified_format' in result
        assert 'ZIP' in result['identified_format']
    
    def test_extract_with_hachoir(self, sample_binary_file):
        """Test hachoir extraction."""
        if not generic_extractor.HACHOIR_AVAILABLE:
            pytest.skip("hachoir not available")
        
        result = generic_extractor.extract_with_hachoir(sample_binary_file)
        
        assert isinstance(result, dict)
    
    def test_empty_file_handling(self, sample_empty_file):
        """Test extraction from empty file."""
        result = generic_extractor.extract(sample_empty_file)
        
        assert isinstance(result, dict)
        assert result['file_size_bytes'] == 0


class TestGenericExtractorLibraryAvailability:
    """Tests for library availability flags."""
    
    def test_hachoir_availability_flag_exists(self):
        """Test HACHOIR_AVAILABLE flag exists."""
        assert hasattr(generic_extractor, 'HACHOIR_AVAILABLE')
        assert isinstance(generic_extractor.HACHOIR_AVAILABLE, bool)


class TestHeaderInspection:
    """Specific tests for header inspection."""
    
    def test_ascii_conversion_non_printable(self, temp_dir):
        """Test ASCII conversion replaces non-printable chars with dots."""
        test_file = os.path.join(temp_dir, "nonprint.bin")
        with open(test_file, 'wb') as f:
            f.write(bytes([0, 1, 2, 65, 66, 67, 255]))  # Mix of non-printable and printable
        
        result = generic_extractor.inspect_header(test_file, header_size=7)
        
        # ASCII should have dots for non-printable and letters for printable
        assert 'ABC' in result['file_header_ascii']
        assert '.' in result['file_header_ascii']
    
    def test_header_size_parameter(self, temp_dir):
        """Test that header_size parameter works."""
        test_file = os.path.join(temp_dir, "sized.bin")
        with open(test_file, 'wb') as f:
            f.write(b'1234567890')
        
        result_short = generic_extractor.inspect_header(test_file, header_size=4)
        result_long = generic_extractor.inspect_header(test_file, header_size=8)
        
        assert len(result_short['file_header_hex'].split()) == 4
        assert len(result_long['file_header_hex'].split()) == 8
