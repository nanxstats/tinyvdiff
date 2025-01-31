# Changelog

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
