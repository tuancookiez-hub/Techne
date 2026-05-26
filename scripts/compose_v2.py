"""Rich README hero banner for Techne — full capability showcase."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 2400, 1500
BG = (10, 10, 14)

# Load pieces
mascot = Image.open("p_mascot_imp.png").resize((780, 780), Image.LANCZOS)
pipeline = Image.open("p_pipeline_imp.png").resize((680, 200), Image.LANCZOS)
badges = Image.open("p_badges_imp.png").resize((680, 240), Image.LANCZOS)
hero_eye = Image.open("p_eye_imprint.png") if os.path.exists("p_eye_imprint.png") else None

canvas = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(canvas)

# Fonts
def get_font(name, size):
    path = f"C:/Windows/Fonts/{name}"
    if os.path.exists(path):
        try: return ImageFont.truetype(path, size)
        except: pass
    return ImageFont.load_default()

big = get_font("impact.ttf", 88)
title = get_font("impact.ttf", 60)
sub = get_font("arialbd.ttf", 34)
body = get_font("arial.ttf", 24)
small = get_font("arial.ttf", 18)
mono = get_font("consola.ttf", 16)
tiny = get_font("consola.ttf", 14)

# Colors
WHT = (230, 230, 230)
BLU = (40, 71, 255)
GLD = (214, 178, 90)
TEL = (46, 112, 107)
CRM = (247, 237, 227)
GRY = (130, 130, 140)

# === LAYOUT ===

# Top bar
draw.text((40, 18), "NOUS RESEARCH PRESENTS", fill=BLU, font=tiny)

# === LEFT SECTION: Mascot portrait ===
canvas.paste(mascot, (50, 55))

# === RIGHT SECTION 1: Capabilities panel ===
cap_x = 920
cap_y = 55
draw.text((cap_x, cap_y), "CAPABILITIES", fill=GLD, font=body)

cap_items = [
    ("👁  Vision Analysis", "Describe, QA, understand images via Kimi"),
    ("🎨  Image Generation", "Text-to-image & image-to-image via Ark Seedream"),
    ("🖨  Imprint Pipeline", "14-step analog print post-processing"),
    ("📦  Batch Pipeline", "Prompt file → bulk gen → post-process"),
    ("🔗  Multi-Model", "Swap backends: Ark, Kimi, OpenRouter, any"),
    ("🔮  Future Ready", "Expand to video, 3D, audio"),
]

y = cap_y + 30
for icon_title, desc in cap_items:
    # Icon + title in gold
    draw.text((cap_x, y), icon_title, fill=GLD, font=small)
    # Description below in gray
    draw.text((cap_x + 5, y + 22), desc, fill=GRY, font=tiny)
    y += 52

# === RIGHT SECTION 2: Models panel ===
mod_x = 920
mod_y = cap_y + 370
draw.text((mod_x, mod_y), "BACKENDS", fill=BLU, font=body)

models = [
    "Ark Seedream 5.0-lite  —  Image Gen",
    "Kimi K2.6           —  Vision Analysis",
    "ByteDance Ark       —  Inference API",
    "OpenRouter          —  Provider bridge",
]

y2 = mod_y + 30
for m in models:
    draw.text((mod_x, y2), m, fill=CRM, font=tiny)
    y2 += 24

# === RIGHT SECTION 3: Badges visual ===
canvas.paste(badges, (cap_x, mod_y + 130))

# === TITLE SECTION (below portrait) ===
draw.text((50, 860), "TECHNE", fill=WHT, font=big)
draw.text((50, 960), "NOUS BRANDING  —  MULTIMODEL", fill=BLU, font=sub)
draw.text((50, 1005), "Codex-only Nous Research visual identity projects, adapted for any model.", fill=CRM, font=body)

# === PIPELINE VISUAL ===
pip_x = 50
pip_y = 1080
draw.text((pip_x, pip_y), "PIPELINE", fill=GLD, font=body)
canvas.paste(pipeline, (pip_x, pip_y + 30))

# Pipeline text labels
pip_labels = ["PROMPT", "SEEDREAM 5.0", "IMPRINT POST", "OUTPUT"]
pip_lx = [pip_x + 20, pip_x + 190, pip_x + 380, pip_x + 540]
for i, (lbl, lx) in enumerate(zip(pip_labels, pip_lx)):
    draw.text((lx, pip_y + 5), lbl, fill=GRY, font=tiny)

# === CAPABILITY TAGS (horizontal bar) ===
tags = ["VISION ANALYSIS", "IMAGE GENERATION", "IMPRINT POST-PROCESS", "BATCH PIPELINE", "MULTI-MODEL"]
tag_x = 50
tag_y = 1340
draw.text((tag_x, tag_y), "·".join(tags), fill=TEL, font=small)

# === FOOTER ===
draw.text((50, 1390), "SEE.  INTERPRET.  UNDERSTAND.  ACT.", fill=WHT, font=body)
draw.text((50, 1430), "FORKED FROM NOUS  ·  BUILT FOR ANY MODEL  ·  OPEN FUTURE", fill=TEL, font=small)
draw.text((1700, 1430), "RELEASE  05.2026", fill=GRY, font=mono)

# === DECORATIVE DIVIDERS ===
# Vertical line separating left/right
draw.line([(870, 55), (870, 850)], fill=GLD, width=1)
# Horizontal line above footer
draw.line([(50, 1370), (2350, 1370)], fill=TEL, width=1)

# Corner star
draw.text((2330, 18), "\u2605", fill=GLD, font=sub)

canvas.save("techne_banner_v7.png")
print(f"Saved: techne_banner_v7.png ({W}x{H})")
