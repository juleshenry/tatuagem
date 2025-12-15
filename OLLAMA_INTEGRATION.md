# Ollama Integration for Tatuagem

## Overview

This document describes the Ollama integration for the Tatuagem ASCII art generator. The integration allows users to generate ASCII art using Large Language Models (LLMs) through Ollama, providing better Unicode support and the ability to handle arbitrary text input.

## Features

### 1. Ollama-Based ASCII Art Generation
- Generate ASCII art using LLM models like Llama 3.2
- Better Unicode character support
- Handles arbitrary text input
- Customizable model selection

### 2. Automatic Fallback
- If Ollama is not installed, the system falls back to the traditional font-based method
- If Ollama server is not running, automatic fallback occurs
- Seamless user experience with clear warning messages

### 3. Input Sanitization
- Prevents prompt injection attacks
- Validates and sanitizes user input
- Limits input length to reasonable values

### 4. Graceful Dependency Handling
- Ollama package is optional
- System works without Ollama installed
- Clear error messages guide users to install dependencies

## Installation

### Prerequisites
1. Python 3.x with pip
2. Existing Tatuagem dependencies (Pillow, numpy)

### Install Ollama Support
```bash
# Install the Ollama Python package
pip install ollama

# Install Ollama server (visit https://ollama.com/download for your OS)
# Or on Linux/macOS:
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama server
ollama serve

# Pull a model
ollama pull llama3.2
```

## Usage

### Basic Ollama Usage
```bash
# Use Ollama for ASCII art generation
python3 tatuagem.py "Hello World" --use-ollama
```

### With Custom Model
```bash
# Specify a different Ollama model
python3 tatuagem.py "Unicode 你好" --use-ollama --ollama-model llama3.2:latest
```

### With Custom Characters
```bash
# Combine Ollama with custom text/backsplash characters
python3 tatuagem.py "Test" --use-ollama --text '@' --backsplash '.'
```

### With Recursion
```bash
# Apply Ollama-generated tattoo to all files in a directory
python3 tatuagem.py "MyProject" --use-ollama --recurse-path ./src/
```

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--use-ollama` | Enable Ollama-based generation | False |
| `--ollama-model` | Specify Ollama model to use | llama3.2:latest |
| `--text` | Character for text/foreground | 1 |
| `--backsplash` | Character for background | 0 |
| `--margin` | Top/bottom margin | 3 |
| `--pattern` | Pattern for backsplash | None |

## Architecture

### Module Structure

```
tatuagem/
├── tatuagem.py          # Main module with Ollama integration
├── ollama_ascii.py      # Ollama ASCII generation logic
├── initi.py             # Font-based initialization (fallback)
├── recurse.py           # Directory recursion with Ollama support
└── test_ollama_integration.py  # Integration tests
```

### Key Functions

#### `ollama_ascii.py`
- `generate_ascii_art_with_ollama()`: Generate ASCII art using Ollama
- `is_ollama_available()`: Check if Ollama server is running
- `get_available_models()`: List available Ollama models
- `sanitize_text_input()`: Sanitize input to prevent injection

#### `tatuagem.py`
- `get_tattoo_string()`: Main function with Ollama support
- Falls back to font-based method if Ollama unavailable

## How It Works

1. **User requests Ollama generation** with `--use-ollama` flag
2. **System checks** if Ollama package is installed
3. **System checks** if Ollama server is running
4. **Input is sanitized** to prevent prompt injection
5. **LLM generates** ASCII art based on the prompt
6. **Response is cleaned** (removing markdown code blocks if present)
7. **Margins are added** according to user settings
8. **If any step fails**, system falls back to font-based method

## Security

### Input Sanitization
- Removes control characters
- Limits to printable alphanumeric and common punctuation
- Enforces maximum input length (200 characters)
- Prevents prompt injection attacks

### Dependency Safety
- Graceful handling of missing dependencies
- No crashes if Ollama is not installed
- Clear error messages for users

## Testing

### Run Integration Tests
```bash
python3 test_ollama_integration.py
```

### Run Demo
```bash
./demo.sh
```

### Manual Testing
```bash
# Test fallback behavior (Ollama not available)
python3 tatuagem.py "Test" --use-ollama

# Test with Ollama available (requires Ollama server)
ollama serve &
python3 tatuagem.py "Test" --use-ollama
```

## Troubleshooting

### "Ollama not available" Warning
- **Cause**: Ollama package not installed or server not running
- **Solution**: Install ollama package and start server:
  ```bash
  pip install ollama
  ollama serve
  ```

### "ollama package not installed" Error
- **Cause**: Python ollama package missing
- **Solution**: `pip install ollama`

### Empty or Incorrect Output
- **Cause**: Model might not be available or input too complex
- **Solution**: 
  - Pull the model: `ollama pull llama3.2`
  - Try simpler input text
  - Check Ollama server logs

### Slow Generation
- **Cause**: LLM inference takes time, especially on CPU
- **Solution**: 
  - Use a smaller model
  - Be patient (first generation is slower)
  - Consider GPU acceleration for Ollama

## Performance Considerations

- **First run**: Slower due to model loading
- **Subsequent runs**: Faster as model stays in memory
- **Network**: No internet needed once model is downloaded
- **Resources**: LLMs require significant RAM/CPU

## Future Improvements

Possible enhancements:
1. Cache generated ASCII art for repeated text
2. Support for more Ollama models
3. Configurable prompt templates
4. Batch generation mode
5. Quality validation of generated art

## Contributing

When adding features to the Ollama integration:
1. Maintain backward compatibility
2. Keep fallback mechanism working
3. Add tests for new functionality
4. Update this documentation
5. Follow existing code style

## License

Same as the main Tatuagem project.
