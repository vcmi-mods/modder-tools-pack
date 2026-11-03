#!/usr/bin/env python3
from pathlib import Path
import argparse
from PIL import Image

def load_ref_palette(path: Path) -> list[int]:
    """Load reference paletted image and return its full 256*3 palette list."""
    ref = Image.open(path)
    if ref.mode != "P":
        raise ValueError(f"Reference image must be paletted (mode P). Got {ref.mode}")
    pal = ref.getpalette()
    if len(pal) < 768:
        raise ValueError("Reference palette must have 256 entries (768 bytes)")
    return pal[:768]

def apply_ref_palette(src: Path, dst: Path, ref_palette: list[int]):
    """Convert any image to P mode with exactly the reference palette."""
    im = Image.open(src)

    # Convert source to RGB first (drop alpha)
    if im.mode != "RGB":
        im = im.convert("RGB")

    # Quantize with reference palette
    ref_img = Image.new("P", (1, 1))
    ref_img.putpalette(ref_palette)

    out = im.quantize(colors=256, method=Image.FASTOCTREE, dither=Image.NONE, palette=ref_img)

    # Force the reference palette (overwrite just in case)
    out.putpalette(ref_palette)

    out.save(dst, optimize=False)
    print(f"{src} -> {dst}")

def main():
    ap = argparse.ArgumentParser(
        description="Force-convert PNGs to use EXACT palette from a reference paletted PNG."
    )
    ap.add_argument("inputs", nargs="+", help="Files or folders to process")
    ap.add_argument("--ref-palette", required=True, help="Reference paletted PNG (e.g., button-org-ok.png)")
    ap.add_argument("--glob", default="**/*.png", help="Glob for folder input (default: **/*.png)")
    ap.add_argument("--in-place", action="store_true", help="Overwrite input files in place")
    ap.add_argument("--suffix", default="-fixed", help="Suffix for output (ignored with --in-place)")
    args = ap.parse_args()

    ref_palette = load_ref_palette(Path(args.ref_palette))

    files: list[Path] = []
    for inp in args.inputs:
        p = Path(inp)
        if p.is_dir():
            files.extend(sorted(p.glob(args.glob)))
        elif p.is_file():
            files.append(p)

    for src in files:
        dst = src if args.in_place else src.with_name(src.stem + args.suffix + src.suffix)
        apply_ref_palette(src, dst, ref_palette)

if __name__ == "__main__":
    main()
