# nano-banana-share

A Claude Code skill that adds **shareable URLs** to AI-generated images.

## What it does

1. Generate image with [nanobanana MCP](https://github.com/zhongweili/nanobanana-mcp-server)
2. Upload to [0x0.st](https://0x0.st) (zero config, no API keys)
3. Get instant shareable URL

## Installation

Copy to your Claude Code skills directory:

```bash
cp -r nano-banana-share ~/.claude/skills/
```

## Usage

**Share the latest generated image:**
```bash
python3 ~/.claude/skills/nano-banana-share/scripts/share.py latest
# Returns: https://0x0.st/XyZ.png
```

**Share a specific image:**
```bash
python3 ~/.claude/skills/nano-banana-share/scripts/share.py /path/to/image.png
```

## How it works

```
┌─────────────────┐     ┌─────────────┐     ┌─────────────┐
│  nanobanana MCP │────▶│  share.py   │────▶│   0x0.st    │
│  (generates PNG)│     │  (uploads)  │     │ (hosts URL) │
└─────────────────┘     └─────────────┘     └─────────────┘
```

## Requirements

- Python 3.10+
- curl
- [nanobanana MCP server](https://github.com/zhongweili/nanobanana-mcp-server) (for generation)

## File retention

0x0.st keeps files for 30 days to 1 year depending on size. Smaller files last longer.

---

*Built with Claude Code*

🤖 Generated with [Claude Code](https://claude.com/claude-code)
