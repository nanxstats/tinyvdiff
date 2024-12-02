from pathlib import Path

import pytest

from .pdf2svg import PDF2SVG
from .snapshot import compare_svgs, update_snapshot


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add tinyvdiff command line options to pytest.

    Args:
        parser: pytest command line parser to extend.
    """
    parser.addoption(
        "--tinyvdiff-update",
        action="store_true",
        default=False,
        help="Update visual regression snapshots.",
    )


@pytest.fixture
def tinyvdiff(request: pytest.FixtureRequest) -> "TinyVDiff":
    """Pytest fixture providing TinyVDiff functionality.

    Args:
        request: Pytest fixture request object.

    Returns:
        Configured TinyVDiff instance for the current test.
    """

    class TinyVDiff:
        """Helper class for visual regression testing with PDFs."""

        def __init__(self) -> None:
            """Initialize TinyVDiff with configuration from pytest."""
            self.pdf2svg = PDF2SVG()
            self.update_snapshots = request.config.getoption("--tinyvdiff-update")
            # Determine the snapshot directory relative to the test file
            self.snapshot_dir = Path(request.node.fspath).parent / "snapshots"

        def assert_pdf_snapshot(self, pdf_path: Path | str, snapshot_name: str) -> None:
            """Assert that a PDF matches its stored snapshot.

            Converts the PDF to SVG and compares it with a stored snapshot,
            updating the snapshot if requested via `--tinyvdiff-update`.

            Args:
                pdf_path: Path to the PDF file to test.
                snapshot_name: Name of the snapshot file to compare against.

            Raises:
                pytest.Failed: If snapshots don't match and updates aren't enabled.
            """
            # Convert PDF to SVG
            svg_generated = self.pdf2svg.convert(pdf_path)
            snapshot_path = self.snapshot_dir / snapshot_name

            if self.update_snapshots or not snapshot_path.exists():
                update_snapshot(svg_generated, snapshot_path)
            else:
                if not compare_svgs(svg_generated, snapshot_path):
                    pytest.fail(f"Snapshot mismatch for {snapshot_name}")

    return TinyVDiff()
