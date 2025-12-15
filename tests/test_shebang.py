"""
Test shebang detection and preservation when tattooing files.
"""
import os
import sys
import tempfile
import shutil
import subprocess

# Add parent directory to path to import tatuagem modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recurse import has_shebang, get_shebang, apply_tattoo_to_directory, get_tattoo


def test_has_shebang():
    """Test shebang detection."""
    # Test with shebang
    content_with_shebang = "#!/usr/bin/env python3\nprint('hello')"
    assert has_shebang(content_with_shebang), "Should detect shebang"
    
    # Test without shebang
    content_without_shebang = "print('hello')"
    assert not has_shebang(content_without_shebang), "Should not detect shebang"
    
    # Test with empty content
    assert not has_shebang(""), "Should not detect shebang in empty content"
    
    print("✓ test_has_shebang passed")


def test_get_shebang():
    """Test shebang extraction."""
    # Test with shebang
    content = "#!/usr/bin/env python3\nprint('hello')"
    shebang = get_shebang(content)
    assert shebang == "#!/usr/bin/env python3", f"Expected '#!/usr/bin/env python3', got '{shebang}'"
    
    # Test without shebang
    content_without = "print('hello')"
    assert get_shebang(content_without) is None, "Should return None for content without shebang"
    
    print("✓ test_get_shebang passed")


def test_tattoo_python_with_shebang():
    """Test that Python files with shebang preserve the shebang after tattooing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a Python file with shebang
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write("#!/usr/bin/env python3\nprint('Hello World')\n")
        
        # Tattoo the file
        tattoo = get_tattoo("test")
        apply_tattoo_to_directory(tmpdir, tattoo)
        
        # Read the result
        with open(test_file, "r") as f:
            content = f.read()
        
        # Check that shebang is preserved at line 1
        lines = content.split('\n')
        assert lines[0] == "#!/usr/bin/env python3", f"Shebang should be first line, got: {lines[0]}"
        
        # Check that file still runs
        result = subprocess.run([sys.executable, test_file], capture_output=True, text=True)
        assert result.returncode == 0, f"File should run successfully, got: {result.stderr}"
        assert "Hello World" in result.stdout, f"Expected 'Hello World' in output, got: {result.stdout}"
        
        print("✓ test_tattoo_python_with_shebang passed")


def test_tattoo_npm_project():
    """Test that npm project with shebang works after tattooing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create package.json
        package_json = os.path.join(tmpdir, "package.json")
        with open(package_json, "w") as f:
            f.write("""{
  "name": "test-npm",
  "version": "1.0.0",
  "scripts": {
    "test": "node index.js"
  }
}""")
        
        # Create index.js with shebang
        index_js = os.path.join(tmpdir, "index.js")
        with open(index_js, "w") as f:
            f.write("#!/usr/bin/env node\nconsole.log('Hello from npm!');\n")
        
        # Tattoo the project
        tattoo = get_tattoo("npm test")
        apply_tattoo_to_directory(tmpdir, tattoo)
        
        # Read the result
        with open(index_js, "r") as f:
            content = f.read()
        
        # Check that shebang is preserved at line 1
        lines = content.split('\n')
        assert lines[0] == "#!/usr/bin/env node", f"Shebang should be first line, got: {lines[0]}"
        
        # Run npm test
        result = subprocess.run(
            ["npm", "test"], 
            cwd=tmpdir, 
            capture_output=True, 
            text=True
        )
        assert result.returncode == 0, f"npm test should succeed, got: {result.stderr}"
        assert "Hello from npm!" in result.stdout, f"Expected 'Hello from npm!' in output, got: {result.stdout}"
        
        print("✓ test_tattoo_npm_project passed")


def test_tattoo_file_without_shebang():
    """Test that files without shebang still work correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a Python file without shebang
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write("print('Hello World')\n")
        
        # Tattoo the file
        tattoo = get_tattoo("test")
        apply_tattoo_to_directory(tmpdir, tattoo)
        
        # Read the result
        with open(test_file, "r") as f:
            content = f.read()
        
        # Check that first line is comment start (no shebang)
        lines = content.split('\n')
        assert lines[0] == '"""', f"First line should be comment delimiter, got: {lines[0]}"
        
        # Check that file still runs
        result = subprocess.run([sys.executable, test_file], capture_output=True, text=True)
        assert result.returncode == 0, f"File should run successfully, got: {result.stderr}"
        assert "Hello World" in result.stdout, f"Expected 'Hello World' in output, got: {result.stdout}"
        
        print("✓ test_tattoo_file_without_shebang passed")


def test_tattoo_file_with_only_shebang():
    """Test edge case of file with only a shebang line."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a file with only shebang
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write("#!/usr/bin/env python3")
        
        # Tattoo the file
        tattoo = get_tattoo("test")
        apply_tattoo_to_directory(tmpdir, tattoo)
        
        # Read the result
        with open(test_file, "r") as f:
            content = f.read()
        
        # Check that shebang is preserved at line 1
        lines = content.split('\n')
        assert lines[0] == "#!/usr/bin/env python3", f"Shebang should be first line, got: {lines[0]}"
        
        print("✓ test_tattoo_file_with_only_shebang passed")


if __name__ == "__main__":
    print("Running shebang detection tests...")
    print()
    
    test_has_shebang()
    test_get_shebang()
    test_tattoo_python_with_shebang()
    test_tattoo_file_without_shebang()
    test_tattoo_file_with_only_shebang()
    test_tattoo_npm_project()
    
    print()
    print("All tests passed! ✓")
