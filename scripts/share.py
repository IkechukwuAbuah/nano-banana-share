#!/usr/bin/env python3
"""Upload nanobanana images to 0x0.st for sharing."""
import subprocess
import sys
from pathlib import Path

OUTPUT_DIR = Path.home() / "nanobanana-images"


def get_latest_image() -> Path | None:
    """Get most recent PNG (excluding thumbnails)."""
    pngs = sorted(
        OUTPUT_DIR.glob("*.png"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    for p in pngs:
        if "_thumb" not in p.name:
            return p
    return None


def upload(image_path: Path) -> str:
    """Upload to 0x0.st, return URL."""
    result = subprocess.run(
        [
            "curl", "-s",
            "-A", "nano-banana-share/1.0",
            "-F", f"file=@{image_path}",
            "https://0x0.st"
        ],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Upload failed: {result.stderr}")
    return result.stdout.strip()


def main():
    # Parse argument
    if len(sys.argv) < 2 or sys.argv[1] == "latest":
        image = get_latest_image()
        if not image:
            print("No images found in ~/nanobanana-images/", file=sys.stderr)
            sys.exit(1)
    else:
        image = Path(sys.argv[1]).expanduser()

    if not image.exists():
        print(f"Image not found: {image}", file=sys.stderr)
        sys.exit(1)

    # Upload and print URL
    try:
        url = upload(image)
        print(url)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
