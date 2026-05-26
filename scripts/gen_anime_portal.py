"""Generate 4 individual anime poster images and tile them into a wide panel (1x4 row)."""
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

# Target: 1x4 horizontal row for 21:9 layout
# Make each poster exactly square (504x504) with horizontal padding
poster_size = 504
gutter = 12
panel_w = 4 * poster_size + 3 * gutter  # 2052
panel_h = poster_size  # 504

panel = Image.new("RGB", (panel_w, panel_h), (11, 11, 14))
for i, img in enumerate(posters):
    # Resize to fit within square, preserving aspect ratio
    img.thumbnail((poster_size, poster_size), Image.LANCZOS)
    # Create square canvas and center
    square = Image.new("RGB", (poster_size, poster_size), (11, 11, 14))
    paste_x = (poster_size - img.width) // 2
    paste_y = (poster_size - img.height) // 2
    square.paste(img, (paste_x, paste_y))
    # Place in panel
    x = i * (poster_size + gutter)
    panel.paste(square, (x, 0))

panel.save(os.path.join(OUT_DIR, "anime_portal.jpg"), "JPEG", quality=92)
print(f"Saved anime_portal.jpg ({panel.size}), each poster: {poster_size}x{poster_size} = 1:1")
