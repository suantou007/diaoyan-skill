# product-competitor-research

一个用于**产品录屏竞品调研**的证据型 skill。

它会先浏览视频、提取稳定截图、核验关键网页信息、沉淀本地 research package，再在需要时把结果发布成一份更正式的 Lark 文档。

## 它能做什么

- **浏览录屏**：梳理整体工作流，按时间戳识别候选功能
- **提取稳定截图**：围绕关键时刻选出可靠画面，而不是只相信一张脆弱的单帧截图
- **做网页核验**：用官方来源确认产品名、定价、套餐、文档、功能命名、发布时间等关键信息
- **补充市场背景**：在需要时补充评论、公司背景、融资、流量和竞品信号
- **保留本地输出**：即使不发布文档，也会留下可复查的截图、笔记和结构化 manifest
- **可选发布到 Lark**：只有在分析完成后，才把结果整理成对外展示的文档

## 默认输出物

- `frames_10s/`
- `contact_sheets/`（可选）
- `selected_screenshots/`
- `notes.md`
- `analysis_manifest.json`

## 安装

```bash
npx skills add Candicezsss/product-competitor-research -g -y
```

### 前置依赖

| 工具 | 安装方式 |
|------|---------|
| ffmpeg | `brew install ffmpeg` |
| Tavily CLI | 参考 `tavily-search` skill / `tvly` 配置 |
| lark-cli | `npm install -g @larksuite/cli` |
| lark-cli skills | `npx skills add larksuite/cli -g -y` |

如果需要发布到 Lark，首次配置：

```bash
lark-cli config init --new
lark-cli auth login --domain drive
```

## 使用方式

例如：

```text
帮我做这个产品的视频竞品调研，这是录屏 @/path/to/recording.mp4
Watch this recording and tell me what the product actually does
分析这个竞品视频，重点看 agent workflow 和定价
```

这个 skill 会补问缺失的信息，例如产品 URL、最关注的问题，以及最终结果是保留在本地还是发布到 Lark。

## 参考成品

- [makeUGC.ai — 对外展示版报告示例](https://www.feishu.cn/docx/ANvWdxGdJoQyKAxuXxtuh4XXsxb)

## 触发词

当你提到 competitor analysis、competitor research、product video research、敏捷研究、竞品调研、竞品分析、product demo review，或者提供 `.mp4` / `.mov` / `.webm` 录屏并希望得到结构化结论时，这个 skill 就适合被触发。
