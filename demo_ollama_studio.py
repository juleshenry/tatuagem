#!/usr/bin/env python3
"""
Demo script showing how to use the Ollama Studio feature.

This script demonstrates the --ollama-studio feature without requiring
actual Ollama installation by showing the command and expected behavior.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def print_demo():
    """Print a demonstration of the Ollama Studio feature."""
    print("="*70)
    print("OLLAMA TATTOO STUDIO - FEATURE DEMONSTRATION")
    print("="*70)
    print()
    
    print("To use the Ollama Studio feature, run:")
    print('  python3 tatuagem.py --ollama-studio "Your prompt here"')
    print()
    
    print("Example:")
    print('  python3 tatuagem.py --ollama-studio "A cute cat"')
    print()
    
    print("="*70)
    print("WORKFLOW")
    print("="*70)
    print()
    
    print("Step 1: Generate ASCII Art from Prompt")
    print("  - The system will use Ollama to generate ASCII art based on your prompt")
    print("  - You'll see the generated art")
    print("  - You can choose to proceed (Y) or regenerate (n)")
    print()
    
    print("Step 2: Choose Header/Footer Options")
    print("  - h: Add only a header")
    print("  - f: Add only a footer")
    print("  - b: Add both header and footer")
    print("  - n: Add neither (use only the generated art)")
    print()
    
    print("Step 3: Header (if selected)")
    print("  - Enter text for the header")
    print("  - Preview the header in Tatuagem ASCII art style")
    print("  - Confirm or redo")
    print()
    
    print("Step 4: Footer (if selected)")
    print("  - Enter text for the footer")
    print("  - Preview the footer in Tatuagem ASCII art style")
    print("  - Confirm or redo")
    print()
    
    print("Final Output:")
    print("  - See your complete tattoo with all selected elements")
    print()
    
    print("="*70)
    print("CUSTOMIZATION OPTIONS")
    print("="*70)
    print()
    
    print("You can combine --ollama-studio with other options:")
    print('  --text "X"         : Character for drawing text (default: "1")')
    print('  --backsplash "."   : Character for background (default: "0")')
    print('  --font "arial.ttf" : Font to use (default: "unicode-arial.ttf")')
    print('  --pattern "~`"     : Pattern for background')
    print('  --margin 5         : Top/bottom margin (default: 3)')
    print()
    
    print("Example with customization:")
    print('  python3 tatuagem.py --ollama-studio "A dragon" --text "@" --backsplash "." --pattern "~`"')
    print()
    
    print("="*70)
    print("REQUIREMENTS")
    print("="*70)
    print()
    print("- Ollama must be installed and running")
    print("- The llama3 model must be available")
    print("- Install Ollama from: https://ollama.ai/")
    print()
    
    print("="*70)


def show_simulated_example():
    """Show a simulated example of the workflow."""
    print()
    print("="*70)
    print("SIMULATED EXAMPLE WORKFLOW")
    print("="*70)
    print()
    
    print("$ python3 tatuagem.py --ollama-studio \"A cat\"")
    print()
    print("=== Ollama Tattoo Studio ===")
    print()
    print("Generating ASCII art from prompt: 'A cat'")
    print()
    print("Generating tattoo...")
    print()
    print("="*60)
    print("Generated Tattoo:")
    print("="*60)
    print("  /\\_/\\  ")
    print(" ( o.o ) ")
    print("  > ^ <  ")
    print("="*60)
    print()
    print("Proceed with this tattoo? (Y/n): Y")
    print()
    print("Would you like to add headers or footers?")
    print("Choose (h=header, f=footer, b=both, n=neither): b")
    print()
    print("Enter header text: MEOW")
    print()
    print("="*60)
    print("Header Preview:")
    print("="*60)
    print("1111   111 11111111  111111  1   1   1")
    print("1   1 1   1 1       1    1  1   1   1")
    print("1   1 1111  1111    1    1  1 1 1 1 1")
    print("1   1 1     1       1    1  1   1   1")
    print("1111  11111 11111111 111111  1   1   1")
    print("="*60)
    print()
    print("Proceed with this header? (Y/n): Y")
    print()
    print("Enter footer text: CAT")
    print()
    print("="*60)
    print("Footer Preview:")
    print("="*60)
    print(" 111   11   1111111")
    print("1   1 1  1     1   ")
    print("1     1111     1   ")
    print("1   1 1  1     1   ")
    print(" 111  1  1     1   ")
    print("="*60)
    print()
    print("Proceed with this footer? (Y/n): Y")
    print()
    print("="*60)
    print("FINAL TATTOO")
    print("="*60)
    print()
    print("1111   111 11111111  111111  1   1   1")
    print("1   1 1   1 1       1    1  1   1   1")
    print("1   1 1111  1111    1    1  1 1 1 1 1")
    print("1   1 1     1       1    1  1   1   1")
    print("1111  11111 11111111 111111  1   1   1")
    print()
    print("  /\\_/\\  ")
    print(" ( o.o ) ")
    print("  > ^ <  ")
    print()
    print(" 111   11   1111111")
    print("1   1 1  1     1   ")
    print("1     1111     1   ")
    print("1   1 1  1     1   ")
    print(" 111  1  1     1   ")
    print()
    print("="*60)
    print()


if __name__ == "__main__":
    print_demo()
    show_simulated_example()
    
    print("="*70)
    print("To see the feature in action, ensure Ollama is installed and run:")
    print('  python3 tatuagem.py --ollama-studio "Your creative prompt"')
    print("="*70)
