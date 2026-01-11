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
| `--overwrite` | When using `--recurse-path`, this flag allows overwriting existing tattoos in files. Without this flag, files that are already tattooed will be skipped. | `False` |

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

### Replace existing tattoos with --overwrite
Update existing tattoos in files that were already tattooed. Without this flag, already-tattooed files will be skipped.
```bash
python3 tatuagem.py "New Tattoo" --recurse-path test_tattoo/ --overwrite
```

## Features

✓ **Shebang detection and preservation** - files with `#!/...` shebangs keep them at the top

✓ **Safe for npm projects** - tattooed npm projects continue to work after tattooing

✓ **Idempotent** - Tattoos won't repeat on themselves if run multiple times

✓ **.tatignore support** - Exclude specific files and directories from tattooing

## .tatignore

Similar to `.gitignore`, you can create a `.tatignore` file in the root of the directory you want to tattoo to specify patterns of files and directories to exclude from tattooing.

### .tatignore Syntax

The `.tatignore` file supports the following patterns:

- **Simple filenames**: `file.txt` - ignores any file named `file.txt`
- **Wildcards**: `*.log` - ignores all files ending with `.log`
- **Directory patterns**: `node_modules/` - ignores all files in `node_modules` directory
- **Recursive patterns**: `build/**` - ignores all files in `build` and its subdirectories
- **Comments**: Lines starting with `#` are treated as comments
- **Empty lines**: Empty lines are ignored

### .tatignore Example

```
# Ignore log files
*.log

# Ignore build artifacts
build/
dist/

# Ignore dependencies
node_modules/

# Ignore specific files
secrets.py
config.local.json

# Ignore test directories
tests/**
```

### Usage with .tatignore

1. Create a `.tatignore` file in the directory you want to tattoo (or copy `.tatignore.example` from this repository)
2. Add patterns for files/directories to exclude
3. Run tatuagem with `--recurse-path` as usual

```bash
# This will respect patterns in .tatignore
python3 tatuagem.py "MyProject" --recurse-path ./my-project/
```
