"""Dense mood board banner — like the upstream THEIA layout."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

W, H = 2400, 1600
BG = (11, 11, 15)

# Load pieces
mascot = Image.open("p_mascot_imp.png").resize((500, 500), Image.LANCZOS)
pipeline = Image.open("p_pipeline_imp.png").resize((500, 170), Image.LANCZOS)
eye_piece = None
if os.path.exists("p_eye_imprint.png"):
    eye_piece = Image.open("p_eye_imprint.png").resize((500, 400), Image.LANCZOS)

canvas = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(canvas)

def font(name, sz):
    p = f"C:/Windows/Fonts/{name}"
    if os.path.exists(p):
        try: return ImageFont.truetype(p, sz)
        except: pass
    return ImageFont.load_default()

h1 = font("impact.ttf", 80)
h2 = font("impact.ttf", 44)
h3 = font("arialbd.ttf", 26)
b1 = font("arial.ttf", 20)
b2 = font("arial.ttf", 16)
sm = font("consola.ttf", 14)
xs = font("consola.ttf", 12)

WHT = (235, 235, 235)
BLU = (40, 71, 255)
GLD = (214, 178, 90)
TEL = (46, 112, 107)
CRM = (247, 237, 227)
GRY = (140, 140, 150)
DIM = (30, 30, 40)

# Draw panel backgrounds (subtle rectangles)
def panel(x, y, w, h, color=DIM):
    draw.rectangle([x, y, x+w, y+h], fill=color, outline=GRY, width=1)

# === TOP ROW ===

# Panel 1: Hero (left)
px, py = 30, 20
panel(px, py, 700, 560)
draw.text((px+15, py+10), "NOUS RESEARCH PRESENTS", fill=BLU, font=xs)
draw.text((px+15, py+30), "TECHNE", fill=WHT, font=h1)
draw.text((px+15, py+120), "NOUS BRANDING  —  MULTIMODEL", fill=BLU, font=h2)
draw.text((px+15, py+175), "Codex-only projects, adapted for any model.", fill=CRM, font=b1)

# Mascot inside hero panel
mascot_x = px + 180
mascot_y = py + 10
canvas.paste(mascot, (mascot_x, mascot_y), mascot if mascot.mode == "RGBA" else None)

# Capabilities text in hero
draw.text((px+15, py+220), "CAPABILITIES", fill=GLD, font=b2)
caps = ["VISION ANALYSIS", "IMAGE GENERATION", "IMPRINT", "BATCH", "MULTI-MODEL"]
y_offset = py + 250
for c in caps:
    draw.text((px+25, y_offset), f"  ·  {c}", fill=CRM, font=sm)
    y_offset += 24

# Panel 2: Identity Lockup (middle)
px2, py2 = 760, 20
panel(px2, py2, 700, 560)
draw.text((px2+15, py2+10), "IDENTITY LOCKUP", fill=BLU, font=sm)

# Color palette swatches
swatch_colors = [(40, 71, 255), (128, 166, 255), (214, 178, 90), (46, 112, 107), (230, 230, 230), (11, 11, 15)]
swatch_w = 60
swatch_h = 40
swatch_gap = 5
total_swatch_w = len(swatch_colors) * (swatch_w + swatch_gap) - swatch_gap
sw_start_x = px2 + 15
for i, c in enumerate(swatch_colors):
    sx = sw_start_x + i * (swatch_w + swatch_gap)
    draw.rectangle([sx, py2+35, sx+swatch_w, py2+35+swatch_h], fill=c, outline=GRY, width=1)

# Palette labels
hex_labels = ["#2847FF", "#80A6FF", "#D6B25A", "#2E706B", "#E6E6E6", "#0B0B0E"]
for i, (lbl, c) in enumerate(zip(hex_labels, swatch_colors)):
    sx = sw_start_x + i * (swatch_w + swatch_gap)
    draw.text((sx, py2+35+swatch_h+3), lbl, fill=GRY if sum(c) > 300 else WHT, font=xs)

# Texture labels
draw.text((px2+15, py2+95), "TEXTURE + FINISH", fill=GLD, font=b2)
textures = ["RISOGRAPH GRAIN", "PHOTOCOPY NOISE", "CRT SCAN LINES", "PAPER FIBER", "INK SMUDGE"]
tx = px2 + 15
for t in textures:
    draw.text((tx, py2+120), t, fill=WHT, font=xs)
    tx += 130

# Typography section
draw.text((px2+15, py2+155), "TYPOGRAPHY", fill=GLD, font=b2)
draw.text((px2+15, py2+180), "HEADLINES: DRUK CONDENSED", fill=WHT, font=b2)
draw.text((px2+15, py2+205), "SUPPORTING: INTER / IBM PLEX SANS", fill=CRM, font=sm)
draw.text((px2+15, py2+225), "MONOSPACE: JETBRAINS MONO", fill=CRM, font=sm)

# Sample terminal text
term_lines = [
    "> initializing vision pipeline...",
    "> decoding visual tokens...",
    "> grounding in context...",
    "> invoking action...",
]
ty = py2 + 255
for tl in term_lines:
    draw.text((px2+15, ty), tl, fill=TEL, font=xs)
    ty += 18

# Panel 3: Research Zine (right)
px3, py3 = 1490, 20
panel(px3, py3, 700, 560)
draw.text((px3+15, py3+10), "PIPELINE", fill=BLU, font=sm)
draw.text((px3+15, py3+35), "SYSTEM FLOW", fill=GLD, font=b2)

# Pipeline text
pipeline_steps = [
    "PROMPT  →",
    "GENERATION  →",
    "IMPRINT POST-PROCESS  →",
    "OUTPUT",
]
pipy = py3 + 65
for s in pipeline_steps:
    draw.text((px3+25, pipy), s, fill=WHT, font=b2)
    pipy += 30

# Pipeline visual
canvas.paste(pipeline, (px3+15, py3+180))

# Zine field notes
draw.text((px3+15, py3+370), "FIELD NOTES", fill=GLD, font=b2)
draw.text((px3+15, py3+400), "To see clearly is to model the world.", fill=CRM, font=sm)
draw.text((px3+15, py3+420), "To model truly, is to act properly.", fill=CRM, font=sm)
draw.text((px3+15, py3+440), "Codex sees. Techne crafts. Nous understands.", fill=TEL, font=xs)

# Panel name labels at bottom
draw.text((px3+15, py3+470), "INTERNAL PAPER // NR-TN-05", fill=GRY, font=xs)
draw.text((px3+15, py3+490), f"RELEASE  05.2026", fill=GRY, font=xs)

# Eye piece in pipeline panel if available
if eye_piece:
    canvas.paste(eye_piece, (px3+460, py3+200), eye_piece if eye_piece.mode == "RGBA" else None)

# === BOTTOM ROW ===

# Panel 4: Symbols (left)
px4, py4 = 30, 610
panel(px4, py4, 700, 550)
draw.text((px4+15, py4+10), "SYMBOLS & MOTIFS", fill=BLU, font=sm)

symbols_data = [
    ("\u2605", "THEIA STAR", "SIGHT / LIGHT"),
    ("\u25C9", "EYE OF PERCEPTION", "OBSERVATION"),
    ("\u2737", "RADIANT PATHS", "SIGNAL / TRAVEL"),
    ("\u25CB", "OPTIC GEOMETRY", "FOCUS / CLARITY"),
    ("\u2661", "MESSENGER'S WING", "HERMES"),
    ("\u25A0", "CODEX SEAL", "KNOWLEDGE"),
]
sy = py4 + 45
for sym, name, desc in symbols_data:
    draw.text((px4+15, sy), f"{sym}  {name}", fill=GLD, font=b2)
    draw.text((px4+130, sy), f"({desc})", fill=GRY, font=xs)
    sy += 35

# Keywords section
draw.text((px4+15, sy+10), "KEYWORDS", fill=BLU, font=b2)
kw_groups = [
    "PERCEPTION  ·  ILLUMINATION  ·  INTERPRETATION",
    "AGENCY  ·  TRANSMISSION  ·  STEERABILITY",
    "TOOL USE  ·  REASONING  ·  GROUNDING",
    "VISION  ·  CONTEXT  ·  CODEX",
]
kwy = sy + 40
for kg in kw_groups:
    draw.text((px4+15, kwy), kg, fill=TEL, font=xs)
    kwy += 18

# Panel 5: Anime Identity (middle)
px5, py5 = 760, 610
panel(px5, py5, 700, 550)
draw.text((px5+15, py5+10), "ANIME IDENTITY", fill=BLU, font=sm)

# Place mascot as centerpiece
canvas.paste(mascot.resize((350, 350), Image.LANCZOS), (px5+170, py5+40))

# Labels around mascot
draw.text((px5+15, py5+50), "PORTAL", fill=GLD, font=b2)
draw.text((px5+15, py5+75), "\u30DD\u30FC\u30BF\u30EB", fill=GRY, font=sm)

draw.text((px5+530, py5+50), "TECHNE", fill=GLD, font=b2)
draw.text((px5+530, py5+75), "\u8996\u899A\u30B9\u30AD\u30EB", fill=GRY, font=sm)

# Bottom labels
draw.text((px5+15, py5+420), "MASCOT IDENTITY", fill=GLD, font=sm)
draw.text((px5+15, py5+445), "ORIGINAL ANONYMOUS STYLIZED ANIME FIGURE", fill=CRM, font=xs)

# Panel 6: Model / Backend (right)
px6, py6 = 1490, 610
panel(px6, py6, 700, 550)
draw.text((px6+15, py6+10), "BACKEND AGNOSTIC", fill=BLU, font=sm)
draw.text((px6+15, py6+35), "MULTI-MODEL ARCHITECTURE", fill=GLD, font=b2)

# Description
models_info = [
    "\"This project is not locked to any single provider.\"",
    "",
    "DESIGNED TO WORK WITH ANY",
    "OPENAI-COMPATIBLE INFERENCE ENDPOINT.",
    "",
    "IMAGE GENERATION  ·  VISION ANALYSIS",
    "POST-PROCESSING  ·  BATCH PIPELINES",
    "ALL THROUGH A UNIFIED INTERFACE.",
    "",
    "NO CODE LOCK-IN. NO VENDOR TRAP.",
    "BRING YOUR OWN MODEL.",
]

my = py6 + 70
for line in models_info:
    if line:
        draw.text((px6+25, my), line, fill=WHT if line.isupper() else GLD, font=b2 if line.isupper() else sm)
    my += 28

# === FULL-WIDTH FOOTER ===
fy = 1190
draw.line([(30, fy), (2370, fy)], fill=TEL, width=1)
draw.text((30, fy+10), "TECHNE IS HOW HERMES CRAFTS", fill=WHT, font=b1)
draw.text((30, fy+38), "VISION IS THE FIRST MESSAGE", fill=BLU, font=b1)
draw.text((30, fy+66), "PERCEPTION  ·  REASONING  ·  ACTION", fill=GLD, font=sm)
draw.text((1500, fy+10), "BUILT BY NOUS", fill=CRM, font=sm)
draw.text((1500, fy+38), "FOR THE OPEN FUTURE", fill=CRM, font=sm)
draw.text((1500, fy+66), "FORKED FROM NOUS  ·  ANY MODEL  ·  OPEN", fill=TEL, font=xs)

# === DECORATIVE ===
# Golden star top right
draw.text((2350, 15), "\u2605", fill=GLD, font=h2)

# Thin border around entire canvas
draw.rectangle([(5, 5), (W-5, H-5)], outline=GRY, width=1)

canvas.save("techne_banner_v9.png")
print(f"Saved: techne_banner_v9.png ({W}x{H})")