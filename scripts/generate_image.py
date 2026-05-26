#!/usr/bin/env python3
"""Generate an image via ByteDance Ark Seedream API. Supports text-to-image and image-to-image."""

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
MODEL = "seedream-4-0-250828"

MIME = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".png": "image/png", ".webp": "image/webp",
    ".gif": "image/gif", ".bmp": "image/bmp",
}


def file_to_data_url(path):
    """Convert a local image file to a base64 data URL."""
    ext = os.path.splitext(path)[1].lower()
    mime = MIME.get(ext, "image/jpeg")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{b64}"


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print("Usage: generate_image.py [--image ref1.jpg ...] <prompt> [output_path]")
        print()
        print("Examples:")
        print("  Text-to-image:")
        print("    python generate_image.py \"A cat\" output.jpg")
        print("  Image-to-image (with reference):")
        print("    python generate_image.py --image ref.jpg \"Same person, different scene\" output.jpg")
        sys.exit(1 if not args else 0)

    if not API_KEY:
        print("ERROR: Set BYTEDANCE_API_KEY env var")
        sys.exit(1)

    # Parse --image flags
    image_paths = []
    while args and args[0] == "--image":
        args.pop(0)
        if args:
            image_paths.append(args.pop(0))
        else:
            print("ERROR: --image requires a file path")
            sys.exit(1)

    prompt = args[0]
    output = args[1] if len(args) > 1 else ""
    postprocess = False
    pp_mode = "imprint"
    pp_intensity = 0.7

    # Check for --postprocess flag in output
    if output and output.startswith("--postprocess"):
        postprocess = True
        output = args[2] if len(args) > 2 else ""
    # Or check args after output
    if len(args) > 2 and args[2] == "--postprocess":
        postprocess = True
        pp_mode = args[3] if len(args) > 3 and not args[3].startswith("--") else "imprint"
        pp_intensity = float(args[4]) if len(args) > 4 and not args[4].startswith("--") else 0.7

    # Validate reference images
    for path in image_paths:
        if not os.path.isfile(path):
            print(f"ERROR: Reference image not found: {path}")
            sys.exit(1)

    # Add time context
    now = time.strftime("%Y-%m-%d %H:%M %Z")
    full_prompt = f"{prompt} [Generated at {now}]"

    body = {"model": MODEL, "prompt": full_prompt, "n": 1, "size": "2K",
            "response_format": "url", "watermark": False}

    # Attach reference images as data URLs
    if image_paths:
        body["image"] = [file_to_data_url(p) for p in image_paths]

    req = urllib.request.Request(
        URL,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"ERROR: API request failed: {e}")
        # Try reading response body for more detail
        if hasattr(e, "read"):
            try:
                detail = e.read().decode()
                print(f"Response: {detail[:500]}")
            except Exception:
                pass
        sys.exit(2)

    if "data" not in data or not data["data"]:
        print(f"ERROR: No image in response: {json.dumps(data, indent=2)}")
        sys.exit(3)

    img = data["data"][0]
    image_url = img.get("url", "")
    size = img.get("size", "unknown")

    if not image_url:
        print(f"ERROR: No URL in response")
        sys.exit(4)

    if output:
        try:
            with urllib.request.urlopen(image_url, timeout=60) as dl:
                img_data = dl.read()
            os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
            with open(output, "wb") as f:
                f.write(img_data)
            print(f"Saved: {output} ({size})")
            # Optional post-processing
            if postprocess:
                try:
                    from postprocess import process as pp
                    pp_path = output.rsplit(".", 1)[0] + "_imprint.png"
                    pp(output, pp_path, pp_intensity, pp_mode)
                    output = pp_path
                except ImportError:
                    print("WARNING: postprocess.py not found in scripts/. Skipping post-process.")
                except Exception as e:
                    print(f"WARNING: Post-processing failed: {e}")
        except Exception as e:
            print(f"ERROR: Download failed: {e}")
            print(f"URL (24h expiry): {image_url}")
            sys.exit(5)
    else:
        print(f"URL: {image_url}")
        print(f"Size: {size}")

    usage = data.get("usage", {})
    if usage:
        print(f"Tokens: {usage.get('total_tokens', '?')}")


if __name__ == "__main__":
    main()