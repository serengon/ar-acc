#!/usr/bin/env python3
"""Generate a public-safe synthetic graph dataset for WTG demo."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path


def build_payload() -> dict[str, object]:
    nodes = [
        {
            "id": "company:alpha",
            "label": "Alpha Infra Ltda",
            "type": "Company",
            "properties": {
                "cnpj": "11.111.111/0001-11",
                "sector": "infrastructure",
                "city": "Sao Paulo",
            },
        },
        {
            "id": "company:beta",
            "label": "Beta Servicos SA",
            "type": "Company",
            "properties": {
                "cnpj": "22.222.222/0001-22",
                "sector": "services",
                "city": "Recife",
            },
        },
        {
            "id": "contract:001",
            "label": "Contrato Municipal 001",
            "type": "Contract",
            "properties": {
                "contract_id": "CT-001",
                "value": 1250000,
                "date": "2025-11-10",
            },
        },
        {
            "id": "sanction:001",
            "label": "Sancao Administrativa 001",
            "type": "Sanction",
            "properties": {
                "sanction_id": "SN-001",
                "date": "2025-08-12",
            },
        },
        {
            "id": "finance:001",
            "label": "Debito Fiscal 001",
            "type": "Finance",
            "properties": {
                "finance_id": "FN-001",
                "value": 320000,
                "date": "2025-09-03",
            },
        },
    ]

    edges = [
        {
            "id": "rel:1",
            "source": "company:alpha",
            "target": "contract:001",
            "type": "VENCEU",
            "properties": {"source": "synthetic"},
        },
        {
            "id": "rel:2",
            "source": "company:alpha",
            "target": "sanction:001",
            "type": "SANCIONADA",
            "properties": {"source": "synthetic"},
        },
        {
            "id": "rel:3",
            "source": "company:alpha",
            "target": "finance:001",
            "type": "DEVE",
            "properties": {"source": "synthetic"},
        },
        {
            "id": "rel:4",
            "source": "company:alpha",
            "target": "company:beta",
            "type": "SOCIO_DE",
            "properties": {"source": "synthetic", "note": "company-level relation"},
        },
    ]

    return {
        "meta": {
            "generated_at_utc": datetime.now(UTC).isoformat(),
            "generator_version": "1.0.0",
            "source": "synthetic",
        },
        "nodes": nodes,
        "edges": edges,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate synthetic graph demo dataset")
    parser.add_argument(
        "--output",
        default="data/demo/synthetic_graph.json",
        help="Output path for synthetic dataset",
    )
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_payload()
    output_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote synthetic dataset to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
