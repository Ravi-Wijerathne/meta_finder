"""
Tests for extractors/image_extractor.py
"""
import os
import pytest
from extractors import image_extractor


class TestImageExtractor:
    """Tests for image_extractor module."""
    
    def test_extract_png(self, sample_png_file):
        """Test extraction from PNG file."""
        result = image_extractor.extract(sample_png_file)
        
        assert isinstance(result, dict)
        assert 'file_name' in result
        assert result['file_name'] == 'sample.png'
        assert 'file_size_bytes' in result
        assert result['file_size_bytes'] > 0
    
    def test_extract_jpeg(self, sample_jpeg_file):
        """Test extraction from JPEG file."""
        result = image_extractor.extract(sample_jpeg_file)
        
        assert isinstance(result, dict)
        assert 'file_name' in result
        assert result['file_name'] == 'sample.jpg'
    
    def test_extract_contains_image_dimensions(self, sample_png_file):
        """Test that image dimensions are extracted."""
        result = image_extractor.extract(sample_png_file)
        
        # If PIL is available, these should be present
        if image_extractor.PIL_AVAILABLE:
            assert 'image_width' in result or 'pil_error' in result
            assert 'image_height' in result or 'pil_error' in result
    
    def test_basic_info_extraction(self, sample_png_file):
        """Test get_basic_info function."""
        result = image_extractor.get_basic_info(sample_png_file)
        
        assert 'file_name' in result
        assert 'file_size_bytes' in result
        assert 'file_size_mb' in result
        assert result['file_name'] == 'sample.png'
    
    def test_extract_with_pil_png(self, sample_png_file):
        """Test PIL extraction on PNG."""
        if not image_extractor.PIL_AVAILABLE:
            pytest.skip("PIL not available")
        
        result = image_extractor.extract_with_pil(sample_png_file)
        
        assert isinstance(result, dict)
        # May contain image info or error
        assert 'image_format' in result or 'pil_error' in result
    
    def test_extract_with_pil_jpeg(self, sample_jpeg_file):
        """Test PIL extraction on JPEG."""
        if not image_extractor.PIL_AVAILABLE:
            pytest.skip("PIL not available")
        
        result = image_extractor.extract_with_pil(sample_jpeg_file)
        
        assert isinstance(result, dict)
    
    def test_extract_with_exifread(self, sample_jpeg_file):
        """Test exifread extraction."""
        if not image_extractor.EXIFREAD_AVAILABLE:
            pytest.skip("exifread not available")
        
        result = image_extractor.extract_with_exifread(sample_jpeg_file)
        
        assert isinstance(result, dict)
    
    def test_extract_corrupted_file(self, corrupted_file):
        """Test extraction from corrupted file handles gracefully."""
        result = image_extractor.extract(corrupted_file)
        
        # Should return dict without crashing
        assert isinstance(result, dict)
        assert 'file_name' in result
    
    def test_extract_non_image_file(self, sample_text_file):
        """Test extraction from non-image file."""
        result = image_extractor.extract(sample_text_file)
        
        # Should handle gracefully, returning basic info at minimum
        assert isinstance(result, dict)
        assert 'file_name' in result


class TestImageExtractorLibraryAvailability:
    """Tests for library availability flags."""
    
    def test_pil_availability_flag_exists(self):
        """Test PIL_AVAILABLE flag exists."""
        assert hasattr(image_extractor, 'PIL_AVAILABLE')
        assert isinstance(image_extractor.PIL_AVAILABLE, bool)
    
    def test_exifread_availability_flag_exists(self):
        """Test EXIFREAD_AVAILABLE flag exists."""
        assert hasattr(image_extractor, 'EXIFREAD_AVAILABLE')
        assert isinstance(image_extractor.EXIFREAD_AVAILABLE, bool)
