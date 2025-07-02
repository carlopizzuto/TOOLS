"""
Configuration management for tools.
"""

import os
from pathlib import Path
from typing import Optional


def load_env_file(env_path: Optional[str] = None) -> None:
    """
    Load environment variables from a .env file.
    
    Args:
        env_path: Path to .env file. If None, looks for .env in current dir and project root.
    """
    if env_path:
        env_files = [Path(env_path)]
    else:
        # Look for .env in current directory and project root
        current_dir = Path.cwd()
        project_root = Path(__file__).parent.parent.parent.parent  # Go up to project root
        env_files = [
            current_dir / ".env",
            project_root / ".env",
        ]
    
    for env_file in env_files:
        if env_file.exists():
            _load_env_vars(env_file)
            break


def _load_env_vars(env_file: Path) -> None:
    """Load environment variables from a file."""
    try:
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and not os.getenv(key):  # Don't override existing env vars
                        os.environ[key] = value
    except Exception:
        # Silently fail if .env file can't be read
        pass


def get_config(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get configuration value from environment variables.
    
    Args:
        key: Environment variable name
        default: Default value if not found
        
    Returns:
        Configuration value or default
    """
    return os.getenv(key, default)


def get_openai_api_key() -> Optional[str]:
    """Get OpenAI API key from environment."""
    return get_config('OPENAI_API_KEY')


def get_output_dir() -> str:
    """Get default output directory."""
    return get_config('TOOLS_OUTPUT_DIR', os.getcwd())


def get_log_level() -> str:
    """Get logging level."""
    return get_config('TOOLS_LOG_LEVEL', 'INFO')


# Auto-load .env file when module is imported
load_env_file() 