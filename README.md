# diaoyan-skill

> 仓库发布名为 `diaoyan-skill`；skill 内部名保留为 `product-competitor-research`，以兼容已有触发语义。

一个用于**产品录屏竞品调研**的证据型 skill。

它会先浏览视频、提取稳定截图、核验关键网页信息、沉淀本地证据资产，然后**默认优先交付飞书文档**；如果当前环境不适合飞书，再退回到本地 HTML 报告。

## 它能做什么

- **浏览录屏**：梳理整体工作流，按时间戳识别候选功能
- **提取稳定截图**：围绕关键时刻选出可靠画面，而不是只相信一张脆弱的单帧截图
- **做网页核验**：用官方来源确认产品名、定价、套餐、文档、功能命名、发布时间等关键信息
- **补充市场背景**：在需要时补充评论、公司背景、融资、流量和竞品信号
- **支持真正的竞品分析方法**：当任务不是简单功能识别，而是要做判断时，默认采用横纵分析法（HV）组织分析
- **支持流程图 / 架构图 / 竞品关系图**：优先走 SVG → 飞书画板 的链路，交付可编辑图示
- **保留本地输出**：即使飞书暂时不可用，也会留下可复查的截图、`notes.html` 和结构化 manifest
- **默认优先飞书交付**：默认使用 `--as user` 输出飞书文档；飞书不可用时再退回本地 HTML

## 推荐交付物

更好的交付物优先级：

1. **飞书文档**
2. **本地 HTML 报告**（`notes.html`）

## 默认输出资产

- `frames_10s/`
- `contact_sheets/`（可选）
- `selected_screenshots/`
- `notes.html`
- `analysis_manifest.json`

## 安装

```bash
npx skills add suantou007/diaoyan-skill -g -y
```

如果你是从旧仓库或旧链接迁移过来的，原安装路径 `Candicezsss/product-competitor-research` 已不再作为当前推荐入口。

### 前置依赖

| 工具 | 安装方式 |
|------|---------|
| ffmpeg | `brew install ffmpeg` |
| Tavily CLI | 参考 `tavily-search` skill / `tvly` 配置 |
| lark-cli | `npm install -g @larksuite/cli` |
| lark-cli skills | `npx skills add larksuite/cli -g -y` |

如果需要第一次配置飞书：

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

这个 skill 会补问缺失的信息，例如产品 URL、最关注的问题，以及当前环境是否能正常输出飞书；如果不能，就自动退回本地 HTML。

## 命名说明

- **仓库名**：`diaoyan-skill`
- **skill 内部名**：`product-competitor-research`

保留内部名是为了兼容已有 skill 触发语义；对外分发、安装和引用仓库时，统一使用 `diaoyan-skill`。

## 参考成品

- [makeUGC.ai — 对外展示版报告示例](https://www.feishu.cn/docx/ANvWdxGdJoQyKAxuXxtuh4XXsxb)

## 触发词

当你提到 competitor analysis、competitor research、product video research、敏捷研究、竞品调研、竞品分析、product demo review，或者提供 `.mp4` / `.mov` / `.webm` 录屏并希望得到结构化结论时，这个 skill 就适合被触发。
