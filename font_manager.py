"""
Font template generation and management.

This module handles creating PNG templates for each character in a font.
"""

from params import TEMPLATE_SIZE, Image, ImageDraw, ImageFont, CHZ
import numpy as np
import os


def get_font_png_path(char: str, new_dir: str):
    """
    Returns the path of the PNG file corresponding to a character.
    
    Args:
        char: The character to get the path for
        new_dir: Directory where font PNG files are stored
    
    Returns:
        Path to the PNG file for this character
    
    Note:
        Special handling for lowercase letters (NIX compatibility) and
        special characters like '/'.
    """
    # Lowercase treated separately for NIX filesystem compatibility
    if 97 <= ord(char) <= 97 + 26:
        font_png_path = f"{new_dir}/__lowercase_{char}__.png"
    elif char in r"/":
        # Use chr() representation for filesystem-unsafe characters
        font_png_path = f"{new_dir}/__chr({ord(char)})__.png"
    else:
        font_png_path = f"{new_dir}/__{char}__.png"
    return font_png_path


def init_and_create_templates(font: str):
    """
    Initialize font templates by creating PNG files for all printable characters.
    
    Args:
        font: Font filename (e.g., 'unicode-arial.ttf')
    
    Note:
        Creates a directory structure: fonts/<font-name>/__<char>__.png
        Uses a black template image and renders each character in yellow.
        Templates are 64x64 pixels (TEMPLATE_SIZE).
    """
    btpng = "black-template.png"
    new_dir = f"fonts/{font[:-4]}"  # Remove .ttf extension
    
    # Create black template image
    sqr = np.zeros((TEMPLATE_SIZE, TEMPLATE_SIZE, 3))
    i = Image.fromarray(sqr, "RGB")
    i.save(btpng)
    
    # Create directory if it doesn't exist
    try:
        os.mkdir(new_dir)
    except FileExistsError:
        pass
    
    # Generate PNG for each printable character
    for o in CHZ:
        print("making", o)
        img = Image.open(btpng)
        fnt = ImageFont.truetype(f"fonts/{font}", 32)
        i1 = ImageDraw.Draw(img)
        anch = "la"
        i1.text(
            (24, 8),
            o,
            anchor=anch,
            font=fnt,
            fill=(255, 255, 0),
        )
        font_png_path = get_font_png_path(o, new_dir)
        img.save(font_png_path)
    
    print("done")


if __name__ == "__main__":
    # Allow running this module directly to generate templates
    import sys
    if len(sys.argv) > 1:
        init_and_create_templates(sys.argv[1])
    else:
        init_and_create_templates("unicode-arial.ttf")
