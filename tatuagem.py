from params import TEMPLATE_SIZE, Image, ImageDraw, ImageFont
from initi import get_font_png_path, init_and_create_templates
import argparse, os

MARGIN = 3  # top and bottom margin of text
KWARGS_LIST = {"text", "backsplash", "font", "pattern", "margin"}
SPACE_MARGIN = 4  # This defines what a space should be in the font, because the space file is a solid sheet
FONT_DEFAULT = "unicode-arial.ttf"
DEFAULT_TEXT_CHAR = "1"
DEFAULT_BACKSPLASH_CHAR = "0"


# 3. Analyze RGB of Templates -> Produce Text Mask
def yield_char_matrix(char: str, font: str = FONT_DEFAULT, **kwargs):
    new_dir = f"fonts/{font[:-4]}"
    fpp = get_font_png_path(char, new_dir)
    imat = Image.open(fpp).quantize().getdata()
    o = [[] for _ in range(imat.size[1])]
    # fmt: off
    for ix, h in enumerate(range(imat.size[1])):
        for w in range(imat.size[0]):
            if char == " " and (SPACE_MARGIN < w < TEMPLATE_SIZE - SPACE_MARGIN):
                continue
            if (
                not sum([o - imat.getpixel((0,0,)) for o in [imat.getpixel((w,i,)) for i in range(imat.size[1])]])
                and char != " "
            ):
                continue
            o[ix].append(
                kwargs['text']
                if imat.getpixel((w, h,)) - imat.getpixel((0, 0,))
                else kwargs['backsplash']
            )
        # fmt: on
    return o


def expose(mat, pattern=None, backsplash=None, margin=None):
    # prints a `matrix`
    pure_mat = list(
        filter(lambda x: x and not all(c == backsplash for c in "".join(x)), mat)
    )
    margin = int(margin)
    pure_mat = (
        (
            marg := [
                [backsplash * sum([len(x) for x in pure_mat[0]])] for _ in range(margin)
            ]
        )
        + pure_mat
        + marg
    )
    for text_list in pure_mat:
        out = "".join(text_list)
        if pattern:
            for i, c in enumerate(out):
                print(pattern[i % len(pattern)] if c == backsplash else c, end="")
        else:
            for i, c in enumerate(out):
                print(c, end="")
        print()


def concat(cmat, amat, sep: str = ""):
    # concatenates character matrices
    if not len(cmat) == len(amat):
        raise ValueError("equal len required")

    x = [[] for _ in range(len(cmat))]
    for ix, ab in enumerate(zip(cmat, amat)):
        a, b = ab
        x[ix] = a + ([sep] if a and b else []) + b
    return x


def tatuagem(frase: str, space_count: int = SPACE_MARGIN, **kwargs):
    # space_count, number of backsplash chars defining a 'space'
    j = []
    oxo = [[] for _ in range(TEMPLATE_SIZE)]
    for x in frase:
        cmat = yield_char_matrix(x, **kwargs)
        if not j:
            j = concat(oxo, cmat)
        else:
            j = concat(j, cmat, sep=(kwargs["backsplash"]) * space_count)
    expose(
        j,
        pattern=kwargs["pattern"],
        backsplash=kwargs["backsplash"],
        margin=kwargs["margin"],
    )


if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description="Tatuagem")
    # text is the char for the printout
    parser.add_argument("--text", default=DEFAULT_TEXT_CHAR, help="Set the text")  # fmt: skip
    parser.add_argument("--backsplash", default=DEFAULT_BACKSPLASH_CHAR, help="Choose backsplash")  # fmt: skip
    parser.add_argument("--font", default=FONT_DEFAULT, metavar="FONT", help="Set the font")  # fmt: skip
    parser.add_argument("--pattern", default=None, metavar="PATTERN", help="Set the pattern for backsplash")  # fmt: skip
    parser.add_argument(
        "--margin", default=MARGIN, help="Margin top and bottom for text"
    )
    args, positional_args = parser.parse_known_args()
    if not os.path.exists(z := f"./fonts/{args.font}"):
        init_and_create_templates(args.font)
    print("")
    print(f"text: {args.text}")
    print(f"backsplash: {args.backsplash}")
    print(f"font: {args.font}")
    print(f"pattern: {args.pattern}")
    print(f"margin: {args.margin}")
    arg0_frase = positional_args[0]
    tatuagem(arg0_frase, **{a: getattr(args, a) for a in KWARGS_LIST})
