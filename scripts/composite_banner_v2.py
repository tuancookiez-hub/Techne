"""Composite Techne banner v2: 4K 21:9 with proper text overlays."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

# Target: 3840 x 1664 (21:9 at 4K)
W, H = 3840, 1664
GUTTER = 24
PANEL_DIR = "banner_panels_v2"
OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

def load_panel(name, target_size):
    """Load panel and resize to target."""
    path = os.path.join(PANEL_DIR, f"{name}.png")
    img = Image.open(path).convert("RGB")
    # Resize with high-quality downsampling
    img = img.resize(target_size, Image.LANCZOS)
    return img

def add_noise(img, intensity=8):
    arr = np.array(img).astype(np.int16)
    noise = np.random.normal(0, intensity, arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def add_vignette(img, intensity=0.25):
    w, h = img.size
    vignette = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(vignette)
    margin = int(min(w, h) * 0.15)
    for i in range(margin):
        alpha = int(255 * (i / margin) * intensity)
        draw.rectangle([i, i, w - 1 - i, h - 1 - i], outline=alpha)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=margin // 2))
    img_rgba = img.convert("RGBA")
    vig_rgba = Image.merge("RGBA", (
        Image.new("L", (w, h), 0),
        Image.new("L", (w, h), 0),
        Image.new("L", (w, h), 0),
        vignette
    ))
    result = Image.alpha_composite(img_rgba, vig_rgba)
    return result.convert("RGB")

# ─── Layout calculations ──────────────────────────────────────
# Left hero: full height, ~38% width
hero_w = int(W * 0.38)
hero_h = H

# Right area: remaining width, split into 2 rows x 3 cols
right_w = W - hero_w - GUTTER
right_x = hero_w + GUTTER

# Each small panel
col_w = (right_w - 2 * GUTTER) // 3
row_h = (H - GUTTER) // 2

# Load panels
hero = load_panel("hero", (hero_w, hero_h))
top_mid = load_panel("top_mid", (col_w, row_h))
top_right = load_panel("top_right", (col_w, row_h))
far_top = load_panel("far_top", (col_w, row_h))
bot_mid = load_panel("bot_mid", (col_w, row_h))
bot_right = load_panel("bot_right", (col_w, row_h))
far_bot = load_panel("far_bot", (col_w, row_h))

# ─── Assemble canvas ──────────────────────────────────────────
canvas = Image.new("RGB", (W, H), (15, 15, 25))

# Place hero
canvas.paste(hero, (0, 0))

# Place small panels (row 0)
canvas.paste(top_mid, (right_x, 0))
canvas.paste(top_right, (right_x + col_w + GUTTER, 0))
canvas.paste(far_top, (right_x + 2 * (col_w + GUTTER), 0))

# Place small panels (row 1)
canvas.paste(bot_mid, (right_x, row_h + GUTTER))
canvas.paste(bot_right, (right_x + col_w + GUTTER, row_h + GUTTER))
canvas.paste(far_bot, (right_x + 2 * (col_w + GUTTER), row_h + GUTTER))

# ─── Add text overlays ────────────────────────────────────────
# Try to load a font, fall back to default
try:
    # Try system fonts
    font_paths = [
        "C:/Windows/Fonts/arialbd.ttf",      # Arial Bold
        "C:/Windows/Fonts/segoeuib.ttf",     # Segoe UI Bold
        "C:/Windows/Fonts/calibrib.ttf",     # Calibri Bold
    ]
    title_font = None
    subtitle_font = None
    body_font = None
    small_font = None
    
    for fp in font_paths:
        if os.path.exists(fp):
            title_font = ImageFont.truetype(fp, 120)
            subtitle_font = ImageFont.truetype(fp, 48)
            body_font = ImageFont.truetype(fp, 36)
            small_font = ImageFont.truetype(fp, 28)
            break
    
    if title_font is None:
        raise IOError("No system font found")
        
except Exception:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    body_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

draw = ImageDraw.Draw(canvas)

# Title block over hero panel, bottom-left
# Add semi-transparent dark overlay for text readability
overlay = Image.new("RGBA", (hero_w, 400), (10, 10, 26, 200))
canvas_rgba = canvas.convert("RGBA")
canvas_rgba.paste(overlay, (0, H - 400), overlay)
canvas = canvas_rgba.convert("RGB")
draw = ImageDraw.Draw(canvas)

# Title: TECHNE
draw.text((60, H - 340), "TECHNE", font=title_font, fill=(245, 245, 255))

# Subtitle
draw.text((60, H - 200), "Model-Agnostic Visual Identity", font=subtitle_font, fill=(200, 210, 230))

# Tagline
draw.text((60, H - 130), "Forked from Nous Research  ·  Adapted for any AI model", font=body_font, fill=(140, 160, 190))

# Small panel labels (optional — clean minimal style)
label_color = (180, 190, 210)
label_bg = (10, 10, 26, 160)

def draw_label(draw, x, y, text, font, text_color, bg_color):
    """Draw text with a small semi-transparent background for readability."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    # Draw background
    draw.rectangle([x - 8, y - 4, x + tw + 8, y + th + 4], fill=bg_color)
    # Draw text
    draw.text((x, y), text, font=font, fill=text_color)

# Top row labels
draw_label(draw, right_x + 20, 20, "CRAFT", small_font, label_color, label_bg)
draw_label(draw, right_x + col_w + GUTTER + 20, 20, "ANALOG → DIGITAL", small_font, label_color, label_bg)
draw_label(draw, right_x + 2 * (col_w + GUTTER) + 20, 20, "CLASSICAL × CODE", small_font, label_color, label_bg)

# Bottom row labels
draw_label(draw, right_x + 20, row_h + GUTTER + 20, "NEURAL MEANDER", small_font, label_color, label_bg)
draw_label(draw, right_x + col_w + GUTTER + 20, row_h + GUTTER + 20, "TECH MANUALS", small_font, label_color, label_bg)
draw_label(draw, right_x + 2 * (col_w + GUTTER) + 20, row_h + GUTTER + 20, "HALFTONE", small_font, label_color, label_bg)

# Corner badge
draw_label(draw, W - 200, 20, "4K 21:9", small_font, (100, 110, 130), label_bg)

# ─── Final effects ────────────────────────────────────────────
canvas = add_noise(canvas, intensity=5)
canvas = add_vignette(canvas, intensity=0.15)

# Save raw composite
raw_path = os.path.join(OUT_DIR, "techne_banner_v2_raw.png")
canvas.save(raw_path, "PNG", optimize=True)
print(f"Saved raw composite: {raw_path} ({canvas.size})")

# Also save as JPG for smaller size
jpg_path = os.path.join(OUT_DIR, "techne_banner_v2_raw.jpg")
canvas.save(jpg_path, "JPEG", quality=92, optimize=True)
print(f"Saved raw composite JPG: {jpg_path}")
