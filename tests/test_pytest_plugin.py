import platform
import uuid
from pathlib import Path

import pytest

from .snapshot_fpdf2 import data, generate_pdf_multi_page, generate_pdf_single_page
from .snapshot_matplotlib import generate_plot

macos_only = pytest.mark.skipif(
    platform.system() != "Darwin", reason="These snapshots are generated on macOS"
)


@pytest.fixture
def temp_pdf(tmp_path):
    """Fixture to create a temporary PDF file path"""
    return tmp_path / "test.pdf"


@macos_only
def test_matplotlib_visual(tinyvdiff, temp_pdf):
    """Test visual regression with single-page PDF generated with matplotlib"""
    pdf_path = generate_plot(temp_pdf)
    tinyvdiff.assert_pdf_snapshot(pdf_path, "snapshot_matplotlib.svg")


@macos_only
def test_fpdf2_single_page_visual(tinyvdiff, temp_pdf):
    """Test visual regression with single-page PDF generated with fpdf2"""
    pdf_path = generate_pdf_single_page(data, temp_pdf)
    tinyvdiff.assert_pdf_snapshot(pdf_path, "snapshot_fpdf2.svg")


@macos_only
def test_fpdf2_multi_page_visual(tinyvdiff, temp_pdf):
    """Test visual regression with multi-page PDF generated with fpdf2"""
    pdf_path = generate_pdf_multi_page(temp_pdf, num_pages=3)
    snapshot_name = "snapshot_multipage.svg"

    # First run should create snapshots
    tinyvdiff.assert_pdf_snapshot(pdf_path, snapshot_name)

    # Verify that all page snapshots were created
    for i in range(1, 4):
        snapshot_path = Path(tinyvdiff.snapshot_dir) / f"snapshot_multipage_p{i}.svg"
        assert snapshot_path.exists()
        snapshot_path.unlink()


@macos_only
def test_fpdf2_multi_page_mismatch(tinyvdiff, temp_pdf):
    """Test that mismatches are detected in multi-page PDFs generated with fpdf2"""
    # Create initial PDF and snapshot
    pdf_path = generate_pdf_multi_page(temp_pdf, num_pages=2)
    snapshot_name = f"test_mismatch_multi_{uuid.uuid4()}.svg"

    tinyvdiff.update_snapshots = True
    tinyvdiff.assert_pdf_snapshot(pdf_path, snapshot_name)
    tinyvdiff.update_snapshots = False

    # Create different PDF with same number of pages
    different_pdf = generate_pdf_multi_page(
        temp_pdf, num_pages=2, content_prefix="Different"
    )

    # Should fail due to content mismatch
    with pytest.raises(pytest.fail.Exception):
        tinyvdiff.assert_pdf_snapshot(different_pdf, snapshot_name)

    # Clean up snapshot files
    for i in range(1, 3):
        snapshot_path = (
            Path(tinyvdiff.snapshot_dir)
            / f"{Path(snapshot_name).stem}_p{i}{Path(snapshot_name).suffix}"
        )
        snapshot_path.unlink()


def test_missing_snapshot(tinyvdiff, temp_pdf):
    """Test behavior when snapshot doesn't exist"""
    pdf_path = generate_plot(temp_pdf)
    snapshot_name = f"temp_snapshot_{uuid.uuid4()}.svg"

    # Should create new snapshot if it doesn't exist
    tinyvdiff.assert_pdf_snapshot(pdf_path, snapshot_name)

    # Verify snapshot was created and clean it up
    snapshot_path = Path(tinyvdiff.snapshot_dir) / snapshot_name
    assert snapshot_path.exists()
    snapshot_path.unlink()


def test_update_snapshot(tinyvdiff, tmp_path):
    """Test snapshot update functionality"""
    # Create a fixed snapshot name
    test_uuid = uuid.uuid4()
    snapshot_name = f"test_update_{test_uuid}.svg"

    # Create two different temporary PDF paths
    original_pdf = tmp_path / "original.pdf"
    updated_pdf = tmp_path / "updated.pdf"

    # First generate and save a snapshot with original data
    pdf_path = generate_pdf_single_page(data, original_pdf)
    tinyvdiff.assert_pdf_snapshot(pdf_path, snapshot_name)

    # Generate a different PDF and update snapshot with --tinyvdiff-update flag
    updated_data = [["Updated", "Header"], ["Updated", "Data"]]
    tinyvdiff.update_snapshots = True
    new_pdf_path = generate_pdf_single_page(updated_data, updated_pdf)
    tinyvdiff.assert_pdf_snapshot(new_pdf_path, snapshot_name)
    tinyvdiff.update_snapshots = False  # Reset update flag

    # Verify that the snapshot matches the updated version
    tinyvdiff.assert_pdf_snapshot(new_pdf_path, snapshot_name)

    # Verify that it doesn't match the original version
    with pytest.raises(pytest.fail.Exception):
        tinyvdiff.assert_pdf_snapshot(pdf_path, snapshot_name)

    # Clean up snapshot file
    snapshot_file = Path(tinyvdiff.snapshot_dir) / snapshot_name
    snapshot_file.unlink()


def test_snapshot_mismatch(tinyvdiff, temp_pdf):
    """Test that mismatched snapshots are detected"""
    # First generate and save a snapshot using original data
    pdf_path = generate_pdf_single_page(data, temp_pdf)
    snapshot_name = "test_mismatch.svg"

    # Force update for the first snapshot
    tinyvdiff.update_snapshots = True
    tinyvdiff.assert_pdf_snapshot(pdf_path, snapshot_name)
    tinyvdiff.update_snapshots = False  # Reset update flag

    # Generate different data that should cause a mismatch
    different_data = [
        ["Different", "Header", "Here"],
        ["Different", "Data", "Row"],
    ]
    different_pdf = generate_pdf_single_page(different_data, temp_pdf)

    # Test should fail due to mismatch
    with pytest.raises(pytest.fail.Exception):
        tinyvdiff.assert_pdf_snapshot(different_pdf, snapshot_name)

    # Clean up snapshot file
    snapshot_file = Path(tinyvdiff.snapshot_dir) / snapshot_name
    snapshot_file.unlink()
