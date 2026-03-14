#!/usr/bin/env python3
"""Download SIOP emendas parlamentares data from Portal da Transparencia.

Usage:
    python etl/scripts/download_siop.py
    python etl/scripts/download_siop.py --start-year 2020 --end-year 2024
    python etl/scripts/download_siop.py --output-dir ./data/siop
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import click
import pandas as pd

# Allow imports from scripts/ directory
sys.path.insert(0, str(Path(__file__).parent))
from _download_utils import download_file, extract_zip, validate_csv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BASE_URL = "https://portaldatransparencia.gov.br/download-de-dados"


def _find_csvs(directory: Path) -> list[Path]:
    """Find all CSV files in a directory."""
    return sorted(directory.glob("*.csv"))


def _download_year(
    year: int,
    raw_dir: Path,
    *,
    skip_existing: bool,
    timeout: int,
) -> list[Path]:
    """Download and extract emendas-parlamentares ZIP for a given year."""
    url = f"{BASE_URL}/emendas-parlamentares/{year}"
    zip_name = f"emendas-parlamentares_{year}.zip"
    zip_path = raw_dir / zip_name

    if skip_existing and zip_path.exists():
        logger.info("Skipping (exists): %s", zip_name)
    else:
        if not download_file(url, zip_path, timeout=timeout):
            return []

    extract_dir = raw_dir / f"emendas_{year}_extracted"
    extract_dir.mkdir(parents=True, exist_ok=True)
    extracted = extract_zip(zip_path, extract_dir)
    return [f for f in extracted if f.suffix.lower() == ".csv"]


def _concat_and_write(
    csv_files: list[Path],
    output_path: Path,
    *,
    sep: str = ";",
    encoding: str = "latin-1",
) -> int:
    """Read multiple CSVs, concatenate, and write to output."""
    frames: list[pd.DataFrame] = []
    for csv_path in csv_files:
        try:
            df = pd.read_csv(
                csv_path,
                sep=sep,
                encoding=encoding,
                dtype=str,
                keep_default_na=False,
            )
            frames.append(df)
            logger.info("  Read %d rows from %s", len(df), csv_path.name)
        except Exception as e:
            logger.warning("  Failed to read %s: %s", csv_path.name, e)

    if not frames:
        return 0

    combined = pd.concat(frames, ignore_index=True)
    combined.to_csv(output_path, index=False, sep=";", encoding="latin-1")
    logger.info("Wrote %d rows to %s", len(combined), output_path)
    return len(combined)


@click.command()
@click.option("--start-year", type=int, default=2020, help="First year to download")
@click.option("--end-year", type=int, default=2024, help="Last year to download")
@click.option("--output-dir", default="./data/siop", help="Output directory")
@click.option("--skip-existing/--no-skip-existing", default=True, help="Skip existing ZIPs")
@click.option("--timeout", type=int, default=600, help="Download timeout in seconds")
def main(
    start_year: int,
    end_year: int,
    output_dir: str,
    skip_existing: bool,
    timeout: int,
) -> None:
    """Download SIOP emendas parlamentares data from Portal da Transparencia."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    raw_dir = out / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    logger.info("=== SIOP Emendas: years %d-%d ===", start_year, end_year)

    all_csvs: list[Path] = []
    for year in range(start_year, end_year + 1):
        logger.info("--- Year %d ---", year)
        csvs = _download_year(year, raw_dir, skip_existing=skip_existing, timeout=timeout)
        if csvs:
            for csv_path in csvs:
                validate_csv(csv_path, encoding="latin-1", sep=";")
            all_csvs.extend(csvs)
        else:
            logger.warning("No data for year %d", year)

    if not all_csvs:
        logger.warning("No CSVs downloaded across all years")
        sys.exit(1)

    # Write one combined CSV per year for pipeline consumption
    # Group extracted CSVs by year
    year_csvs: dict[int, list[Path]] = {}
    for year in range(start_year, end_year + 1):
        year_files = [f for f in all_csvs if f"{year}" in str(f)]
        if year_files:
            year_csvs[year] = year_files

    total_rows = 0
    for year, csvs in sorted(year_csvs.items()):
        output_path = out / f"emendas_{year}.csv"
        rows = _concat_and_write(csvs, output_path)
        total_rows += rows

    logger.info("=== Done: %d total rows across %d years ===", total_rows, len(year_csvs))


if __name__ == "__main__":
    main()
