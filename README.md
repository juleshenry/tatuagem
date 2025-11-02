# Tatuagem, the boastful code signature suite

# Basic Example
```python3 tatuagem.py "tatuagem" ```

* defaults defined in tatuagem.py: '1' for text, '0' for background, unicode-arial.ttf for font 

# Elaborate Syntax Example
```python3 tatuagem.py "L'appel du vide" --font 'unicode-arial.ttf' --backsplash '!' --text '@'```


![alt text](lappel.png)

# Wallpaper: Pattern-Argument Syntax Example
```python3 tatuagem.py "Tatuagem" --pattern '`':,:'' ```

![alt text](tatu.png)


TODO: 

We want to recurse a directory structure and apply comments of the tattoo in the appropriate comment syntax for each file type.

In addition, we want to test this for all languages, major and minor. We want to have a coverage badge for that.



We give the user a chance to have overrides for extensions.

They will give a language that refers to lang_comment_block_syntax.json 

If a file has an extension that has an entry for that language, then use the lang_comment_block_syntax.json 
otherwise use default_extension_syntax.json

"Languages" : {"start" "end"}
if override language: 
    use for an extension, the entry at language
else:
    use default extension comments
"Extensions" : {"start" "end"}
"Languages" : "Extensions"

write this in override.py
