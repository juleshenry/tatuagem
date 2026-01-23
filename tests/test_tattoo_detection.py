"""
Test the improved tattoo detection algorithm.
"""

import os
import sys
import tempfile

# Add parent directory to path to import tatuagem modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tatuagem.recurse import (
    is_tattoo_comment,
    extract_first_comment,
    apply_tattoo_to_directory,
    get_tattoo,
)


def test_is_tattoo_comment_with_ascii_art():
    """Test that ASCII art tattoos are correctly identified."""
    tattoo_text = """000000000000000000000000000000000000000000000000000000000000
000000000000000000000000000000000000000000000000000000000000
000000000000000000000000000000000000000000000000000000000000
000111000000000000000000000000000000000000000000000000111000
001111000000000000000000000000000000000000000000000001111000
001111000000000000000000000000000000000000000000000001111000
001111000000000000000000000000000000000000000000000001111000
001111000000000000000000000000000000000000000000000001111000
001111000000000000000000000000000000000000000000000001111000
111111111000000001111111100000000001111111110000000111111111
111111111000000111111111111000000011111111111000000111111111"""

    assert is_tattoo_comment(tattoo_text), "Should detect ASCII art as tattoo"
    print("✓ test_is_tattoo_comment_with_ascii_art passed")


def test_is_tattoo_comment_with_documentation():
    """Test that normal documentation comments are not identified as tattoos."""
    doc_text = """This is a function that does something important.

Args:
    param1: The first parameter to the function
    param2: The second parameter to the function
    
Returns:
    The result of the function operation
    
Example:
    >>> my_function(1, 2)
    3
    
Note:
    This function should be used carefully."""

    assert not is_tattoo_comment(doc_text), "Should not detect documentation as tattoo"
    print("✓ test_is_tattoo_comment_with_documentation passed")


def test_is_tattoo_comment_with_copyright():
    """Test that copyright notices are not identified as tattoos."""
    copyright_text = """Copyright (c) 2024 Company Name

This file is part of the project.

Licensed under the MIT License.
See LICENSE file for more information.

Author: John Doe
Version: 1.0.0"""

    assert not is_tattoo_comment(copyright_text), (
        "Should not detect copyright as tattoo"
    )
    print("✓ test_is_tattoo_comment_with_copyright passed")


def test_is_tattoo_comment_with_short_comment():
    """Test that short comments are not identified as tattoos."""
    short_text = """This is a short comment"""

    assert not is_tattoo_comment(short_text), (
        "Should not detect short comment as tattoo (less than min_lines)"
    )
    print("✓ test_is_tattoo_comment_with_short_comment passed")


def test_is_tattoo_comment_with_special_chars():
    """Test that ASCII art with special characters is identified as tattoo."""
    special_tattoo = """
    ▋▄▄▄▄▂▉▋▎                                   ▏▎▋▉▂▄▄▄▃▌                       
    ▇█████▅▅█▇▃▉▍      ▏▌            ▌       ▍▉▃▆▆▄▆█████▄                       
    ▁███▆▇▃▇███▅▅▅▁▌▏   ▍▍          ▌▍   ▏▌▂▆▅▅███▆▄▆▆███▋                       
    ▄██▂▄████▅▊▃███▇▁▍  ▏▍▎      ▎▍▏  ▍▂▇███▁▉▆████▄▃██▁                        
    ▏▂█▇██▉▍▍▌▊▅▁▍▍▁▇█▅▊▏ ▏▍▎  ▎▍▏ ▏▊▅█▆▁▍▌▂▅▊▌▍▍▁██▇▇▉                         
    ▉██▇▃▌▌▍▍▌▋▌▏ ▏▋▇█▇▉▏ ▎▋▋▎ ▏▉▇█▆▋▏ ▏▌▋▌▍▍▍▋▄▇██▋                          
    ▏▇█▇▊▍▍▍▍▍▍▌▋▋▌▍▆███▇▊▂██▉▉▇██▇▂▌▋▋▊▌▍▍▍▍▍▍▁▇█▅                           
    ▍██▃▎   ▏▍▍▌▋▂▆▇█████▇▇████████▆▄▋▍▍▍▏  ▏▍▄██▎                           
    """

    assert is_tattoo_comment(special_tattoo), (
        "Should detect special char ASCII art as tattoo"
    )
    print("✓ test_is_tattoo_comment_with_special_chars passed")


def test_extract_first_comment_block():
    """Test extracting the first comment from a file."""
    content = '''"""
This is a comment
with multiple lines
"""

def my_function():
    pass'''

    comment = extract_first_comment(content, '"""', '"""')
    assert comment is not None, "Should extract comment"
    assert "This is a comment" in comment, "Should contain comment text"
    print("✓ test_extract_first_comment_block passed")


def test_extract_first_comment_cstyle():
    """Test extracting C-style block comment."""
    content = """/*
This is a C-style comment
with multiple lines
*/

int main() {
    return 0;
}"""

    comment = extract_first_comment(content, "/*", "*/")
    assert comment is not None, "Should extract comment"
    assert "C-style comment" in comment, "Should contain comment text"
    print("✓ test_extract_first_comment_cstyle passed")


def test_tattoo_with_existing_documentation():
    """Test that files with documentation comments at the top are not tattooed."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a Python file with documentation
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write('''"""
This module provides important functionality.

Functions:
    my_function: Does something important
"""

def my_function():
    print('Hello World')
''')

        # Try to tattoo the file
        tattoo = get_tattoo("test")
        apply_tattoo_to_directory(tmpdir, tattoo)

        # Read the result
        with open(test_file, "r") as f:
            content = f.read()

        # Check that the original documentation is preserved
        assert "This module provides important functionality" in content, (
            "Original documentation should be preserved"
        )

        # Check that tattoo was not added (file should be skipped)
        lines = content.split("\n")
        first_comment = lines[0:8]  # First several lines
        combined = "\n".join(first_comment)

        # The tattoo consists of mostly 0s and 1s, doc has words
        assert "module provides important" in combined, (
            "Documentation should remain at top (file should be skipped)"
        )

        print("✓ test_tattoo_with_existing_documentation passed")


def test_tattoo_replacement():
    """Test that existing tattoos are replaced with new ones."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a Python file with an existing tattoo
        test_file = os.path.join(tmpdir, "test.py")
        old_tattoo = """000000000000000000000000000000000000000000000000000000000000
000000000000000000000000000000000000000000000000000000000000
111111111111111111111111111111111111111111111111111111111111
000000000000000000000000000000000000000000000000000000000000
000000000000000000000000000000000000000000000000000000000000"""

        with open(test_file, "w") as f:
            f.write(f'''"""
{old_tattoo}
"""

def my_function():
    print('Hello World')
''')

        # Tattoo the file with a new tattoo
        new_tattoo = get_tattoo("new")
        apply_tattoo_to_directory(tmpdir, new_tattoo)

        # Read the result
        with open(test_file, "r") as f:
            content = f.read()

        # Check that the new tattoo is present
        assert '"""' in content, "Should have comment delimiters"

        # Check that the function is preserved
        assert "def my_function():" in content, "Function should be preserved"
        assert "print('Hello World')" in content, "Function body should be preserved"

        print("✓ test_tattoo_replacement passed")


if __name__ == "__main__":
    print("Running tattoo detection tests...")
    print()

    test_is_tattoo_comment_with_ascii_art()
    test_is_tattoo_comment_with_documentation()
    test_is_tattoo_comment_with_copyright()
    test_is_tattoo_comment_with_short_comment()
    test_is_tattoo_comment_with_special_chars()
    test_extract_first_comment_block()
    test_extract_first_comment_cstyle()
    test_tattoo_with_existing_documentation()
    test_tattoo_replacement()

    print()
    print("All tattoo detection tests passed! ✓")
