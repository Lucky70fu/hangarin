from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent
ICON_DIR = BASE_DIR / "static" / "images" / "icons"

source = ICON_DIR / "icon-512x512.png"

sizes = [72, 96, 128, 144, 152, 192, 384, 512]

if not source.exists():
    raise FileNotFoundError(
        f"Source icon not found: {source}"
    )

image = Image.open(source).convert("RGBA")

for size in sizes:
    output = ICON_DIR / f"icon-{size}x{size}.png"

    resized = image.resize(
        (size, size),
        Image.Resampling.LANCZOS
    )

    resized.save(output, "PNG")
    print(f"Created: {output}")

print("\nAll PWA icons created successfully!")