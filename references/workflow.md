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
3. 公司与团队
4. 产品定位与目标用户
5. 产品核心功能（先总表，再展开关键功能）
6. 售卖方式与定价
7. 用户评价与外部声量
8. 横纵分析
9. Demo Videos 与视频原链接
10. 相关链接 / Sources

补充约束：

- HTML 不是飞书失败后的“低配导出页”，而是和飞书共享同一套正式研究结构
- 不要让 HTML 继续沿用“证据型功能拆解 / 视频观察 / 网页确认 / 推断”三栏大卡片作为正文主形态
- 这些分层信息应该主要保留在 `analysis_manifest.json`，正文只保留足够支撑判断的精炼表达
- 不要把正文写成“标题很多，但每节只有 1 张图 + 1 段话”的碎片结构
- 正文应该是“标题更少，但每节更厚”：每个主节都要有完整判断和小结

更推荐的高质量写法是：

### 先做一步“主题归并”

在真正写正文前，先不要急着按截图顺序列标题，而是先做一次主题归并：

1. 把视频中的关键动作列出来
2. 判断哪些动作属于同一个更高层的产品能力
3. 只保留 `3–6` 个能力主题进入正文

常见归并方式：

- `引导 + 菜单 + 创建入口` → 一个主题
- `输入方式 + 候选结果 + 试错机制` → 一个主题
- `结果落地 + 场景上下文 + 下一轮生成` → 一个主题

如果你发现自己写出了 7 个以上的功能小节，先不要继续写，优先检查是不是没有做主题归并。

### 写法 A：总表 + 关键小节（默认优先）

1. **功能总表**
   - 列名优先用：`功能 | 视频证据 / 结论 | 竞争意义`
   - 不要默认塞 `时间戳 / 来源` 两列，除非它们真的有决策价值
2. **关键小节**
   - 每个小节优先展开 1 组“能力主题”，而不是 1 个微小操作
   - 顺序：`小标题 → 图片 → 简短图注 → 2~4 段判断`
   - 图注要像：`径向菜单：把专业工具栏游戏化`
   - 不要像：`用于证明：用户通过右键打开主菜单……`
   - 如需补工作流图，默认作为“产品核心功能”章节最后一个小节放入，而不是额外抬成新的大章

推荐把相邻动作合并成一个更有分析价值的主题：

- 可以合并：`径向菜单 + 创建入口 + Create Object`
- 可以合并：`参考图输入 + variant 选择 + 结果落地`
- 可以合并：`场景 Capture + 下一轮生成`

不推荐把这些分别拆成三个标题。

每个主题正文默认使用下面的 4 步结构：

1. **视频里发生了什么**
2. **这暴露出怎样的产品设计取向**
3. **对竞品关系 / 用户门槛 / 产品成熟度意味着什么**
4. **这一节的收束判断**

如果某节缺少第 4 步，通常需要补写；否则整节会显得“有信息、没总结”。

### 可直接套用的“厚写法模板”

下面这个骨架可以直接复用到飞书或 `notes.html`：

```text
1. 执行摘要
   - Callout：
     - 一句话介绍
     - 核心亮点
     - 关键判断
   - Callout 后 2–4 段：
     - 为什么这个产品值得关注
     - 当前最强信号是什么
     - 最大风险或最不确定点是什么

2. 公司与团队
   - 基本信息表
   - 1–2 段总结：
     - 团队背景和产品路线为什么一致
     - 这对今天的竞争位置意味着什么

3. 产品核心功能
   - 3.1 功能总表：功能主题 | 视频证据 / 结论 | 竞争意义
   - 3.2 主题 A
     - 图 / grid
     - 简短图注
     - 第 1 段：视频里发生了什么
     - 第 2 段：背后的产品设计取向
     - 第 3 段：对竞品 / 用户门槛 / 成熟度意味着什么
     - 收束判断
   - 3.3 主题 B
     - 同上
   - 3.4 主题 C
     - 同上
   - 3.x 核心工作流 / 用户路径（如适用，放在本章最后）
     - 工作流图
     - 2–3 段解释闭环与关键摩擦点
     - 收束判断

4. 售卖方式与定价
   - 定价表
   - 2–3 段总结：
     - 这套价格想服务谁
     - 它更像增长型工具还是成熟商业产品
     - 收束判断

5. 用户评价与外部声量
   - 1–2 个正面引用
   - 1–2 个负面 / 风险引用
   - 2–3 段总结：
     - 现在是“方向感强”还是“口碑已成熟”
     - 收束判断

6. 横纵分析
   - 6.1 纵向演进：2–3 段
   - 6.2 横向竞品对比：表 + 2 段解释
   - 6.3 交汇洞察：2–4 段
   - 这一章的最终判断
```

如果你写完后发现：

- 每个主题只有 1 段
- 章节尾部没有“收束判断”
- 总表比正文还长

那基本说明还没有真正套用好这个模板。

### 写法 B：表格内直接放图（当信息密度较低时）

- 可以直接在功能表格对应行插入图片
- 图片下方只写一句短备注，说明图的作用
- 备注应简洁，不要变成一段审计说明

而不是：

`前面写表格，后面再开一个巨大“证据拆解”章节统一解释所有截图`

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
2. 公司与团队
3. 产品定位与目标用户
4. 产品核心功能总表
5. 关键功能小节（图直接跟在对应小节下）
6. 如适用，在产品核心功能章节结尾补“核心工作流 / 用户路径”小节
7. 售卖方式与定价
8. 用户评价与外部声量
9. 横纵分析（内部分“纵向演进 / 横向竞品对比 / 交汇洞察”）
10. Demo Videos 与视频原链接
11. 相关链接 / Sources

写正文时，再加两条：

- **每个大章至少有一个收束段**：解释这一章最重要的判断，不要只有表和图
- **执行摘要后默认再补 2–4 段总括**：说明为什么值得关注、最强信号是什么、最大风险是什么
- **总表只做导航，不替代正文**：真正的价值来自后面的主题展开与章节收口

### 7.2 组件怎么选

- **最重要结论** → `callout`
- **结构化对照** → `lark-table`
- **流程 / 时间线 / 关系 / 架构** → `whiteboard`
- **多张图并排比较** → `grid`
- **外部原话引用** → `quote-container`

### 7.3 图片与图示规则

- 图片必须放在所属功能的小节或所属表格行附近，不能堆到文档底部
- 推荐顺序：**标题 → 图 / grid / 画板 → 图注 → 判断**
- 单张截图不要默认加 caption
- 多步骤流程用 2–4 张图做 `<grid>`
- 工作流 / 时间线 / 竞品关系优先走飞书画板，不用静态拼图硬代替
- 工作流图默认放在“产品核心功能”章节末尾；时间线图放在“横纵分析 > 纵向演进”；竞品关系图放在“横纵分析 > 横向竞品对比”

图注规则：

- 要短、像标题补充，不要像审计备注
- 推荐：`草图输入：粗糙轮廓也能转成更完整视觉方向`
- 不推荐：`用于证明：草图模式允许用户手绘轮廓并生成结果`

标题规则：

- 优先写“能力主题 / 设计取向 / 战略判断”
- 少写“点击了什么 / 打开了什么 / 弹出了什么”这种动作标题
- 如果标题太细，正文分析通常也会跟着变浅

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
- `analysis_manifest.json` 明确记录了 Tavily 与 WebSearch 的分工，而不是只写“已核验”
- 图片没有被单独堆成一个“证据拆解”大章节；而是出现在对应功能位置
- 图注简洁明了，没有大段“用于证明 / 来源 / 时间戳”式啰嗦说明
- 正文整体更像高质量分析报告，而不是取证清单
- HTML 与飞书保持相同的主结构：公司与团队 → 产品定位 → 核心功能 → 定价 → 评价 → 横纵分析 → Demo → Sources
- 标题数量受控，没有切出一堆碎小节
- 每个大节都有足够的总结段，读者看完一节就能拿走判断
- 总表承担的是导航作用，而不是把所有分析都塞进表格里
- 适用图示已按 `diagram_workflow.md` 放入对应章节
- 本地目录里已生成 `notes.html` 与 `analysis_manifest.json`
- 飞书文档已创建并拿到链接；如果没有，已记录用户明确批准的降级原因
- 最终回复写明本地输出路径
