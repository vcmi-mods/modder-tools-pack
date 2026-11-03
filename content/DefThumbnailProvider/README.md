# Heroes III DEF Thumbnail Provider

See what is inside Heroes of Might and Magic III `.def` files directly in
Windows Explorer.

DEF Thumbnail Provider replaces generic file icons with real image previews.
It is useful when browsing, sorting, or editing large collections of Heroes III
graphics because you no longer need to open every file to find the right one.

### Creatures

![Heroes III creature DEF thumbnails in Windows Explorer](docs/images/1.png)

### Map objects

![Heroes III map object DEF thumbnails in Windows Explorer](docs/images/2.png)

## Features

- Shows DEF sprites as thumbnails in Windows Explorer
- Supports the common Heroes III DEF formats
- Keeps transparent backgrounds on modern Windows
- Works on Windows XP SP3 and newer Windows versions
- Includes x86, x64, and ARM64 builds
- Does not change which application opens `.def` files

## Download

Download the package for your version of Windows from
[the latest release](../../releases/latest):

- **x64** for most modern PCs
- **x86** for 32-bit Windows and Windows XP
- **ARM64** for Windows on ARM

Extract the package to a permanent folder. The DLL must stay in that folder
after installation.

## Install

1. Open **Command Prompt as Administrator**.
2. Change to the folder containing `DefThumbnailProvider.dll`.
3. Run:

```bat
regsvr32 /n /i:machine DefThumbnailProvider.dll
```

After the success message, restart Windows Explorer or restart your computer.
Open a folder containing `.def` files and select **Large icons** or
**Extra large icons**.

If previously cached icons remain, see the
[troubleshooting notes](docs/TECHNICAL.md#install).

## Uninstall

Open **Command Prompt as Administrator** in the installation folder and run:

```bat
regsvr32 /u /n /i:machine DefThumbnailProvider.dll
```

Then restart Windows Explorer or restart your computer.

## About

The DEF decoder is based on code and format knowledge from the
[VCMI project](https://github.com/vcmi/vcmi). This project is distributed under
the GPL-2.0-or-later license.

Developers can find build instructions, implementation notes, test tools, COM
details, and licensing information in the
[technical documentation](docs/TECHNICAL.md).
