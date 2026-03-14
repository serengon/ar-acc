import pytest
from httpx import AsyncClient

from aracc.services.baseline_service import BASELINE_QUERIES


def test_baseline_query_files_exist() -> None:
    from aracc.services.neo4j_service import CypherLoader

    for dimension, query_name in BASELINE_QUERIES.items():
        try:
            CypherLoader.load(query_name)
        except FileNotFoundError:
            pytest.fail(
                f"Missing .cypher file for baseline {dimension}: {query_name}.cypher"
            )
        finally:
            CypherLoader.clear_cache()


def test_baseline_queries_cover_dimensions() -> None:
    assert "sector" in BASELINE_QUERIES
    assert "region" in BASELINE_QUERIES


@pytest.mark.anyio
async def test_baseline_invalid_dimension(client: AsyncClient) -> None:
    response = await client.get("/api/v1/baseline/test-id?dimension=invalid")
    assert response.status_code == 400
    assert "Invalid dimension" in response.json()["detail"]


@pytest.mark.anyio
async def test_baseline_endpoint_returns_200(client: AsyncClient) -> None:
    response = await client.get("/api/v1/baseline/test-id")
    assert response.status_code == 200
    data = response.json()
    assert "comparisons" in data
    assert "total" in data
    assert data["entity_id"] == "test-id"


@pytest.mark.anyio
async def test_baseline_with_sector_dimension(client: AsyncClient) -> None:
    response = await client.get("/api/v1/baseline/test-id?dimension=sector")
    assert response.status_code == 200
    data = response.json()
    assert data["entity_id"] == "test-id"


@pytest.mark.anyio
async def test_baseline_with_region_dimension(client: AsyncClient) -> None:
    response = await client.get("/api/v1/baseline/test-id?dimension=region")
    assert response.status_code == 200
    data = response.json()
    assert data["entity_id"] == "test-id"
