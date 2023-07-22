from typing import List
import os
from params import TEMPLATE_SIZE, Image, ImageDraw, ImageFont
from initi import get_font_png_path
import argparse

MARGIN = 12
KWARGS_LIST = {"text", "backsplash", "time_stamp", "font"}
SPACE_MARGIN = 4
FONT_DEFAULT = "Poppins-Medium.ttf"

# 3. Analyze RGB of Templates -> Produce Text Mask
def yield_char_matrix(
    char, font=FONT_DEFAULT, crop_top=False, **kwargs
):
    new_dir = f"fonts/{font[:-4]}"
    fpp = get_font_png_path(char, new_dir)
    imat = Image.open(fpp).quantize().getdata()
    o = [[] for _ in range(imat.size[1])]

    for ix, h in enumerate(range(imat.size[1])):
        if crop_top and not sum(
            [
                o
                - imat.getpixel(
                    (
                        0,
                        0,
                    )
                )
                for o in [
                    imat.getpixel(
                        (
                            i,
                            h,
                        )
                    )
                    for i in range(imat.size[0])
                ]
            ]
        ):
            continue
        if not (MARGIN < h < TEMPLATE_SIZE - MARGIN):
            continue
        for w in range(imat.size[0]):
            if char == " " and (SPACE_MARGIN < w < TEMPLATE_SIZE - SPACE_MARGIN):
                continue
            if (
                not sum(
                    [
                        o
                        - imat.getpixel(
                            (
                                0,
                                0,
                            )
                        )
                        for o in [
                            imat.getpixel(
                                (
                                    w,
                                    i,
                                )
                            )
                            for i in range(imat.size[1])
                        ]
                    ]
                )
                and char != " "
            ):
                continue
            o[ix].append(
                kwargs['text']
                if imat.getpixel(
                    (
                        w,
                        h,
                    )
                )
                - imat.getpixel(
                    (
                        0,
                        0,
                    )
                )
                else kwargs['backsplash']
            )
    return o


# prints a `matrix`
def expose(mat):
    [print("".join(i)) for i in mat if i]  # fmt: skip


def concat(cmat, amat, sep: str = ""):
    if not len(cmat) == len(amat):
        raise ValueError("equal len required")

    x = [[] for _ in range(len(cmat))]
    for ix, ab in enumerate(zip(cmat, amat)):
        a, b = ab
        x[ix] = a + ([sep] if a and b else []) + b
    return x


def tatuagem(frase: str, space_count: int = 2, **kwargs):
    # space_count, number of backsplash chars defining a 'space'
    j = []
    oxo = [[] for _ in range(TEMPLATE_SIZE)]
    for x in frase:
        cmat = yield_char_matrix(x, **kwargs)
        if not j:
            j = concat(oxo, cmat)
        else:
            j = concat(j, cmat, sep=(kwargs["backsplash"]) * space_count)
    expose(j)


if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description="Tatuagem")
    st = "store_true"
    parser.add_argument("--text", "-t", help="Set the text")  # fmt: skip
    parser.add_argument("--backsplash", "-bs", help="Enable backsplash")  # fmt: skip
    parser.add_argument("--time-stamp", "-ts", action=st, help="Enable time stamp")  # fmt: skip
    parser.add_argument("--font", "-f", metavar="FONT", help="Set the font")  # fmt: skip
    # Parse the first argument
    args, positional_args = parser.parse_known_args()
    arg0_frase = positional_args[0]
    # Access the option values
    # if args.text:
    #     print("Text option is enabled")
    # if args.backsplash:
    #     print("Backsplash option is enabled")
    # if args.time_stamp:
    #     print("Time stamp option is enabled")
    if not args.font:
        args.font = "Poppins-Medium.ttf"
    if not args.text:
        args.text="*"
    if not args.backsplash:
        args.backsplash="#"
    tatuagem(arg0_frase, **{a: getattr(args, a) for a in KWARGS_LIST})
