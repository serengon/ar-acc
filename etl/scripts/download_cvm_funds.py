#!/usr/bin/env python3
"""Download CVM fund registry data (cad_fi.csv).

Usage:
    python etl/scripts/download_cvm_funds.py
    python etl/scripts/download_cvm_funds.py --output-dir ./data/cvm_funds
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import click

sys.path.insert(0, str(Path(__file__).parent))
from _download_utils import download_file, validate_csv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# CVM Dados Abertos — Fund registry (cad_fi.csv)
CAD_FI_URL = "https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv"


@click.command()
@click.option("--output-dir", default="./data/cvm_funds", help="Output directory")
@click.option("--skip-existing/--no-skip-existing", default=True, help="Skip existing files")
@click.option("--timeout", type=int, default=300, help="Download timeout in seconds")
def main(output_dir: str, skip_existing: bool, timeout: int) -> None:
    """Download CVM fund registry data."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    dest = out / "cad_fi.csv"
    if skip_existing and dest.exists():
        logger.info("Skipping (already exists): %s", dest)
        return

    logger.info("=== Downloading cad_fi.csv ===")
    if not download_file(CAD_FI_URL, dest, timeout=timeout):
        logger.error("Failed to download cad_fi.csv")
        sys.exit(1)

    validate_csv(dest, encoding="latin-1", sep=";")
    logger.info("=== Done ===")


if __name__ == "__main__":
    main()
