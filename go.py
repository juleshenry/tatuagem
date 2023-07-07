from typing import List
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

CHZ = list(chr(u) for u in range(32, 128) if chr(u).isalpha())
# ~ j = lambda x: (0 if not len(x) or x[0] == "_" else 1)
# ~ free_attrs = lambda k: list(filter(j, dir(k)))
# ~ nex = enumerate

# ~ def explore_more(a: object, attack: List[int]):
# ~ # explore more
# ~ frats_a = free_attrs(a)
# ~ for A in attack:
# ~ print(A, frats_a[A])
# ~ # getattr(a, free_attrs[A])()
# ~ try:
# ~ getattr(a, frats_a[A])()
# ~ except TypeError as te:
# ~ print("TE:", te)
# ~ except ValueError as ve:
# ~ print("VE:", ve)
# ~ except ImportError as ie:
# ~ print("IE:", ie)


# ~ def expose(a: object, attack: List[int] = list([])):
# ~ # print(*(o for o in free_attrs(a)), sep="\n")
# ~ b = a.quantize()
# ~ print(b)
# ~ # print(*(f"{i}. {o}" for i,o in nex(free_attrs(b))), sep="\n")
# ~ explore_more(b, attack)


# 1. Make Template

template_size = 64
sqr = np.zeros((template_size, template_size, 3))
i = Image.fromarray(sqr, "RGB")
i.save("black-template.png")
FONT = "Poppins-Medium.ttf"
new_dir = f"fonts/{FONT[:-4]}"

try:
    os.mkdir(new_dir)
except FileExistsError:
    pass
# # # 2. Print out Templates
for o in CHZ:
    print("doing", o)
    img = Image.open("black-template.png")
    fnt = ImageFont.truetype(f"fonts/{FONT}", 32)
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
    x = "mayusc" if ord(o) <= 91 else "minisc"
    img.save(f"{new_dir}/{x}_{o}.png")


# 3. Analyze RGB of Templates -> Produce Text Mask


def yield_char_matrix(char):
    o = char
    x = "mayusc" if ord(o) <= 91 else "minisc"
    i = Image.open(f"{new_dir}/{x}_{o}.png")
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


oxo = [[] for _ in range(template_size)]


def concat(cmat, amat, sep=""):
    if not len(cmat) == len(amat):
        raise ValueError("equal len required")

    x = [[] for _ in range(len(cmat))]
    for ix, ab in enumerate(zip(cmat, amat)):
        a, b = ab
        x[ix] = a + ([sep] if a and b else []) + b
    return x


j = []
for x in "Tatuagem":
    cmat = yield_char_matrix(x)
    if not j:
        j = concat(oxo, cmat)
    else:
        j = concat(j, cmat, sep="**")
expose(j)

# ~ i.show()
# ~ print(*dir(b),sep='\n')
# ~ expose(a, list(range(0, 59)))


# 4. Print Text Mask interleaved with regex

# for u in chz:
# 	sqr = np.zeroes((8,8,3))
# 	i = Image.open(sqr)
# 	i1 = ImageDraw.Draw(i)

if __name__ == "__main__":
    pass
