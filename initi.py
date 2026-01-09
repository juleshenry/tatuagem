from params import TEMPLATE_SIZE, Image, ImageDraw, ImageFont, CHZ, BASE_DIR
import numpy as np
import os, datetime


def init_and_create_templates(font: str):
    btpng = os.path.join(BASE_DIR, "black-template.png")
    new_dir = os.path.join(BASE_DIR, "fonts", font[:-4])  # cut out .ttf
    sqr = np.zeros((TEMPLATE_SIZE, TEMPLATE_SIZE, 3))
    i = Image.fromarray(sqr, "RGB")
    i.save(btpng)
    try:
        os.mkdir(new_dir)
    except FileExistsError:
        pass
    for o in CHZ:
        print("making", o)
        img = Image.open(btpng)
        fnt = ImageFont.truetype(os.path.join(BASE_DIR, "fonts", font), 32)
        i1 = ImageDraw.Draw(img)
        anch = "la"
        i1 = i1.text(
            (
                24,
                8,
            ),
            o,
            anchor=anch,
            font=fnt,
            fill=(
                255,
                255,
                0,
            ),
        )
        font_png_path = get_font_png_path(o, new_dir)
        img.save(font_png_path)
    print("done")


def get_font_png_path(char: str, new_dir: str):
    """Returns the path of the png corresponding to the character char"""
    font_png_path = f"{new_dir}/__{char}__.png"
    # Lowercase treated separately for NIX reasons
    if 97 <= ord(char) <= 97 + 26:
        font_png_path = f"{new_dir}/__lowercase_{char}__.png"
    elif char in r"/":
        font_png_path = f"{new_dir}/__chr({ord(char)})__.png"
    else:
        font_png_path = f"{new_dir}/__{char}__.png"
    return font_png_path


if __name__ == "__main__":
    init_and_create_templates()
