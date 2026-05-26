import json, os, base64, urllib.request

KEY = ""
with open(os.path.expanduser("~/AppData/Local/hermes/.env")) as f:
    for line in f:
        if line.startswith("BYTEDANCE_API_KEY="):
            KEY = line.split("=", 1)[1].strip()
            break


def d(path):
    with open(path, "rb") as f:
        b = base64.b64encode(f.read()).decode()
    e = os.path.splitext(path)[1].lower()
    m = {".jpg": "image/jpeg", ".png": "image/png"}.get(e, "image/jpeg")
    return f"data:{m};base64,{b}"


# Single generation — mood board style like upstream
refs = [
    "nous-assets/references/anime-nous-manga-xerox-portrait.png",
    "nous-assets/references/style-cyan-xerox-poster.jpg",
    "nous-assets/references/style-blue-registration-character.jpg",
    "nous-assets/references/Hermes-together-reference.png",
]

prompt = """Full brand identity mood board for Techne, a Hermes Agent vision skill. Underground research zine aesthetic, dark background. Top left: large distressed bold white all-caps text TECHNE, smaller electric blue subhead NOUS BRANDING MULTIMODEL, tagline "codex-only projects adapted for any model." Center-left: large portrait of an anime girl mascot with short dark bob hair, blunt bangs, pale skin, large black eyes, light gray headband, three-quarter view, printed sticker style on muted teal background. Top right: 6 color swatches as a palette strip in royal blue light periwinkle mustard gold teal off-white and black. Below palette: capability list in gold text: VISION ANALYSIS IMAGE GENERATION IMPRINT POST-PROCESS BATCH MULTI-MODEL. Center-right: pipeline flow diagram showing eye icon connected to gear icon connected to stamp icon connected to output icon with circuit line arrows. Bottom: full-width tagline "SEE INTERPRET UNDERSTAND ACT" in off-white text. Thin gold vertical divider between left and right panels. Golden star symbol in top right corner. Underground cyber-zine print texture, halftone dots, risograph grain, paper fiber, ink scuffs. Not clean digital art."""

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
    with open("techne_banner_single_raw.jpg", "wb") as f:
        f.write(dl.read())
print(f"Done: techne_banner_single_raw.jpg ({sz}) tk={data['usage']['total_tokens']}")