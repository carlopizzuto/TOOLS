"""
Audio transcription tools using OpenAI's Whisper API.
"""

import os
from typing import Optional
from openai import OpenAI
from ..common.io import ensure_file_exists
from ..common.config import get_openai_api_key


def transcribe_audio(file_path: str, api_key: Optional[str] = None) -> str:
    """
    Transcribe an audio file using OpenAI's Whisper API.
    
    Args:
        file_path (str): Path to the audio file
        api_key (str, optional): OpenAI API key. If not provided, will use OPENAI_API_KEY env var
    
    Returns:
        str: Transcribed text
        
    Raises:
        FileNotFoundError: If the audio file doesn't exist
        Exception: If there's an error with the API call
    """
    # Check if file exists
    ensure_file_exists(file_path)
    
    # Initialize OpenAI client
    if api_key:
        client = OpenAI(api_key=api_key)
    else:
        # Try to get API key from .env file or environment
        env_api_key = get_openai_api_key()
        if env_api_key:
            client = OpenAI(api_key=env_api_key)
        else:
            client = OpenAI()  # Uses OPENAI_API_KEY environment variable
    
    # Open and transcribe the audio file
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    
    return transcript.text


def transcribe_audio_cli(args: list) -> None:
    """
    CLI interface for audio transcription.
    
    Args:
        args (list): Command line arguments
    """
    if len(args) != 1:
        print("Usage: tools audio.transcription <path_to_audio_file>")
        print("Example: tools audio.transcription ./audio.mp3")
        return
    
    audio_file_path = args[0]
    
    try:
        # Transcribe the audio
        transcription = transcribe_audio(audio_file_path)
        
        # Print the result
        print("Transcription:")
        print("-" * 50)
        print(transcription)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}") 