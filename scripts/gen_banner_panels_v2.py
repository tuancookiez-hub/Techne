"""Generate clean panel images for Techne banner — NO text, visuals only."""
import json, os, base64, urllib.request

KEY = ""
fp = os.path.expanduser("~/AppData/Local/hermes/.env")
with open(fp) as f:
    for ln in f:
        if ln.startswith("BYTEDANCE_API_KEY="):
            KEY = ln.strip().split("=", 1)[1]
            break

OUT = "banner_panels_v2"
os.makedirs(OUT, exist_ok=True)

PROMPTS = {
    "hero": (
        "Retro 1960s anime manga portrait of a young woman with black bob hair and white headband, "
        "large dark eyes, neutral expression looking left, high contrast lineart, muted textured teal background, "
        "no text, no letters, no words, no typography, no watermark, clean illustration only",
        "2K"
    ),
    "top_mid": (
        "Cinematic medieval stone dungeon workshop interior, warm wall torches, weathered workbench, "
        "old scrolls and drafting tools, atmospheric dust motes in narrow light beams, dark moody lighting, "
        "no text, no letters, no words, no typography, no labels, pure visual only",
        "2K"
    ),
    "bot_mid": (
        "Circular Greek key meander pattern border enclosing a neural network graph of glowing connected nodes, "
        "cyan and gold nodes on dark navy background, ancient meets modern, "
        "no text, no letters, no words, no typography, no labels, pure visual only",
        "2K"
    ),
    "top_right": (
        "Two hands holding cameras side by side — left hand holds vintage 35mm film SLR, right hand holds modern smartphone, "
        "soft bokeh background, warm lighting, analog meets digital, "
        "no text, no letters, no words, no typography, no labels, pure visual only",
        "2K"
    ),
    "bot_right": (
        "Stack of worn printed pamphlets and tech manuals on a scuffed dark work surface, "
        "retro-futurist geometric art visible on top pamphlet, vintage print aesthetic, "
        "no text, no letters, no words, no typography, no labels, pure visual only",
        "2K"
    ),
    "far_top": (
        "Ancient Greek marble column with circuit board traces radiating from behind it, "
        "deep navy background, classical antiquity merged with modern computing, "
        "no text, no letters, no words, no typography, no labels, pure visual only",
        "2K"
    ),
    "far_bot": (
        "Halftone dot pattern test patch with overlapping CMYK dot swatches, "
        "black blue pink yellow, vintage printer calibration aesthetic, "
        "no text, no letters, no words, no typography, no labels, pure visual only",
        "2K"
    ),
}

def gen(name, prompt, size):
    body = json.dumps({
        "model": "seedream-5-0-260128",
        "prompt": prompt,
        "size": size,
        "response_format": "b64_json",
        "watermark": False
    }).encode()
    req = urllib.request.Request(
        "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations",
        data=body, headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read())
    b64 = data["data"][0]["b64_json"]
    ext = "png"
    path = os.path.join(OUT, f"{name}.{ext}")
    with open(path, "wb") as f:
        f.write(base64.b64decode(b64))
    print(f"Saved: {path}")
    return path

for name, (prompt, size) in PROMPTS.items():
    gen(name, prompt, size)

print("\nAll clean panels generated.")
