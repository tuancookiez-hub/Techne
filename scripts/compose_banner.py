"""Compose generated pieces into a README hero banner mood board."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 2400, 1400
BG = (10, 10, 14)  # #0A0A0E

# Load pieces
portrait = Image.open("p_portrait_imprint.png").resize((900, 900), Image.LANCZOS)
eye = Image.open("p_eye_imprint.png").resize((460, 460), Image.LANCZOS)
symbols = Image.open("p_symbols_imprint.png").resize((460, 340), Image.LANCZOS)

# Create canvas
canvas = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(canvas)

# Try to load a bold font for headings
fonts = [
    "C:/Windows/Fonts/impact.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/consola.ttf",
]

title_font = None
sub_font = None
mono_font = None
cap_font = None

for p in fonts:
    if os.path.exists(p):
        try:
            title_font = ImageFont.truetype(p, 80)
            sub_font = ImageFont.truetype(p, 36)
            cap_font = ImageFont.truetype(p, 22)
        except:
            pass
        break

# Find monospace font
for p in ["C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/cour.ttf", "C:/Windows/Fonts/lucon.ttf"]:
    if os.path.exists(p):
        try:
            mono_font = ImageFont.truetype(p, 18)
        except:
            pass
        break

if not title_font:
    title_font = ImageFont.load_default()
    sub_font = title_font
    mono_font = title_font
    cap_font = title_font

# Colors
OFF_WHITE = (230, 230, 230)
BLUE = (40, 71, 255)
GOLD = (214, 178, 90)
TEAL = (46, 112, 107)
CREAM = (247, 237, 227)
DARK_BG = (10, 10, 14)

# === LAYOUT ===
# Left panel: portrait (900x900) 
canvas.paste(portrait, (60, 60))

# Top-right: eye piece
canvas.paste(eye, (1100, 60))

# Below eye: symbols piece
canvas.paste(symbols, (1100, 560))

# === TEXT ===

# "NOUS RESEARCH PRESENTS" at top left
draw.text((60, 20), "NOUS RESEARCH PRESENTS", fill=BLUE, font=cap_font)

# "TECHNE" big title
draw.text((60, 980), "TECHNE", fill=OFF_WHITE, font=title_font)

# Subtitle
draw.text((60, 1070), "NOUS BRANDING  —  MULTIMODEL", fill=BLUE, font=sub_font)

# Tagline
draw.text((60, 1120), "Codex-only projects, adapted for any model.", fill=CREAM, font=cap_font)

# Capability list (left)
caps = ["IMAGE GEN", "VISION", "IMPRINT", "VIDEO", "3D"]
cap_text = "  ·  ".join(caps)
# We'll add this below or as a footer

# Right panel text - "TECHNE" vertical
draw.text((1150, 540), "CRAFT  ·  SKILL  ·  TECHNOLOGY", fill=GOLD, font=cap_font)

# Bottom right - release info
draw.text((1800, 1300), "FORKED FROM NOUS  ·  BUILT FOR ANY MODEL  ·  OPEN FUTURE", fill=TEAL, font=cap_font)

# Footer tagline across bottom
draw.text((60, 1340), "SEE. INTERPRET. UNDERSTAND. ACT.", fill=OFF_WHITE, font=cap_font)

# Draw border lines (thin gold line between sections)
for x in [1040]:  # vertical divider
    draw.line([(x, 60), (x, 960)], fill=GOLD, width=1)

# Small decorative elements - star in corner
draw.text((2310, 20), "\u2605", fill=GOLD, font=sub_font)

# Add a small label for the project
draw.text((1100, 960), "HERMES ECOSYSTEM CAPABILITY", fill=TEAL, font=cap_font)

# Capabilities section - horizontal list at bottom left
draw.text((60, 1180), cap_text, fill=GOLD, font=cap_font)

# Save
canvas.save("techne_banner_final.png")
print(f"Saved: techne_banner_final.png ({W}x{H})")
