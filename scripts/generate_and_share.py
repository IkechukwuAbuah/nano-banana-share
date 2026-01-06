#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Generate images with Gemini and upload to 0x0.st for shareable URLs.

Usage:
    uv run generate_and_share.py "a cute robot mascot"
    uv run generate_and_share.py "edit: make background blue" --input image.png
    uv run generate_and_share.py "sunset mountains" --resolution 2K --no-upload
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


OUTPUT_DIR = Path.home() / "nanobanana-images"


def get_api_key() -> str | None:
    return os.environ.get("GEMINI_API_KEY")


def generate_image(prompt: str, input_image: Path | None, resolution: str) -> Path:
    """Generate image using Gemini, return local path."""
    from google import genai
    from google.genai import types
    from PIL import Image as PILImage
    from io import BytesIO

    api_key = get_api_key()
    if not api_key:
        print("Error: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Build contents
    if input_image:
        img = PILImage.open(input_image)
        contents = [img, prompt]
        print(f"Editing image: {input_image}")
    else:
        contents = prompt
        print(f"Generating: {prompt[:50]}...")

    # Generate
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(image_size=resolution)
        )
    )

    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"gen_{timestamp}.png"

    for part in response.parts:
        if part.text:
            print(f"Model: {part.text}")
        elif part.inline_data:
            image_data = part.inline_data.data
            if isinstance(image_data, str):
                import base64
                image_data = base64.b64decode(image_data)

            image = PILImage.open(BytesIO(image_data))
            if image.mode == 'RGBA':
                rgb = PILImage.new('RGB', image.size, (255, 255, 255))
                rgb.paste(image, mask=image.split()[3])
                rgb.save(str(output_path), 'PNG')
            else:
                image.convert('RGB').save(str(output_path), 'PNG')

            print(f"Saved: {output_path}")
            return output_path

    print("Error: No image in response", file=sys.stderr)
    sys.exit(1)


def upload(image_path: Path) -> str:
    """Upload to 0x0.st, return URL."""
    result = subprocess.run(
        ["curl", "-s", "-A", "nano-banana-share/1.0", "-F", f"file=@{image_path}", "https://0x0.st"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Upload failed: {result.stderr}")
    return result.stdout.strip()


def main():
    parser = argparse.ArgumentParser(description="Generate image and get shareable URL")
    parser.add_argument("prompt", help="Image description or edit instructions")
    parser.add_argument("--input", "-i", type=Path, help="Input image for editing")
    parser.add_argument("--resolution", "-r", choices=["1K", "2K", "4K"], default="1K")
    parser.add_argument("--no-upload", action="store_true", help="Skip upload, return local path")
    args = parser.parse_args()

    try:
        # Generate
        local_path = generate_image(args.prompt, args.input, args.resolution)

        # Upload (unless --no-upload)
        if args.no_upload:
            print(f"\nLocal: {local_path}")
        else:
            print("Uploading...")
            url = upload(local_path)
            print(f"\nURL: {url}")
            print(f"Local: {local_path}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
