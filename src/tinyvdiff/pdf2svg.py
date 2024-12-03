import os
import shutil
import subprocess
from collections.abc import Sequence
from pathlib import Path

from .constants import PDF2SVG_DEFAULT_PATHS


class PDF2SVG:
    """Wrapper for the pdf2svg command line tool."""

    DEFAULT_PATHS: Sequence[str] = PDF2SVG_DEFAULT_PATHS

    def __init__(self, executable_path: str | None = None):
        """Initialize PDF2SVG wrapper.

        Args:
            executable_path: Optional path to pdf2svg executable.
                If None, will attempt to locate it.

        Raises:
            FileNotFoundError: If pdf2svg executable from the canonical
                locations can't be found, or if a custom path is provided
                but does not exist.
        """
        if executable_path:
            executable_path = str(Path(executable_path).expanduser().resolve())
            if not os.path.isfile(executable_path):
                raise FileNotFoundError(
                    f"Specified pdf2svg executable not found: {executable_path}"
                )
            self.executable_path = executable_path
        else:
            self.executable_path = self._find_executable()
            if not self.executable_path:
                raise FileNotFoundError(
                    "pdf2svg executable not found. Please install it or provide path."
                )

    def _find_executable(self) -> str | None:
        """Locate pdf2svg executable using default paths and PATH environment.

        Returns:
            Path to pdf2svg executable if found, None otherwise.
        """
        # First try PATH - this will respect the current platform
        path = shutil.which("pdf2svg")
        if path:
            return path

        # Try platform-specific default locations
        for path in self.DEFAULT_PATHS:
            expanded_path = str(Path(path).expanduser().resolve())
            if os.path.isfile(expanded_path):
                return expanded_path

        return None

    def convert(
        self,
        input_path: str | Path,
        output_path: str | Path | None = None,
        page: int | None = None,
    ) -> Path:
        """Convert PDF to SVG using pdf2svg.

        Args:
            input_path: Path to input PDF file.
            output_path: Optional path for output SVG file.
                If None, uses input path with .svg extension.
            page: Optional page number to convert (starting from 1).

        Returns:
            Path to generated SVG file

        Raises:
            subprocess.CalledProcessError: If pdf2svg conversion fails.
            ValueError: If page number is less than 1.
            FileNotFoundError: If input file doesn't exist.
        """
        input_path = Path(input_path).expanduser().resolve()
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        if output_path is None:
            output_path = input_path.with_suffix(".svg")
        else:
            output_path = Path(output_path).expanduser().resolve()

        if page is not None:
            if page < 1:
                raise ValueError("Page number must be 1 or greater")
            cmd = [self.executable_path, str(input_path), str(output_path), str(page)]
        else:
            cmd = [self.executable_path, str(input_path), str(output_path)]

        subprocess.run(cmd, check=True, capture_output=True)
        return output_path

    @classmethod
    def is_available(cls) -> bool:
        """Check if pdf2svg is available on the system.

        Returns:
            True if pdf2svg executable can be found, False otherwise.
        """
        try:
            PDF2SVG()
            return True
        except FileNotFoundError:
            return False
