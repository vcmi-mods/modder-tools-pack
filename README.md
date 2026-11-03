# Modders' Tool Pack

An all-in-one collection of tools, converters, editors, templates, and ready-to-use graphics for **Heroes of Might and Magic III** and **VCMI** mod creators.

The pack is distributed as a VCMI development-resource mod, but it does not add gameplay content by itself. Most tools can also be used directly from the `content` directory without launching VCMI.

## Highlights

- Extract and manage Heroes III, Might & Magic, and HotA archives.
- Convert DEF and D32 animations to PNG and VCMI JSON.
- Preview DEF files and display their thumbnails in Windows Explorer.
- Recolor DEF palettes with live frame and animation previews, precise selection masks, and professional color tools.
- Edit DEF graphics, random-map templates, and `HotA.dat`.
- Recalculate VCMI creature AI and fight values.
- Use more than 1,400 curated icons and numerous layered graphics templates.
- Install Explorer integrations with the included self-elevating scripts.

## Requirements and compatibility

- **Operating system:** the supplied executables and Explorer integrations are intended for Windows. Both x86 and x64 builds are included where applicable.
- **VCMI:** version 1.5 or newer is required when the pack is installed as a VCMI mod.
- **HotA archives:** VCMIExtract supports archives from HotA 1.8.1. MMArchive support is limited to HotA 1.7.3.
- **Optional software:** some utilities or templates require Python 2.7/3, ImageMagick, Paint.NET, GIMP, Photoshop, or another editor compatible with the supplied file format. See the relevant entry below.

## Core tools

| Tool | Purpose | Usage notes |
| --- | --- | --- |
| [VCMIExtract](content/vcmiextract) | Extracts LOD, PAC, SND, VID, PAK, DEF, and D32 resources; converts PCX images directly to PNG. | Run `install.cmd` for Explorer extraction commands. Includes x86 and x64 builds. [Upstream project](https://github.com/IvanSavenko/vcmiextract). |
| [DEF2JSON](content/def2json) | Converts DEF/D32 animations to PNG frames and VCMI animation JSON. Supports batch input, sequential/group-0 naming, merged shadows, overlays, and generated VCMI object templates and masks. | Run `install.cmd` for the Explorer submenu, or use the CLI. See the [complete guide](content/def2json/readme.txt). |
| [DEF Thumbnail Provider](content/DefThumbnailProvider) | Displays real DEF sprite thumbnails in Windows Explorer. | Run `install.cmd`, then restart Explorer if thumbnails do not appear. See its [README](content/DefThumbnailProvider/README.md). |
| [DEFRecolor 1.2](content/DEFRecolor) | Professional DEF palette editor with side-by-side live frame and animation previews, usage and color-range selection masks, HSL and advanced corrections, ramps, tone modes, Magic Recolor, effects, undo/redo, and JSON palette exchange. | Portable x86, x64, and ARM64 builds with eight languages and Unicode paths. The matching provider DLL is bundled; optional Explorer thumbnails can be installed directly from the **Tools** menu. See its [README](content/DEFRecolor/readme.md). |
| [DefPreview](content/DefPreview) | Opens, previews, and extracts DEF animations. | Run `install.cmd` to associate `.def` files. The uninstaller restores the previous association. |
| [MMArchive](content/MMArchive) | GUI and CLI manager for listing, previewing, extracting, adding, and replacing files in LOD, LWD, SND, VID, PAC, and related archives. | Run `install.cmd` for archive associations. The CLI also supports filtered extraction and DefTool output; see the [CLI reference](content/MMArchive/src/README_CLI.md). |

## Additional utilities

| Tool | Purpose | Requirements / notes |
| --- | --- | --- |
| [H3DefTool](content/H3DefTool) | Classic editor for creating and editing Heroes III DEF animations. | Windows executable; Russian language files are included. |
| [DEF Recoloring Program](content/DEF%20Recoloring%20Program%20v.0.0.3) | Older palette-based DEF recoloring utility by Macron1. | Detailed instructions are supplied as `doc/Instruction.doc`. |
| [H3 RMG Converter](content/H3%20RMG%20Converter) | Converts Heroes III random-map generator templates by drag and drop. | Python 3; the original readme specifies Python 3.5.1. [Instructions](content/H3%20RMG%20Converter/readme.txt). |
| [TEditor](content/TEditor_1.0) | Visual editor for Heroes III random-map templates, including zones, links, object settings, and TPZ files. | Windows executable; the bundled help is in Russian. |
| [HotA Editor](content/HotA%20Editor) | Edits `HotA.dat`. | Separate x86 and x64 builds are included. Back up the data file before editing it. |
| [Macron's Balancer](content/Macron's%20Balancer) | Recalculates creature AI and fight values in VCMI JSON files. Accepts files or directories by drag and drop. | Requires Python 2.7. [Instructions](content/Macron's%20Balancer/readme.txt). |
| [Puzzle generator](content/puzzle%20generator) | Splits a 596×546 town puzzle image into the 48 pieces expected by VCMI and includes a sample configuration. | Requires ImageMagick. [Instructions](content/puzzle%20generator/readme.txt). |

## Graphics and templates

| Resource | Contents / use |
| --- | --- |
| [Heroes III Modding Resources](content/Heroes%20III%20Modding%20Resources) | More than 1,400 specialty, secondary-skill, artifact, spell-scroll, spell-book, luck, morale, blank-icon, and creature-background images, including tagged HotA, ToW, WoG, and other mod variants. See the [collection notes](content/Heroes%20III%20Modding%20Resources/readme.txt). |
| [Creature positioning frames](content/creature-position-frames) | x2, x3, and x4 two-hex positioning frames for VCMI HD creature graphics. |
| [Adventure Map buttons](content/Adventure%20Map%20buttons) | Layered GIMP/XCF template and a Python palette-fixing helper for adventure-map buttons. |
| [Battlefield Hexes](content/Battlefield%20Hexes) | Transparent battlefield hex overlay for positioning combat graphics. |
| [Shooter projectile template](content/Shooters%20projectile%20template) | Grid for determining projectile offsets from a creature's firing frame. [Instructions](content/Shooters%20projectile%20template/readme.txt). |
| [Mage guild template](content/Mage%20guild%20template) | Paint.NET template and blank background for custom mage-guild windows. |
| [Puzzle template](content/puzzle%20template) | Layered Paint.NET file and sample JSON for manually creating a 48-piece faction puzzle. |
| [Town icon and hall templates](content/Stuff%20to%20make%20town%20icons%20and%20hall%20backgrounds) | Transparent fort overlays and a layered Paint.NET template for town icons and town-hall backgrounds. |
| [Layered town backgrounds](content/h3-towns-as-psd-layers) | Nine town-screen background PSD files, one for each classic faction. |
| [Heroes III logo templates](content/Heroes%20III%20Logo%20Templates) | Layered XCF logo collections covering multiple Heroes III variants. |

## DEF2JSON examples

```console
def2json.exe CREATURE.def
def2json.exe OBJECT.d32 --ignorefilename --ignoregroup
def2json.exe OBJECT.def --mergeshadow --overlay
def2json.exe OBJECT.def --vcmi-template --template-frame 3
def2json.exe OBJECT.d32 --vcmi-template --maskonly
```

The normal output consists of `OBJECT.json` and an `OBJECT` directory containing the extracted PNG frames. `--vcmi-template` additionally creates `OBJECT.template.json`. For every option and restriction, consult the [DEF2JSON guide](content/def2json/readme.txt).

## MMArchive CLI examples

```console
MMArchiveCLI.exe list data.lod
MMArchiveCLI.exe extract data.lod -o extracted
MMArchiveCLI.exe extract sprites.lod -f *.def
MMArchiveCLI.exe add data.lod newfile.txt
MMArchiveCLI.exe extractdef sprites.lod -o deftool
```

MMArchive reads its settings from `MMArchive.ini`. The CLI returns exit code `0` on success and `1` on failure.

## Safety notes

- Back up archives, templates, and game data before modifying them.
- Installers change Windows registry entries for context menus, thumbnail handlers, or file associations and therefore request administrator privileges.
- Use the matching `uninstall.cmd` before moving an installed tool to another directory; then reinstall it from the new location.
- The pack contains third-party executables from multiple authors. Obtain releases from this repository or the linked upstream projects and scan downloads according to your normal security policy.

## Credits, license, and support

The collection is maintained by multiple contributors and contains work by various original authors. Refer to each bundled readme for item-specific authorship and licensing details.

The VCMI package metadata declares **Creative Commons Attribution-ShareAlike 4.0** for the pack. Individual tools, source files, and included assets may carry their own licenses; those item-specific terms take precedence where applicable. DEF Thumbnail Provider, for example, is documented as GPL-2.0-or-later.

- Pack version: **1.3.0**
- VCMI compatibility: **1.5+**
- Community/support: [VCMI Discord](https://discord.gg/chBT42V)
- Pack license: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)