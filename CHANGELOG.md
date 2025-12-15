# Changelog

All notable changes to this project will be documented in this file.

## [Refactor Release] - 2024-12-15

### Added
- **cli.py**: New centralized command-line interface with clear help text and examples
- **core.py**: Core tattoo generation logic with comprehensive docstrings
- **font_manager.py**: Font template creation and management module
- **file_operations.py**: Directory recursion and comment injection functionality
- Comprehensive inline documentation explaining complex behavior
- Enhanced .gitignore to exclude build artifacts and caches
- This CHANGELOG to track project changes

### Changed
- **tatuagem.py**: Now a legacy wrapper with deprecation warnings, maintained for backward compatibility
- **initi.py**: Now a legacy wrapper pointing to font_manager.py
- **recurse.py**: Now a legacy wrapper pointing to file_operations.py
- **README.md**: Updated with new structure, clearer examples, and migration guidance
- All modules now have proper docstrings explaining their purpose and usage

### Removed
- **coverage.py**: Removed incomplete/broken coverage badge generator
- **identify_comments.py**: Removed unused LLM-based comment identifier (required ollama)
- **override.py**: Removed simple comparison script
- Large ASCII art header from tatuagem.py (reduced clutter)

### Fixed
- Better organization prevents spaghetti code
- Clearer separation of concerns between modules
- Easier to add new features without breaking existing code

### Technical Details

#### Strange Behavior Documentation
The following behaviors are now documented with inline comments:

1. **Space character handling** (core.py:yield_char_matrix): 
   - Space characters only render margin columns to reduce width
   - This is because the space template is a solid sheet

2. **Column skipping** (core.py:yield_char_matrix):
   - Empty columns (all background pixels) are skipped to reduce output width
   - This optimizes the visual output but can be confusing

3. **Lowercase file naming** (font_manager.py:get_font_png_path):
   - Lowercase letters get special filenames for NIX filesystem compatibility
   - Prevents case-sensitivity issues on different operating systems

4. **Double tattoo prevention** (file_operations.py:apply_tattoo_to_directory):
   - Simple check to avoid applying tattoos multiple times
   - Checks if tattoo content is already present in file

### Migration Guide

#### For Command-Line Users
Old:
```bash
python tatuagem.py "Text" --text '@' --backsplash '!'
```

New:
```bash
python cli.py "Text" --text '@' --backsplash '!'
```

#### For Python API Users
Old:
```python
from tatuagem import get_tattoo_string, tatuagem
tatuagem("Hello", text='1', backsplash='0', font='unicode-arial.ttf', pattern=None, margin=3)
```

New:
```python
from core import get_tattoo_string, print_tattoo
print_tattoo("Hello", text='1', backsplash='0', font='unicode-arial.ttf', pattern=None, margin=3)
```

#### For Directory Recursion
Old:
```python
from recurse import apply_tattoo_to_directory, get_tattoo
tattoo = get_tattoo("Project")
apply_tattoo_to_directory("./src/", tattoo)
```

New:
```python
from core import get_tattoo_string
from file_operations import apply_tattoo_to_directory
tattoo = get_tattoo_string("Project", text='1', backsplash='0', font='unicode-arial.ttf', pattern=None, margin=3)
apply_tattoo_to_directory("./src/", tattoo)
```

Or simply use the CLI:
```bash
python cli.py "Project" --recurse-path ./src/
```
