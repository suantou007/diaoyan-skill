---
name: product-competitor-research
version: 2.7.0
description: "Create Lark/Feishu documents for product competitor research from recordings, product links, and user notes. Use this skill whenever the user asks for 竞品调研, 竞品分析, 产品调研, 功能拆解, 飞书功能拆解, 完整竞品报告, 敏捷研究, product competitor research, competitor analysis, product feature breakdown, or wants a shareable Lark/Feishu report based on a product demo or recording. This skill intentionally supports only two output modes: Feishu feature breakdown and full Feishu competitor report."
---

# 竞品调研 — 飞书功能拆解与完整报告

将竞品产品录屏、产品链接和用户补充信息整理成飞书文档。当前只保留两种交付模式：

1. **飞书功能拆解**：轻量飞书文档，聚焦产品定位、核心功能、截图和初步判断。
2. **完整报告**：系统竞品调研飞书文档，包含 Executive Summary、公司/团队、功能截图、定价、用户评价和相关链接。

参考文档结构见 [references/reference_doc_structure.md](references/reference_doc_structure.md)。构建脚本模板见 [references/build_script_template.py](references/build_script_template.py)。

## 使用原则

- 只输出飞书文档，不提供纯聊天总结、Markdown 报告或画板模式。
- 先确认用户要的是“飞书功能拆解”还是“完整报告”；如果用户已经说清楚，直接进入对应流程。
- 区分信息来源：视频观察、产品官网/公开资料、用户补充、分析判断不要混在一起。
- 不把普通功能拆解自动升级成完整竞品调研；只有用户选择完整报告或明确要求竞品调研/敏捷研究时，才做外部网络调研。
- 输出要服务产品判断，不只是罗列功能。每个功能点都要说明“它解决什么问题、流程如何表现、对竞争有什么意义”。

## 前置依赖

| 依赖 | 用途 | 检查 | 安装 |
|---|---|---|---|
| ffmpeg / ffprobe | 从录屏中提取视频帧和高清截图 | `ffmpeg -version` | `brew install ffmpeg` |
| Python 3 | 生成飞书文档构建脚本、处理素材 | `python3 --version` | macOS 通常已预装 |
| lark-cli | 创建/更新飞书文档、插入图片、管理权限 | `lark-cli --version` | `npm install -g @larksuite/cli` |
| lark-doc skill | 飞书文档创建、更新、插图 | `lark-cli docs +create --help` | `npx skills add larksuite/cli -g -y` |
| lark-shared skill | 飞书认证、身份切换、权限处理 | 读取 `~/.claude/skills/lark-shared/SKILL.md` | `npx skills add larksuite/cli -g -y` |

首次配置：

```bash
lark-cli config init --new
lark-cli auth login --domain drive
```


## 本地化兼容（可选）

当用户说“本地化兼容”“采用和作者一样的 skill 进行分析”“适配本地 skill”“用我本地已有 skill”或类似表达时，启用这个可选流程。不要默认执行安装或扫描；只有用户明确选择后才处理本地环境。

### 两种模式

向用户提供两个选择：

1. **采用和作者一样的 skill 进行分析**：尽量同步作者本地配置，补齐 hv-analysis、tavily-search，并更新 Lark 能力。
2. **适配本地 skill**：不强制安装新 skill，优先读取本机已下载的 skill，做工具平替和自适应处理，并明确告诉用户本次适配结果。

### 模式一：采用和作者一样的 skill 进行分析

让分析链路尽量接近作者本地配置：

- 使用 **卡兹克的 hv-analysis 横纵分析法** 强化完整报告的纵向演化和横向竞品对比。
- 使用 **tavily-search / Tavily CLI** 做实时网络搜索，提升信息源覆盖和稳定性。
- 将 **lark-cli / lark skills** 更新到最新，减少飞书文档、插图和授权失败。

#### 执行步骤

1. **告知用户将进行本地环境同步**：这会安装或更新本机 Claude skills / CLI 工具，但不会改动项目业务代码。
2. **检查本地 skill 是否存在**：
   - `~/.claude/skills/hv-analysis/SKILL.md`
   - `~/.claude/skills/tavily-search/SKILL.md`
   - `~/.claude/skills/lark-doc/SKILL.md`
   - `~/.claude/skills/lark-shared/SKILL.md`
3. **更新 Lark 能力到最新版本**：

   ```bash
   npx skills add larksuite/cli -g -y
   ```

4. **补齐 tavily-search**：如果 `tavily-search` 或 `tvly` 不存在，按 tavily-search skill 的安装说明安装 Tavily CLI 并完成登录。
5. **补齐 hv-analysis**：如果 `hv-analysis` 不存在，先尝试通过当前环境的 skill 管理器安装；如果无法从短名解析安装源，向用户索要该 skill 的仓库或安装来源，不要猜测 URL。
6. **应用到报告**：
   - 飞书功能拆解：仍保持轻量，不强行引入完整横纵分析。
   - 完整报告：可增加“横纵分析”视角，将产品纵向发展、当下竞品横向对比和交叉洞察写入竞争判断。

### 模式二：适配本地 skill

当用户选择“适配本地 skill”时，不要安装作者同款依赖。先读取本机已存在的 skill，并建立能力映射。

#### 执行步骤

1. **扫描本地 skill**：查看 `~/.claude/skills/` 下与本任务相关的 skill 名称和说明，重点关注：
   - 搜索：`tavily-search`、`web-access`、WebSearch/WebFetch 等。
   - 飞书：`lark-doc`、`lark-markdown`、`lark-drive`、`lark-shared`。
   - 研究方法：`hv-analysis` 或其他深度研究/竞品分析类 skill。
   - 浏览器/网页交互：`agent-browser`、`webapp-testing` 等。
2. **做平替选择**：
   - 有 `tavily-search` 时优先用于网络搜索；没有则使用环境中可用的 web/search 工具。
   - 有 `lark-doc` 时优先创建飞书文档；只有 `lark-markdown` 时可先生成飞书 Markdown，再提示能力差异。
   - 有 `hv-analysis` 时，完整报告可引入横纵分析视角；没有时用普通竞品分析结构替代。
3. **告诉用户自适应结果**：开始正式分析前，用简短列表说明：
   - 本次使用了哪些本地 skill。
   - 哪些作者同款能力缺失，已用什么能力平替。
   - 哪些能力无法平替，会影响报告哪一部分。
4. **把自适应写入交付说明**：最终返回飞书链接时，再补一句“本次本地化适配情况”，方便用户知道报告是如何生成的。

#### 自适应说明模板

```text
本次已适配本地 skill：
- 搜索：使用 tavily-search / web-access / WebSearch（按实际情况填写）
- 飞书：使用 lark-doc / lark-markdown（按实际情况填写）
- 研究方法：使用 hv-analysis / 未检测到，采用内置竞品分析结构替代
- 缺失能力：...，影响：...
```

### 边界

- 本地化兼容是可选增强，不是运行本 Skill 的前置条件。
- 如果用户只是要快速飞书功能拆解，不要为了“作者同款”或“本地适配”把任务升级成重型完整研究。
- “适配本地 skill”不安装新东西，只做能力发现、平替和说明；“作者同款”才安装或更新依赖。
- 安装或登录 Tavily、Lark 可能需要用户交互；遇到交互式登录时，让用户在当前会话中用 `! <command>` 执行。

## Phase 0：前置信息收集

开始前确认四类信息。用户消息里已经给出的内容不要重复追问。

### 1. 输出模式

如果用户没有明确说明，给出两个选项：

| 模式 | 适合情况 | 是否外部调研 |
|---|---|---|
| **飞书功能拆解** | 已经知道产品背景，只需要拆功能、看 UI/流程/能力亮点 | 默认不做，除非用户额外要求 |
| **完整报告** | 第一次系统评估竞品，需要公司、定价、用户反馈和竞争判断 | 必须做 |

### 2. 输入材料

优先收集：

- 产品录屏：`.mp4` / `.mov` / `.webm`
- 产品官网、定价页、文档页、ProductHunt/G2/Reddit 等链接
- 用户已有笔记或关注点
- 想对比的产品或能力维度

如果没有录屏，说明可以继续，但功能截图和 UI 判断会受限。如果有录屏，先从视频抽帧识别真实功能流程。

### 3. 重点关注方向

主动问用户最关心什么，例如：

- Agent 架构 / 生成链路
- 定价模型 / credits 体系
- 3D 资产生成、世界生成、视频生成等具体能力
- 与某个竞品的差异
- 面向 B 端落地的可用性、稳定性、协作能力

这些关注点决定截图选择、Executive Summary 和结论权重。

### 4. 飞书授权

需要创建或编辑飞书文档时，确认 lark-cli 已登录。如果权限不足，按 lark-shared 的认证流程处理，不要绕过权限。

## 工作流概览

```text
Phase 0  前置信息收集
  ├─ 确认模式：飞书功能拆解 / 完整报告
  ├─ 收集录屏、链接、用户关注点
  └─ 检查飞书授权

Phase 1  视频分析（有录屏时）
  ├─ 粗采样建立视频地图
  ├─ 场景变化采样捕捉 UI 切换
  ├─ 候选区间密集采样
  └─ 识别核心功能和截图候选

Phase 2  高清截图提取
  ├─ 为每个功能提取 1-3 张关键截图
  ├─ 删除重复、模糊、无信息量截图
  └─ 建立功能与图片的一一对应关系

Phase 3  外部调研（仅完整报告）
  ├─ 公司与团队
  ├─ 用户与流量
  ├─ 定价与套餐
  └─ 用户评价与口碑

Phase 4  构建飞书文档
  ├─ 写入结构化内容
  ├─ 插入截图并保持图文对齐
  ├─ 授权用户访问
  └─ 返回飞书链接和说明
```

## 模式 A：飞书功能拆解

用于“我只想知道这个产品怎么做、有什么功能、UI/流程如何”的场景。不要主动做公司、融资、定价、用户评价等完整调研。

### 文档结构

1. **Executive Summary Callout**
   - 一句话产品定位
   - 3-5 条核心观察
   - 1-2 条初步机会/风险判断

2. **产品介绍**
   - 产品名称
   - 目标用户/场景
   - 从录屏或用户材料中能确认的核心价值主张

3. **核心功能拆解**
   使用表格或分节结构保持图文对齐。推荐表格列：

   | 功能 | 功能描述 | 图片/视频示意 |
   |---|---|---|

   每个功能包含：
   - 洞察型功能名，不要只写 UI 按钮名。
   - 2-4 句描述：功能做什么、流程如何表现、用户价值是什么。
   - 1-3 张对应截图或时间戳。
   - 必要时补充“产品判断”：这个能力为什么值得关注。

4. **初步判断**
   - 适合借鉴的地方
   - 暂时看不清或需要进一步验证的地方
   - 可继续深挖的问题

5. **素材与来源**
   - 录屏文件名或链接
   - 截图时间戳
   - 用户提供的补充材料

### 质量标准

- 每个主要功能至少有一段清晰解释。
- 截图必须靠近对应功能，不要集中 append 到文档末尾。
- 结论要基于可见证据，不要为了完整性强行扩展。

## 模式 B：完整报告

用于系统评估一个竞品。完整报告必须做外部调研，并在报告中标明来源或不确定性。

### 文档结构

1. **Executive Summary Callout**
   - 一句话介绍
   - 核心亮点 1-3 条
   - 对比与不足 1-2 条
   - 对我方/目标业务的启发或风险

2. **公司与团队**
   - 成立时间、总部、母公司或组织关系
   - 创始人/核心团队背景
   - 融资轮次、投资方、资金用途（如有）
   - 用户规模、流量、典型客户或应用场景（如可查）

3. **产品介绍**
   - 产品定位
   - 目标用户
   - 使用场景
   - 核心卖点

4. **核心功能拆解**
   - 基于录屏提取的功能和截图
   - 基于官网/公开资料补充的视频中未展示功能
   - 每个功能说明竞争意义，而不只是说明“它有什么”

5. **售卖方式和定价**
   - Free / Starter / Pro / Business / Enterprise 等套餐
   - credits、usage limit、seat、商用授权等关键限制
   - 定价模式背后的商业判断

6. **产品评价**
   - Reddit、ProductHunt、G2、X、YouTube、社区评论等公开反馈
   - 正向评价和负向评价分开整理
   - 将评价归纳为产品能力、稳定性、易用性、价格、场景匹配等维度

7. **竞争判断**
   - 该产品真正强在哪里
   - 它的短板或风险是什么
   - 对目标业务/我方产品有什么启发

8. **相关链接**
   - 官网
   - 定价页
   - 文档/帮助中心
   - 社区评价来源
   - 其他引用材料

### 调研要求

- 不确定的信息要标注“不确定/未找到可靠来源”。
- 定价和用户评价优先引用一手页面或高可信来源。
- 公司/融资信息不要只依赖单一搜索摘要，尽量交叉验证。
- 用户评价不要只摘好评，要体现真实问题和边界。

## 视频分析方法

有录屏时执行。目标不是截很多图，而是建立“功能 → 证据截图”的映射。

### 1. 粗采样

用 ffmpeg 每 2-5 秒抽一帧，快速建立视频地图：

```bash
ffmpeg -i input.mp4 -vf fps=1/3 frames/rough_%04d.jpg
```

### 2. 场景变化采样

补捉快速切换、弹窗、结果页等关键 UI：

```bash
ffmpeg -i input.mp4 -vf "select='gt(scene,0.25)',showinfo" -vsync vfr frames/scene_%04d.jpg
```

### 3. 候选区间密集采样

对关键时间段加密抽帧，例如每秒 2 帧：

```bash
ffmpeg -ss 00:01:20 -to 00:01:45 -i input.mp4 -vf fps=2 frames/dense_%04d.jpg
```

### 4. 高清截图提取

为最终报告中的每个功能提取高清图，避免用低清采样图直接进报告：

```bash
ffmpeg -ss 00:01:23.5 -i input.mp4 -frames:v 1 screenshots/feature_name.jpg
```

### 5. 截图筛选

保留：
- 能说明核心功能的界面
- 展示输入、生成中、结果态、编辑态的关键节点
- 与功能描述一一对应的画面

删除：
- 模糊、重复、过渡动画、加载页
- 无法说明功能差异的装饰画面
- 会泄露不该公开信息的截图

## 飞书文档构建

### 图文对齐

优先使用表格或稳定锚点结构绑定图片和文字。推荐流程：

1. 先生成完整文档骨架。
2. 在需要插图的位置写入唯一锚点，例如 `【IMG_ANCHOR:feature_01】`。
3. 使用 `lark-cli docs +media-insert` 按 selection 插入图片。
4. 插图后检查图片是否在对应功能附近。

不要把图片全部追加到文末；这会破坏报告可读性。

### 图片路径

插入图片时使用相对路径，并把工作目录设置到图片目录，避免路径解析失败。

错误示例：

```bash
lark-cli docs +media-insert DOC_TOKEN --path /absolute/path/image.jpg
```

推荐示例：

```bash
cd screenshots
lark-cli docs +media-insert DOC_TOKEN --path feature_01.jpg --selection "【IMG_ANCHOR:feature_01】"
```

### 构建脚本

当报告包含多张图片时，优先写一个临时 Python 构建脚本，按“创建文档 → 写内容 → 插图 → 授权 → 校验”的顺序执行。可参考 `references/build_script_template.py`。

## 权限与交付

完成文档后：

1. 确认文档能被用户打开。
2. 必要时用 lark-cli 授权用户 full_access。
3. 返回飞书链接。
4. 简要说明报告包含哪些部分、哪些信息来自视频、哪些来自外部调研。
5. 如果有未确认信息，明确列出。

## 质量检查清单

### 通用

- [ ] 用户选择了“飞书功能拆解”或“完整报告”。
- [ ] 飞书文档已创建并返回链接。
- [ ] 核心功能与截图一一对应。
- [ ] 图片没有集中在文档末尾。
- [ ] 报告区分视频观察、公开资料和分析判断。
- [ ] 不确定信息已标注。
- [ ] 文档权限已处理。

### 飞书功能拆解

- [ ] 没有主动加入公司、融资、定价、用户评价等完整调研章节。
- [ ] 功能名是洞察型标题，而不是简单 UI 名称。
- [ ] 每个功能都有描述、截图/时间戳和初步判断。

### 完整报告

- [ ] 公司/团队、定价、用户评价均有外部来源支撑。
- [ ] 用户评价包含正负两面。
- [ ] Executive Summary 有明确竞争判断。
- [ ] 相关链接完整列出。
