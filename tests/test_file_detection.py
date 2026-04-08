"""
Tests for utils/file_detection.py
"""
import os
import pytest
from utils.file_detection import detect_type, get_file_category


class TestDetectType:
    """Tests for detect_type function."""
    
    def test_detect_text_file(self, sample_text_file):
        """Test detection of text files."""
        mime_type = detect_type(sample_text_file)
        assert mime_type in ['text/plain', 'text/x-python', 'application/octet-stream']
    
    def test_detect_png_file(self, sample_png_file):
        """Test detection of PNG images."""
        mime_type = detect_type(sample_png_file)
        assert 'png' in mime_type.lower() or mime_type == 'image/png'
    
    def test_detect_jpeg_file(self, sample_jpeg_file):
        """Test detection of JPEG images."""
        mime_type = detect_type(sample_jpeg_file)
        assert 'jpeg' in mime_type.lower() or 'jpg' in mime_type.lower() or mime_type == 'image/jpeg'
    
    def test_detect_zip_file(self, sample_zip_file):
        """Test detection of ZIP archives."""
        mime_type = detect_type(sample_zip_file)
        assert 'zip' in mime_type.lower()
    
    def test_detect_pdf_file(self, sample_pdf_file):
        """Test detection of PDF documents."""
        mime_type = detect_type(sample_pdf_file)
        assert 'pdf' in mime_type.lower()
    
    def test_detect_non_existent_file(self, non_existent_file):
        """Test handling of non-existent files."""
        mime_type = detect_type(non_existent_file)
        assert mime_type == "unknown/unknown"
    
    def test_detect_binary_file(self, sample_binary_file):
        """Test detection of binary files."""
        mime_type = detect_type(sample_binary_file)
        assert mime_type is not None
    
    def test_detect_empty_file(self, sample_empty_file):
        """Test detection of empty files."""
        mime_type = detect_type(sample_empty_file)
        # Empty files might return various types depending on detection method
        assert mime_type is not None


class TestGetFileCategory:
    """Tests for get_file_category function."""
    
    def test_image_category(self):
        """Test image MIME type categorization."""
        assert get_file_category('image/jpeg') == 'image'
        assert get_file_category('image/png') == 'image'
        assert get_file_category('image/gif') == 'image'
        assert get_file_category('image/webp') == 'image'
        assert get_file_category('image/bmp') == 'image'
    
    def test_audio_category(self):
        """Test audio MIME type categorization."""
        assert get_file_category('audio/mpeg') == 'audio'
        assert get_file_category('audio/wav') == 'audio'
        assert get_file_category('audio/ogg') == 'audio'
        assert get_file_category('audio/flac') == 'audio'
    
    def test_video_category(self):
        """Test video MIME type categorization."""
        assert get_file_category('video/mp4') == 'video'
        assert get_file_category('video/webm') == 'video'
        assert get_file_category('video/quicktime') == 'video'
        assert get_file_category('video/x-msvideo') == 'video'
    
    def test_document_category(self):
        """Test document MIME type categorization."""
        assert get_file_category('application/pdf') == 'document'
        assert get_file_category('application/msword') == 'document'
        assert get_file_category('text/plain') == 'document'
        assert get_file_category('application/vnd.openxmlformats-officedocument.wordprocessingml.document') == 'document'
    
    def test_archive_category(self):
        """Test archive MIME type categorization."""
        assert get_file_category('application/zip') == 'archive'
        assert get_file_category('application/x-tar') == 'archive'
        assert get_file_category('application/x-gzip') == 'archive'
        assert get_file_category('application/x-rar-compressed') == 'archive'
        assert get_file_category('application/x-7z-compressed') == 'archive'
    
    def test_other_category(self):
        """Test fallback to 'other' category."""
        assert get_file_category('application/octet-stream') == 'other'
        assert get_file_category('application/javascript') == 'other'
        assert get_file_category('unknown/unknown') == 'other'
    
    def test_none_mime_type(self):
        """Test handling of None MIME type."""
        assert get_file_category(None) == 'other'
    
    def test_empty_mime_type(self):
        """Test handling of empty string MIME type."""
        assert get_file_category('') == 'other'
    
    def test_case_insensitivity(self):
        """Test that categorization is case-insensitive."""
        assert get_file_category('IMAGE/JPEG') == 'image'
        assert get_file_category('Audio/MPEG') == 'audio'
        assert get_file_category('VIDEO/Mp4') == 'video'
