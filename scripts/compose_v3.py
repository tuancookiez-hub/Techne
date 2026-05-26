"""Refined README hero banner — better hierarchy, bigger text."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 2400, 1350
BG = (10, 10, 14)

mascot = Image.open("p_mascot_imp.png").resize((520, 520), Image.LANCZOS)
badges = Image.open("p_badges_imp.png").resize((520, 180), Image.LANCZOS)
pipeline = Image.open("p_pipeline_imp.png").resize((600, 180), Image.LANCZOS)

canvas = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(canvas)

def get_font(name, size):
    p = f"C:/Windows/Fonts/{name}"
    if os.path.exists(p):
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

h1 = get_font("impact.ttf", 100)
h2 = get_font("impact.ttf", 52)
h3 = get_font("arialbd.ttf", 30)
b1 = get_font("arial.ttf", 22)
b2 = get_font("arial.ttf", 18)
sm = get_font("consola.ttf", 15)
xs = get_font("consola.ttf", 13)

WHT = (230, 230, 230)
BLU = (40, 71, 255)
GLD = (214, 178, 90)
TEL = (46, 112, 107)
CRM = (247, 237, 227)
GRY = (140, 140, 150)

# Top bar
draw.text((40, 18), "NOUS RESEARCH PRESENTS", fill=BLU, font=xs)

# === LEFT: Portrait (smaller, more compact) ===
canvas.paste(mascot, (40, 40))

# === MIDDLE-LEFT: Title block (aligned with portrait top) ===
tx = 610
draw.text((tx, 40), "TECHNE", fill=WHT, font=h1)
draw.text((tx, 150), "NOUS BRANDING  —  MULTIMODEL", fill=BLU, font=h3)
draw.text((tx, 195), "Codex-only projects, adapted for any model.", fill=CRM, font=b1)
draw.text((tx, 225), "Built for Hermes Agent — vision + generation + analog imprint.", fill=GRY, font=b2)

# Pipeline (aligned under title)
draw.text((tx, 280), "PIPELINE", fill=GLD, font=b2)
canvas.paste(pipeline, (tx, 305))

# Pipeline labels
steps = [("PROMPT", 0), ("SEEDREAM 5.0", 170), ("IMPRINT POST", 350), ("OUTPUT", 500)]
for label, offset in steps:
    draw.text((tx + offset, 285), label, fill=GRY, font=xs)

# === RIGHT: Capabilities column ===
rx = 1280
draw.text((rx, 40), "CAPABILITIES", fill=GLD, font=b1)

caps = [
    ("Vision Analysis", "Describe, QA, understand images"),
    ("Image Generation", "Text & image-to-image via Seedream"),
    ("Imprint Pipeline", "14-step analog print effects"),
    ("Batch Pipeline", "Prompt file → bulk gen → process"),
    ("Multi-Model", "Swap Ark, Kimi, OpenRouter, any"),
    ("Future Ready", "Video, 3D, audio on roadmap"),
]

y = 70
for title, desc in caps:
    draw.text((rx, y), title, fill=GLD, font=b2)
    draw.text((rx + 5, y + 22), desc, fill=GRY, font=xs)
    y += 48

# Backends section
draw.text((rx, y + 10), "BACKENDS", fill=BLU, font=b1)
y += 40
backends = [
    "Ark Seedream 5.0-lite   — Image Gen",
    "Kimi K2.6               — Vision Analysis",
    "ByteDance Ark           — Inference API",
    "OpenRouter              — Provider Bridge",
]
for b in backends:
    draw.text((rx, y), b, fill=CRM, font=xs)
    y += 22

# Badges visual
canvas.paste(badges, (rx + 20, y + 15))

# === FULL-WIDTH FOOTER ===
draw.line([(40, 1200), (2360, 1200)], fill=TEL, width=1)

tags = ["VISION ANALYSIS", "IMAGE GENERATION", "IMPRINT POST-PROCESS", "BATCH PIPELINE", "MULTI-MODEL"]
draw.text((40, 1220), "  ·  ".join(tags), fill=TEL, font=b2)
draw.text((40, 1260), "SEE.  INTERPRET.  UNDERSTAND.  ACT.", fill=WHT, font=b1)
draw.text((40, 1295), "FORKED FROM NOUS  ·  BUILT FOR ANY MODEL  ·  OPEN FUTURE", fill=TEL, font=sm)
draw.text((1850, 1295), "RELEASE  05.2026", fill=GRY, font=xs)

# Divider between mid and right
draw.line([(1240, 40), (1240, 1150)], fill=GLD, width=1)

# Corner star
draw.text((2330, 18), "\u2605", fill=GLD, font=h3)

canvas.save("techne_banner_v8.png")
print(f"Saved: techne_banner_v8.png ({W}x{H})")
