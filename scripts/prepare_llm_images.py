#!/usr/bin/env python3
"""
Prepare LLM-safe visual inputs for video analysis.

This script creates small JPEG derivatives under <workdir>/llm_images so agents do
not accidentally send original screenshots/contact sheets as giant base64 payloads.
Keep the original frames/screenshots as evidence; use only llm_images/* for model
or sub-agent image inputs.
"""

from __future__ import annotations

import argparse
import io
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont, ImageOps


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


try:
    RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:  # pragma: no cover - old Pillow
    RESAMPLE = Image.LANCZOS


def natural_key(path: Path) -> list[object]:
    parts = re.split(r"(\d+)", path.name)
    return [int(p) if p.isdigit() else p.lower() for p in parts]


def iter_images(path: Path) -> list[Path]:
    if not path.exists():
        return []
    return sorted(
        [p for p in path.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS],
        key=natural_key,
    )


def open_rgb(path: Path) -> Image.Image:
    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img)
        if img.mode != "RGB":
            img = img.convert("RGB")
        return img.copy()


def resize_max_edge(img: Image.Image, max_edge: int) -> Image.Image:
    w, h = img.size
    edge = max(w, h)
    if edge <= max_edge:
        return img.copy()
    scale = max_edge / edge
    return img.resize((max(1, round(w * scale)), max(1, round(h * scale))), RESAMPLE)


def jpeg_bytes(img: Image.Image, quality: int) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True, progressive=True)
    return buf.getvalue()


def save_jpeg_under_limit(
    img: Image.Image,
    out_path: Path,
    *,
    max_bytes: int,
    max_edge: int,
    start_quality: int,
) -> tuple[int, tuple[int, int], int, bool]:
    """Save JPEG, reducing quality and dimensions until it fits the byte budget."""

    out_path.parent.mkdir(parents=True, exist_ok=True)
    best: tuple[bytes, tuple[int, int], int] | None = None
    edge = max_edge

    while edge >= 560:
        candidate = resize_max_edge(img, edge)
        for quality in range(start_quality, 43, -6):
            data = jpeg_bytes(candidate, quality)
            best = (data, candidate.size, quality)
            if len(data) <= max_bytes:
                out_path.write_bytes(data)
                return len(data), candidate.size, quality, True
        edge = math.floor(edge * 0.85)

    assert best is not None
    data, size, quality = best
    out_path.write_bytes(data)
    return len(data), size, quality, len(data) <= max_bytes


def fit_letterbox(img: Image.Image, box: tuple[int, int], bg: tuple[int, int, int]) -> Image.Image:
    bw, bh = box
    img = resize_max_edge(img, max(bw, bh))
    w, h = img.size
    scale = min(bw / w, bh / h)
    resized = img.resize((max(1, round(w * scale)), max(1, round(h * scale))), RESAMPLE)
    canvas = Image.new("RGB", box, bg)
    x = (bw - resized.width) // 2
    y = (bh - resized.height) // 2
    canvas.paste(resized, (x, y))
    return canvas


def frame_label(path: Path, interval_sec: float | None) -> str:
    match = re.search(r"(\d+)(?=\D*$)", path.stem)
    if match and interval_sec:
        idx = max(0, int(match.group(1)) - 1)
        seconds = int(round(idx * interval_sec))
        return f"{seconds // 60:02d}:{seconds % 60:02d}  {path.name}"
    return path.name


def make_sheet(
    files: list[Path],
    *,
    cols: int,
    thumb_width: int,
    thumb_height: int,
    interval_sec: float | None,
) -> Image.Image:
    rows = math.ceil(len(files) / cols)
    pad = 12
    label_h = 28
    width = cols * thumb_width + (cols + 1) * pad
    height = rows * (thumb_height + label_h) + (rows + 1) * pad
    bg = (245, 247, 250)
    tile_bg = (232, 236, 242)
    sheet = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for i, path in enumerate(files):
        row, col = divmod(i, cols)
        x = pad + col * (thumb_width + pad)
        y = pad + row * (thumb_height + label_h + pad)
        try:
            img = open_rgb(path)
            tile = fit_letterbox(img, (thumb_width, thumb_height), tile_bg)
        except Exception:
            tile = Image.new("RGB", (thumb_width, thumb_height), (252, 228, 228))
            ImageDraw.Draw(tile).text((10, 10), f"failed: {path.name}", fill=(120, 0, 0), font=font)
        sheet.paste(tile, (x, y + label_h))
        draw.rectangle([x, y, x + thumb_width, y + label_h], fill=(28, 35, 45))
        draw.text((x + 8, y + 8), frame_label(path, interval_sec), fill=(255, 255, 255), font=font)

    return sheet


def sanitize_image(
    source: Path,
    dest: Path,
    *,
    max_bytes: int,
    max_edge: int,
    quality: int,
) -> dict:
    img = open_rgb(source)
    size_bytes, (w, h), used_quality, within_limit = save_jpeg_under_limit(
        img,
        dest,
        max_bytes=max_bytes,
        max_edge=max_edge,
        start_quality=quality,
    )
    return {
        "source": str(source),
        "safe_path": str(dest),
        "bytes": size_bytes,
        "width": w,
        "height": h,
        "quality": used_quality,
        "within_limit": within_limit,
    }


def batched(items: list[Path], n: int) -> Iterable[list[Path]]:
    for i in range(0, len(items), n):
        yield items[i : i + n]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", required=True, type=Path, help="Video analysis work directory.")
    parser.add_argument("--frames-dir", type=Path, help="Survey frames dir. Default: <workdir>/frames_10s")
    parser.add_argument("--selected-dir", type=Path, help="Selected screenshots dir. Default: <workdir>/selected_screenshots")
    parser.add_argument("--contact-dir", type=Path, help="Existing contact sheets dir. Default: <workdir>/contact_sheets")
    parser.add_argument("--outdir", type=Path, help="Output dir. Default: <workdir>/llm_images")
    parser.add_argument("--frame-interval-sec", type=float, default=10.0, help="Seconds between survey frames, for labels.")
    parser.add_argument("--batch-size", type=int, default=12, help="Frames per generated contact sheet.")
    parser.add_argument("--cols", type=int, default=4, help="Columns per generated contact sheet.")
    parser.add_argument("--thumb-width", type=int, default=360)
    parser.add_argument("--thumb-height", type=int, default=220)
    parser.add_argument("--max-edge", type=int, default=1600, help="Maximum long edge for safe images.")
    parser.add_argument("--max-bytes", type=int, default=350_000, help="Target max bytes per safe JPEG.")
    parser.add_argument("--quality", type=int, default=72, help="Starting JPEG quality.")
    parser.add_argument("--no-generated-sheets", action="store_true", help="Do not generate contact sheets from frames.")
    parser.add_argument("--no-selected", action="store_true", help="Do not sanitize selected screenshots.")
    parser.add_argument("--sanitize-existing-sheets", action="store_true", help="Also sanitize existing contact_sheets/* images.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workdir = args.workdir.expanduser().resolve()
    frames_dir = (args.frames_dir or workdir / "frames_10s").expanduser().resolve()
    selected_dir = (args.selected_dir or workdir / "selected_screenshots").expanduser().resolve()
    contact_dir = (args.contact_dir or workdir / "contact_sheets").expanduser().resolve()
    outdir = (args.outdir or workdir / "llm_images").expanduser().resolve()

    manifest: dict = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "policy": {
            "use_only_for_model_input": str(outdir),
            "never_use": ["raw screenshots as model input", "raw contact sheets as model input", 'detail:"original"', "pasted base64 image data"],
            "max_bytes": args.max_bytes,
            "max_edge": args.max_edge,
        },
        "items": [],
        "warnings": [],
    }

    if not args.no_generated_sheets:
        frames = iter_images(frames_dir)
        if not frames:
            manifest["warnings"].append(f"No survey frames found in {frames_dir}")
        for sheet_idx, group in enumerate(batched(frames, args.batch_size), start=1):
            sheet = make_sheet(
                group,
                cols=args.cols,
                thumb_width=args.thumb_width,
                thumb_height=args.thumb_height,
                interval_sec=args.frame_interval_sec,
            )
            dest = outdir / "contact_sheets" / f"llm_sheet_{sheet_idx:03d}.jpg"
            size_bytes, (w, h), used_quality, within_limit = save_jpeg_under_limit(
                sheet,
                dest,
                max_bytes=args.max_bytes,
                max_edge=args.max_edge,
                start_quality=args.quality,
            )
            manifest["items"].append(
                {
                    "kind": "generated_contact_sheet",
                    "safe_path": str(dest),
                    "bytes": size_bytes,
                    "width": w,
                    "height": h,
                    "quality": used_quality,
                    "within_limit": within_limit,
                    "sources": [str(p) for p in group],
                }
            )

    if args.sanitize_existing_sheets:
        for source in iter_images(contact_dir):
            dest = outdir / "contact_sheets" / f"safe_{source.stem}.jpg"
            item = sanitize_image(
                source,
                dest,
                max_bytes=args.max_bytes,
                max_edge=args.max_edge,
                quality=args.quality,
            )
            item["kind"] = "sanitized_existing_contact_sheet"
            manifest["items"].append(item)

    if not args.no_selected:
        for source in iter_images(selected_dir):
            dest = outdir / "selected_screenshots" / f"{source.stem}.jpg"
            item = sanitize_image(
                source,
                dest,
                max_bytes=args.max_bytes,
                max_edge=args.max_edge,
                quality=args.quality,
            )
            item["kind"] = "sanitized_selected_screenshot"
            manifest["items"].append(item)

    manifest_path = outdir / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    count = len(manifest["items"])
    over = [i for i in manifest["items"] if not i.get("within_limit", True)]
    print(f"Wrote {count} LLM-safe image(s) to {outdir}")
    print(f"Manifest: {manifest_path}")
    if over:
        print(f"WARNING: {len(over)} file(s) still exceed max-bytes; avoid sending them as model input.")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
