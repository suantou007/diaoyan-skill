---
name: product-competitor-research
version: 2.6.0
description: "Analyze product demos or competitor products from recordings and/or web research, with selectable output modes from lightweight chat notes to full Lark agile research (敏捷研究). Use this skill whenever the user mentions product demo review, feature breakdown from video, 视频解析, 视频截图分析, 视频帧提取, 视频采样, 录屏分析, ffmpeg 截图, competitor analysis, competitor research, product feature research, watch recording of competitor, 敏捷研究, 功能拆解, 竞品调研, or 竞品分析. Keep the trigger broad for video/product analysis, but only start competitor/web research when the user explicitly asks for 竞品/调研/竞品分析/competitor research or chooses the full agile research mode. The skill covers video sampling, screenshot extraction, image/text alignment in Lark docs, optional SVG-to-Feishu/Lark whiteboard structural visualizations, lightweight feature writeups, and full competitor research with company/pricing/review sources."
---

# 竞品调研 — 从录屏到飞书报告

将产品演示录屏转化为轻量视频解析、功能拆解或完整飞书竞品调研文档。支持从纯聊天结论到完整敏捷研究的多种输出模式；当产品关系、流程、架构或竞品定位适合可视化时，支持先生成 SVG，再通过 Lark 转化为可编辑的飞书画板内容。

参考文档结构见 [references/reference_doc_structure.md](references/reference_doc_structure.md)（基于真实竞品研究报告）。

## 前置依赖

开始前，按所选输出模式验证必要依赖是否可用。录屏分析需要 ffmpeg/ffprobe，飞书文档需要 lark-cli/lark-doc，结构画板才需要 lark-whiteboard 和 whiteboard-cli；如有缺失，帮助用户安装后再继续。

### 工具

| 依赖 | 用途 | 检查 | 安装 |
|---|---|---|---|
| **ffmpeg / ffprobe** | 从录屏中提取视频帧（采样 + 高清） | `ffmpeg -version` | `brew install ffmpeg` (macOS) |
| **Python 3** | 编写飞书文档构建脚本，处理图文交错 | `python3 --version` | macOS 通常已预装 |
| **lark-cli** | 创建/更新飞书文档、插入图片、管理权限 | `lark-cli --version` | `npm install -g @larksuite/cli` |
| **@larksuite/whiteboard-cli** | 将 SVG 转为飞书画板 OpenAPI JSON | `npx -y @larksuite/whiteboard-cli@^0.2.10 -v` | npx 自动拉取 |

### Skills（Claude Code）

以下 skills 随 lark-cli 附带。如缺失，安装：`npx skills add larksuite/cli -g -y`

| Skill | 用途 | 检查 | 安装路径 |
|---|---|---|---|
| **[lark-shared](../lark-shared/SKILL.md)** | 认证 (`auth login`)、身份切换 (`--as user/bot`)、权限错误处理 | 读取 skill 确认存在 | `~/.claude/skills/lark-shared/SKILL.md` |
| **[lark-doc](../lark-doc/SKILL.md)** | `docs +create`、`docs +update`、`docs +media-insert`、`docs +fetch` — 所有文档操作 | `lark-cli docs +create --help` | `~/.claude/skills/lark-doc/SKILL.md` |
| **[lark-whiteboard](../lark-whiteboard/SKILL.md)** | 结构图/流程图/架构图等飞书画板内容创建与更新 | `lark-cli whiteboard --help` | `~/.claude/skills/lark-whiteboard/SKILL.md` |

### 工具权限

| 工具 | 用途 | 适用范围 |
|---|---|---|
| **搜索工具** | 公司信息、定价、用户评价（Reddit/ProductHunt/G2） | 仅在用户明确要做竞品/调研，或选择完整敏捷研究时使用。优先用当前环境可用的高质量搜索工具；如有 tavily-search/web-access 则优先，其次 WebSearch/WebFetch。 |

### 首次配置

如果本机从未配置过 lark-cli：
```bash
lark-cli config init --new
```
这会启动交互式设置流程 — 从输出中提取授权链接并分享给用户。

如果 lark-cli 已安装但用户未认证：
```bash
lark-cli auth login --domain drive
```
这会授予创建和编辑飞书文档的权限。认证 scope 和身份类型的详细信息见 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)。

## Phase 0: 前置收集（分析开始前）

当用户描述要分析的产品、录屏或竞品时，先判断用户是否已经给出足够信息。用户初始消息中已经提供的信息可以直接跳过；缺少输出偏好时必须给用户选择，不要替用户默认做重型飞书调研。

### 0a. 屏幕录制（强烈推荐）

如果用户没有提供录屏，主动建议："如果你有产品的屏幕录制（.mp4/.mov/.webm），我可以从中提取截图、直接识别 UI 中的功能，写出准确度更高的报告。这决定了报告是基于产品真实样貌，还是泛泛的网络调研总结。"

录屏**不阻塞流程** — 没有也能继续。报告仍可通过用户提供的上下文构建；只有在用户明确要求竞品/调研或选择完整敏捷研究时，才补充网络调研。否则不要把普通视频解析升级成竞品研究。

无论是否有录屏，都要鼓励用户分享更多上下文 — 产品 URL、笔记、自己的印象 — 确保产出符合人的判断而非泛泛的网络抓取。

### 0b. 输出模式与轻重选择

主动给用户选择输出模式；如果用户已明确指定（如"做完整竞品调研"、"只要快速总结"），直接采用该模式。

1. **轻量聊天结论**：不建飞书文档。输出 5-8 条核心观察、关键截图时间点和风险/机会判断。适合快速看懂录屏。
2. **Markdown 功能拆解**：输出结构化 Markdown。包含 executive summary、5-7 个核心功能、截图清单/时间戳。适合先审内容再决定是否进飞书。
3. **飞书功能拆解**：创建轻量 Lark 文档。只做产品介绍和功能截图，不做公司/融资/定价/用户评价。
4. **完整报告（敏捷研究）**：创建完整 Lark 文档。包含 Executive summary + 公司/团队/融资 + 功能及截图 + 定价层级 + Reddit/ProductHunt/G2 用户评价。

**可选增强：飞书画板结构图**。当用户提到结构图、流程图、架构、能力关系、agent pipeline、用户路径、竞品定位矩阵，或分析中出现文字/表格难以表达的关系结构时，询问是否额外生成飞书画板。画板不是完整报告的必选项；只有结构表达明显更清晰，或用户明确要求“看板/画板/结构图”时才执行。

如果用户只是说"解析视频/总结录屏/看看这个产品"，默认提供以上四档选择，并说明推荐从轻量聊天结论或 Markdown 功能拆解开始。只有用户明确说"竞品"、"调研"、"竞品分析"、"competitor research"，或选择第 4 档时，才启动完整网络竞品调研。结构画板只作为可选增强，不要把普通视频解析自动升级为画板制作。

### 0c. 重点关注方向

"你希望我重点关注哪些功能或竞争维度？比如：agent 架构、定价模型、某个特定能力、与某产品在 X 方面的对比。"

这决定了 executive summary 的侧重和哪些功能获得深度覆盖。没有用户输入，报告容易变得泛泛而谈，无法服务于用户真正需要做的决策。

## 工作流概览

```
┌──────────────────────────────────────────────────────┐
│  Phase 0: 前置收集                                      │
│     ├── 屏幕录制（推荐，非必须）                          │
│     ├── 输出模式（轻量聊天 / Markdown / 飞书功能 / 完整）  │
│     ├── 竞品调研门槛（用户明确要竞品/调研才启动）           │
│     └── 重点关注方向                                    │
├──────────────────────────────────────────────────────┤
│  Phase 1: 视频 → 多策略采样 → 功能识别  ← 有录屏时执行    │
│  Phase 2: 高清截图提取与逐张校验        ← 有录屏时执行    │
│  Phase 3: 网络调研                  ← 仅完整/明确调研     │
│     ├── 公司及团队背景                                  │
│     ├── 用户与流量（SimilarWeb）                         │
│     ├── 定价与方案                                      │
│     └── 用户评价（Reddit, ProductHunt, G2）              │
│  Phase 4: 构建输出（聊天 / Markdown / 飞书 / SVG→画板）       │
│     └── 结构类内容可选生成 SVG → 飞书画板                       │
│  Phase 5: 权限检查与授权（飞书模式）                       │
└──────────────────────────────────────────────────────┘
```

---

## 输出模式

### 轻量聊天结论

用于用户只想快速看懂录屏或产品时。不要创建飞书文档，不做公司/定价/评价调研。输出：
- 3-5 句结论先行
- 5-8 条功能/体验观察，每条带时间戳或截图候选
- 1-3 条值得继续深挖的问题

### Markdown 功能拆解

用于用户想先审内容、不急着进飞书时。输出 Markdown，结构同"功能拆解"但图片以本地截图路径/时间戳清单表示。不要调用 Lark。

### 飞书功能拆解 / 完整报告

只有用户选择飞书输出时才创建 Lark 文档。飞书功能拆解只包含产品定位、核心功能和截图；完整报告才包含公司、融资、定价、评价等外部调研。

### 可选：飞书画板结构图

用于表达“关系”和“结构”，不是替代截图表格。适合以下内容：产品能力地图、生成链路/agent pipeline、用户路径、信息架构、多角色协作流程、竞品定位关系、商业化漏斗、时间线或因果链路。

执行方式固定为：**先生成 SVG 源图，再用 Lark whiteboard 工具转成飞书画板内容**。不要只把 SVG 当普通图片贴进文档；画板的价值是可编辑、可缩放、可继续协作。

## 输出文档结构 — 完整报告（敏捷研究）

最终飞书文档按以下结构组织（基于验证过的竞品研究格式）：

### 1. Executive Summary Callout

文档顶部放置 `<callout emoji="bulb" background-color="light-orange">`。callout 内合并产品定位、核心亮点和竞争对比 — 不要在末尾单独创建"优势与不足总结"章节。结构：

- **一句话介绍** — 一句话定位（谁做的、做什么的、核心打法是什么）
- **核心亮点** — 编号列表（1-3 条），该产品做得好的地方，以竞争优势角度呈现
- **对比与不足** — 编号列表（1-2 条），产品自身的关键不足和差距。基于产品本身进行分析 — 除非用户明确要求，否则不要引用抖音小游戏或任何特定竞品。用 `<text color="red">` 标注关键缺陷。

callout 是文档阅读量最高的部分。这里放有判断力的竞争评估，不是中性描述。读者应在 10 秒内理解竞争威胁/机会。

### 2. 公司与团队 (Company & Team)

来自**网络搜索**，非视频分析。

- **基本信息**：成立年份、总部、母公司、融资轮次（金额、投资方、资金用途）
- **创始人及核心成员**：CEO/CTO 背景、过往经历、相关专业能力
- **用户和客户**：SimilarWeb 流量数据、估算用户量、与竞品对比、典型客户画像、知名品牌 logo

### 3. 产品介绍 (Product Introduction)

#### 核心功能 (Core Features) — 来自视频分析

这是基于视频分析构建的章节。**优先使用表格或稳定锚点结构来绑定文字与截图**，核心目标是让每张图和对应功能描述在飞书中保持同一行/同一段，不再出现图片集中在末尾或错位。

推荐表格列：`功能 | 功能描述 | 图片/视频示意`。每个功能一行：
1. `功能`：洞察型功能名，可用 `<text bgcolor="light-yellow">` 高亮最突出的功能
2. `功能描述`：2-4 句，说明功能做什么、UI/流程如何表现、竞争层面的意义
3. `图片/视频示意`：放对应截图、截图锚点或多图 grid

如果某个功能是多步骤流程，表格单元格过窄会影响阅读时，改用独立子章节 + `<grid cols="2">` / `<grid cols="3">` 展示多张截图。无论用表格还是章节，都要使用唯一锚点（如 `【IMG_ANCHOR:feature_slug】`）或 selection 定位，让 `media-insert` 插入到对应功能附近，而不是 append 到文档末尾。

对于视频中没有清晰展示但产品网站上可发现的功能，仅在用户明确要竞品/调研或完整报告时通过网络搜索补充；普通视频解析不要擅自扩展成外部调研。

#### 产品定位和优势 (Positioning & Advantages)

来自网络搜索，2-3 段关于产品如何定位自己的描述。通常包含 3 条编号的竞争优势。

#### 售卖方式和定价 (Sales Model & Pricing)

来自产品定价页的**网络搜索**。使用 **lark-table** 展示定价层级：

| | Free | Starter | Business | Enterprise |
|---|---|---|---|---|
| 价格 | ... | ... | ... | ... |
| Key limits | ... | ... | ... | ... |

同时标注 SaaS 和 API 定价模式（如适用）。

#### 产品评价 (Product Reviews)

来自 **Reddit**、**ProductHunt**、**G2** 的搜索。包含：
- 整体评分/情感倾向
- 2-3 条正面引用，使用 `<quote-container>` 块
- 1-2 条负面引用，展示真实的痛点
- 评价截图（如有）

### 4. Demo 视频（有录屏时）

将原始录屏以 `<file>` 元素嵌入，使用 `<grid>` 布局，让读者可以直接观看 demo。如果用户也测试了产品并有输出视频（如生成的内容），创建对比 grid 展示参考输入和生成输出 side-by-side，附带质量观察说明。

### 5. 结构画板（可选）

当报告中存在复杂关系结构（如功能地图、生成链路、agent 协作流程、用户路径、竞品定位关系）时，在飞书文档中嵌入或链接一个画板。画板内容必须来自 SVG → Lark whiteboard 转换流程，而不是普通截图。

**不需要单独的"优势与不足总结"章节** — 竞争判断已在 executive summary callout 中体现。

### 6. 相关链接（可选）

使用 `<mention-doc>` 引用相关分析文档。

---

## 输出文档结构 — 功能拆解

当用户选择**功能拆解**范围时使用此结构。更加精简 — 无公司信息、无定价、无评价。参考 Higgsfield Super Computer 分析报告格式。

### 1. Executive Summary Callout

同样使用 `<callout emoji="bulb" background-color="light-orange">` 格式：

- **一句话介绍** — 一句话定位
- **核心亮点** — 编号列表（1-3 条），以竞争优势角度呈现
- 可选 **对比不足** — 基于产品本身分析不足。除非用户明确要求，否则不要引用抖音小游戏或任何特定竞品。

### 2. 功能章节（共 5-7 个）

优先使用能保证图文对应的结构：
- **一图/少图对应一个功能**：用 `功能 | 功能描述 | 图片/视频示意` 表格，每行一个功能
- **多步骤流程**：用独立 `## N. 洞察型标题` 章节 + 2-4 张截图 grid

每个功能包含：
- 1-2 张截图或截图锚点，必须和对应功能描述在同一行/同一段附近
- 2-4 句描述，说明功能做什么、视频中如何展示、竞争层面的意义
- 必要时用 `---` 分隔各功能块

章节标题应描述功能的特别之处，而非仅仅命名。例如："视觉分镜先行的视频生成管线" 而非 "视频生成功能"。

将相关能力合并到同一章节 — 一个典型产品应有 5-7 个功能章节，而非 10+。

### 3. 结构画板（可选）

如果功能拆解中出现“多个模块如何协同”“用户从输入到产出的路径”“agent 或生成管线如何流转”这类结构问题，增加一个飞书画板。先把结构抽象成 SVG，再转换为可编辑画板；不要把画板用于展示单张 UI 截图，截图仍放在功能表格或 grid 中。

**无公司/团队章节，无定价表，无评价章节；是否嵌入 demo 视频或结构画板取决于用户是否选择飞书输出及是否需要结构表达。**

---

## Phase 1: 视频分析 — 多策略采样与功能识别

> **需要录屏。** 如果没有提供录屏，跳过 Phase 1-2。功能章节通过用户提供的上下文来构建；只有明确竞品/调研时才补充网络信息。

不要只用固定每 10 秒一帧。固定采样会漏掉短暂弹窗、下拉菜单、hover 状态、生成结果页和快速切换的关键 UI。采用三段式采样：

```bash
WORKDIR="/tmp/competitor_analysis_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$WORKDIR/coarse" "$WORKDIR/scenes" "$WORKDIR/dense"

ffprobe -v error -show_entries format=duration -of csv=p=0 "<video_path>"

# A. 全局粗采样：建立视频地图
ffmpeg -i "<video_path>" -vf "fps=1/10,scale=1280:-1" -q:v 3 "$WORKDIR/coarse/frame_%04d.jpg"

# B. 场景变化采样：补捉快速 UI 切换
ffmpeg -i "<video_path>" -vf "select='gt(scene,0.25)',scale=1280:-1" -vsync vfr -q:v 3 "$WORKDIR/scenes/scene_%04d.jpg"

# C. 候选区间密集采样：围绕关键功能时间段补帧
ffmpeg -ss <START_TS> -t <DURATION_SECONDS> -i "<video_path>" -vf "fps=1,scale=1280:-1" -q:v 2 "$WORKDIR/dense/<feature_slug>_%03d.jpg"
```

执行顺序：
1. 先读 coarse 帧，建立时间线和主要功能块
2. 再读 scenes 帧，找被粗采样漏掉的弹窗、状态切换、结果页
3. 对每个候选功能记录时间区间，使用 dense 采样补到可读 UI 状态
4. 最后只保留 5-7 个主要功能进入报告；原始识别可以有 10-20 个候选，但要合并相关能力

每个候选功能记录：
1. **功能名称** — 简洁、描述性，优先写成洞察型标题
2. **时间区间** — 起止时间，而不是只记单个帧序号
3. **截图候选** — coarse/scenes/dense 中最能代表该功能的文件
4. **展示了什么** — UI 元素、agent 行为、关键差异化点
5. **为什么重要** — 用户价值或竞争意义
6. **置信度** — 高/中/低；低置信度功能不要写成确定事实

## Phase 2: 高清截图提取

对每个进入报告的功能，提取一张或多张高质量帧。沿用 Phase 1 的 `WORKDIR`，不要使用固定 `/tmp/competitor_analysis`，避免多任务或多视频互相覆盖。

```bash
mkdir -p "$WORKDIR/final"
ffmpeg -ss <TIMESTAMP> -i "<video_path>" -frames:v 1 -q:v 1 "$WORKDIR/final/<NN>_<feature_slug>.jpg"
```

`-q:v 1` = 近无损 JPEG。检查文件大小 — 小于 5KB 的帧通常已损坏。

### 关键步骤：逐一验证每张截图

**必须回看每张最终截图**，确认其展示的是对应功能的正确 UI 状态。采样帧只是候选证据 — 用户可能在采样间隔内滚过目标画面，scene 采样也可能只捕获转场。常见失败模式：
- 帧捕获到过渡/滚动画面而非静止的 UI 状态
- 功能跨多个屏幕但帧只捕获了一个
- 时间戳偏差几秒，显示的是前一个或后一个功能

对于展示多步骤流程的功能（如三步向导），考虑提取多帧并用 `<grid>` 布局展示，而非单一截图。构建文档时，如果某功能有多张图片，使用 `<grid cols="2">` 配合 `<column>` 元素。

## Phase 3: 网络调研（仅在明确需要时执行）

> **只在两种情况下执行：** 用户明确提到竞品/调研/竞品分析/competitor research，或用户选择完整报告（敏捷研究）。功能拆解、Markdown 拆解和轻量聊天结论默认跳过此阶段。不要把普通视频解析自动升级为外部竞品研究。

使用当前环境可用的搜索工具收集视频中无法获取的信息。尽可能将以下搜索作为并行子 agent 分发。每条关键事实必须在草稿中保留来源 URL 或来源名称；融资、定价、流量、用户评价不能无来源写入最终文档。

### 3a. 公司与团队
搜索：`"<公司名>" founded team funding crunchbase`
关注：成立日期、总部、创始人背景、融资轮次、投资方。

### 3b. 用户与流量
搜索：`"<公司名>" site:similarweb.com` 或 `"<产品URL>" monthly visits users`
关注：月网站流量、估算用户数、增长趋势。

### 3c. 定价
搜索：`"<公司名>" pricing plans` 或直接访问产品定价页。
关注：层级名称、价格、功能限制、积分系统、API 定价。

### 3d. 用户评价 — Reddit
搜索：`site:reddit.com "<产品名>" review`
关注：真实用户体验、投诉、赞誉、与替代品对比。

### 3e. 用户评价 — ProductHunt
搜索：`site:producthunt.com "<产品名>"`
关注：发布反响、评分、创始人回复、功能需求。

### 3f. 用户评价 — G2
搜索：`site:g2.com "<产品名>" reviews`
关注：星级评分、优劣模式、企业 vs 中小企业评价差异。

在最终文档中引用用户评价时，保持引用简短（1-2 句），使用 `<quote-container>` 格式。正面和负面评价都要包含。每条引用后标注来源平台；涉及金额、价格、融资、流量的事实要附来源链接或在相关链接区集中列出来源。

---

## Phase 4: 构建飞书文档

### 图文对齐构建模式

飞书文档的核心质量问题是图片和文字错位。不要把所有图片追加到文档末尾；先写入完整文本骨架和稳定锚点，再把图片插入到对应锚点附近。

推荐流程：

1. **先规划完整结构**：确定 executive summary、功能表/功能章节、定价、评价、demo 视频等全部章节。
2. **写入带锚点的 Markdown**：每个需要截图的位置放唯一可搜索锚点，例如 `【IMG_ANCHOR:feature_01_storyboard】`。
3. **使用 selection 插入图片**：用 `docs +media-insert --selection-with-ellipsis` 将图片插入到对应锚点，而不是无定位 append。
4. **逐张校验飞书渲染**：确认每张图仍在对应功能行/段附近；若锚点残留，最后再删除锚点文本。

核心功能推荐表格骨架：

```markdown
<lark-table rows="3" cols="3" column-widths="160,360,260">
  <lark-tr>
    <lark-td>**功能**</lark-td>
    <lark-td>**功能描述**</lark-td>
    <lark-td>**图片/视频示意**</lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td><text bgcolor="light-yellow">故事板驱动生成</text></lark-td>
    <lark-td>2-4 句说明功能表现和竞争意义。</lark-td>
    <lark-td>【IMG_ANCHOR:feature_01_storyboard】</lark-td>
  </lark-tr>
</lark-table>
```

图片插入命令：

```bash
lark-cli docs +media-insert \
  --doc "<DOC_ID>" \
  --file ./01_storyboard.jpg \
  --selection-with-ellipsis "【IMG_ANCHOR:feature_01_storyboard】" \
  --align center \
  --caption "故事板驱动生成界面"
```

如果当前 `lark-cli docs +media-insert --help` 确认没有 `--selection-with-ellipsis`，才退回逐章节追加模式；退回时必须按"标题 → 图片 → 描述"顺序构建，且每插一张图就校验位置。

### 关键：图片插入必须使用相对路径

`lark-cli docs +media-insert` **要求相对路径**。绝对路径会报 "unsafe file path" 错误。

```bash
# 错误
lark-cli docs +media-insert --doc "<DOC_ID>" --file "/Users/me/images/shot.jpg"

# 正确 — 相对路径 + 设置 cwd 到图片目录 + selection 锚点定位
cd /path/to/images && lark-cli docs +media-insert \
  --doc "<DOC_ID>" \
  --file ./shot.jpg \
  --selection-with-ellipsis "【IMG_ANCHOR:feature_slug】" \
  --align center \
  --caption "Description"
```

Python 脚本中使用 `subprocess.run([...], cwd=IMG_DIR, shell=False)`，不要拼接 shell 字符串。

### 构建脚本

图片较多（10+）或使用表格/锚点时，使用 Python 构建脚本避免 shell 转义问题。完整模板见 [references/build_script_template.py](references/build_script_template.py)。

关键模式：将 markdown 写入临时文件，通过 `--markdown @file` 传给 `lark-cli docs +update --api-version v2`；所有命令用 subprocess 参数列表执行，失败即停止。图片插入必须带 `--selection-with-ellipsis` 或明确记录 fallback 原因。

### 结构表达：SVG → 飞书画板

当内容本质是结构关系时，不要只用长段落、截图堆叠或普通图片表达。结构画板适合表达：
- 产品能力地图：模块、入口、能力边界、依赖关系
- 生成链路 / agent pipeline：输入、规划、检索、生成、审核、导出
- 用户路径：从导入素材到生成结果、二次编辑、发布的关键节点
- 竞品定位结构：产品之间的能力重叠、差异化、目标用户分层
- 商业化漏斗、时间线、因果链路或多角色协作流程

执行前先读取 [`../lark-whiteboard/SKILL.md`](../lark-whiteboard/SKILL.md)，遵循其认证、dry-run 和写入规则。本 skill 中的固定路线是：**先生成 SVG，再转换为飞书画板 OpenAPI JSON，最后写入 whiteboard**。

推荐产物放在当前项目目录下的时间戳目录，例如：

```text
./diagrams/YYYY-MM-DDTHHMMSS/
  diagram.svg
  diagram.json
  diagram.png
```

步骤：

1. **生成 SVG 源图**：用清晰的 SVG 表达结构。节点文字要短，层级要少，避免把报告全文塞进画板；每个节点只承载一个判断或结构点。
2. **创建或定位 whiteboard token**：如果飞书文档里还没有画板，先追加一个空白画板并从响应中取 `block_type == "whiteboard"` 的 `block_token`。
3. **SVG 转 OpenAPI JSON**：用 `@larksuite/whiteboard-cli` 将 SVG 转为飞书画板可写入的 JSON。
4. **dry-run 检查**：向已有画板写入前必须先 `--overwrite --dry-run`；如果输出提示会删除已有 nodes，必须向用户确认后才能执行真正写入。
5. **写入并回看**：写入后查询或打开文档确认画板可见、文字未溢出、结构关系清晰。

创建空白画板：

```bash
lark-cli docs +update \
  --api-version v2 \
  --doc "<DOC_ID>" \
  --command append \
  --content '<whiteboard type="blank"></whiteboard>' \
  --as user
```

SVG 转换并 dry-run：

```bash
npx -y @larksuite/whiteboard-cli@^0.2.10 -i "./diagrams/<TS>/diagram.svg" --to openapi --format json \
  | lark-cli whiteboard +update \
    --whiteboard-token "<WHITEBOARD_TOKEN>" \
    --source - --input_format raw \
    --idempotent-token "<TS>-structure-board" \
    --overwrite --dry-run --as user
```

确认安全后写入：

```bash
npx -y @larksuite/whiteboard-cli@^0.2.10 -i "./diagrams/<TS>/diagram.svg" --to openapi --format json \
  | lark-cli whiteboard +update \
    --whiteboard-token "<WHITEBOARD_TOKEN>" \
    --source - --input_format raw \
    --idempotent-token "<TS>-structure-board" \
    --overwrite --as user
```

不要把 SVG 只作为 `<image>` 插入文档；如果用户要的是可协作的结构表达，最终交付应是飞书画板。SVG/PNG 可以作为本地备份或预览，但不是主要交付物。

### Lark Markdown 语法参考

竞品研究中使用的关键格式元素：

```markdown
# Callout 块
<callout emoji="bulb" background-color="light-orange">
**内容**
</callout>

# 表格（核心功能、定价等场景使用）
<lark-table rows="3" cols="4" column-widths="125,210,210,210">
  <lark-tr>
    <lark-td>**表头**</lark-td>
    ...
  </lark-tr>
</lark-table>

# 图片 grid（并排布局）
<grid cols="3">
  <column width="33">
    <image token="..." width="366" height="642" align="center"/>
  </column>
  ...
</grid>

# 用户评价引用
<quote-container>
*"用户评价原文"*
— 来源, 日期
</quote-container>

# 文字高亮
<text bgcolor="light-yellow">**重点功能**</text>

# 嵌入视频/文件
<view type="2">
  <file token="..." name="demo.mp4"/>
</view>
```

### 频率限制

lark-cli 调用之间加 0.3–0.5s 延迟。迭代构建模式会产生大量 API 调用。

## Phase 5: 权限检查与授权

只有创建飞书文档时执行。不要默认手动授权；先检查 `docs +create --as bot` 返回的 `permission_grant` 字段。lark-cli 通常会尝试给当前 CLI 用户自动授予 `full_access`。

处理规则：
- `permission_grant.status = granted`：记录成功，无需额外授权
- `skipped`：提示用户先完成 `lark-cli auth login`，再继续授权
- `failed`：文档已创建成功，但需要重试授权或让用户申请访问

仅当自动授权 skipped/failed 或用户明确无法访问时，才执行手动授权：

```bash
# Step 1: 获取用户的 open_id
lark-cli contact +get-user

# Step 2: 授予用户 full_access（以 bot 身份执行）
lark-cli drive permission.members create \
  --params '{"token":"<DOC_ID>","type":"docx"}' \
  --data '{"member_type":"openid","member_id":"<user_open_id>","perm":"full_access","type":"user"}' \
  --as bot
```

如果授权失败（error 1063003/1063001 — 常见于应用缺少 `drive:drive` scope），明确告知用户文档已创建成功但可能需要申请访问权限或让 bot 手动分享。

---

## 经验教训（来自 makeUGC / SymphonyAI 研究）

以下模式来自实际生产运行，应指导后续执行。

### 构建前规划完整文档结构

在撰写任何内容前，确定完整的章节列表 — 包括子章节和每张图片的锚点。不要靠事后删减重建来挪图片：可能丢失 image token、错放章节或破坏 callout 结构。`--selection-with-ellipsis` 可以降低错位风险，但前提是你已经在文档骨架里放好了稳定、唯一的锚点。

### 绝不在 callout 边界附近做精确编辑

对 `<callout>` 块内或相邻内容使用 `replace_range` 和 `delete_range` 可能会不可预测地重新排列文档结构。如果标题被包裹在 callout 中，仅替换标题文本可能破坏 callout 并打散内容。倾向于重建整个 callout + 周边章节，而非修补单行。

Callout 内换行折叠是 lark-cli 已知限制 — 单 `\n` 在 callout 内会被折叠。接受这一点继续往下，不要花费多轮尝试修复。内容依然可读。

### 嵌入源录屏为可播放视频

不要只提取静态截图 — 使用 `<file token="..." name="..."/>` 包裹在 `<view type="2">` 中，将原始 `.mp4` 文件直接嵌入文档。这样读者可以自己观看 demo。如果用户测试了产品并有输出样例，创建 side-by-side 对比 grid：

```markdown
<grid cols="2">
  <column width="50">
    <view type="2">
      <file token="..." name="reference.mp4"/>
    </view>
    参考视频
  </column>
  <column width="50">
    <view type="2">
      <file token="..." name="generated.mp4"/>
    </view>
    生成的视频（质量评价）
  </column>
</grid>
```

### 合并相关功能

不要给每个小功能独立的 `## N. 标题` 章节。合并相关能力：
- 分类筛选可以作为内容库下的一个 bullet point，而非独立章节
- Ad Library 可以归入 Video Agent 概述
- 一个典型产品应有 5-7 个主要章节，而非 10+

### 使用洞察型章节标题

不好："视频生成与积分消耗"（中性，仅描述是什么）
好："生成时自动弹出文件夹/项目选择器"（描述值得注意的地方）

标题应传达该功能在竞争层面的意义，而非仅做标注。

### 高效读取采样帧

不要按顺序读取所有采样帧 — 这会消耗大量上下文在重复内容上（加载画面、过渡、重复状态）。策略：
1. 先批量读取 coarse 帧，每次 6-8 张，建立主时间线
2. 对重复内容（loading spinner、滚动中间帧、同一页面微小变化）只保留代表帧
3. 再读取 scenes 帧补漏，重点找弹窗、菜单、结果页、状态切换
4. 对候选功能用 dense 采样补帧，直到拿到可读且能代表功能的截图
5. 记录"为什么选这张图"，避免后续写文档时图文错配

---

## 常见问题

| 问题 | 解决方案 |
|---------|----------|
| ffmpeg 未安装 | `brew install ffmpeg` (macOS) |
| Lark 无法从 localhost 下载 | 绝不使用 `<image url="http://localhost:..."/>`。用 `docs +media-insert` 配合本地文件 |
| Shell 转义破坏 heredoc | 复杂 markdown 使用 Python 构建脚本，通过 `--markdown @file` 传参，禁止 `shell=True` |
| lark-cli 在 JSON 前输出 WARN | 找到第一个以 `{` 开头的行作为 JSON 解析起点 |
| 图片文件 < 5KB | 可能已损坏 — 在稍不同的时间戳重新提取 |
| media-insert 拒绝路径 | 必须用相对路径，cwd 设置到图片目录 |
| Callout 内换行折叠 | 已知限制 — 不要花时间修复，内容依然可读 |
| replace_range 在 callout 附近 | 避免 — 会打散内容，改为重建整个章节 |
| 文档中间插入图片 | 优先使用 `--selection-with-ellipsis` + 唯一锚点；若当前 CLI 不支持，再退回预规划逐章节追加 |
| 结构关系难以用表格表达 | 生成 SVG，再用 `@larksuite/whiteboard-cli` 转为飞书画板，而不是塞进长段落 |
| 写入已有飞书画板 | 必须先 `--overwrite --dry-run`；若提示会删除已有 nodes，先向用户确认 |

## 质量检查清单

### 所有模式通用

- [ ] 已按用户选择的输出模式执行；未把轻量视频解析擅自升级为完整竞品调研
- [ ] 只有用户明确提到竞品/调研或选择完整报告时，才执行公司/定价/评价等网络调研
- [ ] Executive summary callout 或聊天结论包含判断（核心亮点/风险），而非仅中性描述
- [ ] 末尾无单独的"优势与不足总结"章节 — 竞争分析仅放在 callout 或开头结论中
- [ ] 每张最终截图已回看验证，与其功能描述一致
- [ ] 功能已合并（5-7 个主要章节，而非 10+）
- [ ] 章节标题描述的是值得注意之处，而非仅命名功能
- [ ] 核心功能使用表格或锚点章节保证图文对应；图片未集中在末尾，未错配到其他功能
- [ ] 若使用 `【IMG_ANCHOR:...】`，最终文档中无多余锚点残留，或残留锚点有明确用途
- [ ] 分析中未引用抖音小游戏或任何特定竞品，除非用户明确要求
- [ ] 外部事实（融资、定价、流量、评价）有来源
- [ ] 若内容包含复杂结构关系，已判断是否需要飞书画板；需要时已按 SVG → whiteboard 流程执行
- [ ] 若写入飞书画板，已先完成 dry-run；涉及删除已有 nodes 时已获得用户确认
- [ ] 所有图片在飞书文档中正确渲染
- [ ] 飞书文档已检查 `permission_grant`，用户有编辑权限或已说明授权失败原因

### 完整报告（敏捷研究）额外检查

- [ ] 公司章节包含成立信息、团队背景和融资
- [ ] 多步骤流程使用 grid 布局展示多张截图，而非单帧
- [ ] 源录屏已嵌入为可播放视频（如有）
- [ ] 定价章节覆盖所有层级及真实价格
- [ ] 评价章节引用了至少 2 个来源的评价
- [ ] 正面和负面评价均有体现
