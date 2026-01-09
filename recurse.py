import os
import argparse
import shutil
import json
import fnmatch
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
from params import TEMPLATE_SIZE, BASE_DIR
from typing import Optional, List

# Load mappings once
try:
    with open(os.path.join(BASE_DIR, "extension_to_lang.json"), "r", encoding="utf-8") as f:
        EXT_TO_LANG = json.load(f)
    with open(os.path.join(BASE_DIR, "lang_to_block_syntax.json"), "r", encoding="utf-8") as f:
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


def has_shebang(content: str) -> bool:
    """Check if the content starts with a shebang line."""
    if not content:
        return False
    first_line = content.split('\n', 1)[0]
    return first_line.startswith('#!')


def get_shebang(content: str) -> Optional[str]:
    """Extract the shebang line from content if present."""
    if has_shebang(content):
        return content.split('\n', 1)[0]
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
            partial_path = "/".join(path_parts[:i+1])
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
            if not prefix or path.startswith(prefix) or fnmatch.fnmatch(path, prefix + "*"):
                if not suffix or path.endswith(suffix) or fnmatch.fnmatch(path, "*" + suffix):
                    return True
    
    # Standard fnmatch for simple patterns
    return fnmatch.fnmatch(path, pattern)


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
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    # Avoid double tattooing if possible (simple check)
                    # We check if the first line of the tattoo is already in the file
                    tattoo_lines = commented_tattoo.split("\n")
                    if len(tattoo_lines) > 1 and tattoo_lines[1].strip() in content:
                        print(f"Skipping {filepath} (already tattooed?)")
                        continue
                    ext = os.path.splitext(os.path.basename(filepath))[1].lower()
                    lang = EXT_TO_LANG.get(ext)
                    syntax = LANG_TO_SYNTAX.get(lang)
                    if not syntax:
                        continue
                    start = clean_syntax(syntax.get("start"))
                    end = clean_syntax(syntax.get("end"))
                    
                    # Check for shebang and preserve it
                    shebang = get_shebang(content)
                    if shebang:
                        # Remove shebang from content temporarily
                        if '\n' in content:
                            content_without_shebang = content.split('\n', 1)[1]
                        else:
                            # Only shebang, no other content
                            content_without_shebang = ''
                        
                        if content_without_shebang.strip().startswith(start): # already tattooed
                            # Try to extract existing content after tattoo
                            try:
                                parts = content_without_shebang.split(start, 1)
                                if len(parts) > 1:
                                    rest = parts[1].split(end, 1)
                                    if len(rest) > 1:
                                        new_content = shebang + "\n" + commented_tattoo + "\n\n" + rest[1]
                                    else:
                                        new_content = shebang + "\n" + commented_tattoo + "\n\n" + content_without_shebang
                                else:
                                    new_content = shebang + "\n" + commented_tattoo + "\n\n" + content_without_shebang
                            except (IndexError, ValueError):
                                new_content = shebang + "\n" + commented_tattoo + "\n\n" + content_without_shebang
                        else:
                            new_content = shebang + "\n" + commented_tattoo + "\n\n" + content_without_shebang
                    else:
                        if content.strip().startswith(start): # already tattooed
                            # Try to extract existing content after tattoo
                            try:
                                parts = content.split(start, 1)
                                if len(parts) > 1:
                                    rest = parts[1].split(end, 1)
                                    if len(rest) > 1:
                                        new_content = commented_tattoo + "\n\n" + rest[1]
                                    else:
                                        new_content = commented_tattoo + "\n\n" + content
                                else:
                                    new_content = commented_tattoo + "\n\n" + content
                            except (IndexError, ValueError):
                                new_content = commented_tattoo + "\n\n" + content
                        else:
                            new_content = commented_tattoo + "\n\n" + content
                    
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
