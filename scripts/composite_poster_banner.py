"""Dense poster collage banner — multiple generated posters arranged like Theia reference.

Layout: Asymmetrical collage with varied panel sizes, no stretching, black gutters.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 3840, 2400
GUTTER = 16
BG = (11, 11, 14)
FOOTER_H = 100

PANEL_DIR = "style_panels"
OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

content_h = H - FOOTER_H - GUTTER

# Define panel placements: (name, x, y, w, h)
# Top row
placements = [
    # Large hero poster (top-left, spans 2 rows)
    ("00_nous_create_poster", 0, 0, 1000, 1260),
    
    # Top row right of hero
    ("eye_01", 1016, 0, 620, 620),
    ("anime_hero_01", 1652, 0, 620, 620),
    ("hermes_statue", 2288, 0, 620, 620),
    ("zine_cover_01", 2924, 0, 916, 620),
    
    # Second row
    ("symbols_grid", 1016, 636, 620, 620),
    ("anime_reading", 1652, 636, 620, 620),
    ("telescope", 2288, 636, 620, 620),
    ("field_note_01", 2924, 636, 916, 620),
    
    # Third row (below hero)
    ("01_retro_media", 0, 1276, 490, 490),
    ("02_analog_newspaper", 506, 1276, 490, 490),
    ("03_hermetic_print", 0, 1782, 490, 490),
    ("04_cyanotype_city", 506, 1782, 490, 490),
    
    # Third row right
    ("05_network_diagram", 1016, 1276, 790, 996),
    ("06_veiled_classical", 1822, 1276, 790, 996),
    ("07_planetary_broadcast", 2628, 1276, 620, 490),
    ("08_manufactured_multiples", 3264, 1276, 576, 490),
    ("09_motorsport", 2628, 1782, 620, 490),
    ("anime_window", 3264, 1782, 576, 490),
]

def load_panel(name, size):
    for ext in [".png", ".jpg", ".jpeg"]:
        path = os.path.join(PANEL_DIR, f"{name}{ext}")
        if os.path.exists(path):
            img = Image.open(path).convert("RGB")
            target_w, target_h = size
            img_ratio = img.width / img.height
            target_ratio = target_w / target_h
            
            # Preserve aspect ratio — never stretch
            if img_ratio > target_ratio:
                new_w = target_w
                new_h = int(target_w / img_ratio)
            else:
                new_h = target_h
                new_w = int(target_h * img_ratio)
            
            img = img.resize((new_w, new_h), Image.LANCZOS)
            canvas = Image.new("RGB", size, BG)
            paste_x = (target_w - new_w) // 2
            paste_y = (target_h - new_h) // 2
            canvas.paste(img, (paste_x, paste_y))
            return canvas
    raise FileNotFoundError(f"Panel not found: {name}")

banner = Image.new("RGB", (W, H), BG)

for name, x, y, pw, ph in placements:
    try:
        panel = load_panel(name, (pw, ph))
        banner.paste(panel, (x, y))
        print(f"  Placed: {name} at ({x},{y}) size {pw}x{ph}")
    except Exception as e:
        print(f"  ERROR {name}: {e}")

# Footer — more obvious with background bar
draw = ImageDraw.Draw(banner)
try:
    font = ImageFont.truetype("C:/Windows/Fonts/Impact.ttf", 48)
except:
    font = ImageFont.load_default()

footer_text = "NOUS BRANDING  *  MULTI-MODEL VISUAL IDENTITY  *  PERCEPTION. REASONING. ACTION.  *  BUILT BY NOUS. FOR THE OPEN FUTURE.  *  NOUSRESEARCH.COM"
bbox = draw.textbbox((0, 0), footer_text, font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]
text_x = (W - text_w) // 2
text_y = content_h + (FOOTER_H - text_h) // 2

# Draw background bar for footer
footer_bar = Image.new("RGB", (W, FOOTER_H), (40, 40, 50))
banner.paste(footer_bar, (0, content_h))

# Redraw on the bar
draw = ImageDraw.Draw(banner)
draw.text((text_x, text_y), footer_text, font=font, fill=(255, 255, 255))

# Save
banner.save(os.path.join(OUT_DIR, "nous-posters-banner-raw.png"), "PNG")
banner.save(os.path.join(OUT_DIR, "nous-posters-banner-raw.jpg"), "JPEG", quality=92)
print(f"\nSaved: {os.path.join(OUT_DIR, 'nous-posters-banner-raw.jpg')}")
