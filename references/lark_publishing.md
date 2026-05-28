# 飞书发布

默认优先发布到飞书，并对所有 create / update 操作使用 **`--as user`**。

前提是：本地报告资产已经完成，并且已经按 `reference_doc_structure.md` 完整收集整理。飞书是正式交付，不是简版摘要。

## 推荐工作流

1. 先在本地完成分析，并覆盖 `reference_doc_structure.md` 的所有模块
2. 读取 `diagram_workflow.md`，规划工作流图、时间线图、竞品关系/能力地图中适用的图
3. 图片和图示上传一次并拿到 token；流程/时间线/关系图优先用飞书画板
4. 在本地组装最终 Markdown / XML 布局，按结构一次性创建或少量分段写入
5. 最后检查渲染结果、图示位置和截图位置

不要把飞书文档当成工作草稿。

## 默认规则

- 默认对所有飞书创建 / 更新操作显式传 `--as user`
- 优先用 token-first 和最终布局重建，不要默认走反复 append 的方式
- 飞书报告必须完整覆盖 `reference_doc_structure.md`：执行摘要、公司团队、用户/客户/流量、核心功能、定位优势、定价、评价、Demo、链接；缺失项写明“未找到/未核验”
- 飞书报告也应有明确的视觉层级、节奏和版式，不要只追求“信息塞进去”
- 图片必须出现在**对应功能段落内部**，不要集中追加到文档末尾
- 单张截图应放在该功能标题下、说明文字前；读者应先看到图，再读解释
- 如果一个功能对应多步操作或多个稳定 UI 状态，使用 2–4 张图的 `<grid>`，紧跟在该功能标题后，再写文字说明
- “产品快照”类总览图可以放在 Executive Summary 或 Product Snapshot 之后，但不能替代具体功能图
- 截图默认**不要**用 `--caption`，否则容易在图片下方出现不想要的白边 / 留白
- 如果需要图片说明，直接把说明写成图片下方普通文本
- 如果使用 `docs +media-insert`，文件路径必须是**相对路径**，并且命令执行时 `cwd` 要切到图片目录

## 图片位置规则

### 飞书文档

推荐顺序：

1. 功能标题
2. 图片或图片 grid
3. 说明文字
4. 下一功能标题

不要使用下面这种错误顺序：

1. 所有文字先写完
2. 所有图片最后统一插入到底部

### HTML 报告

HTML 中也保持同样规则：

- 每个 `<section>` 内部，先放功能标题
- 再放 `<img>` 或图片组
- 再放说明文字、证据来源、时间戳

不要让图片脱离所属 section 单独堆到页面尾部。

## 相对路径提醒

```bash
# 错误
lark-cli docs +media-insert --doc "<DOC_ID>" --file "/absolute/path/shot.jpg"

# 更稳妥
cd /path/to/images && lark-cli docs +media-insert --doc "<DOC_ID>" --file ./shot.jpg --align center
```

## 飞书不可用时的兜底

如果当前环境无法正常输出飞书，或者发布过程开始变脆弱、混乱或难以维护，就停止在线编辑，先交付 `notes.html` 和本地证据资产。调研结果本身不应该依赖飞书是否发成功。

## 报告结构要求

飞书交付默认就是正式报告：必须使用 [reference_doc_structure.md](reference_doc_structure.md) 作为信息架构；结合 [diagram_workflow.md](diagram_workflow.md) 规划画板/图示；再用 [lark_report_design.md](lark_report_design.md)、[lark_report_skeleton.md](lark_report_skeleton.md) 和 [lark_component_guide.md](lark_component_guide.md) 做版式与组件选择。
