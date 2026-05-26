"""Composite 9-style banner: 3x3 grid showing all v11 Nous lanes."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2400, 2400  # Square 3x3 grid
GUTTER = 16
BG = (11, 11, 14)

PANEL_DIR = "style_panels"
OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

# 3x3 grid, each cell is equal size
cell_w = (W - 2 * GUTTER) // 3
cell_h = (H - 2 * GUTTER) // 3

print(f"Layout: {W}x{H} (3x3 grid), cells={cell_w}x{cell_h}")

panels = [
    "01_retro_media",
    "02_analog_newspaper", 
    "03_hermetic_print",
    "04_cyanotype_city",
    "05_network_diagram",
    "06_veiled_classical",
    "07_planetary_broadcast",
    "08_manufactured_multiples",
    "09_motorsport",
]

def load_panel(name, size):
    for ext in [".png", ".jpg", ".jpeg"]:
        path = os.path.join(PANEL_DIR, f"{name}{ext}")
        if os.path.exists(path):
            img = Image.open(path).convert("RGB")
            target_w, target_h = size
            img_ratio = img.width / img.height
            target_ratio = target_w / target_h
            ratio_diff = abs(img_ratio - target_ratio) / max(img_ratio, target_ratio)
            if ratio_diff < 0.50:
                return img.resize((target_w, target_h), Image.LANCZOS)
            if img_ratio > target_ratio:
                new_w, new_h = target_w, int(target_w / img_ratio)
            else:
                new_h, new_w = target_h, int(target_h * img_ratio)
            img = img.resize((new_w, new_h), Image.LANCZOS)
            canvas = Image.new("RGB", size, BG)
            canvas.paste(img, (0, 0))
            return canvas
    raise FileNotFoundError(f"Panel not found: {name}")

banner = Image.new("RGB", (W, H), BG)

draw = ImageDraw.Draw(banner)

for i, name in enumerate(panels):
    col = i % 3
    row = i // 3
    x = col * (cell_w + GUTTER)
    y = row * (cell_h + GUTTER)
    
    panel = load_panel(name, (cell_w, cell_h))
    banner.paste(panel, (x, y))
    
    # Add label
    label = name.replace("01_", "").replace("02_", "").replace("03_", "").replace("04_", "").replace("05_", "").replace("06_", "").replace("07_", "").replace("08_", "").replace("09_", "").replace("_", " ").upper()
    
    # Draw label background
    bbox = draw.textbbox((0, 0), label)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    label_bg = Image.new("RGBA", (text_w + 8, text_h + 4), (0, 0, 0, 180))
    banner.paste(label_bg, (x + 4, y + 4), label_bg)
    draw.text((x + 8, y + 6), label, fill=(255, 255, 255))

# Save
banner.save(os.path.join(OUT_DIR, "nous-styles-banner-raw.png"), "PNG")
banner.save(os.path.join(OUT_DIR, "nous-styles-banner-raw.jpg"), "JPEG", quality=92)
print(f"Saved: {os.path.join(OUT_DIR, 'nous-styles-banner-raw.jpg')}")
