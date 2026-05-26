"""Generate 4 individual anime poster images and tile them into a wide panel."""
import os
from PIL import Image
import urllib.request, json, base64

API_KEY = ""
env_path = os.path.expanduser("~/AppData/Local/hermes/.env")
if os.path.isfile(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("BYTEDANCE_API_KEY="):
                API_KEY = line.split("=", 1)[1].strip()
                break

ROOT = "F:\\HermesVision\\AndurilsVision"
OUT_DIR = os.path.join(ROOT, "banner_panels")

refs = [
    os.path.join(ROOT, "nous-assets", "references", "anime-nous-manga-xerox-portrait.png"),
    os.path.join(ROOT, "nous-assets", "references", "anime-nous-opart-poster.png"),
]
refs = [r for r in refs if os.path.isfile(r)]

def file_to_data_url(path):
    ext = os.path.splitext(path)[1].lower()
    mime = {".jpg": "image/jpeg", ".png": "image/png"}.get(ext, "image/jpeg")
    with open(path, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"

def gen(prompt):
    body = {
        "model": "seedream-5-0-260128",
        "prompt": prompt,
        "n": 1,
        "size": "2K",
        "response_format": "url",
        "watermark": False,
        "image": [file_to_data_url(r) for r in refs]
    }
    req = urllib.request.Request(
        "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read())
    img_url = data["data"][0]["url"]
    with urllib.request.urlopen(img_url, timeout=60) as dl:
        return Image.open(dl).convert("RGB")

# Generate 4 posters
posters = [
    gen("Anime girl with short dark bob hair, white headband, beauty mark under left eye. Standing in a glowing geometric portal gateway, cyan light, sacred geometry. Retro 90s anime manga style, risograph grain. NO TEXT."),
    gen("Black silhouette of anime girl with short dark bob hair, white headband. Against a gradient background from gold to cyan. Retro 90s anime style. NO TEXT."),
    gen("Anime girl with short dark bob hair, white headband, beauty mark. Halftone dot print style, newsprint texture, black and white with cyan accents. Retro manga aesthetic. NO TEXT."),
    gen("Anime girl with short dark bob hair, white headband. Op-art geometric background, cyan and gold maze pattern. Retro 90s anime manga style. NO TEXT."),
]

# Target panel size
panel_w, panel_h = 1194, 488
gutter = 8
poster_w = (panel_w - gutter) // 2
poster_h = (panel_h - gutter) // 2

# Resize and tile
panel = Image.new("RGB", (panel_w, panel_h), (11, 11, 14))
for i, img in enumerate(posters):
    img = img.resize((poster_w, poster_h), Image.LANCZOS)
    x = (i % 2) * (poster_w + gutter)
    y = (i // 2) * (poster_h + gutter)
    panel.paste(img, (x, y))

panel.save(os.path.join(OUT_DIR, "anime_portal.jpg"), "JPEG", quality=92)
print(f"Saved anime_portal.jpg ({panel.size})")
