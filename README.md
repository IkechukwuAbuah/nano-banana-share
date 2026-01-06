# nano-banana-share

A Claude Code skill for **AI image generation with shareable URLs**.

## What it does

When triggered, Claude will:
1. **Generate** image using nanobanana MCP (Gemini)
2. **Upload** to [0x0.st](https://0x0.st)
3. **Return** shareable URL

No API keys needed for hosting. Zero config.

## Installation

```bash
cp -r nano-banana-share ~/.claude/skills/
```

## Triggers

Say things like:
- "generate an image and share it"
- "create a picture of X and give me a link"
- "shareable image of..."
- "image URL for..."

## Example

**You**: "Generate a cute robot mascot and share it"

**Claude**:
1. Calls `mcp__nanobanana__generate_image`
2. Runs `share.py` with the output path
3. Returns: "Here's your image: https://0x0.st/abc123.png"

## How it works

```
┌─────────────────┐     ┌─────────────┐     ┌─────────────┐
│  nanobanana MCP │────▶│  share.py   │────▶│   0x0.st    │
│   (Gemini AI)   │     │  (curl)     │     │   (URL)     │
└─────────────────┘     └─────────────┘     └─────────────┘
        ▲                                          │
        │              Claude orchestrates         │
        └──────────────────────────────────────────┘
```

## Requirements

- [nanobanana MCP server](https://github.com/zhongweili/nanobanana-mcp-server)
- `GEMINI_API_KEY` environment variable
- Python 3.10+, curl

## Standalone usage

The upload script also works independently:

```bash
# Share any image
python3 scripts/share.py /path/to/image.png

# Share latest nanobanana image
python3 scripts/share.py latest
```

## File retention

0x0.st keeps files 30 days to 1 year (smaller = longer).

---

🤖 Built with [Claude Code](https://claude.com/claude-code)
