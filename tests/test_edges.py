"""
Test error paths and entry points.
"""

import os
import runpy
import sys

import pytest

# Add parent directory to path to import tatuagem modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tatuagem import core, recurse
from tatuagem.recurse import (
    apply_tattoo_to_directory,
    extract_first_comment,
    get_tattoo,
    load_tatignore_patterns,
    resolve_language,
)


def test_render_helpers(capsys):
    assert core.tatuar([["0", "0"], []]) == ""  # nothing but background
    with pytest.raises(ValueError):
        core.concat([[]], [[], []])
    core.expose([["1", "0"]], margin=0)
    assert capsys.readouterr().out == "10\n\n"


def test_cli_errors(tmp_path, capsys):
    with pytest.raises(SystemExit):
        core.main(["hi", "--dry-run"])  # needs --recurse-path
    empty = tmp_path / "empty.txt"
    empty.write_text("  \n")
    with pytest.raises(SystemExit):
        core.main(["--file", str(empty)])
    assert "whitespace" in capsys.readouterr().err


def test_cli_file_renders_its_text(tmp_path, capsys):
    f = tmp_path / "t.txt"
    f.write_text("ok")
    core.main(["--file", str(f), "--margin", "0"])
    assert capsys.readouterr().out.strip("\n").startswith(("0", "1"))


def test_python_m_tatuagem(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["tatuagem", "--version"])
    with pytest.raises(SystemExit) as e:
        runpy.run_module("tatuagem", run_name="__main__")
    assert e.value.code == 0
    assert capsys.readouterr().out.startswith("tatuagem ")


def test_legacy_recurse_cli(monkeypatch, tmp_path, capsys):
    (tmp_path / "a.py").write_text("x = 1\n")
    monkeypatch.setattr(sys, "argv", ["recurse", "--text", "hi", "--path", str(tmp_path)])
    recurse.main()
    assert (tmp_path / "a.py").read_text().endswith("x = 1\n")
    assert "Tattooed" in capsys.readouterr().out
    monkeypatch.setattr(sys, "argv", ["recurse", "--text", "hi", "--path", str(tmp_path / "nope")])
    recurse.main()
    assert "Path not found" in capsys.readouterr().out


def test_empty_tattoo_aborts(tmp_path, capsys):
    (tmp_path / "a.py").write_text("x = 1\n")
    assert apply_tattoo_to_directory(str(tmp_path), "  \n") == []
    assert "Aborting" in capsys.readouterr().out


def test_binary_and_unreadable_files_are_skipped(tmp_path):
    (tmp_path / "blob.py").write_bytes(b"\xff\xfe\x00binary")
    (tmp_path / "ok.py").write_text("x = 1\n")
    changed = apply_tattoo_to_directory(str(tmp_path), get_tattoo("b"))
    assert changed == [str(tmp_path / "ok.py")]


def test_unexpected_errors_are_reported(tmp_path, monkeypatch, capsys):
    (tmp_path / "a.py").write_text("x = 1\n")

    def boom(*args):
        raise RuntimeError("kaboom")

    monkeypatch.setattr(recurse, "_tattoo_file", boom)
    assert apply_tattoo_to_directory(str(tmp_path), get_tattoo("b")) == []
    assert "kaboom" in capsys.readouterr().out


def test_unreadable_tatignore(tmp_path, capsys):
    (tmp_path / ".tatignore").mkdir()
    assert load_tatignore_patterns(str(tmp_path)) == []
    assert "Could not read .tatignore" in capsys.readouterr().out


def test_ignored_directories_are_pruned(tmp_path):
    (tmp_path / ".tatignore").write_text("vendor/\n")
    (tmp_path / "vendor").mkdir()
    (tmp_path / "vendor" / "lib.py").write_text("x = 1\n")
    assert apply_tattoo_to_directory(str(tmp_path), get_tattoo("v")) == []


def test_extract_first_comment_line_and_missing():
    assert extract_first_comment("# a\n# b\ncode", "#", "#") == " a\n b"
    assert extract_first_comment("code", "/*", "*/") is None
    assert extract_first_comment("/* never closed", "/*", "*/") is None


@pytest.mark.parametrize(
    "name, text, lang",
    [
        ("a.pl", "main :- write(hi).\n", "Prolog"),
        ("a.pl", "print 'hi';\n", "Perl"),
        ("a.m", "#import <Foundation/Foundation.h>\n", "Objective-C"),
        ("a.m", "% comment\ndisp('hi')\n", "MATLAB"),
        ("a.pro", "; IDL\npro hello\n", "IDL"),
        ("a.pro", "hello :- true.\n", "Prolog"),
    ],
)
def test_content_heuristics(tmp_path, name, text, lang):
    f = tmp_path / name
    f.write_text(text)
    assert resolve_language(str(f)) == lang
