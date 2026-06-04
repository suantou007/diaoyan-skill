#!/usr/bin/env python3
"""
Insert document images into Feishu with retry and post-insert validation.

The current `lark-cli docs +media-insert` path can occasionally return empty
JSON or transient errors while the document may or may not have actually been
updated. This helper wraps the command with:

- deterministic per-image insertion plans
- retries with backoff
- validation via `docs +fetch` after each attempt
- optional summary JSON for debugging
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class PlanItemResult:
    file: str
    status: str
    attempts: int
    anchor: str | None
    image_name: str
    existing_before: int
    existing_after: int
    message: str
    command_stdout: str | None = None
    command_stderr: str | None = None
    parsed_response: dict[str, Any] | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path, help="Insertion plan JSON path.")
    parser.add_argument("--summary-out", type=Path, help="Optional path for JSON summary.")
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=None,
        help="Override plan max_attempts.",
    )
    parser.add_argument(
        "--validate-polls",
        type=int,
        default=None,
        help="Override plan validate_polls.",
    )
    parser.add_argument(
        "--validate-wait-sec",
        type=float,
        default=None,
        help="Override plan validate_wait_sec.",
    )
    parser.add_argument(
        "--backoff-sec",
        type=float,
        default=None,
        help="Override plan retry backoff in seconds.",
    )
    return parser.parse_args()


def read_plan(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def resolve_path(raw: str, base_dir: Path) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = (base_dir / path).resolve()
    return path


def run_cmd(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def fetch_doc_content(doc_id: str, cwd: Path) -> str:
    proc = run_cmd(
        [
            "lark-cli",
            "docs",
            "+fetch",
            "--api-version",
            "v2",
            "--as",
            "user",
            "--doc",
            doc_id,
        ],
        cwd,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"docs +fetch failed: {proc.stderr.strip() or proc.stdout.strip()}")
    payload = json.loads(proc.stdout)
    return payload["data"]["document"]["content"]


def count_images(doc_content: str, image_name: str) -> int:
    pattern = re.compile(rf'<img\b[^>]*\bname="{re.escape(image_name)}"')
    return len(pattern.findall(doc_content))


def parse_json_stdout(stdout: str) -> dict[str, Any] | None:
    stdout = stdout.strip()
    if not stdout:
        return None
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return None


def validate_insert(
    *,
    doc_id: str,
    cwd: Path,
    image_name: str,
    previous_count: int,
    validate_polls: int,
    validate_wait_sec: float,
) -> tuple[bool, int]:
    for poll in range(validate_polls):
        if poll > 0:
            time.sleep(validate_wait_sec)
        content = fetch_doc_content(doc_id, cwd)
        current_count = count_images(content, image_name)
        if current_count > previous_count:
            return True, current_count
    return False, previous_count


def build_insert_cmd(
    *,
    doc_id: str,
    rel_file: str,
    item: dict[str, Any],
) -> list[str]:
    cmd = [
        "lark-cli",
        "docs",
        "+media-insert",
        "--as",
        "user",
        "--doc",
        doc_id,
        "--file",
        rel_file,
        "--align",
        item.get("align", "center"),
    ]
    if item.get("selection"):
        cmd.extend(["--selection-with-ellipsis", item["selection"]])
    if item.get("before"):
        cmd.append("--before")
    if item.get("caption"):
        cmd.extend(["--caption", item["caption"]])
    if item.get("width"):
        cmd.extend(["--width", str(item["width"])])
    if item.get("height"):
        cmd.extend(["--height", str(item["height"])])
    return cmd


def insert_one(
    *,
    doc_id: str,
    base_dir: Path,
    cwd: Path,
    item: dict[str, Any],
    max_attempts: int,
    validate_polls: int,
    validate_wait_sec: float,
    backoff_sec: float,
) -> PlanItemResult:
    image_path = resolve_path(item["file"], base_dir)
    if not image_path.exists():
        return PlanItemResult(
            file=item["file"],
            status="failed",
            attempts=0,
            anchor=item.get("selection"),
            image_name=image_path.name,
            existing_before=0,
            existing_after=0,
            message=f"Image not found: {image_path}",
        )

    rel_file = os.path.relpath(image_path, cwd)
    before_content = fetch_doc_content(doc_id, cwd)
    existing_before = count_images(before_content, image_path.name)
    if existing_before > 0 and item.get("skip_if_exists", True):
        return PlanItemResult(
            file=item["file"],
            status="skipped",
            attempts=0,
            anchor=item.get("selection"),
            image_name=image_path.name,
            existing_before=existing_before,
            existing_after=existing_before,
            message="Image already exists in document.",
        )

    last_stdout: str | None = None
    last_stderr: str | None = None
    last_json: dict[str, Any] | None = None
    current_count = existing_before

    for attempt in range(1, max_attempts + 1):
        cmd = build_insert_cmd(doc_id=doc_id, rel_file=rel_file, item=item)
        proc = run_cmd(cmd, cwd)
        last_stdout = proc.stdout.strip() or None
        last_stderr = proc.stderr.strip() or None
        last_json = parse_json_stdout(proc.stdout)

        inserted, validated_count = validate_insert(
            doc_id=doc_id,
            cwd=cwd,
            image_name=image_path.name,
            previous_count=current_count,
            validate_polls=validate_polls,
            validate_wait_sec=validate_wait_sec,
        )
        if inserted:
            message = "Inserted and validated."
            if proc.returncode != 0:
                message = "Validated after a command-level failure."
            elif last_json is None:
                message = "Validated after a non-JSON/empty response."
            return PlanItemResult(
                file=item["file"],
                status="inserted",
                attempts=attempt,
                anchor=item.get("selection"),
                image_name=image_path.name,
                existing_before=existing_before,
                existing_after=validated_count,
                message=message,
                command_stdout=last_stdout,
                command_stderr=last_stderr,
                parsed_response=last_json,
            )

        if attempt < max_attempts:
            time.sleep(backoff_sec * attempt)

    return PlanItemResult(
        file=item["file"],
        status="failed",
        attempts=max_attempts,
        anchor=item.get("selection"),
        image_name=image_path.name,
        existing_before=existing_before,
        existing_after=current_count,
        message="All retry attempts exhausted without validation.",
        command_stdout=last_stdout,
        command_stderr=last_stderr,
        parsed_response=last_json,
    )


def main() -> int:
    args = parse_args()
    plan_path = args.plan.expanduser().resolve()
    plan = read_plan(plan_path)

    base_dir = plan_path.parent
    cwd = resolve_path(plan.get("cwd", "."), base_dir)
    doc_id = plan["doc_id"]
    max_attempts = args.max_attempts or plan.get("max_attempts", 4)
    validate_polls = args.validate_polls or plan.get("validate_polls", 3)
    validate_wait_sec = args.validate_wait_sec or plan.get("validate_wait_sec", 1.5)
    backoff_sec = args.backoff_sec or plan.get("backoff_sec", 2.0)

    results: list[PlanItemResult] = []
    for item in plan.get("items", []):
        result = insert_one(
            doc_id=doc_id,
            base_dir=base_dir,
            cwd=cwd,
            item=item,
            max_attempts=max_attempts,
            validate_polls=validate_polls,
            validate_wait_sec=validate_wait_sec,
            backoff_sec=backoff_sec,
        )
        results.append(result)

    summary = {
        "doc_id": doc_id,
        "cwd": str(cwd),
        "max_attempts": max_attempts,
        "validate_polls": validate_polls,
        "validate_wait_sec": validate_wait_sec,
        "backoff_sec": backoff_sec,
        "results": [asdict(result) for result in results],
        "ok": all(result.status in {"inserted", "skipped"} for result in results),
        "inserted_count": sum(result.status == "inserted" for result in results),
        "failed_count": sum(result.status == "failed" for result in results),
        "skipped_count": sum(result.status == "skipped" for result in results),
    }

    summary_text = json.dumps(summary, ensure_ascii=False, indent=2)
    if args.summary_out:
        args.summary_out.expanduser().resolve().write_text(summary_text + "\n", encoding="utf-8")
    print(summary_text)
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
