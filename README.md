# Tatuagem, the boastful code signature suite
![coverage](coverage.svg)

Tatuagem is a tool to generate ASCII art signatures (tattoos) and apply them to your code files recursively.

## Usage

```bash
python3 tatuagem.py [text_input] [options]
```

### Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `text_input` | The string you want to convert into a tattoo. Required if `--file` is not provided. | None |
| `--text` | The character used to draw the text pixels. | `1` |
| `--backsplash` | The character used to fill the background. | `0$*~` |
| `--font` | The TrueType font file (.ttf) to use for generating the text shape. | `unicode-arial.ttf` |
| `--pattern` | A repeating string pattern to use for the background. Overrides `--backsplash`. | None |
| `--margin` | Number of empty lines (margin) to add above and below the text. | `3` |
| `--recurse-path` | Path to a directory. Tatuagem will walk through this directory and prepend the tattoo to every file found. | None |
| `--file`, `-f` | Path to a file containing text. <br>• **Standard Mode**: The content of the file is converted into the tattoo art.<br>• **Recurse Mode** (with `--recurse-path`): The content of the file is used *as-is* for the tattoo (useful for pre-generated art). | None |
| `--ollama-studio` | Interactive Ollama tattoo studio. Generate AI-powered ASCII art from a text prompt with an interactive CLI menu to add headers and footers. Requires Ollama to be installed. | None |

## Examples

### Basic Example
Generate a simple tattoo.
```bash
python3 tatuagem.py "tatuagem"
```
*Defaults: '1' for text, '0' for background, unicode-arial.ttf for font*

### Elaborate Syntax Example
Customizing the text and background characters.
```bash
python3 tatuagem.py "L'appel du vide" --font 'unicode-arial.ttf' --backsplash '!' --text '@'
```

![alt text](lappel.png)

### Wallpaper: Pattern-Argument Syntax Example
Using a pattern string for the background.
```bash
python3 tatuagem.py "Tatuagem" --pattern '`':,:''
```

![alt text](tatu.png)

### Recurse your project
Apply the generated tattoo to all files in `test_tattoo/`.
```bash
python tatuagem.py "Tatuagem" --pattern '`':,:''  --recurse-path test_tattoo/
```

### Recurse your project with a text file
Apply the contents of `tests/aeaea.inc` as a header to all files in `test_tattoo/`.
```bash
python3 tatuagem.py --file tests/aeaea.inc --recurse-path test_tattoo/
```

### Ollama Studio (AI-Powered ASCII Art)
Generate AI-powered ASCII art using Ollama's language models with an interactive CLI menu.

**Requirements**: Install [Ollama](https://ollama.ai/) and ensure the `llama3` model is available.

**Basic usage:**
```bash
python3 tatuagem.py --ollama-studio "A majestic dragon"
```

**Interactive workflow:**
1. **Generate tattoo from prompt** - AI generates ASCII art, you confirm or regenerate
2. **Choose add-ons** - Select header (h), footer (f), both (b), or neither (n)
3. **Customize header** - Enter text, preview in Tatuagem style, confirm or redo
4. **Customize footer** - Enter text, preview in Tatuagem style, confirm or redo
5. **Final output** - View complete tattoo with all selected elements

**With customization:**
```bash
python3 tatuagem.py --ollama-studio "A cat" --text "@" --backsplash "." --pattern "~`"
```

**Demo:**
```bash
python3 demo_ollama_studio.py
```

## Features

✓ **Shebang detection and preservation** - files with `#!/...` shebangs keep them at the top
✓ **Safe for npm projects** - tattooed npm projects continue to work after tattooing
✓ **Idempotent** - Tattoos won't repeat on themselves if run multiple times
✓ **Ollama Studio** - AI-powered ASCII art generation with interactive CLI menu for headers and footers
