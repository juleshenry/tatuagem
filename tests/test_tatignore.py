"""
Test .tatignore functionality for excluding files from tattooing.
"""

import os
import sys
import tempfile

# Add parent directory to path to import tatuagem modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tatuagem.recurse import (
    load_tatignore_patterns,
    should_ignore,
    apply_tattoo_to_directory,
    get_tattoo,
)


def test_load_tatignore_patterns():
    """Test loading patterns from .tatignore file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create .tatignore file
        tatignore_path = os.path.join(tmpdir, ".tatignore")
        with open(tatignore_path, "w") as f:
            f.write("# This is a comment\n")
            f.write("*.log\n")
            f.write("node_modules/\n")
            f.write("\n")  # Empty line
            f.write("build/**\n")

        patterns = load_tatignore_patterns(tmpdir)
        assert len(patterns) == 3, f"Expected 3 patterns, got {len(patterns)}"
        assert "*.log" in patterns
        assert "node_modules/" in patterns
        assert "build/**" in patterns

        print("✓ test_load_tatignore_patterns passed")


def test_should_ignore_simple_filename():
    """Test ignoring by simple filename."""
    with tempfile.TemporaryDirectory() as tmpdir:
        patterns = ["test.log"]

        # Create test file
        test_file = os.path.join(tmpdir, "test.log")
        open(test_file, "w").close()

        assert should_ignore(test_file, tmpdir, patterns), "Should ignore test.log"

        # File that shouldn't be ignored
        other_file = os.path.join(tmpdir, "test.txt")
        assert not should_ignore(other_file, tmpdir, patterns), (
            "Should not ignore test.txt"
        )

        print("✓ test_should_ignore_simple_filename passed")


def test_should_ignore_wildcard():
    """Test ignoring with wildcard patterns."""
    with tempfile.TemporaryDirectory() as tmpdir:
        patterns = ["*.log", "*.tmp"]

        # Files that should be ignored
        log_file = os.path.join(tmpdir, "error.log")
        tmp_file = os.path.join(tmpdir, "temp.tmp")

        assert should_ignore(log_file, tmpdir, patterns), "Should ignore *.log"
        assert should_ignore(tmp_file, tmpdir, patterns), "Should ignore *.tmp"

        # File that shouldn't be ignored
        py_file = os.path.join(tmpdir, "script.py")
        assert not should_ignore(py_file, tmpdir, patterns), "Should not ignore *.py"

        print("✓ test_should_ignore_wildcard passed")


def test_should_ignore_directory():
    """Test ignoring entire directories."""
    with tempfile.TemporaryDirectory() as tmpdir:
        patterns = ["node_modules", "build"]

        # Create directory structure
        node_modules = os.path.join(tmpdir, "node_modules")
        os.makedirs(node_modules, exist_ok=True)

        # File in ignored directory
        file_in_node_modules = os.path.join(node_modules, "package.js")

        assert should_ignore(file_in_node_modules, tmpdir, patterns), (
            "Should ignore files in node_modules"
        )

        # File in build subdirectory
        build_dir = os.path.join(tmpdir, "src", "build")
        os.makedirs(build_dir, exist_ok=True)
        file_in_build = os.path.join(build_dir, "output.js")

        assert should_ignore(file_in_build, tmpdir, patterns), (
            "Should ignore files in build directory"
        )

        print("✓ test_should_ignore_directory passed")


def test_should_ignore_recursive_pattern():
    """Test ignoring with ** recursive pattern."""
    with tempfile.TemporaryDirectory() as tmpdir:
        patterns = ["build/**"]

        # Create nested structure
        build_dir = os.path.join(tmpdir, "build", "dist", "js")
        os.makedirs(build_dir, exist_ok=True)

        # File deep in build directory
        nested_file = os.path.join(build_dir, "app.js")

        assert should_ignore(nested_file, tmpdir, patterns), (
            "Should ignore files matching build/**"
        )

        # File not in build
        src_file = os.path.join(tmpdir, "src", "app.js")
        assert not should_ignore(src_file, tmpdir, patterns), (
            "Should not ignore files outside build"
        )

        print("✓ test_should_ignore_recursive_pattern passed")


def test_tatignore_integration():
    """Test full integration of .tatignore with tattooing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create .tatignore
        tatignore_path = os.path.join(tmpdir, ".tatignore")
        with open(tatignore_path, "w") as f:
            f.write("*.log\n")
            f.write("ignored.py\n")
            f.write("test_dir/\n")

        # Create files
        included_file = os.path.join(tmpdir, "included.py")
        with open(included_file, "w") as f:
            f.write("print('should be tattooed')\n")

        ignored_file = os.path.join(tmpdir, "ignored.py")
        with open(ignored_file, "w") as f:
            f.write("print('should not be tattooed')\n")

        log_file = os.path.join(tmpdir, "test.log")
        with open(log_file, "w") as f:
            f.write("log content\n")

        # Create ignored directory with file
        test_dir = os.path.join(tmpdir, "test_dir")
        os.makedirs(test_dir, exist_ok=True)
        dir_file = os.path.join(test_dir, "file.py")
        with open(dir_file, "w") as f:
            f.write("print('in ignored dir')\n")

        # Apply tattoo
        tattoo = get_tattoo("test")
        apply_tattoo_to_directory(tmpdir, tattoo)

        # Check that included file was tattooed
        with open(included_file, "r") as f:
            included_content = f.read()
        assert '"""' in included_content, "Included file should be tattooed"
        assert "should be tattooed" in included_content, (
            "Original content should remain"
        )

        # Check that ignored files were NOT tattooed
        with open(ignored_file, "r") as f:
            ignored_content = f.read()
        assert '"""' not in ignored_content, "Ignored file should not be tattooed"
        assert ignored_content == "print('should not be tattooed')\n", (
            "Ignored file should remain unchanged"
        )

        with open(dir_file, "r") as f:
            dir_content = f.read()
        assert '"""' not in dir_content, "File in ignored dir should not be tattooed"

        print("✓ test_tatignore_integration passed")


def test_tatignore_no_file():
    """Test that tattooing works normally when .tatignore doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create file without .tatignore
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write("print('hello')\n")

        # Apply tattoo
        tattoo = get_tattoo("test")
        apply_tattoo_to_directory(tmpdir, tattoo)

        # Check that file was tattooed
        with open(test_file, "r") as f:
            content = f.read()
        assert '"""' in content, "File should be tattooed when no .tatignore exists"

        print("✓ test_tatignore_no_file passed")


def test_tatignore_empty_file():
    """Test that empty .tatignore file doesn't affect tattooing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create empty .tatignore
        tatignore_path = os.path.join(tmpdir, ".tatignore")
        open(tatignore_path, "w").close()

        # Create file
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write("print('hello')\n")

        # Apply tattoo
        tattoo = get_tattoo("test")
        apply_tattoo_to_directory(tmpdir, tattoo)

        # Check that file was tattooed
        with open(test_file, "r") as f:
            content = f.read()
        assert '"""' in content, "File should be tattooed with empty .tatignore"

        print("✓ test_tatignore_empty_file passed")


if __name__ == "__main__":
    print("Running .tatignore tests...")
    print()

    test_load_tatignore_patterns()
    test_should_ignore_simple_filename()
    test_should_ignore_wildcard()
    test_should_ignore_directory()
    test_should_ignore_recursive_pattern()
    test_tatignore_integration()
    test_tatignore_no_file()
    test_tatignore_empty_file()

    print()
    print("All .tatignore tests passed! ✓")
