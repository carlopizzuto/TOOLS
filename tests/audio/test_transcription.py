"""
Tests for audio transcription tools.
"""

import pytest
import os
from unittest.mock import patch, mock_open, MagicMock
from tools.audio.transcription import transcribe_audio, transcribe_audio_cli


class TestTranscribeAudio:
    """Test cases for transcribe_audio function."""
    
    def test_transcribe_audio_file_not_found(self):
        """Test that FileNotFoundError is raised when file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            transcribe_audio("nonexistent_file.mp3")
    
    @patch('tools.audio.transcription.OpenAI')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data=b"audio data")
    def test_transcribe_audio_success(self, mock_file, mock_exists, mock_openai):
        """Test successful audio transcription."""
        # Setup mocks
        mock_exists.return_value = True
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_transcript = MagicMock()
        mock_transcript.text = "Hello world"
        mock_client.audio.transcriptions.create.return_value = mock_transcript
        
        # Test
        result = transcribe_audio("test.mp3")
        
        # Assertions
        assert result == "Hello world"
        mock_openai.assert_called_once()
        mock_client.audio.transcriptions.create.assert_called_once()
    
    @patch('tools.audio.transcription.OpenAI')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data=b"audio data")
    def test_transcribe_audio_with_api_key(self, mock_file, mock_exists, mock_openai):
        """Test transcription with custom API key."""
        # Setup mocks
        mock_exists.return_value = True
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_transcript = MagicMock()
        mock_transcript.text = "Hello world"
        mock_client.audio.transcriptions.create.return_value = mock_transcript
        
        # Test
        result = transcribe_audio("test.mp3", api_key="test-key")
        
        # Assertions
        assert result == "Hello world"
        mock_openai.assert_called_once_with(api_key="test-key")


class TestTranscribeAudioCLI:
    """Test cases for transcribe_audio_cli function."""
    
    @patch('builtins.print')
    def test_transcribe_audio_cli_no_args(self, mock_print):
        """Test CLI with no arguments."""
        transcribe_audio_cli([])
        mock_print.assert_called_with("Usage: tools audio.transcription <path_to_audio_file>")
    
    @patch('builtins.print')
    def test_transcribe_audio_cli_too_many_args(self, mock_print):
        """Test CLI with too many arguments."""
        transcribe_audio_cli(["file1.mp3", "file2.mp3"])
        mock_print.assert_called_with("Usage: tools audio.transcription <path_to_audio_file>")
    
    @patch('tools.audio.transcription.transcribe_audio')
    @patch('builtins.print')
    def test_transcribe_audio_cli_success(self, mock_print, mock_transcribe):
        """Test successful CLI transcription."""
        mock_transcribe.return_value = "Hello world"
        
        transcribe_audio_cli(["test.mp3"])
        
        mock_transcribe.assert_called_once_with("test.mp3")
        mock_print.assert_any_call("Transcription:")
        mock_print.assert_any_call("-" * 50)
        mock_print.assert_any_call("Hello world")
    
    @patch('tools.audio.transcription.transcribe_audio')
    @patch('builtins.print')
    def test_transcribe_audio_cli_file_not_found(self, mock_print, mock_transcribe):
        """Test CLI with file not found error."""
        mock_transcribe.side_effect = FileNotFoundError("File not found: test.mp3")
        
        transcribe_audio_cli(["test.mp3"])
        
        mock_print.assert_called_with("Error: File not found: test.mp3")
    
    @patch('tools.audio.transcription.transcribe_audio')
    @patch('builtins.print')
    def test_transcribe_audio_cli_general_error(self, mock_print, mock_transcribe):
        """Test CLI with general error."""
        mock_transcribe.side_effect = Exception("API error")
        
        transcribe_audio_cli(["test.mp3"])
        
        mock_print.assert_called_with("An error occurred: API error") 