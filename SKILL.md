---
name: product-competitor-research
version: 3.0.0
description: "Analyze a competitor product from a demo recording and targeted web verification. Produce evidence-backed research notes with timestamps, screenshots, confirmed facts, open questions, and optional Lark publication. Use this skill whenever the user wants competitor analysis, product video research, 敏捷研究, 竞品调研, 竞品分析, feature evidence extraction, or a structured write-up from a .mp4/.mov/.webm demo."
---

# Product Competitor Research from Recording

Use this skill to turn a product demo recording into **evidence-backed** competitor research.

The default deliverable is a **local research package**. Lark publication is optional and happens only after the analysis is already complete.

Use one workflow:

1. inspect the recording
2. verify key claims on the web
3. preserve local evidence
4. optionally publish a polished report

## Before starting

Verify only the tools you actually need:

- **ffmpeg / ffprobe** — required for video work
- **Tavily search** (`tvly`) or the `tavily-search` skill — required for web verification
- **lark-cli** plus **lark-shared / lark-doc** — only if the user wants a Lark doc

If Lark publishing is not requested, do not spend turns on Lark setup.

## Upfront intake

Gather any missing inputs before analysis:

- recording path or video file
- product name and official URL if known
- the user’s main question / competitive angle
- whether the final deliverable should stay local or be published to Lark

Keep intake focused on the product, the user’s question, and whether publication is needed.

## Evidence rules

Keep three layers separate in notes and conclusions:

- **Observed in video**
- **Confirmed on web**
- **Inference / hypothesis**

Hard rules:

- Any capability not directly shown in the video or confirmed on an official source must be labeled as inference or omitted.
- Every screenshot-backed claim should carry a timestamp or timestamp range.
- Prefer “unknown / not shown / unverified” over overstated conclusions.
- Use official sources first for product names, feature names, pricing, packaging, integrations, and changelog claims.

## Workflow overview

1. Survey the video
2. Extract stable screenshots
3. Verify key claims on the web
4. Build a local research package
5. Optionally publish to Lark

## Phase 1: Survey the video

See [references/video_analysis.md](references/video_analysis.md) for commands and heuristics.

Goal: understand the whole demo before writing conclusions.

Minimum outputs from this phase:

- rough product workflow
- candidate feature list
- key timestamp ranges
- obvious gaps or ambiguous moments that need verification

Use low-frequency survey frames and contact sheets to avoid over-reading repetitive footage. Record feature candidates with:

- working feature name
- timestamp or range
- observed UI state
- likely user intent
- why it matters competitively
- confidence (`high` / `medium` / `low`)

## Phase 2: Extract stable screenshots

See [references/video_analysis.md](references/video_analysis.md).

Do not rely on a single screenshot extracted from one exact timestamp when the UI is moving.

For each candidate feature:

- capture a small burst around the target moment
- pick the most stable frame
- re-read the chosen frame before using it in conclusions
- use multiple images when the flow spans several screens

Always preserve survey frames, contact sheets, and selected screenshots in a persistent local folder before ending the session.

## Phase 3: Verify key claims on the web

See [references/search_recipes.md](references/search_recipes.md).

Web verification is part of the default workflow, not a premium add-on. At minimum, verify against:

- official homepage
- official docs or help center
- pricing or packaging page if relevant
- changelog / release notes / blog when the video shows newly launched behavior

Add broader market context only when it helps answer the user’s question:

- reviews: Reddit, ProductHunt, G2
- company / team / funding / traffic
- competitor comparisons

Keep source boundaries explicit in your notes.

## Phase 4: Build the local research package

See [references/output_schema.md](references/output_schema.md).

Always preserve a local package such as:

- `frames_10s/`
- `contact_sheets/` (optional but recommended)
- `selected_screenshots/`
- `notes.md`
- `analysis_manifest.json`

The local package is the default output and the fallback if publication is delayed or unnecessary.

## Phase 5: Optional Lark publication

Only do this when the user explicitly wants a Lark doc.
See [references/lark_publishing.md](references/lark_publishing.md).

Key rules:

- finish the analysis locally before publishing
- prefer token-first publishing and final-layout rebuilds
- do **not** use `--caption` for screenshots by default
- if explanation text is needed, add it as normal text below the image
- treat Lark as a publishing layer, not the source of truth for the analysis

When the user wants a polished stakeholder report, use [references/reference_doc_structure.md](references/reference_doc_structure.md) as a formatting reference.

## Default deliverable structure

Unless the user asks for another format, organize the findings as:

1. Executive summary
2. Product snapshot
3. Evidence-backed feature breakdown
4. Key workflow / user journey
5. Pricing / packaging
6. Market or review signals (only when helpful)
7. Open questions and unverified claims
8. Source assets

## Quality bar

Before finishing, confirm:

- screenshots match the claims they support
- timestamps are attached to screenshot-backed claims
- speculative claims are labeled or removed
- web verification used official sources for product facts
- the local evidence package is preserved and its path is stated
- any Lark output reflects the already-finished local analysis instead of serving as the working draft

For a final QA pass, use [references/checklist.md](references/checklist.md).
