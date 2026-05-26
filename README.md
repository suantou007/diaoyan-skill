# product-competitor-research

A Claude Code skill that turns a competitor's screen recording into a structured Lark doc — with features, screenshots, company background, pricing, and user reviews.

## What it does

Drop in a screen recording of a competitor product, and the skill will:

- **Extract features from the recording** — identifies distinct features, pulls high-quality screenshots, and pairs each with a description
- **Research the company** — founding info, team backgrounds, funding rounds, SimilarWeb traffic
- **Pull pricing** — tiers, limits, credit systems from the product's pricing page
- **Scrape user reviews** — real feedback from Reddit, ProductHunt, and G2
- **Generate a Lark doc** — structured, with interleaved screenshots and text, ready to share

## Two report modes

| Mode | What you get | Best for |
|------|-------------|----------|
| **Full report (敏捷研究)** | Executive summary + company/team + features with screenshots + pricing + user reviews | First time evaluating a new competitor |
| **Feature-only (功能拆解)** | Executive summary + features with screenshots and descriptions | Already know the company, just need to understand the product |

## Install

```bash
npx skills add Candicezsss/product-competitor-research -g -y
```

### Prerequisites

| Tool | Install |
|------|---------|
| ffmpeg | `brew install ffmpeg` |
| lark-cli | `npm install -g @larksuite/cli` |
| lark-cli skills | `npx skills add larksuite/cli -g -y` |

First-time lark-cli setup:
```bash
lark-cli config init --new
lark-cli auth login --domain drive
```

## Usage

Just tell Claude what you want:

```
"帮我做个竞品调研，这是录屏 @/path/to/recording.mp4"
"I want to do a feature breakdown of this competitor"
"Watch this recording and extract the key features"
```

The skill will ask you for anything it still needs — report scope, what to highlight, and a recording if you haven't provided one.

## Example outputs

- [makeUGC.ai — Full report (敏捷研究)](https://www.feishu.cn/docx/ANvWdxGdJoQyKAxuXxtuh4XXsxb)
- [Higgsfield Super Computer — Feature-only (功能拆解)](https://www.feishu.cn/docx/KJRpdOtuyogz2fxMKdbuy7Nlsbg)

## Trigger phrases

The skill activates when you mention: competitor analysis, competitor research, product feature research, 敏捷研究, 功能拆解, 竞品调研, 竞品分析, product demo review, feature breakdown, or share a .mp4/.mov/.webm file asking for insights.
