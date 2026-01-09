import json
import os
from params import BASE_DIR


if __name__ == "__main__":
    try:
        with open(os.path.join(BASE_DIR, "lang_to_block_syntax.json"), "r") as f:
            lang_block = json.load(f)
    except FileNotFoundError:
        lang_block = {"Languages": {}, "Block Syntaxes": {}}

    try:
        with open(os.path.join(BASE_DIR, "extension_to_lang.json"), "r") as f:
            ext_lang = json.load(f)
    except FileNotFoundError:
        ext_lang = {}
    languages_in_syntax = set(lang_block.keys())

    # Get languages from ext_lang values
    languages_in_ext = set(ext_lang.values())

    # Find intersection (languages present in both)
    intersection = languages_in_syntax.intersection(languages_in_ext)

    # Find set difference (languages in syntax but not in ext mapping)
    syntax_only = languages_in_syntax.difference(languages_in_ext)

    # Find set difference (languages in ext mapping but not in syntax)
    ext_only = languages_in_ext.difference(languages_in_syntax)
    # # print(f"Intersection: {intersection}")
    #     print(f"Syntax only: {syntax_only}")
    #     print(f"Ext only: {ext_only}")

    for ext, lang in ext_lang.items():
        if lang in lang_block and not lang_block[lang]:
            print(
                f"Extension: {ext}, Language: {lang}, Block Syntax: {lang_block[lang]}"
            )
        # else:
        #     print(f"Extension: {ext}, Language: {lang}, Block Syntax: Not Found")
