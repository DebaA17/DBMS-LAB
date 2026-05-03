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


FENCE_RE = re.compile(
    r"(?sm)^(?P<fence>```+)\s*(?P<lang>[A-Za-z0-9_-]+)?\s*\n(?P<body>.*?)\n(?P=fence)\s*$"
)


@dataclass(frozen=True)
class SqlBlock:
    index: int
    body: str


def iter_sql_fenced_blocks(markdown_text: str) -> list[SqlBlock]:
    blocks: list[SqlBlock] = []
    index = 0
    for m in FENCE_RE.finditer(markdown_text):
        lang = (m.group("lang") or "").strip().lower()
        if lang != "sql":
            continue
        index += 1
        body = m.group("body").rstrip() + "\n"
        blocks.append(SqlBlock(index=index, body=body))
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
