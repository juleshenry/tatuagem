"""
DEPRECATED: This file is maintained for backward compatibility only.
Please use cli.py for the command-line interface.

Legacy main entry point for Tatuagem ASCII art generator.
"""

import warnings
warnings.warn(
    "tatuagem.py is deprecated. Please use 'python cli.py' instead.",
    DeprecationWarning,
    stacklevel=2
)

from core import (
    yield_char_matrix, concat, tatuar, get_tattoo_string, print_tattoo as tatuagem,
    MARGIN, SPACE_MARGIN, FONT_DEFAULT, DEFAULT_TEXT_CHAR, DEFAULT_BACKSPLASH_CHAR
)
from font_manager import init_and_create_templates
import argparse
import os

KWARGS_LIST = {"text", "backsplash", "font", "pattern", "margin"}


# Legacy expose function for backward compatibility
def expose(mat, pattern=None, backsplash=None, margin=None):
    """DEPRECATED: Use core.tatuar() instead."""
    tatu = tatuar(mat, pattern=pattern, backsplash=backsplash, margin=margin)
    print(tatu)


if __name__ == "__main__":
    # Legacy CLI - redirect to new cli.py
    parser = argparse.ArgumentParser(description="Tatuagem (DEPRECATED - use cli.py)")
    parser.add_argument("--text", default=DEFAULT_TEXT_CHAR, help="Set the text")
    parser.add_argument("--backsplash", default=DEFAULT_BACKSPLASH_CHAR, help="Choose backsplash")
    parser.add_argument("--font", default=FONT_DEFAULT, metavar="FONT", help="Set the font")
    parser.add_argument("--pattern", default=None, metavar="PATTERN", help="Set the pattern for backsplash")
    parser.add_argument("--margin", default=MARGIN, help="Margin top and bottom for text")
    parser.add_argument("--recurse-path", help="Path to recurse and apply tattoo")

    args, positional_args = parser.parse_known_args()
    
    if not positional_args:
        parser.error("Please provide a text phrase to tattoo")
    
    font_dir = f"./fonts/{args.font[:-4]}"
    if not os.path.exists(font_dir):
        init_and_create_templates(args.font)
    
    print(f"text: {args.text}")
    print(f"backsplash: {args.backsplash}")
    print(f"font: {args.font}")
    print(f"pattern: {args.pattern}")
    print(f"margin: {args.margin}")
    arg0_frase = positional_args[0]

    if args.recurse_path:
        from file_operations import apply_tattoo_to_directory
        tattoo = get_tattoo_string(arg0_frase, **{a: getattr(args, a) for a in KWARGS_LIST})
        apply_tattoo_to_directory(args.recurse_path, tattoo)
    else:
        tatuagem(arg0_frase, **{a: getattr(args, a) for a in KWARGS_LIST})
