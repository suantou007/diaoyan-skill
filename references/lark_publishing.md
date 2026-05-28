# 飞书发布

默认优先发布到飞书，并对所有 create / update 操作使用 **`--as user`**。

前提是：本地报告资产已经完成，并且已经按 `reference_doc_structure.md` 收集整理完整。飞书是正式交付，不是简版摘要。

## 发布前只看 3 件事

1. **结构**：先按 [reference_doc_structure.md](reference_doc_structure.md) 检查信息模块是否齐全  
2. **图示**：再按 [diagram_workflow.md](diagram_workflow.md) 判断哪些地方必须补图  
3. **骨架**：最后按 [lark_report_skeleton.md](lark_report_skeleton.md) 组织飞书正文顺序

不要在飞书写法上查太多文档；默认把这 3 份用好就够了。

## 最小工作流

1. 先在本地完成分析，并覆盖正式报告结构
2. 规划工作流图 / 时间线图 / 竞品关系图中适用的图
3. 在本地组装最终 XML / Markdown，再创建或少量分段写入飞书
4. 最后检查图示位置、截图位置和版式节奏

不要把飞书文档当工作草稿反复 append。

## 核心规则

- 默认对所有飞书创建 / 更新操作显式传 `--as user`
- 优先一次性结构化写入，不要默认走长篇碎片式 append
- 飞书报告必须完整覆盖 `reference_doc_structure.md`；缺失项写明“未找到 / 未核验 / 视频未展示”
- 图片必须放在**对应功能小节内部**，不能堆到文档底部
- 推荐顺序：**标题 → 图 / grid / 画板 → 说明文字 → 判断**
- 单张截图不要默认加 `--caption`
- 多步骤流程用 2–4 张图的 `<grid>`
- 流程、时间线、架构、竞品关系优先用飞书画板，不用静态拼图替代
- `docs +media-insert` 用相对路径，执行时切到图片目录

## 相对路径提醒

```bash
# 错误
lark-cli docs +media-insert --doc "<DOC_ID>" --file "/absolute/path/shot.jpg"

# 正确
cd /path/to/images && lark-cli docs +media-insert --doc "<DOC_ID>" --file ./shot.jpg --align center
```

## 飞书不可用时的兜底

如果飞书发布开始变脆弱、混乱或权限不通，就停止在线编辑，先交付 `notes.html` 和本地证据资产。调研结果不应该依赖飞书是否发成功。
