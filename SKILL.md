---
name: product-competitor-research
version: 3.3.0
description: "基于产品演示录屏与定向网页校验做竞品调研，默认使用 Tavily 做网页核验、使用飞书文档做正式交付；若 Tavily 或飞书未配置，先询问用户是否安装/配置，而不是静默降级。适用于 competitor analysis、product video research、敏捷研究、竞品调研、竞品分析、feature evidence extraction，或用户提供 .mp4/.mov/.webm 录屏并希望获得结构化结论的场景。"
---

# 基于录屏的产品竞品调研

> 对外仓库名可为 `diaoyan-skill`；skill 内部名保留 `product-competitor-research`，以兼容既有触发语义。

这个 skill 用来把产品演示录屏整理成**证据型竞品研究**。默认先完成本地 evidence package，再**用 Tavily 做网页核验、发布飞书文档**。如果 Tavily 或飞书未配置，不要静默降级；先询问用户是否现在安装/配置。

## 何时使用

- 用户给出 `.mp4` / `.mov` / `.webm` 录屏，希望看懂产品做了什么
- 用户要竞品分析、敏捷研究、正式调研报告
- 用户需要带时间戳、截图、网页核验和开放问题的结论

## 默认工作流

1. intake：补齐视频路径、产品名、官网和重点问题
2. 浏览视频并提取稳定截图
3. 用 Tavily 核验官网 / 文档 / 定价 / 更新日志
4. 产出本地 evidence package
5. 默认发布飞书；不可用时交付 `notes.html`

## 开始前只检查必要工具

- `ffmpeg` / `ffprobe`
- `python3` + Pillow（供 `scripts/prepare_llm_images.py` 使用）
- **Tavily CLI（`tvly`）**：默认网页核验必须使用；如果没装 / 未登录 / 不可用，先问用户要不要现在安装或配置
- **飞书 CLI（`lark-cli`、`lark-doc`）**：默认正式交付必须使用；如果没装 / 未登录 / token 失效，先问用户要不要现在配置或刷新

## 四条硬规则

1. **证据分层**：始终分开写
   - 视频观察
   - 网页确认
   - 推断 / 开放问题

2. **正式报告必须读结构文件**：只要交付飞书或 `notes.html`，就必须覆盖 [references/reference_doc_structure.md](references/reference_doc_structure.md)。缺失项也要写成“未找到 / 未核验 / 视频未展示”，不能静默省略。

3. **正式竞品分析必须运行时检索用户 skill 库**：优先寻找 `hv-analysis`、`tavily-search`、图示 / 飞书类 skill，用最小集合辅助纵向演进、横向对比和交汇洞察；并在 `analysis_manifest.json` 记录 `skills_consulted`。

4. **需要流程 / 时间线 / 竞品关系时必须补图**：发布飞书时先读 [references/diagram_workflow.md](references/diagram_workflow.md)。默认优先 `SVG → 飞书画板`；HTML 兜底插入 SVG / PNG。

5. **默认一定是 Tavily + 飞书**：不要把内置 WebSearch / `web.run` 或本地 HTML 当默认路径。`tvly` 不可用时，先问用户“要不要现在安装/配置 Tavily？”；飞书不可用时，先问用户“要不要现在配置/刷新飞书 CLI？”。只有用户明确同意降级，才能不用 Tavily 或不发飞书。

## 只保留 3 份参考文件

1. [references/workflow.md](references/workflow.md) —— 执行手册：视频分析、网页核验、本地输出、飞书发布、QA
2. [references/reference_doc_structure.md](references/reference_doc_structure.md) —— 正式报告必须覆盖的信息
3. [references/diagram_workflow.md](references/diagram_workflow.md) —— 什么时候补图、图放哪里、怎么走飞书画板
4. [references/checklist.md](references/checklist.md) —— 最终 QA 与发布前检查

额外只用：
- `scripts/prepare_llm_images.py`：安全图压缩，避免 413
- `assets/notes_template.html`：`notes.html` 模板

## 执行顺序

### 1. Intake

确认：
- 录屏路径
- 产品名 / 官网（已知则直接用）
- 用户最关心的问题
- 当前环境的 `tvly` 是否可用；如果不行，先问用户要不要安装/配置 Tavily
- 当前环境是否能正常发布飞书；如果不行，先问用户要不要配置/刷新飞书 CLI

### 2. 视频证据

按 `references/workflow.md` 的视频流程做：
- 先全片 survey，再下判断
- 先生成 `llm_images/`，再给模型 / 子 agent 看图
- 不发原图、不贴 base64、不用 `detail: "original"`

### 3. 网页核验

至少核验：
- 官方首页
- 官方 docs / help
- pricing / plans
- changelog / release notes / blog（视频明显展示新功能时）

默认必须使用 **Tavily CLI（`tvly`）** 做这些查询。不要把内置 WebSearch / `web.run` 当默认方案。只有当：

- 用户明确允许降级；或
- Tavily 只能找到 URL，但需要登录态 / 强动态页面补抓

才可以额外补 `web-access`；这时 Tavily 仍应作为默认搜索入口。

### 4. 本地交付资产

默认保留：
- `frames_10s/`
- `contact_sheets/`
- `selected_screenshots/`
- `llm_images/`
- `notes.html`
- `analysis_manifest.json`

### 5. 正式交付

- 默认必须发布飞书
- 飞书发布前先看结构，再看图示，再写正文
- 如果飞书 CLI / 认证不可用，先问用户要不要现在配置或刷新；只有用户明确同意降级，才退回 `notes.html`

## 报告至少要覆盖

除非用户明确只要快速草稿，否则至少覆盖：

1. 顶部观点型执行摘要
2. 公司与团队 / 用户客户 / 流量信号
3. 产品介绍：核心功能、定位优势、定价套餐、产品评价
4. Demo 视频：原始录屏路径、关键片段、输入输出、多步骤截图
5. 横纵分析：纵向演进、横向对比、交汇洞察
6. 关键图示：工作流 / 时间线 / 竞品关系 / 能力地图
7. 相关链接、素材路径、未确认问题

## 质量门槛

结束前确认：

- 截图支撑了对应结论，且带时间戳
- 官方事实优先来自官方来源
- 推断已显式标记
- `reference_doc_structure.md` 的模块都覆盖了
- `skills_consulted` 已记录实际使用 / 跳过 / unavailable
- 网页核验默认实际使用了 Tavily；如果没有，已记录用户明确批准的降级原因
- 图示按 `diagram_workflow.md` 放进对应章节，而不是堆到末尾
- 飞书文档已实际创建并返回链接；如果没有，已记录用户明确批准的降级原因
- 最终 QA 对照 `references/checklist.md`
- 最终回复写明本地输出路径
