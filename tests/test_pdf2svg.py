from pathlib import Path

import pytest

from tinyvdiff.pdf2svg import PDF2SVG

from .snapshot_fpdf2 import generate_pdf_multi_page


@pytest.fixture
def pdf2svg():
    """Pytest fixture providing PDF2SVG instance if available on system"""
    if not PDF2SVG.is_available():
        pytest.skip("pdf2svg not available on this system")
    return PDF2SVG()


@pytest.fixture
def sample_pdf(tmp_path):
    """Pytest fixture providing a sample multi-page PDF file"""
    pdf_path = tmp_path / "test.pdf"
    return generate_pdf_multi_page(pdf_path, num_pages=2)


def test_pdf2svg_init():
    """Test PDF2SVG class initialization"""
    if not PDF2SVG.is_available():
        with pytest.raises(FileNotFoundError):
            PDF2SVG()
    else:
        converter = PDF2SVG()
        assert converter.executable_path
        assert Path(converter.executable_path).exists()


def test_pdf2svg_invalid_executable():
    """Test initialization with invalid executable path"""
    with pytest.raises(FileNotFoundError):
        PDF2SVG(executable_path="/nonexistent/pdf2svg")


def test_pdf2svg_convert_basic(pdf2svg, sample_pdf, tmp_path):
    """Test basic PDF to SVG conversion"""
    output_svg = tmp_path / "output.svg"
    result = pdf2svg.convert(sample_pdf, output_svg)

    assert result == output_svg
    assert output_svg.exists()
    assert output_svg.stat().st_size > 0


def test_pdf2svg_convert_specific_page(pdf2svg, sample_pdf, tmp_path):
    """Test converting specific page from PDF"""
    output_svg = tmp_path / "output.svg"
    result = pdf2svg.convert(sample_pdf, output_svg, page=2)

    assert result == output_svg
    assert output_svg.exists()


def test_pdf2svg_convert_invalid_page(pdf2svg, sample_pdf, tmp_path):
    """Test converting with invalid page number"""
    output_svg = tmp_path / "output.svg"
    with pytest.raises(ValueError):
        pdf2svg.convert(sample_pdf, output_svg, page=0)


def test_pdf2svg_convert_missing_input(pdf2svg, tmp_path):
    """Test converting non-existent input file"""
    with pytest.raises(FileNotFoundError):
        pdf2svg.convert(tmp_path / "nonexistent.pdf")


def test_pdf2svg_default_output(pdf2svg, sample_pdf):
    """Test conversion with default output path"""
    result = pdf2svg.convert(sample_pdf)
    expected_output = Path(sample_pdf).with_suffix(".svg")

    assert result == expected_output
    assert expected_output.exists()
    expected_output.unlink()
