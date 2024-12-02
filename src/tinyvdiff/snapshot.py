import re
import shutil


def normalize_svg(svg_content):
    # Remove elements that may vary between runs
    svg_content = re.sub(r"<metadata>.*?</metadata>", "", svg_content, flags=re.DOTALL)
    svg_content = re.sub(r'id="[^"]+"', "", svg_content)
    return svg_content.strip()


def compare_svgs(generated_svg_path, snapshot_svg_path):
    with (
        open(generated_svg_path, "r") as gen_file,
        open(snapshot_svg_path, "r") as snap_file,
    ):
        gen_svg = normalize_svg(gen_file.read())
        snap_svg = normalize_svg(snap_file.read())
        return gen_svg == snap_svg


def update_snapshot(generated_svg_path, snapshot_svg_path):
    snapshot_svg_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(generated_svg_path, snapshot_svg_path)
