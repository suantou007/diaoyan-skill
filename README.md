# diaoyan-skill

一个用于产品录屏竞品调研的证据型 skill。它会浏览视频、提取稳定截图、使用 Tavily 核验关键网页信息、沉淀本地证据资产，并默认交付飞书文档。

## 4.0 正式报告结构

1. 速览结论
2. 基本信息与关键数据
3. 产品简介
4. 功能分析
5. 体验流程分析
6. 竞品分析
7. 主要信息来源

核心变化：

- 先完成正文，再反向提炼开头速览
- 产品简介后并排展示官网首页和编辑器首页等产品全貌图
- 功能分析只依据录屏，并强制截图与功能判断准确匹配
- 体验流程独立成章，覆盖完整用户路径
- 竞品分析采用 2 个亮点对标竞品 + 2 个同类型竞品
- 事实型章节附直接来源链接，文末按官方和非官方分组
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
