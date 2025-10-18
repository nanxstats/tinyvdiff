# Changelog

## tinyvdiff 0.5.0

### Improvements

- Specify explicit UTF-8 encoding when reading and writing SVG files so
  snapshot comparisons always use the same encoding (#49).
  This change cannot eliminate SVG content differences caused by different
  platforms or `pdf2svg` versions, but it helps avoid subtle bugs from
  text file encoding discrepancies.

### Linting

- Added ruff linter configuration to `pyproject.toml` with popular rule sets
  including pycodestyle, Pyflakes, pyupgrade, flake8-bugbear, flake8-simplify,
  and isort (#47).
- Fixed `ruff check` linting issues including F401, UP015, and SIM112 (#47).

## tinyvdiff 0.4.1

### Maintenance

- Added Python 3.14 support and set as default development environment (#43).
- Updated GitHub Actions workflows to use the latest `checkout` and
  `setup-python` versions (#43).
- Refactored the logo generation script to use ImageMagick, removing the
  previous R and hexSticker dependency (#45).

## tinyvdiff 0.4.0

### Typing

- Add mypy as a development dependency and fix all mypy type checking issues (#39).

### Maintenance

- Add a GitHub Actions workflow to run mypy checks and a mypy badge to `README.md` (#40).

## tinyvdiff 0.3.9

### Maintenance

- Removed download statistics badge from `README.md` due to availability issues
  with the service (#35).
- Use Python 3.13.7 for the default package development environment (#36).

## tinyvdiff 0.3.8

### Testing

- Updated SVG snapshot files using the latest version of pdf2svg (0.2.4)
  from Homebrew so that the macOS-only snapshot tests pass correctly (#32).

## tinyvdiff 0.3.7

### Maintenance

- Use uv to manage project (#30).

## tinyvdiff 0.3.6

### Maintenance

- Changed logo typeface for a fresh look. Updated the logo text rendering
  workflow to use SVG and web browsers for better results (#28).

## tinyvdiff 0.3.5

### Maintenance

- Changed logo image path from relative to absolute URL for proper rendering
  on PyPI (#26).

## tinyvdiff 0.3.4

### Maintenance

- Use isort and ruff to sort imports and format Python code.
  Use shell-format to format shell scripts (#24).

## tinyvdiff 0.3.3

### Maintenance

- Add Python 3.13 to the list of supported Python versions and
  use it for the default package development environment (#22).
- Add badges for CI tests and mkdocs workflows to `README.md` (#23).

## tinyvdiff 0.3.2

### Documentation

- Use `pip` and `python3` in installation instructions consistently.
- Use more specific package description.

## tinyvdiff 0.3.1

### Documentation

- Added a [setup guide article](https://nanx.me/tinyvdiff/articles/setup/)
  with a demo project detailing the steps and practical considerations for
  using tinyvdiff in projects (#20).

## tinyvdiff 0.3.0

### New features

- The pytest plugin now supports multi-page PDF files.
  Each multi-page PDF will correspond to SVG snapshots with file name
  suffixes `_p1.svg`, `_p2.svg`, `...` (#15).
- Added a pytest parser option `--tinyvdiff-pdf2svg` to allow specifying a
  custom path to `pdf2svg` in test files or project-wide `conftest.py`
  when needed (#18).

### Testing

- Added unit tests for the low-level conversion and snapshotting facilities
  that support the pytest plugin (#17).

### Improvements

- Exposed key functions in `__init__.py` so that users can use the simpler
  `import tinyvdiff as tvd` and `tvd.` syntax to access them (#16).

## tinyvdiff 0.2.0

### New features

- Added a pytest plugin for visual regression testing (#11).

### Improvements

- Refactored type hints to use shorthand syntax for union and optional types.
  As a result, tinyvdiff now requires Python >= 3.10 (#4).

## tinyvdiff 0.1.0

### New features

- Implemented a wrapper for the `pdf2svg` command line tool to convert
  PDF files to SVG format.
