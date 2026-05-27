# 视频分析

## 1. 先创建持久化工作目录

建议创建类似这样的目录：

```bash
mkdir -p ~/Desktop/<product>_video_analysis/{frames_10s,contact_sheets,selected_screenshots}
```

所有衍生素材都尽量放在这里，不要长期留在 `/tmp`。

## 2. 先全局浏览整段录屏

先看时长：

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 "<video_path>"
```

提取低频 survey frames：

```bash
ffmpeg -i "<video_path>" -vf "fps=1/10,scale=1280:-1" -q:v 3 "<workdir>/frames_10s/frame_%04d.jpg"
```

如果 demo 很短，可以把频率调到 `fps=1/5`。阅读 survey frames 时建议每次看 6–8 张，重复 loading、过场或相近状态可以跳过。

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
ffmpeg -ss 00:02:34 -i "<video_path>" -frames:v 1 -q:v 2 "<workdir>/selected_screenshots/03_feature_t0.jpg"
```

通常围绕 `t-2s`、`t-1s`、`t`、`t+1s`、`t+2s` 各取一张，然后把最稳定的一张改名成标准文件名，例如：

```text
03_feature.jpg
```

如果一个功能跨了多个稳定 UI 状态，就保留多张图。

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

如果无法找回原始公开视频链接，要明确写“未找回”，不要拿另一个官方 demo 冒充原始来源。
