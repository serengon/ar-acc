#!/usr/bin/env python3
"""Download ICIJ OffshoreLeaks bulk CSV data.

Usage:
    python etl/scripts/download_icij.py
    python etl/scripts/download_icij.py --output-dir ./data/icij
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import click

# Allow imports from scripts/ directory
sys.path.insert(0, str(Path(__file__).parent))
from _download_utils import download_file, extract_zip

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BULK_DOWNLOAD_URL = "https://offshoreleaks.icij.org/pages/database"
CSV_ZIP_URL = "https://offshoreleaks-data.icij.org/offshoreleaks/csv/full-oldb.LATEST.zip"

EXPECTED_FILES = [
    "nodes-entities.csv",
    "nodes-officers.csv",
    "nodes-intermediaries.csv",
    "relationships.csv",
]


@click.command()
@click.option("--output-dir", default="./data/icij", help="Output directory")
@click.option("--skip-existing/--no-skip-existing", default=True, help="Skip if ZIP already exists")
@click.option("--timeout", type=int, default=600, help="Download timeout in seconds")
def main(output_dir: str, skip_existing: bool, timeout: int) -> None:
    """Download ICIJ OffshoreLeaks bulk CSV data."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    raw_dir = out / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    zip_path = raw_dir / "full-oldb.LATEST.zip"

    if skip_existing and zip_path.exists():
        logger.info("Skipping download (exists): %s", zip_path.name)
    else:
        if not download_file(CSV_ZIP_URL, zip_path, timeout=timeout):
            logger.warning("Failed to download ICIJ data")
            sys.exit(1)

    # Extract
    extracted = extract_zip(zip_path, out)
    if not extracted:
        logger.warning("Failed to extract ICIJ ZIP")
        sys.exit(1)

    # Verify expected files
    found = 0
    for expected in EXPECTED_FILES:
        path = out / expected
        if path.exists():
            logger.info("Found: %s", expected)
            found += 1
        else:
            logger.warning("Missing expected file: %s", expected)

    logger.info("=== Done: %d/%d expected files found ===", found, len(EXPECTED_FILES))
    if found == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
