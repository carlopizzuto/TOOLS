"""
Common path utilities for file system operations.
"""

import os
from pathlib import Path


def get_absolute_path(file_path: str) -> str:
    """
    Get the absolute path of a file, resolving relative paths.
    
    Args:
        file_path (str): Path to resolve
        
    Returns:
        str: Absolute path
    """
    return os.path.abspath(os.path.expanduser(file_path))


def ensure_directory(dir_path: str) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        dir_path (str): Directory path to ensure exists
    """
    Path(dir_path).mkdir(parents=True, exist_ok=True) 