import json, os, base64, urllib.request, sys

KEY = ""
env_path = os.path.expanduser("~/AppData/Local/hermes/.env")
if os.path.isfile(env_path):
    with open(env_path) as f:
        for line in f:
            if line.startswith("BYTEDANCE_API_KEY="):
                KEY = line.split("=", 1)[1].strip()
                break
DIR = "."


def d(path):
    with open(os.path.join(DIR, path), "rb") as f:
        b = base64.b64encode(f.read()).decode()
    e = os.path.splitext(path)[1].lower()
    m = {".jpg": "image/jpeg", ".png": "image/png"}.get(e, "image/jpeg")
    return f"data:{m};base64,{b}"


def gen(refs, prompt, out):
    body = {"model": "seedream-5-0-260128", "prompt": prompt, "n": 1, "size": "2K", "response_format": "url", "watermark": False}
    if refs:
        body["image"] = [d(r) for r in refs]
    req = urllib.request.Request("https://ark.ap-southeast.bytepluses.com/api/v3/images/generations", data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read())
    url = data["data"][0]["url"]
    with urllib.request.urlopen(url, timeout=60) as dl:
        with open(out, "wb") as f:
            f.write(dl.read())
    print(f"{out} ({data['data'][0].get('size','?')})")

gen(
    ["nous-assets/references/anime-nous-manga-xerox-portrait.png", "nous-assets/references/anime-nous-blueprint-scene.jpg", "nous-assets/references/anime-nous-opart-poster.png"],
    "Retro 90s anime portrait of young woman, short dark bob hair with flipped ends, blunt bangs, pale skin, large anime eyes with solid black irises and white catchlights, thin light gray headband, three-quarter view facing left, pensive expression, muted teal-gray background, clean sharp linework, limited palette of dusty teal gray pale gray and deep black, printed sticker style, grainy paper texture",
    "p_mascot.jpg",
)

gen(
    ["nous-assets/references/Hermes-mind-reference.png", "nous-assets/references/style-cyan-xerox-poster.jpg"],
    "Technical schematic diagram showing three icons connected by circuit lines: an eye node connected to a gear node connected to a stamp icon, golden circuit traces on dark navy background, blueprint grid lines, xerox texture, underground lab aesthetic",
    "p_pipeline.jpg",
)

gen(
    ["nous-assets/references/style-industrial-duotone-grid.jpg", "nous-assets/references/style-cyan-xerox-poster.jpg"],
    "Three stylized geometric shield emblems arranged horizontally, each a different color: electric blue, acid green, signal orange, connected by glowing circuit traces on dark background, underground tech zine aesthetic, halftone dots, risograph grain",
    "p_badges.jpg",
)
