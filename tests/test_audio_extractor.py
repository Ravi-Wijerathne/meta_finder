"""
Tests for extractors/audio_extractor.py
"""
import os
import pytest
from extractors import audio_extractor


class TestAudioExtractor:
    """Tests for audio_extractor module."""
    
    def test_extract_mp3(self, sample_mp3_file):
        """Test extraction from MP3 file."""
        result = audio_extractor.extract(sample_mp3_file)
        
        assert isinstance(result, dict)
        assert 'file_name' in result
        assert result['file_name'] == 'sample.mp3'
        assert 'file_size_bytes' in result
    
    def test_basic_info_extraction(self, sample_mp3_file):
        """Test get_basic_info function."""
        result = audio_extractor.get_basic_info(sample_mp3_file)
        
        assert 'file_name' in result
        assert 'file_size_bytes' in result
        assert 'file_size_mb' in result
    
    def test_extract_with_mutagen(self, sample_mp3_file):
        """Test mutagen extraction."""
        if not audio_extractor.MUTAGEN_AVAILABLE:
            pytest.skip("mutagen not available")
        
        result = audio_extractor.extract_with_mutagen(sample_mp3_file)
        
        assert isinstance(result, dict)
        # May have data or error, both are valid
    
    def test_extract_with_tinytag(self, sample_mp3_file):
        """Test tinytag extraction."""
        if not audio_extractor.TINYTAG_AVAILABLE:
            pytest.skip("tinytag not available")
        
        result = audio_extractor.extract_with_tinytag(sample_mp3_file)
        
        assert isinstance(result, dict)
    
    def test_extract_non_audio_file(self, sample_text_file):
        """Test extraction from non-audio file."""
        result = audio_extractor.extract(sample_text_file)
        
        # Should handle gracefully
        assert isinstance(result, dict)
        assert 'file_name' in result
    
    def test_extract_corrupted_audio(self, corrupted_file):
        """Test extraction from corrupted file."""
        result = audio_extractor.extract(corrupted_file)
        
        # Should not crash
        assert isinstance(result, dict)


class TestAudioExtractorLibraryAvailability:
    """Tests for library availability flags."""
    
    def test_mutagen_availability_flag_exists(self):
        """Test MUTAGEN_AVAILABLE flag exists."""
        assert hasattr(audio_extractor, 'MUTAGEN_AVAILABLE')
        assert isinstance(audio_extractor.MUTAGEN_AVAILABLE, bool)
    
    def test_tinytag_availability_flag_exists(self):
        """Test TINYTAG_AVAILABLE flag exists."""
        assert hasattr(audio_extractor, 'TINYTAG_AVAILABLE')
        assert isinstance(audio_extractor.TINYTAG_AVAILABLE, bool)
