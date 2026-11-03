# DEFRecolor

Professional palette editor for Heroes of Might and Magic III DEF graphics.

DEFRecolor combines precise palette editing with live frame and animation previews. It is designed for modders who want to recolor creatures, heroes, adventure-map objects and interface assets without repeatedly exporting frames to another graphics editor.

![DEFRecolor workspace](modern-ui.png)

The built-in guide documents the complete recoloring workflow and every editing category directly in the application.

![DEFRecolor built-in guide](help-guide.png)

## Highlights

- Side-by-side original and recolored palettes.
- Live comparison of the current frame and looping animation.
- Separate group and frame navigation.
- Multiple color selection with `Ctrl+click`.
- Eyedropper selection directly from rendered DEF previews.
- Selection by current frame, group, whole DEF, shared colors or unused colors.
- Color-family, highlight, shadow and neutral selections from the **Select** menu.
- Protected DEF transparency and shadow indices `0–7`.
- Undo and redo for committed palette changes.
- Local zoom and pan inside the preview workspace.
- JSON palette import and export.
- Drag-and-drop and command-line file opening.
- Dynamically discovered external language packs.

## Editing tools

### Selection and masks

Pick colors in the edited palette, sample a visible DEF pixel with the eyedropper, or build a selection from palette usage and color ranges. Selected colors are outlined in the edited palette.

### Corrections

Adjust hue, saturation, lightness, contrast, gamma, exposure, vibrance, temperature and tint. Changes are shown live before they are committed.

### Ramp and tone

Map selected shades to a two- or three-color ramp while preserving luminance order. Tone modes include Color, Multiply, Screen and Overlay.

### Magic Recolor

Choose a representative palette color, expand the set with the Similarity slider, select a target color and control the resulting strength. Relative shade preservation keeps highlights and shadows coherent.

### Advanced effects

Apply grayscale, sepia, invert, posterize and automatic contrast to the selected editable colors.

### Restore and reset

Restore selected colors, restore the complete palette, cancel a live preview or reset only the active adjustment controls.

## Installation

DEFRecolor is portable and does not require an installer.

1. Download the release ZIP.
2. Extract the complete archive to one directory.
3. Keep `DefThumbnailProvider.dll` next to `DEFRecolor.exe`.
4. Run `DEFRecolor.exe` and open a `.def` file.

The executable and `DefThumbnailProvider.dll` must use the same architecture. The DLL provides DEF decoding and rendering for the live previews and is based on [DefThumbnailProvider](https://github.com/GeorgeK1ng/DefThumbnailProvider).

Release packages are provided for:

- **x86** — 32-bit Windows systems, built with MSVC v142 for Windows 7 compatibility.
- **x64** — standard 64-bit Windows systems, built with MSVC v142 for Windows 7 compatibility.
- **ARM64** — Windows on ARM devices, built with the current MSVC v143 toolset.

Each package is standalone: the matching provider DLL, languages and required license files are already included. The thumbnail provider does not need to be registered in Windows for DEFRecolor; keeping the DLL beside the executable is sufficient.

### Windows Explorer thumbnails

Registration is optional. DEFRecolor loads the adjacent DLL directly for its own previews, while Windows Explorer requires the provider to be registered before it can display DEF thumbnails.

1. Start the matching DEFRecolor build for your Windows architecture.
2. Choose **Tools → Install thumbnail provider**.
3. Read the confirmation and approve the Windows administrator prompt.
4. Reopen Explorer if existing folders do not refresh immediately.

DEFRecolor performs the machine-wide registration directly; it does not create or execute temporary BAT or VBS scripts. The application reports cancellation, a missing DLL and the registration process result. To remove the Explorer integration, choose **Tools → Uninstall thumbnail provider** and approve the administrator prompt. Uninstalling the provider does not remove DEFRecolor or user settings.

The **Tools** menu shows only the action that currently makes sense. DEFRecolor verifies the machine-wide CLSID, registered DLL path and the thumbnail handlers for `.def`, `.d32` and `.p32`. A complete valid registration shows **Uninstall**; a missing, incomplete or stale registration shows **Install**, which also repairs the registration.

Use an x64 package for the normal 64-bit Windows Explorer, x86 for a 32-bit Windows installation and ARM64 for native Windows on ARM. `DEFRecolor.exe` and `DefThumbnailProvider.dll` in one package always have matching architectures.

Recommended release layout:

```text
DEFRecolor/
├── DEFRecolor.exe
├── DefThumbnailProvider.dll
├── languages/
│   ├── english.json
│   ├── czech.json
│   ├── german.json
│   └── ...
└── README.md
```

Release ZIPs do not contain a separate `LICENSE` file or `licenses` directory.

## Quick start

1. Open a DEF with **File → Open DEF**, drag it onto the application, or drag it onto `DEFRecolor.exe`.
2. Choose an animation group and frame in the top toolbar.
3. Select one or more colors in the edited palette. Hold `Ctrl` to add or remove individual colors.
4. Choose a tool category in the right inspector.
5. Tune the controls while watching the original and recolored previews.
6. Press the category's **Apply** button to create one undoable history step.
7. Save the result. DEFRecolor proposes a filename based on the opened file.

Optional: install Explorer thumbnails at any time from **Tools → Install thumbnail provider**. Administrator permission is required only for installation or uninstallation, not for ordinary editing.

The original palette and previews never change. The edited side always shows the result that will be saved.

## Preview controls

- Use the mouse wheel over the preview workspace to zoom.
- Zoom is centered on the visible sprite rather than the transparent DEF canvas.
- Use the local scrollbars to inspect an enlarged frame.
- **100%** resets zoom and preview position.
- Animation speed affects both looping animation previews.
- Pause freezes the animations without changing the selected frame.

## Keyboard shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+O` | Open DEF |
| `Ctrl+S` | Save DEF |
| `Ctrl+I` | Import JSON palette |
| `Ctrl+E` | Export JSON palette |
| `Ctrl+Z` | Undo palette change |
| `Ctrl+Y` | Redo palette change |
| `Ctrl+1` … `Ctrl+6` | Switch tool category |
| `F1` | Open the built-in guide |

## Command line

Paths are Unicode-aware and may contain spaces or non-Latin characters.

```text
DEFRecolor.exe "input.def"
DEFRecolor.exe /load "input.def" /save "output.def"
DEFRecolor.exe /load "input.def" /import "palette.json" /save "output.def"
DEFRecolor.exe /load "input.def" /export "palette.json"
```

## Settings

User preferences are stored in:

```text
%APPDATA%\DEFRecolor\settings.json
```

The file contains recent DEF paths and the 16 custom colors used by Windows color dialogs. DEFRecolor no longer creates separate binary settings files.

## Languages

Included translations:

- English
- Czech
- German
- Polish
- French
- Russian
- Ukrainian
- Chinese

Language files are discovered dynamically from the `languages` directory. To add a translation, copy `english.json`, translate its values without changing the keys, and restart DEFRecolor. The new language is added to the menu automatically.

## Building from source

Requirements:

- Visual Studio 2019 or newer with **Desktop development with C++**.
- Windows SDK.
- CMake, used to build the bundled provider dependency.

Clone the repository including its provider submodule:

```text
git clone --recurse-submodules https://github.com/GeorgeK1ng/DEFRecolor.git
```

For an existing checkout:

```text
git submodule update --init --recursive
```

Open `DEFRecolor.sln`, select `Release` and either `x64` or `ARM64`, then build the solution. MSBuild configures and builds `external/DefThumbnailProvider` automatically, copies the matching DLL beside DEFRecolor and copies all language packs. The application and provider use the statically linked MSVC runtime, so a separate Visual C++ Redistributable is not required by the release package.

GitHub Actions uses the same solution build and publishes ready-to-run `x86`, `x64` and `ARM64` ZIP artifacts. Intel builds use the MSVC 14.29/v142 environment; ARM64 uses v143. The bundled provider is compiled with the same architecture and toolset as DEFRecolor, so no separately downloaded provider is needed.

## DefThumbnailProvider dependency

[DefThumbnailProvider](https://github.com/GeorgeK1ng/DefThumbnailProvider) is included as a pinned git submodule under `external/DefThumbnailProvider`. DEFRecolor loads its editor API directly from the adjacent DLL for decoding, frame metadata and rendering. Keeping it as a submodule provides reproducible builds while allowing the provider to remain an independently maintained project.

When updating the dependency, update the submodule commit deliberately and verify all architecture packages.

## Notes for DEF modding

DEF palette indices `0–7` commonly have format-specific transparency and shadow roles. They are protected by default. Disable protection only when you deliberately need to edit those indices and understand how the target DEF type uses them.

Palette edits affect the complete DEF because the format uses one shared palette. Frame and group controls change navigation and selection masks; they do not create separate per-frame palettes.

## License

DEFRecolor licensing information is maintained in the repository’s [LICENSE](https://github.com/GeorgeK1ng/DEFRecolor/blob/main/LICENSE).

Issues and feature requests are welcome in the [GitHub issue tracker](https://github.com/GeorgeK1ng/DEFRecolor/issues).


