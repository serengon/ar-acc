"""DDJJ — Declaraciones Juradas Patrimoniales de Funcionarios.

Ingests asset declarations from public officials.

Source: https://datos.jus.gob.ar/dataset/declaraciones-juradas-patrimoniales
"""

from __future__ import annotations

import logging
from pathlib import Path

import httpx
import pandas as pd

from aracc_etl.base import Pipeline
from aracc_etl.loader import Neo4jBatchLoader
from aracc_etl.transforms.document_formatting import format_cuit, strip_document
from aracc_etl.transforms.name_normalization import normalize_name

logger = logging.getLogger(__name__)

_TIPO_DJ = {0: "Inicial", 1: "Anual", 2: "Baja"}

_URLS = {
    "declaraciones": (
        "https://datos.jus.gob.ar/dataset/"
        "4680199f-6234-4262-8a2a-8f7993bf784d/resource/"
        "a331ccb8-5c13-447f-9bd6-d8018a4b8a62/download/"
        "declaraciones-juradas-2024-consolidado-al-20251222.csv"
    ),
    "bienes": (
        "https://datos.jus.gob.ar/dataset/"
        "4680199f-6234-4262-8a2a-8f7993bf784d/resource/"
        "ffa28585-9adb-473e-9627-0ffe1938d288/download/"
        "declaraciones-juradas-bienes-2024-consolidado-al-20251222.csv"
    ),
    "deudas": (
        "https://datos.jus.gob.ar/dataset/"
        "4680199f-6234-4262-8a2a-8f7993bf784d/resource/"
        "dd1c30e2-e773-47fd-ac80-9afaf3f1baa4/download/"
        "declaraciones-juradas-deudas-2024-consolidado-al-20251222.csv"
    ),
    "familia": (
        "https://datos.jus.gob.ar/dataset/"
        "4680199f-6234-4262-8a2a-8f7993bf784d/resource/"
        "aeb174ff-26b5-4586-827f-872afdc52b49/download/"
        "declaraciones-juradas-grupo-familiar-2024-consolidado-al-20251222.csv"
    ),
}


def parse_dash_decimal(value: str | float | None) -> float | None:
    """Parse monetary values where dashes are decimal separators.

    The principal DDJJ CSV uses dash as the decimal separator:
    ``35278884-41`` means 35278884.41, ``0-00`` means 0.0.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip()
    if not s or s.lower() == "nan":
        return None
    # If it contains a dash that is NOT the leading negative sign, treat as decimal sep
    if "-" in s:
        parts = s.rsplit("-", maxsplit=1)
        if len(parts) == 2 and parts[1].isdigit():
            # Check if the left part is a valid number (may start with -)
            try:
                integer_part = parts[0].replace(".", "").replace(",", "")
                return float(f"{integer_part}.{parts[1]}")
            except ValueError:
                pass
    # Fallback: try direct float conversion
    try:
        return float(s.replace(",", "."))
    except ValueError:
        return None


class DdjjFuncionariosPipeline(Pipeline):
    name = "ddjj_funcionarios"
    source_id = "ddjj_funcionarios"

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]
        self.df_persons: pd.DataFrame = pd.DataFrame()
        self.df_declarations: pd.DataFrame = pd.DataFrame()
        self.df_assets: pd.DataFrame = pd.DataFrame()
        self.df_debts: pd.DataFrame = pd.DataFrame()
        self.df_family: pd.DataFrame = pd.DataFrame()

    def extract(self) -> None:
        out_dir = Path(self.data_dir) / "ddjj_funcionarios"
        out_dir.mkdir(parents=True, exist_ok=True)

        for key, url in _URLS.items():
            dest = out_dir / f"{key}.csv"
            if dest.exists():
                logger.info("[%s] %s already downloaded, skipping", self.name, key)
                continue
            logger.info("[%s] Downloading %s ...", self.name, key)
            with httpx.stream("GET", url, follow_redirects=True, timeout=120) as resp:
                resp.raise_for_status()
                with open(dest, "wb") as f:
                    for chunk in resp.iter_bytes(chunk_size=1024 * 64):
                        f.write(chunk)
            logger.info("[%s] Saved %s", self.name, dest)

    def transform(self) -> None:
        base = Path(self.data_dir) / "ddjj_funcionarios"

        # --- Load CSVs ---
        df_decl = pd.read_csv(base / "declaraciones.csv", dtype=str, keep_default_na=False)
        df_bienes = pd.read_csv(base / "bienes.csv", dtype=str, keep_default_na=False)
        df_deudas = pd.read_csv(base / "deudas.csv", dtype=str, keep_default_na=False)
        df_fam = pd.read_csv(base / "familia.csv", dtype=str, keep_default_na=False)

        # Strip whitespace from column names (bienes and familia have leading spaces)
        df_decl.columns = df_decl.columns.str.strip()
        df_bienes.columns = df_bienes.columns.str.strip()
        df_deudas.columns = df_deudas.columns.str.strip()
        df_fam.columns = df_fam.columns.str.strip()

        self.rows_in = len(df_decl)

        # Apply limit
        if self.limit:
            df_decl = df_decl.head(self.limit)
            # Filter related tables by CUIT set
            cuit_set = set(df_decl["cuit"].unique())
            df_bienes = df_bienes[df_bienes["cuit"].isin(cuit_set)]
            df_deudas = df_deudas[df_deudas["cuit"].isin(cuit_set)]
            df_fam = df_fam[df_fam["cuit"].isin(cuit_set)]

        # --- Normalize CUITs ---
        for df in [df_decl, df_bienes, df_deudas, df_fam]:
            df["cuit_fmt"] = df["cuit"].apply(
                lambda x: format_cuit(strip_document(x))
            )

        # --- Persons ---
        persons_decl = df_decl[["cuit_fmt", "funcionario_apellido_nombre"]].copy()
        persons_decl = persons_decl.rename(columns={"cuit_fmt": "cuil"})
        persons_decl["name"] = persons_decl["funcionario_apellido_nombre"].apply(
            normalize_name
        )
        persons_decl = persons_decl[["cuil", "name"]].drop_duplicates(subset=["cuil"])
        persons_decl["source"] = "ddjj_funcionarios"
        self.df_persons = persons_decl[persons_decl["cuil"].str.len() > 0]

        # --- Declarations ---
        # dj_id already exists in the CSV
        tipo_col = "tipo_declaracion_jurada_id"
        df_decl["tipo"] = df_decl[tipo_col].apply(
            lambda x: _TIPO_DJ.get(int(float(x)), x) if x else None
        )

        money_cols = [
            "total_bienes_inicio", "deudas_inicio",
            "total_bienes_final", "total_deudas_final",
            "total_ingreso_neto_c1234",
        ]
        for col in money_cols:
            if col in df_decl.columns:
                df_decl[col + "_num"] = df_decl[col].apply(parse_dash_decimal)

        declarations = df_decl[[
            "dj_id", "cuit_fmt", "anio", "tipo", "organismo", "cargo",
        ]].copy()
        declarations = declarations.rename(columns={"cuit_fmt": "cuil"})
        for col in money_cols:
            num_col = col + "_num"
            if num_col in df_decl.columns:
                declarations[col] = df_decl[num_col]
        declarations["organismo"] = declarations["organismo"].apply(normalize_name)
        declarations["cargo"] = declarations["cargo"].apply(normalize_name)
        self.df_declarations = declarations[declarations["dj_id"].str.len() > 0]

        # --- Assets ---
        if not df_bienes.empty:
            # dj_id already in CSV; build unique asset_id
            df_bienes["asset_idx"] = df_bienes.groupby("dj_id").cumcount()
            df_bienes["asset_id"] = (
                df_bienes["dj_id"].astype(str) + "_A" + df_bienes["asset_idx"].astype(str)
            )
            assets = df_bienes[["asset_id", "dj_id"]].copy()
            assets["dj_id"] = assets["dj_id"].astype(str)
            assets["tipo"] = df_bienes.get("bien_tipo", "")
            assets["descripcion"] = df_bienes.get("bien_descripcion", "")
            if "bien_importe" in df_bienes.columns:
                assets["valor"] = pd.to_numeric(
                    df_bienes["bien_importe"], errors="coerce"
                )
            if "bien_titularidad" in df_bienes.columns:
                assets["titularidad"] = pd.to_numeric(
                    df_bienes["bien_titularidad"], errors="coerce"
                )
            assets["periodo"] = df_bienes.get("periodo_inicio_cierre", "")
            self.df_assets = assets
        else:
            self.df_assets = pd.DataFrame()

        # --- Debts ---
        if not df_deudas.empty:
            # dj_id already in CSV
            df_deudas["debt_idx"] = df_deudas.groupby("dj_id").cumcount()
            df_deudas["debt_id"] = (
                df_deudas["dj_id"].astype(str) + "_D" + df_deudas["debt_idx"].astype(str)
            )
            debts = df_deudas[["debt_id", "dj_id"]].copy()
            debts["dj_id"] = debts["dj_id"].astype(str)
            debts["tipo"] = df_deudas.get("deuda_tipo", "")
            debts["descripcion"] = df_deudas.get("deuda_descripcion", "")
            if "deuda_importe" in df_deudas.columns:
                debts["monto"] = pd.to_numeric(
                    df_deudas["deuda_importe"], errors="coerce"
                )
            if "deuda_radicacion_localizacion" in df_deudas.columns:
                debts["radicacion"] = df_deudas["deuda_radicacion_localizacion"]
            if "deuda_clasificacion" in df_deudas.columns:
                debts["clasificacion"] = df_deudas["deuda_clasificacion"]
            debts["periodo"] = df_deudas.get("periodo_inicio_cierre", "")
            self.df_debts = debts
        else:
            self.df_debts = pd.DataFrame()

        # --- Family ---
        if not df_fam.empty:
            df_fam["funcionario_cuil"] = df_fam["cuit_fmt"]
            df_fam["familiar_nombre_norm"] = df_fam["familiar_apellido_nombre"].apply(
                normalize_name
            )
            df_fam["familiar_cuil_fmt"] = df_fam["familiar_cuit"].apply(
                lambda x: format_cuit(strip_document(x)) if x else ""
            )
            df_fam["vinculo"] = df_fam.get("familiar_parentesco", "")
            family = df_fam[[
                "funcionario_cuil", "familiar_nombre_norm", "familiar_cuil_fmt", "vinculo",
            ]].copy()
            family = family.rename(columns={
                "familiar_nombre_norm": "familiar_nombre",
                "familiar_cuil_fmt": "familiar_cuil",
            })
            self.df_family = family
        else:
            self.df_family = pd.DataFrame()

        logger.info(
            "[%s] Transform complete: %d declarations, %d assets, %d debts, %d family",
            self.name,
            len(self.df_declarations),
            len(self.df_assets),
            len(self.df_debts),
            len(self.df_family),
        )

    def load(self) -> None:
        loader = Neo4jBatchLoader(
            self.driver,
            batch_size=self.chunk_size,
            neo4j_database=self.neo4j_database,
        )

        # --- Person nodes ---
        person_rows = self.df_persons.to_dict("records")
        n = loader.load_nodes("Person", person_rows, "cuil")
        logger.info("[%s] Loaded %d Person nodes", self.name, n)

        # --- Declaration nodes ---
        decl_rows = self.df_declarations.to_dict("records")
        n = loader.run_query_with_retry(
            "UNWIND $rows AS row "
            "MERGE (d:Declaration {dj_id: row.dj_id}) "
            "SET d.anio = row.anio, d.tipo = row.tipo, "
            "    d.organismo = row.organismo, d.cargo = row.cargo, "
            "    d.total_bienes_inicio = row.total_bienes_inicio, "
            "    d.total_bienes_final = row.total_bienes_final, "
            "    d.total_deudas_final = row.total_deudas_final, "
            "    d.ingresos = row.total_ingreso_neto_c1234",
            decl_rows,
        )
        logger.info("[%s] Loaded %d Declaration nodes", self.name, n)

        # --- Person -[:PRESENTO_DDJJ]-> Declaration ---
        presento_rows = [
            {"source_key": r["cuil"], "target_key": r["dj_id"]}
            for r in decl_rows
            if r.get("cuil") and r.get("dj_id")
        ]
        n = loader.load_relationships(
            "PRESENTO_DDJJ", presento_rows,
            "Person", "cuil", "Declaration", "dj_id",
        )
        logger.info("[%s] Loaded %d PRESENTO_DDJJ rels", self.name, n)

        # --- PublicOffice nodes + OCUPA_CARGO rels ---
        offices = self.df_declarations[["organismo", "cargo"]].drop_duplicates()
        offices["office_id"] = offices["organismo"] + "|" + offices["cargo"]
        office_rows = offices.to_dict("records")
        n = loader.run_query_with_retry(
            "UNWIND $rows AS row "
            "MERGE (o:PublicOffice {office_id: row.office_id}) "
            "SET o.organismo = row.organismo, o.cargo = row.cargo",
            office_rows,
        )
        logger.info("[%s] Loaded %d PublicOffice nodes", self.name, n)

        cargo_rows = [
            {
                "source_key": r["cuil"],
                "target_key": r["organismo"] + "|" + r["cargo"],
            }
            for r in decl_rows
            if r.get("cuil") and r.get("organismo") and r.get("cargo")
        ]
        # Deduplicate
        seen: set[tuple[str, str]] = set()
        unique_cargo: list[dict[str, str]] = []
        for cr in cargo_rows:
            key = (cr["source_key"], cr["target_key"])
            if key not in seen:
                seen.add(key)
                unique_cargo.append(cr)
        n = loader.load_relationships(
            "OCUPA_CARGO", unique_cargo,
            "Person", "cuil", "PublicOffice", "office_id",
        )
        logger.info("[%s] Loaded %d OCUPA_CARGO rels", self.name, n)

        # --- DeclaredAsset nodes + INCLUYE_BIEN rels ---
        if not self.df_assets.empty:
            asset_rows = self.df_assets.to_dict("records")
            n = loader.run_query_with_retry(
                "UNWIND $rows AS row "
                "MERGE (a:DeclaredAsset {asset_id: row.asset_id}) "
                "SET a.tipo = row.tipo, a.descripcion = row.descripcion, "
                "    a.valor = row.valor, a.titularidad = row.titularidad, "
                "    a.periodo = row.periodo",
                asset_rows,
            )
            logger.info("[%s] Loaded %d DeclaredAsset nodes", self.name, n)

            bien_rels = [
                {"source_key": r["dj_id"], "target_key": r["asset_id"]}
                for r in asset_rows
                if r.get("dj_id") and r.get("asset_id")
            ]
            n = loader.load_relationships(
                "INCLUYE_BIEN", bien_rels,
                "Declaration", "dj_id", "DeclaredAsset", "asset_id",
            )
            logger.info("[%s] Loaded %d INCLUYE_BIEN rels", self.name, n)

        # --- DeclaredDebt nodes + INCLUYE_DEUDA rels ---
        if not self.df_debts.empty:
            debt_rows = self.df_debts.to_dict("records")
            n = loader.run_query_with_retry(
                "UNWIND $rows AS row "
                "MERGE (d:DeclaredDebt {debt_id: row.debt_id}) "
                "SET d.tipo = row.tipo, d.descripcion = row.descripcion, "
                "    d.monto = row.monto, d.radicacion = row.radicacion, "
                "    d.periodo = row.periodo",
                debt_rows,
            )
            logger.info("[%s] Loaded %d DeclaredDebt nodes", self.name, n)

            deuda_rels = [
                {"source_key": r["dj_id"], "target_key": r["debt_id"]}
                for r in debt_rows
                if r.get("dj_id") and r.get("debt_id")
            ]
            n = loader.load_relationships(
                "INCLUYE_DEUDA", deuda_rels,
                "Declaration", "dj_id", "DeclaredDebt", "debt_id",
            )
            logger.info("[%s] Loaded %d INCLUYE_DEUDA rels", self.name, n)

        # --- FAMILIAR_DE rels ---
        if not self.df_family.empty:
            fam_rows = self.df_family.to_dict("records")
            n = loader.run_query_with_retry(
                "UNWIND $rows AS row "
                "MATCH (p:Person {cuil: row.funcionario_cuil}) "
                "MERGE (f:Person {cuil: CASE WHEN row.familiar_cuil <> '' "
                "  THEN row.familiar_cuil ELSE 'FAM_' + row.familiar_nombre END}) "
                "ON CREATE SET f.source = 'ddjj_funcionarios_familiar', "
                "    f.name = row.familiar_nombre "
                "MERGE (p)-[r:FAMILIAR_DE]->(f) "
                "SET r.vinculo = row.vinculo",
                fam_rows,
            )
            logger.info("[%s] Loaded %d FAMILIAR_DE rels", self.name, n)

        self.rows_loaded = len(self.df_declarations)
        logger.info("[%s] Load complete: %d rows loaded", self.name, self.rows_loaded)
