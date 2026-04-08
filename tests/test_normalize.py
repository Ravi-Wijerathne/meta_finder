"""
Tests for utils/normalize.py
"""
import pytest
from datetime import datetime
from utils.normalize import normalize_metadata, format_nested_dict


class TestNormalizeMetadata:
    """Tests for normalize_metadata function."""
    
    def test_basic_metadata_normalization(self, sample_metadata):
        """Test basic metadata normalization."""
        result = normalize_metadata(sample_metadata, '/path/to/test.jpg', 'image/jpeg')
        
        # Check header
        assert 'METADATA EXTRACTION REPORT' in result
        assert '/path/to/test.jpg' in result
        assert 'image/jpeg' in result
        
        # Check metadata fields
        assert 'File Name: test.jpg' in result
        assert 'File Size Bytes: 12345' in result
        assert 'Image Width: 1920' in result
        assert 'Exif Make: Canon' in result
    
    def test_empty_metadata(self):
        """Test handling of empty metadata."""
        result = normalize_metadata({}, '/path/to/test.txt', 'text/plain')
        
        assert 'METADATA EXTRACTION REPORT' in result
        assert 'No metadata found' in result
    
    def test_none_metadata(self):
        """Test handling of None metadata."""
        result = normalize_metadata(None, '/path/to/test.txt', 'text/plain')
        
        assert 'No metadata found' in result
    
    def test_nested_dict_metadata(self, nested_metadata):
        """Test handling of nested dictionaries."""
        result = normalize_metadata(nested_metadata, '/path/to/test.jpg', 'image/jpeg')
        
        assert 'Gps Info:' in result
        assert 'GPSLatitude' in result
        assert '51.5074' in result
    
    def test_binary_data_handling(self, nested_metadata):
        """Test handling of binary data."""
        result = normalize_metadata(nested_metadata, '/path/to/test.jpg', 'image/jpeg')
        
        assert 'binary data' in result.lower() or '4 bytes' in result
    
    def test_list_data_handling(self, nested_metadata):
        """Test handling of list data."""
        result = normalize_metadata(nested_metadata, '/path/to/test.jpg', 'image/jpeg')
        
        assert 'item1' in result
        assert 'item2' in result
    
    def test_metadata_count(self, sample_metadata):
        """Test metadata field count is included."""
        result = normalize_metadata(sample_metadata, '/path/to/test.jpg', 'image/jpeg')
        
        assert 'Total metadata fields:' in result
        assert str(len(sample_metadata)) in result
    
    def test_timestamp_included(self, sample_metadata):
        """Test that generation timestamp is included."""
        result = normalize_metadata(sample_metadata, '/path/to/test.jpg', 'image/jpeg')
        
        assert 'Generated:' in result
        # Should contain date in format YYYY-MM-DD
        current_year = str(datetime.now().year)
        assert current_year in result
    
    def test_special_characters_in_values(self):
        """Test handling of special characters."""
        metadata = {
            'description': 'Test with "quotes" and <tags>',
            'unicode_field': 'Ünïcödé tëxt 日本語',
        }
        result = normalize_metadata(metadata, '/path/to/test.txt', 'text/plain')
        
        assert '"quotes"' in result
        assert 'Ünïcödé' in result
    
    def test_underscore_to_space_conversion(self):
        """Test that underscores are converted to spaces in keys."""
        metadata = {'some_key_name': 'value'}
        result = normalize_metadata(metadata, '/path/to/test.txt', 'text/plain')
        
        # Key should be title-cased with spaces
        assert 'Some Key Name:' in result


class TestFormatNestedDict:
    """Tests for format_nested_dict function."""
    
    def test_simple_nested_dict(self):
        """Test formatting of simple nested dict."""
        d = {'key1': 'value1', 'key2': 'value2'}
        result = format_nested_dict(d)
        
        assert 'key1: value1' in result
        assert 'key2: value2' in result
    
    def test_deeply_nested_dict(self):
        """Test formatting of deeply nested dict."""
        d = {
            'level1': {
                'level2': {
                    'level3': 'deep_value'
                }
            }
        }
        result = format_nested_dict(d)
        
        assert 'level1' in result
        assert 'level2' in result
        assert 'deep_value' in result
    
    def test_mixed_content_dict(self):
        """Test dict with mixed value types."""
        d = {
            'string_key': 'string_value',
            'number_key': 42,
            'nested_key': {'inner': 'value'},
        }
        result = format_nested_dict(d)
        
        assert 'string_value' in result
        assert '42' in result
        assert 'inner' in result
    
    def test_empty_dict(self):
        """Test formatting of empty dict."""
        result = format_nested_dict({})
        assert result == ""
