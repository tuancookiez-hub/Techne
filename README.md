# Nous Branding — MultiModel

![Banner](output/nous-branding-banner-composite-imprint.png)

**Nous Research visual identity, model-agnostic.**  
Forked from [hermes-theia-codex-vision](https://github.com/plntrprotocol/hermes-theia-codex-vision) and [nous-branding](https://github.com/plntrprotocol/nous-branding). Adapted to work with any image generation backend — no Codex CLI, no ChatGPT Plus required.

---

## What It Does

| Capability | How |
|---|---|
| **Image generation** | Text-to-image or image-to-image via ByteDance Ark Seedream-5.0 |
| **Analog post-processing** | 14-step imprint pipeline — risograph grain, CRT scanlines, xerox decay, plate wobble, ink bleed, paper texture, palette compression |
| **Image analysis** | Describe, QA, and understand images via Kimi K2.6 vision |
| **Batch generation** | Generate multiple images from a prompt file, with optional shared reference |
| **Identity-preserve** | Pass reference images with `--image ref.jpg` for consistent characters/style |

## Supported Models

| Model | Provider | Use Case | Cost |
|---|---|---|---|
| **Seedream 5.0** | ByteDance Ark | Primary image generation | Free tier (50 gens/day) |
| **Kimi K2.6** | Moonshot | Vision analysis, image QA | Pay-per-use |
| **Any OpenAI-compatible** | Any | Drop-in replacement for Codex | Varies |

**You do NOT need:**
- ❌ Codex CLI
- ❌ ChatGPT Plus subscription
- ❌ OpenAI API key
- ❌ Specific model vendor lock-in

## Quick Start

```bash
# Text-to-image
python scripts/generate_image.py "A portrait at dawn in a forest" out.jpg

# With style reference + automatic imprint post-processing
python scripts/generate_image.py --image ref.jpg \
  "Same aesthetic, different subject" out.jpg --postprocess

# Image-to-image with multiple references
python scripts/generate_image.py --image face.jpg --image scene.jpg \
  "Place person from image 1 into scene from image 2" out.jpg

# Batch with consistent reference
python scripts/batch_generate.py --image ref.jpg prompts.txt ./output

# Just post-process an existing image
python scripts/postprocess.py raw.png final.png --mode imprint --intensity 0.7

# Analyze an image
python scripts/analyze_image.py photo.jpg "Describe this"
```

## Banner Example

This banner was generated entirely with the pipeline below — 9 panels via Seedream 5.0, composited with PIL, imprint post-processed:

```bash
python scripts/gen_panels.py           # generate 9 panels
python scripts/composite_banner.py     # composite into 21:9 grid
python scripts/postprocess.py \
  output/nous-branding-banner-composite-raw.jpg \
  output/nous-branding-banner-composite-imprint.png \
  --mode imprint --intensity 0.4
```

## Pipeline

```
prompt + [--image refs] → Seedream-5.0 → raw output → Imprint post-process → final
                                                         ├─ risograph grain
                                                         ├─ xerox thresholding
                                                         ├─ registration offset
                                                         ├─ plate wobble
                                                         ├─ CRT scanlines
                                                         ├─ ink bleed
                                                         ├─ paper texture
                                                         ├─ palette compression
                                                         └─ ... 6 more effects
```

## Requirements

| Requirement | Details |
|---|---|
| **ByteDance Ark key** | `BYTEDANCE_API_KEY` in `~/.hermes/.env` — from your Ark console |
| **Seedream model** | `seedream-5-0-260128` — must be **activated** on the Ark dashboard |
| **Kimi API key** | `KIMI_API_KEY` in `.env` — for image analysis |
| **Python libs** | Pillow + numpy (pre-installed with Hermes) |

## Project Structure

```
.
├── SKILL.md                     # Hermes skill definition
├── README.md                    # this file
├── .gitignore                   # prevents key/image leaks
├── scripts/
│   ├── generate_image.py        # Seedream gen + --image refs + --postprocess
│   ├── batch_generate.py        # Batch gen with optional shared reference
│   ├── analyze_image.py         # Vision analysis via Kimi
│   ├── postprocess.py           # 14-step analog print pipeline
│   ├── gen_panels.py            # Generate banner panel images (no text)
│   └── composite_banner.py      # Composite panels into 4K 21:9 grid + text
├── references/                  # Style docs, design language, lane audits
│   ├── nous-branding-skill.md   # Upstream Nous branding style guide (v2.1)
│   ├── design.md                # Core design principles
│   ├── design-language.md       # Visual language spec
│   ├── pitfalls.md              # Known gotchas
│   ├── reference-index.md       # Reference image index
│   ├── reference-catalog.md     # Full reference catalog
│   ├── identity-constants-template.md
│   ├── v8-pipeline-notes.md     # Legacy pipeline docs
│   ├── v9-imprint-pipeline.md   # Current imprint pipeline spec
│   ├── v10-*.md / v11-*.md     # Style lane audits & candidates
│   └── x-posts/                 # Nous X/Twitter reference screenshots
├── nous-assets/                 # Style reference images (from upstream)
│   ├── references/              # Character & style reference PNGs/JPGs
│   └── palettes/                # Color palette references
├── banner_panels/               # Generated panel images (intermediate)
└── output/                      # Final images
```

## Why MultiModel?

The upstream projects require **Codex CLI + ChatGPT Plus** for image generation. This fork rewrites the execution layer to work with any model:

| Original | This Fork |
|---|---|
| `codex exec --image` (vision) | `analyze_image.py` / Hermes `vision_analyze` |
| `codex exec -s workspace-write` (image gen) | `generate_image.py` → Ark Seedream API |
| `--mode imprint` post-process | Same `postprocess.py`, added as optional pipeline step |
| ChatGPT Plus subscription required | **No subscription** — use free Ark quota or any API key |

Future: image → video → 3D, same principle — swap the backend, keep the skill.

## License

MIT — forked from [plntrprotocol/hermes-theia-codex-vision](https://github.com/plntrprotocol/hermes-theia-codex-vision) and [plntrprotocol/nous-branding](https://github.com/plntrprotocol/nous-branding). All upstream credit to Llovos/plntrprotocol.
