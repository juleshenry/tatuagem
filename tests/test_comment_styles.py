"""
Test comment style selection, safe fallbacks, and re-tattooing for line/block comments.
"""

import os
import subprocess
import sys

import pytest

# Add parent directory to path to import tatuagem modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tatuagem import recurse
from tatuagem.recurse import _tattoo_file, comment_style, comment_text, get_tattoo, resolve_language

ART = "\n".join(["*/ -- ## /\\ '''\"\"\" " * 3] * 6)


@pytest.fixture
def langs(monkeypatch):
    monkeypatch.setattr(
        recurse,
        "EXT_TO_LANG",
        {
            ".c": "C",
            ".sh": "Shell",
            ".py": "Python",
            ".php": "PHP",
            ".bf": "Brainfuck",
            ".hs": "Haskell",
            "Makefile": "Makefile",
        },
    )
    monkeypatch.setattr(
        recurse,
        "LANG_TO_SYNTAX",
        {
            "C": {"block": {"start": "/*", "end": "*/"}, "line": "//"},
            "Shell": {"block": None, "line": "#"},
            "Python": {"block": {"start": '"""', "end": '"""'}, "line": "#"},
            "PHP": {"block": {"start": "/*", "end": "*/"}, "line": "//", "top_ok": False},
            "Brainfuck": {"block": None, "line": None},
            "Haskell": {"block": {"start": "{-", "end": "-}"}, "line": "--"},
            "Makefile": {"block": None, "line": "#"},
        },
    )


def test_resolve_language_prefers_exact_filename(langs):
    assert resolve_language("/x/Makefile") == "Makefile"
    assert resolve_language("/x/a.C") == "C"
    assert resolve_language("/x/README") is None


def test_block_preferred_when_safe(langs):
    assert comment_style("a.c", "0101") == ("block", "/*", "*/")


def test_falls_back_to_line_when_text_would_close_block(langs):
    assert comment_style("a.c", ART) == ("line", "//", "")
    out = comment_text("a.c", ART)
    assert all(line.startswith("//") for line in out.split("\n"))


def test_falls_back_when_text_would_open_nested_block(langs):
    assert comment_style("a.hs", "a {- b") == ("line", "--", "")


def test_python_picks_safe_quotes_then_falls_back(langs):
    assert comment_style("a.py", "plain") == ("block", '"""', '"""')
    assert comment_style("a.py", "has 'quote'") == ("block", 'r"""', '"""')
    assert comment_style("a.py", 'has """') == ("block", "r'''", "'''")
    assert comment_style("a.py", "has \"\"\" and '''") == ("line", "#", "")


def test_unsupported_languages(langs):
    assert comment_style("a.php", "x") is None  # top_ok false
    assert comment_style("a.bf", "x") is None  # no comment syntax
    assert comment_style("a.unknown", "x") is None


def test_line_comment_overwrite_keeps_code(langs, tmp_path):
    """Regression: overwrite used to split line-comment files at the second '#'."""
    f = tmp_path / "run.sh"
    f.write_text("#!/bin/sh\necho '# not a comment'\n")
    first = _tattoo_file(str(f), get_tattoo("one"), overwrite=False)
    f.write_text(first)
    second = _tattoo_file(str(f), get_tattoo("two"), overwrite=True)
    assert second.startswith("#!/bin/sh\n# ")
    assert second.endswith("\necho '# not a comment'\n")
    assert second.count("echo") == 1
    assert get_tattoo("two").split("\n")[3] in second
    assert get_tattoo("one").split("\n")[3] not in second


def test_line_comment_tattoo_is_idempotent(langs, tmp_path):
    f = tmp_path / "Makefile"
    f.write_text("all:\n\techo hi\n")
    f.write_text(_tattoo_file(str(f), get_tattoo("mk"), overwrite=False))
    assert _tattoo_file(str(f), get_tattoo("mk"), overwrite=False) is None
    assert _tattoo_file(str(f), get_tattoo("other"), overwrite=False) is None


def test_module_entry_point():
    r = subprocess.run(
        [sys.executable, "-m", "tatuagem", "--version"], capture_output=True, text=True
    )
    assert r.returncode == 0
    assert r.stdout.startswith("tatuagem ")


def test_preamble_stays_on_top(langs, tmp_path):
    f = tmp_path / "enc.py"
    f.write_text("#!/usr/bin/env python\n# -*- coding: latin-1 -*-\nx = 1\n")
    out = _tattoo_file(str(f), get_tattoo("py"), overwrite=False)
    assert out.startswith("#!/usr/bin/env python\n# -*- coding: latin-1 -*-\n")
    assert out.endswith("x = 1\n")


def test_split_preamble():
    assert recurse.split_preamble("# syntax=docker/dockerfile:1\nFROM x\n") == (
        "# syntax=docker/dockerfile:1\n",
        "FROM x\n",
    )
    assert recurse.split_preamble("x = 1\n") == ("", "x = 1\n")
    assert recurse.split_preamble("#!/bin/sh") == ("#!/bin/sh\n", "")


def test_keep_first_and_require_first(langs, monkeypatch, tmp_path):
    recurse.EXT_TO_LANG[".xml"] = "XML"
    recurse.LANG_TO_SYNTAX["XML"] = {
        "block": {"start": "<!--", "end": "-->"},
        "keep_first": ["<?xml"],
        "forbid": ["--"],
    }
    recurse.LANG_TO_SYNTAX["PHP"] = {
        "block": {"start": "/*", "end": "*/"},
        "line": "//",
        "keep_first": ["<?php"],
        "require_first": True,
    }
    x = tmp_path / "a.xml"
    x.write_text('<?xml version="1.0"?>\n<a/>\n')
    out = _tattoo_file(str(x), get_tattoo("x"), overwrite=False)
    assert out.startswith('<?xml version="1.0"?>\n<!--\n')
    assert _tattoo_file(str(x), "a -- b\n" * 6, overwrite=False) is None  # forbidden

    p = tmp_path / "a.php"
    p.write_text("<?php\necho 1;\n")
    assert _tattoo_file(str(p), get_tattoo("p"), overwrite=False).startswith("<?php\n/*\n")
    p.write_text("<html><?php echo 1; ?></html>\n")
    assert _tattoo_file(str(p), get_tattoo("p"), overwrite=False) is None


def test_resolve_language_from_shebang(tmp_path):
    for line, lang in [
        ("#!/bin/ksh", "Ksh"),
        ("#!/usr/bin/env python3", "Python"),
        ("#!/usr/bin/env -S node --flag", "JavaScript"),
        ("#!/bin/bash -e", "Shell"),
        ("#!/usr/bin/unknown", None),
        ("echo hi", None),
    ]:
        f = tmp_path / "script"
        f.write_text(line + "\necho\n")
        assert resolve_language(str(f)) == lang, line


@pytest.mark.parametrize(
    "name, prefix",
    [
        ("a.cob", "      *> "),  # column-7 '*' (fixed form) and '*>' (free form)
        ("a.vb", "' "),
        ("a.bas", "' "),
        ("a.applescript", "(*\n"),
    ],
)
def test_real_language_data(name, prefix):
    assert comment_text(name, "0110\n1001").startswith(prefix)
    assert comment_text("compiled.scpt", "0110") is None  # binary AppleScript
