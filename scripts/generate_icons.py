#!/usr/bin/env python3
"""Generate PWA icons from the logo."""

from pathlib import Path
from PIL import Image

def generate_icons():
    """Generate PWA icons in various sizes."""
    # Paths
    logo_path = Path(__file__).parent.parent / "app" / "assets" / "logo.png"
    static_path = Path(__file__).parent.parent / "app" / "static"

    # Ensure static folder exists
    static_path.mkdir(exist_ok=True)

    # Load logo
    logo = Image.open(logo_path)

    # Convert to RGBA if needed
    if logo.mode != 'RGBA':
        logo = logo.convert('RGBA')

    # Create a square canvas with the logo centered
    size = max(logo.size)
    square = Image.new('RGBA', (size, size), (14, 17, 23, 255))  # #0E1117 background

    # Center the logo
    x = (size - logo.size[0]) // 2
    y = (size - logo.size[1]) // 2
    square.paste(logo, (x, y), logo)

    # Generate different sizes
    sizes = [
        (192, "icon-192.png"),
        (512, "icon-512.png"),
        (180, "apple-touch-icon.png"),
        (152, "icon-152.png"),
        (144, "icon-144.png"),
        (96, "icon-96.png"),
        (72, "icon-72.png"),
        (48, "icon-48.png"),
    ]

    for icon_size, filename in sizes:
        resized = square.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        output_path = static_path / filename
        resized.save(output_path, "PNG")
        print(f"Created: {output_path}")

    # Also create favicon.ico
    favicon_sizes = [(16, 16), (32, 32), (48, 48)]
    favicon_images = []
    for fsize in favicon_sizes:
        favicon_images.append(square.resize(fsize, Image.Resampling.LANCZOS))

    favicon_path = static_path / "favicon.ico"
    favicon_images[0].save(
        favicon_path,
        format='ICO',
        sizes=[(16, 16), (32, 32), (48, 48)]
    )
    print(f"Created: {favicon_path}")

    print("\nAll icons generated successfully!")

if __name__ == "__main__":
    generate_icons()
