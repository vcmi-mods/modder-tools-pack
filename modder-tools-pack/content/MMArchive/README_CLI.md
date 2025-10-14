# MMArchive Command Line Interface

This is a command-line version of the MMArchive GUI application, designed to work with Heroes of Might and Magic archive files (.lod, .snd, .vid, .lwd, .pac files).

## Files Created

- `MMArchiveCLI.dpr` - Main command-line program
- `MMArchiveCLI.bdsproj` - Borland Developer Studio project file
- `README_CLI.md` - This documentation

## Version

Current version: 1.2.5

## Features

The command-line version provides these archive operations:

1. **List** - Display all files in an archive
2. **Extract** - Extract files from an archive (with optional file type filtering)
3. **Add** - Add a single file to an archive
4. **ExtractDef** - Extract DEF files for DefTool (creates HDL and BMP files)
5. **Help** - Display usage information

## Usage

```
MMArchiveCLI.exe <operation> <archive> [options]
```

### Operations

- `list <archive>` - List all files in the archive
- `extract <archive> [-o output_dir] [-f *.ext]` - Extract files with optional output directory and file filter
- `add <archive> <file>` - Add a file to the archive
- `extractdef <archive> [-o output_dir]` - Extract DEF files for DefTool with HDL and BMP files
- `version` - Show version information
- `help` - Show help information

### Options

- `-o <directory>` - Specify output directory (default: archive filename with dots replaced by underscores)
- `-f <*.extension>` - Filter files by extension (e.g., *.bmp, *.def)

### Default Output Directories

- **extract**: `<archive_name_with_underscores>\` (e.g., `sprites.lod` → `sprites_lod\`)
- **extractdef**: `<archive_name_with_underscores>_deftool\` (e.g., `sprites.lod` → `sprites_lod_deftool\`)

### Examples

```batch
# List files in data.lod
MMArchiveCLI.exe list data.lod

# Extract all files to default folder (archive name with dots as underscores)
MMArchiveCLI.exe extract data.lod
# Creates folder: data_lod\

# Extract all files to custom directory
MMArchiveCLI.exe extract data.lod -o my_output

# Extract only .bmp files to custom directory
MMArchiveCLI.exe extract data.lod -o my_output -f *.bmp

# Extract only .def files to default folder
MMArchiveCLI.exe extract sprites.lod -f *.def
# Creates folder: sprites_lod\

# Add a file to the archive
MMArchiveCLI.exe add data.lod newfile.txt

# Extract DEF files for DefTool (creates HDL + BMP files)
MMArchiveCLI.exe extractdef sprites.lod
# Creates folder: sprites_lod_deftool\

# Extract DEF files to custom directory
MMArchiveCLI.exe extractdef sprites.lod -o my_deftool_output

# Show version
MMArchiveCLI.exe version

# Show help
MMArchiveCLI.exe help
```

## Compilation

To compile this project:

1. Open `MMArchiveCLI.bdsproj` in Borland Developer Studio 2006
2. Ensure the search path includes required directories:
   - `..\RSPak`
   - `..\RSPak\Extra`
   - `..\RSPak\Extra\ZLib`
3. Build the project

## Dependencies

The CLI version uses the same core archive handling units as the GUI version:
- `RSLod.pas` - Main archive handling
- `RSDef.pas` - DEF file processing
- `RSUtils.pas` - Utility functions
- `RSSysUtils.pas` - System utilities
- `IniFiles.pas` - Configuration file support

## Differences from GUI Version

The command-line version:
- Removes all GUI dependencies (Forms, Controls, etc.)
- Uses console output instead of visual interface
- Supports file type filtering for extraction
- Includes DefTool extraction functionality
- Reads settings from MMArchive.ini (shared with GUI version)
- Uses simple command-line argument parsing
- Has comprehensive error handling and user feedback

## Configuration

The CLI automatically reads settings from `MMArchive.ini` on startup (same as GUI version):
- **Def Extract With External Shadow** - Include external shadows in DEF extraction (applies to extractdef operation)
- **Def Extract In 24 Bits** - Extract DEF files in 24-bit color mode (applies to extractdef operation)
- **Ignore Unpacking Errors** - Continue processing despite archive errors (applies to all operations)

All INI settings are loaded once at startup and applied to all archive operations. If the INI file doesn't exist, it will be created with default values. If the INI file cannot be read, default values are used.

## Limitations

- No interactive file selection
- No preview capabilities
- No advanced filtering or sorting beyond file extensions
- Single file operations only (no batch processing)
- Limited to basic archive operations

## Error Handling

The program returns exit codes:
- 0: Success
- 1: Error (file not found, operation failed, etc.)

Error messages are written to standard output.