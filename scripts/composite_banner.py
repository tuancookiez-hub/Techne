"""Composite Nous Branding banner: 4K 21:9 mood board layout."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

W, H = 3840, 1664
GUTTER = 16
PANEL_DIR = "banner_panels"
OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

# Colors
BG = (11, 11, 14)  # #0B0B0E
PANEL_BORDER = (26, 26, 26)
FOOTER_BG = (230, 230, 230)
TEXT_WHITE = (245, 245, 255)
TEXT_BLUE = (40, 71, 255)
TEXT_GOLD = (214, 178, 90)
TEXT_GRAY = (140, 160, 190)

# Layout calculations (matching Theia banner)
# 4 cols x 6 rows + footer
# Content area = 93% of height, footer = 7%
content_h = int(H * 0.93)
footer_h = H - content_h - GUTTER

# 6 rows + 5 gutters in content area
row_h = (content_h - 5 * GUTTER) // 6
# 4 cols + 3 gutters in width
col_w = (W - 3 * GUTTER) // 4

print(f"Layout: {col_w}x{row_h} cells, footer={footer_h}px")

def load_panel(name, size):
    for ext in [".png", ".jpg", ".jpeg"]:
        path = os.path.join(PANEL_DIR, f"{name}{ext}")
        if os.path.exists(path):
            img = Image.open(path).convert("RGB")
            return img.resize(size, Image.LANCZOS)
    raise FileNotFoundError(f"Panel not found: {name}")

def get_font(size, bold=True):
    weight = "bd" if bold else ""
    candidates = [
        f"C:/Windows/Fonts/arial{weight}.ttf",
        f"C:/Windows/Fonts/segoeui{weight}.ttf",
        f"C:/Windows/Fonts/calibri{weight}.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

# ─── Build canvas ─────────────────────────────────────────────
canvas = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(canvas)

# Panel positions (x, y, w, h)
panels = {
    "hero": (0, 0, col_w, row_h * 4 + GUTTER * 3),
    "identity": (col_w + GUTTER, 0, col_w, row_h * 4 + GUTTER * 3),
    "top_zine": (2 * (col_w + GUTTER), 0, col_w, row_h * 2 + GUTTER),
    "bot_zine": (2 * (col_w + GUTTER), 2 * (row_h + GUTTER), col_w, row_h * 2 + GUTTER),
    "system_diagram": (3 * (col_w + GUTTER), 0, col_w, row_h * 2 + GUTTER),
    "field_note": (3 * (col_w + GUTTER), 2 * (row_h + GUTTER), col_w, row_h * 2 + GUTTER),
    "symbols": (0, 4 * (row_h + GUTTER), col_w, row_h * 2 + GUTTER),
    "anime_portal": (col_w + GUTTER, 4 * (row_h + GUTTER), col_w * 2 + GUTTER, row_h * 2 + GUTTER),
    "layout_refs": (3 * (col_w + GUTTER), 4 * (row_h + GUTTER), col_w, row_h * 2 + GUTTER),
}

# Place panels
for name, (x, y, w, h) in panels.items():
    try:
        panel = load_panel(name, (w, h))
        canvas.paste(panel, (x, y))
        # Draw border
        draw.rectangle([x, y, x + w - 1, y + h - 1], outline=PANEL_BORDER, width=2)
    except FileNotFoundError:
        # Fill with placeholder color if panel missing
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(30, 30, 35), outline=PANEL_BORDER, width=2)
        print(f"  Warning: panel '{name}' not found, using placeholder")

# ─── Footer ───────────────────────────────────────────────────
footer_y = 6 * (row_h + GUTTER)
draw.rectangle([0, footer_y, W - 1, H - 1], fill=FOOTER_BG)

footer_text = [
    "NOUS BRANDING IS HOW HERMES CREATES.",
    "VISUAL IDENTITY FOR THE OPEN FUTURE.",
    "PERCEPTION. REASONING. ACTION.",
    "BUILT BY NOUS. FOR ANY MODEL.",
    "NOUSRESEARCH.COM"
]

# Draw footer text segments
try:
    footer_font = get_font(24, bold=False)
    seg_w = W // len(footer_text)
    for i, text in enumerate(footer_text):
        x = i * seg_w + 20
        y = footer_y + (footer_h - 24) // 2
        draw.text((x, y), text, fill=(20, 20, 20), font=footer_font)
except Exception as e:
    print(f"Footer text error: {e}")

# ─── Save ─────────────────────────────────────────────────────
raw_path = os.path.join(OUT_DIR, "nous-branding-banner-composite-raw.png")
canvas.save(raw_path, "PNG", optimize=True)
print(f"Saved: {raw_path} ({canvas.size})")

# Also save JPG
jpg_path = os.path.join(OUT_DIR, "nous-branding-banner-composite-raw.jpg")
canvas.save(jpg_path, "JPEG", quality=92, optimize=True)
print(f"Saved: {jpg_path}")
