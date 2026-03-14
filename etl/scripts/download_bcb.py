#!/usr/bin/env python3
"""Download BCB (Banco Central do Brasil) penalties data.

Usage:
    python etl/scripts/download_bcb.py
    python etl/scripts/download_bcb.py --output-dir ./data/bcb
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import click
import pandas as pd

# Allow imports from scripts/ directory
sys.path.insert(0, str(Path(__file__).parent))
from _download_utils import download_file, validate_csv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# BCB penalties ranking (tipo=2 = penalties)
BCB_URL = "https://www3.bcb.gov.br/rdrweb/rest/ext/ranking/arquivo?tipo=2"

EXPECTED_COLUMNS = [
    "CNPJ",
    "Nome Instituição",
    "Tipo Penalidade",
    "Valor Penalidade",
    "Número Processo",
    "Data Decisão",
]


def _download_penalties(output_dir: Path, *, skip_existing: bool, timeout: int) -> Path | None:
    """Download BCB penalties CSV."""
    raw_dir = output_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    csv_path = raw_dir / "penalidades_raw.csv"

    if skip_existing and csv_path.exists():
        logger.info("Skipping (exists): %s", csv_path.name)
        return csv_path

    if not download_file(BCB_URL, csv_path, timeout=timeout):
        logger.warning("Failed to download from BCB. Try downloading manually.")
        return None

    validate_csv(csv_path, encoding="latin-1", sep=";")
    return csv_path


def _process_csv(csv_path: Path, output_path: Path) -> bool:
    """Read raw CSV, validate columns, write pipeline-ready CSV."""
    try:
        df = pd.read_csv(
            csv_path,
            sep=";",
            encoding="latin-1",
            dtype=str,
            keep_default_na=False,
        )
    except Exception as e:
        logger.warning("Failed to read %s: %s", csv_path, e)
        return False

    logger.info("BCB penalties: %d rows, columns: %s", len(df), list(df.columns))

    # Validate expected columns are present
    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing:
        logger.warning("BCB penalties: missing expected columns: %s", missing)

    df.to_csv(output_path, sep=";", index=False, encoding="latin-1")
    logger.info("Wrote %d rows to %s", len(df), output_path)
    return True


@click.command()
@click.option("--output-dir", default="./data/bcb", help="Output directory")
@click.option("--skip-existing/--no-skip-existing", default=True, help="Skip existing files")
@click.option("--timeout", type=int, default=300, help="Download timeout in seconds")
def main(output_dir: str, skip_existing: bool, timeout: int) -> None:
    """Download BCB penalties data."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    logger.info("=== BCB Penalties ===")
    csv_path = _download_penalties(out, skip_existing=skip_existing, timeout=timeout)
    if csv_path is None:
        logger.warning("Failed to download BCB penalties")
        sys.exit(1)

    output_path = out / "penalidades.csv"
    if not _process_csv(csv_path, output_path):
        sys.exit(1)

    logger.info("=== Done ===")


if __name__ == "__main__":
    main()
