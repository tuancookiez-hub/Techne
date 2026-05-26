#!/usr/bin/env python3
"""Batch generate images from a prompt file using ByteDance Ark Seedream API."""

import base64, json, os, sys, time, urllib.request

API_KEY = os.environ.get("BYTEDANCE_IMAGE_API_KEY") or os.environ.get("BYTEDANCE_API_KEY", "")
if not API_KEY:
    env_path = os.path.expanduser("~/AppData/Local/hermes/.env")
    if os.path.isfile(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("BYTEDANCE_API_KEY="):
                    API_KEY = line.split("=", 1)[1].strip()
                    break

URL = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"
MODEL = "seedream-5-0-260128"

MIME = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".png": "image/png", ".webp": "image/webp",
    ".gif": "image/gif", ".bmp": "image/bmp",
}


def file_to_data_url(path):
    ext = os.path.splitext(path)[1].lower()
    mime = MIME.get(ext, "image/jpeg")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{b64}"


def generate_one(prompt, output_path, ref_images=None):
    """Generate a single image, return True on success."""
    body = {"model": MODEL, "prompt": prompt, "n": 1, "size": "2K",
            "response_format": "url", "watermark": True}
    if ref_images:
        body["image"] = [file_to_data_url(p) for p in ref_images]

    req = urllib.request.Request(
        URL,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

    if "data" not in data or not data["data"]:
        print(f"  ERROR: No image: {json.dumps(data, indent=2)[:300]}")
        return False

    img_url = data["data"][0].get("url", "")
    if not img_url:
        return False

    try:
        with urllib.request.urlopen(img_url, timeout=60) as dl:
            img_data = dl.read()
        with open(output_path, "wb") as f:
            f.write(img_data)
        return True
    except Exception as e:
        print(f"  ERROR: Download failed: {e}")
        print(f"  URL (24h): {img_url}")
        return False


def main():
    args = sys.argv[1:]
    if len(args) < 2 or args[0] in ("-h", "--help"):
        print("Usage: batch_generate.py [--image ref.jpg ...] <prompt_file> <output_dir>")
        print("  prompt_file: one prompt per line. Lines starting with # are skipped.")
        print("  --image: optional reference image(s) applied to all generations")
        sys.exit(1 if args and args[0] not in ("-h", "--help") else 0)

    if not API_KEY:
        print("ERROR: Set BYTEDANCE_API_KEY env var")
        sys.exit(1)

    # Parse --image
    ref_images = []
    while args and args[0] == "--image":
        args.pop(0)
        if args:
            ref_images.append(args.pop(0))
        else:
            print("ERROR: --image requires a file path")
            sys.exit(1)

    prompt_file = args[0]
    output_dir = args[1]

    if not os.path.isfile(prompt_file):
        print(f"ERROR: Prompt file not found: {prompt_file}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    with open(prompt_file) as f:
        prompts = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]

    if not prompts:
        print("ERROR: No valid prompts found")
        sys.exit(1)

    now = time.strftime("%Y-%m-%d %H:%M %Z")

    success = 0
    for i, prompt in enumerate(prompts, 1):
        padded = f"{i:03d}"
        out_path = os.path.join(output_dir, f"{padded}.png")
        full_prompt = f"{prompt} [Generated at {now}]"

        print(f"=== #{i}: {prompt[:60]}... ===")
        if generate_one(full_prompt, out_path, ref_images):
            print(f"  → Saved: {out_path}")
            success += 1
        else:
            print(f"  ✗ Failed: {prompt[:60]}")

        if i < len(prompts):
            time.sleep(1)  # rate limit buffer

    print(f"BATCH DONE: {success}/{len(prompts)} images generated in {output_dir}")
    sys.exit(0 if success == len(prompts) else 1)


if __name__ == "__main__":
    main()