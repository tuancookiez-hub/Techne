import json, os, base64, urllib.request

KEY = ""
with open(os.path.expanduser("~/AppData/Local/hermes/.env")) as f:
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
    "nous-assets/references/Hermes-together-reference.png",
    "nous-assets/references/style-cyan-xerox-poster.jpg",
]

prompt = """Create a brand identity mood board for Techne project in a dark grid layout. 1280x853 pixels. 2 rows of 3 panels each with thin borders between them. Underground research zine aesthetic, halftone dots, risograph grain.

Top left panel: Large bold white text 'TECHNE' at top. Smaller blue text 'NOUS BRANDING MULTIMODEL' below. Anime girl portrait with short dark bob hair, headband, pale skin, large black eyes with white catchlights, facing left. Tagline 'Codex-only projects adapted for any model' at bottom of panel.

Top middle panel: Header text 'IDENTITY LOCKUP'. Six color swatches in a row: blue #2847FF, light blue #80A6FF, gold #D6B25A, teal #2E706B, off-white #E6E6E6, black #0B0B0E. Labels under each: RISOGRAPH, PHOTOCOPY, CRT SCAN, PAPER, INK. Header text 'TYPOGRAPHY: Inter, JetBrains Mono'. Terminal text: '> initializing vision pipeline' '> decoding visual tokens' '> grounding in context'.

Top right panel: Header text 'PIPELINE'. Flow: PROMPT arrow to SEEDREAM arrow to IMPRINT arrow to OUTPUT. Small technical diagram with eye icon and gear icon connected by circuit lines. Text 'VISION ANALYSIS,' 'IMAGE GENERATION,' 'POST-PROCESS'.

Bottom left panel: Header text 'SYMBOLS'. Six small icons: star labeled SIGHT, eye labeled OBSERVATION, starburst labeled SIGNAL, circle labeled FOCUS, wing labeled HERMES, square labeled CODEX. Keywords: PERCEPTION, AGENCY, TOOL USE, VISION.

Bottom middle panel: Header text 'ANIME IDENTITY'. Centered anime girl mascot portrait. Text 'PORTAL' and Japanese text 'ポータル'. Text 'TECHNE' and Japanese '視覚スキル' (vision skill).

Bottom right panel: Header text 'MULTI-MODEL'. Text: 'Not locked to any single provider. Designed for any OpenAI-compatible endpoint.' 'IMAGE GENERATION  VISION ANALYSIS  POST-PROCESSING  BATCH PIPELINES.' 'No code lock-in. No vendor trap. Bring your own model.'

Full width footer at bottom: 'TECHNE IS HOW HERMES CRAFTS  VISION IS THE FIRST MESSAGE  PERCEPTION  REASONING  ACTION' 'FORKED FROM NOUS  BUILT FOR ANY MODEL  OPEN FUTURE'

Golden star symbol in top right corner. Thin golden border around entire image. Underground zine print texture, halftone, risograph grain, paper scuffs."""

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
    with open("techne_banner_final_raw.jpg", "wb") as f:
        f.write(dl.read())
print(f"Done: (sz) tk={data['usage']['total_tokens']}")