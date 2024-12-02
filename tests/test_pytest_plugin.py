from pathlib import Path
import platform
import uuid

import pytest

from .snapshot_matplotlib import generate_plot
from .snapshot_fpdf2 import generate_fpdf2, data

macos_only = pytest.mark.skipif(
    platform.system() != "Darwin", reason="These snapshots are generated on macOS"
)


@pytest.fixture
def temp_pdf(tmp_path):
    """Fixture to create a temporary PDF file path"""
    return tmp_path / "test.pdf"


@macos_only
def test_matplotlib_visual(tinyvdiff, temp_pdf):
    """Test visual regression with matplotlib-generated PDF"""
    pdf_path = generate_plot(temp_pdf)
    tinyvdiff.assert_pdf_snapshot(pdf_path, "snapshot_matplotlib.svg")


@macos_only
def test_fpdf_visual(tinyvdiff, temp_pdf):
    """Test visual regression with fpdf2-generated PDF"""
    pdf_path = generate_fpdf2(data, temp_pdf)
    tinyvdiff.assert_pdf_snapshot(pdf_path, "snapshot_fpdf2.svg")


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

    # First generate and save a snapshot with fpdf2 data
    pdf_path = generate_fpdf2(data, original_pdf)
    tinyvdiff.assert_pdf_snapshot(pdf_path, snapshot_name)

    # Generate a different PDF and update snapshot with --tinyvdiff-update flag
    updated_data = [["Updated", "Header"], ["Updated", "Data"]]
    tinyvdiff.update_snapshots = True
    new_pdf_path = generate_fpdf2(updated_data, updated_pdf)
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
    # First generate and save a snapshot using fpdf2 data
    pdf_path = generate_fpdf2(data, temp_pdf)
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
    different_pdf = generate_fpdf2(different_data, temp_pdf)

    # Test should fail due to mismatch
    with pytest.raises(pytest.fail.Exception):
        tinyvdiff.assert_pdf_snapshot(different_pdf, snapshot_name)

    # Clean up snapshot file
    snapshot_file = Path(tinyvdiff.snapshot_dir) / snapshot_name
    snapshot_file.unlink()
