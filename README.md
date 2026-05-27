# product-competitor-research

An evidence-backed competitor research skill for product demo recordings.

It surveys the video, extracts stable screenshots, verifies key claims on the web, preserves a local research package, and optionally publishes a polished Lark doc after the analysis is done.

## What it does

- **Survey the recording** — map the overall workflow and identify candidate features with timestamps
- **Extract stable screenshots** — choose reliable frames around key moments instead of trusting one brittle single-frame grab
- **Verify on the web** — confirm names, pricing, packaging, docs, and release claims on official sources
- **Add broader context when useful** — reviews, company background, funding, traffic, and competitive signals
- **Preserve local outputs** — screenshots, notes, and a structured manifest remain available even if no doc is published
- **Optionally publish to Lark** — only after the local analysis is complete

## Default outputs

- `frames_10s/`
- `contact_sheets/` (optional)
- `selected_screenshots/`
- `notes.md`
- `analysis_manifest.json`

## Install

```bash
npx skills add Candicezsss/product-competitor-research -g -y
```

### Prerequisites

| Tool | Install |
|------|---------|
| ffmpeg | `brew install ffmpeg` |
| Tavily CLI | See the `tavily-search` skill / `tvly` setup |
| lark-cli | `npm install -g @larksuite/cli` |
| lark-cli skills | `npx skills add larksuite/cli -g -y` |

First-time lark-cli setup (only if publishing to Lark):

```bash
lark-cli config init --new
lark-cli auth login --domain drive
```

## Usage

Examples:

```text
帮我做这个产品的视频竞品调研，这是录屏 @/path/to/recording.mp4
Watch this recording and tell me what the product actually does
分析这个竞品视频，重点看 agent workflow 和定价
```

The skill will gather any missing inputs such as product URL, the main competitive question, and whether the final result should stay local or be published to Lark.

## Example polished output

- [makeUGC.ai — stakeholder report example](https://www.feishu.cn/docx/ANvWdxGdJoQyKAxuXxtuh4XXsxb)

## Trigger phrases

The skill activates when you mention competitor analysis, competitor research, product video research, 敏捷研究, 竞品调研, 竞品分析, product demo review, or share a `.mp4` / `.mov` / `.webm` file and ask for structured insights.
