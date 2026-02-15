# TightyTile

A minimal-dimension image concatenation CLI.

## Core Principles / Core Features

- Downscale only
- No upscaling
- No padding

## Installation

```powershell
uv sync
```

## Commands

```text
Usage: tighty-tile [OPTIONS] COMMAND [ARGS]...

  Command-line interface for TightyTile.

Options:
  -v, --verbose  Enable verbose output.
  --help         Show this message and exit.

Commands:
  concat*  Concatenate multiple images into a single image.
```

```text
Usage: tighty-tile concat [OPTIONS] [IMAGE_PATHS]...

  Concatenate multiple images into a single image.

Options:
  -d, --direction [h|horizontal|v|vertical]
                                  Direction to concatenate images.
  -o, --output FILE               Output file path for the concatenated image.
  --help                          Show this message and exit.
```

## Examples

```powershell
tighty-tile a.jpg b.jpg -d h -o out.webp
```

```powershell
tighty-tile a.png b.png c.png -d vertical
```

If `-o` is not specified, output is written to the current directory as `TightyTile_<timestamp>.webp`.
