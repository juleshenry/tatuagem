import os
import argparse
import shutil
import json
from tatuagem import (
    yield_char_matrix,
    tatuar,
    concat,
    SPACE_MARGIN,
    FONT_DEFAULT,
    DEFAULT_TEXT_CHAR,
    DEFAULT_BACKSPLASH_CHAR,
    MARGIN,
)
from params import TEMPLATE_SIZE
from typing import Optional
import heapq

# Load mappings once
try:
    with open("extension_to_lang.json", "r", encoding="utf-8") as f:
        EXT_TO_LANG = json.load(f)
    with open("lang_to_block_syntax.json", "r", encoding="utf-8") as f:
        LANG_TO_SYNTAX = json.load(f)
except FileNotFoundError:
    print("Warning: JSON mapping files not found.")
    EXT_TO_LANG = {}
    LANG_TO_SYNTAX = {}


def get_tattoo(phrase):
    kwargs = {
        "text": DEFAULT_TEXT_CHAR,
        "backsplash": DEFAULT_BACKSPLASH_CHAR,
        "font": FONT_DEFAULT,
        "pattern": None,
        "margin": MARGIN,
    }
    j = []
    oxo = [[] for _ in range(TEMPLATE_SIZE)]
    for x in phrase:
        cmat = yield_char_matrix(x, **kwargs)
        if not j:
            j = concat(oxo, cmat)
        else:
            j = concat(j, cmat, sep=(kwargs["backsplash"]) * SPACE_MARGIN)
    return tatuar(
        j,
        pattern=kwargs["pattern"],
        backsplash=kwargs["backsplash"],
        margin=kwargs["margin"],
    )


def clean_syntax(s):
    if not s:
        return s
    if s.startswith("`") and s.endswith("`") and len(s) > 1:
        return s[1:-1]
    return s


# Constants for tattoo detection
MIN_TATTOO_LINE_LENGTH = 20  # Minimum line length to consider as tattoo
ASCII_ART_THRESHOLD = 0.8  # Percentage of repeated chars indicating ASCII art
MIN_ASCII_ART_LINES = 5  # Minimum consecutive ASCII art lines to detect tattoo


def comment_text(filepath, text) -> Optional[str]:
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
        # Block comment
        return f"{start}\n{text}\n{end}"
    else:
        # Start == End
        if len(start) >= 3:
            # Likely block delimiter like """
            return f"{start}\n{text}\n{end}"
        else:
            # Likely line comment
            lines = text.split("\n")
            # Remove empty last line from split if text ends with newline
            if lines and not lines[-1]:
                lines.pop()
            commented_lines = [f"{start} {line}" for line in lines]
            return "\n".join(commented_lines)


def apply_tattoo_to_directory(target_path, tattoo):
    print(f"Tattooing into {target_path}...")

    for root, dirs, files in os.walk(target_path):
        for file in files:
            filepath = os.path.join(root, file)
            # Skip if it's likely a binary or hidden file or the script itself
            if file.startswith("."):
                continue

            try:
                # Check if we can comment this file
                commented_tattoo = comment_text(filepath, tattoo)
                if commented_tattoo:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # Check for shebang on first line
                    lines = content.split("\n")
                    shebang = ""
                    content_start_idx = 0
                    if lines and lines[0].strip().startswith("#!"):
                        shebang = lines[0] + "\n"
                        content_start_idx = 1
                    
                    # Get content after shebang (if any)
                    remaining_content = "\n".join(lines[content_start_idx:])
                    
                    # Check if tattoo already exists at the beginning of the file (after shebang)
                    # Look for comment block syntax at start with ASCII art pattern
                    ext = os.path.splitext(os.path.basename(filepath))[1].lower()
                    lang = EXT_TO_LANG.get(ext)
                    syntax = LANG_TO_SYNTAX.get(lang) if lang else None
                    
                    if syntax:
                        start = clean_syntax(syntax.get("start"))
                        end = clean_syntax(syntax.get("end"))
                        
                        # Check if file starts with comment delimiter followed by ASCII art
                        remaining_lines = remaining_content.strip().split("\n")
                        if len(remaining_lines) > 5 and remaining_lines[0].strip().startswith(start):
                            # Look for tattoo pattern: several consecutive lines with mostly 0s and 1s
                            # or other repeated characters (indicating ASCII art)
                            ascii_art_lines = 0
                            for i in range(1, min(10, len(remaining_lines))):
                                line = remaining_lines[i].strip()
                                # Check if line is mostly repeated characters (typical of ASCII art tattoos)
                                if len(line) > MIN_TATTOO_LINE_LENGTH:
                                    # Count repeating characters
                                    char_counts = {}
                                    for char in line:
                                        char_counts[char] = char_counts.get(char, 0) + 1
                                    # If 2-3 characters make up >80% of the line, it's likely ASCII art
                                    top_chars = heapq.nlargest(3, char_counts.values())
                                    if sum(top_chars) > len(line) * ASCII_ART_THRESHOLD:
                                        ascii_art_lines += 1
                            
                            # If we found several ASCII art lines, file is already tattooed
                            if ascii_art_lines >= MIN_ASCII_ART_LINES:
                                print(f"Skipping {filepath} (already tattooed)")
                                continue
                    
                    # Add tattoo after shebang (if present)
                    new_content = shebang + commented_tattoo + "\n\n" + remaining_content
                    
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Tattooed {filepath}")
                else:
                    # print(f"Skipping {filepath} (unknown language)")
                    pass
            except (UnicodeDecodeError, IsADirectoryError, PermissionError):
                pass
            except Exception as e:
                print(f"Error processing {filepath}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Recurse directory and add tattoo comments"
    )
    parser.add_argument("--text", required=True, help="Text to tattoo")
    parser.add_argument("--path", required=True, help="Path to recurse")

    args = parser.parse_args()

    target_path = os.path.expanduser(args.path)
    if not os.path.exists(target_path):
        print(f"Path not found: {target_path}")
        return

    tattoo = get_tattoo(args.text).strip()
    apply_tattoo_to_directory(target_path, tattoo)


if __name__ == "__main__":
    main()
