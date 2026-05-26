#!/usr/bin/env python3
"""
Template for building a Lark doc whose screenshots stay aligned with feature text.

Usage:
  1. Set DOC_ID to the target document token
  2. Set IMG_DIR to the directory containing screenshots
  3. Populate FEATURES
  4. Run: python3 build_script_template.py
"""

from __future__ import annotations

import html
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

DOC_ID = "YOUR_DOC_ID_HERE"
IMG_DIR = Path("/path/to/your/images")

FEATURES = [
    {
        "slug": "storyboard_generation",
        "title": "Storyboard-driven generation",
        "description": "2-4 sentences describing what this feature does, how it appears in the UI, and why it matters competitively.",
        "image": "01_storyboard_generation.jpg",
        "caption": "Storyboard-driven generation UI",
        "highlight": True,
    },
]

HEADER_CALLOUT = """<callout emoji="bulb" background-color="light-orange">
**Competitor / Product Analysis**

- **One-line positioning:** ...
- **Core highlights:** ...
- **Key gaps or risks:** ...
</callout>"""

SUMMARY_CALLOUT = """<callout emoji="pin" background-color="light-green">
**Key Takeaways**

- **Takeaway 1:** ...
- **Takeaway 2:** ...
</callout>"""


def image_anchor(slug: str) -> str:
    return f"【IMG_ANCHOR:{slug}】"


def extract_json(text: str) -> dict | None:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip().startswith("{"):
            candidate = "\n".join(lines[index:])
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                continue
    return None


def run_lark(args: list[str], *, cwd: Path | None = None) -> dict:
    result = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        check=False,
    )
    combined = "\n".join(part for part in [result.stdout, result.stderr] if part)
    data = extract_json(combined)

    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed ({result.returncode}): {' '.join(args)}\n{combined[-1200:]}"
        )
    if data and data.get("ok") is False:
        raise RuntimeError(f"lark-cli returned ok=false: {json.dumps(data, ensure_ascii=False)[:1200]}")
    return data or {"raw_output": combined.strip()}


def update_doc(mode: str, markdown: str) -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as handle:
        handle.write(markdown)
        markdown_path = Path(handle.name)

    try:
        return run_lark(
            [
                "lark-cli",
                "docs",
                "+update",
                "--api-version",
                "v2",
                "--doc",
                DOC_ID,
                "--mode",
                mode,
                "--markdown",
                f"@{markdown_path}",
            ]
        )
    finally:
        markdown_path.unlink(missing_ok=True)


def insert_image(filename: str, anchor: str, caption: str) -> dict:
    path = Path(filename)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Image filename must be relative to IMG_DIR: {filename}")
    if not (IMG_DIR / filename).exists():
        raise FileNotFoundError(IMG_DIR / filename)

    return run_lark(
        [
            "lark-cli",
            "docs",
            "+media-insert",
            "--doc",
            DOC_ID,
            "--file",
            f"./{filename}",
            "--selection-with-ellipsis",
            anchor,
            "--align",
            "center",
            "--caption",
            caption,
        ],
        cwd=IMG_DIR,
    )


def build_feature_table(features: list[dict]) -> str:
    rows = [
        '<lark-table rows="{}" cols="3" column-widths="160,360,260">'.format(len(features) + 1),
        "  <lark-tr>",
        "    <lark-td>**功能**</lark-td>",
        "    <lark-td>**功能描述**</lark-td>",
        "    <lark-td>**图片/视频示意**</lark-td>",
        "  </lark-tr>",
    ]

    for feature in features:
        title = html.escape(feature["title"])
        if feature.get("highlight"):
            title = f'<text bgcolor="light-yellow">{title}</text>'
        description = html.escape(feature["description"])
        anchor = image_anchor(feature["slug"])
        rows.extend(
            [
                "  <lark-tr>",
                f"    <lark-td>{title}</lark-td>",
                f"    <lark-td>{description}</lark-td>",
                f"    <lark-td>{anchor}</lark-td>",
                "  </lark-tr>",
            ]
        )

    rows.append("</lark-table>")
    return "\n".join(rows)


def build_document() -> str:
    return f"""{HEADER_CALLOUT}

---

## 产品介绍

### 核心功能

{build_feature_table(FEATURES)}

---

{SUMMARY_CALLOUT}
"""


def validate_config() -> None:
    if DOC_ID == "YOUR_DOC_ID_HERE":
        raise ValueError("Set DOC_ID before running the script.")
    if not IMG_DIR.exists():
        raise FileNotFoundError(IMG_DIR)
    slugs = [feature["slug"] for feature in FEATURES]
    if len(slugs) != len(set(slugs)):
        raise ValueError("Feature slugs must be unique because they are used as image anchors.")
    for feature in FEATURES:
        for key in ["slug", "title", "description", "image", "caption"]:
            if not feature.get(key):
                raise ValueError(f"Missing {key} in feature: {feature}")
        image_path = Path(feature["image"])
        if image_path.is_absolute() or ".." in image_path.parts:
            raise ValueError(f"Feature image must be relative to IMG_DIR: {feature['image']}")
        if not (IMG_DIR / feature["image"]).exists():
            raise FileNotFoundError(IMG_DIR / feature["image"])


def main() -> None:
    validate_config()

    print("Writing document skeleton with image anchors...")
    update_doc("overwrite", build_document())
    time.sleep(0.5)

    for index, feature in enumerate(FEATURES, start=1):
        anchor = image_anchor(feature["slug"])
        print(f"[{index}/{len(FEATURES)}] inserting {feature['image']} at {anchor}")
        insert_image(feature["image"], anchor, feature["caption"])
        time.sleep(0.4)

    print("Done. Open the document and verify each screenshot is next to the matching feature text.")
    print(f"Doc: https://www.feishu.cn/docx/{DOC_ID}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
