from pathlib import Path

import pytest

from .pdf import get_pdf_page_count
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
    parser.addoption(
        "--tinyvdiff-pdf2svg",
        default=None,
        help="Path to a custom pdf2svg executable.",
    )


class TinyVDiff:
    """Helper class for visual regression testing with PDFs."""

    def __init__(self, request: pytest.FixtureRequest) -> None:
        """Initialize TinyVDiff with configuration from pytest."""
        pdf2svg_path = request.config.getoption("--tinyvdiff-pdf2svg")
        self.pdf2svg = PDF2SVG(executable_path=pdf2svg_path)
        self.update_snapshots = request.config.getoption("--tinyvdiff-update")
        # Determine the snapshot directory relative to the test file
        self.snapshot_dir = Path(request.node.fspath).parent / "snapshots"

    def assert_pdf_snapshot(self, pdf_path: Path | str, snapshot_name: str) -> None:
        """Assert that a PDF matches its stored snapshot.

        Converts each page of the PDF to SVG and compares it with stored
        snapshots, updating the snapshots if requested via `--tinyvdiff-update`.

        Args:
            pdf_path: Path to the PDF file to test.
            snapshot_name: Base name for the snapshot files.
                For multi-page PDFs, page number will be inserted before file
                extension. For example, a two-page `test.pdf` becomes
                `test_p1.svg` and `test_p2.svg`.

        Raises:
            pytest.Failed: If snapshots do not match and updates are not enabled.
        """
        num_pages = get_pdf_page_count(pdf_path)
        if num_pages == 0:
            pytest.fail(f"PDF file has no pages: {pdf_path}")

        # Split snapshot name into base and extension for multi-page handling
        snapshot_base = Path(snapshot_name)
        snapshot_stem = snapshot_base.stem
        snapshot_suffix = snapshot_base.suffix

        for page in range(1, num_pages + 1):
            # Generate page-specific snapshot name
            page_snapshot_name = (
                f"{snapshot_stem}_p{page}{snapshot_suffix}"
                if num_pages > 1
                else snapshot_name
            )
            snapshot_path = self.snapshot_dir / page_snapshot_name

            # Convert specific PDF page to SVG
            svg_generated = self.pdf2svg.convert(pdf_path, page=page)

            if self.update_snapshots or not snapshot_path.exists():
                update_snapshot(svg_generated, snapshot_path)
            else:
                if not compare_svgs(svg_generated, snapshot_path):
                    pytest.fail(f"Snapshot mismatch for {page_snapshot_name}")


@pytest.fixture
def tinyvdiff(request: pytest.FixtureRequest) -> TinyVDiff:
    """Pytest fixture providing TinyVDiff functionality.

    Args:
        request: Pytest fixture request object.

    Returns:
        Configured TinyVDiff instance for the current test.
    """
    return TinyVDiff(request)
