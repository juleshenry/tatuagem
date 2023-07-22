from params import TEMPLATE_SIZE, Image, ImageDraw, ImageFont, CHZ
import numpy as np
import os


def init_and_create_templates(font="Poppins-Medium.ttf"):
    btpng = "black-template.png"
    new_dir = f"fonts/{font[:-4]}"
    sqr = np.zeros((TEMPLATE_SIZE, TEMPLATE_SIZE, 3))
    i = Image.fromarray(sqr, "RGB")
    i.save(btpng)
    try:
        os.mkdir(new_dir)
    except FileExistsError:
        pass
    for o in CHZ:
        img = Image.open(btpng)
        fnt = ImageFont.truetype(f"fonts/{font}", 32)
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
        return img.save(font_png_path)


def get_font_png_path(o: str, new_dir: str):
    font_png_path = f"{new_dir}/__{o}__.png"
    try:
        with open(font_png_path) as s:
            if o.isalpha():
                font_png_path = f"{new_dir}/__lowercase_{o}__.png"
    except FileNotFoundError:
        try:
            font_png_path = f"{new_dir}/__{o}__.png"
        except FileNotFoundError and FileNotFoundError:  # ~ I'm a demon <3 -jh
            font_png_path = f"{new_dir}/__chr({ord(o)})__.png"
    return font_png_path


if __name__ == "__main__":
    init_and_create_templates()
