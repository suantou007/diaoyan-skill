# 飞书发布

默认优先发布到飞书，并对所有 create / update 操作使用 **`--as user`**。

前提是：本地报告资产已经完成。

## 推荐工作流

1. 先在本地完成分析
2. 图片上传一次并拿到 token
3. 在本地组装最终 Markdown / XML 布局
4. 尽量用少量写操作创建或覆盖文档
5. 最后检查渲染结果

不要把飞书文档当成工作草稿。

## 默认规则

- 默认对所有飞书创建 / 更新操作显式传 `--as user`
- 优先用 token-first 和最终布局重建，不要默认走反复 append 的方式
- 截图默认**不要**用 `--caption`，否则容易在图片下方出现不想要的白边 / 留白
- 如果需要图片说明，直接把说明写成图片下方普通文本
- 如果使用 `docs +media-insert`，文件路径必须是**相对路径**，并且命令执行时 `cwd` 要切到图片目录

## 相对路径提醒

```bash
# 错误
lark-cli docs +media-insert --doc "<DOC_ID>" --file "/absolute/path/shot.jpg"

# 更稳妥
cd /path/to/images && lark-cli docs +media-insert --doc "<DOC_ID>" --file ./shot.jpg --align center
```

## 飞书不可用时的兜底

如果当前环境无法正常输出飞书，或者发布过程开始变脆弱、混乱或难以维护，就停止在线编辑，先交付 `notes.html` 和本地证据资产。调研结果本身不应该依赖飞书是否发成功。

## 报告结构参考

如果要做一份给同事 / 老板看的正式报告，在本地 evidence assets 完成后，再参考 [reference_doc_structure.md](reference_doc_structure.md)。
