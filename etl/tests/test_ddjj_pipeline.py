"""Tests for the DDJJ Funcionarios pipeline."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd
import pytest

from aracc_etl.pipelines.ddjj_funcionarios import (
    DdjjFuncionariosPipeline,
    parse_dash_decimal,
)

FIXTURES = Path(__file__).parent / "fixtures" / "ddjj"


# ---------------------------------------------------------------------------
# parse_dash_decimal
# ---------------------------------------------------------------------------


class TestParseDashDecimal:
    def test_normal_dash_decimal(self) -> None:
        assert parse_dash_decimal("35278884-41") == 35278884.41

    def test_zero(self) -> None:
        assert parse_dash_decimal("0-00") == 0.0

    def test_integer_only(self) -> None:
        assert parse_dash_decimal("1500000") == 1500000.0

    def test_none(self) -> None:
        assert parse_dash_decimal(None) is None

    def test_empty_string(self) -> None:
        assert parse_dash_decimal("") is None

    def test_nan_string(self) -> None:
        assert parse_dash_decimal("nan") is None

    def test_float_passthrough(self) -> None:
        assert parse_dash_decimal(42.5) == 42.5

    def test_int_passthrough(self) -> None:
        assert parse_dash_decimal(100) == 100.0

    def test_large_value(self) -> None:
        assert parse_dash_decimal("8500000-75") == 8500000.75


# ---------------------------------------------------------------------------
# parse_tipo_dj (int(float(x)) regression)
# ---------------------------------------------------------------------------


class TestParseTipoDJ:
    """Regression tests for the int(float(x)) pattern used to look up _TIPO_DJ."""

    def _parse(self, value: str) -> str | None:
        from aracc_etl.pipelines.ddjj_funcionarios import _TIPO_DJ
        return _TIPO_DJ.get(int(float(value)), value) if value else None

    def test_zero_float_string(self) -> None:
        assert self._parse("0.00") == "Inicial"

    def test_one_float_string(self) -> None:
        assert self._parse("1.00") == "Anual"

    def test_two_float_string(self) -> None:
        assert self._parse("2.00") == "Baja"

    def test_zero_int_string(self) -> None:
        assert self._parse("0") == "Inicial"

    def test_one_int_string(self) -> None:
        assert self._parse("1") == "Anual"

    def test_unknown_falls_back_to_value(self) -> None:
        assert self._parse("99.00") == "99.00"


# ---------------------------------------------------------------------------
# CSV fixture loading
# ---------------------------------------------------------------------------


class TestFixtureLoading:
    def test_declaraciones_csv(self) -> None:
        df = pd.read_csv(FIXTURES / "declaraciones.csv", dtype=str)
        df.columns = df.columns.str.strip()
        assert len(df) == 3
        assert "cuit" in df.columns
        assert "organismo" in df.columns
        assert "total_bienes_inicio" in df.columns

    def test_bienes_csv_strip_columns(self) -> None:
        df = pd.read_csv(FIXTURES / "bienes.csv", dtype=str)
        # Columns have leading spaces
        assert any(c.startswith(" ") for c in df.columns)
        df.columns = df.columns.str.strip()
        assert "cuit" in df.columns
        assert "tipo_bien" in df.columns

    def test_deudas_csv(self) -> None:
        df = pd.read_csv(FIXTURES / "deudas.csv", dtype=str)
        df.columns = df.columns.str.strip()
        assert len(df) == 3
        assert "tipo_deuda" in df.columns

    def test_familia_csv_strip_columns(self) -> None:
        df = pd.read_csv(FIXTURES / "familia.csv", dtype=str)
        assert any(c.startswith(" ") for c in df.columns)
        df.columns = df.columns.str.strip()
        assert "familiar_nombres" in df.columns
        assert "vinculo_familiar_tipo" in df.columns


# ---------------------------------------------------------------------------
# Transform
# ---------------------------------------------------------------------------


class TestTransform:
    @pytest.fixture()
    def pipeline(self) -> DdjjFuncionariosPipeline:
        driver = MagicMock()
        with tempfile.TemporaryDirectory() as tmpdir:
            link = Path(tmpdir) / "ddjj_funcionarios"
            os.symlink(FIXTURES, link)
            p = DdjjFuncionariosPipeline(
                driver=driver,
                data_dir=tmpdir,
                neo4j_database="neo4j",
            )
            p.transform()
            yield p  # type: ignore[misc]

    def test_transform_produces_dataframes(
        self, pipeline: DdjjFuncionariosPipeline
    ) -> None:
        assert len(pipeline.df_persons) == 3
        assert len(pipeline.df_declarations) == 3
        assert len(pipeline.df_assets) == 4
        assert len(pipeline.df_debts) == 3
        assert len(pipeline.df_family) == 3

    def test_cuit_normalization(self, pipeline: DdjjFuncionariosPipeline) -> None:
        for cuil in pipeline.df_persons["cuil"]:
            assert len(cuil) == 13, f"Bad CUIL format: {cuil}"
            assert cuil[2] == "-" and cuil[11] == "-", f"Bad CUIL dashes: {cuil}"

    def test_name_normalization(self, pipeline: DdjjFuncionariosPipeline) -> None:
        for name in pipeline.df_persons["nombre"].tolist():
            assert name == name.upper(), f"Name not normalized: {name}"

    def test_money_parsing_in_declarations(
        self, pipeline: DdjjFuncionariosPipeline
    ) -> None:
        first = pipeline.df_declarations.iloc[0]
        assert first["total_bienes_inicio"] == pytest.approx(35278884.41)

    def test_limit_applied(self) -> None:
        driver = MagicMock()
        with tempfile.TemporaryDirectory() as tmpdir:
            link = Path(tmpdir) / "ddjj_funcionarios"
            os.symlink(FIXTURES, link)
            p = DdjjFuncionariosPipeline(
                driver=driver,
                data_dir=tmpdir,
                neo4j_database="neo4j",
                limit=1,
            )
            p.transform()
        assert len(p.df_declarations) == 1


# ---------------------------------------------------------------------------
# Load (mocked Neo4j)
# ---------------------------------------------------------------------------


class TestLoad:
    def test_load_calls_neo4j(self) -> None:
        driver = MagicMock()
        session_mock = MagicMock()
        driver.session.return_value.__enter__ = MagicMock(return_value=session_mock)
        driver.session.return_value.__exit__ = MagicMock(return_value=False)

        p = DdjjFuncionariosPipeline(driver=driver, neo4j_database="neo4j")
        p.df_persons = pd.DataFrame({
            "cuil": ["20-12345678-9"],
            "nombre": ["GARCIA JUAN CARLOS"],
            "source": ["ddjj_funcionarios"],
        })
        p.df_declarations = pd.DataFrame({
            "dj_id": ["20-12345678-9_202401_I"],
            "cuil": ["20-12345678-9"],
            "anio": ["2024"],
            "tipo": ["Anual"],
            "organismo": ["MINISTERIO DE ECONOMIA"],
            "cargo": ["SUBSECRETARIO"],
            "total_bienes_inicio": [35278884.41],
            "total_bienes_cierre": [42000000.50],
            "total_deudas_cierre": [1200000.00],
            "ingreso_neto_anual": [8500000.75],
        })
        p.df_assets = pd.DataFrame()
        p.df_debts = pd.DataFrame()
        p.df_family = pd.DataFrame()

        p.load()

        assert session_mock.run.call_count > 0
        assert p.rows_loaded == 1
