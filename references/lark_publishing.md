# Lark 发布

只有在**本地 research package 已经完成**后，才开始发布到 Lark。

## 推荐工作流

1. 先在本地完成分析
2. 图片上传一次并拿到 token
3. 在本地组装最终 Markdown / XML 布局
4. 尽量用少量写操作创建或覆盖文档
5. 最后检查渲染结果

不要把 Lark 文档当成工作草稿。

## 默认规则

- 如果用户要求用自己的身份，显式传 `--as user`
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

## 发布失败时的兜底

如果发布过程开始变脆弱、混乱或难以维护，就停止在线编辑，先交付本地 package。调研结果本身不应该依赖文档是否发成功。

## 报告结构参考

如果要做一份给同事 / 老板看的正式报告，在本地 evidence package 完成后，再参考 [reference_doc_structure.md](reference_doc_structure.md)。
