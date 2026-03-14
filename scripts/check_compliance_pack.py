#!/usr/bin/env python3
"""Compliance pack gate for legal and ethics baseline."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_FILES = [
    "ETHICS.md",
    "LGPD.md",
    "PRIVACY.md",
    "TERMS.md",
    "DISCLAIMER.md",
    "SECURITY.md",
    "ABUSE_RESPONSE.md",
    "docs/legal/legal-index.md",
]

REQUIRED_SECTIONS: dict[str, list[str]] = {
    "ETHICS.md": [
        "## Mission and public-interest framing",
        "## Prohibited uses",
        "## Human-review requirement for high-risk allegations",
        "## Non-accusatory language standard",
    ],
    "LGPD.md": [
        "## Legal basis posture",
        "## Data categories and exclusions",
        "## Data subject rights workflow",
        "## Retention and deletion principles",
        "## Cross-border processing note",
    ],
    "PRIVACY.md": [
        "## What telemetry and logs are collected",
        "## What is not collected",
        "## Retention windows and access controls",
        "## Abuse investigation logging statement",
    ],
    "TERMS.md": [
        "## Acceptable use",
        "## Limitation of liability",
        "## No legal accusation guarantee",
        "## Enforcement actions and suspension",
    ],
    "DISCLAIMER.md": [
        "## Patterns are signals, not proof",
        "## Source quality limitations and false-positive caveat",
        "## Temporal and identity confidence caveat",
    ],
    "SECURITY.md": [
        "## Reporting vulnerabilities",
        "## Supported versions",
        "## Disclosure SLA targets",
    ],
    "ABUSE_RESPONSE.md": [
        "## Incident severity matrix",
        "## Triage and response actions",
        "## Escalation path and evidence retention",
    ],
    "docs/legal/legal-index.md": [
        "## Core policies",
        "## Applicability by deployment model",
        "## Change log policy",
    ],
}

README_REQUIRED_LINKS = [
    "ETHICS.md",
    "LGPD.md",
    "PRIVACY.md",
    "TERMS.md",
    "DISCLAIMER.md",
    "SECURITY.md",
    "ABUSE_RESPONSE.md",
]


def _extract_links(markdown_text: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", markdown_text)


def _exists(repo_root: Path, rel_path: str) -> bool:
    return (repo_root / rel_path).exists()


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate compliance pack baseline")
    parser.add_argument("--repo-root", default=".", help="Repository root")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    errors: list[str] = []

    for rel_path in REQUIRED_FILES:
        if not _exists(repo_root, rel_path):
            errors.append(f"Missing required file: {rel_path}")

    for rel_path, sections in REQUIRED_SECTIONS.items():
        full_path = repo_root / rel_path
        if not full_path.exists():
            continue
        content = full_path.read_text(encoding="utf-8")
        for section in sections:
            if section not in content:
                errors.append(f"{rel_path}: missing section header: {section}")

    legal_index = repo_root / "docs" / "legal" / "legal-index.md"
    if legal_index.exists():
        links = _extract_links(legal_index.read_text(encoding="utf-8"))
        for rel_path in [
            "../../ETHICS.md",
            "../../LGPD.md",
            "../../PRIVACY.md",
            "../../TERMS.md",
            "../../DISCLAIMER.md",
            "../../SECURITY.md",
            "../../ABUSE_RESPONSE.md",
            "./public-compliance-pack.md",
        ]:
            if rel_path not in links:
                errors.append(f"docs/legal/legal-index.md: missing link: {rel_path}")
        for rel_link in links:
            target = (legal_index.parent / rel_link).resolve()
            if rel_link.startswith("http"):
                continue
            if not target.exists():
                errors.append(
                    "docs/legal/legal-index.md: broken link target: "
                    f"{rel_link}"
                )

    readme = repo_root / "README.md"
    if readme.exists():
        readme_content = readme.read_text(encoding="utf-8")
        links = _extract_links(readme_content)
        if "## Legal & Ethics" not in readme_content:
            errors.append("README.md: missing section header: ## Legal & Ethics")
        for rel_path in README_REQUIRED_LINKS:
            if rel_path not in links:
                errors.append(f"README.md: missing legal link: {rel_path}")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
