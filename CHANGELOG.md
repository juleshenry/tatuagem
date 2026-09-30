# Changelog

## v0.1.17 (2026-09-30)

* Fix: README images now render on PyPI (absolute raw GitHub URLs instead of repo-relative paths), with real alt text

## v0.1.16 (2026-09-30)

* Language data rebuilt for all 468 corpus languages (the old table was LLM-generated and had broken entries like `(* *)` / `(*)`)
* Safe commenting: block comments only when the tattoo can't close or nest into them, otherwise line comments, otherwise skip; per-language `forbid` (`--` in XML, `\u` in Java, `"` in OCaml)
* `<?php` / `<?xml ?>` declarations, encoding cookies and Dockerfile parser directives stay above the tattoo
* Language detection by exact filename (Makefile, Dockerfile…), content heuristics for `.pl` / `.m` / `.pro`, and shebang for extensionless scripts
* Fix: `--overwrite` on line-comment languages cut the file at the second `#`
* Fix: `.s` used `;` comments, which are statement separators in GNU as on x86
* COBOL (`      *>`, valid in fixed and free form), Visual Basic / VBA and text AppleScript (`.applescript`) supported; compiled `.scpt` is never touched
* Corpus: dropped 17 joke/unidentifiable folders; fixed extensionless VB/VBA samples and a mis-indented COBOL sample
* Language and unit-test coverage computed in CI and published as badges; CI fails below 90% language coverage (91.9% today)

## v0.1.15 (2026-09-30)

* Fix: version was set to `v0.0.15`, lower than the published 0.1.14; `publish.py` now refuses non-increasing versions
* Glyphs are rendered in memory: no more PNG templates written into site-packages, any Unicode character works, `--font` accepts a path to any `.ttf`/`.otf`
* Output is byte-identical to 0.1.14 for printable ASCII
* Drop the deprecated `Image.getdata()` (removed in Pillow 14)
* Tattoo headers in the package are raw strings, fixing `SyntaxWarning: invalid escape sequence` on Python 3.12+
* CLI: unknown flags are errors; settings print only with `--verbose` (to stderr) so stdout is just the tattoo; new `--dry-run` and `--check`
* `.tatignore` uses real gitignore semantics (via `pathspec`); hidden directories are skipped
* Dev scripts moved out of the package into `scripts/`
* CI: tests on Python 3.12–3.14 (+ macOS/Windows), ruff, dogfood check, wheel smoke test; publishing waits for CI and checks the tag matches the version

## v0.1.14 (2026-03-03)

* Automated release update

## v0.1.13 (2026-02-07)

* Automated release update

## v0.1.12 (2026-02-07)

* Automated release update

## v0.1.12 (2026-02-06)

* Automated release update

## v0.1.11 (2026-02-06)

* Automated release update

## v0.1.10 (2026-02-05)

* Automated release update

## v0.1.9 (2026-02-05)

* Automated release update

## v0.1.7 (2026-01-23)

* Automated release update

## v0.1.6 (2026-01-23)

* Automated release update

## v0.1.5 (2026-01-23)

* Automated release update

## v0.1.5 (2026-01-23)

* Automated release update

## v0.1.1

### What's Changed
* Agora by @DerekITCoder in https://github.com/juleshenry/tatuagem/pull/6
* Add shebang detection to prevent crashes when tattooing executable scripts by @Copilot in https://github.com/juleshenry/tatuagem/pull/11
* Update Readme by @juleshenry in https://github.com/juleshenry/tatuagem/pull/14

### New Contributors
* @DerekITCoder made their first contribution in https://github.com/juleshenry/tatuagem/pull/6
* @Copilot made their first contribution in https://github.com/juleshenry/tatuagem/pull/11
* @juleshenry made their first contribution in https://github.com/juleshenry/tatuagem/pull/14

**Full Changelog**: https://github.com/juleshenry/tatuagem/commits/v0.1.1
