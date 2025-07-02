"""
Common I/O utilities for file operations.
"""

import os
from typing import Optional


def ensure_file_exists(file_path: str) -> None:
    """
    Check if a file exists and raise FileNotFoundError if it doesn't.
    
    Args:
        file_path (str): Path to the file to check
        
    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")


def safe_file_read(file_path: str, mode: str = "r", encoding: Optional[str] = "utf-8") -> str:
    """
    Safely read a file with proper error handling.
    
    Args:
        file_path (str): Path to the file to read
        mode (str): File mode (default: "r")
        encoding (str, optional): File encoding (default: "utf-8")
        
    Returns:
        str: File contents
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    ensure_file_exists(file_path)
    
    try:
        with open(file_path, mode, encoding=encoding) as f:
            return f.read()
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {e}") 