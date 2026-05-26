"""Generate 9 panels, one per v11 Expanded Lane."""
import os, json, base64, urllib.request
from PIL import Image

API_KEY=*** = os.path.expanduser("~/AppData/Local/hermes/.env")
if os.path.isfile(env_path):
    with open(env_path) as f:
        for line in f:
            line=line.strip()
            if line.startswith("BYTEDANCE_API_KEY="):
                API_KEY=***

ROOT="F:\\HermesVision\\AndurilsVision"
OUT_DIR=os.path.join(ROOT,"banner_panels")
os.makedirs(OUT_DIR, exist_ok=True)

refs_dir=os.path.join(ROOT,"nous-assets","references")

def ref(name):
    p=os.path.join(refs_dir,name)
    return p if os.path.isfile(p) else None

def file_to_data_url(path):
    ext=os.path.splitext(path)[1].lower()
    mime={".jpg":"image/jpeg",".png":"image/png"}.get(ext,"image/jpeg")
    with open(path,"rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"

def gen(prompt, ref_files):
    images=[file_to_data_url(r) for r in ref_files if r and os.path.isfile(r)]
    body={
        "model":"seedream-5-0-260128",
        "prompt":prompt,
        "n":1,
        "size":"2K",
        "response_format":"url",
        "watermark":False,
        "image":images
    }
    req=urllib.request.Request(
        "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations",
        data=json.dumps(body).encode(),
        headers={"Content-Type":"application/json","Authorization":f"Bearer {API_KEY}"}
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        data=json.loads(resp.read())
    img_url=data["data"][0]["url"]
    with urllib.request.urlopen(img_url, timeout=60) as dl:
        return Image.open(dl).convert("RGB")

lanes=[
    ("lane_01_retro_media",
     "Retro media player interface relic. CRT monitor glow, VHS tracking lines, cyan UI elements on black. 90s software aesthetic, pixelated icons, scanlines. NO TEXT.",
     [ref("Hermes-player-reference.png"), ref("style-cyan-xerox-poster.jpg"), ref("style-rough-print.jpg")]),
    
    ("lane_02_newspaper",
     "Analog newspaper direct response ad. Rough newsprint texture, bold headline space, coupon cutout lines, classified ad layout. Vintage print ad aesthetic. NO TEXT.",
     [ref("Hermes4.3-reference .png"), ref("style-rough-print.jpg"), ref("style-cyan-xerox-poster.jpg")]),
    
    ("lane_03_hermetic",
     "Ornate hermetic print artifact. Medieval broadside, alchemical symbols, gold leaf accents on aged parchment. Occult institutional seal, decorative border. NO TEXT.",
     [ref("Hermes-jam-reference.png"), ref("Hermes-classical-reference .png"), ref("style-rough-print.jpg")]),
    
    ("lane_04_cyanotype",
     "Cyanotype surveillance city. Blue-toned urban aerial photo, analog security camera aesthetic, evidence marker, urban anomaly archive. Prussian blue monochrome. NO TEXT.",
     [ref("Computersaysno-reference .png"), ref("style-blue-registration-character.jpg"), ref("style-cyan-xerox-poster.jpg")]),
    
    ("lane_05_network",
     "Network diagram primitive. Hand-drawn node graph, civic infrastructure map, community connection web. Minimal line art, dot matrix printer aesthetic. NO TEXT.",
     [ref("Hermes-together-reference.png"), ref("Nous-Discord-reference .png"), ref("Hermes-mind-reference.png"), ref("style-cyan-xerox-poster.jpg")]),
    
    ("lane_06_veiled",
     "Veiled classical artifact. Close-cropped marble statue fragment, draped fabric, museum scan aesthetic. Occult archive record, soft focus, aged paper texture. NO TEXT.",
     [ref("image 3.PNG"), ref("Hermes-classical-reference .png"), ref("style-blue-registration-character.jpg"), ref("style-rough-print.jpg")]),
    
    ("lane_07_planetary",
     "Planetary broadcast identity. Satellite-era communication card, Earth from space, broadcast tower signals. Retro futurism, 70s NASA aesthetic, cyan and gold. NO TEXT.",
     [ref("image0 2.JPG"), ref("Hermes-together-reference.png"), ref("Nous-Discord-reference .png"), ref("style-cyan-xerox-poster.jpg")]),
    
    ("lane_08_multiples",
     "Manufactured multiples. Repeated product array, industrial packaging grid, ritual objects in rows. Duotone cyan and black, factory aesthetic, stamped labels. NO TEXT.",
     [ref("image0 3.JPG"), ref("style-industrial-duotone-grid.jpg"), ref("style-cyan-xerox-poster.jpg"), ref("style-rough-grain.jpg")]),
    
    ("lane_09_motorsport",
     "Motorsport sponsor field research. Racing livery stripes, rally car aesthetic, field research team patches. Industrial duotone, speed lines, sponsor logo spaces. NO TEXT.",
     [ref("Nous-car-reference.png"), ref("style-industrial-duotone-grid.jpg"), ref("style-rough-grain.jpg")]),
]

for name, prompt, refs in lanes:
    refs=[r for r in refs if r]
    print(f"Generating {name}...")
    try:
        img=gen(prompt, refs)
        img.save(os.path.join(OUT_DIR, f"{name}.jpg"), "JPEG", quality=92)
        print(f"  Saved: {name}.jpg ({img.size})")
    except Exception as e:
        print(f"  ERROR: {e}")
