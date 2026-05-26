"""Composite 9-style banner: 2x3 grid + portrait hero + accents, with NOUS text."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 3840, 1664  # 21:9 banner
GUTTER = 16
BG = (11, 11, 14)

PANEL_DIR = "style_panels"
OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

# Layout:
# Left: 2x3 grid (2 cols, 3 rows = 6 panels) - TALL panels
# Right: Portrait hero (tall, narrow) + 2 accent panels stacked
# Big NOUS text

grid_cols, grid_rows = 2, 3
grid_w = int(W * 0.40)  # Left 40% for tall grid
right_w = W - grid_w - GUTTER  # Right 60% for portrait + accents

grid_cell_w = (grid_w - (grid_cols - 1) * GUTTER) // grid_cols
grid_cell_h = (H - (grid_rows - 1) * GUTTER) // grid_rows

hero_w = int(right_w * 0.55)  # Portrait hero is narrow
hero_h = H
accent_w = right_w - hero_w - GUTTER
accent_h = (H - GUTTER) // 2

print(f"Layout: {W}x{H}")
print(f"Grid: {grid_w}x{H}, cells={grid_cell_w}x{grid_cell_h}")
print(f"Hero: {hero_w}x{hero_h} (portrait)")
print(f"Accents: {accent_w}x{accent_h}")

panels = [
    "01_retro_media", "02_analog_newspaper", "03_hermetic_print",
    "04_cyanotype_city", "05_network_diagram", "06_veiled_classical",
    "07_planetary_broadcast", "08_manufactured_multiples", "09_motorsport",
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

# Place 2x3 grid (panels 0-5) on the LEFT
for i in range(6):
    col = i % grid_cols
    row = i // grid_cols
    x = col * (grid_cell_w + GUTTER)
    y = row * (grid_cell_h + GUTTER)
    panel = load_panel(panels[i], (grid_cell_w, grid_cell_h))
    banner.paste(panel, (x, y))
    
    # Label
    label = panels[i].split("_", 1)[1].replace("_", " ").upper()
    bbox = draw.textbbox((0, 0), label)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    label_bg = Image.new("RGBA", (text_w + 8, text_h + 4), (0, 0, 0, 180))
    banner.paste(label_bg, (x + 4, y + 4), label_bg)
    draw.text((x + 8, y + 6), label, fill=(255, 255, 255))

# Right side: Portrait hero (panel 6 - planetary broadcast)
hero_x = grid_w + GUTTER
hero_y = 0
hero = load_panel(panels[6], (hero_w, hero_h))
banner.paste(hero, (hero_x, hero_y))

# 2 accent panels stacked to the RIGHT of hero (panels 7, 8)
for i, idx in enumerate([7, 8]):
    x = hero_x + hero_w + GUTTER
    y = i * (accent_h + GUTTER)
    panel = load_panel(panels[idx], (accent_w, accent_h))
    banner.paste(panel, (x, y))
    
    label = panels[idx].split("_", 1)[1].replace("_", " ").upper()
    bbox = draw.textbbox((0, 0), label)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    label_bg = Image.new("RGBA", (text_w + 8, text_h + 4), (0, 0, 0, 180))
    banner.paste(label_bg, (x + 4, y + 4), label_bg)
    draw.text((x + 8, y + 6), label, fill=(255, 255, 255))

# Big NOUS text overlay (bottom left, over grid area)
try:
    font = ImageFont.truetype("C:/Windows/Fonts/Impact.ttf", 200)
except:
    font = ImageFont.load_default()

text = "NOUS"
bbox = draw.textbbox((0, 0), text, font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]
text_x = 40
text_y = H - text_h - 40

# Text shadow
draw.text((text_x + 6, text_y + 6), text, font=font, fill=(0, 0, 0))
# Text
draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))

# Save
banner.save(os.path.join(OUT_DIR, "nous-styles-banner-raw.png"), "PNG")
banner.save(os.path.join(OUT_DIR, "nous-styles-banner-raw.jpg"), "JPEG", quality=92)
print(f"Saved: {os.path.join(OUT_DIR, 'nous-styles-banner-raw.jpg')}")
