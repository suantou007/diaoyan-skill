# 运行时调研 Skill 选择

本 skill 只负责“视频证据包 + 报告交付”。遇到真正的竞品分析 / 敏捷研究 / 深度研究时，必须先检查用户当前可用的 skill 库，挑选能增强调研质量的 skill 联动使用。

## 什么时候必须检索

以下任一条件满足时，必须执行：

- 用户要求竞品分析、敏捷研究、深度研究、给老板/同事看的正式报告
- 最终交付是飞书文档或 `notes.html`
- 需要公司/团队/融资/用户/定价/口碑/横向对比/纵向演进/战略判断

## 检索方向

优先关注这些关键词和能力：

- `hv-analysis`、横纵分析、deep research、深度研究、竞品分析
- product video research、competitor research、evidence extraction
- web search、网页核验、浏览器访问、Tavily
- lark-doc、lark-whiteboard、diagram、可视化

## 使用原则

- 能调用用户库已有 skill，就不要把它的方法论复制进本 skill。
- `hv-analysis` 适合补强纵向演进、横向对比、横纵交汇洞察；如果可用，正式竞品报告默认优先使用。
- `tavily-search` / `web-access` 适合网页检索和动态页面核验。
- `lark-whiteboard` / `diagram_workflow.md` 适合飞书画板和结构图。
- 如果发现多个相关 skill，只选择当前任务真正需要的最小集合，并说明顺序。

## 记录到 manifest

`analysis_manifest.json` 应包含：

```json
{
  "skills_consulted": [
    {
      "name": "hv-analysis",
      "status": "used",
      "reason": "用于纵向演进、横向竞品和交汇洞察"
    },
    {
      "name": "tavily-search",
      "status": "used",
      "reason": "用于网页核验和补充来源"
    },
    {
      "name": "some-skill",
      "status": "skipped",
      "reason": "与本次视频证据分析重复"
    }
  ]
}
```

如果检索不到可用调研 skill，写：`status: "unavailable"`，并在报告中说明降级。
