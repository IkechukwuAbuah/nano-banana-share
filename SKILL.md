---
name: nano-banana-share
description: "AI image generation with shareable URLs. Extends nano-banana by uploading to 0x0.st. Triggers: generate and share, shareable image, image URL, upload image, share this image, get link for image."
version: 1.0.0
author: claude-code
created: 2026-01-06
---

# Nano Banana Share - Image Generation with Shareable URLs

## Overview

Self-contained AI image generation with automatic upload to 0x0.st for shareable URLs. Uses Gemini 3 Pro Image API directly - no MCP server required.

## When to Use

- User wants to generate an image AND share it via URL
- User has an existing image and wants a shareable link
- User says "share", "URL", "link", or "upload" in context of images

## Workflow

### Self-Contained (Recommended)

Generate + upload in one command:

```bash
uv run ~/.claude/skills/nano-banana-share/scripts/generate_and_share.py "a cute robot mascot"
```

With options:
```bash
# Higher resolution
uv run generate_and_share.py "sunset mountains" --resolution 2K

# Edit existing image
uv run generate_and_share.py "edit: make background blue" --input image.png

# Local only (skip upload)
uv run generate_and_share.py "test prompt" --no-upload
```

**Output**:
```
Generating: a cute robot mascot...
Saved: /Users/x/nanobanana-images/gen_20260106_191234.png
Uploading...

URL: https://0x0.st/abc123.png
Local: /Users/x/nanobanana-images/gen_20260106_191234.png
```

### Upload Only (Existing Images)

To share an existing image without generating:

```bash
python3 ~/.claude/skills/nano-banana-share/scripts/share.py /path/to/image.png

# Or share most recent from ~/nanobanana-images/
python3 ~/.claude/skills/nano-banana-share/scripts/share.py latest
```

## Script Reference

### generate_and_share.py (Primary)

**Location**: `scripts/generate_and_share.py`

**Requirements**: `GEMINI_API_KEY` environment variable

**Usage**:
```bash
uv run generate_and_share.py "prompt" [options]
```

**Arguments**:
- `prompt`: Image description or edit instructions
- `--input, -i`: Input image for editing
- `--resolution, -r`: 1K (default), 2K, or 4K
- `--no-upload`: Skip upload, return local path only

### share.py (Upload Only)

**Location**: `scripts/share.py`

**Usage**:
```bash
python3 share.py [image_path|latest]
```

**Arguments**:
- `image_path`: Full path to image file
- `latest`: Upload most recent image from ~/nanobanana-images/

**Output**: Prints shareable URL to stdout

## Hosting Details

**Service**: [0x0.st](https://0x0.st) - The Null Pointer

| Aspect | Detail |
|--------|--------|
| Max file size | 512 MB |
| Retention | 30 days minimum, up to 1 year for small files |
| Auth required | None |
| Rate limit | Reasonable use |

## Example Session

**User**: "Generate a cute robot mascot and share it with me"

**Steps**:
1. Call `mcp__nanobanana__generate_image` with prompt "cute robot mascot, friendly design, vibrant colors"
2. Note the output path from response
3. Run `share.py` with that path
4. Return: "Here's your image: https://0x0.st/XyZ.png"

## Prompting

For prompt crafting guidance, refer to the parent skill:
- Formula: Subject + Style + Lighting + Composition + Quality
- Templates available in `~/.claude/skills/nano-banana/references/`

## Limitations

- URLs expire after 30 days to 1 year (size-dependent)
- No editing of hosted images (generate new + re-upload)
- Requires internet connection for upload
- 0x0.st may rate-limit heavy usage
