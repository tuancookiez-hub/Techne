#!/usr/bin/env python3
"""Analyze an image via Hermes vision_analyze or fallback to API.

For Hermes agents: use the vision_analyze tool directly instead.
This script provides a standalone CLI for debugging/testing.

Usage:
    python analyze_image.py <image_path> [question]
"""

import base64, json, os, sys, urllib.request

# Try multiple env vars and .env fallback
KIMI_KEY = ""
for var in ["KIMI_API_KEY", "MOONSHOT_API_KEY"]:
    KIMI_KEY = os.environ.get(var, "")
    if KIMI_KEY:
        break
if not KIMI_KEY:
    env_path = os.path.expanduser("~/AppData/Local/hermes/.env")
    if os.path.isfile(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("KIMI_API_KEY="):
                    KIMI_KEY = line.split("=", 1)[1].strip()
                    break

# Possible Kimi API endpoints
ENDPOINTS = [
    "https://api.moonshot.cn/v1/chat/completions",
    "https://api.kimi.com/coding/v1/chat/completions",
]


def try_vision(img_b64, mime, question, url):
    """Try vision analysis against one endpoint."""
    body = json.dumps({
        "model": "kimi-k2.6",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{img_b64}"}},
                {"type": "text", "text": question},
            ],
        }],
        "max_tokens": 2000,
    }).encode()

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {KIMI_KEY}",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
        if "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"]
    except Exception:
        pass
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: analyze_image.py <image_path> [question]")
        print()
        print("NOTE: In Hermes, use the vision_analyze tool instead.")
        print("      This script is a standalone fallback.")
        sys.exit(1)

    img_path = sys.argv[1]
    question = sys.argv[2] if len(sys.argv) > 2 else "Describe this image in detail"

    if not os.path.isfile(img_path):
        print(f"ERROR: Image not found: {img_path}")
        sys.exit(1)

    ext = os.path.splitext(img_path)[1].lower()
    mime = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".webp": "image/webp",
        ".gif": "image/gif",
    }.get(ext, "image/jpeg")

    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    if KIMI_KEY:
        for url in ENDPOINTS:
            result = try_vision(b64, mime, question, url)
            if result:
                print(result)
                return
        print("ERROR: All Kimi endpoints failed. Key may be expired.")
        sys.exit(2)
    else:
        print("ERROR: KIMI_API_KEY not found in env or .env")
        print("TIP: Use Hermes' vision_analyze tool instead - it's preconfigured.")
        sys.exit(1)


if __name__ == "__main__":
    main()