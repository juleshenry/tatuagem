TEMPLATE_SIZE = 64
from PIL import Image, ImageDraw, ImageFont

CHZ = list(chr(u) for u in range(32, 128) ) #if chr(u).isalpha())