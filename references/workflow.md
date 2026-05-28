# 执行手册

这份文件合并了旧的分散说明。除 `reference_doc_structure.md` 和 `diagram_workflow.md` 外，其余执行细节都看这里。

## 1. 导航

- **正式报告结构**：先读 `reference_doc_structure.md`
- **图示 / 画板**：需要流程、时间线、竞品关系时读 `diagram_workflow.md`
- **视频分析、网页核验、本地输出、飞书发布、QA**：读本文件

如果用户明确只要快速草稿，可以降级；否则默认按正式报告结构交付。

## 2. Intake 与工具检查

开始前补齐：

- 视频路径
- 产品名
- 官网 URL（已知则直接用）
- 用户最关心的问题 / 竞品视角
- Tavily 是否可用；不可用时不要静默换 WebSearch，先问用户要不要安装/配置 Tavily
- 飞书是否可用；不可用时不要静默退回 HTML，先问用户要不要配置/刷新飞书 CLI

只检查当前任务真正需要的工具：

- `ffmpeg` / `ffprobe`
- `python3` + Pillow
- `tvly`（默认网页核验必须用）
- `lark-cli` / `lark-doc`（默认正式交付必须用）

### 默认规则：Tavily + 飞书

正式运行时，默认链路必须是：

1. **Tavily 搜索 / 核验**
2. **飞书文档交付**

禁止默认行为：

- 没有 Tavily 就直接改用内置 WebSearch / `web.run`
- 没有飞书就直接只产出 `notes.html`

正确行为：

- `tvly` 缺失、未登录、网络不可用、鉴权失败 → **先问用户要不要现在安装/配置 Tavily**
- `lark-cli` 缺失、用户身份未授权、token 刷新失败、权限不通 → **先问用户要不要现在配置/刷新飞书 CLI**

只有用户明确同意降级，才允许不用 Tavily 或不发飞书。

补充规则：

- **Tavily 是默认入口，不是唯一来源。** 如果 Tavily 没抓到关键事实，尤其是价格、套餐额度、限制、日期、具体数字，就必须继续补 WebSearch / `web.run`；如果页面是强动态或需要登录态，再补 `web-access`。

## 3. 运行时调研 Skill 选择

以下任一情况满足时，必须先检索用户 skill 库：

- 用户要竞品分析、敏捷研究、深度研究、给老板 / 同事看的正式报告
- 最终交付是飞书文档或 `notes.html`
- 需要公司 / 团队 / 融资 / 用户 / 定价 / 评价 / 横向对比 / 纵向演进 / 战略判断

默认优先级：

1. `hv-analysis`：补强纵向演进、横向对比、横纵交汇洞察
2. `tavily-search`：默认网页检索与来源发现
3. `lark-whiteboard`：把流程图 / 时间线 / 关系图写进飞书画板

补充规则：

- `web-access` 不是默认搜索入口；只有 Tavily 已找到线索，但需要登录态 / 动态页面补抓时再调用
- `web.run` / WebSearch 是 **Tavily 之后的补足层**：当 Tavily 没抓到关键事实时，应继续补查
- manifest 里要把 Tavily 与 WebSearch / `web-access` 的分工写清楚，避免出现“skill 说默认 Tavily，实际偷偷换成别的搜索”或“明明没查到还假装查全了”

原则：

- 只选真正需要的最小集合，不要什么都调
- 不把其他 research skill 的方法论明文复制进本 skill
- 检索不到可用 skill 时，也要继续完成报告，并在 manifest 标 `unavailable`

`analysis_manifest.json` 至少记录：

```json
{
  "skills_consulted": [
    {
      "name": "hv-analysis",
      "status": "used | skipped | unavailable",
      "reason": "用于纵向演进、横向竞品和交汇洞察"
    }
  ]
}
```

## 4. 视频分析与 413 防护

### 4.1 创建持久化工作目录

```bash
mkdir -p ~/Desktop/<product>_video_analysis/{frames_10s,contact_sheets,selected_screenshots,llm_images}
```

所有衍生素材都尽量放在这个目录，不要长期留在 `/tmp`。

### 4.2 全局 survey

先看时长：

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 "<video_path>"
```

低频抽帧：

```bash
ffmpeg -i "<video_path>" -vf "fps=1/10,scale='min(1280,iw)':-2" -q:v 4 "<workdir>/frames_10s/frame_%04d.jpg"
```

如果视频很短，可改成 `fps=1/5`。

### 4.3 先生成安全图，再让模型看图

```bash
python3 "<skill_dir>/scripts/prepare_llm_images.py" --workdir "<workdir>"
```

硬规则：

- 发给模型或子 agent 的图片只来自 `llm_images/`
- 不发送原始截图、原始 contact sheet、base64 图片
- 不用 `detail: "original"`
- 一次最多给子 agent 1–2 张安全图
- 任何超大图继续压缩，不要硬塞进会话

### 4.4 维护候选功能日志

对每个候选功能，至少记录：

- 暂定标题
- 时间戳 / 时间范围
- 观察到的 UI
- 对应的用户任务
- 竞争意义
- 置信度（`high` / `medium` / `low`）

### 4.5 提取稳定截图

不要迷信单帧。围绕目标时间点取一个 burst，再选最稳的一张。

```bash
ffmpeg -ss 00:02:34 -i "<video_path>" -frames:v 1 -vf "scale='min(1600,iw)':-2" -q:v 3 "<workdir>/selected_screenshots/03_feature_t0.jpg"
```

通常围绕 `t-2s`、`t-1s`、`t`、`t+1s`、`t+2s` 各取一张；多状态功能可保留多张图。

选好截图后，重新生成安全图：

```bash
python3 "<skill_dir>/scripts/prepare_llm_images.py" --workdir "<workdir>" --no-generated-sheets
```

### 4.6 必须保留的证据

- 原始录屏路径
- survey frames
- contact sheets（如果生成）
- selected screenshots
- `llm_images/manifest.json`

## 5. 网页核验（默认 Tavily，关键缺口必须继续补）

最低核验集合：

1. 官方首页
2. 官方 docs / help center
3. 官方 pricing / plans
4. 官方 changelog / release notes / blog（视频展示明显新功能时）

可按需补充：

- ProductHunt / G2 / Reddit 的评价
- 公司 / 创始人 / 融资 / 流量 / 客户
- 竞品比较和替代方案

基本原则：

- 产品事实优先看官方来源
- 视频展示了什么、网页确认了什么、你推断了什么，三者必须分开
- 二手来源用于补充背景，不要当作核心产品事实的第一来源

默认直接用 Tavily。推荐最小查询集：

```bash
tvly search "\"<product>\" official site" --max-results 5 --json
tvly search "\"<product>\" pricing OR plans" --include-domains <official_domain> --max-results 8 --json
tvly search "\"<product>\" docs OR help OR documentation" --include-domains <official_domain> --max-results 8 --json
tvly search "\"<company_or_product>\" founder funding" --max-results 8 --json
```

如果 `tvly` 不可用：

1. 不要直接切到 WebSearch / `web.run`
2. 先问用户：**要不要现在安装/配置 Tavily？**
3. 只有用户明确同意降级，才改用别的联网方式

如果需要动态页面或登录态补抓：

- 先用 Tavily 找到 URL 和来源
- 再用 `web-access` 做补抓
- 在 manifest 里把二者的分工写清楚

### Tavily 没抓到时怎么补

只要遇到下面这些高价值字段，就不能因为 Tavily 没返回而直接停下：

- 价格
- 套餐额度 / credits / limits
- 关键限制（是否带水印、导出限制、seat、API 有无）
- 具体发布日期 / 更新日期
- 公司关键数字

补查顺序：

1. **先 Tavily**
2. **再 WebSearch / `web.run`**
3. **最后 `web-access`**（仅强动态页面 / 登录态必需时）

如果补到最后还是没有，就显式写：

- `Tavily 未抓到`
- `WebSearch 已补查`
- `仍未找到可靠来源`

不要只写一个模糊的“未抓到”。

## 6. 本地输出

推荐目录结构：

```text
<product>_video_analysis/
├── frames_10s/
├── contact_sheets/
├── selected_screenshots/
├── llm_images/
├── notes.html
└── analysis_manifest.json
```

### 6.1 `notes.html`

直接基于 `assets/notes_template.html` 生成，风格保持：

- editorial / research dossier / strategy memo
- 像正式研究报告，不像 SaaS 营销页
- 不要炫技，不要堆花哨特效

推荐顺序：

1. 封面 / Hero
2. 执行摘要
3. 公司与团队 / 产品快照
4. 产品介绍表格（功能 / 描述 / 图片证据 / 时间戳 / 来源）
5. 核心工作流 / 用户路径
6. 纵向演进
7. 横向对比
8. 开放问题 / 未确认项 / 相关链接

默认不要再做一个单独的大型“证据型功能拆解”章节，把图片集中堆放在后面。更推荐：

- **直接在产品介绍 / 核心功能表格中放图**
- 图片紧贴它对应的功能行或功能小节
- 图片旁边或图片下方直接写备注，说明“这张图在证明什么”

也就是说，默认结构应是：

`功能 | 说明 | 图片证据（带备注） | 时间戳 / 来源`

### 6.2 `analysis_manifest.json`

最低需要覆盖：

- `product`、`official_url`、`video`
- `company_profile`
- `pricing`
- `reviews`
- `skills_consulted`
- `hv_analysis`
- `diagrams`
- `features`

`features` 里至少保留：

- `id` / `title`
- `timestamp_start` / `timestamp_end`
- `screenshots`
- `llm_safe_images`
- `observed_ui`
- `confirmed_facts`
- `inferences`
- `web_sources`
- `confidence`

关键规则：`observed_ui`、`confirmed_facts`、`inferences` 必须分开。

## 7. 飞书发布（默认必须交付飞书）

默认必须飞书，并对所有 create / update 操作显式传 `--as user`。

发布前只做 3 件事：

1. 先按 `reference_doc_structure.md` 检查模块是否齐全
2. 再按 `diagram_workflow.md` 规划哪些地方必须补图
3. 最后写飞书正文

### 7.1 正文顺序

推荐顺序：

1. 顶部执行摘要 Callout
2. 公司与团队 / 产品快照
3. 核心功能拆解
4. 核心工作流 / 用户路径
5. 纵向演进
6. 横向对比
7. 定价 / 套餐 / 评价
8. 开放问题 / 未确认项 / 相关链接

### 7.2 组件怎么选

- **最重要结论** → `callout`
- **结构化对照** → `lark-table`
- **流程 / 时间线 / 关系 / 架构** → `whiteboard`
- **多张图并排比较** → `grid`
- **外部原话引用** → `quote-container`

### 7.3 图片与图示规则

- 图片必须放在所属小节内部，不能堆到文档底部
- 推荐顺序：**标题 → 图 / grid / 画板 → 说明文字 → 判断**
- 单张截图不要默认加 caption
- 多步骤流程用 2–4 张图做 `<grid>`
- 工作流 / 时间线 / 竞品关系优先走飞书画板，不用静态拼图硬代替

### 7.4 路径注意

`docs +media-insert` 用相对路径；执行前先 `cd` 到图片目录。

```bash
cd /path/to/images && lark-cli docs +media-insert --doc "<DOC_ID>" --file ./shot.jpg --align center
```

### 7.5 飞书不可用时

如果权限不通、在线编辑开始混乱、token 刷新失败或排版持续失控：

1. 先问用户：**要不要现在配置 / 刷新飞书 CLI？**
2. 只有用户明确允许降级，才改成交付 `notes.html` 和本地证据资产

换句话说：**默认是飞书，不是“飞书优先但随时静默退回 HTML”。**

## 8. 最终 QA

结束前确认：

- 已覆盖 `reference_doc_structure.md` 的正式报告模块
- 缺失项已明确写成“未找到 / 未核验 / 视频未展示”
- 视频观察 / 网页确认 / 推断 已清晰分开
- 由截图支撑的结论都带时间戳
- 选中的截图是稳定画面，不是过渡态
- `scripts/prepare_llm_images.py` 已跑过，发给模型的图只来自 `llm_images/`
- `skills_consulted` 已记录实际使用 / 跳过 / unavailable
- Tavily 已作为默认搜索入口实际执行；如果没有，已记录用户明确批准的降级原因
- Tavily 没抓到的价格 / 套餐 / 限制等关键事实，已继续用 WebSearch / `web.run` 补查
- 图片没有被单独堆成一个“证据拆解”大章节；而是出现在对应表格 / 对应功能位置，并带有明确备注说明图片作用
- 适用图示已按 `diagram_workflow.md` 放入对应章节
- 本地目录里已生成 `notes.html` 与 `analysis_manifest.json`
- 飞书文档已创建并拿到链接；如果没有，已记录用户明确批准的降级原因
- 最终回复写明本地输出路径
