# PSEUDO ___INIT__.PY
import os

TEMPLATE_SIZE = 64
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHZ = list(chr(u) for u in range(32, 128))  # if chr(u).isalpha())
