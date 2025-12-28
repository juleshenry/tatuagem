# Tatuagem, the boastful code signature suite
![coverage](coverage.svg)

# Basic Example
```python3 tatuagem.py "tatuagem" ```

* defaults defined in tatuagem.py: '1' for text, '0' for background, unicode-arial.ttf for font 

# Elaborate Syntax Example
```python3 tatuagem.py "L'appel du vide" --font 'unicode-arial.ttf' --backsplash '!' --text '@'```


![alt text](lappel.png)

# Wallpaper: Pattern-Argument Syntax Example
```python3 tatuagem.py "Tatuagem" --pattern '`':,:'' ```

![alt text](tatu.png)

# Recurse your project
```python tatuagem.py "Tatuagem" --pattern '`':,:''  --recurse-path test_tattoo/```

## Features

✓ Shebang detection and preservation - files with `#!/...` shebangs keep them at the top
✓ Safe for npm projects - tattooed npm projects continue to work after tattooing

TODO: 

make is so tatoos wont repeat on itself 