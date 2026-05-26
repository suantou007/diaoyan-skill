# Reference: Good Competitor Study Structure

Source: Lark doc `CjfpdyinQo1df5xrQlvl7iTBgnb` — "Topview AI【敏捷研究】"

This document illustrates what a well-structured competitor agile research (敏捷研究) looks like.

## Document Structure

Use this structure only for the **full agile research** mode. Lightweight chat notes and Markdown/Feishu feature breakdowns should omit company, pricing, review, and funding sections unless the user explicitly asks for competitor research.

### 1. Executive Summary Callout (light-orange)

A single callout block at the top that combines positioning AND competitive judgment. This replaces any separate "优势与不足总结" section — put all competitive analysis here so the reader gets the full picture in 10 seconds.

Structure (from the makeUGC study, which refined the Topview format):
- **一句话介绍** — One-line positioning including what's their main play and what's new
- **核心亮点** — Numbered list (1-3 items) of competitive strengths
- **对比[our product]的差异和不足** — Numbered list (1-2 items) of key weaknesses vs our product, with `<text color="red">` highlighting critical gaps

Key principle: opinionated and comparative, not neutral. The reader should immediately understand whether this competitor is a threat.

### 2. 公司与团队 (Company & Team)

#### 基本信息 (Basic Info)
- Founding year, HQ location
- Parent company (if any)
- Funding rounds: amount, lead investors, use of funds

#### 创始人及核心成员 (Founders & Key Members)
- CEO and CTO backgrounds — previous companies and roles
- Relevant domain expertise (e.g., "built Alibaba's AI design platform 'Luban'")

#### 用户和客户 (Users & Customers)
- Website traffic from SimilarWeb (with screenshot)
- Estimated user count (derived from traffic)
- Comparison to competitors' traffic
- Typical customer profiles: enterprise brands + SMB segment
- Customer logos (with screenshot)

### 3. 产品介绍 (Product Introduction)

#### 核心功能 (Core Features)
- Prefer a **lark-table** with columns: 功能 | 功能描述 | 图片/视频示意 when each feature maps to 1-2 screenshots
- Each row is one feature; this is the default pattern because it keeps screenshots and descriptions visually bound together
- Put a unique image anchor in the image cell before insertion, e.g. `【IMG_ANCHOR:feature_01_storyboard】`, then insert the screenshot with `docs +media-insert --selection-with-ellipsis`
- If the feature is a multi-step flow, use a standalone subsection plus `<grid cols="2">` or `<grid cols="3">` instead of squeezing multiple images into a narrow table cell
- Highlight the standout feature with `<text bgcolor="light-yellow">**Feature Name**</text>`
- Include personal hands-on testing notes where possible
- Feature descriptions should be 2-4 sentences, specific about what it does and what the screenshot proves

#### 产品定位和优势 (Positioning & Advantages)
- 2-3 paragraphs on market positioning
- Numbered competitive advantages (typically 3)

#### 售卖方式和定价 (Sales Model & Pricing)
- Pricing tiers in a **lark-table**: Free | Starter | Business | Enterprise
- Row dimensions: price, credits, key feature limits, watermark, other features
- Note API pricing model if applicable

#### 产品评价 (Product Reviews)
- Source reviews from **G2**, **ProductHunt**, and other platforms
- Include both positive and negative reviews
- Use `<quote-container>` for review quotes (keep them short)
- Include review screenshots where possible
- Summarize overall sentiment and common complaints

### 4. Demo Videos
- Embed original recordings as playable `<file>` in `<view type="2">` wrappers
- Use `<grid cols="2">` for side-by-side comparisons (reference vs generated output)
- Readers value watching the demo themselves, not just seeing static screenshots

### 5. Structural Whiteboard (Optional)
- Use a Feishu/Lark whiteboard when the analysis needs to show relationships, not just evidence screenshots
- Good candidates: product capability maps, generation pipelines, agent workflows, user journeys, competitive positioning structures, funnels, timelines, and causal chains
- Generate `diagram.svg` first, then convert it through `@larksuite/whiteboard-cli` to OpenAPI JSON and write it into a Feishu whiteboard
- Do not insert the SVG only as a normal image when the user needs an editable board; the whiteboard is the primary artifact
- Before overwriting an existing whiteboard, run `whiteboard +update --overwrite --dry-run`; if the dry-run says existing nodes will be deleted, get user confirmation before writing

### 6. Related Links
- Links to related competitor analysis docs using `<mention-doc>`

**No separate "优势与不足总结" section.** All competitive judgment goes in the executive summary callout.

## Key Formatting Patterns

- **Callout blocks**: `<callout emoji="..." background-color="light-orange">` for summaries
- **Tables**: `<lark-table>` for core feature rows and pricing; use anchors in image cells to prevent screenshot/text mismatch
- **Image grids**: `<grid cols="2">` with `<column>` for side-by-side images or multi-step flows
- **Quotes**: `<quote-container>` for user reviews
- **Highlighting**: `<text bgcolor="light-yellow">` for standout items, `<text color="red">` for critical weaknesses
- **Embedded videos**: `<view type="2"><file token="..." name="..."/></view>` for playable recordings
- **Video comparisons**: `<grid cols="2">` with reference video vs output video side-by-side
- **Whiteboards**: SVG-first structural diagrams converted into Feishu/Lark whiteboard content for editable relationship maps

## Structural Principles (from production experience)

- **5-7 main feature sections**, not 10+. Merge related capabilities (e.g., category filtering → bullet under Content Library)
- **Section titles should describe the insight**, not the feature. "生成时自动弹出文件夹/项目选择器" > "视频生成与积分消耗"
- **Multi-step flows get grid layouts** with 2-4 screenshots, not a single frame
- **Relationship structures get whiteboards** when the reader needs to understand module dependencies, workflow transitions, or competitive positioning at a glance
- **Plan the full structure before building** — write stable image anchors into the document skeleton first, then insert media with `--selection-with-ellipsis`; mid-document delete-rebuild remains fragile and risks losing image tokens
