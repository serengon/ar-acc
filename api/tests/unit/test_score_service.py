from unittest.mock import AsyncMock, MagicMock

import pytest

from aracc.services.neo4j_service import CypherLoader
from aracc.services.score_service import (
    _conn_percentile,
    _fin_percentile,
    compute_exposure,
)


class TestConnPercentile:
    def test_zero_connections(self) -> None:
        assert _conn_percentile(0) == 0.0

    def test_low_connections(self) -> None:
        assert _conn_percentile(1) == 25.0
        assert _conn_percentile(2) == 25.0

    def test_medium_connections(self) -> None:
        assert _conn_percentile(3) == 50.0
        assert _conn_percentile(5) == 50.0

    def test_high_connections(self) -> None:
        assert _conn_percentile(10) == 75.0
        assert _conn_percentile(15) == 75.0

    def test_very_high_connections(self) -> None:
        result = _conn_percentile(50)
        assert result == 90.0

    def test_extreme_connections(self) -> None:
        result = _conn_percentile(100)
        assert 90.0 < result <= 99.0


class TestFinPercentile:
    def test_zero_volume(self) -> None:
        assert _fin_percentile(0.0) == 0.0

    def test_small_volume(self) -> None:
        result = _fin_percentile(10_000.0)
        assert 0.0 < result < 25.0

    def test_medium_volume(self) -> None:
        result = _fin_percentile(100_000.0)
        assert 20.0 <= result <= 30.0

    def test_large_volume(self) -> None:
        result = _fin_percentile(10_000_000.0)
        assert 50.0 <= result <= 80.0

    def test_very_large_volume(self) -> None:
        result = _fin_percentile(100_000_000.0)
        assert 75.0 <= result <= 95.0


@pytest.mark.anyio
async def test_compute_exposure_returns_response() -> None:
    session = AsyncMock()

    score_record = MagicMock()
    score_record.__getitem__ = lambda self, key: {
        "entity_id": "4:abc:1",
        "entity_labels": ["Company"],
        "connection_count": 10,
        "source_count": 3,
        "financial_volume": 50000.0,
        "cnae_principal": "4711-3/02",
        "role": None,
    }[key]

    async def mock_run(cypher: str, params: dict, timeout: float = 15):  # type: ignore[no-untyped-def]
        result = AsyncMock()
        result.single = AsyncMock(return_value=score_record)
        return result

    session.run = mock_run

    response = await compute_exposure(session, "4:abc:1")

    assert response.entity_id == "4:abc:1"
    assert 0.0 <= response.exposure_index <= 100.0
    assert len(response.factors) == 5
    assert response.peer_group == "CNAE 4711-3/02"
    assert len(response.sources) > 0


@pytest.mark.anyio
async def test_compute_exposure_entity_not_found() -> None:
    session = AsyncMock()

    async def mock_run(cypher: str, params: dict, timeout: float = 15):  # type: ignore[no-untyped-def]
        result = AsyncMock()
        result.single = AsyncMock(return_value=None)
        return result

    session.run = mock_run

    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc_info:
        await compute_exposure(session, "nonexistent")
    assert exc_info.value.status_code == 404


@pytest.mark.anyio
async def test_compute_exposure_person_peer_group() -> None:
    session = AsyncMock()

    score_record = MagicMock()
    score_record.__getitem__ = lambda self, key: {
        "entity_id": "4:abc:2",
        "entity_labels": ["Person"],
        "connection_count": 5,
        "source_count": 2,
        "financial_volume": 0.0,
        "cnae_principal": None,
        "role": "deputado",
    }[key]

    async def mock_run(cypher: str, params: dict, timeout: float = 15):  # type: ignore[no-untyped-def]
        result = AsyncMock()
        result.single = AsyncMock(return_value=score_record)
        return result

    session.run = mock_run

    response = await compute_exposure(session, "4:abc:2")
    assert response.peer_group == "Person (Person)"
    assert 0.0 <= response.exposure_index <= 100.0


@pytest.mark.anyio
async def test_compute_exposure_source_attribution() -> None:
    session = AsyncMock()

    score_record = MagicMock()
    score_record.__getitem__ = lambda self, key: {
        "entity_id": "4:abc:3",
        "entity_labels": ["Company"],
        "connection_count": 0,
        "source_count": 1,
        "financial_volume": 0.0,
        "cnae_principal": None,
        "role": None,
    }[key]

    async def mock_run(cypher: str, params: dict, timeout: float = 15):  # type: ignore[no-untyped-def]
        result = AsyncMock()
        result.single = AsyncMock(return_value=score_record)
        return result

    session.run = mock_run

    response = await compute_exposure(session, "4:abc:3")
    assert response.sources[0].database == "neo4j_analysis"

    # Each factor should have source attribution
    for factor in response.factors:
        assert len(factor.sources) > 0


def test_entity_score_query_traverses_same_as() -> None:
    """Verify entity_score.cypher aggregates across SAME_AS equivalents."""
    CypherLoader.clear_cache()
    cypher = CypherLoader.load("entity_score")
    assert "SAME_AS" in cypher
    # Ensures the query collects equivalent nodes
    assert "equivs" in cypher
    # Ensures SAME_AS links are excluded from connection counts
    assert "type(r) <> 'SAME_AS'" in cypher


def test_entity_timeline_query_traverses_same_as() -> None:
    """Verify entity_timeline.cypher includes events from SAME_AS equivalents."""
    CypherLoader.clear_cache()
    cypher = CypherLoader.load("entity_timeline")
    assert "SAME_AS" in cypher
    assert "equivs" in cypher
    assert "type(r) <> 'SAME_AS'" in cypher


def test_graph_expand_query_includes_same_as() -> None:
    """Verify graph_expand.cypher traverses SAME_AS relationships."""
    CypherLoader.clear_cache()
    cypher = CypherLoader.load("graph_expand")
    assert "SAME_AS" in cypher


def test_entity_connections_query_includes_same_as() -> None:
    """Verify entity_connections.cypher supports SAME_AS and optional probable links."""
    CypherLoader.clear_cache()
    cypher = CypherLoader.load("entity_connections")
    assert "SAME_AS" in cypher
    assert "POSSIBLE_SAME_AS" in cypher
    assert "$include_probable" in cypher


@pytest.mark.anyio
async def test_compute_exposure_aggregated_same_as_data() -> None:
    """Score service handles aggregated data from SAME_AS equivalent nodes."""
    session = AsyncMock()

    # Simulates aggregated data: higher connection count and multiple sources
    # from SAME_AS traversal across TSE candidate + CUIT person + author nodes
    score_record = MagicMock()
    score_record.__getitem__ = lambda self, key: {
        "entity_id": "4:abc:10",
        "entity_labels": ["Person"],
        "connection_count": 85,
        "source_count": 5,
        "financial_volume": 2_500_000.0,
        "cnae_principal": None,
        "role": "deputado",
    }[key]

    async def mock_run(cypher: str, params: dict, timeout: float = 15):  # type: ignore[no-untyped-def]
        result = AsyncMock()
        result.single = AsyncMock(return_value=score_record)
        return result

    session.run = mock_run

    response = await compute_exposure(session, "4:abc:10")
    assert response.entity_id == "4:abc:10"
    assert response.exposure_index > 0.0
    # High connection count from aggregated SAME_AS data → high percentile
    conn_factor = next(f for f in response.factors if f.name == "connections")
    assert conn_factor.percentile >= 90.0
    # Multiple sources from cross-pipeline traversal
    src_factor = next(f for f in response.factors if f.name == "sources")
    assert src_factor.percentile == 100.0
