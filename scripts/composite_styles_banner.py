"""Composite 9-style banner matching upstream Theia layout.

Layout:
- Top-left: Hero poster (NOUS CREATE)
- Below hero: 2 panels stacked
- Right of hero: 6 panels in 3x2 grid
- Footer: Full-width text banner at bottom

No stretching. Original sizes with black gutters.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 3840, 2400  # Taller for footer
GUTTER = 20
BG = (11, 11, 14)
FOOTER_H = 120

PANEL_DIR = "style_panels"
OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

# Available space for panels (above footer)
content_h = H - FOOTER_H - GUTTER

# Left column: hero poster + 2 panels below
left_w = int(W * 0.35)  # 35% width for left column
right_w = W - left_w - GUTTER  # 65% for right grid

# Hero takes top 60% of left column
hero_h = int(content_h * 0.60)
# 2 panels below share remaining 40%
left_bottom_h = (content_h - hero_h - GUTTER) // 2

# Right side: 3x2 grid
grid_cols, grid_rows = 3, 2
grid_cell_w = (right_w - (grid_cols - 1) * GUTTER) // grid_cols
grid_cell_h = (content_h - (grid_rows - 1) * GUTTER) // grid_rows

print(f"Layout: {W}x{H}")
print(f"Left: {left_w}x{content_h}, hero={left_w}x{hero_h}, bottom={left_w}x{left_bottom_h}")
print(f"Right grid: {right_w}x{content_h}, cells={grid_cell_w}x{grid_cell_h}")

HERO = "00_nous_create_poster"
left_bottom = ["07_planetary_broadcast", "08_manufactured_multiples"]
right_grid = [
    "01_retro_media", "02_analog_newspaper", "03_hermetic_print",
    "04_cyanotype_city", "05_network_diagram", "06_veiled_classical",
]

def load_panel(name, size):
    """Load panel and fit within size without stretching."""
    for ext in [".png", ".jpg", ".jpeg"]:
        path = os.path.join(PANEL_DIR, f"{name}{ext}")
        if os.path.exists(path):
            img = Image.open(path).convert("RGB")
            target_w, target_h = size
            img_ratio = img.width / img.height
            target_ratio = target_w / target_h
            
            # Always preserve aspect ratio — never stretch
            if img_ratio > target_ratio:
                new_w = target_w
                new_h = int(target_w / img_ratio)
            else:
                new_h = target_h
                new_w = int(target_h * img_ratio)
            
            img = img.resize((new_w, new_h), Image.LANCZOS)
            canvas = Image.new("RGB", size, BG)
            # Center the image
            paste_x = (target_w - new_w) // 2
            paste_y = (target_h - new_h) // 2
            canvas.paste(img, (paste_x, paste_y))
            return canvas
    raise FileNotFoundError(f"Panel not found: {name}")

banner = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(banner)

# ─── Left column ──────────────────────────────────────────────

# Hero poster (top-left)
hero = load_panel(HERO, (left_w, hero_h))
banner.paste(hero, (0, 0))

# 2 panels below hero
for i, name in enumerate(left_bottom):
    y = hero_h + GUTTER + i * (left_bottom_h + GUTTER)
    panel = load_panel(name, (left_w, left_bottom_h))
    banner.paste(panel, (0, y))

# ─── Right grid (3x2) ─────────────────────────────────────────

for i, name in enumerate(right_grid):
    col = i % grid_cols
    row = i // grid_cols
    x = left_w + GUTTER + col * (grid_cell_w + GUTTER)
    y = row * (grid_cell_h + GUTTER)
    panel = load_panel(name, (grid_cell_w, grid_cell_h))
    banner.paste(panel, (x, y))

# ─── Footer ───────────────────────────────────────────────────

footer_y = content_h + GUTTER
footer = Image.new("RGB", (W, FOOTER_H), (230, 230, 230))  # Light gray like Theia
draw_footer = ImageDraw.Draw(footer)

try:
    font = ImageFont.truetype("C:/Windows/Fonts/Consolas.ttf", 28)
except:
    font = ImageFont.load_default()

footer_text = "NOUS BRANDING IS HOW HERMES CREATES.  *  VISUAL IDENTITY FOR THE OPEN FUTURE.  *  PERCEPTION. REASONING. ACTION.  *  BUILT BY NOUS. FOR ANY MODEL.  *  NOUSRESEARCH.COM"
bbox = draw_footer.textbbox((0, 0), footer_text, font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]
text_x = (W - text_w) // 2
text_y = (FOOTER_H - text_h) // 2

draw_footer.text((text_x, text_y), footer_text, font=font, fill=(20, 20, 20))
banner.paste(footer, (0, footer_y))

# Save
banner.save(os.path.join(OUT_DIR, "nous-styles-banner-raw.png"), "PNG")
banner.save(os.path.join(OUT_DIR, "nous-styles-banner-raw.jpg"), "JPEG", quality=92)
print(f"Saved: {os.path.join(OUT_DIR, 'nous-styles-banner-raw.jpg')}")
