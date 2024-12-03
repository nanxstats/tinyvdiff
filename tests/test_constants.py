import sys

import pytest

from tinyvdiff.constants import PDF2SVG_PATHS, _get_program_data_path


def test_pdf2svg_paths_structure():
    """Test that PDF2SVG_PATHS contains expected platform keys"""
    assert set(PDF2SVG_PATHS.keys()) == {"darwin", "linux", "win32"}


def test_platform_specific_paths():
    """Test that current platform has valid paths defined"""
    platform_paths = PDF2SVG_PATHS[sys.platform]
    assert isinstance(platform_paths, tuple)
    assert len(platform_paths) > 0
    assert all(isinstance(path, str) for path in platform_paths)


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_windows_program_data():
    """Test Windows ProgramData path resolution"""
    program_data = _get_program_data_path()
    assert isinstance(program_data, str)
    assert program_data.endswith("ProgramData")
