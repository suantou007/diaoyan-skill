---
name: product-competitor-research
version: 2.8.1
description: "Create Lark/Feishu documents for product competitor research from recordings, product links, and user notes. Use this skill whenever the user asks for 竞品调研, 竞品分析, 产品调研, 功能拆解, 飞书功能拆解, 完整竞品报告, 敏捷研究, product competitor research, competitor analysis, product feature breakdown, product demo review, or wants a shareable Lark/Feishu report based on a product demo or recording. This skill intentionally supports only two output modes: Feishu feature breakdown and full Feishu competitor report."
---

# 竞品调研 — 飞书功能拆解与完整报告

将竞品产品录屏、产品链接和用户补充信息整理成飞书/Lark 文档。只支持两种交付模式：

1. **飞书功能拆解**：轻量飞书文档，聚焦产品定位、核心功能、截图、流程和初步产品判断。
2. **完整报告**：系统竞品调研飞书文档，包含 Executive Summary、公司/团队、产品介绍、功能截图、定价、用户评价、Demo 视频和相关链接。

参考文档结构见 [references/reference_doc_structure.md](references/reference_doc_structure.md)。构建脚本模板见 [references/build_script_template.py](references/build_script_template.py)。

## 使用原则

- 只输出飞书/Lark 文档，不把最终交付降级成纯聊天总结、Markdown 报告或单独画板。
- 先确认用户要的是“飞书功能拆解”还是“完整报告”；如果用户已经说清楚，直接进入对应流程。
- 录屏强烈建议但不阻塞：没有录屏也继续做，只是跳过视频抽帧和截图配对。
- **图片识别必须把截图/视频帧作为图片传给具备视觉能力的模型读取，一定不能使用 OCR、截图文字抽取、Tesseract 或纯文件名/时间戳推断来替代视觉识别。**
- 不把普通功能拆解自动升级成完整竞品调研；只有用户选择完整报告或明确要求竞品调研/敏捷研究时，才做公司、融资、定价、用户评价等外部调研。
- 区分信息来源：视频观察、产品官网/公开资料、用户补充、分析判断不要混在一起。
- 输出要服务产品判断，不只是罗列功能。每个功能点都要说明它解决什么问题、流程如何表现、对竞争有什么意义。

## 前置配置

运行前只确认一次依赖，分为必需能力和可选增强；除非用户明确选择本地化兼容，不要扫描或安装可选增强。

### 必需能力

| 能力 | 用途 | 检查 | 安装 / 更新 |
|---|---|---|---|
| ffmpeg / ffprobe | 从录屏中提取视频帧、获取时长、导出高清截图 | `ffmpeg -version` / `ffprobe -version` | `brew install ffmpeg` |
| Python 3 | 生成飞书文档构建脚本、处理素材、规避 shell 转义问题 | `python3 --version` | macOS 通常已预装 |
| lark-cli + lark skills | 创建/更新飞书文档、插入图片、上传文件、处理授权 | `lark-cli --version` | `npm install -g @larksuite/cli`；`npx skills add larksuite/cli -g -y` |

首次使用飞书时：

```bash
lark-cli config init --new
lark-cli auth login --domain drive
```

遇到交互式登录时，让用户在当前会话中用 `! <command>` 执行，不要绕过授权。

### 可选增强

| 能力 | 用途 | 安装 / 更新 |
|---|---|---|
| hv-analysis | 卡兹克横纵分析法，用于完整报告的纵向演化 + 横向竞品对比 | `npx skills add https://github.com/KKKKhazix/khazix-skills -g -y --skill hv-analysis` |
| tavily-search | Tavily 官方搜索 skill，用于完整报告的实时网络搜索 | `npx skills add https://github.com/tavily-ai/skills -g -y --skill tavily-search`；已安装时可用 `npx skills update tavily-search -g -y` |

## 本地化兼容（可选）

只有用户明确选择“本地化兼容”“采用和作者一样的 skill 进行分析”“适配本地 skill”“用我本地已有 skill”或类似表达时，才启用这个流程。

- **采用和作者一样的 skill 进行分析**：直接检查并安装/更新全部可选增强能力，包括 `hv-analysis`、`tavily-search`，同时用 `npx skills add larksuite/cli -g -y` 更新 Lark 能力。
- **适配本地 skill**：先扫描 `~/.claude/skills/` 和 `~/.agents/skills/` 下的本地 skill，优先使用已有的搜索、飞书、研究方法类能力做平替；如果没有可替代能力，再安装对应可选增强。
- 告诉用户本次用了哪些本地能力、补装了哪些能力、仍缺什么能力。
- 飞书功能拆解保持轻量，不因为本地化兼容升级成完整报告；完整报告可以使用 `hv-analysis` 增加横纵分析视角，使用 `tavily-search` 增强外部信息检索。

## Phase 0：前置信息收集（开始分析前）

当用户描述一个想研究的竞品或产品时，先主动收集下面信息。用户初始消息里已经给出的内容不要重复追问。

### 0a. 产品录屏（强烈建议，但不阻塞）

如果用户还没有提供录屏，建议他们提供：如果有 `.mp4` / `.mov` / `.webm` 录屏，可以直接从真实 UI 中抽取截图、识别功能流程，并写出更准确的报告。录屏能把报告从“泛泛的网页调研”变成“基于真实界面和流程的产品判断”。

录屏不是阻塞项。用户没有录屏时继续推进：

- 跳过 Phase 1 和 Phase 2。
- 完整报告从官网、文档、公开资料和用户补充中构建功能描述，但不会强行配截图。
- 飞书功能拆解可以使用产品官网/文档补足功能理解，但不展开公司、融资、定价、用户评价等完整调研章节，除非用户明确要求。

无论是否有录屏，都鼓励用户提供产品 URL、已有笔记、他们自己的印象和关注点，让报告服务真实决策，而不是生成通用抓取总结。

### 0b. 输出模式

如果用户没有明确说明，给出两个选项并让用户选择：

| 模式 | 适合情况 | 外部调研 |
|---|---|---|
| **飞书功能拆解** | 已经知道产品背景，只想拆功能、看 UI/流程/能力亮点 | 默认不做公司、融资、定价、评价；只有用户额外要求才补充 |
| **完整报告** | 第一次系统评估竞品，需要给团队或利益相关方看完整判断 | 必须做公司/团队、流量、定价、用户评价等外部调研 |

### 0c. 重点关注方向

主动问用户最关心什么，例如：

- Agent 架构 / 生成链路
- 定价模型 / credits 体系
- 3D 资产生成、世界生成、视频生成等具体能力
- 与某个竞品或我方产品的差异
- 面向 B 端落地的可用性、稳定性、协作能力

这些关注点会影响 Executive Summary、截图选择、功能深度和竞争判断。如果没有用户输入，报告容易变成泛泛罗列。

### 0d. 飞书授权

需要创建或编辑飞书文档时，确认 `lark-cli` 已配置并登录。如果权限不足，按 `lark-shared` 的认证流程处理，不要绕过权限。

## 工作流概览

```text
Phase 0  前置信息收集
  ├─ 录屏（强烈建议，但不阻塞）
  ├─ 输出模式：飞书功能拆解 / 完整报告
  ├─ 用户关注点与对比对象
  └─ 飞书授权

Phase 1  视频分析（仅有录屏时）
  ├─ ffprobe 获取时长
  ├─ 低频抽帧建立视频地图
  ├─ 必要时做场景变化采样和候选区间密集采样
  └─ 识别功能、时间戳、UI 证据和竞争意义

Phase 2  高清截图提取（仅有录屏时）
  ├─ 为每个功能提取 1-3 张高清图
  ├─ 读回每张截图，确认画面和功能描述匹配
  ├─ 多步骤流程用 grid，而不是只放单帧
  └─ 删除重复、模糊、过渡态、无信息量截图

Phase 3  外部调研（仅完整报告）
  ├─ 公司与团队
  ├─ 用户与流量
  ├─ 定价与套餐
  └─ 用户评价与口碑

Phase 4  构建飞书文档
  ├─ 先规划完整结构和图片锚点
  ├─ 写入结构化内容
  ├─ 插入截图、视频和必要的飞书画板
  └─ 校验图文对齐

Phase 5  授权与交付
  ├─ 授权用户 full_access
  ├─ 确认文档可打开
  └─ 返回飞书链接和未确认信息
```

---

## 模式 A：飞书功能拆解

用于“我只想知道这个产品怎么做、有什么功能、UI/流程如何”的场景。不要主动加入公司、融资、定价、用户评价等完整调研章节。

### 1. Executive Summary Callout

文档顶部使用 `<callout emoji="💡" background-color="light-orange">`，集中承载产品定位和初步判断：

- **一句话介绍**：一句话说明产品定位和目标场景。
- **核心亮点**：1-3 条值得关注的能力，按竞争意义而不是 UI 顺序组织。
- **对比不足**：如果用户指定了对比对象，可以写 1-2 条差异或不足；关键差距用 `<text color="red">` 高亮。

不要在文末再单独设置“优势与不足总结”章节。读者应该在 10 秒内看到这个产品是否值得继续关注。

### 2. 产品介绍

- 产品名称
- 目标用户/场景
- 从录屏、官网或用户材料中能确认的核心价值主张
- 信息来源说明：视频观察 / 官网资料 / 用户补充 / 分析判断

### 3. 核心功能拆解

主功能控制在 **5-7 个**，通常不要超过 10 个。合并相关能力，不要给每个小按钮单独开章节。

当每个功能只有 1-2 张截图时，优先使用表格保持图文对齐：

| 功能 | 功能描述 | 图片/视频示意 |
|---|---|---|

每个功能包含：

- 洞察型功能名，不要只写 UI 按钮名。
- 2-4 句描述：功能做什么、流程如何表现、用户价值是什么。
- 1-3 张对应截图或时间戳。
- 必要时补充“产品判断”：这个能力为什么值得关注。

如果某个功能是多步骤流程，不要把多张图硬塞进狭窄表格单元格；改用独立小节，并配合 `<grid cols="2">` 或 `<grid cols="3">`。

### 4. 初步判断

- 适合借鉴的地方
- 暂时看不清或需要进一步验证的地方
- 可继续深挖的问题

### 5. 素材与来源

- 录屏文件名或链接
- 截图时间戳
- 用户提供的补充材料
- 官网/文档链接（如用于补足功能描述）

### 飞书功能拆解质量要求

- 没有公司/团队、融资、定价、用户评价等完整报告章节，除非用户明确要求。
- 每个主要功能都有清晰解释、证据截图或时间戳。
- 截图靠近对应功能，不集中 append 到文档末尾。
- 结论基于可见证据；不为了完整性强行扩展。

---

## 模式 B：完整报告

用于系统评估一个竞品。完整报告必须做外部调研，并在报告中标明来源或不确定性。

### 1. Executive Summary Callout

文档顶部使用 `<callout emoji="💡" background-color="light-orange">`。这个 callout 同时承载产品定位、核心亮点和竞争判断，替代单独的“优势与不足总结”章节。

结构：

- **一句话介绍**：说明产品是谁做的、解决什么问题、主打什么变化。
- **核心亮点**：1-3 条竞争优势，必须有观点，不要中立罗列。
- **对比[我方产品/目标业务]的差异和不足**：1-2 条关键短板或风险，关键差距用 `<text color="red">` 高亮。
- **对我方/目标业务的启发或风险**：说明它对当前业务决策意味着什么。

### 2. 公司与团队

这部分来自公开资料和外部调研，不从视频里推断。

- **基本信息**：成立年份、总部、母公司或所属组织、融资轮次、金额、投资方、资金用途。
- **创始人及核心成员**：CEO/CTO 背景、曾任公司和职位、相关领域经验。
- **用户和客户**：SimilarWeb 流量数据、估算用户数、与竞品流量对比、典型客户画像、客户 logo。

公司/融资信息不要只依赖单一搜索摘要，尽量交叉验证；不确定时明确标注“未找到可靠来源”或“不确定”。

### 3. 产品介绍

#### 核心功能

这部分优先来自录屏分析。使用 **lark-table** 或稳定锚点结构保持图文对齐，推荐列：

| 功能 | 功能描述 | 图片/视频示意 |
|---|---|---|

每一行对应一个功能。突出能力可用 `<text bgcolor="light-yellow">**Feature Name**</text>` 高亮。图片列插入从录屏中提取的截图。

视频里没有清楚展示、但官网或文档可确认的能力，可以补充，但必须标明来源。每个功能都要说明竞争意义，而不只是说明“它有什么”。

#### 产品定位和优势

用 2-3 段说明市场定位、目标用户、使用场景和核心卖点。通常整理 3 条竞争优势。

#### 售卖方式和定价

来自产品定价页或公开资料。优先用 **lark-table** 展示套餐：

| | Free | Starter | Business | Enterprise |
|---|---|---|---|---|
| 价格 | ... | ... | ... | ... |
| credits / usage limit | ... | ... | ... | ... |
| 关键功能限制 | ... | ... | ... | ... |
| 水印 / 商用授权 | ... | ... | ... | ... |

如适用，同时说明 SaaS、API、seat、credits、商用授权等定价模式，并解释定价背后的商业判断。

#### 产品评价

从 Reddit、ProductHunt、G2、X、YouTube、社区评论等公开反馈中收集。必须同时包含正向和负向反馈。

- 总体情绪或评分
- 2-3 条正向评价，使用 `<quote-container>`
- 1-2 条负向评价，展示真实痛点
- 尽可能附评价截图
- 归纳为产品能力、稳定性、易用性、价格、场景匹配等维度

引用要短，优先一两句话；不要只摘好评。

### 4. Demo 视频（有录屏时）

不要只提取静态截图。把原始 `.mp4` / `.mov` / `.webm` 上传并以可播放文件嵌入文档，让读者可以自己看 demo。

如果用户也有实测输出视频，例如参考视频和生成结果，使用左右对比：

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

### 5. 结构化画板（可选）

当报告需要表达逻辑关系，例如产品能力地图、生成链路、Agent 工作流、用户路径、模块依赖、竞品定位、漏斗或时间线，优先使用飞书画板/图表，而不是只插入一张静态图片。具体流程见 Phase 4 的“飞书图标逻辑关系图”。

### 6. 相关链接

- 官网
- 定价页
- 文档/帮助中心
- ProductHunt / G2 / Reddit / X / YouTube / 社区评价来源
- 其他引用材料
- 相关竞品分析文档，可用 `<mention-doc>` 链接

完整报告不要单独设置“优势与不足总结”章节；所有竞争判断都放在执行摘要 callout 里。

---

## Phase 1：视频分析 — Survey Frames 与功能识别

> **需要录屏。** 如果没有录屏，完全跳过 Phase 1 和 Phase 2。改用官网、公开资料和用户补充构建功能章节；如果是飞书功能拆解，则只补足功能理解，不展开完整报告的外部调研章节。

### 1. 获取视频时长

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 "<video_path>"
```

### 2. 低频抽帧建立视频地图

先用低频抽帧建立整体视频地图，不要一上来截大量高清图：

```bash
mkdir -p /tmp/competitor_frames
ffmpeg -i "<video_path>" -vf "fps=1/10,scale=1280:-1" -q:v 3 /tmp/competitor_frames/frame_%04d.jpg
```

`fps=1/10` 表示每 10 秒 1 帧。15 分钟视频大约得到 90 帧。

**识别 survey frames 时必须直接把图片文件传给视觉模型阅读画面；一定不能使用 OCR 或把图片转成文字后再猜测 UI/功能。**

读帧时识别不同功能，并为每个功能记录：

1. **功能名**：简洁、描述性强。
2. **大致时间戳**：帧号 × 10 秒。
3. **画面内容**：UI 元素、Agent 行为、状态变化、差异化能力。
4. **为什么重要**：竞争意义和产品判断。

一个 15 分钟 demo 通常会产生 10-20 个候选功能，最终报告要合并成 5-7 个主要功能。

### 3. 必要时补充场景变化采样

低频采样容易错过快速切换、弹窗、结果页或短暂状态。遇到这些情况时补充场景变化采样：

```bash
ffmpeg -i "<video_path>" -vf "select='gt(scene,0.25)',showinfo" -vsync vfr /tmp/competitor_frames/scene_%04d.jpg
```

### 4. 候选区间密集采样

对关键时间段加密抽帧，例如每秒 2 帧，捕捉输入、生成中、结果态、编辑态等关键节点：

```bash
ffmpeg -ss 00:01:20 -to 00:01:45 -i "<video_path>" -vf fps=2 /tmp/competitor_frames/dense_%04d.jpg
```

### 5. 高效读取 survey frames

不要顺序读完所有 survey frames，这会浪费上下文在加载页、过渡动画、重复状态上。推荐策略：

1. 每批读取 6-8 张。
2. 如果发现连续重复内容，例如 loading spinner，直接跳过到下一个明显不同的区间。
3. 对 3 分钟、18 张 survey frames 的视频，通常只需要读 12-14 张有差异的图。
4. 一旦识别出候选功能，再回到对应时间段做高清提取。

---

## Phase 2：高清截图提取

为每个最终功能提取 1-3 张高清图，避免把低清 survey frame 直接放进报告。

```bash
mkdir -p /tmp/competitor_analysis
ffmpeg -ss <TIMESTAMP> -i "<video_path>" -frames:v 1 -q:v 1 /tmp/competitor_analysis/<NN>_<feature_name>.jpg
```

`-q:v 1` 表示近无损 JPEG。检查文件大小，低于 5KB 的图片很可能损坏，需要换时间戳重新提取。

### 关键要求：必须把图片传给模型读回

**始终把每张提取出来的高清截图作为图片传给具备视觉能力的模型 read back**，确认它真的展示了对应功能的正确 UI 状态。**一定不能使用 OCR、截图文字抽取或 Tesseract 替代图片识别。** 10 秒间隔的 survey frames 只是近似定位，用户可能在两个采样点之间已经滚动或切换页面。

常见失败模式：

- 截到过渡动画、滚动中画面，而不是稳定 UI。
- 功能是多屏流程，但单帧只截到其中一步。
- 时间戳偏差几秒，截到了前一个或后一个功能。
- 截图模糊、重复、信息量低，无法证明功能差异。
- 截图包含不应公开的信息。

多步骤流程不要只放单帧。可提取多张图并使用 `<grid cols="2">` 或 `<grid cols="3">` 展示输入、处理中、结果态、编辑态。

---

## Phase 3：外部调研（仅完整报告）

> **仅完整报告执行。** 飞书功能拆解默认跳过本阶段，不加入公司、融资、定价、用户评价等章节。没有录屏但仍选择飞书功能拆解时，可以查官网/文档补足功能描述，但不要扩展成完整竞品研究。

使用 WebSearch、tavily-search 或可替代的本地搜索 skill 收集视频里看不到的信息。能并行时，用子 agent 并行检索。

### 3a. 公司与团队

搜索：`"<company name>" founded team funding crunchbase`

寻找：成立时间、总部、创始人背景、核心团队、融资轮次、投资方、资金用途。

### 3b. 用户与流量

搜索：`"<company name>" site:similarweb.com` 或 `"<product URL>" monthly visits users`

寻找：月访问量、估算用户数、增长趋势、与竞品的流量对比。

### 3c. 定价

搜索：`"<company name>" pricing plans`，或直接访问定价页。

寻找：套餐名、价格、credits、功能限制、seat、商用授权、水印、API 价格。

### 3d. Reddit 用户评价

搜索：`site:reddit.com "<product name>" review`

寻找：真实用户体验、抱怨、称赞、和替代品对比。

### 3e. ProductHunt 用户评价

搜索：`site:producthunt.com "<product name>"`

寻找：发布反馈、评分、创始人回复、功能请求。

### 3f. G2 用户评价

搜索：`site:g2.com "<product name>" reviews`

寻找：星级评分、pros/cons 模式、企业用户和 SMB 用户的差异。

### 3g. 其他公开来源

必要时补充 X、YouTube、Discord/社区论坛、帮助中心、更新日志。引用前判断来源可信度，避免把广告文案当成事实。

用户评价引用要短，使用 `<quote-container>`，同时呈现正负两面。不确定信息必须标注“不确定/未找到可靠来源”。

---

## Phase 4：构建飞书文档

### 先规划完整结构

构建前先决定完整章节、子章节、图片数量和锚点。中途用删除重建或 `replace_range` 做外科手术很脆弱，容易丢失图片 token、打散 callout 或造成图文错位。

推荐先生成完整文档骨架，在需要插图的位置写入唯一锚点，例如 `【IMG_ANCHOR:feature_01】`，再按锚点插入图片并回看位置。

### 图文对齐

报告必须让图片和文字交错出现，而不是把图片全部 append 到文末。常用模式：

1. 写入 Executive Summary callout 和第一段内容。
2. 对每个需要图片的功能：
   - 插入图片或在锚点处替换。
   - 追加该功能描述和下一个功能标题。
3. 对纯文本章节，例如公司、定价、评价，直接追加 Markdown。

如果当前 `docs +media-insert` 能按 selection 插入，优先使用锚点：

```bash
cd /path/to/images
lark-cli docs +media-insert "<DOC_ID>" --path feature_01.jpg --selection "【IMG_ANCHOR:feature_01】"
```

如果只能 append 到末尾，就按“标题 → 插图 → 文本 → 下一标题”的迭代模式构建，避免最后统一插图。

### 关键要求：图片路径必须是相对路径

`lark-cli docs +media-insert` 要求相对路径。绝对路径会触发 `unsafe file path`。

```bash
# 错误
lark-cli docs +media-insert --doc "<DOC_ID>" --file "/Users/me/images/shot.jpg"

# 正确：切到图片目录，用相对路径
cd /path/to/images && lark-cli docs +media-insert --doc "<DOC_ID>" --file ./shot.jpg --align center --caption "Description"
```

Python 脚本中用 `subprocess.run(cmd, cwd=IMG_DIR)`。

### 构建脚本

当报告包含多张图片，尤其是 10 张以上时，优先写临时 Python 构建脚本，按“创建文档 → 写内容 → 插图/视频 → 授权 → 校验”的顺序执行。可参考 [references/build_script_template.py](references/build_script_template.py)。

关键模式：先把 Markdown 写到 `/tmp/_lark_md.txt`，再在 `lark-cli` 命令中用 `$(cat /tmp/_lark_md.txt)` 引用，避免反引号、引号、特殊字符和多行 Markdown 造成 shell 转义问题。

### Lark/飞书 Markdown 常用格式

```markdown
# Callout blocks
<callout emoji="💡" background-color="light-orange">
**Content here**
</callout>

# Tables
<lark-table rows="3" cols="4" column-widths="125,210,210,210">
  <lark-tr>
    <lark-td>**Header**</lark-td>
    ...
  </lark-tr>
</lark-table>

# Image grids
<grid cols="3">
  <column width="33">
    <image token="..." width="366" height="642" align="center"/>
  </column>
</grid>

# User review quotes
<quote-container>
*"User quote here"*
— Source, date
</quote-container>

# Text highlighting
<text bgcolor="light-yellow">**Highlighted feature**</text>
<text color="red">critical gap</text>

# Embedded videos
<view type="2">
  <file token="..." name="demo.mp4"/>
</view>

# Related docs
<mention-doc token="..."/>
```

### 飞书图标逻辑关系图

当报告需要表达逻辑关系时，例如产品能力地图、生成链路、Agent 工作流、用户路径、模块依赖、竞品定位、漏斗或时间线，优先使用飞书画板/图表，而不是只插入一张静态图片。推荐流程是：**先生成 SVG，再用 Lark 工具转换成可编辑的飞书画板内容**。

1. **判断是否需要结构图**：只有当关系、层级、流向或依赖比单张证据截图更重要时才画图；普通 UI 截图仍放在表格或图片网格里。
2. **先生成 `diagram.svg`**：用简洁节点、箭头、分组框、泳道或矩阵表达逻辑关系；节点文字短，说明性文字放在文档正文。
3. **转换为飞书画板 OpenAPI JSON**：优先按本地 `lark-whiteboard` / `lark-whiteboard-svg` skill 执行；核心命令形态是：

   ```bash
   npx -y @larksuite/whiteboard-cli@^0.2.11 -i diagram.svg --to openapi --format json \
     | lark-cli whiteboard +update \
       --whiteboard-token "<WHITEBOARD_TOKEN>" \
       --source - --input_format raw \
       --idempotent-token "<10+字符唯一串>" \
       --overwrite --dry-run --as user
   ```

4. **先 dry-run，再正式写入**：如果 dry-run 提示会删除已有节点，必须先向用户确认；确认后去掉 `--dry-run` 正式写入。
5. **回看画板**：写入后导出或查询预览，检查文字是否溢出、节点是否重叠、箭头方向是否清楚。
6. **插入文档说明**：在飞书文档中保留画板 block 或链接，并用一两句话解释图的结论；不要只把 SVG 当普通图片插入来替代可编辑画板。

### 速率限制

迭代构建会产生很多 `lark-cli` API 调用。两次调用之间加 0.3-0.5 秒延迟，降低限流和写入失败概率。

---

## Phase 5：授权与交付

创建文档后必须处理权限。如果文档用 bot 身份创建，用户默认不能编辑；即使用 user 身份创建，也要验证用户能访问。

```bash
# Step 1: 获取用户 open_id
lark-cli contact +get-user

# Step 2: 授权用户 full_access（通常用 bot 执行）
lark-cli drive permission.members create \
  --params '{"file_token":"<DOC_ID>","file_type":"docx"}' \
  --body '{"member_type":"openchat","member_id":"<user_open_id>","perm":"full_access"}' \
  --as bot
```

如果授权失败，例如 1063003 / 1063001，通常是 app 缺少 `drive:drive` scope。明确告诉用户：文档已经创建成功，但可能需要用户申请访问，或让 bot/管理员手动分享，不要假装权限已经处理好。

交付时返回：

1. 飞书文档链接。
2. 报告包含哪些部分。
3. 哪些信息来自视频、哪些来自公开资料、哪些是分析判断。
4. 未确认或可靠性不足的信息。
5. 如有必要，提醒用户检查权限和图片/视频渲染。

---

## Lessons Learned（来自 makeUGC / SymphonyAI 等生产研究）

### 构建前先规划完整结构

先确定完整章节、子章节和图片位置，再开始写文档。中途删除重建非常脆弱：可能丢失图片 token、错放章节、破坏 callout 结构。如果已经知道 Video Agent 会有 6 个子章节，就在初始构建脚本中一次规划进去。

### 不要在 callout 边界附近做外科手术

`replace_range` 和 `delete_range` 作用在 `<callout>` 内部或邻近位置时，可能不可预测地重排文档结构。如果标题被包在 callout 里，只替换标题可能会打散 callout。优先重建整个 callout 和相邻 section，而不是单独 patch 几行。

Callout 内部换行折叠是已知 lark-cli 限制。内容仍可读时接受这个限制，不要反复消耗时间修换行。

### 嵌入原始录屏

不要只截静态图片。把原始 `.mp4` 文件以 `<file token="..." name="..."/>` 嵌入 `<view type="2">`，让读者可以自己观看 demo。如果有用户实测输出，做参考输入和生成结果的 side-by-side 对比。

### 合并相关功能

不要给每个小功能单独开 `## N. Title`。合并相关能力：

- 分类筛选可以作为 Content Library 的 bullet，而不是独立章节。
- Ad Library 可以放在 Video Agent overview 下。
- 典型产品主功能控制在 5-7 个，不要超过 10 个。

### 写洞察型标题

差：`视频生成与积分消耗`（中性描述是什么）

好：`生成时自动弹出文件夹/项目选择器`（说明这个功能有什么值得注意的差异）

标题应该传达为什么这个功能有竞争意义，而不仅是功能标签。

### 高效读取 survey frames

不要顺序读取所有帧。先批量看 6-8 张，遇到重复 loading/过渡/滚动就跳过，只在候选功能附近回头密集采样和高清截图。

### 信息来源不要混淆

视频只能证明“画面里出现了什么”；官网只能证明“产品宣称了什么”；用户评价只能证明“部分用户如何反馈”；分析判断要标明是判断。不要把这些混成一个确定事实。

---

## Gotchas

| 问题 | 解决方式 |
|---|---|
| ffmpeg 未安装 | `brew install ffmpeg` |
| 没有录屏 | 不阻塞；跳过 Phase 1-2，用公开资料和用户补充继续，但不要伪造截图 |
| 飞书功能拆解被升级成完整调研 | 不要升级；只有用户选择完整报告或明确要求竞品调研/敏捷研究才做外部调研 |
| Lark 不能下载 localhost 图片 | 不要用 `<image url="http://localhost:..."/>`；用 `docs +media-insert` 上传本地文件 |
| Shell heredoc / 特殊字符破坏命令 | 用 Python 构建脚本，把 Markdown 写到临时文件 |
| lark-cli WARN 行出现在 JSON 前 | 解析输出时找到第一行以 `{` 开头的 JSON |
| 图片小于 5KB | 大概率损坏；换一个时间戳重新提取 |
| media-insert 拒绝路径 | 必须使用相对路径，并把 cwd 设为图片目录 |
| 图片集中到文末 | 先规划锚点；或按“标题 → 插图 → 文本”的迭代模式构建 |
| 多步骤流程只截单张图 | 提取多张图，用 `<grid>` 展示流程 |
| Callout 换行折叠 | 已知限制；内容可读即可，不要反复修 |
| callout 附近 replace_range | 避免；重建整个 callout 或 section |
| 中途重建丢图片 token | 构建前规划结构和锚点，不做脆弱的中途插入 |
| whiteboard overwrite 可能删节点 | 先 dry-run；如果提示会删除已有节点，必须确认后再执行 |

## 质量检查清单

### 通用

- [ ] 用户选择了“飞书功能拆解”或“完整报告”。
- [ ] 飞书文档已创建并返回链接。
- [ ] Executive Summary callout 有竞争判断，不只是中性描述。
- [ ] 没有单独的“优势与不足总结”章节；竞争判断集中在 callout。
- [ ] 录屏存在时，每张截图都已作为图片传给视觉模型读回并确认匹配功能描述；没有使用 OCR 替代图片识别。
- [ ] 核心功能与截图一一对应，图片没有集中在文档末尾。
- [ ] 主功能合并为 5-7 个，通常不超过 10 个。
- [ ] 标题是洞察型标题，而不是简单功能标签。
- [ ] 区分视频观察、公开资料、用户补充和分析判断。
- [ ] 不确定信息已标注。
- [ ] 所有图片、视频、表格、画板在飞书中渲染正常。
- [ ] 用户有 edit / full_access 权限，或明确说明权限处理失败原因。

### 飞书功能拆解

- [ ] 没有主动加入公司、融资、定价、用户评价等完整调研章节。
- [ ] 每个功能都有描述、截图/时间戳和产品判断。
- [ ] 没有录屏时，不伪造截图；可用官网/文档补足功能描述并标注来源。
- [ ] 初步判断聚焦可借鉴点、看不清的问题和后续验证方向。

### 完整报告

- [ ] 公司/团队、定价、用户评价均有外部来源支撑。
- [ ] 公司/融资信息尽量交叉验证，不确定处明确标注。
- [ ] Pricing table 覆盖主要套餐、credits、功能限制和商用/API 信息。
- [ ] 用户评价至少来自 2 类来源，并包含正负两面。
- [ ] 多步骤流程使用 grid 布局，而不是单帧截图。
- [ ] 有录屏时，原始 demo 被作为可播放视频嵌入。
- [ ] Executive Summary 有明确竞争判断和对我方/目标业务的启发。
- [ ] 相关链接完整列出。

### 结构化画板

- [ ] 只有在关系、层级、流向或依赖需要表达时才画图。
- [ ] 先生成 SVG，再转换为飞书画板 OpenAPI JSON。
- [ ] 覆盖已有画板前先 dry-run。
- [ ] 飞书文档中保留画板或链接，并用正文解释图的结论。
