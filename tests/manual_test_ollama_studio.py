#!/usr/bin/env python3
"""
Comprehensive manual test script for the Ollama Studio feature.
This script simulates user interactions to test the complete workflow.
"""
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tatuagem import ollama_studio


def test_scenario_1_basic_no_addons():
    """Test: Generate tattoo and choose no addons."""
    print("\n" + "="*70)
    print("SCENARIO 1: Basic tattoo with no header/footer")
    print("="*70)
    
    # Mock subprocess and user inputs
    mock_subprocess_result = MagicMock()
    mock_subprocess_result.returncode = 0
    mock_subprocess_result.stdout = "  /\\_/\\\n ( o.o )\n  > ^ <\n"
    
    with patch('tatuagem.subprocess.run', return_value=mock_subprocess_result):
        with patch('builtins.input', side_effect=['y', 'n']):  # Confirm tattoo, no addons
            # Capture output
            captured_output = StringIO()
            sys.stdout = captured_output
            
            try:
                ollama_studio("A cute cat", text='1', backsplash='0', 
                             font='unicode-arial.ttf', pattern=None, margin=3)
            finally:
                sys.stdout = sys.__stdout__
            
            output = captured_output.getvalue()
            
    # Verify output contains expected elements
    assert "Ollama Tattoo Studio" in output
    assert "A cute cat" in output
    assert "o.o" in output
    assert "FINAL TATTOO" in output
    print("✓ Scenario 1 passed")


def test_scenario_2_with_header():
    """Test: Generate tattoo with header only."""
    print("\n" + "="*70)
    print("SCENARIO 2: Tattoo with header only")
    print("="*70)
    
    # Mock subprocess
    mock_subprocess_result = MagicMock()
    mock_subprocess_result.returncode = 0
    mock_subprocess_result.stdout = "ASCII ART HERE"
    
    with patch('tatuagem.subprocess.run', return_value=mock_subprocess_result):
        # Confirm tattoo, choose header only, enter "TEST", confirm header
        with patch('builtins.input', side_effect=['y', 'h', 'TEST', 'y']):
            captured_output = StringIO()
            sys.stdout = captured_output
            
            try:
                ollama_studio("Test prompt", text='1', backsplash='0', 
                             font='unicode-arial.ttf', pattern=None, margin=3)
            finally:
                sys.stdout = sys.__stdout__
            
            output = captured_output.getvalue()
    
    assert "Header Preview:" in output
    assert "FINAL TATTOO" in output
    print("✓ Scenario 2 passed")


def test_scenario_3_with_both():
    """Test: Generate tattoo with both header and footer."""
    print("\n" + "="*70)
    print("SCENARIO 3: Tattoo with both header and footer")
    print("="*70)
    
    # Mock subprocess
    mock_subprocess_result = MagicMock()
    mock_subprocess_result.returncode = 0
    mock_subprocess_result.stdout = "MAIN ASCII ART"
    
    with patch('tatuagem.subprocess.run', return_value=mock_subprocess_result):
        # Confirm tattoo, choose both, enter header "HEADER", confirm, enter footer "FOOTER", confirm
        with patch('builtins.input', side_effect=['y', 'b', 'HEADER', 'y', 'FOOTER', 'y']):
            captured_output = StringIO()
            sys.stdout = captured_output
            
            try:
                ollama_studio("Test", text='1', backsplash='0', 
                             font='unicode-arial.ttf', pattern=None, margin=3)
            finally:
                sys.stdout = sys.__stdout__
            
            output = captured_output.getvalue()
    
    assert "Header Preview:" in output
    assert "Footer Preview:" in output
    assert "FINAL TATTOO" in output
    print("✓ Scenario 3 passed")


def test_scenario_4_regenerate():
    """Test: Regenerate tattoo before proceeding."""
    print("\n" + "="*70)
    print("SCENARIO 4: Regenerate tattoo")
    print("="*70)
    
    # Mock subprocess with two different outputs
    call_count = [0]
    
    def mock_run(*args, **kwargs):
        result = MagicMock()
        result.returncode = 0
        call_count[0] += 1
        if call_count[0] == 1:
            result.stdout = "FIRST ATTEMPT"
        else:
            result.stdout = "SECOND ATTEMPT"
        return result
    
    with patch('tatuagem.subprocess.run', side_effect=mock_run):
        # Reject first, accept second, no addons
        with patch('builtins.input', side_effect=['n', 'y', 'n']):
            captured_output = StringIO()
            sys.stdout = captured_output
            
            try:
                ollama_studio("Test", text='1', backsplash='0', 
                             font='unicode-arial.ttf', pattern=None, margin=3)
            finally:
                sys.stdout = sys.__stdout__
            
            output = captured_output.getvalue()
    
    assert "Regenerating..." in output
    assert "SECOND ATTEMPT" in output
    assert call_count[0] == 2  # Should have called Ollama twice
    print("✓ Scenario 4 passed")


def test_scenario_5_redo_header():
    """Test: Redo header before proceeding."""
    print("\n" + "="*70)
    print("SCENARIO 5: Redo header")
    print("="*70)
    
    # Mock subprocess
    mock_subprocess_result = MagicMock()
    mock_subprocess_result.returncode = 0
    mock_subprocess_result.stdout = "ASCII ART"
    
    with patch('tatuagem.subprocess.run', return_value=mock_subprocess_result):
        # Confirm tattoo, choose header, enter "BAD", reject, enter "GOOD", confirm
        with patch('builtins.input', side_effect=['y', 'h', 'BAD', 'n', 'GOOD', 'y']):
            captured_output = StringIO()
            sys.stdout = captured_output
            
            try:
                ollama_studio("Test", text='1', backsplash='0', 
                             font='unicode-arial.ttf', pattern=None, margin=3)
            finally:
                sys.stdout = sys.__stdout__
            
            output = captured_output.getvalue()
    
    assert "Let's redo the header..." in output
    print("✓ Scenario 5 passed")


if __name__ == "__main__":
    print("="*70)
    print("RUNNING COMPREHENSIVE MANUAL TESTS FOR OLLAMA STUDIO")
    print("="*70)
    
    test_scenario_1_basic_no_addons()
    test_scenario_2_with_header()
    test_scenario_3_with_both()
    test_scenario_4_regenerate()
    test_scenario_5_redo_header()
    
    print("\n" + "="*70)
    print("ALL MANUAL TESTS PASSED! ✓")
    print("="*70)
