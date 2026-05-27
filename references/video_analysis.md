# 视频分析

## 0. LLM 图像输入安全（防 413）

视频分析很容易把截图 / contact sheet 以 base64 写入会话历史；一旦图片过大，后续请求会在 `aiden-aiproxy` 报 `413 Payload Too Large`。因此：

- **原始视频、原始截图、原始 contact sheet 只作为本地证据保存，不直接发给模型或子 agent。**
- **给模型看的图片必须先生成到 `<workdir>/llm_images/`，并且单张目标不超过 350 KB、长边不超过 1600 px。**
- **不要使用 `detail: "original"` 查看图片；如果工具允许选择 detail，使用默认 / high，不用 original。**
- **不要把图片手动转成 base64 粘进 prompt。**
- **子 agent 一次最多看 1–2 张 `llm_images` 里的安全图；不要一次传整批截图。**
- 如果某张安全图仍超过 350 KB，先继续压缩或切分，不要发送。

本 skill 自带压缩与 contact sheet 生成脚本：

```bash
python3 "<skill_dir>/scripts/prepare_llm_images.py" --workdir "<workdir>"
```

其中 `<skill_dir>` 是当前 skill 目录，例如 `~/.agents/skills/product-competitor-research` 或源码目录 `~/diaoyan-skill`。

## 1. 先创建持久化工作目录

建议创建类似这样的目录：

```bash
mkdir -p ~/Desktop/<product>_video_analysis/{frames_10s,contact_sheets,selected_screenshots,llm_images}
```

所有衍生素材都尽量放在这里，不要长期留在 `/tmp`。

## 2. 先全局浏览整段录屏

先看时长：

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 "<video_path>"
```

提取低频 survey frames。为减少后续图像体积，survey frame 默认不要超过 1280px 宽：

```bash
ffmpeg -i "<video_path>" -vf "fps=1/10,scale='min(1280,iw)':-2" -q:v 4 "<workdir>/frames_10s/frame_%04d.jpg"
```

如果 demo 很短，可以把频率调到 `fps=1/5`。阅读 survey frames 时建议每次看 6–8 张，重复 loading、过场或相近状态可以跳过。

### 2.1 生成 LLM-safe contact sheets

抽帧后，先生成安全图，再把 `llm_images/contact_sheets/llm_sheet_*.jpg` 给模型阅读：

```bash
python3 "<skill_dir>/scripts/prepare_llm_images.py" --workdir "<workdir>"
find "<workdir>/llm_images" -type f -name '*.jpg' -exec ls -lh {} \;
```

只使用 `llm_images/` 里的图片做视觉输入。`contact_sheets/` 和 `selected_screenshots/` 下的原始图只用于证据归档和最终报告发布，不直接发给模型。

如果要分派子 agent：

- prompt 里只写任务、原视频路径、工作目录和时间戳规则；
- 图片只附加 `llm_images/contact_sheets/llm_sheet_XXX.jpg`；
- 一次最多 1–2 张；
- 明确要求子 agent 不联网、不写总报告、不再打开原始大图；
- 禁止 `detail: "original"`。

## 3. 维护候选功能日志

对每个候选功能，至少记录：

- 暂定标题
- 时间戳或时间范围
- 观察到的 UI
- 可能对应的用户任务
- 竞争意义
- 置信度（`high` / `medium` / `low`）

在网页确认正式名称之前，可以一直使用工作标题。

## 4. 提取稳定截图，不要迷信单帧

对关键时刻，不要只依赖一个精确时间点。围绕目标时间点提取一小组截图，再选最稳的一张。

示例：

```bash
ffmpeg -ss 00:02:34 -i "<video_path>" -frames:v 1 -vf "scale='min(1600,iw)':-2" -q:v 3 "<workdir>/selected_screenshots/03_feature_t0.jpg"
```

通常围绕 `t-2s`、`t-1s`、`t`、`t+1s`、`t+2s` 各取一张，然后把最稳定的一张改名成标准文件名，例如：

```text
03_feature.jpg
```

如果一个功能跨了多个稳定 UI 状态，就保留多张图。

选好截图后，重新运行安全图生成脚本，之后只查看 `llm_images/selected_screenshots/*.jpg`：

```bash
python3 "<skill_dir>/scripts/prepare_llm_images.py" --workdir "<workdir>" --no-generated-sheets
```

## 5. 重新回看最终选中的截图

在把截图写进结论前，确认它：

- 不是过渡帧
- 不是滚动中间态
- 不是裁错状态
- 确实展示了你要描述的功能

如果依然模糊，就标记为“待核验”，并通过网页信息补充，不要直接写成确定结论。

## 6. 保留源证据

始终保留：

- 原始录屏路径
- survey frames
- contact sheets（如果生成了）
- selected screenshots
- `llm_images/manifest.json`（记录哪些安全图被生成、大小与来源）

如果无法找回原始公开视频链接，要明确写“未找回”，不要拿另一个官方 demo 冒充原始来源。
