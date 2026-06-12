#!/usr/bin/env python3
"""Extract ```sql fenced blocks from markdown into runnable SQL*Plus scripts.

- Scans ASSIGNMENT_*/Solution.md files.
- Outputs one .sql file per Solution.md.
- Skips code blocks that try to manage users/roles (CREATE USER / GRANT CONNECT).

This is intentionally simple and dependency-free.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SqlBlock:
    index: int
    body: str
    label: str | None = None


def _nearest_heading_label(lines: list[str], before_line: int) -> str | None:
    """Find the nearest markdown heading above a given line index."""

    # Scan upwards, skipping blank lines and separators.
    for i in range(before_line, -1, -1):
        raw = lines[i].rstrip("\n")
        s = raw.strip()
        if not s:
            continue
        if s in {"---", "- - -", "***"}:
            continue

        m = re.match(r"^(#{2,6})\s+(.*)$", s)
        if m:
            label = m.group(2).strip()
            # Avoid overly generic section labels.
            if label:
                return label

        # Some files use bold pseudo-headings (e.g., **(A) Insert into ...**)
        m2 = re.match(r"^\*\*(.+?)\*\*$", s)
        if m2:
            label = m2.group(1).strip()
            if label:
                return label

    return None


def iter_sql_fenced_blocks(markdown_text: str) -> list[SqlBlock]:
    """Extract SQL fenced blocks, carrying a nearby heading as a label."""

    lines = markdown_text.splitlines(True)
    blocks: list[SqlBlock] = []
    index = 0

    in_fence = False
    fence = ""
    fence_lang = ""
    fence_start_line = 0
    body_lines: list[str] = []

    for line_no, line in enumerate(lines):
        if not in_fence:
            m = re.match(r"^(```+)\s*([A-Za-z0-9_-]+)?\s*$", line.rstrip("\n"))
            if not m:
                continue
            fence = m.group(1)
            fence_lang = (m.group(2) or "").strip().lower()
            in_fence = True
            fence_start_line = line_no
            body_lines = []
            continue

        # inside fence
        if line.rstrip("\n").strip() == fence:
            # fence closes
            in_fence = False
            if fence_lang == "sql":
                index += 1
                body = "".join(body_lines).rstrip() + "\n"
                label = _nearest_heading_label(lines, fence_start_line - 1)
                blocks.append(SqlBlock(index=index, body=body, label=label))
            fence = ""
            fence_lang = ""
            body_lines = []
            continue

        body_lines.append(line)

    return blocks


def should_skip_block(sql: str) -> bool:
    # User/role management requires higher privileges and varies by environment.
    lowered = sql.lower()
    if re.search(r"\bcreate\s+user\b", lowered):
        return True
    if re.search(r"\bgrant\s+(connect|resource)\b", lowered):
        return True
    return False


def build_sqlplus_script(source_md: Path, blocks: list[SqlBlock]) -> str:
    lines: list[str] = []
    lines.append("-- Auto-generated from: %s" % source_md.as_posix())
    lines.append("set echo on")
    lines.append("set feedback on")
    lines.append("set heading on")
    lines.append("set linesize 200")
    lines.append("set pagesize 50000")
    lines.append("set long 50000")
    lines.append("set longchunksize 50000")
    lines.append("set serveroutput on")
    lines.append("set termout on")
    lines.append("whenever oserror exit 9")
    lines.append("whenever sqlerror exit sql.sqlcode rollback")
    lines.append("")

    kept = 0
    for block in blocks:
        if should_skip_block(block.body):
            continue
        kept += 1
        if block.label:
            lines.append(f"prompt \nprompt ==== {block.label} ====")
        else:
            lines.append(f"prompt \nprompt ==== Block {block.index} ====")
        lines.append(f"prompt -- BEGIN block {block.index}")
        lines.append(block.body.rstrip())
        lines.append(f"prompt -- END block {block.index}")
        lines.append("")

    if kept == 0:
        lines.append("prompt No runnable SQL blocks found (or all were skipped).")

    lines.append("exit")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Path to repository root (default: auto)",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        required=True,
        help="Output directory for generated .sql scripts",
    )
    args = parser.parse_args()

    repo_root: Path = args.repo_root
    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    md_files = sorted(repo_root.glob("ASSIGNMENT_*/Solution.md"))
    if not md_files:
        raise SystemExit("No ASSIGNMENT_*/Solution.md files found")

    for md_path in md_files:
        # Skip ASSIGNMENT_13 since it uses interactive SQL*Plus bind variables.
        if md_path.parent.name == "ASSIGNMENT_13":
            print(f"Skipping {md_path.parent.name} (interactive execution)")
            continue

        text = md_path.read_text(encoding="utf-8")
        blocks = iter_sql_fenced_blocks(text)
        script = build_sqlplus_script(md_path, blocks)

        # e.g. ASSIGNMENT_3/Solution.md -> ASSIGNMENT_3.sql
        assignment_name = md_path.parent.name
        out_path = out_dir / f"{assignment_name}.sql"
        out_path.write_text(script, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
