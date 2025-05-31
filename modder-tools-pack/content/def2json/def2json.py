#!/usr/bin/env python3

import sys
import os
import json
from pathlib import Path
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilenames

from homm3data import deffile


def process_def(path):
    foldername = os.path.dirname(path)
    filename = os.path.basename(path)

    output_dir = os.path.join(foldername, Path(filename).stem)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    tmp_json = {"images": [], "basepath": Path(filename).stem + "/"}

    with deffile.open(path) as d:
        for group in d.get_groups():
            for frame in range(d.get_frame_count(group)):
                frame_base_name = d.get_image_name(group, frame)
                tmp_json["images"].append({
                    "group": group,
                    "frame": frame,
                    "file": f"{frame_base_name}.png"
                })

                img = d.read_image('normal', group, frame)
                img.save(os.path.join(output_dir, f"{frame_base_name}.png"))

                img = d.read_image('shadow', group, frame)
                if img is not None:
                    img.save(os.path.join(output_dir, f"{frame_base_name}-shadow.png"))

                img = d.read_image('overlay', group, frame)
                if img is not None:
                    img.save(os.path.join(output_dir, f"{frame_base_name}-overlay.png"))

    json_path = os.path.join(foldername, f"{Path(filename).stem}.json")
    with open(json_path, "w", encoding="utf-8") as o:
        json.dump(tmp_json, o, indent=4, ensure_ascii=False)


def main():
    paths = sys.argv[1:]

    # If no command-line args, fall back to GUI
    if not paths:
        Tk().withdraw()  # hide root window
        paths = askopenfilenames(filetypes=[("H3 def", ".def")])

    if not paths:
        print("No files selected or provided.")
        return

    for path in paths:
        try:
            process_def(path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process {path}:\n{e}")


if __name__ == "__main__":
    main()
