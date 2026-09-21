DEF2JSON for Heroes III / VCMI
================================

DEF2JSON extracts Heroes III DEF and D32 animation files to PNG images and
creates the animation JSON configuration used by VCMI.

The x86 and x64 EXE builds are standalone. The Python source is also included,
but running it directly requires Python 3, Pillow and the homm3data module.


WHAT THE NEW VERSION ADDS
-------------------------

The original def2json.org.py only supported DEF files. It opened DEF files,
exported their normal, shadow and overlay layers, and generated a basic JSON
file using the original frame names.

The new def2json.py and the supplied EXE builds additionally provide:

* DEF and D32 support, detected automatically from the file header.
* Multiple input files in a single command.
* A file-selection dialog when no paths are supplied.
* Config-only mode without exporting PNG files.
* Sequential frame names, group-0 naming, or both at the same time.
* Optional merging of DEF shadow layers into the normal PNG images.
* Optional overlay generation from visible yellow (255,255,0) and green
  (0,255,0) pixels when the source does not contain an overlay layer.
* Automatic VCMI object-template JSON generation from a selected frame.
* Automatic object-mask detection on a 32x32 tile grid, including active,
  blocked, visible and hole tiles, plus a default visitableFrom mask.
* Template-only mode that extracts frames to a temporary directory and removes
  them after creating the object template.
* Per-frame error handling and a def2json.log file instead of aborting the
  whole batch when one frame fails.


OUTPUT
------

For an input named OBJECT.def or OBJECT.d32, normal extraction creates:

* OBJECT.json       - VCMI animation configuration
* OBJECT\*.png      - extracted animation frames and optional layers

With --vcmi-template it also creates:

* OBJECT.template.json - VCMI object template with mask and visitableFrom


COMMAND-LINE USAGE
------------------

def2json.exe [options] file1.def [file2.d32 ...]

Options:

--onlyconfig
    Create only OBJECT.json. Do not export PNG images.

--ignorefilename
    Ignore original frame names and use sequential names inside each group.

--ignoregroup
    Put all exported frames into group 0 naming.

--mergeshadow
    Merge the shadow layer into the normal PNG. Applies to DEF files only.

--overlay
    Generate an overlay PNG from yellow/green pixels when no source overlay
    exists. For D32 files the overlay is generated from the decoded image.

--vcmi-template
    Generate OBJECT.template.json from an exported PNG frame.

--template-frame NUMBER
    Select the zero-based exported frame used to calculate the VCMI object
    mask. The default is frame 0.

--maskonly
    Use with --vcmi-template. Export PNGs temporarily, create only the object
    template, then delete the temporary files. OBJECT.json is not created.

-h, --help
    Display the built-in command-line help.

The switches can be combined, except that --maskonly requires --vcmi-template
and cannot be combined with --onlyconfig.

Examples:

def2json.exe CREATURE.def
def2json.exe OBJECT.d32 --ignorefilename --ignoregroup
def2json.exe OBJECT.def --mergeshadow --overlay
def2json.exe OBJECT.def --vcmi-template --template-frame 3
def2json.exe OBJECT.d32 --vcmi-template --maskonly


WINDOWS EXPLORER CONTEXT MENU
-----------------------------

Run install.cmd to add a DEF2JSON submenu to the context menu of .def and .d32
files. The installer requests administrator privileges, chooses the x86 or x64
EXE for the current Windows installation and stores its absolute path.

The context menu provides the common extraction, naming, overlay and VCMI
template combinations. The DEF menu also offers merged-shadow extraction.
Use the command line when a custom --template-frame value is needed.

Run uninstall.cmd to remove only the DEF2JSON context-menu entries.


ORIGINAL PROJECT
----------------

Based on: https://github.com/Laserlicht/def_to_vcmi_json
