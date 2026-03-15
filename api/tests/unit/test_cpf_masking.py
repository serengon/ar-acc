"""Tests for CUIL/CUIT masking middleware and helpers."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from aracc.middleware.cuil_masking import (
    _collect_pep_cuils,
    _is_pep_record,
    mask_cuils_in_json,
    mask_formatted_cuil,
    mask_raw_cuil,
)

if TYPE_CHECKING:
    from httpx import AsyncClient


# ---------------------------------------------------------------------------
# Unit tests for pure helper functions
# ---------------------------------------------------------------------------


class TestMaskFormattedCUIL:
    def test_basic(self) -> None:
        assert mask_formatted_cuil("20-12345678-9") == "**-*****678-9"

    def test_another(self) -> None:
        assert mask_formatted_cuil("30-11122233-4") == "**-*****233-4"


class TestMaskRawCUIL:
    def test_basic(self) -> None:
        assert mask_raw_cuil("20123456789") == "*******6789"

    def test_zeros(self) -> None:
        assert mask_raw_cuil("00000000000") == "*******0000"


class TestIsPepRecord:
    def test_explicit_is_pep_true(self) -> None:
        assert _is_pep_record({"name": "Juan", "cuil": "20123456789", "is_pep": True})

    def test_explicit_is_pep_false(self) -> None:
        assert not _is_pep_record({"name": "Juan", "cuil": "20123456789", "is_pep": False})

    @pytest.mark.parametrize(
        "role",
        [
            "diputado",
            "senador",
            "concejal",
            "intendente",
            "gobernador",
            "presidente",
            "ministro",
            "Diputada",
            "SENADORA",
            "Ministra",
            "secretario",
            "legislador",
        ],
    )
    def test_political_role(self, role: str) -> None:
        assert _is_pep_record({"name": "X", "cuil": "20111111111", "role": role})

    def test_cargo_field(self) -> None:
        assert _is_pep_record({"name": "X", "cuil": "20111111111", "cargo": "Diputado"})

    @pytest.mark.parametrize(
        "role",
        [
            "Diputado Nacional",
            "diputado nacional",
            "DIPUTADO NACIONAL",
            "Senador de la Nacion",
            "senadora de la nacion",
            "Concejal Suplente",
            "Ministro de Estado",
            "Gobernadora de la Provincia de Buenos Aires",
            "Presidente de la Nacion",
            "Jefe de Gobierno",
        ],
    )
    def test_compound_role_detected_as_pep(self, role: str) -> None:
        """Compound PEP roles like 'diputado nacional' must be detected via substring match."""
        assert _is_pep_record({"name": "X", "cuil": "20111111111", "role": role})

    def test_compound_cargo_detected_as_pep(self) -> None:
        """Compound PEP cargo like 'Diputado Nacional' must be detected via substring match."""
        assert _is_pep_record({"name": "X", "cuil": "20111111111", "cargo": "Diputado Nacional"})

    def test_non_pep_role(self) -> None:
        assert not _is_pep_record({"name": "X", "cuil": "20111111111", "role": "asesor"})

    def test_no_role_no_is_pep(self) -> None:
        assert not _is_pep_record({"name": "X", "cuil": "20111111111"})


class TestCollectPepCuils:
    def test_flat_pep(self) -> None:
        data = {"cuil": "20-12345678-9", "is_pep": True}
        assert _collect_pep_cuils(data) == {"20123456789"}

    def test_flat_non_pep(self) -> None:
        data = {"cuil": "20-12345678-9", "is_pep": False}
        assert _collect_pep_cuils(data) == set()

    def test_nested_list(self) -> None:
        data = {
            "results": [
                {"cuil": "20111111111", "role": "diputado"},
                {"cuil": "20222222222", "role": "asesor"},
            ]
        }
        peps = _collect_pep_cuils(data)
        assert "20111111111" in peps
        assert "20222222222" not in peps

    def test_deeply_nested(self) -> None:
        data = {"a": {"b": {"c": [{"cuil": "20333333333", "is_pep": True}]}}}
        assert "20333333333" in _collect_pep_cuils(data)

    def test_compound_role_collected(self) -> None:
        """Compound roles like 'Diputado Nacional' must be recognized in the walk."""
        data = {
            "results": [
                {"cuil": "20111111111", "role": "Diputado Nacional"},
                {"cuil": "20222222222", "role": "asesor parlamentario"},
            ]
        }
        peps = _collect_pep_cuils(data)
        assert "20111111111" in peps
        assert "20222222222" not in peps

    def test_cuit_field_collected(self) -> None:
        """CUIT field on PEP records must also be collected."""
        data = {"cuit": "30111111111", "is_pep": True}
        assert "30111111111" in _collect_pep_cuils(data)


# ---------------------------------------------------------------------------
# Unit tests for mask_cuils_in_json
# ---------------------------------------------------------------------------


class TestMaskCuilsInJson:
    def test_formatted_cuil_masked(self) -> None:
        text = '{"cuil": "20-12345678-9"}'
        result = mask_cuils_in_json(text)
        assert "**-*****678-9" in result
        assert "20-12345" not in result

    def test_raw_cuil_masked(self) -> None:
        text = '{"cuil": "20123456789"}'
        result = mask_cuils_in_json(text)
        assert "*******6789" in result
        assert "2012345" not in result

    def test_pep_cuil_not_masked(self) -> None:
        text = '{"cuil": "20123456789"}'
        result = mask_cuils_in_json(text, pep_cuils={"20123456789"})
        assert "20123456789" in result

    def test_pep_formatted_cuil_not_masked(self) -> None:
        text = '{"cuil": "20-12345678-9"}'
        result = mask_cuils_in_json(text, pep_cuils={"20123456789"})
        assert "20-12345678-9" in result

    def test_multiple_cuils(self) -> None:
        text = json.dumps({
            "people": [
                {"name": "A", "cuil": "20-11122233-4"},
                {"name": "B", "cuil": "23-55566677-8"},
            ]
        })
        result = mask_cuils_in_json(text)
        assert "**-*****233-4" in result
        assert "**-*****677-8" in result

    def test_mixed_pep_and_non_pep(self) -> None:
        text = json.dumps({
            "people": [
                {"name": "A", "cuil": "20-11122233-4"},
                {"name": "B", "cuil": "23-55566677-8"},
            ]
        })
        result = mask_cuils_in_json(text, pep_cuils={"20111222334"})
        assert "20-11122233-4" in result  # PEP: not masked
        assert "**-*****677-8" in result  # Non-PEP: masked

    def test_empty_string(self) -> None:
        assert mask_cuils_in_json("") == ""

    def test_no_cuils(self) -> None:
        text = '{"name": "hello"}'
        assert mask_cuils_in_json(text) == text

    def test_null_cuil_value(self) -> None:
        text = '{"cuil": null}'
        assert mask_cuils_in_json(text) == text

    def test_cuil_in_nested_json(self) -> None:
        text = json.dumps({
            "entity": {
                "details": {
                    "personal": {"cuil": "20-98765432-1"}
                }
            }
        })
        result = mask_cuils_in_json(text)
        assert "**-*****432-1" in result

    def test_short_digit_sequence_not_masked(self) -> None:
        """A 6-digit number should NOT be treated as CUIL."""
        text = '{"partial": "123456"}'
        result = mask_cuils_in_json(text)
        assert "123456" in result

    def test_non_json_text_passthrough(self) -> None:
        text = "This is plain text with no CUILs."
        assert mask_cuils_in_json(text) == text


# ---------------------------------------------------------------------------
# Integration tests via the ASGI app
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_health_not_masked(client: AsyncClient) -> None:
    """Non-CUIL JSON responses pass through unchanged."""
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
