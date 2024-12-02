from pathlib import Path

import pytest
from fpdf import FPDF

from tinyvdiff.pdf import get_pdf_page_count


def create_test_pdf(output_path: Path, num_pages: int) -> Path:
    """Helper function to create a PDF with specified number of pages"""
    pdf = FPDF()
    for i in range(num_pages):
        pdf.add_page()
        pdf.set_font("times", size=16)
        pdf.text(10, 20, f"Test page {i + 1}")
    pdf.output(str(output_path))
    return output_path


def test_get_pdf_page_count_single_page(tmp_path):
    pdf_path = tmp_path / "single_page.pdf"
    create_test_pdf(pdf_path, 1)
    assert get_pdf_page_count(pdf_path) == 1


def test_get_pdf_page_count_multiple_pages(tmp_path):
    pdf_path = tmp_path / "multi_page.pdf"
    create_test_pdf(pdf_path, 5)
    assert get_pdf_page_count(pdf_path) == 5


def test_get_pdf_page_count_missing_file(tmp_path):
    pdf_path = tmp_path / "nonexistent.pdf"
    with pytest.raises(FileNotFoundError):
        get_pdf_page_count(pdf_path)


def test_get_pdf_page_count_invalid_file(tmp_path):
    invalid_pdf = tmp_path / "invalid.pdf"
    invalid_pdf.write_text("This is not a PDF file")

    with pytest.raises(ValueError):
        get_pdf_page_count(invalid_pdf)


def test_get_pdf_page_count_string_path(tmp_path):
    pdf_path = str(tmp_path / "nonexistent.pdf")
    with pytest.raises(FileNotFoundError):
        get_pdf_page_count(pdf_path)
