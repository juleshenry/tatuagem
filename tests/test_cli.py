"""
Test the command line interface, --dry-run/--check, and that the repo dogfoods its own tattoos.
"""

import os
import subprocess
import sys
import warnings

import pytest

# Add parent directory to path to import tatuagem modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tatuagem.core import main
from tatuagem.recurse import apply_tattoo_to_directory, get_tattoo, is_tattoo_comment

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_stdout_is_only_the_tattoo(capsys):
    main(["hi"])
    out, err = capsys.readouterr()
    assert "backsplash:" not in out
    assert set(out) <= {"0", "1", "\n"}, out[-400:]
    assert err == ""


def test_verbose_goes_to_stderr(capsys):
    main(["hi", "--verbose"])
    out, err = capsys.readouterr()
    assert "backsplash: 0" in err
    assert "backsplash:" not in out


def test_unknown_flag_is_an_error(capsys):
    with pytest.raises(SystemExit) as e:
        main(["hi", "--patern", "x"])
    assert e.value.code == 2


def test_unknown_font_is_an_error(capsys):
    with pytest.raises(SystemExit) as e:
        main(["hi", "--font", "nope.ttf"])
    assert e.value.code == 2
    assert "bundled fonts" in capsys.readouterr().err


def test_no_text_is_an_error(capsys):
    with pytest.raises(SystemExit) as e:
        main([])
    assert e.value.code == 2


def test_dry_run_does_not_write(tmp_path):
    f = tmp_path / "a.py"
    f.write_text("print(1)\n")
    changed = apply_tattoo_to_directory(str(tmp_path), get_tattoo("x"), dry_run=True)
    assert changed == [str(f)]
    assert f.read_text() == "print(1)\n"


def test_check_exit_code(tmp_path):
    (tmp_path / "a.py").write_text("print(1)\n")
    with pytest.raises(SystemExit) as e:
        main(["x", "--recurse-path", str(tmp_path), "--check"])
    assert e.value.code == 1
    main(["x", "--recurse-path", str(tmp_path)])
    main(["x", "--recurse-path", str(tmp_path), "--check"])  # now passes


def test_hidden_directories_are_skipped(tmp_path):
    hidden = tmp_path / ".venv"
    hidden.mkdir()
    (hidden / "lib.py").write_text("print(1)\n")
    assert apply_tattoo_to_directory(str(tmp_path), get_tattoo("x")) == []


PACKAGE_SOURCES = [
    os.path.join(ROOT, "tatuagem", f)
    for f in sorted(os.listdir(os.path.join(ROOT, "tatuagem")))
    if f.endswith(".py")
]


@pytest.mark.parametrize("path", PACKAGE_SOURCES, ids=os.path.basename)
def test_package_sources_are_tattooed(path):
    """Dogfood: every module ships with a tattoo, and the tattoo never breaks compilation."""
    with open(path, encoding="utf-8") as f:
        src = f.read()
    start = next(d for d in ('r"""', '"""') if src.startswith(d))
    body = src[len(start) :].split('"""', 1)[0]
    assert is_tattoo_comment(body)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        compile(src, path, "exec")


def test_repo_dogfood_check():
    """Same check CI and publish.py run."""
    r = subprocess.run(
        [sys.executable, "-m", "tatuagem", "--file", "test_input.txt", "--recurse-path", ".", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
