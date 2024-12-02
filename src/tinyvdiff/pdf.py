from pathlib import Path

from pypdf import PdfReader


def get_pdf_page_count(pdf_path: str | Path) -> int:
    """
    Get the number of pages in a PDF file.

    Args:
        pdf_path (str | Path): Path to the PDF file.

    Returns:
        int: Number of pages in the PDF file.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        ValueError: If the file is not a valid PDF.
    """
    pdf_path = Path(pdf_path).expanduser().resolve()

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    try:
        reader = PdfReader(str(pdf_path))
        return len(reader.pages)
    except Exception as e:
        raise ValueError(f"Invalid PDF file: {pdf_path}") from e
