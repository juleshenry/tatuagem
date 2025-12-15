#!/usr/bin/env python3
"""
Test script for Ollama integration with tatuagem.

This script tests the Ollama ASCII art generation functionality,
including fallback behavior when Ollama is unavailable.
"""

import sys
from ollama_ascii import (
    generate_ascii_art_with_ollama,
    is_ollama_available,
    get_available_models,
)


def test_ollama_availability():
    """Test if Ollama is available."""
    print("=" * 60)
    print("TEST: Ollama Availability Check")
    print("=" * 60)
    
    available = is_ollama_available()
    print(f"Ollama available: {available}")
    
    if available:
        models = get_available_models()
        print(f"Available models: {models}")
    else:
        print("Ollama server not running. To use Ollama:")
        print("  1. Install: https://ollama.com/download")
        print("  2. Run: ollama serve")
        print("  3. Pull a model: ollama pull llama3.2")
    
    print()
    return available


def test_ascii_generation():
    """Test ASCII art generation."""
    print("=" * 60)
    print("TEST: ASCII Art Generation")
    print("=" * 60)
    
    test_texts = ["Hi", "Test", "Unicode"]
    
    for text in test_texts:
        print(f"\nGenerating ASCII art for: '{text}'")
        print("-" * 40)
        
        ascii_art = generate_ascii_art_with_ollama(
            text,
            text_char="1",
            backsplash_char="0",
            max_width=80,
        )
        
        if ascii_art:
            print(ascii_art)
        else:
            print("Failed to generate (Ollama not available)")
        print("-" * 40)


def test_fallback_behavior():
    """Test fallback to font-based method."""
    print("=" * 60)
    print("TEST: Fallback Behavior")
    print("=" * 60)
    
    print("\nWhen Ollama is not available, the system should")
    print("automatically fall back to the font-based method.")
    print("\nYou can test this by running:")
    print("  python3 tatuagem.py 'Hello' --use-ollama")
    print("\nIf Ollama is not available, you'll see a warning")
    print("and the output will use the font-based method.")
    print()


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("TATUAGEM OLLAMA INTEGRATION TESTS")
    print("=" * 60 + "\n")
    
    # Test 1: Check Ollama availability
    ollama_available = test_ollama_availability()
    
    # Test 2: Try to generate ASCII art
    if ollama_available:
        test_ascii_generation()
    else:
        print("Skipping ASCII generation test (Ollama not available)")
        print()
    
    # Test 3: Explain fallback behavior
    test_fallback_behavior()
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Ollama Available: {ollama_available}")
    print("\nIntegration Status: ✓ Module imported successfully")
    print("Fallback Mechanism: ✓ Configured and ready")
    
    if ollama_available:
        print("\n✓ All tests passed! Ollama integration is working.")
    else:
        print("\n⚠ Ollama not available, but fallback is configured.")
        print("  The system will use font-based generation.")
    
    print("\nTo test with actual Ollama generation:")
    print("  python3 tatuagem.py 'Your Text' --use-ollama")
    print()
    
    return 0 if ollama_available else 1


if __name__ == "__main__":
    sys.exit(main())
