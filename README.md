# diaoyan-skill

一个用于产品录屏竞品调研的证据型 skill。它会浏览视频、提取稳定截图、使用 Tavily 核验关键网页信息、沉淀本地证据资产，并默认交付飞书文档。

## 4.2.0 正式报告结构

1. 速览结论
2. 基本信息与关键数据
3. 产品简介
4. 体验流程分析
5. 竞品分析
6. 主要信息来源

核心变化：

- 先完成正文，再反向提炼开头速览
- 产品名只要来自推断或存在歧义，先向用户确认，再允许发布正式报告
- 产品简介后并排展示官网首页和编辑器首页等产品全貌图
- 体验流程分析合并原功能分析，按完整路径组织能力主题
- 截图只保留简短图注，不在正文写显式截图时间
- 竞品分析优先从用户提供的 Base / bitable 竞品池选择
- 竞品统一覆盖产品定位、用户画像、功能概述、差距 / 优势、可借鉴点
- 外部资料事实按需就近嵌入简短超链接，不生成统一来源尾注
- 文末来源按官方和非官方分组，页面标题作为超链接
- 截图策略使用等距兜底、场景变化候选、关键 burst、本地清晰度与去重选优

## 默认交付

- 飞书正式报告
- 同结构的 `notes.html`
- `analysis_manifest.json`
- 视频截图与 LLM-safe 图片
- 飞书插图计划与校验摘要

## 安装

```bash
npx skills add suantou007/diaoyan-skill -g -y
```

## 主要文件

- `SKILL.md`
- `references/reference_doc_structure.md`
- `references/workflow.md`
- `references/diagram_workflow.md`
- `references/checklist.md`
- `assets/notes_template.html`
- `assets/feishu_template.xml`
- `scripts/prepare_llm_images.py`
- `scripts/insert_feishu_media_with_retry.py`
