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

TODO: 

make is so tatoos wont repeat on itself
make it so it wont crash on node package manager
add some sort of checker to tell if the first line is a shebang 