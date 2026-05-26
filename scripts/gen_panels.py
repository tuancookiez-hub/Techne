"""Generate banner panels for Nous Branding — MultiModel. No text, visuals only."""
import json, os, base64, urllib.request, sys

API_KEY = ""
env_path = os.path.expanduser("~/AppData/Local/hermes/.env")
if os.path.isfile(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("BYTEDANCE_API_KEY="):
                API_KEY = line.split("=", 1)[1].strip()
                break

if not API_KEY:
    print("ERROR: No BYTEDANCE_API_KEY found")
    sys.exit(1)

ROOT = "F:\\HermesVision\\AndurilsVision"
OUT_DIR = "banner_panels"
os.makedirs(OUT_DIR, exist_ok=True)

def file_to_data_url(path):
    ext = os.path.splitext(path)[1].lower()
    mime = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}.get(ext, "image/jpeg")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{b64}"

# Core reference images for Nous branding consistency
refs = [
    os.path.join(ROOT, "nous-assets", "references", "anime-nous-manga-xerox-portrait.png"),
    os.path.join(ROOT, "nous-assets", "references", "anime-nous-blueprint-scene.jpg"),
    os.path.join(ROOT, "nous-assets", "references", "style-cyan-xerox-poster.jpg"),
    os.path.join(ROOT, "nous-assets", "references", "style-industrial-duotone-grid.jpg"),
]
refs = [r for r in refs if os.path.isfile(r)]

def gen(name, prompt, size="2K"):
    print(f"\nGenerating {name}...")
    body = {
        "model": "seedream-5-0-260128",
        "prompt": prompt,
        "n": 1,
        "size": size,
        "response_format": "url",
        "watermark": False,
    }
    if refs:
        body["image"] = [file_to_data_url(r) for r in refs]
    
    req = urllib.request.Request(
        "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read())
        img_url = data["data"][0].get("url", "")
        if not img_url:
            print(f"  ERROR: No URL")
            return False
        
        with urllib.request.urlopen(img_url, timeout=60) as dl:
            img_data = dl.read()
        
        ext = "jpg"
        path = os.path.join(OUT_DIR, f"{name}.{ext}")
        with open(path, "wb") as f:
            f.write(img_data)
        print(f"  Saved: {path} ({len(img_data)} bytes)")
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

# ─── Panel prompts (no text, visuals only) ────────────────────

panels = {
    "hero": (
        "Underground research zine aesthetic. Black background with subtle starfield. "
        "Classical Greek marble statue fragment merged with glowing cyan circuit board traces and golden astrolabe geometric halo. "
        "Golden sparks, sacred geometry linework. Dark moody lighting. "
        "Risograph grain, xerox decay texture, halftone dots. "
        "Retro 90s anime manga style mixed with neoclassical sculpture. "
        "NO TEXT. NO WORDS. NO LETTERS. Pure visual only."
    ),
    
    "identity": (
        "Aged cream paper texture background. Underground research zine aesthetic. "
        "Six color swatches in a horizontal row: dark electric blue, light periwinkle, mustard gold, forest teal, off-white, deep black. "
        "Five texture finish samples below: risograph grain dots, photocopy noise, CRT scanlines, paper fiber, ink smudge. "
        "Typography specimen samples showing bold condensed uppercase letterforms. "
        "Golden 8-pointed compass starburst accent. "
        "Risograph print aesthetic, grainy paper, vintage technical manual cover style. "
        "NO TEXT. NO WORDS. NO LETTERS. Pure visual only."
    ),
    
    "top_zine": (
        "Off-white aged paper background. Underground zine aesthetic. "
        "Close-up of a detailed human eye with circuit board patterns in the iris, glowing cyan and gold nodes. "
        "Barcode element at bottom. Grainy paper texture, risograph dots. "
        "Retro 90s anime manga style, black linework. "
        "Cyan and gold accent colors. "
        "NO TEXT. NO WORDS. NO LETTERS. Pure visual only."
    ),
    
    "bot_zine": (
        "Split layout: left half off-white, right half cyan-blue. "
        "Anime girl with short dark bob hair, white headband, beauty mark under left eye, pale skin, large dark anime eyes. "
        "Retro 90s anime manga style, black linework, grainy paper texture. "
        "Neutral pensive expression. "
        "Underground zine aesthetic, risograph print, xerox decay. "
        "NO TEXT. NO WORDS. NO LETTERS. Pure visual only."
    ),
    
    "system_diagram": (
        "Aged cream paper background. Hand-drawn technical sketch style. "
        "Human head in profile with astrolabe geometric grid overlay on the eye area. "
        "Vertical workflow chart with connected boxes and arrows. "
        "Vintage lab notebook aesthetic, black ink linework, technical annotations. "
        "Golden compass rose accent. "
        "NO TEXT. NO WORDS. NO LETTERS. Pure visual only."
    ),
    
    "field_note": (
        "Off-white aged paper with coffee stains and wear. Vintage lab notebook page. "
        "Detailed eye illustration with technical cross-section annotations. "
        "Handwritten-style technical notes and measurements around the edges. "
        "Paper ID stamp element in corner. "
        "Black ink, cyan highlights, grainy texture. "
        "NO TEXT. NO WORDS. NO LETTERS. Pure visual only."
    ),
    
    "symbols": (
        "Dark black background. Underground research zine aesthetic. "
        "Six brand icons in a horizontal row: golden 8-pointed star, human eye with glow, radiating signal paths, geometric compass, winged messenger symbol, sealed wax stamp. "
        "Below: rows of small keyword blocks in categorized groups. "
        "Cyan, gold, and white icons on black. Risograph grain, halftone texture. "
        "NO TEXT. NO WORDS. NO LETTERS. Pure visual only."
    ),
    
    "anime_portal": (
        "Four poster mockups arranged in a 2x2 grid with small gutters. "
        "Same anime girl character in all four: short dark bob hair, white headband, beauty mark under left eye, pale skin, large dark eyes. "
        "Poster 1: Portal scene with geometric gateway, cyan glow. "
        "Poster 2: Silhouette against gradient background. "
        "Poster 3: Acid mascot card with halftone dots. "
        "Poster 4: Op-art geometric pattern with character portrait. "
        "Retro 90s anime manga style, risograph print, grainy paper. "
        "Cyan, gold, black palette. "
        "NO TEXT. NO WORDS. NO LETTERS. Pure visual only."
    ),
    
    "layout_refs": (
        "Four layout demo posters in a 2x2 grid with small gutters. "
        "Poster 1: Neoclassical Greek statue with circuit overlay on dark background. "
        "Poster 2: Technical radar/astrolabe drawing on aged paper. "
        "Poster 3: Satellite dish photograph with cyan tint. "
        "Poster 4: Abstract geometric cover art with halftone dots. "
        "Underground zine aesthetic, risograph grain, vintage print texture. "
        "NO TEXT. NO WORDS. NO LETTERS. Pure visual only."
    ),
}

success = 0
for name, prompt in panels.items():
    if gen(name, prompt):
        success += 1

print(f"\nDone: {success}/{len(panels)} panels generated in {OUT_DIR}/")
