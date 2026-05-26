"""Generate a clean mascot portrait for the mood board banner."""
import json, os, base64, urllib.request

KEY = ""
fp = os.path.expanduser("~/AppData/Local/hermes/.env")
with open(fp) as f:
    for line in f:
        if "BYTEDANCE_API_KEY" in line and "=" in line:
            KEY = line.split("=", 1)[1].strip()
            break

def d(path):
    with open(path, "rb") as f:
        b = base64.b64encode(f.read()).decode()
    e = os.path.splitext(path)[1].lower()
    m = {".jpg":"image/jpeg",".png":"image/png"}.get(e,"image/jpeg")
    return f"data:{m};base64,{b}"

# Use the actual Nous mascot ref + blueprint scene for lighting
refs = [
    "nous-assets/references/anime-nous-manga-xerox-portrait.png",
    "nous-assets/references/anime-nous-blueprint-scene.jpg",
    "nous-assets/references/style-blue-registration-character.jpg",
]

# Prompt focused on getting the correct Nous mascot right
prompt = "Anime portrait of young woman, short dark bob hair with outward-flipped ends, thick blunt bangs across forehead, pale light gray skin, large black anime eyes with white catchlights, thin light gray headband tying at crown, three-quarter view facing left, pensive neutral expression, small closed mouth with white highlight on lower lip, light gray collar clothing visible at shoulders. Muted dusty teal-gray background with subtle grain texture. Clean sharp black linework. Limited color palette: black, pale gray, dusty teal. Retro 90s anime style, printed sticker aesthetic, grainy paper texture."

body = json.dumps({
    "model": "seedream-5-0-260128",
    "prompt": prompt,
    "image": [d(r) for r in refs],
    "n": 1,
    "size": "2K",
    "response_format": "url",
    "watermark": False,
})

req = urllib.request.Request("https://ark.ap-southeast.bytepluses.com/api/v3/images/generations", data=body.encode(), headers={"Content-Type":"application/json","Authorization":f"Bearer {KEY}"})
with urllib.request.urlopen(req, timeout=120) as r:
    data = json.loads(r.read())

url = data["data"][0]["url"]
with urllib.request.urlopen(url, timeout=60) as dl:
    with open("mascot_raw.jpg", "wb") as f:
        f.write(dl.read())
print(f"Done: mascot_raw.jpg ({data['data'][0].get('size','?')})")