# Tatuagem, the boastful code signature suite
![coverage](coverage.svg)

# Basic Example
```python3 tatuagem.py "tatuagem" ```

* defaults defined in tatuagem.py: '1' for text, '0' for background, unicode-arial.ttf for font

# Ollama-Powered ASCII Art (NEW!)
Generate ASCII art using Ollama LLM for better Unicode support and arbitrary text:

```bash
python3 tatuagem.py "Hello World" --use-ollama
```

With custom model:
```bash
python3 tatuagem.py "Unicode 你好" --use-ollama --ollama-model llama3.2:latest
```

**Prerequisites:**
1. Install Ollama: https://ollama.com/download
2. Start Ollama server: `ollama serve`
3. Pull a model: `ollama pull llama3.2`

**Note:** If Ollama is not available, the system automatically falls back to the traditional font-based method.

# Elaborate Syntax Example
```python3 tatuagem.py "L'appel du vide" --font 'unicode-arial.ttf' --backsplash '!' --text '@'```


![alt text](lappel.png)

# Wallpaper: Pattern-Argument Syntax Example
```python3 tatuagem.py "Tatuagem" --pattern '`':,:'' ```

![alt text](tatu.png)

# Recurse your project
```python tatuagem.py "Tatuagem" --pattern '`':,:''  --recurse-path test_tattoo/```

TODO: 

make is so tatoos wont repeat on itself
make it so it wont crash on node package manager
add some sort of checker to tell if the first line is a shebang 