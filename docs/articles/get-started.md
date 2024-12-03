# Get started


<!-- `.md` and `.py` files are generated from the `.qmd` file. Please edit that file. -->

!!! tip

    To run the code from this article as a Python script:

    ```bash
    python3 examples/get-started.py
    ```

## Import tinyvdiff

``` python
from tinyvdiff.pdf2svg import PDF2SVG
```

## System dependency

tinyvdiff requires the `pdf2svg` command line tool. The easiest way to
make `pdf2svg` available is to install it via these commands using
package managers.

On macOS (using Homebrew):

``` bash
brew install pdf2svg
```

On Ubuntu:

``` bash
sudo apt-get install pdf2svg
```

On Windows (using Chocolatey):

``` bash
choco install pdf2svg-win
```

If you do not have permission to install CLI tools globally, you can
customize the location of the `pdf2svg` executable. As long as there is
a user-accessible path to the executable, tinyvdiff will work.
