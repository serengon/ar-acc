#!/usr/bin/env python3
"""Download OpenSanctions bulk data in FollowTheMoney JSONL format.

Usage:
    python etl/scripts/download_opensanctions.py
    python etl/scripts/download_opensanctions.py --output-dir ./data/opensanctions
    python etl/scripts/download_opensanctions.py --dataset br_transparency
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

DATASETS = {
    "default": "https://data.opensanctions.org/datasets/latest/default/entities.ftm.json",
    "br_transparency": "https://data.opensanctions.org/datasets/latest/br_transparency/entities.ftm.json",
}


@click.command()
@click.option("--output-dir", default="./data/opensanctions", help="Output directory")
@click.option(
    "--dataset",
    type=click.Choice(list(DATASETS.keys())),
    default="default",
    help="Which dataset to download (default: full global, br_transparency: Brazil-specific)",
)
@click.option("--skip-existing/--no-skip-existing", default=True, help="Skip existing")
@click.option("--timeout", type=int, default=600, help="Download timeout in seconds")
def main(output_dir: str, dataset: str, skip_existing: bool, timeout: int) -> None:
    """Download OpenSanctions FtM JSONL data."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    url = DATASETS[dataset]
    dest = out / "entities.ftm.json"

    if skip_existing and dest.exists():
        logger.info("Skipping download (exists): %s", dest.name)
    else:
        if not download_file(url, dest, timeout=timeout):
            logger.warning("Failed to download OpenSanctions data")
            sys.exit(1)

    # Quick validation: count lines
    line_count = 0
    with open(dest, encoding="utf-8") as f:
        for _ in f:
            line_count += 1

    logger.info("=== Done: %s downloaded (%d entities) ===", dataset, line_count)


if __name__ == "__main__":
    main()
