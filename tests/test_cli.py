"""
Tests for the CLI interface.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock
from tools.cli import main


class TestCLI:
    """Test cases for the CLI interface."""
    
    @patch('sys.argv', ['tools'])
    @patch('tools.cli.argparse.ArgumentParser.print_help')
    def test_cli_no_args(self, mock_help):
        """Test CLI with no arguments shows help."""
        with pytest.raises(SystemExit):
            main()
        mock_help.assert_called_once()
    
    @patch('sys.argv', ['tools', 'invalid.tool'])
    @patch('builtins.print')
    def test_cli_invalid_tool(self, mock_print):
        """Test CLI with invalid tool."""
        with pytest.raises(SystemExit):
            main()
        mock_print.assert_any_call("Error: Unknown tool 'invalid.tool'")
    
    @patch('sys.argv', ['tools', 'invalidformat'])
    @patch('builtins.print')
    def test_cli_invalid_format(self, mock_print):
        """Test CLI with invalid tool format."""
        with pytest.raises(SystemExit):
            main()
        mock_print.assert_any_call("Error: Tool must be in format 'category.tool_name', got: invalidformat")
    
    @patch('sys.argv', ['tools', 'audio.transcription', 'test.mp3'])
    @patch('tools.cli.importlib.import_module')
    def test_cli_valid_tool(self, mock_import):
        """Test CLI with valid tool."""
        # Setup mock
        mock_module = MagicMock()
        mock_func = MagicMock()
        mock_module.transcribe_audio_cli = mock_func
        mock_import.return_value = mock_module
        
        # Test
        main()
        
        # Assertions
        mock_import.assert_called_once_with('tools.audio.transcription')
        mock_func.assert_called_once_with(['test.mp3'])
    
    @patch('sys.argv', ['tools', 'audio.transcription', 'test.mp3'])
    @patch('tools.cli.importlib.import_module')
    @patch('builtins.print')
    def test_cli_import_error(self, mock_print, mock_import):
        """Test CLI with import error."""
        mock_import.side_effect = ImportError("No module named 'openai'")
        
        with pytest.raises(SystemExit):
            main()
        
        mock_print.assert_any_call("Error: Could not import tool 'audio.transcription': No module named 'openai'")
        mock_print.assert_any_call("For audio tools, run: pip install tools[audio]") 