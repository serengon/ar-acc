#!/usr/bin/env python3
"""Download Camara dos Deputados CEAP expense data.

Usage:
    python etl/scripts/download_camara.py
    python etl/scripts/download_camara.py --years 2023,2024
    python etl/scripts/download_camara.py --output-dir ./data/camara
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path

import click

sys.path.insert(0, str(Path(__file__).parent))
from _download_utils import download_file, extract_zip, validate_csv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BASE_URL = "https://www.camara.leg.br/cotas/Ano-{year}.csv.zip"


@click.command()
@click.option(
    "--years",
    default=lambda: ",".join(str(y) for y in range(2009, datetime.now().year + 1)),
    help="Comma-separated years to download (default: 2009-current)",
)
@click.option("--output-dir", default="./data/camara", help="Output directory")
@click.option("--skip-existing/--no-skip-existing", default=True, help="Skip existing files")
@click.option("--timeout", type=int, default=300, help="Download timeout in seconds")
def main(years: str, output_dir: str, skip_existing: bool, timeout: int) -> None:
    """Download CEAP expense data from Camara dos Deputados."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    raw_dir = out / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    year_list = [y.strip() for y in years.split(",")]
    success_count = 0

    for year in year_list:
        logger.info("=== Year %s ===", year)
        url = BASE_URL.format(year=year)
        zip_path = raw_dir / f"Ano-{year}.csv.zip"
        csv_dest = out / f"Ano-{year}.csv"

        if skip_existing and csv_dest.exists():
            logger.info("Skipping (exists): %s", csv_dest.name)
            success_count += 1
            continue

        if not download_file(url, zip_path, timeout=timeout):
            logger.warning("Failed to download year %s", year)
            continue

        extracted = extract_zip(zip_path, raw_dir)
        if not extracted:
            continue

        # Find the extracted CSV
        csv_file = None
        for f in extracted:
            if f.suffix.lower() == ".csv":
                csv_file = f
                break

        if csv_file is None:
            logger.warning("No CSV found in ZIP for year %s", year)
            continue

        # Move to final location
        csv_file.rename(csv_dest)
        validate_csv(csv_dest, encoding="latin-1", sep=";")
        success_count += 1

    logger.info("=== Done: %d/%d years downloaded ===", success_count, len(year_list))
    if success_count == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
