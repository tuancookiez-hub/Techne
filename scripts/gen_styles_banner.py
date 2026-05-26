"""Generate 9 panels, each in a different v11 Nous style lane."""
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
OUT_DIR = "style_panels"
os.makedirs(OUT_DIR, exist_ok=True)

def file_to_data_url(path):
    ext = os.path.splitext(path)[1].lower()
    mime = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}.get(ext, "image/jpeg")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{b64}"

def get_refs_for_lane(lane_name):
    ref_dir = os.path.join(ROOT, "nous-assets", "references")
    lane_refs = {
        "retro_media": ["Hermes-player-reference.png", "style-cyan-xerox-poster.jpg", "style-rough-print.jpg"],
        "analog_newspaper": ["Hermes4.3-reference .png", "style-rough-print.jpg", "style-cyan-xerox-poster.jpg"],
        "hermetic_print": ["Hermes-jam-reference.png", "Hermes-classical-reference .png", "style-rough-print.jpg"],
        "cyanotype_city": ["Computersaysno-reference .png", "style-blue-registration-character.jpg", "style-cyan-xerox-poster.jpg"],
        "network_diagram": ["Hermes-together-reference.png", "Nous-Discord-reference .png", "Hermes-mind-reference.png", "style-cyan-xerox-poster.jpg"],
        "veiled_classical": ["image 3.PNG", "Hermes-classical-reference .png", "style-blue-registration-character.jpg", "style-rough-print.jpg"],
        "planetary_broadcast": ["image0 2.JPG", "Hermes-together-reference.png", "Nous-Discord-reference .png", "style-cyan-xerox-poster.jpg"],
        "manufactured_multiples": ["image0 3.JPG", "style-industrial-duotone-grid.jpg", "style-cyan-xerox-poster.jpg", "style-rough-grain.jpg"],
        "motorsport": ["Nous-car-reference.png", "style-industrial-duotone-grid.jpg", "style-rough-grain.jpg"],
    }
    refs = lane_refs.get(lane_name, [])
    return [os.path.join(ref_dir, r) for r in refs if os.path.isfile(os.path.join(ref_dir, r))]

def gen(name, prompt, refs, size="2K"):
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
            print("  ERROR: No URL")
            return False
        with urllib.request.urlopen(img_url, timeout=60) as dl:
            img_data = dl.read()
        path = os.path.join(OUT_DIR, f"{name}.jpg")
        with open(path, "wb") as f:
            f.write(img_data)
        print(f"  Saved: {path} ({len(img_data)} bytes)")
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

# ─── 9 v11 style lanes ─────────────────────────────────────────

lanes = {
    "01_retro_media": (
        "Retro media interface relic aesthetic. CRT monitor bezel frame, analog VU meters, broadcast utility console with glowing cyan and gold indicators. Risograph grain, halftone dots, xerox decay texture. Underground zine aesthetic, 90s tech nostalgia. NO TEXT. NO WORDS. Pure visual only.",
        "retro_media"
    ),
    "02_analog_newspaper": (
        "Analog newspaper direct response aesthetic. Classified ad layout, coupon cutout borders, bold headline typography blocks, order form fields. Aged newsprint yellow paper, ink smudge texture, risograph grain. Underground zine meets vintage direct mail. NO TEXT. NO WORDS. Pure visual only.",
        "analog_newspaper"
    ),
    "03_hermetic_print": (
        "Ornate hermetic print artifact aesthetic. Archival broadside layout, model seal emblem, occult institutional certificate border with decorative corners. Aged parchment, gold foil accents, blackletter-inspired framing. Sacred geometry motifs, compass and square symbols. NO TEXT. NO WORDS. Pure visual only.",
        "hermetic_print"
    ),
    "04_cyanotype_city": (
        "Cyanotype surveillance city aesthetic. Blue-toned urban evidence photograph, analog surveillance still, anomaly archive documentation. Prussian blue monochrome, high contrast, grainy film texture. Street scene with geometric overlays, measurement marks. NO TEXT. NO WORDS. Pure visual only.",
        "cyanotype_city"
    ),
    "05_network_diagram": (
        "Network diagram primitive aesthetic. Primitive community network map, civic infrastructure diagram, agent connection flowchart with nodes and edges. Hand-drawn technical sketch style, black ink on cream paper. Minimal geometric shapes, connection lines, hub nodes. NO TEXT. NO WORDS. Pure visual only.",
        "network_diagram"
    ),
    "06_veiled_classical": (
        "Veiled classical artifact aesthetic. Close-cropped marble statue fragment, veiled figure detail, museum archive scan. Soft focus, dramatic chiaroscuro lighting, stone texture. Occult archive record aesthetic, aged paper overlay. NO TEXT. NO WORDS. Pure visual only.",
        "veiled_classical"
    ),
    "07_planetary_broadcast": (
        "Planetary broadcast identity aesthetic. Satellite-era communication card, planetary broadcast poster, space agency visual identity. Earth from space, satellite dish arrays, signal wave patterns. Cyan and gold on dark background, retro-futuristic 70s NASA style. NO TEXT. NO WORDS. Pure visual only.",
        "planetary_broadcast"
    ),
    "08_manufactured_multiples": (
        "Manufactured multiples aesthetic. Repeated product array, packaging grid, ritual-industrial objects in ordered rows. Duotone cyan and black, industrial grid overlay, barcode elements. Mass production aesthetic, identical units with slight variation. NO TEXT. NO WORDS. Pure visual only.",
        "manufactured_multiples"
    ),
    "09_motorsport": (
        "Motorsport sponsor field research aesthetic. Racing livery design, rally team identity, field research vehicle graphics. Bold diagonal stripes, sponsor logo blocks, tire tread patterns. Industrial duotone, gritty texture, speed lines. NO TEXT. NO WORDS. Pure visual only.",
        "motorsport"
    ),
}

success = 0
for name, (prompt, lane_key) in lanes.items():
    refs = get_refs_for_lane(lane_key)
    if gen(name, prompt, refs):
        success += 1

print(f"\nDone: {success}/{len(lanes)} style panels generated in {OUT_DIR}/")
