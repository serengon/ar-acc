import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_graph_rejects_invalid_depth(client: AsyncClient) -> None:
    response = await client.get("/api/v1/graph/test-id?depth=5")
    assert response.status_code == 422


@pytest.mark.anyio
async def test_graph_accepts_valid_depth(client: AsyncClient) -> None:
    response = await client.get("/api/v1/graph/test-id?depth=2")
    assert response.status_code != 422


@pytest.mark.anyio
async def test_graph_accepts_entity_types_filter(client: AsyncClient) -> None:
    response = await client.get("/api/v1/graph/test-id?entity_types=person,company")
    assert response.status_code != 422
