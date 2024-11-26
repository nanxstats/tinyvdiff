import os
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path


def _get_program_data_path() -> str:
    """Get the ProgramData path on Windows."""
    return os.environ.get("ProgramData", "C:\\ProgramData")


# OS-specific default paths for pdf2svg executable
PDF2SVG_PATHS: Mapping[str, Sequence[str]] = {
    "darwin": (
        # Homebrew Intel
        "/usr/local/bin/pdf2svg",
        # Homebrew Apple Silicon
        "/opt/homebrew/bin/pdf2svg",
        # MacPorts
        "/opt/local/bin/pdf2svg",
    ),
    "linux": (
        # Common Linux locations
        "/usr/bin/pdf2svg",
        "/usr/local/bin/pdf2svg",
        # Snap packages
        "/snap/bin/pdf2svg",
    ),
    "win32": (
        # Chocolatey
        str(Path(_get_program_data_path()) / "chocolatey" / "bin" / "pdf2svg.exe"),
        # Scoop
        str(
            Path(os.environ.get("USERPROFILE", "")) / "scoop" / "shims" / "pdf2svg.exe"
        ),
    ),
}

# Get the default paths for the current platform
PDF2SVG_DEFAULT_PATHS: Sequence[str] = PDF2SVG_PATHS.get(sys.platform, ("pdf2svg",))
