# Setup guide

## The whole game

- Ensure Python and system dependency are installed in both local and remote.
- Local: produce PDF, generate SVG snapshots as ground truth,
  and store in repo.
- Remote: CI workflow can also generate reasonably similar PDF,
  convert to SVG, and compare.

## Add development dependency

Add tinyvdiff as a development dependency:

```bash
rye add --dev tinyvdiff
```

Also install it in your CI/CD workflow.

## Install pdf2svg

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

### GitHub Actions workflow

Similar. Example.

### Customize pdf2svg path

If you do not have permission to install CLI tools globally, you can customize
the location of the `pdf2svg` executable. As long as there is a user-accessible
path to the executable, tinyvdiff will work.

## Write snapshot tests

```python
import tinyvdiff as tvd
```

Where they will be stored by default. Multi-page PDF snapshot naming pattern.

## Generate snapshot

Run `pytest --...`

Then run `pytest` or `pytest tests/test_your_test.py`.

## Run in CI workflows

Commit the snapshots in version control. See if it works in remote CI workflows.

If the snapshots need to be updated, regenerate them using the same command.
