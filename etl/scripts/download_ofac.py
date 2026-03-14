#!/usr/bin/env python3
"""Download OFAC SDN data from US Treasury.

Downloads the SDN (Specially Designated Nationals) list, address file,
and alias file.

Usage:
    python etl/scripts/download_ofac.py
    python etl/scripts/download_ofac.py --output-dir ./data/ofac
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

BASE_URL = "https://www.treasury.gov/ofac/downloads"

FILES = {
    "sdn.csv": f"{BASE_URL}/sdn.csv",
    "add.csv": f"{BASE_URL}/add.csv",
    "alt.csv": f"{BASE_URL}/alt.csv",
}


@click.command()
@click.option("--output-dir", default="./data/ofac", help="Output directory")
@click.option(
    "--skip-existing/--no-skip-existing", default=True, help="Skip existing files"
)
@click.option("--timeout", type=int, default=300, help="Download timeout in seconds")
def main(output_dir: str, skip_existing: bool, timeout: int) -> None:
    """Download OFAC SDN, address, and alias CSV files."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    success_count = 0
    for filename, url in FILES.items():
        dest = out / filename

        if skip_existing and dest.exists():
            logger.info("Skipping (exists): %s", filename)
            success_count += 1
            continue

        logger.info("=== Downloading %s ===", filename)
        if download_file(url, dest, timeout=timeout):
            success_count += 1
        else:
            logger.warning("Failed to download %s", filename)

    logger.info("=== Done: %d/%d files downloaded ===", success_count, len(FILES))
    if success_count == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
