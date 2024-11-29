# tinyvdiff <img src="docs/assets/logo.png" align="right" width="120" />

[![PyPI version](https://img.shields.io/pypi/v/tinyvdiff)](https://pypi.org/project/tinyvdiff/)
![Python versions](https://img.shields.io/pypi/pyversions/tinyvdiff)
[![PyPI Downloads](https://img.shields.io/pypi/dm/tinyvdiff)](https://pypistats.org/packages/tinyvdiff)
![License](https://img.shields.io/pypi/l/tinyvdiff)

Minimalist visual regression testing helpers.

## Installation

You can install tinyvdiff from PyPI:

```bash
pip3 install tinyvdiff
```

Or install the development version from GitHub:

```bash
git clone https://github.com/nanxstats/tinyvdiff.git
cd tinyvdiff
python3 -m pip install -e .
```

## System dependency

tinyvdiff requires the `pdf2svg` command line tool.
The easiest way to make `pdf2svg` available is to install it via these commands
using package managers.

On macOS (using Homebrew):

```bash
brew install pdf2svg
```

On Ubuntu:

```bash
sudo apt-get install pdf2svg
```

On Windows (using Chocolatey):

```bash
choco install pdf2svg-win
```

If you do not have permission to install CLI tools globally, you can customize
the location of the `pdf2svg` executable. As long as there is a user-accessible
path to the executable, tinyvdiff will work.

## Why tinyvdiff?

Designing a visual regression testing framework involves balancing several
competing challenges, particularly when it comes to the snapshot file format
used for comparisons. The ideal format must meet three seemingly conflicting
criteria:

1. **Support for diverse input types:** Graphics and documents are often
   generated using different tools and formats (for example, PNG and PDF),
   making direct comparisons difficult.
2. **Bitwise reproducibility in plain text:** The format should capture the
   precise appearance of the output while being deterministic and easy to
   inspect visually.
3. **Platform independence:** Subtle differences in system fonts or
   dependencies can lead to inconsistent outputs across environments,
   yet the format should produce visually identical results on any system.

## How tinyvdiff works

tinyvdiff takes a pragmatic approach by relaxing the third criterion and
making reasonable assumptions about the first to deliver a simple yet
effective solution:

1. Input files must be in **vector PDF** format, which are then converted to
   **vector SVG** snapshots, leaving it to developers to choose the tools
   and workflows for generating the PDFs.
2. PDFs are converted to **vector SVG** using `pdf2svg` for comparison.
3. We assume it is sufficient to run visual regression tests in a single
   CI/CD operating system environment. Snapshots should be generated in a
   similar OS environment to ensure consistency with the CI/CD system.
