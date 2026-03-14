#!/usr/bin/env python3
"""Download Brasil.IO company-company holdings data.

Downloads the holding.csv.gz file containing CNPJ-to-CNPJ ownership
relationships extracted from Receita Federal partner data.

Usage:
    python etl/scripts/download_holdings.py
    python etl/scripts/download_holdings.py --output-dir ./data/holdings
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import click

# Allow imports from scripts/ directory
sys.path.insert(0, str(Path(__file__).parent))
from _download_utils import download_file

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# Primary URL (Brasil.IO data bucket)
PRIMARY_URL = "https://data.brasil.io/dataset/socios-brasil/holding.csv.gz"
# Fallback URL (S3 bucket)
FALLBACK_URL = (
    "https://brasil-io-public.s3.amazonaws.com/dataset/socios-brasil/holding.csv.gz"
)


@click.command()
@click.option("--output-dir", default="./data/holdings", help="Output directory")
@click.option(
    "--skip-existing/--no-skip-existing", default=True, help="Skip existing files"
)
@click.option("--timeout", type=int, default=600, help="Download timeout in seconds")
def main(output_dir: str, skip_existing: bool, timeout: int) -> None:
    """Download Brasil.IO holdings data (company-company ownership)."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    dest = out / "holding.csv.gz"

    if skip_existing and dest.exists():
        logger.info("Skipping (exists): %s", dest.name)
        return

    logger.info("=== Downloading holdings data ===")
    if download_file(PRIMARY_URL, dest, timeout=timeout):
        logger.info("=== Done: holding.csv.gz downloaded ===")
        return

    logger.info("Primary URL unavailable, trying S3 fallback...")
    if download_file(FALLBACK_URL, dest, timeout=timeout):
        logger.info("=== Done: holding.csv.gz downloaded (from S3) ===")
        return

    logger.warning("Failed to download holdings data from both URLs")
    sys.exit(1)


if __name__ == "__main__":
    main()
