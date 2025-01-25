import pytest

from tinyvdiff.snapshot import compare_svgs, normalize_svg, update_snapshot


@pytest.fixture
def sample_svg_content():
    """Pytest fixture providing sample SVG content"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg id="unique_123" width="100" height="100">
    <metadata>
        <created>2024-12-02</created>
    </metadata>
    <rect id="rect_456" x="10" y="10" width="80" height="80"/>
</svg>"""


@pytest.fixture
def sample_svg_file(tmp_path, sample_svg_content):
    """Pytest fixture providing a sample SVG file"""
    svg_file = tmp_path / "test.svg"
    svg_file.write_text(sample_svg_content)
    return svg_file


def test_normalize_svg_removes_metadata(sample_svg_content):
    """Test that normalize_svg removes metadata elements"""
    normalized = normalize_svg(sample_svg_content)
    assert "<metadata>" not in normalized
    assert "<created>2024-03-20</created>" not in normalized


def test_normalize_svg_removes_ids(sample_svg_content):
    """Test that normalize_svg removes ID attributes"""
    normalized = normalize_svg(sample_svg_content)
    assert 'id="unique_123"' not in normalized
    assert 'id="rect_456"' not in normalized


def test_normalize_svg_preserves_structure(sample_svg_content):
    """Test that normalize_svg preserves essential SVG structure"""
    normalized = normalize_svg(sample_svg_content)
    assert "<svg" in normalized
    assert "<rect" in normalized
    assert 'width="100"' in normalized
    assert 'height="100"' in normalized


def test_compare_svgs_identical(tmp_path, sample_svg_content):
    """Test comparing identical SVGs"""
    svg1 = tmp_path / "svg1.svg"
    svg2 = tmp_path / "svg2.svg"

    svg1.write_text(sample_svg_content)
    svg2.write_text(sample_svg_content)

    assert compare_svgs(svg1, svg2)


def test_compare_svgs_different_ids(tmp_path, sample_svg_content):
    """Test comparing SVGs with different IDs but same content"""
    svg1 = tmp_path / "svg1.svg"
    svg2 = tmp_path / "svg2.svg"

    svg1.write_text(sample_svg_content)
    modified_content = sample_svg_content.replace(
        'id="unique_123"', 'id="different_123"'
    )
    svg2.write_text(modified_content)

    assert compare_svgs(svg1, svg2)


def test_compare_svgs_different_content(tmp_path, sample_svg_content):
    """Test comparing SVGs with different content"""
    svg1 = tmp_path / "svg1.svg"
    svg2 = tmp_path / "svg2.svg"

    svg1.write_text(sample_svg_content)
    modified_content = sample_svg_content.replace('width="80"', 'width="90"')
    svg2.write_text(modified_content)

    assert not compare_svgs(svg1, svg2)


def test_update_snapshot(tmp_path, sample_svg_content):
    """Test updating snapshot file"""
    source = tmp_path / "source.svg"
    snapshot = tmp_path / "snapshots" / "test.svg"

    source.write_text(sample_svg_content)
    update_snapshot(source, snapshot)

    assert snapshot.exists()
    assert snapshot.read_text() == sample_svg_content


def test_update_snapshot_creates_dirs(tmp_path, sample_svg_content):
    """Test that update_snapshot creates necessary directories"""
    source = tmp_path / "source.svg"
    snapshot = tmp_path / "nested" / "directory" / "test.svg"

    source.write_text(sample_svg_content)
    update_snapshot(source, snapshot)

    assert snapshot.exists()
    assert snapshot.read_text() == sample_svg_content
