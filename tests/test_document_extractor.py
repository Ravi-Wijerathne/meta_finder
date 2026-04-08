"""
Tests for extractors/document_extractor.py
"""
import os
import pytest
from extractors import document_extractor


class TestDocumentExtractor:
    """Tests for document_extractor module."""
    
    def test_extract_text_file(self, sample_text_file):
        """Test extraction from text file."""
        result = document_extractor.extract(sample_text_file)
        
        assert isinstance(result, dict)
        assert 'file_name' in result
        assert 'num_characters' in result
        assert 'num_lines' in result
        assert 'num_words' in result
    
    def test_extract_text_file_content(self, sample_text_file):
        """Test that text file stats are correct."""
        result = document_extractor.extract(sample_text_file)
        
        assert result['num_lines'] == 3
        assert result['num_words'] > 0
        assert 'preview' in result
    
    def test_extract_pdf(self, sample_pdf_file):
        """Test extraction from PDF file."""
        if not document_extractor.PYPDF2_AVAILABLE:
            pytest.skip("PyPDF2 not available")
        
        result = document_extractor.extract(sample_pdf_file)
        
        assert isinstance(result, dict)
        assert 'file_name' in result
        # PDF-specific fields may or may not be present depending on the minimal PDF
    
    def test_basic_info_extraction(self, sample_text_file):
        """Test get_basic_info function."""
        result = document_extractor.get_basic_info(sample_text_file)
        
        assert 'file_name' in result
        assert 'file_size_bytes' in result
        assert 'file_size_mb' in result
    
    def test_extract_txt_function(self, sample_text_file):
        """Test extract_txt function directly."""
        result = document_extractor.extract_txt(sample_text_file)
        
        assert 'num_characters' in result
        assert 'num_lines' in result
        assert 'num_words' in result
        assert 'preview' in result
    
    def test_extract_pdf_function(self, sample_pdf_file):
        """Test extract_pdf function directly."""
        if not document_extractor.PYPDF2_AVAILABLE:
            pytest.skip("PyPDF2 not available")
        
        result = document_extractor.extract_pdf(sample_pdf_file)
        
        assert isinstance(result, dict)
        # May have num_pages or pdf_error
    
    def test_extract_empty_text_file(self, sample_empty_file):
        """Test extraction from empty text file."""
        # Rename to .txt extension
        txt_file = sample_empty_file.replace('.txt', '_renamed.txt')
        os.rename(sample_empty_file, txt_file) if os.path.exists(sample_empty_file) else None
        
        result = document_extractor.extract_txt(txt_file if os.path.exists(txt_file) else sample_empty_file)
        
        assert isinstance(result, dict)
        # Empty file handling
    
    def test_extract_unknown_document_type(self, temp_dir):
        """Test extraction from unknown document type."""
        unknown_file = os.path.join(temp_dir, "document.xyz")
        with open(unknown_file, 'w') as f:
            f.write("Unknown content")
        
        result = document_extractor.extract(unknown_file)
        
        assert isinstance(result, dict)
        assert 'note' in result or 'file_name' in result
    
    def test_extract_preserves_file_name(self, sample_text_file):
        """Test that original file name is preserved."""
        result = document_extractor.extract(sample_text_file)
        
        assert result['file_name'] == os.path.basename(sample_text_file)


class TestDocumentExtractorLibraryAvailability:
    """Tests for library availability flags."""
    
    def test_pypdf2_availability_flag_exists(self):
        """Test PYPDF2_AVAILABLE flag exists."""
        assert hasattr(document_extractor, 'PYPDF2_AVAILABLE')
        assert isinstance(document_extractor.PYPDF2_AVAILABLE, bool)
    
    def test_docx_availability_flag_exists(self):
        """Test DOCX_AVAILABLE flag exists."""
        assert hasattr(document_extractor, 'DOCX_AVAILABLE')
        assert isinstance(document_extractor.DOCX_AVAILABLE, bool)


class TestTextExtraction:
    """Specific tests for text file extraction."""
    
    def test_text_preview_truncation(self, temp_dir):
        """Test that preview is truncated for long files."""
        long_file = os.path.join(temp_dir, "long.txt")
        with open(long_file, 'w') as f:
            f.write("x" * 500)  # 500 characters
        
        result = document_extractor.extract_txt(long_file)
        
        # Preview should be limited to 200 chars
        assert len(result['preview']) <= 200
    
    def test_text_newline_handling_in_preview(self, temp_dir):
        """Test that newlines are replaced with spaces in preview."""
        multiline_file = os.path.join(temp_dir, "multiline.txt")
        with open(multiline_file, 'w') as f:
            f.write("Line1\nLine2\nLine3")
        
        result = document_extractor.extract_txt(multiline_file)
        
        # Newlines should be replaced with spaces
        assert '\n' not in result['preview']
    
    def test_word_count_accuracy(self, temp_dir):
        """Test accurate word counting."""
        word_file = os.path.join(temp_dir, "words.txt")
        with open(word_file, 'w') as f:
            f.write("one two three four five")
        
        result = document_extractor.extract_txt(word_file)
        
        assert result['num_words'] == 5
