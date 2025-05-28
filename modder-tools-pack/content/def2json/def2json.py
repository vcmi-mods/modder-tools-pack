#!/usr/bin/env python3

from tkinter.filedialog import askopenfilenames
from tkinter import messagebox
import os
from pathlib import Path
import json

from homm3data import deffile

paths = askopenfilenames(filetypes=[("H3 def", ".def")])
for path in paths:
    foldername = os.path.dirname(path)
    filename = os.path.basename(path)

    Path(os.path.join(foldername, Path(filename).stem)).mkdir(parents=True, exist_ok=True)

    tmp_json = { "images": [], "basepath": Path(filename).stem + "/" }
    with deffile.open(path) as d:
        for group in d.get_groups():
            for frame in range(d.get_frame_count(group)):
                frame_base_name = d.get_image_name(group, frame)
                tmp_json["images"].append({ "group": group, "frame": frame, "file": "%s.png" % frame_base_name })

                img = d.read_image('normal', group, frame)
                img.save(os.path.join(foldername, Path(filename).stem, "%s.png" % frame_base_name))
                img = d.read_image('shadow', group, frame)
                if img is not None:
                    img.save(os.path.join(foldername, Path(filename).stem, "%s-shadow.png" % frame_base_name))
                img = d.read_image('overlay', group, frame)
                if img is not None:
                    img.save(os.path.join(foldername, Path(filename).stem, "%s-overlay.png" % frame_base_name))
        
        with open(os.path.join(foldername, "%s.json" % Path(filename).stem), "w+") as o:
            json.dump(tmp_json, o, indent=4, ensure_ascii=False)