"""
Core tattoo generation logic.

This module contains the primary functions for generating ASCII art "tattoos"
from text strings using custom fonts.
"""

from params import TEMPLATE_SIZE
from font_manager import get_font_png_path
from PIL import Image

# Default configuration
MARGIN = 3  # top and bottom margin of text
SPACE_MARGIN = 4  # Space width in characters (space file is a solid sheet)
FONT_DEFAULT = "unicode-arial.ttf"
DEFAULT_TEXT_CHAR = "1"
DEFAULT_BACKSPLASH_CHAR = "0"


def yield_char_matrix(char: str, font: str = FONT_DEFAULT, text: str = DEFAULT_TEXT_CHAR, 
                      backsplash: str = DEFAULT_BACKSPLASH_CHAR, **kwargs):
    """
    Convert a character to a binary matrix representation.
    
    Args:
        char: The character to convert
        font: Font name (without path, e.g., 'unicode-arial.ttf')
        text: Character to use for foreground pixels
        backsplash: Character to use for background pixels
        **kwargs: Additional arguments (ignored)
    
    Returns:
        List of lists representing the character as a matrix
    
    Note:
        Special handling for space character: only renders margins to reduce width.
        Skips empty columns (columns with all background pixels) to reduce output width.
    """
    new_dir = f"fonts/{font[:-4]}"
    fpp = get_font_png_path(char, new_dir)
    imat = Image.open(fpp).quantize().getdata()
    o = [[] for _ in range(imat.size[1])]
    
    # Process each pixel
    for ix, h in enumerate(range(imat.size[1])):
        for w in range(imat.size[0]):
            # Special space handling: only keep margin columns
            if char == " " and (SPACE_MARGIN < w < TEMPLATE_SIZE - SPACE_MARGIN):
                continue
            
            # Skip empty columns (all background pixels) for non-space characters
            if not sum([o - imat.getpixel((0, 0)) for o in [imat.getpixel((w, i)) for i in range(imat.size[1])]]) and char != " ":
                continue
            
            # Determine if pixel is foreground or background
            o[ix].append(
                text if imat.getpixel((w, h)) - imat.getpixel((0, 0)) else backsplash
            )
    
    return o


def concat(cmat, amat, sep: str = ""):
    """
    Concatenate two character matrices horizontally.
    
    Args:
        cmat: First character matrix
        amat: Second character matrix
        sep: Separator string to insert between matrices
    
    Returns:
        Combined character matrix
    
    Raises:
        ValueError: If matrices have different heights
    """
    if not len(cmat) == len(amat):
        raise ValueError("equal len required")

    x = [[] for _ in range(len(cmat))]
    for ix, ab in enumerate(zip(cmat, amat)):
        a, b = ab
        x[ix] = a + ([sep] if a and b else []) + b
    return x


def tatuar(mat, pattern=None, backsplash=None, margin=None):
    """
    Convert a character matrix to a string with optional pattern overlay.
    
    Args:
        mat: Character matrix to render
        pattern: Optional pattern string to overlay on background characters
        backsplash: Background character
        margin: Number of blank lines to add at top and bottom
    
    Returns:
        String representation of the matrix with newlines
    
    Note:
        Filters out empty rows and rows that are all background characters.
        Pattern cycles through characters if provided.
    """
    # Filter empty rows and all-background rows
    pure_mat = list(
        filter(lambda x: x and not all(c == backsplash for c in "".join(x)), mat)
    )
    
    margin = int(margin)
    # Add margin rows
    marg = [[backsplash * sum([len(x) for x in pure_mat[0]])] for _ in range(margin)]
    pure_mat = marg + pure_mat + marg
    
    tatuagem = ""
    for text_list in pure_mat:
        out = "".join(text_list)
        if pattern:
            # Apply pattern to background characters
            for i, c in enumerate(out):
                tatuagem += pattern[i % len(pattern)] if c == backsplash else c
        else:
            tatuagem += out
        tatuagem += "\n"
    return tatuagem


def get_tattoo_string(phrase: str, space_count: int = SPACE_MARGIN, text: str = DEFAULT_TEXT_CHAR,
                      backsplash: str = DEFAULT_BACKSPLASH_CHAR, font: str = FONT_DEFAULT,
                      pattern=None, margin=MARGIN):
    """
    Generate an ASCII art tattoo from a text phrase.
    
    Args:
        phrase: Text to convert to ASCII art
        space_count: Number of background chars defining a space between characters
        text: Character for foreground pixels
        backsplash: Character for background pixels
        font: Font file name
        pattern: Optional pattern for background
        margin: Top/bottom margin in lines
    
    Returns:
        String containing the ASCII art tattoo
    """
    kwargs = {
        "text": text,
        "backsplash": backsplash,
        "font": font,
    }
    
    j = []
    oxo = [[] for _ in range(TEMPLATE_SIZE)]
    
    for x in phrase:
        cmat = yield_char_matrix(x, **kwargs)
        if not j:
            j = concat(oxo, cmat)
        else:
            j = concat(j, cmat, sep=backsplash * space_count)
    
    return tatuar(j, pattern=pattern, backsplash=backsplash, margin=margin)


def print_tattoo(phrase: str, space_count: int = SPACE_MARGIN, **kwargs):
    """
    Generate and print an ASCII art tattoo to stdout.
    
    Args:
        phrase: Text to convert to ASCII art
        space_count: Number of background chars defining a space
        **kwargs: Additional arguments passed to get_tattoo_string
    """
    tatu = get_tattoo_string(phrase, space_count, **kwargs)
    print(tatu)
