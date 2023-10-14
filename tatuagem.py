from params import TEMPLATE_SIZE, Image, ImageDraw, ImageFont
from initi import get_font_png_path, init_and_create_templates
import argparse, os

MARGIN = 10 # top and bottom margin of text
KWARGS_LIST = {"text", "backsplash", "time_stamp", "font", "regex", "margin"}
SPACE_MARGIN = 4  # This defines what a space should be in the font, because the space file is a solid sheet
FONT_DEFAULT = "unicode-arial.ttf"
DEFAULT_TEXT_CHAR = "*"
DEFAULT_BACKSPLASH_CHAR = "#"

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




def expose(mat, regex=None, backsplash=None, margin=None):
    # prints a `matrix`
    in_top = True
    for text_list in mat:
        if text_list:
            out = "".join(text_list)
            if regex:
                for i, c in enumerate(out):
                    if c == backsplash:
                        print(regex[i % len(regex)], end="")
                    else:
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
    expose(j, regex=kwargs["regex"], backsplash=kwargs["backsplash"], margin=kwargs['margin'])


if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description="Tatuagem")
    # text is the char for the printout
    parser.add_argument("--text", default=DEFAULT_TEXT_CHAR, help="Set the text")  # fmt: skip
    parser.add_argument("--backsplash", default=DEFAULT_BACKSPLASH_CHAR, help="Choose backsplash")  # fmt: skip
    parser.add_argument("--time-stamp", default=True, help="Enable time stamp")  # fmt: skip
    parser.add_argument("--font", default=FONT_DEFAULT, metavar="FONT", help="Set the font")  # fmt: skip
    parser.add_argument("--regex", default=None, metavar="REGEX", help="Set the regex pattern for backsplash")  # fmt: skip
    parser.add_argument('--margin', default = MARGIN, help = "Margin top and bottom for text")
    args, positional_args = parser.parse_known_args()
    if not os.path.exists(z := f"./fonts/{args.font}"):
        init_and_create_templates(args.font)
    arg0_frase = positional_args[0]
    tatuagem(arg0_frase, **{a: getattr(args, a) for a in KWARGS_LIST})
