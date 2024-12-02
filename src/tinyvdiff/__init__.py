"""
tinyvdiff - Minimalist visual regression testing helpers
"""

from .pdf import get_pdf_page_count
from .pdf2svg import PDF2SVG
from .pytest_plugin import TinyVDiff
from .snapshot import normalize_svg, compare_svgs, update_snapshot
