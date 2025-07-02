# Tools

A collection of utility tools for LLMs and automation. This project provides a simple, extensible framework for organizing and running various utility tools through a unified command-line interface.

## Features

- **Modular Design**: Tools are organized by category (audio, image, text, etc.)
- **Simple CLI**: Single entry point with intuitive `category.tool` syntax
- **Optional Dependencies**: Install only what you need
- **LLM-Friendly**: Designed to be easily used by AI assistants and automation scripts

## Installation

### Basic Installation
```bash
pip install -e .
```

### With Specific Tool Categories
```bash
# For audio tools
pip install -e .[audio]

# For image tools
pip install -e .[image]

# For text tools
pip install -e .[text]

# For all tools
pip install -e .[all]

# For development
pip install -e .[dev]
```

## Usage

### Command Line Interface

The general syntax is:
```bash
tools <category>.<tool_name> [arguments...]
```

### Available Tools

#### Audio Tools
- **`audio.transcription`** - Transcribe audio files using OpenAI Whisper
  ```bash
  tools audio.transcription audio.mp3
  ```

#### Image Tools (Coming Soon)
- **`image.resize`** - Resize images
- **`image.convert`** - Convert image formats

#### Text Tools (Coming Soon)
- **`text.sentiment`** - Analyze text sentiment
- **`text.summarize`** - Summarize text

### Python API

You can also use the tools directly in Python:

```python
from tools.audio import transcribe_audio

# Transcribe an audio file
transcription = transcribe_audio("audio.mp3")
print(transcription)
```

## Project Structure

```
tools/
├── src/tools/              # Main package
│   ├── audio/              # Audio processing tools
│   ├── image/              # Image processing tools
│   ├── text/               # Text processing tools
│   ├── common/             # Shared utilities
│   └── cli.py              # Command-line interface
├── tests/                  # Test files
├── docs/                   # Documentation
└── scripts/                # Utility scripts
```

## Development

### Adding New Tools

1. Create your tool in the appropriate category directory (e.g., `src/tools/audio/new_tool.py`)
2. Add a CLI function that accepts a list of arguments
3. Register the tool in `src/tools/cli.py`
4. Update the category's `__init__.py` to export your tool
5. Add tests in the corresponding test directory

### Example Tool Structure

```python
# src/tools/audio/new_tool.py
def my_audio_tool(file_path: str, option: str = "default") -> str:
    """Core tool function."""
    # Implementation here
    pass

def my_audio_tool_cli(args: list) -> None:
    """CLI interface for the tool."""
    if len(args) < 1:
        print("Usage: tools audio.my_tool <file_path> [option]")
        return
    
    result = my_audio_tool(args[0], args[1] if len(args) > 1 else "default")
    print(result)
```

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/ tests/
flake8 src/ tests/
```

## Configuration

### Environment Variables

The tools can be configured using environment variables or a `.env` file:

- **`OPENAI_API_KEY`**: Required for audio transcription tools
- **`OPENAI_BASE_URL`**: Optional custom OpenAI API endpoint
- **`TOOLS_OUTPUT_DIR`**: Default output directory for generated files
- **`TOOLS_LOG_LEVEL`**: Logging level (DEBUG, INFO, WARNING, ERROR)

### Using .env Files

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your configuration:
   ```bash
   OPENAI_API_KEY=your_actual_api_key_here
   TOOLS_OUTPUT_DIR=/path/to/your/output
   ```

3. The tools will automatically load the `.env` file from:
   - Current working directory
   - Project root directory

**Note**: Never commit your `.env` file to version control!

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your tool following the project structure
4. Add tests for your tool
5. Submit a pull request

## Roadmap

- [ ] Image processing tools (resize, convert, optimize)
- [ ] Text analysis tools (sentiment, summarization, translation)
- [ ] Document processing tools (PDF, Word, etc.)
- [ ] Web scraping tools
- [ ] Data conversion tools (CSV, JSON, XML)
- [ ] Automation helpers (file operations, system tasks) 