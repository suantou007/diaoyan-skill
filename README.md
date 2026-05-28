# diaoyan-skill

> 仓库发布名为 `diaoyan-skill`；skill 内部名保留为 `product-competitor-research`，以兼容已有触发语义。

一个用于**产品录屏竞品调研**的证据型 skill。

它会先浏览视频、提取稳定截图、核验关键网页信息、沉淀本地证据资产，然后**默认优先交付飞书文档**；如果当前环境不适合飞书，再退回到本地 HTML 报告。

## 它能做什么

- 浏览录屏并按时间戳梳理候选功能
- 通过 `prepare_llm_images.py` 避免大图导致的 `413 Payload Too Large`
- 提取稳定截图并保留本地证据包
- 用官网 / 文档 / 定价页做网页核验
- 在正式竞品分析中运行时检索用户 skill 库（如 `hv-analysis`）补强研究质量
- 强制覆盖正式报告结构，而不是只做功能流水账
- 在飞书里按 `diagram_workflow.md` 输出可编辑图示

## 当前文件结构

仓库侧保留：

- `README.md`
- `SKILL.md`
- `references/reference_doc_structure.md`
- `references/diagram_workflow.md`
- `references/workflow.md`
- `references/checklist.md`
- `assets/notes_template.html`
- `scripts/prepare_llm_images.py`

其中对 skill 运行最关键的是：

1. `reference_doc_structure.md`
2. `diagram_workflow.md`
3. `workflow.md`
4. `checklist.md`

## 安装

```bash
npx skills add suantou007/diaoyan-skill -g -y
```

## 前置依赖

| 工具 | 安装方式 |
|------|---------|
| ffmpeg | `brew install ffmpeg` |
| Python Pillow | `python3 -m pip install pillow` |
| lark-cli | `npm install -g @larksuite/cli` |

网页核验优先使用用户已有的 `tavily-search` 或 `web-access` skill。

## 适用场景

- 用户提供 `.mp4` / `.mov` / `.webm` 录屏，希望了解产品到底做了什么
- 用户要求竞品分析、敏捷研究、正式调研报告
- 用户希望最终交付飞书文档或 `notes.html`

## 触发词

当你提到 competitor analysis、competitor research、product video research、敏捷研究、竞品调研、竞品分析、product demo review，或者提供录屏并希望得到结构化结论时，这个 skill 适合被触发。
