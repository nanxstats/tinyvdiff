"""
tinyvdiff - Minimalist visual regression testing plugin for pytest
"""

from .pdf import get_pdf_page_count
from .pdf2svg import PDF2SVG
from .pytest_plugin import TinyVDiff
from .snapshot import compare_svgs, normalize_svg, update_snapshot
