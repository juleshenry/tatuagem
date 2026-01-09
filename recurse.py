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
from params import TEMPLATE_SIZE, BASE_DIR
from typing import Optional

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
