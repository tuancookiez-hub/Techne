"""Composite Techne banner: 4K 21:9 mood board layout."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

# Target: 3840 x 1664 (21:9 at 4K)
W, H = 3840, 1664
GUTTER = 8  # px between panels

# Layout (left to right):
# [hero] [top_mid] [top_right] [far_top]
# [hero] [bot_mid] [bot_right] [far_bot]
# hero = 1280x1664
# mid = 1024x832 each (top/bot stacked)
# right = 768x832 each (top/bot stacked)
# far = 768x832 each (top/bot stacked)
# Check: 1280 + 1024 + 768 + 768 = 3840 ✓
#        832 + 832 = 1664 ✓

hero_w = 1280
mid_w = 1024
right_w = 768
far_w = 768
panel_h = H // 2  # 832

# Load panels
panels_dir = "banner_panels"
hero = Image.open(os.path.join(panels_dir, "panel_hero.jpg")).convert("RGB")
top_mid = Image.open(os.path.join(panels_dir, "panel_top_mid.jpg")).convert("RGB")
bot_mid = Image.open(os.path.join(panels_dir, "panel_bot_mid.jpg")).convert("RGB")
top_right = Image.open(os.path.join(panels_dir, "panel_top_right.jpg")).convert("RGB")
bot_right = Image.open(os.path.join(panels_dir, "panel_bot_right.jpg")).convert("RGB")
far_top = Image.open(os.path.join(panels_dir, "panel_far_top.jpg")).convert("RGB")
far_bot = Image.open(os.path.join(panels_dir, "panel_far_bot.jpg")).convert("RGB")

# Resize to target dimensions
hero = hero.resize((hero_w, H), Image.Resampling.LANCZOS)
top_mid = top_mid.resize((mid_w, panel_h), Image.Resampling.LANCZOS)
bot_mid = bot_mid.resize((mid_w, panel_h), Image.Resampling.LANCZOS)
top_right = top_right.resize((right_w, panel_h), Image.Resampling.LANCZOS)
bot_right = bot_right.resize((right_w, panel_h), Image.Resampling.LANCZOS)
far_top = far_top.resize((far_w, panel_h), Image.Resampling.LANCZOS)
far_bot = far_bot.resize((far_w, panel_h), Image.Resampling.LANCZOS)

# Create canvas
canvas = Image.new("RGB", (W, H), "#0A0A1A")

# Paste panels
# Hero (full height left)
canvas.paste(hero, (0, 0))
# Mid column
x_mid = hero_w + GUTTER
canvas.paste(top_mid, (x_mid, 0))
canvas.paste(bot_mid, (x_mid, panel_h + GUTTER))
# Right column
x_right = x_mid + mid_w + GUTTER
canvas.paste(top_right, (x_right, 0))
canvas.paste(bot_right, (x_right, panel_h + GUTTER))
# Far column
x_far = x_right + right_w + GUTTER
canvas.paste(far_top, (x_far, 0))
canvas.paste(far_bot, (x_far, panel_h + GUTTER))

# Add text overlays
draw = ImageDraw.Draw(canvas)

# Try to load a font, fallback to default
try:
    # Try system fonts
    font_paths = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/ARLRDBD.TTF",  # Arial Rounded Bold
        "C:/Windows/Fonts/segoeuib.ttf",   # Segoe UI Bold
    ]
    title_font = None
    for fp in font_paths:
        if os.path.exists(fp):
            title_font = ImageFont.truetype(fp, 120)
            subtitle_font = ImageFont.truetype(fp, 48)
            tag_font = ImageFont.truetype(fp, 32)
            break
    if title_font is None:
        raise IOError("No font found")
except Exception:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    tag_font = ImageFont.load_default()

# Title: TECHNE — positioned over hero panel, bottom-left
# Add semi-transparent dark overlay for text readability
overlay = Image.new("RGBA", (hero_w, 400), (10, 10, 26, 180))
canvas_rgba = canvas.convert("RGBA")
# Paste overlay at bottom-left of hero panel
canvas_rgba.paste(overlay, (0, H-400), overlay)
canvas = canvas_rgba.convert("RGB")
draw = ImageDraw.Draw(canvas)

# Draw text with subtle shadow
shadow_color = "#000000"
text_color = "#F7EDE3"
accent_color = "#00AEEF"

# TECHNE title
x_title = 60
y_title = H - 320
draw.text((x_title+3, y_title+3), "TECHNE", font=title_font, fill=shadow_color)
draw.text((x_title, y_title), "TECHNE", font=title_font, fill=text_color)

# Subtitle
y_sub = y_title + 140
draw.text((x_title+2, y_sub+2), "Model-Agnostic Visual Identity", font=subtitle_font, fill=shadow_color)
draw.text((x_title, y_sub), "Model-Agnostic Visual Identity", font=subtitle_font, fill=text_color)

# Tagline
y_tag = y_sub + 70
draw.text((x_title+1, y_tag+1), "Forked from Nous Research · Adapted for any AI model", font=tag_font, fill=shadow_color)
draw.text((x_title, y_tag), "Forked from Nous Research · Adapted for any AI model", font=tag_font, fill=accent_color)

# Add small label on top-right area
label_text = "4K 21:9"
draw.text((W-200, 30), label_text, font=tag_font, fill=(255,255,255,128))

# Save raw composite
os.makedirs("output", exist_ok=True)
raw_path = "output/techne_banner_4k_raw.png"
canvas.save(raw_path, "PNG")
print(f"Saved raw composite: {raw_path} ({canvas.size})")

# Also save as JPG for smaller size
jpg_path = "output/techne_banner_4k_raw.jpg"
canvas.save(jpg_path, "JPEG", quality=95)
print(f"Saved raw composite JPG: {jpg_path}")
