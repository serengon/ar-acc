#!/usr/bin/env python3
"""Download Senado Federal CEAPS expense data.

Usage:
    python etl/scripts/download_senado.py
    python etl/scripts/download_senado.py --years 2023,2024
    python etl/scripts/download_senado.py --output-dir ./data/senado
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path

import click

sys.path.insert(0, str(Path(__file__).parent))
from _download_utils import download_file, validate_csv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BASE_URL = "https://www.senado.leg.br/transparencia/LAI/verba/{year}.csv"


@click.command()
@click.option(
    "--years",
    default=lambda: ",".join(str(y) for y in range(2008, datetime.now().year + 1)),
    help="Comma-separated years to download (default: 2008-current)",
)
@click.option("--output-dir", default="./data/senado", help="Output directory")
@click.option("--skip-existing/--no-skip-existing", default=True, help="Skip existing files")
@click.option("--timeout", type=int, default=300, help="Download timeout in seconds")
def main(years: str, output_dir: str, skip_existing: bool, timeout: int) -> None:
    """Download CEAPS expense data from Senado Federal."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    year_list = [y.strip() for y in years.split(",")]
    success_count = 0

    for year in year_list:
        logger.info("=== Year %s ===", year)
        url = BASE_URL.format(year=year)
        dest = out / f"{year}.csv"

        if skip_existing and dest.exists():
            logger.info("Skipping (exists): %s", dest.name)
            success_count += 1
            continue

        if download_file(url, dest, timeout=timeout):
            validate_csv(dest, encoding="latin-1", sep=";")
            success_count += 1
        else:
            logger.warning("Failed to download year %s", year)

    logger.info("=== Done: %d/%d years downloaded ===", success_count, len(year_list))
    if success_count == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
