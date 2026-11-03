#!/usr/bin/env python3

import argparse
import json
import logging
import os
import shutil
import struct
import sys
import tempfile
import warnings
from pathlib import Path
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilenames

from PIL import Image
from homm3data import deffile

TILE_SIZE = 32

logger_initialized = False
log_path = Path.cwd() / "def2json.log"


def ensure_logger():
    global logger_initialized
    if not logger_initialized:
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format='[%(levelname)s] %(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        logger_initialized = True


def custom_warning(message, category, filename, lineno, file=None, line=None):
    ensure_logger()
    logging.warning(f"{filename}:{lineno} {category.__name__}: {message}")


warnings.showwarning = custom_warning


def detect_format(path):
    with open(path, "rb") as f:
        magic = struct.unpack("<I", f.read(4))[0]
        return "d32" if magic == 0x46323344 else "def"


def generate_overlay_from_overlay_colors(img: Image.Image) -> Image.Image | None:
    overlay_colors = [(255, 255, 0), (0, 255, 0)]
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    pixels = img.load()
    overlay_pixels = overlay.load()
    found = False

    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if (r, g, b) in overlay_colors and a > 0:
                overlay_pixels[x, y] = (255, 255, 255, 255)
                found = True

    return overlay if found else None


def tile_edges(length: int, tile_size: int = TILE_SIZE):
    """Return tile boundaries for a grid anchored at the bottom/right edge."""
    if length <= 0:
        return [0]
    leading_size = length % tile_size
    edges = [0]
    if leading_size:
        edges.append(leading_size)
    while edges[-1] < length:
        edges.append(min(edges[-1] + tile_size, length))
    return edges


def find_alpha_bbox_tiles(img: Image.Image, tile_size: int = TILE_SIZE, min_visible_pixels: int = 8):
    x_edges = tile_edges(img.width, tile_size)
    y_edges = tile_edges(img.height, tile_size)
    stats = collect_tile_stats(img, 0, 0, len(x_edges) - 2, len(y_edges) - 2, tile_size)
    occupied = detect_occupied_tiles(stats, min_visible_pixels)
    occupied_positions = [
        (x, y)
        for y, row in enumerate(occupied)
        for x, is_occupied in enumerate(row)
        if is_occupied
    ]
    if not occupied_positions:
        raise ValueError(
            f"Image has no tile containing at least {min_visible_pixels} visible pixels."
        )

    xs, ys = zip(*occupied_positions)
    return min(xs), min(ys), max(xs), max(ys)


def collect_tile_stats(img: Image.Image, tile_left: int, tile_top: int, tile_right: int, tile_bottom: int, tile_size: int = TILE_SIZE):
    alpha = img.getchannel("A")
    x_edges = tile_edges(img.width, tile_size)
    y_edges = tile_edges(img.height, tile_size)
    stats = []

    for ty in range(tile_top, tile_bottom + 1):
        row = []
        for tx in range(tile_left, tile_right + 1):
            x0, x1 = x_edges[tx], x_edges[tx + 1]
            y0, y1 = y_edges[ty], y_edges[ty + 1]
            lower_y = y0 + (y1 - y0) // 2
            visible_pixels = sum(alpha.crop((x0, y0, x1, y1)).histogram()[1:])
            lower_half_pixels = sum(alpha.crop((x0, lower_y, x1, y1)).histogram()[1:])

            row.append({
                "visible_pixels": visible_pixels,
                "lower_half_pixels": lower_half_pixels
            })
        stats.append(row)

    return stats


def detect_occupied_tiles(stats, min_visible_pixels: int = 8):
    return [[cell["visible_pixels"] >= min_visible_pixels for cell in row] for row in stats]


def find_bottom_row(occupied):
    for y in range(len(occupied) - 1, -1, -1):
        if any(occupied[y]):
            return y
    return None


def choose_active_tile(stats, occupied):
    bottom_row = find_bottom_row(occupied)
    if bottom_row is None:
        raise ValueError("No occupied tiles detected.")

    width = len(occupied[0])
    center_x = (width - 1) / 2.0
    best_score = None
    best_pos = None

    for x in range(width):
        if not occupied[bottom_row][x]:
            continue

        cell = stats[bottom_row][x]
        score = cell["lower_half_pixels"] * 10 + cell["visible_pixels"] * 2 - abs(x - center_x) * 5

        if best_score is None or score > best_score:
            best_score = score
            best_pos = (x, bottom_row)

    if best_pos is None:
        raise ValueError("Could not determine active tile.")

    return best_pos


def build_vcmi_mask(occupied, active_tile):
    height = len(occupied)
    width = len(occupied[0])
    ax, ay = active_tile

    mask = [["0" for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            if not occupied[y][x]:
                continue
            if (x, y) == (ax, ay):
                mask[y][x] = "A"
            elif y == ay:
                mask[y][x] = "B"
            else:
                mask[y][x] = "V"

    for y in range(height):
        for x in range(width):
            if occupied[y][x]:
                continue
            has_visible_above = any(occupied[yy][x] for yy in range(0, y))
            if not has_visible_above or y > ay:
                continue
            nearest_above = None
            for yy in range(y - 1, -1, -1):
                if occupied[yy][x]:
                    nearest_above = yy
                    break
            if nearest_above is not None and (y - nearest_above) <= 2:
                mask[y][x] = "H"

    while mask and all(ch == "0" for ch in mask[0]):
        mask.pop(0)
    while mask and mask[0] and all(row[0] == "0" for row in mask):
        mask = [row[1:] for row in mask]
    while mask and all(ch == "0" for ch in mask[-1]):
        mask.pop()
    while mask and mask[0] and all(row[-1] == "0" for row in mask):
        mask = [row[:-1] for row in mask]

    return ["".join(row) for row in mask]


def build_default_visitable_from():
    return ["---", "+++", "+++"]


def generate_vcmi_template_from_png(png_source, animation_name=None, animation_extension="def"):
    if isinstance(png_source, Image.Image):
        img = png_source.convert("RGBA")
        source_stem = animation_name or "animation"
    else:
        img = Image.open(png_source).convert("RGBA")
        source_stem = Path(png_source).stem
    tile_left, tile_top, tile_right, tile_bottom = find_alpha_bbox_tiles(img)
    stats = collect_tile_stats(img, tile_left, tile_top, tile_right, tile_bottom)
    occupied = detect_occupied_tiles(stats)
    active_tile = choose_active_tile(stats, occupied)
    mask = build_vcmi_mask(occupied, active_tile)

    stem = source_stem.upper()
    object_name = (animation_name or stem).upper()
    animation_file = f"{object_name}.{animation_extension.lower()}"

    return {
        object_name: {
            "animation": animation_file,
            "editorAnimation": animation_file,
            "visitableFrom": build_default_visitable_from(),
            "mask": mask
        }
    }


def export_frame_images(d, filetype, output_dir, only_config=False, ignore_filename=False, ignore_group=False, merge_shadow=False, overlay_from_colours=False, template_frame=None):
    images = []
    exported_frames = []
    template_image = None
    global_frame_index = 0
    filename_counts = {}

    for group in d.get_groups():
        frame_count = d.get_frame_count(group)
        filename_counts[group] = 0

        for frame in range(frame_count):
            real_group = group if filetype == "def" else 0
            real_frame = frame

            if ignore_group and ignore_filename:
                image_name = f"0_{global_frame_index}"
            elif ignore_group:
                image_name = f"0_{d.get_image_name(group, frame)}"
            elif ignore_filename:
                image_name = f"{group}_{filename_counts[group]}"
            else:
                image_name = d.get_image_name(group, frame)

            entry = {
                "group": real_group,
                "frame": global_frame_index if filetype == "d32" else real_frame,
                "file": f"{image_name}.png"
            }

            try:
                if not only_config:
                    if filetype == "def":
                        normal_img = d.read_image("normal", group, frame)
                        if normal_img is None:
                            raise ValueError("Normal image is missing")
                        if global_frame_index == template_frame:
                            template_image = normal_img.copy()
                        shadow_img = None if merge_shadow else d.read_image("shadow", group, frame)
                        overlay_img = d.read_image("overlay", group, frame)

                        png_path = os.path.join(output_dir, f"{image_name}.png")
                        if merge_shadow:
                            combined = d.read_image("combined", group, frame)
                            if combined is None:
                                raise ValueError("Combined normal/shadow image is missing")
                            combined.save(png_path)
                        else:
                            normal_img.save(png_path)
                            if shadow_img:
                                shadow_img.save(os.path.join(output_dir, f"{image_name}-shadow.png"))

                        if overlay_img:
                            overlay_img.save(os.path.join(output_dir, f"{image_name}-overlay.png"))
                        elif overlay_from_colours and normal_img:
                            generated_overlay = generate_overlay_from_overlay_colors(normal_img)
                            if generated_overlay:
                                generated_overlay.save(os.path.join(output_dir, f"{image_name}-overlay.png"))

                    elif filetype == "d32":
                        img = d.read_image("normal", group, frame)
                        if img is None:
                            raise ValueError("Image is None (possibly invalid dimensions)")
                        if global_frame_index == template_frame:
                            template_image = img.copy()

                        png_path = os.path.join(output_dir, f"{image_name}.png")
                        img.save(png_path)

                        if overlay_from_colours:
                            overlay = generate_overlay_from_overlay_colors(img)
                            if overlay:
                                overlay.save(os.path.join(output_dir, f"{image_name}-overlay.png"))

                images.append(entry)
                exported_frames.append(not only_config)

            except Exception as e:
                ensure_logger()
                errmsg = f"Failed to process group {group}, frame {frame}: {e}"
                logging.error(errmsg)
                print(f"[ERROR] {errmsg}")
                exported_frames.append(False)

            filename_counts[group] += 1
            global_frame_index += 1

    return images, exported_frames, template_image


def process_def_file(path, filetype, only_config=False, ignore_filename=False, ignore_group=False, merge_shadow=False, overlay_from_colours=False, vcmi_template=False, template_frame=0, mask_only=False):
    foldername = os.path.dirname(path)
    filename = os.path.basename(path)
    stem = Path(filename).stem
    output_dir = os.path.join(foldername, stem)

    temp_dir_obj = None
    export_dir = output_dir
    if mask_only:
        temp_dir_obj = tempfile.TemporaryDirectory(prefix=f"{stem}_", suffix="_vcmi_template")
        export_dir = temp_dir_obj.name
    else:
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    try:
        with deffile.open(path) as d:
            images, exported_frames, template_image = export_frame_images(
                d,
                filetype,
                export_dir,
                only_config=only_config,
                ignore_filename=ignore_filename,
                ignore_group=ignore_group,
                merge_shadow=merge_shadow,
                overlay_from_colours=overlay_from_colours,
                template_frame=template_frame if vcmi_template else None,
            )

        if not mask_only:
            json_path = os.path.join(foldername, f"{stem}.json")
            json_data = {
                "basepath": stem + "/",
                "images": images
            }
            with open(json_path, "w", encoding="utf-8") as o:
                json.dump(json_data, o, indent=4, ensure_ascii=False)

        if vcmi_template:
            if not any(exported_frames):
                if only_config:
                    print("[WARN] --vcmi-template ignored because --onlyconfig does not export PNG files.")
                else:
                    print("[WARN] No PNG files were generated, template was not created.")
            else:
                if template_frame < 0 or template_frame >= len(exported_frames):
                    raise ValueError(f"template_frame {template_frame} is out of range, frame count is {len(exported_frames)}")
                if not exported_frames[template_frame]:
                    raise ValueError(f"frame {template_frame} was not exported successfully")

                template = generate_vcmi_template_from_png(
                    template_image,
                    animation_name=stem.upper(),
                    animation_extension=filetype,
                )
                template_json_path = os.path.join(foldername, f"{stem}.template.json")
                with open(template_json_path, "w", encoding="utf-8") as o:
                    json.dump(template, o, indent=4, ensure_ascii=False)
                print(f"[INFO] VCMI template written to {template_json_path}")

    finally:
        if temp_dir_obj is not None:
            temp_dir_obj.cleanup()
            print("[INFO] Temporary PNG files removed.")


def build_argument_parser():
    parser = argparse.ArgumentParser(
        description="Export Heroes III DEF/D32 to PNG/JSON and optionally generate a VCMI template JSON from one frame.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("paths", nargs="*", help="Input DEF/D32 files. If omitted, a file dialog will open.")
    parser.add_argument("--onlyconfig", action="store_true", help="Generate only the main .json config, do not export PNG files.")
    parser.add_argument("--ignorefilename", action="store_true", help="Ignore original frame names and generate sequential names.")
    parser.add_argument("--ignoregroup", action="store_true", help="Force all exported frames into group 0 naming.")
    parser.add_argument("--mergeshadow", action="store_true", help="Merge shadow layer into normal PNG for DEF files.")
    parser.add_argument("--overlay", action="store_true", help="Generate overlay PNG from yellow/green pixels when no overlay exists.")
    parser.add_argument("--vcmi-template", action="store_true", help="Generate DEFNAME.template.json from an exported PNG frame.")
    parser.add_argument("--template-frame", type=int, default=0, help="Zero-based source frame index to use for VCMI template generation.")
    parser.add_argument("--maskonly", action="store_true", help="With --vcmi-template export PNGs only to a temporary folder, generate template, then delete the temporary PNGs. Main DEFNAME.json is not generated in this mode.")
    return parser


def select_paths_via_dialog():
    Tk().withdraw()
    return askopenfilenames(filetypes=[("HoMaM 3 DEF/D32 files", ".def .d32")])


def main():
    parser = build_argument_parser()
    args = parser.parse_args()

    if args.maskonly and not args.vcmi_template:
        parser.error("--maskonly requires --vcmi-template")
    if args.maskonly and args.onlyconfig:
        parser.error("--maskonly cannot be combined with --onlyconfig")

    paths = list(args.paths)
    used_file_dialog = not paths
    if not paths:
        paths = select_paths_via_dialog()

    if not paths:
        print("No files selected or provided.")
        return

    for path in paths:
        try:
            filetype = detect_format(path)
            flags = []
            if args.onlyconfig:
                flags.append("onlyconfig")
            if args.ignorefilename:
                flags.append("ignorefilename")
            if args.ignoregroup:
                flags.append("ignoregroup")
            if args.mergeshadow and filetype == "def":
                flags.append("mergeshadow")
            if args.overlay:
                flags.append("overlay")
            if args.vcmi_template:
                flags.append(f"vcmi-template frame={args.template_frame}")
            if args.maskonly:
                flags.append("maskonly")

            suffix = f" [{' | '.join(flags)}]" if flags else ""
            print(f"[INFO] Processing {path} ({filetype.upper()}){suffix}")

            process_def_file(
                path,
                filetype,
                only_config=args.onlyconfig,
                ignore_filename=args.ignorefilename,
                ignore_group=args.ignoregroup,
                merge_shadow=args.mergeshadow,
                overlay_from_colours=args.overlay,
                vcmi_template=args.vcmi_template,
                template_frame=args.template_frame,
                mask_only=args.maskonly,
            )

        except Exception as e:
            ensure_logger()
            logging.error(f"Error while processing '{path}': {e}")
            print(f"[ERROR] Failed to process {path}: {e}")
            if used_file_dialog:
                try:
                    messagebox.showerror("Error", f"Failed to process {path}:\n{e}")
                except Exception:
                    pass


if __name__ == "__main__":
    main()