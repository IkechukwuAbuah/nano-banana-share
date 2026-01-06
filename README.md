# nano-banana-share

A Claude Code skill for **AI image generation with shareable URLs**.

## What it does

Self-contained image generation + sharing in one command:

```bash
uv run generate_and_share.py "a cute robot mascot"
```

**Output:**
```
Generating: a cute robot mascot...
Saved: ~/nanobanana-images/gen_20260106_191234.png
Uploading...

URL: https://0x0.st/abc123.png
Local: ~/nanobanana-images/gen_20260106_191234.png
```

No MCP server needed. Uses Gemini 3 Pro Image API directly.

## Installation

```bash
cp -r nano-banana-share ~/.claude/skills/
export GEMINI_API_KEY="your-key"
```

## Usage

### Generate + Share (One Command)

```bash
# Basic generation
uv run generate_and_share.py "sunset over mountains"

# Higher resolution
uv run generate_and_share.py "portrait photography" --resolution 2K

# Edit existing image
uv run generate_and_share.py "edit: add a rainbow" --input photo.png

# Local only (skip upload)
uv run generate_and_share.py "test prompt" --no-upload
```

### Upload Only (Existing Images)

```bash
# Share any image
python3 share.py /path/to/image.png

# Share latest generated
python3 share.py latest
```

## Claude Code Triggers

Say things like:
- "generate an image and share it"
- "create a picture of X and give me a link"
- "shareable image of..."
- "image URL for..."

## How it works

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────┐
│  Gemini 3 Pro   │────▶│  generate_and_  │────▶│   0x0.st    │
│   Image API     │     │  share.py       │     │   (URL)     │
└─────────────────┘     └─────────────────┘     └─────────────┘
                              │
                              ▼
                        ~/nanobanana-images/
```

## Requirements

- Python 3.10+
- `GEMINI_API_KEY` environment variable
- curl (for upload)

## File retention

0x0.st keeps files 30 days to 1 year (smaller = longer).

---

🤖 Built with [Claude Code](https://claude.com/claude-code)
