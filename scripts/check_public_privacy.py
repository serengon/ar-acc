#!/usr/bin/env python3
"""Public-surface privacy gate checks for WTG open release."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CPF_RAW_RE = re.compile(r"(?<!\d)\d{11}(?!\d)")
CPF_FMT_RE = re.compile(r"\d{3}\.\d{3}\.\d{3}-\d{2}")
FORBIDDEN_IN_PUBLIC_QUERIES = (
    ":Person",
    ":Partner",
    ".cpf",
    "doc_partial",
    "doc_raw",
)


def check_public_queries(repo_root: Path) -> list[str]:
    errors: list[str] = []
    query_dir = repo_root / "api" / "src" / "aracc" / "queries"
    for path in sorted(query_dir.glob("public_*.cypher")):
        content = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_IN_PUBLIC_QUERIES:
            if token in content:
                errors.append(f"{path}: forbidden token in public query: {token}")
    return errors


def check_demo_data(repo_root: Path) -> list[str]:
    errors: list[str] = []
    demo_dir = repo_root / "data" / "demo"
    for path in sorted(demo_dir.glob("*.json")):
        raw = path.read_text(encoding="utf-8")
        if CPF_RAW_RE.search(raw) or CPF_FMT_RE.search(raw):
            errors.append(f"{path}: possible CPF-like value found")
        payload = json.loads(raw)
        for node in payload.get("nodes", []):
            label = str(node.get("type", ""))
            if label in {"Person", "Partner"}:
                errors.append(f"{path}: forbidden demo label {label}")
            props = node.get("properties", {})
            if isinstance(props, dict):
                lowered = {str(k).lower() for k in props.keys()}
                if "cpf" in lowered or "doc_partial" in lowered or "doc_raw" in lowered:
                    errors.append(f"{path}: forbidden personal key in demo node")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Run public privacy checks")
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root path",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    errors = [
        *check_public_queries(repo_root),
        *check_demo_data(repo_root),
    ]
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
