# Setup guide

!!! tip

    A project demonstrating most of the setups in this guide is available
    from this GitHub repository: <https://github.com/nanxstats/tinyvdiff-demo>.

## Overview

Setting up tinyvdiff for your project is similar to using other
pytest plugins. In this guide, we will describe the key steps and
the important details.

- Install Python dependency and system dependency in both
  local development environment and CI/CD environment.

- In the development envirnment:

    - Write tests that produces (stable) PDF outputs.
    - Run `pytest --tinyvdiff-update` to generate SVG snapshots as ground truth.
    - Track the snapshots in version control.

- In CI/CD workflows:

    - Select an operating system to run these tests. It should produce
      technically similar PDF outputs to those from the development environment.
    - Run `pytest` to compare the live results to the snapshot SVGs.

This guide assumes you use **pytest** in your project and the CI/CD workflow
already works.

## Install tinyvdiff

Add and install tinyvdiff as a development dependency. If you use Rye:

```bash
rye add --dev tinyvdiff
```

Next, install tinyvdiff in your CI/CD workflow. This could vary depending on
how your workflow adds/installs Python dependencies. One canonical way
is to install from PyPI:

```bash
pip install tinyvdiff
```

## Install pdf2svg

tinyvdiff requires the `pdf2svg` command line tool to convert PDF to SVG.
The easiest way to make `pdf2svg` available locally is to install it via
these commands.

On macOS (using Homebrew):

```bash
brew install pdf2svg
```

On Debian/Ubuntu:

```bash
sudo apt-get install pdf2svg
```

On Windows (using Chocolatey):

```bash
choco install pdf2svg-win
```

You can use exactly the same commands to install `pdf2svg` in your
GitHub Actions workflows. See [customizing GitHub-hosted
runners](https://docs.github.com/en/actions/using-github-hosted-runners/using-github-hosted-runners/customizing-github-hosted-runners).

## Write snapshot tests

Assume your function can already generate (technically) reproducible PDF
outputs. You can then write snapshot tests for it with pytest and tinyvdiff.
An example test looks like this:

```python
import pytest

from tinyvdiff_demo.matplotlib import generate_plot


@pytest.fixture
def temp_pdf(tmp_path):
    """Fixture to create a temporary PDF file path"""
    return tmp_path / "test.pdf"


def test_matplotlib_visual(tinyvdiff, temp_pdf):
    """Test visual regression with PDF generated with matplotlib"""
    pdf_path = generate_plot(temp_pdf)
    tinyvdiff.assert_pdf_snapshot(pdf_path, "snapshot_matplotlib.svg")
```

The tests normally lives in `tests/test_*.py`.

## Generate snapshots

To generate the snapshots, run this command in terminal:

```bash
pytest --tinyvdiff-update
```

The snapshots will be stored in `tests/snapshots/` by default.
Both single-page and multi-page PDF inputs are supported.
For multi-page PDFs, a two-page PDF with the target snapshot name
`snapshot_example.svg` will become `snapshot_example_p1.svg` and
`snapshot_example_p2.svg`.

If the snapshots need to be updated, regenerate them using the same command.

After the snapshots are ready, run `pytest` or `pytest tests/test_*.py`
in terminal to check whether the tests can pass.

## Run on CI/CD

Commit and push the snapshots to the remote repository.
See if the tests can pass in CI/CD workflows.

To emphasize our assumption: any subtle differences, such as OS version,
system fonts, or dependencies can lead to inconsistent SVG outputs,
so make sure the environment that generates the snapshots is as similar
as the CI/CD environment. Or, use the strategy detailed in the last
two sections of this guide.

## Custom pdf2svg path

If you do not have permission to install `pdf2svg` globally, you can customize
the location of the `pdf2svg` executable for the pytest plugin.

For example, you can run tests with the `--tinyvdiff-pdf2svg` option:

```bash
pytest --tinyvdiff-pdf2svg=/custom/path/pdf2svg
```

Or, apply the custom path using [pytest configuration
files](https://docs.pytest.org/en/stable/reference/customize.html).

## Use snapshots from CI/CD

Sometimes, it is challenging to pinpoint the source of technical differences
between the snapshots generated by the CI/CD runner and local development
environment. Say, you have confirmed that the apperance of the snapshots from
the runner is accurate - you can let the runner update the snapshots,
download the snapshots as artifacts, and use them as reference snapshots
in the repository directly. For example, in a GitHub Actions workflow:

```yaml
jobs:
    steps:
      - name: Test with pytest
        run: |
          pytest --tinyvdiff-update
      - name: Upload snapshot artifacts
        uses: actions/upload-artifact@v4
        with:
          name: test-snapshots-py${{ matrix.python-version }}
          path: tests/snapshots/
```

Run the workflow and download the artifacts from the job outputs page,
where a download URL will be provided in the "upload snapshot artifacts" step.

You may also want to limit these tests to only run on the CI/CD platform as below.

!!!note

    You can also do this the other way around: use the local platform
    snapshots as reference, and only run these tests locally while skipping
    them in CI/CD. This might be a simpler solution especially if you value
    running tests locally and running them often.

## Skip tests except for targeted platform

Running visual regression tests conditionally on only one platform is useful,
especially if:

- Your selected CI/CD platform is different from your local development platform.
- The snapshots generated by the two platforms are different and
  are difficult to align.
- You have decided to use the snapshots generated by the CI/CD platform
  (or the local platform) as reference snapshots.

For example, skip the tests except when running on Linux:

```python
import platform

skip_if_not_linux = pytest.mark.skipif(
    platform.system() != "Linux", reason="These tests only run on Linux"
)

@skip_if_not_linux
def test_matplotlib_visual(tinyvdiff, temp_pdf):
    ...
```