#!/bin/bash
# Demo script for Tatuagem ASCII art generation

echo "=========================================="
echo "TATUAGEM ASCII ART GENERATOR - DEMO"
echo "=========================================="
echo ""

echo "1. Basic Example (Default Settings)"
echo "-----------------------------------"
python3 tatuagem.py "Hi"
echo ""

echo "2. Custom Characters"
echo "-----------------------------------"
python3 tatuagem.py "OK" --text '@' --backsplash '.'
echo ""

echo "3. With Pattern"
echo "-----------------------------------"
python3 tatuagem.py "Test" --pattern '.,;:'
echo ""

echo "4. Ollama Mode (will use font-based if Ollama unavailable)"
echo "-----------------------------------"
python3 tatuagem.py "Unicode" --use-ollama
echo ""

echo "=========================================="
echo "DEMO COMPLETE"
echo "=========================================="
echo ""
echo "To use Ollama for better Unicode support:"
echo "  1. Install Ollama: https://ollama.com/download"
echo "  2. Start server: ollama serve"
echo "  3. Pull model: ollama pull llama3.2"
echo "  4. Run: python3 tatuagem.py 'Your Text' --use-ollama"
echo ""
