#!/usr/bin/env python3
"""Download CEIS/CNEP sanctions data from Portal da Transparencia.

Usage:
    python etl/scripts/download_sanctions.py
    python etl/scripts/download_sanctions.py --date 20260101
    python etl/scripts/download_sanctions.py --output-dir ./data/sanctions
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path

import click
import pandas as pd

# Allow imports from scripts/ directory
sys.path.insert(0, str(Path(__file__).parent))
from _download_utils import download_file, extract_zip, validate_csv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BASE_URL = "https://portaldatransparencia.gov.br/download-de-dados"

# Real government CSV columns → pipeline expected columns
COLUMN_MAP = {
    "CPF OU CNPJ DO SANCIONADO": "cpf_cnpj",
    "NOME DO SANCIONADO": "nome",
    "RAZÃO SOCIAL - CADASTRO RECEITA": "nome",  # fallback name
    "CATEGORIA DA SANÇÃO": "tipo_sancao",
    "DATA INÍCIO SANÇÃO": "data_inicio",
    "DATA FINAL SANÇÃO": "data_fim",
    "FUNDAMENTAÇÃO LEGAL": "motivo",
}


def _find_csv_in_dir(directory: Path) -> Path | None:
    """Find the first CSV file in a directory."""
    csvs = list(directory.glob("*.csv"))
    return csvs[0] if csvs else None


def _remap_columns(df: pd.DataFrame, dataset: str) -> pd.DataFrame:
    """Remap real government column names to pipeline-expected names."""
    mapped = pd.DataFrame()

    for real_col, pipeline_col in COLUMN_MAP.items():
        if real_col in df.columns:
            if pipeline_col in mapped.columns:
                # Fill blanks from fallback column (e.g. nome)
                mapped[pipeline_col] = mapped[pipeline_col].where(
                    mapped[pipeline_col].str.strip() != "", df[real_col],
                )
            else:
                mapped[pipeline_col] = df[real_col]

    if "nome" not in mapped.columns:
        logger.warning("%s: 'nome' column not found after mapping", dataset)

    return mapped


def _download_dataset(
    dataset: str, date_str: str, output_dir: Path, *, skip_existing: bool, timeout: int,
) -> Path | None:
    """Download and extract a single sanctions dataset (ceis or cnep)."""
    url = f"{BASE_URL}/{dataset}/{date_str}"
    raw_dir = output_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    zip_name = f"{dataset}_{date_str}.zip"
    zip_path = raw_dir / zip_name

    if skip_existing and zip_path.exists():
        logger.info("Skipping (exists): %s", zip_name)
    else:
        if not download_file(url, zip_path, timeout=timeout):
            return None

    # Extract
    extract_dir = raw_dir / f"{dataset}_extracted"
    extract_dir.mkdir(parents=True, exist_ok=True)
    extracted = extract_zip(zip_path, extract_dir)
    if not extracted:
        return None

    csv_path = _find_csv_in_dir(extract_dir)
    if csv_path is None:
        logger.warning("No CSV found after extracting %s", zip_name)
        return None

    validate_csv(csv_path, encoding="latin-1", sep=";")
    return csv_path


def _process_csv(csv_path: Path, dataset: str, output_path: Path) -> bool:
    """Read raw CSV, remap columns, write pipeline-ready CSV."""
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

    logger.info("%s: %d rows, columns: %s", dataset, len(df), list(df.columns))
    mapped = _remap_columns(df, dataset)
    expected_cols = {"cpf_cnpj", "nome", "tipo_sancao", "data_inicio", "data_fim", "motivo"}
    missing = expected_cols - set(mapped.columns)
    if missing:
        logger.warning("%s: missing columns after mapping: %s", dataset, missing)
        # Add empty columns for missing
        for col in missing:
            mapped[col] = ""

    mapped.to_csv(output_path, index=False, encoding="latin-1")
    logger.info("Wrote %d rows to %s", len(mapped), output_path)
    return True


@click.command()
@click.option(
    "--date",
    default=lambda: datetime.now().strftime("%Y%m%d"),
    help="Date for download URL (YYYYMMDD). Defaults to today.",
)
@click.option("--output-dir", default="./data/sanctions", help="Output directory")
@click.option("--skip-existing/--no-skip-existing", default=True, help="Skip existing ZIPs")
@click.option("--timeout", type=int, default=300, help="Download timeout in seconds")
def main(date: str, output_dir: str, skip_existing: bool, timeout: int) -> None:
    """Download CEIS and CNEP sanctions data."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    success_count = 0
    for dataset in ("ceis", "cnep"):
        logger.info("=== %s ===", dataset.upper())
        csv_path = _download_dataset(
            dataset, date, out, skip_existing=skip_existing, timeout=timeout,
        )
        if csv_path is None:
            logger.warning("Failed to download %s", dataset)
            continue

        output_path = out / f"{dataset}.csv"
        if _process_csv(csv_path, dataset, output_path):
            success_count += 1

    logger.info("=== Done: %d/2 datasets downloaded ===", success_count)
    if success_count == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
