import json, os, base64, urllib.request

KEY = ""
env = os.path.expanduser("~/AppData/Local/hermes/.env")
with open(env) as f:
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
    print(f"{out} ({data['data'][0].get('size','?')}) tokens={data['usage']['total_tokens']}")


gen(
    ["nous-assets/references/anime-nous-blueprint-scene.jpg", "nous-assets/references/style-blue-registration-character.jpg", "nous-assets/references/anime-nous-acid-mascot-card.png"],
    "Striking anime girl mascot portrait, electric blue and deep navy, dark short hair, beauty mark under eye, facing forward, glowing cyan eyes, dramatic lighting, geometric halo behind head, deep black background, underground cyber-zine print",
    "p_portrait.jpg",
)

gen(
    ["nous-assets/references/Hermes-mind-reference.png"],
    "Close-up stylized human eye, highly detailed, electric blue iris with golden sunburst pattern, geometric rings, circuit traces, dark background, risograph grain",
    "p_eye.jpg",
)

gen(
    ["nous-assets/references/style-cyan-xerox-poster.jpg"],
    "Golden geometric astrolabe rings on dark background, 8-pointed golden star at center, 3 orbiting glowing orbs in electric blue acid green and signal orange, radar grid lines, underground lab aesthetic",
    "p_symbols.jpg",
)