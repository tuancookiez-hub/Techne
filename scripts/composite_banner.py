"""Composite Nous Branding banner: 3:2 aspect ratio matching Theia upstream."""
import os
from PIL import Image, ImageDraw, ImageFont

# Target: 2400 x 1600 (3:2, matching Theia's 1280x853 aspect ratio)
# Scaled up for retina displays
W, H = 2400, 1600
GUTTER = 12
PANEL_DIR = "banner_panels"
OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

# Colors
BG = (11, 11, 14)
PANEL_BORDER = (26, 26, 26)
FOOTER_BG = (230, 230, 230)

# Layout: match Theia exactly
# 4 cols x 6 rows + footer
# Content = 93% height, footer = 7%
content_h = int(H * 0.93)
footer_h = H - content_h

# 6 rows + 5 gutters
row_h = (content_h - 5 * GUTTER) // 6
# 4 cols + 3 gutters
col_w = (W - 3 * GUTTER) // 4

print(f"Layout: {W}x{H} ({W/H:.2f}:1), cells={col_w}x{row_h}, footer={footer_h}px")

def load_panel(name, size):
    for ext in [".png", ".jpg", ".jpeg"]:
        path = os.path.join(PANEL_DIR, f"{name}{ext}")
        if os.path.exists(path):
            img = Image.open(path).convert("RGB")
            # Crop to target aspect ratio before resizing to avoid distortion
            target_w, target_h = size
            target_ratio = target_w / target_h
            img_w, img_h = img.size
            img_ratio = img_w / img_h
            
            if img_ratio > target_ratio:
                # Image is wider than target — crop width
                new_w = int(img_h * target_ratio)
                left = (img_w - new_w) // 2
                img = img.crop((left, 0, left + new_w, img_h))
            else:
                # Image is taller than target — crop height
                new_h = int(img_w / target_ratio)
                top = (img_h - new_h) // 2
                img = img.crop((0, top, img_w, top + new_h))
            
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

# Panel positions matching Theia layout exactly
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
        draw.rectangle([x, y, x + w - 1, y + h - 1], outline=PANEL_BORDER, width=2)
    except FileNotFoundError:
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

try:
    footer_font = get_font(16, bold=False)
    seg_w = W // len(footer_text)
    for i, text in enumerate(footer_text):
        x = i * seg_w + 15
        y = footer_y + (footer_h - 16) // 2
        draw.text((x, y), text, fill=(20, 20, 20), font=footer_font)
except Exception as e:
    print(f"Footer text error: {e}")

# ─── Save ─────────────────────────────────────────────────────
raw_path = os.path.join(OUT_DIR, "nous-branding-banner-composite-raw.png")
canvas.save(raw_path, "PNG", optimize=True)
print(f"Saved: {raw_path} ({canvas.size})")

jpg_path = os.path.join(OUT_DIR, "nous-branding-banner-composite-raw.jpg")
canvas.save(jpg_path, "JPEG", quality=92, optimize=True)
print(f"Saved: {jpg_path}")
