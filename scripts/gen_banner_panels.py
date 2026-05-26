"""Generate panel images for Techne 4K 21:9 mood board banner."""
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
    m = {".jpg":"image/jpeg",".png":"image/png",".webp":"image/webp"}.get(e,"image/jpeg")
    return f"data:{m};base64,{b}"

# Reference assets for consistent Nous branding
refs = [
    "nous-assets/references/anime-nous-manga-xerox-portrait.png",
    "nous-assets/references/anime-nous-blueprint-scene.jpg",
    "nous-assets/references/style-blue-registration-character.jpg",
]

# Panel definitions: (filename, size, prompt)
# Sizes for 4K 21:9 (3840x1664) composite:
# - hero: 1280x1664 (left 1/3)
# - top_mid: 1280x832 (top center)
# - bot_mid: 1280x832 (bottom center)
# - top_right: 640x832 (top right)
# - bot_right: 640x832 (bottom right)
# - far_right: 640x1664 (far right strip)
# Actually let's do a cleaner 5-panel layout:
# [  hero  ] [   wide_top   ] [  top_small  ]
# [  hero  ] [   wide_bot   ] [  bot_small  ]
# hero = 1280x1664, wide = 1280x832 each, small = 640x832 each
# Total: 1280 + 1280 + 640 = 3200... need 3840
# Let's do:
# [  hero  ] [  top_mid  ] [ top_right ] [  far_top  ]
# [  hero  ] [  bot_mid  ] [ bot_right ] [  far_bot  ]
# hero = 1280x1664, mid = 1024x832, right = 768x832, far = 768x832
# 1280+1024+768+768 = 3840 ✓

panels = [
    ("panel_hero", "2K", 
     "Anime portrait of young woman, short dark bob hair with outward-flipped ends, thick blunt bangs, pale light gray skin, large black anime eyes with white catchlights, thin light gray headband, three-quarter view facing left, pensive neutral expression. Muted dusty teal-gray background with subtle grain. Clean sharp black linework. Limited palette: black, pale gray, dusty teal. Retro 90s anime style, printed sticker aesthetic, grainy paper texture."),
    
    ("panel_top_mid", "2K", 
     "Cinematic wide shot of an ancient Greek workshop interior, stone walls with warm torchlight, wooden workbench covered with scrolls, bronze tools, clay tablets with geometric diagrams. Warm amber and deep indigo palette. Dust particles in light beams. Vintage print texture, risograph aesthetic, grainy zine style. Underground lab meets classical antiquity."),
    
    ("panel_bot_mid", "2K", 
     "Abstract visualization of neural network nodes merging with ancient Greek geometric patterns, glowing cyan and gold connections on dark indigo background. Sacred geometry meets machine learning. Vintage print texture, grainy paper, risograph dots. Limited color palette: indigo, cyan, gold, black."),
    
    ("panel_top_right", "2K", 
     "Close-up of hands holding a vintage film camera and a modern smartphone side by side, both capturing the same scene. Warm tungsten lighting, shallow depth of field. Retro 90s anime style, grainy paper texture, muted dusty teal and amber palette."),
    
    ("panel_bot_right", "2K", 
     "Stack of vintage zines and technical manuals on a metal desk, top zine showing abstract geometric cover art in cyan and orange. Overhead shot, dramatic side lighting. Grainy texture, risograph print aesthetic, dust particles."),
    
    ("panel_far_top", "2K", 
     "Minimalist composition: single ancient Greek column fragment with circuit board traces growing out of it like vines. Pale stone against deep indigo background. Clean linework, vintage print texture, limited palette."),
    
    ("panel_far_bot", "2K", 
     "Macro shot of vintage printer ink dots and halftone patterns forming an abstract landscape. Cyan, magenta, yellow, black ink colors. Extreme close-up, tactile paper texture, grainy, risograph aesthetic."),
]

out_dir = "banner_panels"
os.makedirs(out_dir, exist_ok=True)

for name, size, prompt in panels:
    print(f"\nGenerating {name}...")
    body = json.dumps({
        "model": "seedream-5-0-260128",
        "prompt": prompt,
        "image": [d(r) for r in refs],
        "n": 1,
        "size": size,
        "response_format": "url",
        "watermark": False,
    })
    
    req = urllib.request.Request(
        "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations",
        data=body.encode(),
        headers={"Content-Type":"application/json","Authorization":f"Bearer {KEY}"}
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read())
        url = data["data"][0]["url"]
        with urllib.request.urlopen(url, timeout=60) as dl:
            path = os.path.join(out_dir, f"{name}.jpg")
            with open(path, "wb") as f:
                f.write(dl.read())
        print(f"  Saved: {path}")
    except Exception as e:
        print(f"  FAILED: {e}")
