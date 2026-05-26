"""Composite Nous Branding banner: 4K 21:9 mood board layout.
Panels are NEVER stretched. If aspect ratios don't match, letterbox with black."""
import os
from PIL import Image, ImageDraw, ImageFont

# 21:9 ultrawide at 4K
W, H = 3840, 1664
GUTTER = 16
PANEL_DIR = "banner_panels"
OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

# Colors
BG = (11, 11, 14)
PANEL_BORDER = (26, 26, 26)
FOOTER_BG = (230, 230, 230)

# Layout: 4 cols x 6 rows + footer
# Hero + Identity are tall (rows 1-4)
# Zines + Diagrams are square-ish (rows 1-2, 3-4)
# Bottom row (rows 5-6): symbols, anime_portal, layout_refs
# Footer: row 7

content_h = int(H * 0.93)
footer_h = H - content_h

row_h = (content_h - 5 * GUTTER) // 6
col_w = (W - 3 * GUTTER) // 4

print(f"Layout: {W}x{H} (21:9), cells={col_w}x{row_h}, footer={footer_h}px")

def load_panel(name, size):
    """Load panel and fit within size.
    Uses slight stretch if ratios are close (within 15%), otherwise letterbox."""
    for ext in [".png", ".jpg", ".jpeg"]:
        path = os.path.join(PANEL_DIR, f"{name}{ext}")
        if os.path.exists(path):
            img = Image.open(path).convert("RGB")
            target_w, target_h = size
            
            img_ratio = img.width / img.height
            target_ratio = target_w / target_h
            ratio_diff = abs(img_ratio - target_ratio) / max(img_ratio, target_ratio)
            
            # If ratios are close (within 50%), stretch to fill
            # This eliminates black space for square images in wide slots
            if ratio_diff < 0.50:
                return img.resize((target_w, target_h), Image.LANCZOS)
            
            # Otherwise use fit mode (preserve aspect ratio, letterbox)
            if img_ratio > target_ratio:
                new_w = target_w
                new_h = int(target_w / img_ratio)
            else:
                new_h = target_h
                new_w = int(target_h * img_ratio)
            
            img = img.resize((new_w, new_h), Image.LANCZOS)
            canvas = Image.new("RGB", size, BG)
            # Align to top-left instead of centering — black space goes to right/bottom
            paste_x = 0
            paste_y = 0
            canvas.paste(img, (paste_x, paste_y))
            return canvas
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

# Panel positions
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

# Place panels (fit mode, no stretch)
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

jpg_path = os.path.join(OUT_DIR, "nous-branding-banner-composite-raw.jpg")
canvas.save(jpg_path, "JPEG", quality=92, optimize=True)
print(f"Saved: {jpg_path}")
