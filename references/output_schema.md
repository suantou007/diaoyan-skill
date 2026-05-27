# 输出结构

更好的交付物是：**飞书文档**或**本地 HTML 报告**。

默认先保留一套本地资产，用来支持这两种交付。

## 推荐目录结构

```text
<product>_video_analysis/
├── frames_10s/
├── contact_sheets/   # 可选
├── selected_screenshots/
├── notes.html
└── analysis_manifest.json
```

## `notes.html`

本地兜底交付统一使用 `notes.html`，不要再输出 `notes.md`。

生成的 HTML 报告应与下列逻辑结构一致：

```text
<产品名>

1. 执行摘要
2. 产品快照
3. 证据型功能拆解
   3.1 <功能标题>
   - Timestamp
   - Screenshot
   - Observed in video
   - Confirmed on web
   - Inference / open question
   - Competitive significance
4. 核心工作流 / 用户路径
5. 定价 / 套餐
6. 市场或评论信号
7. 未确认问题与开放问题
8. 素材路径
```

HTML 不需要过度复杂，但应具备基本可读性，例如：

- 清晰标题层级
- 截图与说明对应
- 明显区分“视频观察 / 网页确认 / 推断”
- 能直接交付给人阅读，而不是只是机器中间产物

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
  "features": [
    {
      "id": "03_asset_library",
      "title": "Asset library with category filtering",
      "timestamp_start": "00:02:34",
      "timestamp_end": "00:02:50",
      "screenshots": [
        "selected_screenshots/03_asset_library.jpg"
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

关键原则：`observed_ui`、`confirmed_facts`、`inferences` 三类信息必须分开。
