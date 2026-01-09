"""
Test Ollama Studio feature without requiring Ollama installation.
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path to import tatuagem modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tatuagem import generate_ascii_art_from_prompt, get_user_confirmation, ollama_studio


class TestOllamaStudio(unittest.TestCase):
    """Test cases for Ollama Studio feature."""
    
    @patch('tatuagem.subprocess.run')
    def test_generate_ascii_art_from_prompt_success(self, mock_run):
        """Test successful ASCII art generation."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "  /\\_/\\\n ( o.o )\n  > ^ <\n"
        mock_run.return_value = mock_result
        
        result = generate_ascii_art_from_prompt("cat")
        
        self.assertIsNotNone(result)
        self.assertIn("o.o", result)
        mock_run.assert_called_once()
        
    @patch('tatuagem.subprocess.run')
    def test_generate_ascii_art_from_prompt_failure(self, mock_run):
        """Test ASCII art generation failure."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Error"
        mock_run.return_value = mock_result
        
        result = generate_ascii_art_from_prompt("test")
        
        self.assertIsNone(result)
        
    @patch('tatuagem.subprocess.run')
    def test_generate_ascii_art_ollama_not_found(self, mock_run):
        """Test when Ollama is not installed."""
        mock_run.side_effect = FileNotFoundError()
        
        result = generate_ascii_art_from_prompt("test")
        
        self.assertIsNone(result)
        
    @patch('builtins.input', return_value='y')
    def test_get_user_confirmation_valid(self, mock_input):
        """Test user confirmation with valid input."""
        result = get_user_confirmation("Test?", {"y": True, "n": False})
        
        self.assertEqual(result, "y")
        
    @patch('builtins.input', side_effect=['invalid', 'y'])
    def test_get_user_confirmation_retry(self, mock_input):
        """Test user confirmation with retry after invalid input."""
        result = get_user_confirmation("Test?", {"y": True, "n": False})
        
        self.assertEqual(result, "y")
        self.assertEqual(mock_input.call_count, 2)
        
    @patch('tatuagem.subprocess.run')
    @patch('builtins.input', side_effect=['y', 'n'])  # Confirm tattoo, no header/footer
    def test_ollama_studio_basic_flow(self, mock_input, mock_run):
        """Test basic Ollama Studio workflow."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "ASCII ART"
        mock_run.return_value = mock_result
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            ollama_studio("test prompt", text='1', backsplash='0', 
                         font='unicode-arial.ttf', pattern=None, margin=3)
        finally:
            sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("Ollama Tattoo Studio", output)
        self.assertIn("ASCII ART", output)
        self.assertIn("FINAL TATTOO", output)


def test_functions_imported():
    """Test that all new functions can be imported."""
    from tatuagem import generate_ascii_art_from_prompt, get_user_confirmation, ollama_studio
    print("✓ All Ollama Studio functions imported successfully")


if __name__ == "__main__":
    print("Running Ollama Studio tests...")
    print()
    
    # Run basic import test
    test_functions_imported()
    
    # Run unit tests
    unittest.main(verbosity=2)
