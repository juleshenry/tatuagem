import os
import argparse
import shutil
import json
from tatuagem import (
    yield_char_matrix,
    tatuar,
    concat,
    SPACE_MARGIN,
    FONT_DEFAULT,
    DEFAULT_TEXT_CHAR,
    DEFAULT_BACKSPLASH_CHAR,
    MARGIN,
)
from params import TEMPLATE_SIZE
from typing import Optional


def get_tattoo(phrase):
    kwargs = {
        "text": DEFAULT_TEXT_CHAR,
        "backsplash": DEFAULT_BACKSPLASH_CHAR,
        "font": FONT_DEFAULT,
        "pattern": None,
        "margin": MARGIN,
    }
    j = []
    oxo = [[] for _ in range(TEMPLATE_SIZE)]
    for x in phrase:
        cmat = yield_char_matrix(x, **kwargs)
        if not j:
            j = concat(oxo, cmat)
        else:
            j = concat(j, cmat, sep=(kwargs["backsplash"]) * SPACE_MARGIN)
    return tatuar(
        j,
        pattern=kwargs["pattern"],
        backsplash=kwargs["backsplash"],
        margin=kwargs["margin"],
    )


def comment_text(filepath, text) -> Optional[str]:
    ext = os.path.splitext(os.path.basename(filepath))[1].lower()
    lines = text.strip().split("\n")
    with open("extension_to_lang.json", "r", encoding="utf-8") as f:
        ext_lang = json.load(f)
    lang = ext_lang.get(ext, None)
    if not lang:
        return None  # No language found for this extension
    with open("lang_to_block_syntax.json", "r", encoding="utf-8") as f:
        lang_block = json.load(f)
    comment_syntax = lang_block.get(lang, None)
    if not comment_syntax:
        return None  # No comment syntax found for this language


def main():
    #  ✅  for every file in our tests, identify the comment syntax
    #  ✅ create a throwaway copy of all the files and tattoo them
    # 3. from our comment syntax json, add a code coverage badge

    # -1: update the ovo.yaml files with debian linux installation commands
    parser = argparse.ArgumentParser(
        description="Recurse directory and add tattoo comments"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default="tests/hello_worlds",
        help="Directory to recurse (default: tests/hello_worlds)",
    )
    args = parser.parse_args()

    # Create a copy for testing
    copy_path = args.directory  # + '_copy'
    # shutil.copytree(args.directory, copy_path)

    tattoo = get_tattoo("tatuagem")

    with open("lang_to_block_syntax.json", "r", encoding="utf-8") as f:
        block = json.load(f)

    good_counter = total_counter = 0

    for root, dirs, files in os.walk(copy_path):
        for file in files:
            if file == "ovo.yaml":
                continue
            total_counter += 1
            filepath = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            print(filepath)
            start_end = block.get(os.path.split(os.path.dirname(filepath))[-1], None)
            if start_end:
                good_counter += 1
                print(start_end)

            # try:
            #     with open(filepath, 'r', encoding='utf-8') as f:
            #         content = f.read()
            #     commented_tattoo = comment_text(filepath, tattoo)
            #     new_content = commented_tattoo + '\n\n' + content
            #     with open(filepath, 'w', encoding='utf-8') as f:
            #         f.write(new_content)
            # except (UnicodeDecodeError, IsADirectoryError, PermissionError):
            #     pass  # skip binary files or errors

    # Delete the test copy
    return good_counter / total_counter
    # shutil.rmtree(copy_path)


import anybadge

if __name__ == "__main__":
    coverage = main()
    badge = anybadge.Badge(
        "coverage",
        round(coverage * 100, 4),
        thresholds={10: "red", 20: "orange", 30: "green"},
    )
    import os

    try:
        os.remove("coverage.svg")
    except FileNotFoundError:
        pass
    # Now create the badge
    badge.write_badge("coverage.svg")
