"""
Test the --overwrite flag functionality.
"""

import os
import sys
import tempfile
import shutil

# Add parent directory to path to import tatuagem modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tatuagem.recurse import apply_tattoo_to_directory, get_tattoo


def test_overwrite_flag_false_skips_tattooed_files():
    """Test that overwrite=False skips files that are already tattooed."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a Python file
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write("print('Hello World')\n")

        # Tattoo the file first time
        tattoo1 = get_tattoo("first")
        apply_tattoo_to_directory(tmpdir, tattoo1, overwrite=False)

        # Read the result
        with open(test_file, "r") as f:
            content_after_first = f.read()

        # Verify it was tattooed
        assert '"""' in content_after_first, "File should have Python comment delimiter"
        assert "print('Hello World')" in content_after_first, (
            "Original code should be in file"
        )

        # Try to tattoo again with different text and overwrite=False
        tattoo2 = get_tattoo("second")
        apply_tattoo_to_directory(tmpdir, tattoo2, overwrite=False)

        # Read the result again
        with open(test_file, "r") as f:
            content_after_second = f.read()

        # Content should be the same (not overwritten)
        assert content_after_first == content_after_second, (
            "File should not be overwritten when overwrite=False"
        )

        print("✓ test_overwrite_flag_false_skips_tattooed_files passed")


def test_overwrite_flag_true_replaces_tattoos():
    """Test that overwrite=True replaces existing tattoos."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a Python file
        test_file = os.path.join(tmpdir, "test.py")
        original_code = "print('Hello World')\n"
        with open(test_file, "w") as f:
            f.write(original_code)

        # Tattoo the file first time
        tattoo1 = get_tattoo("first")
        apply_tattoo_to_directory(tmpdir, tattoo1, overwrite=False)

        # Read the result
        with open(test_file, "r") as f:
            content_after_first = f.read()

        # Verify it was tattooed
        assert '"""' in content_after_first, "File should have comment delimiter"
        assert original_code in content_after_first, "Original code should be preserved"

        # Tattoo again with different text and overwrite=True
        tattoo2 = get_tattoo("second")
        apply_tattoo_to_directory(tmpdir, tattoo2, overwrite=True)

        # Read the result again
        with open(test_file, "r") as f:
            content_after_second = f.read()

        # Content should be different (overwritten)
        assert content_after_first != content_after_second, (
            "File should be overwritten when overwrite=True"
        )
        assert original_code in content_after_second, (
            "Original code should still be preserved"
        )

        print("✓ test_overwrite_flag_true_replaces_tattoos passed")


def test_overwrite_preserves_shebang():
    """Test that overwrite preserves shebang when replacing tattoos."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a Python file with shebang
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write("#!/usr/bin/env python3\nprint('Hello World')\n")

        # Tattoo the file first time
        tattoo1 = get_tattoo("first")
        apply_tattoo_to_directory(tmpdir, tattoo1, overwrite=False)

        # Read the result
        with open(test_file, "r") as f:
            content = f.read()

        lines = content.split("\n")
        assert lines[0] == "#!/usr/bin/env python3", "Shebang should be preserved"

        # Tattoo again with overwrite=True
        tattoo2 = get_tattoo("second")
        apply_tattoo_to_directory(tmpdir, tattoo2, overwrite=True)

        # Read the result again
        with open(test_file, "r") as f:
            content = f.read()

        lines = content.split("\n")
        assert lines[0] == "#!/usr/bin/env python3", (
            "Shebang should still be preserved after overwrite"
        )

        print("✓ test_overwrite_preserves_shebang passed")


def test_overwrite_on_fresh_file():
    """Test that overwrite=True works on files that haven't been tattooed yet."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a Python file
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write("print('Hello World')\n")

        # Tattoo with overwrite=True (even though file is not tattooed)
        tattoo = get_tattoo("test")
        apply_tattoo_to_directory(tmpdir, tattoo, overwrite=True)

        # Read the result
        with open(test_file, "r") as f:
            content = f.read()

        # Verify it was tattooed
        assert '"""' in content, "File should have comment delimiter"
        assert "print('Hello World')" in content, "Original code should be preserved"

        print("✓ test_overwrite_on_fresh_file passed")


def test_default_behavior_is_no_overwrite():
    """Test that the default behavior (no overwrite parameter) doesn't overwrite."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a Python file
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write("print('Hello World')\n")

        # Tattoo the file first time (with default parameter)
        tattoo1 = get_tattoo("first")
        apply_tattoo_to_directory(tmpdir, tattoo1)

        # Read the result
        with open(test_file, "r") as f:
            content_after_first = f.read()

        # Try to tattoo again with default parameter
        tattoo2 = get_tattoo("second")
        apply_tattoo_to_directory(tmpdir, tattoo2)

        # Read the result again
        with open(test_file, "r") as f:
            content_after_second = f.read()

        # Content should be the same (not overwritten by default)
        assert content_after_first == content_after_second, (
            "Default behavior should not overwrite"
        )

        print("✓ test_default_behavior_is_no_overwrite passed")


if __name__ == "__main__":
    print("Running overwrite flag tests...")
    print()

    test_overwrite_flag_false_skips_tattooed_files()
    test_overwrite_flag_true_replaces_tattoos()
    test_overwrite_preserves_shebang()
    test_overwrite_on_fresh_file()
    test_default_behavior_is_no_overwrite()

    print()
    print("All overwrite tests passed! ✓")
