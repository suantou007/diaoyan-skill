# 输出结构

更好的交付物是：**飞书文档**或**本地 HTML 报告**。

默认先保留一套本地资产，用来支持这两种交付。

## 推荐目录结构

```text
<product>_video_analysis/
├── frames_10s/
├── contact_sheets/   # 可选；原始/发布用，不直接发模型
├── selected_screenshots/
├── llm_images/       # 模型/子 agent 专用压缩安全图
├── notes.html
└── analysis_manifest.json
```

## `notes.html`

本地兜底交付统一使用 `notes.html`，不要再输出 `notes.md`。
推荐直接基于 [assets/notes_template.html](../assets/notes_template.html) 生成，并参考 [html_report_design.md](html_report_design.md) 的页面规范。

生成的 HTML 报告必须覆盖 [reference_doc_structure.md](reference_doc_structure.md) 的正式报告模块；不要只写功能流水账。推荐逻辑结构：

```text
<产品名>

1. 执行摘要 Callout
   - 一句话介绍
   - 核心亮点
   - 对比我方/竞品的差异与不足
2. 公司与团队
   - 基本信息：成立时间、总部、母公司、融资
   - 创始人与核心成员
   - 用户、客户、流量、品牌客户或“未找到”
3. 产品介绍
   - 核心功能表：功能 | 描述 | 图片/视频证据 | 来源
   - 产品定位和优势
   - 售卖方式和定价（含 API 定价；没有则写未发现）
   - 产品评价：G2/ProductHunt/社区/媒体，正负反馈分开
4. Demo 视频
   - 原始录屏路径
   - 输入 vs 输出对比
   - 关键片段和多步骤截图 grid
5. 横纵分析
   - 纵向演进
   - 横向竞品对比
   - 横纵交汇洞察
6. 图示
   - 工作流 / 时间线 / 竞品关系 / 能力地图中适用者
7. 相关链接、素材路径、未确认问题
```

HTML 不需要过度复杂，但应具备基本可读性，例如：

- 完整覆盖 `reference_doc_structure.md`；缺失项明确写“未找到/未核验”，不能省略
- 清晰标题层级
- 截图与说明对应，且图片放在所属功能标题下、说明文字前
- 明显区分“视频观察 / 网页确认 / 推断”
- 能直接交付给人阅读，而不是只是机器中间产物
- 整体上像一份正式前端报告页面，而不是纯文本 dump

推荐 section 内部顺序：

1. 功能标题
2. 图片或图片组
3. 时间戳
4. 视频观察
5. 网页确认
6. 推断 / 开放问题
7. 竞争意义

## `analysis_manifest.json`

建议每个候选功能保留一条记录。最低字段如下：

```json
{
  "product": "Example Product",
  "official_url": "https://example.com",
  "video": {
    "path": "/path/to/video.mp4",
    "duration_seconds": 540
  },
  "company_profile": {
    "founded": "未核验",
    "headquarters": "未核验",
    "parent_company": "未找到",
    "funding": [],
    "team": [],
    "traffic_or_customers": []
  },
  "pricing": {
    "plans": [],
    "api_pricing": "未找到"
  },
  "reviews": {
    "positive": [],
    "negative": [],
    "missing_sources": []
  },
  "skills_consulted": [
    {
      "name": "hv-analysis",
      "status": "used | skipped | unavailable",
      "reason": "用于纵向演进、横向对比和交汇洞察"
    }
  ],
  "hv_analysis": {
    "skill_used": "hv-analysis | other research skill | unavailable",
    "vertical_evolution": [],
    "horizontal_comparison": [],
    "intersection_insights": []
  },
  "diagrams": [
    {
      "type": "workflow | timeline | competitor_map | capability_map",
      "path": "diagrams/workflow.svg",
      "lark_whiteboard": "block/token if published"
    }
  ],
  "features": [
    {
      "id": "03_asset_library",
      "title": "Asset library with category filtering",
      "timestamp_start": "00:02:34",
      "timestamp_end": "00:02:50",
      "screenshots": [
        "selected_screenshots/03_asset_library.jpg"
      ],
      "llm_safe_images": [
        "llm_images/selected_screenshots/03_asset_library.jpg"
      ],
      "observed_ui": [
        "Left sidebar shows asset categories",
        "Dragging an item places it into the scene"
      ],
      "confirmed_facts": [
        "Official site describes a reusable asset library"
      ],
      "inferences": [
        "Category taxonomy may also influence recommendation quality"
      ],
      "web_sources": [
        "official-homepage",
        "official-docs"
      ],
      "confidence": "high"
    }
  ]
}
```

关键原则：`observed_ui`、`confirmed_facts`、`inferences` 三类信息必须分开。`screenshots` 保存原始证据/发布图，`llm_safe_images` 只记录发给模型或子 agent 的压缩安全图。
