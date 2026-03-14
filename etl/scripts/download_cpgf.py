#!/usr/bin/env python3
"""Download CPGF (government credit card expense) data from Portal da Transparencia.

Usage:
    python etl/scripts/download_cpgf.py
    python etl/scripts/download_cpgf.py --start-year 2020 --end-year 2025
    python etl/scripts/download_cpgf.py --output-dir ./data/cpgf
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

BASE_URL = "https://portaldatransparencia.gov.br/download-de-dados/cpgf"


def _generate_months(start_year: int, end_year: int) -> list[str]:
    """Generate YYYYMM strings for each month in the range."""
    now = datetime.now()
    months: list[str] = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            if year == now.year and month > now.month:
                break
            months.append(f"{year}{month:02d}")
    return months


@click.command()
@click.option(
    "--start-year",
    type=int,
    default=lambda: datetime.now().year - 1,
    help="Start year (default: previous year)",
)
@click.option(
    "--end-year",
    type=int,
    default=lambda: datetime.now().year,
    help="End year (default: current year)",
)
@click.option("--output-dir", default="./data/cpgf", help="Output directory")
@click.option("--skip-existing/--no-skip-existing", default=True, help="Skip existing files")
@click.option("--timeout", type=int, default=600, help="Download timeout in seconds")
def main(
    start_year: int,
    end_year: int,
    output_dir: str,
    skip_existing: bool,
    timeout: int,
) -> None:
    """Download CPGF government credit card expense data."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    raw_dir = out / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    months = _generate_months(start_year, end_year)
    logger.info("Downloading CPGF for %d months (%s to %s)", len(months), months[0], months[-1])

    success_count = 0
    for yyyymm in months:
        csv_dest = out / f"cpgf_{yyyymm}.csv"
        if skip_existing and csv_dest.exists():
            logger.info("Skipping (exists): %s", csv_dest.name)
            success_count += 1
            continue

        url = f"{BASE_URL}/{yyyymm}"
        zip_path = raw_dir / f"cpgf_{yyyymm}.zip"

        logger.info("=== %s ===", yyyymm)
        if not download_file(url, zip_path, timeout=timeout):
            logger.warning("Failed to download %s", yyyymm)
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
            logger.warning("No CSV found in ZIP for %s", yyyymm)
            continue

        csv_file.rename(csv_dest)
        validate_csv(csv_dest, encoding="latin-1", sep="\t")
        success_count += 1

    logger.info("=== Done: %d/%d months downloaded ===", success_count, len(months))
    if success_count == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
