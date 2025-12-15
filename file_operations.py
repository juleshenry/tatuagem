"""
File operations for applying tattoos to source code files.

This module handles recursively adding ASCII art comments to source files.
"""

import os
import json
from typing import Optional
from core import get_tattoo_string, DEFAULT_TEXT_CHAR, DEFAULT_BACKSPLASH_CHAR, FONT_DEFAULT, MARGIN

# Load language mappings
try:
    with open("extension_to_lang.json", "r", encoding="utf-8") as f:
        EXT_TO_LANG = json.load(f)
    with open("lang_to_block_syntax.json", "r", encoding="utf-8") as f:
        LANG_TO_SYNTAX = json.load(f)
except FileNotFoundError:
    print("Warning: JSON mapping files not found.")
    EXT_TO_LANG = {}
    LANG_TO_SYNTAX = {}


def clean_syntax(s):
    """
    Remove backticks from syntax delimiters if present.
    
    Args:
        s: Syntax delimiter string
    
    Returns:
        Cleaned syntax string
    """
    if not s:
        return s
    if s.startswith("`") and s.endswith("`") and len(s) > 1:
        return s[1:-1]
    return s


def comment_text(filepath: str, text: str) -> Optional[str]:
    """
    Wrap text in comment syntax appropriate for the file type.
    
    Args:
        filepath: Path to the file (used to determine language)
        text: Text to wrap in comments
    
    Returns:
        Text wrapped in appropriate comment syntax, or None if unknown file type
    
    Note:
        Handles both block comments (/* */) and line comments (//).
        For line comments (start == end, length < 3), each line is prefixed.
        For block comments, text is wrapped with delimiters.
    """
    ext = os.path.splitext(os.path.basename(filepath))[1].lower()
    lang = EXT_TO_LANG.get(ext)
    if not lang:
        return None

    syntax = LANG_TO_SYNTAX.get(lang)
    if not syntax:
        return None

    start = clean_syntax(syntax.get("start"))
    end = clean_syntax(syntax.get("end"))

    if not start or not end or start == "none" or end == "none":
        return None

    if start != end:
        # Block comment (e.g., /* */)
        return f"{start}\n{text}\n{end}"
    else:
        # Start == End case
        if len(start) >= 3:
            # Likely block delimiter like """
            return f"{start}\n{text}\n{end}"
        else:
            # Likely line comment (e.g., //, #)
            lines = text.split("\n")
            # Remove empty last line from split if text ends with newline
            if lines and not lines[-1]:
                lines.pop()
            commented_lines = [f"{start} {line}" for line in lines]
            return "\n".join(commented_lines)


def apply_tattoo_to_directory(target_path: str, tattoo: str):
    """
    Recursively apply a tattoo comment to all source files in a directory.
    
    Args:
        target_path: Root directory to process
        tattoo: ASCII art tattoo string to add as a comment
    
    Note:
        - Skips hidden files (starting with '.')
        - Skips binary files and files without recognized extensions
        - Attempts to avoid double-tattooing by checking if tattoo already exists
        - Only processes files with known comment syntax
    """
    print(f"Tattooing into {target_path}...")

    for root, dirs, files in os.walk(target_path):
        for file in files:
            filepath = os.path.join(root, file)
            
            # Skip hidden files
            if file.startswith("."):
                continue

            try:
                # Check if we can comment this file
                commented_tattoo = comment_text(filepath, tattoo)
                if commented_tattoo:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # Simple check to avoid double tattooing
                    # Check if the second line of the tattoo is already in the file
                    tattoo_lines = commented_tattoo.split("\n")
                    if len(tattoo_lines) > 1 and tattoo_lines[1].strip() in content:
                        print(f"Skipping {filepath} (already tattooed?)")
                        continue
                    
                    # Get comment syntax info
                    ext = os.path.splitext(os.path.basename(filepath))[1].lower()
                    lang = EXT_TO_LANG.get(ext)
                    syntax = LANG_TO_SYNTAX.get(lang) if lang else None
                    
                    if not syntax:
                        continue
                    
                    start = clean_syntax(syntax.get("start"))
                    end = clean_syntax(syntax.get("end"))
                    
                    # If file already starts with comment, replace it
                    # Otherwise, prepend tattoo
                    if content.strip().startswith(start):
                        # Attempt to replace existing comment block
                        try:
                            new_content = commented_tattoo + "\n\n" + content.split(start)[1].split(end)[1]
                        except (IndexError, AttributeError):
                            # If parsing fails, just prepend
                            new_content = commented_tattoo + "\n\n" + content
                    else:
                        new_content = commented_tattoo + "\n\n" + content
                    
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Tattooed {filepath}")
                    
            except (UnicodeDecodeError, IsADirectoryError, PermissionError):
                # Skip binary files or permission errors
                pass
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
