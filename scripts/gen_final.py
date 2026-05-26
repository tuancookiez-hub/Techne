import json, os, base64, urllib.request

# Read key from env file directly
KEY = ""
env_path = os.path.expanduser("~/AppData/Local/hermes/.env")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if "BYTEDANCE_API_KEY" in line and "=" in line:
            KEY = line.split("=", 1)[1].strip()
            break


def d(path):
    with open(path, "rb") as f:
        b = base64.b64encode(f.read()).decode()
    e = os.path.splitext(path)[1].lower()
    m = {".jpg": "image/jpeg", ".png": "image/png"}.get(e, "image/jpeg")
    return f"data:{m};base64,{b}"


refs = [
    "nous-assets/references/anime-nous-manga-xerox-portrait.png",
    "nous-assets/references/style-cyan-xerox-poster.jpg",
    "nous-assets/references/Hermes-together-reference.png",
    "nous-assets/references/style-blue-registration-character.jpg",
]

prompt = "Full brand identity mood board grid layout for Techne project. Dark background. 6 panels in 2 rows with thin borders. Top left: anime girl mascot portrait with short dark bob hair headband, TECHNE title bold white, NOUS BRANDING MULTIMODEL blue subtitle. Top middle: IDENTITY LOCKUP with 6 color swatches blue gold teal off-white black, hex codes, texture labels risograph grain photocopy noise CRT lines. Top right: PIPELINE flow diagram eye gear stamp circuit lines. Bottom left: SYMBOLS 6 icons star eye sunburst circle wing square with labels. Bottom middle: ANIME IDENTITY centered girl portrait. Bottom right: backend agnostic text. Full-width footer with tagline. Golden star. Underground zine texture halftone risograph grain paper scuffs ink bleed. Not clean digital art."

body = json.dumps({
    "model": "seedream-5-0-260128",
    "prompt": prompt,
    "image": [d(r) for r in refs],
    "n": 1,
    "size": "2K",
    "response_format": "url",
    "watermark": False,
})

req = urllib.request.Request("https://ark.ap-southeast.bytepluses.com/api/v3/images/generations", data=body.encode(), headers={"Content-Type": "application/json", "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req, timeout=120) as r:
    data = json.loads(r.read())

url = data["data"][0]["url"]
sz = data["data"][0].get("size", "?")
with urllib.request.urlopen(url, timeout=60) as dl:
    with open("techne_banner_v10_raw.jpg", "wb") as f:
        f.write(dl.read())
print(f"Done: techne_banner_v10_raw.jpg ({sz}) tk={data['usage']['total_tokens']}")