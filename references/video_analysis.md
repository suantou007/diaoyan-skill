# Video analysis

## 1. Create a persistent work folder

Prefer a folder such as:

```bash
mkdir -p ~/Desktop/<product>_video_analysis/{frames_10s,contact_sheets,selected_screenshots}
```

Keep all derived assets there rather than leaving them in `/tmp`.

## 2. Survey the whole recording first

Check duration:

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 "<video_path>"
```

Extract low-frequency survey frames:

```bash
ffmpeg -i "<video_path>" -vf "fps=1/10,scale=1280:-1" -q:v 3 "<workdir>/frames_10s/frame_%04d.jpg"
```

Use `fps=1/5` for a very short demo if needed. Read survey frames in batches of 6–8 and skip repetitive loading or transition states.

## 3. Keep a candidate feature log

For each candidate feature, record:

- working title
- timestamp or range
- observed UI
- likely user task
- competitive significance
- confidence (`high` / `medium` / `low`)

Use working titles until the official name is verified on the web.

## 4. Extract stable screenshots, not brittle singles

For a key moment, extract a small burst around the target timestamp rather than trusting one exact frame.

Example pattern:

```bash
ffmpeg -ss 00:02:34 -i "<video_path>" -frames:v 1 -q:v 2 "<workdir>/selected_screenshots/03_feature_t0.jpg"
```

Repeat around roughly `t-2s`, `t-1s`, `t`, `t+1s`, and `t+2s`, then keep the most stable image and rename it to the canonical filename, for example:

```text
03_feature.jpg
```

Use multiple screenshots when a feature spans more than one settled UI state.

## 5. Re-read the chosen image

Before using a screenshot in conclusions, confirm it is:

- not a transition frame
- not mid-scroll
- not cropped at the wrong state
- actually showing the feature being described

If the feature is still ambiguous, mark it as ambiguous and verify it on the web before writing a strong claim.

## 6. Preserve source evidence

Always keep:

- original recording path
- survey frames
- contact sheets if created
- selected screenshots

If the original public URL cannot be recovered, say so explicitly instead of substituting a different official demo.
