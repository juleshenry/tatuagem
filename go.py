from typing import List
import os
from params import TEMPLATE_SIZE, Image, ImageDraw, ImageFont
from initi import get_font_png_path

kwargs_list = {"text", "backsplash", "time_stamp", "font"}

# 3. Analyze RGB of Templates -> Produce Text Mask
def yield_char_matrix(char, font="Poppins-Medium.ttf"):
    new_dir = f"fonts/{font[:-4]}"
    o = char
    fpp = get_font_png_path(char, new_dir)
    i = Image.open(fpp)
    b = i.quantize().getdata()
    print(o * 99)
    o = [[] for _ in range(b.size[1])]
    for ix, h in enumerate(range(b.size[1])):
        # ~ if not sum([o-b.getpixel((0,0,)) for o in [b.getpixel((i,h,)) for i in range(b.size[0])]]):
        # ~ continue
        if not (12 < h < 64 - 12):
            continue
        for w in range(b.size[0]):
            if not sum(
                [
                    o
                    - b.getpixel(
                        (
                            0,
                            0,
                        )
                    )
                    for o in [
                        b.getpixel(
                            (
                                w,
                                i,
                            )
                        )
                        for i in range(b.size[1])
                    ]
                ]
            ):
                continue
            o[ix].append(
                "#"
                if b.getpixel(
                    (
                        w,
                        h,
                    )
                )
                - b.getpixel(
                    (
                        0,
                        0,
                    )
                )
                else "*"
            )
    return o


def expose(mat):
    # prints a `matrix`
    for i in mat:
        if i:
            print("".join(i))


def concat(cmat, amat, sep=""):
    if not len(cmat) == len(amat):
        raise ValueError("equal len required")

    x = [[] for _ in range(len(cmat))]
    for ix, ab in enumerate(zip(cmat, amat)):
        a, b = ab
        x[ix] = a + ([sep] if a and b else []) + b
    return x


def tatuagem(frase: str, **kwargs):
    for k, v in kwargs.items():
        print(k, v)
    j = []
    oxo = [[] for _ in range(TEMPLATE_SIZE)]
    for x in frase:
        cmat = yield_char_matrix(x, font=kwargs["font"])
        if not j:
            j = concat(oxo, cmat)
        else:
            j = concat(j, cmat, sep="**")
    expose(j)

import argparse

if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description="Tatuagem")

    # Add the options
    parser.add_argument("--text", "-t", action="store_true", help="Set the text option")
    parser.add_argument(
        "--backsplash", "-bs", action="store_true", help="Enable backsplash option"
    )
    parser.add_argument(
        "--time-stamp", "-ts", action="store_true", help="Enable time stamp option"
    )
    parser.add_argument("--font", "-f", metavar="FONT", help="Set the font option")

    # Parse the first argument
    args, positional_args = parser.parse_known_args()

    arg0_frase = positional_args[0]
    # Access the option values
    if args.text:
        print("Text option is enabled")

    if args.backsplash:
        print("Backsplash option is enabled")

    if args.time_stamp:
        print("Time stamp option is enabled")

    if args.font:

        print("Font option is set to:", args.font)
    if not args.font:
        args.font = "Poppins-Medium.ttf"

    tatuagem(arg0_frase, **{a: getattr(args, a) for a in kwargs_list})
