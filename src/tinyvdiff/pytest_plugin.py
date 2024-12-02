from pathlib import Path

import pytest

from .pdf2svg import PDF2SVG
from .snapshot import compare_svgs, update_snapshot


def pytest_addoption(parser):
    parser.addoption(
        "--tinyvdiff-update",
        action="store_true",
        default=False,
        help="Update visual regression snapshots.",
    )


@pytest.fixture
def tinyvdiff(request):
    class TinyVDiff:
        def __init__(self):
            self.pdf2svg = PDF2SVG()
            self.update_snapshots = request.config.getoption("--tinyvdiff-update")
            # Determine the snapshot directory relative to the test file
            self.snapshot_dir = Path(request.node.fspath).parent / "snapshots"

        def assert_pdf_snapshot(self, pdf_path, snapshot_name):
            # Convert PDF to SVG
            svg_generated = self.pdf2svg.convert(pdf_path)
            snapshot_path = self.snapshot_dir / snapshot_name

            if self.update_snapshots or not snapshot_path.exists():
                update_snapshot(svg_generated, snapshot_path)
            else:
                if not compare_svgs(svg_generated, snapshot_path):
                    pytest.fail(f"Snapshot mismatch for {snapshot_name}")

    return TinyVDiff()
