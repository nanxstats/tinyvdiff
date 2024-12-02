import re
import shutil
from pathlib import Path


def normalize_svg(svg_content: str) -> str:
    """Normalize SVG content by removing variable content.

    Removes metadata and ID attributes that may vary between runs while
    preserving the visual content of the SVG.

    Args:
        svg_content: Raw SVG file content as string.

    Returns:
        Normalized SVG content with variable content removed.
    """
    # Remove elements that may vary between runs
    svg_content = re.sub(r"<metadata>.*?</metadata>", "", svg_content, flags=re.DOTALL)
    svg_content = re.sub(r'id="[^"]+"', "", svg_content)
    return svg_content.strip()


def compare_svgs(generated_svg_path: Path | str, snapshot_svg_path: Path | str) -> bool:
    """Compare two SVG files by their normalized content.

    Args:
        generated_svg_path: Path to the newly generated SVG file.
        snapshot_svg_path: Path to the snapshot SVG file to compare against.

    Returns:
        True if the SVGs match after normalization, False otherwise.
    """
    with (
        open(generated_svg_path, "r") as gen_file,
        open(snapshot_svg_path, "r") as snap_file,
    ):
        gen_svg = normalize_svg(gen_file.read())
        snap_svg = normalize_svg(snap_file.read())
        return gen_svg == snap_svg


def update_snapshot(
    generated_svg_path: Path | str, snapshot_svg_path: Path | str
) -> None:
    """Update or create a snapshot SVG file from a generated SVG.

    Args:
        generated_svg_path: Path to the source SVG file.
        snapshot_svg_path: Path where the snapshot should be saved.
    """
    snapshot_svg_path = Path(snapshot_svg_path)
    snapshot_svg_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(generated_svg_path, snapshot_svg_path)
