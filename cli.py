"""
Command-line interface for Tatuagem.

This module provides a clean, organized CLI for generating ASCII art tattoos
and applying them to source code files.
"""

import argparse
import os
import sys

from core import (
    print_tattoo, get_tattoo_string, SPACE_MARGIN, FONT_DEFAULT,
    DEFAULT_TEXT_CHAR, DEFAULT_BACKSPLASH_CHAR, MARGIN
)
from font_manager import init_and_create_templates
from file_operations import apply_tattoo_to_directory


def create_parser():
    """
    Create and configure the argument parser.
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="Tatuagem - Generate ASCII art tattoos from text",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage - print tattoo to stdout
  python cli.py "Hello World"
  
  # Custom text and background characters
  python cli.py "Code" --text '@' --backsplash '!'
  
  # Apply pattern to background
  python cli.py "Pattern" --pattern "\`':,:'"
  
  # Apply tattoo to all files in a directory
  python cli.py "MyProject" --recurse-path ./src/
  
  # Use custom font
  python cli.py "Custom" --font myfont.ttf
        """
    )
    
    # Positional argument for the text to tattoo
    parser.add_argument(
        "phrase",
        help="Text phrase to convert to ASCII art tattoo"
    )
    
    # Appearance options
    appearance = parser.add_argument_group("appearance options")
    appearance.add_argument(
        "--text",
        default=DEFAULT_TEXT_CHAR,
        help=f"Character to use for foreground/text (default: '{DEFAULT_TEXT_CHAR}')"
    )
    appearance.add_argument(
        "--backsplash",
        default=DEFAULT_BACKSPLASH_CHAR,
        help=f"Character to use for background (default: '{DEFAULT_BACKSPLASH_CHAR}')"
    )
    appearance.add_argument(
        "--pattern",
        default=None,
        metavar="PATTERN",
        help="Pattern string to overlay on background (e.g., \"`':,:\")"
    )
    appearance.add_argument(
        "--margin",
        type=int,
        default=MARGIN,
        help=f"Number of blank lines for top and bottom margin (default: {MARGIN})"
    )
    
    # Font options
    font_group = parser.add_argument_group("font options")
    font_group.add_argument(
        "--font",
        default=FONT_DEFAULT,
        metavar="FONT",
        help=f"Font file to use (default: {FONT_DEFAULT})"
    )
    
    # File operations
    file_ops = parser.add_argument_group("file operations")
    file_ops.add_argument(
        "--recurse-path",
        metavar="PATH",
        help="Apply tattoo as comments to all source files in the specified directory"
    )
    
    return parser


def main():
    """
    Main entry point for the CLI.
    """
    parser = create_parser()
    args = parser.parse_args()
    
    # Check if font templates exist, create if needed
    font_dir = f"./fonts/{args.font[:-4]}"
    if not os.path.exists(font_dir):
        print(f"Font templates not found. Creating templates for {args.font}...")
        init_and_create_templates(args.font)
    
    # Build kwargs for tattoo generation
    tattoo_kwargs = {
        "text": args.text,
        "backsplash": args.backsplash,
        "font": args.font,
        "pattern": args.pattern,
        "margin": args.margin,
    }
    
    # Display configuration
    print(f"text: {args.text}")
    print(f"backsplash: {args.backsplash}")
    print(f"font: {args.font}")
    print(f"pattern: {args.pattern}")
    print(f"margin: {args.margin}")
    print()
    
    # Execute the requested operation
    if args.recurse_path:
        # Apply tattoo to directory
        tattoo = get_tattoo_string(args.phrase, **tattoo_kwargs)
        apply_tattoo_to_directory(args.recurse_path, tattoo)
    else:
        # Print tattoo to stdout
        print_tattoo(args.phrase, **tattoo_kwargs)


if __name__ == "__main__":
    main()
