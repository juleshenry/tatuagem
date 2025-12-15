"""
Ollama-based ASCII art generation for tatuagem.

This module provides ASCII art generation using Ollama LLM API,
which supports Unicode characters and arbitrary input text.
Falls back to font-based generation when Ollama is unavailable.
"""

import ollama
from typing import Optional, List


def generate_ascii_art_with_ollama(
    text: str,
    model: str = "llama3.2:latest",
    text_char: str = "1",
    backsplash_char: str = "0",
    max_width: int = 100,
) -> Optional[str]:
    """
    Generate ASCII art using Ollama LLM.
    
    Args:
        text: The text to convert to ASCII art
        model: Ollama model to use (default: llama3.2:latest)
        text_char: Character to use for text (default: "1")
        backsplash_char: Character to use for background (default: "0")
        max_width: Maximum width of ASCII art in characters
        
    Returns:
        ASCII art string or None if generation fails
    """
    try:
        prompt = f"""Generate ASCII art for the text: "{text}"

Requirements:
- Use ONLY '{text_char}' for the text/foreground
- Use ONLY '{backsplash_char}' for the background
- Maximum width: {max_width} characters
- Make it bold and clear
- Do NOT include any explanations, just output the ASCII art
- Start directly with the art, no extra text before or after

Example format (for the text "Hi"):
{backsplash_char * 20}
{text_char}{text_char}{text_char}{backsplash_char}{backsplash_char}{text_char}{text_char}{text_char}
{text_char}{text_char}{text_char}{backsplash_char}{backsplash_char}{text_char}{text_char}{text_char}
{backsplash_char * 20}

Now generate ASCII art for: "{text}"
"""
        
        response = ollama.chat(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an ASCII art generator. You only output ASCII art using the specified characters. You never include explanations or extra text.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        
        # Extract the ASCII art from response
        ascii_art = response["message"]["content"].strip()
        
        # Clean up the response - remove any markdown code blocks if present
        if ascii_art.startswith("```"):
            lines = ascii_art.split("\n")
            # Remove first and last lines if they are code block markers
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            ascii_art = "\n".join(lines).strip()
        
        return ascii_art
        
    except Exception as e:
        print(f"Error generating ASCII art with Ollama: {e}")
        return None


def is_ollama_available(host: str = "http://localhost:11434") -> bool:
    """
    Check if Ollama server is available and responding.
    
    Args:
        host: Ollama server host URL
        
    Returns:
        True if Ollama is available, False otherwise
    """
    try:
        # Try to list available models as a health check
        ollama.list()
        return True
    except Exception:
        return False


def get_available_models() -> List[str]:
    """
    Get list of available Ollama models.
    
    Returns:
        List of model names
    """
    try:
        models = ollama.list()
        return [model["name"] for model in models.get("models", [])]
    except Exception:
        return []


def convert_matrix_to_string(matrix: List[List[str]]) -> str:
    """
    Convert a character matrix to a string representation.
    
    Args:
        matrix: 2D list of characters
        
    Returns:
        String representation with newlines
    """
    return "\n".join(["".join(row) for row in matrix if row])


if __name__ == "__main__":
    # Test the Ollama ASCII art generation
    import sys
    
    if len(sys.argv) > 1:
        test_text = " ".join(sys.argv[1:])
    else:
        test_text = "Hello"
    
    print(f"Testing Ollama ASCII art generation for: {test_text}")
    print("-" * 50)
    
    if is_ollama_available():
        print("Ollama is available!")
        print(f"Available models: {get_available_models()}")
        print("-" * 50)
        
        art = generate_ascii_art_with_ollama(test_text)
        if art:
            print(art)
        else:
            print("Failed to generate ASCII art")
    else:
        print("Ollama is not available. Please start Ollama server first.")
        print("Install: https://ollama.com/download")
        print("Then run: ollama serve")
