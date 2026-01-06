---
name: nano-banana-share
description: "AI image generation with shareable URLs. Extends nano-banana by uploading to 0x0.st. Triggers: generate and share, shareable image, image URL, upload image, share this image, get link for image."
version: 1.0.0
author: claude-code
created: 2026-01-06
---

# Nano Banana Share - Image Generation with Shareable URLs

## Overview

This skill wraps the nano-banana image generation capability and adds automatic upload to 0x0.st for shareable URLs. No API keys or accounts required.

## When to Use

- User wants to generate an image AND share it via URL
- User has an existing nanobanana image and wants a shareable link
- User says "share", "URL", "link", or "upload" in context of images

## Workflow

### Generate + Share (New Image)

1. **Generate** using nanobanana MCP:
   ```
   mcp__nanobanana__generate_image with user's prompt
   ```

2. **Get the output path** from the MCP response (e.g., `/Users/x/nanobanana-images/gen_*.png`)

3. **Upload** using the share script:
   ```bash
   python3 ~/.claude/skills/nano-banana-share/scripts/share.py /path/to/image.png
   ```

4. **Return the URL** to the user (e.g., `https://0x0.st/abc123.png`)

### Share Existing Image

To share the most recent generated image:
```bash
python3 ~/.claude/skills/nano-banana-share/scripts/share.py latest
```

To share a specific image:
```bash
python3 ~/.claude/skills/nano-banana-share/scripts/share.py /path/to/image.png
```

## Script Reference

**Location**: `scripts/share.py`

**Usage**:
```bash
share.py [image_path|latest]
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
