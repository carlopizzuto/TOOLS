"""
Tests for common I/O utilities.
"""

import pytest
import os
from unittest.mock import patch, mock_open
from tools.common.io import ensure_file_exists, safe_file_read


class TestEnsureFileExists:
    """Test cases for ensure_file_exists function."""
    
    @patch('os.path.exists')
    def test_ensure_file_exists_success(self, mock_exists):
        """Test that no exception is raised when file exists."""
        mock_exists.return_value = True
        
        # Should not raise any exception
        ensure_file_exists("existing_file.txt")
        mock_exists.assert_called_once_with("existing_file.txt")
    
    @patch('os.path.exists')
    def test_ensure_file_exists_not_found(self, mock_exists):
        """Test that FileNotFoundError is raised when file doesn't exist."""
        mock_exists.return_value = False
        
        with pytest.raises(FileNotFoundError) as exc_info:
            ensure_file_exists("nonexistent_file.txt")
        
        assert "File not found: nonexistent_file.txt" in str(exc_info.value)
        mock_exists.assert_called_once_with("nonexistent_file.txt")


class TestSafeFileRead:
    """Test cases for safe_file_read function."""
    
    @patch('tools.common.io.ensure_file_exists')
    @patch('builtins.open', new_callable=mock_open, read_data="file content")
    def test_safe_file_read_success(self, mock_file, mock_ensure):
        """Test successful file reading."""
        result = safe_file_read("test.txt")
        
        assert result == "file content"
        mock_ensure.assert_called_once_with("test.txt")
        mock_file.assert_called_once_with("test.txt", "r", encoding="utf-8")
    
    @patch('tools.common.io.ensure_file_exists')
    @patch('builtins.open', new_callable=mock_open, read_data="binary content")
    def test_safe_file_read_custom_mode(self, mock_file, mock_ensure):
        """Test file reading with custom mode and encoding."""
        result = safe_file_read("test.txt", mode="rb", encoding=None)
        
        assert result == "binary content"
        mock_ensure.assert_called_once_with("test.txt")
        mock_file.assert_called_once_with("test.txt", "rb", encoding=None)
    
    @patch('tools.common.io.ensure_file_exists')
    def test_safe_file_read_file_not_found(self, mock_ensure):
        """Test that FileNotFoundError is propagated."""
        mock_ensure.side_effect = FileNotFoundError("File not found: test.txt")
        
        with pytest.raises(FileNotFoundError):
            safe_file_read("test.txt")
    
    @patch('tools.common.io.ensure_file_exists')
    @patch('builtins.open')
    def test_safe_file_read_io_error(self, mock_file, mock_ensure):
        """Test that IOError is raised when reading fails."""
        mock_file.side_effect = IOError("Permission denied")
        
        with pytest.raises(IOError) as exc_info:
            safe_file_read("test.txt")
        
        assert "Error reading file test.txt" in str(exc_info.value) 