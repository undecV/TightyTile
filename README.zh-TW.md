# TightyTile

最小化維度的圖片拼接工具（CLI）。

## 核心原則／核心功能

- 只會縮小圖片（downscale）
- 絕不放大圖片（no upscale）
- 絕不以填充補空白（no padding）

## 安裝

```powershell
uv sync
```

## 指令

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

## 用法範例

```powershell
tighty-tile a.jpg b.jpg -d h -o out.webp
```

```powershell
tighty-tile a.png b.png c.png -d vertical
```

未指定 `-o` 時，會輸出為目前目錄下的 `TightyTile_時間戳.webp`。
