"""
DEPRECATED: This file is maintained for backward compatibility only.
Please use file_operations.py and cli.py instead.
"""

import warnings
warnings.warn(
    "recurse.py is deprecated. Please use 'python cli.py --recurse-path <path> \"text\"' instead.",
    DeprecationWarning,
    stacklevel=2
)

import os
import argparse
from file_operations import apply_tattoo_to_directory, comment_text, clean_syntax
from core import get_tattoo_string, DEFAULT_TEXT_CHAR, DEFAULT_BACKSPLASH_CHAR, FONT_DEFAULT, MARGIN

# Backward compatibility wrapper
def get_tattoo(phrase):
    """DEPRECATED: Use core.get_tattoo_string() instead."""
    return get_tattoo_string(
        phrase,
        text=DEFAULT_TEXT_CHAR,
        backsplash=DEFAULT_BACKSPLASH_CHAR,
        font=FONT_DEFAULT,
        pattern=None,
        margin=MARGIN
    )


def main():
    parser = argparse.ArgumentParser(
        description="Recurse directory and add tattoo comments (DEPRECATED - use cli.py)"
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
