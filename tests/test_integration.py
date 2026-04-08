"""
Integration tests for MetaFinder - tests the complete extraction pipeline.
"""
import os
import pytest
from utils.file_detection import detect_type, get_file_category
from utils.normalize import normalize_metadata
from utils.text_writer import save_metadata, generate_output_filename
from extractors import (
    image_extractor,
    audio_extractor,
    video_extractor,
    document_extractor,
    archive_extractor,
    generic_extractor
)


def get_metadata(file_path, category):
    """Helper function mimicking main.py logic."""
    if category == 'image':
        return image_extractor.extract(file_path)
    elif category == 'audio':
        return audio_extractor.extract(file_path)
    elif category == 'video':
        return video_extractor.extract(file_path)
    elif category == 'document':
        return document_extractor.extract(file_path)
    elif category == 'archive':
        return archive_extractor.extract(file_path)
    else:
        return generic_extractor.extract(file_path)


class TestFullPipeline:
    """Test complete extraction pipeline from file to output."""
    
    def test_png_full_pipeline(self, sample_png_file, temp_dir):
        """Test full pipeline for PNG image."""
        # Step 1: Detect type
        mime_type = detect_type(sample_png_file)
        assert mime_type is not None
        
        # Step 2: Get category
        category = get_file_category(mime_type)
        assert category == 'image'
        
        # Step 3: Extract metadata
        metadata = get_metadata(sample_png_file, category)
        assert isinstance(metadata, dict)
        assert 'file_name' in metadata
        
        # Step 4: Normalize to text
        text_content = normalize_metadata(metadata, sample_png_file, mime_type)
        assert 'METADATA EXTRACTION REPORT' in text_content
        assert 'sample.png' in text_content
        
        # Step 5: Save to file
        output_path = os.path.join(temp_dir, "output_metadata.txt")
        success = save_metadata(text_content, output_path)
        assert success is True
        assert os.path.exists(output_path)
        
        # Verify saved content
        with open(output_path, 'r', encoding='utf-8') as f:
            saved_content = f.read()
        assert saved_content == text_content
    
    def test_text_full_pipeline(self, sample_text_file, temp_dir):
        """Test full pipeline for text document."""
        mime_type = detect_type(sample_text_file)
        category = get_file_category(mime_type)
        
        metadata = get_metadata(sample_text_file, category)
        text_content = normalize_metadata(metadata, sample_text_file, mime_type)
        
        output_path = os.path.join(temp_dir, "text_metadata.txt")
        success = save_metadata(text_content, output_path)
        
        assert success is True
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'num_characters' in content.lower() or 'Num Characters' in content
    
    def test_zip_full_pipeline(self, sample_zip_file, temp_dir):
        """Test full pipeline for ZIP archive."""
        mime_type = detect_type(sample_zip_file)
        category = get_file_category(mime_type)
        
        assert category == 'archive'
        
        metadata = get_metadata(sample_zip_file, category)
        text_content = normalize_metadata(metadata, sample_zip_file, mime_type)
        
        output_path = os.path.join(temp_dir, "zip_metadata.txt")
        success = save_metadata(text_content, output_path)
        
        assert success is True
        assert 'Num Files' in text_content or 'num_files' in text_content.lower()
    
    def test_pdf_full_pipeline(self, sample_pdf_file, temp_dir):
        """Test full pipeline for PDF document."""
        mime_type = detect_type(sample_pdf_file)
        category = get_file_category(mime_type)
        
        assert category == 'document'
        
        metadata = get_metadata(sample_pdf_file, category)
        text_content = normalize_metadata(metadata, sample_pdf_file, mime_type)
        
        output_path = os.path.join(temp_dir, "pdf_metadata.txt")
        success = save_metadata(text_content, output_path)
        
        assert success is True
    
    def test_binary_full_pipeline(self, sample_binary_file, temp_dir):
        """Test full pipeline for unknown binary file."""
        mime_type = detect_type(sample_binary_file)
        category = get_file_category(mime_type)
        
        # Unknown files should go to 'other' category
        assert category == 'other'
        
        metadata = get_metadata(sample_binary_file, category)
        text_content = normalize_metadata(metadata, sample_binary_file, mime_type)
        
        output_path = os.path.join(temp_dir, "binary_metadata.txt")
        success = save_metadata(text_content, output_path)
        
        assert success is True
        # Generic extractor should provide hashes
        assert 'md5' in text_content.lower() or 'hash' in text_content.lower()


class TestOutputFilenameGeneration:
    """Test automatic output filename generation."""
    
    def test_output_filename_from_input(self, sample_png_file):
        """Test that output filename is correctly generated."""
        output_path = generate_output_filename(sample_png_file)
        
        assert output_path.endswith('_metadata.txt')
        assert 'sample' in output_path
    
    def test_output_in_same_directory(self, sample_png_file):
        """Test output file is in same directory as input."""
        output_path = generate_output_filename(sample_png_file)
        
        input_dir = os.path.dirname(sample_png_file)
        output_dir = os.path.dirname(output_path)
        
        assert input_dir == output_dir


class TestMetadataConsistency:
    """Test that metadata extraction is consistent."""
    
    def test_extraction_is_deterministic(self, sample_png_file):
        """Test that repeated extraction gives same results."""
        result1 = image_extractor.extract(sample_png_file)
        result2 = image_extractor.extract(sample_png_file)
        
        # Core fields should be identical
        assert result1['file_name'] == result2['file_name']
        assert result1['file_size_bytes'] == result2['file_size_bytes']
    
    def test_hash_consistency(self, sample_binary_file):
        """Test that hash values are consistent."""
        result1 = generic_extractor.calculate_hashes(sample_binary_file)
        result2 = generic_extractor.calculate_hashes(sample_binary_file)
        
        assert result1['md5_hash'] == result2['md5_hash']
        assert result1['sha256_hash'] == result2['sha256_hash']


class TestCategoryRouting:
    """Test that files are routed to correct extractors."""
    
    def test_image_routing(self, sample_png_file, sample_jpeg_file):
        """Test image files are routed to image extractor."""
        for file_path in [sample_png_file, sample_jpeg_file]:
            mime_type = detect_type(file_path)
            category = get_file_category(mime_type)
            assert category == 'image', f"Expected 'image' for {file_path}, got '{category}'"
    
    def test_archive_routing(self, sample_zip_file, sample_tar_file):
        """Test archive files are routed to archive extractor."""
        for file_path in [sample_zip_file, sample_tar_file]:
            mime_type = detect_type(file_path)
            category = get_file_category(mime_type)
            assert category == 'archive', f"Expected 'archive' for {file_path}, got '{category}'"
    
    def test_document_routing(self, sample_pdf_file, sample_text_file):
        """Test document files are routed to document extractor."""
        for file_path in [sample_pdf_file, sample_text_file]:
            mime_type = detect_type(file_path)
            category = get_file_category(mime_type)
            assert category == 'document', f"Expected 'document' for {file_path}, got '{category}'"
