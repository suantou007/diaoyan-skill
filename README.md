# diaoyan-skill

> 仓库发布名为 `diaoyan-skill`；skill 名为 `diaoyan`。旧的 `product-competitor-research` 只作为触发语义兼容，不再作为内部名称。

一个用于**产品录屏竞品调研**的证据型 skill。

它会先浏览视频、提取稳定截图、通过 **Tavily** 核验关键网页信息、沉淀本地证据资产，然后**默认交付飞书文档**。如果 Tavily 或飞书未配置，正确行为是先询问用户是否安装/配置，而不是静默降级。

正式交付默认收口为一套更紧凑的研究结构：

1. 公司与团队
2. 产品定位与目标用户
3. 产品核心功能（总表 → 关键小节 → 如有必要并入核心工作流）
4. 售卖方式与定价
5. 用户评价与外部声量
6. 横纵分析
7. Demo Videos 与视频原链接
8. 相关链接 / Sources

默认**不**在正文里机械重复“时间戳 / 来源 / 用于证明”；这些信息优先沉淀在本地 evidence package 与 `analysis_manifest.json`，只有在真正帮助判断时才写进正文。

另外，当前 skill 的写作方向明确调整为：**标题更少、内容更厚**。默认按能力主题归并章节，不鼓励把一个个微小操作拆成很多小标题。

这次还把一套更具体的“厚写法”沉淀了进去：

- 先把视频里的零散动作归并成 **3–6 个能力主题**
- 总表只做索引，不承担主要分析
- 每个主题至少回答“发生了什么 / 暴露了什么设计取向 / 对竞争意味着什么 / 最后怎么判断”
- 每个大章结尾都要有一句或一段**收束判断**
- 如果某个小节只有 1 张图 + 1 段话，默认视为切得太细，应该并回更大的主题

## 它能做什么

- 浏览录屏并按时间戳梳理候选功能
- 通过 `prepare_llm_images.py` 避免大图导致的 `413 Payload Too Large`
- 提取稳定截图并保留本地证据包
- 默认用 Tavily 做官网 / 文档 / 定价页核验；Tavily 没抓到的关键字段继续补 WebSearch
- 在正式竞品分析中运行时检索当前会话可用 skills；必要时用 `tool_search` 发现懒加载工具（如 `hv-analysis`）补强研究质量
- 强制覆盖正式报告结构，而不是只做功能流水账
- 在飞书里按 `diagram_workflow.md` 输出可编辑图示
- 让 HTML 与飞书默认使用同一套章节顺序与写作风格，而不是一个精细、一个凑合

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
| lark-cli | `npm install -g @larksuite/cli`，用 `lark-cli auth status` 检查认证 |

默认网页核验必须先使用 Tavily；Tavily 没抓到关键事实时继续补 WebSearch，`web-access` 只作为动态页面 / 登录态补抓的补充工具。默认正式交付必须发布到飞书。

## 适用场景

- 用户提供 `.mp4` / `.mov` / `.webm` 录屏，希望了解产品到底做了什么
- 用户要求竞品分析、敏捷研究、正式调研报告
- 用户希望最终交付飞书文档或 `notes.html`

## 触发词

当你提到 competitor analysis、competitor research、product video research、敏捷研究、竞品调研、竞品分析、product demo review，或者提供录屏并希望得到结构化结论时，这个 skill 适合被触发。
