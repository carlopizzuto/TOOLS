"""
Command-line interface for the tools package.
"""

import sys
import argparse
import importlib
from typing import List


def list_tools() -> None:
    """List all available tools."""
    print("Available tools:")
    print()
    
    # Audio tools
    print("Audio Tools:")
    print("  audio.transcribe    - Transcribe audio files using OpenAI Whisper")
    print()
    
    # Image tools
    print("Image Tools:")
    print("  image.resize        - Resize images (coming soon)")
    print("  image.convert       - Convert image formats (coming soon)")
    print()
    
    # Text tools
    print("Text Tools:")
    print("  text.sentiment      - Analyze text sentiment (coming soon)")
    print()
    
    print("Usage: tools <tool_name> [arguments...]")
    print("Example: tools audio.transcribe audio.mp3")


def main() -> None:
    """
    Main CLI entry point that dispatches to appropriate tools.
    """
    parser = argparse.ArgumentParser(
        prog="tools",
        description="A collection of utility tools for LLMs and automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tools list
  tools audio.transcribe audio.mp3
  tools image.resize image.jpg 800 600
  tools text.sentiment "This is a great day!"

Available tools:
  list                 - List all available tools
  audio.transcribe     - Transcribe audio files using OpenAI Whisper
  image.resize         - Resize images (coming soon)
  image.convert        - Convert image formats (coming soon)
  text.sentiment       - Analyze text sentiment (coming soon)
        """
    )
    
    parser.add_argument(
        "tool",
        help="Tool to run (e.g., list, audio.transcribe, image.resize)"
    )
    
    parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Arguments to pass to the tool"
    )
    
    # Parse arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    ns = parser.parse_args()
    
    # Handle special commands
    if ns.tool == "list":
        list_tools()
        return
    
    # Route to appropriate tool
    try:
        # Map tools to their CLI functions (supporting both old and new naming)
        tool_mapping = {
            # Audio tools
            "audio.transcribe": ("tools.audio.transcribe", "transcribe_audio_cli"),
            
            # Image tools (placeholders)
            "image.resize": ("tools.image.resize", "resize_image_cli"),
            "image.convert": ("tools.image.convert", "convert_image_cli"),
            
            # Text tools (placeholders)
            "text.sentiment": ("tools.text.sentiment", "analyze_sentiment_cli"),
        }
        
        if ns.tool not in tool_mapping:
            print(f"Error: Unknown tool '{ns.tool}'")
            print("Run 'tools list' to see available tools")
            sys.exit(1)
        
        # Import and call the tool
        module_path, func_name = tool_mapping[ns.tool]
        try:
            module = importlib.import_module(module_path)
            func = getattr(module, func_name)
            func(ns.args)
        except ImportError:
            print(f"Error: Tool '{ns.tool}' is not yet implemented")
            print("Run 'tools list' to see available tools")
            sys.exit(1)
        except AttributeError:
            print(f"Error: Tool '{ns.tool}' is not properly configured")
            sys.exit(1)
        
    except ImportError as e:
        print(f"Error: Could not import tool '{ns.tool}': {e}")
        print("Make sure you have installed the required dependencies.")
        if "audio" in ns.tool:
            print("For audio tools, run: pip install tools[audio]")
        elif "image" in ns.tool:
            print("For image tools, run: pip install tools[image]")
        elif "text" in ns.tool:
            print("For text tools, run: pip install tools[text]")
        sys.exit(1)
    except Exception as e:
        print(f"Error running tool '{ns.tool}': {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 