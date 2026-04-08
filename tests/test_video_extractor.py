"""
Tests for extractors/video_extractor.py
"""
import os
import pytest
from unittest.mock import patch, MagicMock
from extractors import video_extractor


class TestVideoExtractor:
    """Tests for video_extractor module."""
    
    def test_extract_returns_dict(self, sample_binary_file):
        """Test extract returns a dictionary."""
        result = video_extractor.extract(sample_binary_file)
        
        assert isinstance(result, dict)
        assert 'file_name' in result
    
    def test_basic_info_extraction(self, sample_binary_file):
        """Test get_basic_info function."""
        result = video_extractor.get_basic_info(sample_binary_file)
        
        assert 'file_name' in result
        assert 'file_size_bytes' in result
        assert 'file_size_mb' in result
    
    def test_extract_with_hachoir(self, sample_binary_file):
        """Test hachoir extraction."""
        if not video_extractor.HACHOIR_AVAILABLE:
            pytest.skip("hachoir not available")
        
        result = video_extractor.extract_with_hachoir(sample_binary_file)
        
        assert isinstance(result, dict)
    
    def test_ffprobe_not_found_handling(self, temp_dir):
        """Test graceful handling when ffprobe is not found."""
        test_file = os.path.join(temp_dir, "test.mp4")
        with open(test_file, 'wb') as f:
            f.write(b'\x00' * 100)
        
        # Mock shutil.which to return None
        with patch('shutil.which', return_value=None):
            with patch('os.path.exists', return_value=False):
                result = video_extractor.extract_with_ffprobe(test_file)
        
        assert isinstance(result, dict)
        # Should indicate ffprobe not found
        assert 'ffprobe_note' in result or 'ffprobe_error' in result or len(result) == 0
    
    @patch('subprocess.run')
    @patch('shutil.which')
    def test_ffprobe_success(self, mock_which, mock_run, temp_dir):
        """Test successful ffprobe extraction."""
        mock_which.return_value = 'ffprobe'
        
        # Mock ffprobe output
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '{"format": {"format_name": "mp4", "duration": "120.5"}, "streams": []}'
        mock_run.return_value = mock_result
        
        test_file = os.path.join(temp_dir, "test.mp4")
        with open(test_file, 'wb') as f:
            f.write(b'\x00' * 100)
        
        result = video_extractor.extract_with_ffprobe(test_file)
        
        assert isinstance(result, dict)
        assert result.get('format_name') == 'mp4'
    
    @patch('subprocess.run')
    @patch('shutil.which')
    def test_ffprobe_timeout(self, mock_which, mock_run, temp_dir):
        """Test ffprobe timeout handling."""
        import subprocess
        mock_which.return_value = 'ffprobe'
        mock_run.side_effect = subprocess.TimeoutExpired('ffprobe', 30)
        
        test_file = os.path.join(temp_dir, "test.mp4")
        with open(test_file, 'wb') as f:
            f.write(b'\x00' * 100)
        
        result = video_extractor.extract_with_ffprobe(test_file)
        
        assert isinstance(result, dict)
        assert 'ffprobe_error' in result
        assert 'Timeout' in result['ffprobe_error']
    
    def test_extract_non_video_file(self, sample_text_file):
        """Test extraction from non-video file."""
        result = video_extractor.extract(sample_text_file)
        
        # Should handle gracefully
        assert isinstance(result, dict)
        assert 'file_name' in result


class TestVideoExtractorLibraryAvailability:
    """Tests for library availability flags."""
    
    def test_hachoir_availability_flag_exists(self):
        """Test HACHOIR_AVAILABLE flag exists."""
        assert hasattr(video_extractor, 'HACHOIR_AVAILABLE')
        assert isinstance(video_extractor.HACHOIR_AVAILABLE, bool)
