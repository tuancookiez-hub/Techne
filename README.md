# Nous Branding — MultiModel

![Banner](banner.png)

*Above: A 21:9 banner generated with this pipeline.*

![Styles Banner](banner2.png)

*Above: 18 generated posters in a dense collage — showcasing the full range of Nous visual identity lanes.*

**Nous Research visual identity, model-agnostic.**  
Forked from [hermes-theia-codex-vision](https://github.com/plntrprotocol/hermes-theia-codex-vision) and [nous-branding](https://github.com/plntrprotocol/nous-branding). Works with any image generation backend.

---

## What It Does

| Capability | How |
|---|---|
| **Image generation** | Text-to-image or image-to-image via any API (OpenAI-compatible, local, etc.) |
| **Analog post-processing** | 14-step imprint pipeline — risograph grain, CRT scanlines, xerox decay, plate wobble, ink bleed, paper texture, palette compression |
| **Image analysis** | Describe, QA, and understand images via any vision model |
| **Batch generation** | Generate multiple images from a prompt file, with optional shared reference |
| **Identity-preserve** | Pass reference images with `--image ref.jpg` for consistent characters/style |

## Quick Start

### How it works

1. **Configure your API** — Pick any image generation model (3 examples below)
2. **Generate images** — Text-to-image, with style references, or batch
3. **Post-process** — Run the imprint pipeline for analog print aesthetics
4. **Composite** — For banners: generate panels → composite with PIL → imprint

### 1. Configure your API

Edit `scripts/generate_image.py` and set your endpoint + key:

```python
# Example: OpenAI (DALL-E 3)
API_URL = "https://api.openai.com/v1/images/generations"
API_KEY = "sk-..."
MODEL = "dall-e-3"

# Example: Stability AI
# API_URL = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
# API_KEY = "sk-..."
# MODEL = "sd3-large"

# Example: Any OpenAI-compatible endpoint
# API_URL = "https://your-provider.com/v1/images/generations"
# API_KEY = "your-key"
# MODEL = "your-model"
```

Same for vision analysis in `scripts/analyze_image.py`.

### 2. Generate images

```bash
# Single image
python scripts/generate_image.py "A portrait at dawn in a forest" out.jpg

# With style reference + auto imprint
python scripts/generate_image.py --image ref.jpg \
  "Same aesthetic, different subject" out.jpg --postprocess

# Multiple references
python scripts/generate_image.py --image face.jpg --image scene.jpg \
  "Place person from image 1 into scene from image 2" out.jpg

# Batch generation
python scripts/batch_generate.py --image ref.jpg prompts.txt ./output

# Post-process existing image
python scripts/postprocess.py raw.png final.png --mode imprint --intensity 0.7

# Analyze an image
python scripts/analyze_image.py photo.jpg "Describe this"
```

## Banner Example

This banner was generated entirely with the pipeline below — 9 panels via image generation, composited with PIL, imprint post-processed:

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
prompt + [--image refs] → Image API → raw output → Imprint post-process → final
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
| **Image generation API** | Any OpenAI-compatible API, local model, or custom backend. Configure endpoint + key in `scripts/generate_image.py` |
| **Vision API** | Any vision-capable model. Configure in `scripts/analyze_image.py` |
| **Python libs** | Pillow + numpy (pre-installed with Hermes) |

## Project Structure

```
.
├── SKILL.md                     # Hermes skill definition
├── README.md                    # this file
├── .gitignore                   # prevents key/image leaks
├── banner.png                   # Example banner output
├── scripts/
│   ├── generate_image.py        # Image gen + --image refs + --postprocess
│   ├── batch_generate.py        # Batch gen with optional shared reference
│   ├── analyze_image.py         # Vision analysis
│   ├── postprocess.py           # 14-step analog print pipeline
│   ├── gen_panels.py            # Generate banner panel images (no text)
│   ├── gen_anime_portal.py      # Generate 4 poster tiles
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
└── output/                      # Final images
```

## Why MultiModel?

The upstream projects require **Codex CLI + ChatGPT Plus** for image generation. This fork rewrites the execution layer to work with any model:

| Original | This Fork |
|---|---|
| `codex exec --image` (vision) | `analyze_image.py` / any vision model |
| `codex exec -s workspace-write` (image gen) | `generate_image.py` → any image API |
| `--mode imprint` post-process | Same `postprocess.py`, model-agnostic |
| ChatGPT Plus subscription required | **Any backend** — swap the API, keep the pipeline |

## License

MIT — forked from [plntrprotocol/hermes-theia-codex-vision](https://github.com/plntrprotocol/hermes-theia-codex-vision) and [plntrprotocol/nous-branding](https://github.com/plntrprotocol/nous-branding). All upstream credit to Llovos/plntrprotocol.
