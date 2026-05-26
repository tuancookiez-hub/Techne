---
name: techne
description: "Nous Branding MultiModel — Codex-only visual identity projects adapted for any model. Image gen via Ark Seedream, vision via Kimi, analog imprint post-processing. No ChatGPT Plus required."
version: 1.0.0
author: Techne
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Vision, Image-Generation, Seedream, ByteDance-Ark, Kimi, Imprint]
    related_skills: []
---

# Techne — Nous Branding MultiModel

## Overview

**Codex-only Nous Research visual identity projects, adapted for any model.**

Use **ByteDance Ark Seedream-4.0** for image generation, **Kimi K2.6** for vision analysis, and the **Imprint pipeline** for analog print post-processing. No Codex CLI, no ChatGPT Plus.

This skill covers:

- **Image generation** — Text-to-image via Ark Seedream API
- **Image analysis** — Describe, QA, and understand local images via Kimi vision
- **Batch generation** — Multiple images from a prompt file
- **Identity-preserve generation** — Use reference images + Kimi description for consistent identity

**Auth is API key, not OAuth.** Uses `BYTEDANCE_API_KEY` from `.env` for generation and `KIMI_API_KEY` for vision.

---

## When to Use

- Generating images from text prompts
- Analyzing images in detail (who/what, style, mood, colors, composition)
- Generating portraits, editorial characters, scenes
- QA of generated images for consistency or artifacts

**Don't use for:**
- Quick image lookups (use Hermes `vision_analyze` tool if the image is a URL)
- Video generation (use Seedance models on Ark)
- 3D model generation (use Hyper3D on Ark)

---

## Prerequisites

| Requirement | Details |
|---|---|
| **Seedream model activated** | Activate `seedream-4-0-250828` on Ark dashboard |
| **BYTEDANCE_API_KEY** | Image gen key in `.env` |
| **KIMI_API_KEY** | Already configured for vision |

---

## Image Generation

### Basic Generation

```bash
python scripts/generate_image.py \
  "A photorealistic portrait of a woman in a Pacific Northwest forest at dawn" \
  output.jpg
```

Output is a 2K (2848x1600) JPEG image saved locally.

### Generate with Reference (Image-to-Image)

Seedream supports reference images directly — pass them with `--image`:

```bash
# Single reference for style/identity guidance
python scripts/generate_image.py --image reference.jpg \
  "Same person, different outfit, garden setting" output.jpg

# Multiple references (e.g., style + subject)
python scripts/generate_image.py --image style_ref.jpg --image subject.jpg \
  "Combine the style of image 1 with the subject from image 2" output.jpg
```

Local images are base64-encoded and sent as data URLs — no uploading needed.

### Batch with Consistent Reference

```bash
# Every generation in the batch uses the same reference for identity consistency
python scripts/batch_generate.py --image reference.jpg prompts.txt ./output
```

### Prompt Style Guide

| Use case | Style | Expected time |
|---|---|---|
| Iterative exploration | Brief single-line | ~8s |
| Final canonical assets | Verbose detailed description | ~8s |

---

## Image Analysis

### Analyze a Local Image

```bash
python scripts/analyze_image.py /path/to/photo.jpg \
  "Describe this image in detail — who/what, style, mood, colors, composition"
```

### QA Generated Images

```bash
python scripts/analyze_image.py /path/to/generated.jpg \
  "Does this image match the prompt? Any artifacts or inconsistencies?"
```

---

## Batch Generation

```bash
python scripts/batch_generate.py prompts.txt ./output
```

prompts.txt:
```
A futuristic city at sunset, digital art
A cat on a windowsill, watercolor
# This line is skipped
A mountain landscape, oil painting
```

---

## Messenger Delivery Workflow

For images requested over Telegram, Discord, or other messaging:

1. Generate via `generate_image.py`
2. Verify output with `file` / `ls -lh`
3. Run a quick `analyze_image.py` QA pass for scene match, artifacts
4. Deliver with `MEDIA:/absolute/path/to/file` in the final response

---

## Key API Details

**Endpoint:** `POST https://ark.ap-southeast.bytepluses.com/api/v3/images/generations`

**Default parameters:**
```json
{
  "model": "seedream-4-0-250828",
  "prompt": "...",
  "n": 1,
  "size": "2K",
  "response_format": "url",
  "watermark": true
}
```

Returns a URL valid for 24 hours. Scripts auto-download and save locally.

**Rate limits:** ~1 request/second recommended. Concurrent tasks shown on Ark dashboard.

---

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `401 Unauthorized` | Invalid API key | Check `BYTEDANCE_API_KEY` in `.env` |
| `Model not found/404` | Model not activated | Activate `seedream-4-0` on Ark dashboard |
| `403 Forbidden` | Free credits exhausted | Check quota on dashboard |
| `KIMI_API_KEY` error | Vision key missing | Check `KIMI_API_KEY` in `.env` |
| `Image not found` | Bad path | Use absolute paths |
| Timeout | Large image or slow API | Use `timeout=120` in terminal calls |

## Verification Checklist

- [ ] `seedream-4-0-250828` activated on Ark dashboard
- [ ] `BYTEDANCE_API_KEY` set in `.env`
- [ ] `KIMI_API_KEY` set in `.env`
- [ ] Test generation works: `python scripts/generate_image.py "test" test.jpg`
- [ ] Test analysis works: `python scripts/analyze_image.py test.jpg`
