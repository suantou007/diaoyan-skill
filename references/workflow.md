# 执行手册

## 1. 导航

- 正式报告结构：`reference_doc_structure.md`
- 图示、产品全貌图和竞品关系图：`diagram_workflow.md`
- 发布前检查：`checklist.md`

正式报告必须先完成正文第 2 至第 7 章，再根据全文反向生成开头速览。

## 2. Intake 与工具检查

开始前确认：

- 视频路径
- 产品名与官网
- 用户最关心的问题
- `tvly` 是否可用
- `lark-cli auth status` 是否可正常发布飞书

默认链路是 Tavily + 飞书。任何一项不可用时，先询问用户是否安装、配置或刷新；只有用户明确同意，才能降级。

## 3. 工作目录

```bash
mkdir -p ~/Desktop/<product>_video_analysis/{frames_10s,scene_candidates,contact_sheets,selected_screenshots,llm_images,official_product_views}
```

默认保留：

```text
<product>_video_analysis/
├── frames_10s/
├── scene_candidates/
├── contact_sheets/
├── selected_screenshots/
├── llm_images/
├── official_product_views/
├── notes.html
├── analysis_manifest.json
├── feishu_media_plan.json
└── feishu_media_insert_summary.json
```

## 4. 视频分析与截图

### 4.1 全片 survey

先读时长：

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 "<video_path>"
```

等距帧只作为覆盖兜底：

```bash
ffmpeg -i "<video_path>" -vf "fps=1/10,scale='min(1280,iw)':-2" -q:v 4 "<workdir>/frames_10s/frame_%04d.jpg"
```

场景变化候选：

```bash
ffmpeg -i "<video_path>" -vf "select='gt(scene,0.18)',scale='min(1280,iw)':-2" -vsync vfr -q:v 4 "<workdir>/scene_candidates/scene_%04d.jpg"
```

候选过少时降到 `0.12`，过多时升到 `0.25`。

### 4.2 生成 LLM-safe 图片

```bash
python3 "<skill_dir>/scripts/prepare_llm_images.py" --workdir "<workdir>"
```

硬规则：

- 模型或子 agent 只接收 `llm_images/`
- 不发送原始截图、原始 contact sheet、base64 或 `detail: "original"`
- 一次最多给子 agent 1 至 2 张安全图

### 4.3 候选功能日志

先记录视频动作，不急着写正文：

- 时间戳范围
- 观察到的 UI
- 用户任务
- 输入、反馈和结果
- 可匹配截图
- 置信度

再把相邻动作归并成 3 至 6 个功能主题。

### 4.4 稳定截图选择

候选池来自：

1. `frames_10s/`
2. `scene_candidates/`
3. 关键时间点 burst

围绕目标点取 `t-2s`、`t-1s`、`t`、`t+1s`、`t+2s`。来自场景变化点时，优先取变化后 `0.5–1.5s` 的稳定帧。

本地选优规则：

- 清晰度：文字、按钮、面板边界清楚
- 稳定态：弹窗展开、结果加载完成、无过渡动画
- 信息量：能说明入口、输入、反馈、结果、编辑或导出
- 去重：同一状态只保留最清晰且最有解释力的一张
- 覆盖：不让某一阶段占满候选名额

必须过滤：

- 黑屏与 loading
- 模糊与半渲染状态
- 系统窗口或通知误入
- 鼠标遮挡关键区域
- 重复 UI 和低信息量画面

数量门槛：

- `selected_screenshots/` 默认至少 16 张
- 正文默认使用 8 至 10 张
- 扩大候选池不增加最终图片数与模型输入量

## 5. 网页核验与来源注册

### 5.1 查询顺序

1. Tavily 搜索与页面抽取
2. WebSearch / `web.run` 补关键缺口
3. `web-access` 补强动态页面或登录态页面

最低核验集合：

- 官方首页与产品入口
- 官方 docs / help
- pricing / plans
- 官方公告、blog、更新日志
- 公司、团队、融资、用户规模
- 竞品官方页面和必要的第三方来源

### 5.2 来源分组

所有网页来源先注册到 `source_registry`：

```json
{
  "source_registry": {
    "official": [
      {
        "title": "页面标题",
        "url": "https://example.com",
        "supports": ["basic_info", "product_intro"]
      }
    ],
    "non_official": [
      {
        "title": "媒体报道标题",
        "url": "https://example.com/article",
        "supports": ["basic_info", "competitor_analysis"]
      }
    ]
  }
}
```

规则：

- 官方来源优先支撑产品事实
- 非官方来源用于交叉验证、市场信号、用户评价与竞争背景
- 每个事实型章节只引用本节实际使用的来源
- 功能分析只依据录屏，不强行补网页来源

### 5.3 产品全貌图

产品简介后需要 2 至 4 张产品全貌图。按以下优先级获取并保存到 `official_product_views/`：

1. 官网首页
2. 编辑器首页或产品工作台首页
3. 社区、内容分发或关键终端首页
4. 录屏中的编辑器总览
5. 官方帮助中心或官方博客素材

并排图应能解释产品构成，不要只选风格相似的宣传图。

## 6. 正文生成

### 6.1 必须先写第 2 至第 7 章

按以下顺序生成草稿：

1. 基本信息与关键数据
2. 产品简介与产品全貌图
3. 功能分析
4. 体验流程分析
5. 竞品分析
6. 主要信息来源

完成后做内部一致性检查，再反向生成“速览结论”并放在最前。

### 6.2 基本信息与关键数据

- 使用表格
- 融资、用户规模和定价优先写具体数字、时间口径与直接链接
- 章末生成简短“本节来源”

### 6.3 产品简介

- 使用 **产品定位** / **核心需求** / **主体验** / **当前阶段**
- 简介后立即放产品全貌截图 grid
- 章末生成“本节来源”

### 6.4 功能分析

只依据录屏，写 3 至 6 个能力主题。每个主题采用：

```text
小标题
功能说明：用户做什么、关键交互是什么、系统如何反馈
匹配截图：准确展示该功能，带短图注
体验判断：亮点、摩擦或限制
```

禁止：

- 把官网宣传口径当作录屏观察
- 用无关或模糊截图支撑功能判断
- 为了形式完整而附网页来源

### 6.5 体验流程分析

默认路径：

```text
入口与 onboarding → 输入或创建 → 生成或处理 → 编辑与反馈 → 导出或分享
```

交付至少包含一张流程图或流程表。分析关键反馈、等待、跳转、付费点和摩擦点。章末只列本节实际使用的网页来源。

### 6.6 竞品分析

#### 选择流程

1. 从功能分析与体验流程中提炼本产品 1 至 2 个核心亮点
2. 为每个亮点选择一个最能代表该亮点的竞品，共 2 个
3. 选择 2 个最直接的同类型竞品
4. 优先四个产品互不重复；必须重叠时说明原因

#### 两组表格

亮点对标竞品：

```text
产品 | 对标亮点 | 实现方式 | 用户价值 | 本产品差距 / 优势 | 可借鉴点
```

同类型竞品：

```text
产品 | 定位与用户 | 平台与场景 | 核心流程 | 内容生态 | 商业化 | 关键差异
```

末尾写“竞争判断”，合并本产品竞争位置、优势、短板和关键约束。章末列来源。

### 6.7 主要信息来源

分为：

- 官方信息
- 非官方信息

只列页面标题与直接 URL。

### 6.8 反向生成速览

速览必须从已完成正文中提炼：

- 总体判断
- 产品构成
- 关键模块
- 亮点
- 短板
- 综合竞争判断

不要在速览中新增正文没有支持的事实或判断。

## 7. `analysis_manifest.json`

最低结构：

```json
{
  "product": "",
  "official_url": "",
  "video": {},
  "overview": {
    "generated_after_body": true,
    "overall_judgment": "",
    "product_components": [],
    "key_modules": [],
    "strengths": [],
    "limitations": [],
    "competitive_judgment": ""
  },
  "basic_info": {},
  "section_sources": {
    "basic_info": [],
    "product_intro": [],
    "experience_flow": [],
    "competitor_analysis": []
  },
  "source_registry": {
    "official": [],
    "non_official": []
  },
  "official_product_views": [],
  "function_analysis": [],
  "experience_flow": {
    "steps": [],
    "diagram": {},
    "friction_points": [],
    "feedback_loops": []
  },
  "competitor_analysis": {
    "highlight_competitors": [],
    "same_type_competitors": [],
    "selection_rationale": [],
    "competitive_judgment": ""
  },
  "screenshot_selection": {},
  "skills_consulted": [],
  "consistency_check": {}
}
```

`function_analysis` 每项至少保留：

- `id` / `title`
- `timestamp_start` / `timestamp_end`
- `screenshots` / `llm_safe_images`
- `observed_ui`
- `experience_judgment`
- `inferences`
- `confidence`

功能分析不放 `confirmed_facts` 或 `web_sources`；需要网页确认的事实放到其他章节。

`screenshot_selection` 至少记录：

- `candidate_sources`
- `selection_rules`
- `cost_guardrail`
- `rejected_patterns`

## 8. HTML 与飞书发布

### 8.1 HTML

- 基于 `assets/notes_template.html`
- 与飞书使用同一七章结构
- 产品简介后使用并排产品全貌图
- 事实型章节显示简短来源块
- 文末按官方与非官方分组

### 8.2 飞书

- 使用 `assets/feishu_template.xml` 作为模板源
- 所有 create / update 命令显式传 `--api-version v2 --as user`
- 图片放在所属章节，不能堆到文末
- 并列图片使用 grid / 分栏
- 体验流程图与竞品关系图优先画板
- `docs +media-insert` 失败时重试，并用 `docs +fetch` 验证图片真实插入

推荐插图：

```bash
python3 "<skill_dir>/scripts/insert_feishu_media_with_retry.py" \
  --plan "<workdir>/feishu_media_plan.json" \
  --summary-out "<workdir>/feishu_media_insert_summary.json"
```

## 9. 最终 QA

发布前逐项执行 `references/checklist.md`。公开正文中不得出现内部一致性检查、搜索过程、失败记录或工具说明。
