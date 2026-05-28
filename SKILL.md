---
name: product-competitor-research
version: 3.2.0
description: "基于产品演示录屏与定向网页校验做竞品调研，产出带时间戳、截图、已确认事实、开放问题的证据型研究结果，并优先交付为飞书文档或本地 HTML。适用于 competitor analysis、product video research、敏捷研究、竞品调研、竞品分析、feature evidence extraction，或用户提供 .mp4/.mov/.webm 录屏并希望获得结构化结论的场景。"
---

# 基于录屏的产品竞品调研

> 对外仓库名为 `diaoyan-skill`；skill 内部名保留为 `product-competitor-research`，以兼容既有触发语义。

这个 skill 用来把产品演示录屏转成**证据驱动**的竞品研究结果。

更好的默认交付物是：**飞书文档**或**本地 HTML 报告**。无论最终交付哪一种，都要保留本地证据资产。

统一采用一条工作流：

1. 先看录屏
2. 再核验网页信息
3. 保留本地证据
4. 默认优先输出飞书文档；如果飞书不可用，再输出 `notes.html`

## 开始前

只检查当前任务真正需要的工具：

- **ffmpeg / ffprobe**：做视频抽帧时必需
- **Python Pillow / PIL**：生成 `llm_images/` 安全图时必需；缺失时先安装 `pillow`
- **Tavily**（`tvly`）或 `tavily-search` skill：做网页校验时必需
- **lark-cli**、**lark-shared**、**lark-doc**：推荐默认输出飞书文档时使用

如果飞书可用，默认优先走飞书，并对创建 / 更新操作使用 `--as user`。如果飞书不可用，再退回本地 HTML，不要因此阻塞分析。

## 前置 intake

在开始分析前，补齐缺失输入：

- 录屏文件或视频路径
- 产品名称、官网 URL（如果已知）
- 用户最关心的问题 / 竞品视角
- 当前环境是否能正常输出飞书；如果不能，则自动退回本地 HTML

intake 聚焦在产品、问题和交付条件上，不要让用户去手动选择“飞书还是本地”这种本该由流程自动处理的事情。

## 证据规则

在笔记和结论里，始终把以下三类信息分开：

- **视频中直接观察到的内容**
- **网页中确认过的内容**
- **推断 / 假设**

硬规则：

- 任何能力，如果既没有在视频里直接展示，也没有在官方来源中确认，就必须标成“推断”，或者干脆不写。
- 凡是由截图支撑的结论，都要带时间戳或时间范围。
- 遇到不确定的地方，优先写“未知 / 未展示 / 未核验”，不要写得过满。
- 产品名、功能名、定价、套餐、集成能力、changelog 这类事实，优先用官方来源确认。

## 工作流概览

1. 全局浏览视频
2. 提取稳定截图
3. 核验关键网页信息
4. 本地生成报告资产
5. 默认优先发布到飞书（`--as user`）；若不可用则输出 `notes.html`

## 竞品分析方法：运行时检索并联动用户 skill 库

如果任务是**真正的竞品分析 / 敏捷研究 / 深度研究**，不要只停留在“功能列表 + 截图说明”。开始正式分析前，必须有意识地检索当前用户 skill 库中可用的调研相关 skill，并选择能增强本次输出的 skill 联动使用；具体记录方式见 [references/runtime_skill_selection.md](references/runtime_skill_selection.md)。

默认检索方向包括但不限于：

- 横纵分析 / deep research / 竞品分析：优先考虑 `hv-analysis`
- 产品视频研究 / evidence extraction / competitor research：避免重复本 skill，但可借鉴用户库中更专门的研究 skill
- 网页检索 / 来源核验：如 `tavily-search`、`web-access`
- 可视化 / 知识整理 / 飞书发布：按交付需要调用对应 skill

执行规则：

- 若发现 `hv-analysis` 或其他更适配的调研 skill，明确声明并读取/遵循它，用它补强纵向演进、横向竞品和横纵交汇判断。
- 本 skill 只保留视频证据工作流，不复制其他研究 skill 的方法论明文；不要在本 skill 内维护第二份 HV 或竞品研究说明。
- 若没有发现可用调研 skill，说明已降级，但仍必须覆盖纵向演进、横向对比和交汇洞察，并标注信息缺口。
- 最终报告的 `analysis_manifest.json` 应记录 `skills_consulted`：检索过哪些 skill、实际使用哪些、为什么跳过哪些。

运行时至少把视频证据包、已确认网页事实、竞品候选和用户关注点交给被选中的研究 skill 框架，而不是事后只写一个简短“战略判断”。

## 正式报告结构与可视化交付

只要最终产出 **飞书文档或 `notes.html`**，都必须先读取并覆盖 [references/reference_doc_structure.md](references/reference_doc_structure.md) 的正式报告结构。不能只输出“执行摘要 + 功能拆解”这种简版；缺失的信息也要写成“未找到 / 未核验 / 视频未展示”，不要静默省略。

当报告里需要表达以下内容时，优先补一张图，而不是只写文字：

- 核心工作流 / 用户路径
- 产品架构或能力模块关系
- 纵向时间线
- 横向竞品格局 / 对比关系

默认推荐使用 **SVG → 飞书画板** 的链路生成可编辑流程图。发布飞书时必须读取并执行 [references/diagram_workflow.md](references/diagram_workflow.md) 的图示规划；HTML 兜底时也应插入 SVG/PNG 图示。

## 阶段 1：全局浏览视频

具体命令和启发式策略见 [references/video_analysis.md](references/video_analysis.md)。

这个阶段的目标是：**先看懂整个 demo，再写结论。**

这一阶段至少要产出：

- 粗粒度的产品流程
- 候选功能列表
- 关键时间戳范围
- 需要进一步核验的模糊点或缺口

建议使用低频抽帧和 contact sheet 快速浏览全片，避免把大量上下文浪费在重复画面上。**所有发给模型或子 agent 的截图 / contact sheet 必须先按 `references/video_analysis.md` 生成到 `llm_images/`，不要发送原始大图、不要粘贴 base64、不要使用 `detail: "original"`。**记录候选功能时，至少写下：

- 暂定功能名
- 时间戳或时间范围
- 观察到的 UI 状态
- 可能对应的用户意图
- 这个点的竞争意义
- 置信度（`high` / `medium` / `low`）

## 阶段 2：提取稳定截图

具体方法见 [references/video_analysis.md](references/video_analysis.md)。

如果 UI 正在动，不要只依赖某一个精确时间点截出来的单张图。

对每个候选功能：

- 围绕目标时间点提取一个小 burst
- 从中选最稳定的一张
- 在引用前重新回看这张图
- 如果一个功能跨了多个界面状态，就使用多张图

在会话结束前，始终把 survey frames、contact sheets 和 selected screenshots 存到持久化本地目录里。

## 阶段 3：核验关键网页信息

具体搜索 recipe 见 [references/search_recipes.md](references/search_recipes.md)。

网页核验是默认流程的一部分，不是“高级版附加项”。至少要核验：

- 官方首页
- 官方 docs / help center
- 定价或套餐页（如果相关）
- changelog / release notes / blog（当视频里出现明显新功能时）

只有在对用户问题有帮助时，才继续补充更广的市场信息：

- 用户评价：Reddit、ProductHunt、G2
- 公司 / 团队 / 融资 / 流量
- 与其他竞品的对比

在笔记里明确标注每条信息来自哪里。

## 阶段 4：本地生成报告资产

结构见 [references/output_schema.md](references/output_schema.md)。正式报告信息架构必须覆盖 [references/reference_doc_structure.md](references/reference_doc_structure.md)；`notes.html` 的设计规范与模板见 [references/html_report_design.md](references/html_report_design.md) 与 [assets/notes_template.html](assets/notes_template.html)。

默认应保留一套本地资产，例如：

- `frames_10s/`
- `contact_sheets/`（可选但推荐）
- `selected_screenshots/`
- `llm_images/`（给模型/子 agent 阅读的压缩安全图，必须由 `scripts/prepare_llm_images.py` 生成）
- `notes.html`
- `analysis_manifest.json`

这些资产用于支持两种更好的交付物：**飞书文档**或 **`notes.html`**。

## 阶段 5：默认优先发布到飞书，若不可用则输出 HTML

具体做法见 [references/lark_publishing.md](references/lark_publishing.md)。
飞书正式版报告的信息结构必须先按 [references/reference_doc_structure.md](references/reference_doc_structure.md) 收集整理；设计规范与骨架模板见 [references/lark_report_design.md](references/lark_report_design.md) 与 [references/lark_report_skeleton.md](references/lark_report_skeleton.md)。
飞书组件什么时候用，见 [references/lark_component_guide.md](references/lark_component_guide.md)。需要流程、时间线、架构或竞品关系时，必须读取并使用 [references/diagram_workflow.md](references/diagram_workflow.md)。

关键规则：

- 默认优先输出飞书文档，并对 create / update 操作使用 `--as user`
- 先在本地完成分析，再开始发布
- 优先使用 token-first 和最终布局重建
- 图片必须插在**对应功能小节的标题和说明之间**，不要堆到文档底部
- 单张截图：放在该功能标题下、正文说明前
- 多步骤流程：用 2–4 张图组成 grid，放在该流程说明前
- 如果要表达流程、时间线、竞品关系或架构，按 `diagram_workflow.md` 优先用飞书画板而不是静态图片；至少规划工作流图、纵向时间线图、横向竞品关系/能力地图中适用的图
- 截图默认**不要**使用 `--caption`
- 如果需要说明文字，把它写成图片下方的普通文本
- 如果飞书不可用，则在本地输出 `notes.html`
- 把飞书当作发布层，而不是分析的事实来源

不要把 `reference_doc_structure.md` 当“可选参考”。生成 HTML 或飞书时，它是必读结构；用户明确只要快速草稿时，才可以降级，并要说明降级。

## 默认交付结构

除非用户明确要求快速草稿，否则按 `reference_doc_structure.md` 的正式报告结构组织结果，并至少覆盖：

1. 顶部观点型执行摘要 Callout：一句话介绍、核心亮点、对比我方/竞品的差异和不足
2. 公司与团队：成立时间、总部、母公司、融资、创始人与核心团队、用户/客户/流量信号
3. 产品介绍：核心功能表、产品定位和优势、售卖方式和定价、产品评价/口碑
4. Demo 视频：原始录屏路径、关键片段、输入 vs 输出、多步骤截图 grid
5. 横纵分析：检索并调用适配的调研 skill（优先 `hv-analysis`）后形成纵向演进、横向对比、横纵交汇洞察
6. 图示：工作流/时间线/竞品关系/能力地图，飞书优先画板，HTML 插入 SVG/PNG
7. 相关链接与素材来源
8. 未确认问题与下一步验证清单

每个模块都要有内容；查不到时写“未找到/未核验”，不能直接省略。

## 质量门槛

结束前确认：

- 截图确实支撑对应结论
- 由截图支撑的结论带了时间戳
- 推断性表述已经标明，或被删除
- 产品事实优先使用官方来源核验
- 本地 evidence assets 已保存，并在最终回复里写明路径
- `reference_doc_structure.md` 的所有正式报告模块都已覆盖；缺失项已显式标“未找到/未核验”
- 深度竞品/正式报告已检索用户 skill 库中的调研相关 skill，并记录实际联动/跳过原因；不可用时已说明降级
- 飞书交付已按 `diagram_workflow.md` 规划并插入适用图示/画板；HTML 兜底已插入图示
- 若使用视觉模型或子 agent，确认只发送了 `llm_images/` 内的安全图，且没有 `detail: "original"` / base64 大图进入会话
- 更好的最终交付是飞书文档或 `notes.html`
- 如果发布了飞书，它反映的是已经完成的本地分析，而不是边做边拼的草稿

最后做一次 QA 时，使用 [references/checklist.md](references/checklist.md)。
