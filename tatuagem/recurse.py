import os
import sys
import argparse
import shutil
import json
import fnmatch
from . import core
from .core import (
    yield_char_matrix,
    tatuar,
    concat,
    SPACE_MARGIN,
    FONT_DEFAULT,
    DEFAULT_TEXT_CHAR,
    DEFAULT_BACKSPLASH_CHAR,
    MARGIN,
)
from .params import TEMPLATE_SIZE, BASE_DIR
from typing import Optional, List


# Load mappings once
def load_json_mappings():
    try:
        ext_to_lang_path = os.path.join(BASE_DIR, "extension_to_lang.json")
        lang_to_syntax_path = os.path.join(BASE_DIR, "lang_to_block_syntax.json")

        with open(ext_to_lang_path, "r", encoding="utf-8") as f:
            ext_to_lang = json.load(f)
        with open(lang_to_syntax_path, "r", encoding="utf-8") as f:
            lang_to_syntax = json.load(f)
        return ext_to_lang, lang_to_syntax
    except FileNotFoundError:
        # Try relative to this file if BASE_DIR fails or is weird
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            ext_to_lang_path = os.path.join(current_dir, "extension_to_lang.json")
            lang_to_syntax_path = os.path.join(current_dir, "lang_to_block_syntax.json")
            with open(ext_to_lang_path, "r", encoding="utf-8") as f:
                ext_to_lang = json.load(f)
            with open(lang_to_syntax_path, "r", encoding="utf-8") as f:
                lang_to_syntax = json.load(f)
            return ext_to_lang, lang_to_syntax
        except FileNotFoundError:
            print("Warning: JSON mapping files not found.")
            return {}, {}


EXT_TO_LANG, LANG_TO_SYNTAX = load_json_mappings()


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


def has_shebang(content: str) -> bool:
    """Check if the content starts with a shebang line."""
    if not content:
        return False
    first_line = content.split("\n", 1)[0]
    return first_line.startswith("#!")


def get_shebang(content: str) -> Optional[str]:
    """Extract the shebang line from content if present."""
    if has_shebang(content):
        return content.split("\n", 1)[0]
    return None


def load_tatignore_patterns(target_path: str) -> List[str]:
    """
    Load patterns from .tatignore file in the target directory.
    Returns a list of patterns to ignore.
    """
    tatignore_path = os.path.join(target_path, ".tatignore")
    patterns = []

    if os.path.exists(tatignore_path):
        try:
            with open(tatignore_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith("#"):
                        patterns.append(line)
        except Exception as e:
            print(f"Warning: Could not read .tatignore file: {e}")

    return patterns


def should_ignore(filepath: str, target_path: str, patterns: List[str]) -> bool:
    """
    Check if a file should be ignored based on .tatignore patterns.
    Similar to .gitignore, supports:
    - Simple filenames: "file.txt"
    - Wildcards: "*.log"
    - Directory patterns: "node_modules/"
    - Path patterns: "build/**"
    """
    if not patterns:
        return False

    # Get relative path from target directory
    try:
        rel_path = os.path.relpath(filepath, target_path)
    except ValueError:
        # If paths are on different drives (Windows), use absolute comparison
        rel_path = filepath

    # Normalize path separators
    rel_path = rel_path.replace(os.sep, "/")

    for pattern in patterns:
        # Remove trailing slash for directory patterns
        pattern = pattern.rstrip("/")

        # Check for exact match
        if rel_path == pattern:
            return True

        # Check if pattern matches filename
        filename = os.path.basename(filepath)
        if _match_pattern(filename, pattern):
            return True

        # Check if pattern matches any part of the path
        if _match_pattern(rel_path, pattern):
            return True

        # Check if any directory in the path matches the pattern
        path_parts = rel_path.split("/")
        for i in range(len(path_parts)):
            partial_path = "/".join(path_parts[: i + 1])
            if _match_pattern(partial_path, pattern):
                return True

            # Check directory names
            if _match_pattern(path_parts[i], pattern):
                return True

    return False


def _match_pattern(path: str, pattern: str) -> bool:
    """
    Match a path against a pattern using fnmatch-like behavior.
    Supports wildcards (* and ?) and ** for recursive matching.
    """
    # Handle ** for recursive directory matching
    if "**" in pattern:
        # Convert ** pattern to regex-like matching
        parts = pattern.split("**")
        if len(parts) == 2:
            prefix, suffix = parts
            prefix = prefix.rstrip("/")
            suffix = suffix.lstrip("/")

            # Check if path matches the pattern with ** in between
            if (
                not prefix
                or path.startswith(prefix)
                or fnmatch.fnmatch(path, prefix + "*")
            ):
                if (
                    not suffix
                    or path.endswith(suffix)
                    or fnmatch.fnmatch(path, "*" + suffix)
                ):
                    return True

    # Standard fnmatch for simple patterns
    return fnmatch.fnmatch(path, pattern)


def is_tattoo_comment(text: str, min_lines: int = 15) -> bool:
    """
    Determine if a comment block is a tattoo (ASCII art) rather than human-readable documentation.

    A tattoo is characterized by:
    - Large number of lines (usually > 20)
    - High density of '0' and '1' characters (default for this tool)
    - Very few actual words
    """
    if not text or not text.strip():
        return False

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Need a significant number of lines to be a tattoo from this tool
    if len(lines) < min_lines:
        return False

    total_chars = 0
    pattern_chars = 0
    alnum_chars = 0

    for line in lines:
        for char in line:
            total_chars += 1
            if char in "01 \t":
                pattern_chars += 1
            if char.isalnum():
                alnum_chars += 1

    if total_chars == 0:
        return False

    # Ratio of 0, 1, and spaces
    pattern_ratio = pattern_chars / total_chars

    # Ratio of alphanumeric characters that are NOT 0 or 1
    # Real words will have many other letters
    other_alnum_chars = 0
    for line in lines:
        for char in line:
            if char.isalnum() and char not in "01":
                other_alnum_chars += 1

    other_alnum_ratio = other_alnum_chars / total_chars if total_chars > 0 else 0

    # It's a tattoo if it's mostly 0/1/space AND has very few other letters
    return pattern_ratio > 0.8 and other_alnum_ratio < 0.05


def extract_first_comment(content: str, start: str, end: str) -> Optional[str]:
    """
    Extract the content of the first comment block in the file.

    Args:
        content: The file content
        start: Comment start delimiter
        end: Comment end delimiter

    Returns:
        The text inside the first comment block, or None if not found
    """
    if not content.strip().startswith(start):
        return None

    try:
        # For line comments where start == end and it's short (like //, #)
        # vs block comments where start == end but it's long (like """, ''')
        is_line_comment = (start == end) and len(start) <= 2

        if is_line_comment:
            # Line comments - extract consecutive commented lines
            lines = content.split("\n")
            comment_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith(start):
                    # Remove the comment delimiter and add to list
                    comment_lines.append(line.replace(start, "", 1))
                elif comment_lines:
                    # Stop when we hit a non-comment line after starting
                    break
            return "\n".join(comment_lines)
        else:
            # Block comments
            # Split by start delimiter
            parts = content.split(start, 1)
            if len(parts) <= 1:
                return None

            # Get the part after start delimiter
            after_start = parts[1]

            # Split by end delimiter
            comment_parts = after_start.split(end, 1)
            if not comment_parts:
                return None

            # Return the comment content (without delimiters)
            comment_content = comment_parts[0]
            return comment_content.strip()
    except (IndexError, ValueError):
        return None


def comment_text(filepath, text) -> Optional[str]:
    """Return commented text based on file extension and language syntax."""
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
        if lang == "Python" and start == '"""':
            return f"r{start}\n{text}\n{end}"
        return f"{start}\n{text}\n{end}"
    else:
        # Start == End
        if len(start) >= 3:
            # Likely block delimiter like """
            if lang == "Python" and start == '"""':
                return f"r{start}\n{text}\n{end}"
            return f"{start}\n{text}\n{end}"
        else:
            # Likely line comment
            lines = text.split("\n")
            # Remove empty last line from split if text ends with newline
            if lines and not lines[-1]:
                lines.pop()
            commented_lines = [f"{start} {line}" for line in lines]
            return "\n".join(commented_lines)


def apply_tattoo_to_directory(target_path, tattoo, overwrite=False):
    print(f"Tattooing into {target_path}...")

    # Load .tatignore patterns
    ignore_patterns = load_tatignore_patterns(target_path)
    if ignore_patterns:
        print(f"Loaded {len(ignore_patterns)} ignore pattern(s) from .tatignore")

    for root, dirs, files in os.walk(target_path):
        for file in files:
            filepath = os.path.join(root, file)
            # Skip if it's likely a binary or hidden file or the script itself
            if file.startswith("."):
                continue

            # Check if file should be ignored based on .tatignore
            if should_ignore(filepath, target_path, ignore_patterns):
                print(f"Skipping {filepath} (matched .tatignore)")
                continue

            try:
                # Check if we can comment this file
                commented_tattoo = comment_text(filepath, tattoo)
                if commented_tattoo:
                    ext = os.path.splitext(os.path.basename(filepath))[1].lower()
                    lang = EXT_TO_LANG.get(ext)
                    syntax = LANG_TO_SYNTAX.get(lang)
                    if not syntax:
                        continue
                    start = clean_syntax(syntax.get("start"))
                    end = clean_syntax(syntax.get("end"))

                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Check for shebang and preserve it
                    shebang = get_shebang(content)
                    if shebang:
                        content_body = (
                            content.split("\n", 1)[1] if "\n" in content else ""
                        )
                    else:
                        content_body = content

                    # More robust double-tattooing check
                    # We check if the file already starts with a tattoo comment
                    has_existing_tattoo = False
                    first_comment_content = None

                    # We look at the body (after shebang)
                    syntax = LANG_TO_SYNTAX.get(lang)
                    if not syntax:
                        continue
                    start = clean_syntax(syntax.get("start"))
                    end = clean_syntax(syntax.get("end"))

                    if content_body.strip().startswith(start):
                        first_comment_content = extract_first_comment(
                            content_body, start, end
                        )
                        if first_comment_content and is_tattoo_comment(
                            first_comment_content
                        ):
                            has_existing_tattoo = True

                    if has_existing_tattoo:
                        # If we have an existing tattoo, compare it with the new one
                        if (
                            first_comment_content
                            and first_comment_content.strip() == tattoo.strip()
                        ):
                            print(
                                f"Skipping {filepath} (already tattooed with this exact content)"
                            )
                            continue

                        if not overwrite:
                            print(
                                f"Skipping {filepath} (already tattooed, use --overwrite to replace)"
                            )
                            continue

                        # Replace existing tattoo
                        # Determine where the existing tattoo ends
                        is_line_comment = (start == end) and len(start) <= 2
                        if is_line_comment:
                            lines = content_body.split("\n")
                            # Find start of tattoo (skip potential empty lines after shebang)
                            i = 0
                            while i < len(lines) and not lines[i].strip().startswith(
                                start
                            ):
                                i += 1
                            # Skip all consecutive comment lines
                            while i < len(lines) and lines[i].strip().startswith(start):
                                i += 1
                            body_without_tattoo = "\n".join(lines[i:]).lstrip()
                        else:
                            # Block comment replacement
                            parts = content_body.split(end, 1)
                            body_without_tattoo = (
                                parts[1].lstrip() if len(parts) > 1 else content_body
                            )

                        new_content = (
                            (shebang + "\n" if shebang else "")
                            + commented_tattoo
                            + "\n\n"
                            + body_without_tattoo
                        )
                        print(f"Re-tattooed {filepath} (replaced existing tattoo)")
                    else:
                        # Prepend tattoo (preserving shebang if present)
                        new_content = (
                            (shebang + "\n" if shebang else "")
                            + commented_tattoo
                            + "\n\n"
                            + content_body.lstrip()
                        )
                        print(f"Tattooed {filepath}")

                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
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
