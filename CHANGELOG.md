# Changelog

## v0.1.15 (unreleased)

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
