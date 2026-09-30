"""
Test in-memory glyph rendering.
"""

import hashlib
import os
import sys

import pytest

# Add parent directory to path to import tatuagem modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tatuagem.core import get_tattoo_string, resolve_font_path, yield_char_matrix
from tatuagem.params import BASE_DIR


def _sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def test_output_matches_png_pipeline():
    """Hashes captured from the old render-to-PNG pipeline (v0.1.14)."""
    assert _sha(get_tattoo_string("tatuagem")) == (
        "73dc8dd1a4a5da3f50a1487368a84da2f7d6adb645c1e15615586cee96f960e8"
    )
    assert _sha(
        get_tattoo_string(
            "Hello, World!",
            font="Poppins-Medium.ttf",
            text="█",
            backsplash=" ",
            pattern="`':,",
            margin=1,
        )
    ) == "5afdb12b5d9385eadd5dae55bf361369cba134e3440daeeeee86ed8f0c8e65a1"


def test_non_ascii_characters_render():
    """Glyphs outside printable ASCII used to crash with FileNotFoundError."""
    out = get_tattoo_string("ção")
    assert "1" in out


def test_space_is_fixed_width():
    mat = yield_char_matrix(" ")
    assert len(mat) == 64
    assert all(len(row) == 9 for row in mat)
    assert all(c == "0" for row in mat for c in row)


def test_font_by_path():
    path = os.path.join(BASE_DIR, "fonts", "Poppins-Medium.ttf")
    assert get_tattoo_string("ab", font=path) == get_tattoo_string("ab", font="Poppins-Medium.ttf")


def test_unknown_font_lists_bundled_fonts():
    with pytest.raises(FileNotFoundError, match="unicode-arial.ttf"):
        resolve_font_path("nope.ttf")


def test_render_does_not_write_to_package(tmp_path):
    before = sorted(os.listdir(os.path.join(BASE_DIR, "fonts")))
    get_tattoo_string("zq!", font="Poppins-Medium.ttf")
    assert sorted(os.listdir(os.path.join(BASE_DIR, "fonts"))) == before
