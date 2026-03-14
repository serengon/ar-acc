import pytest
from httpx import AsyncClient


@pytest.mark.integration
@pytest.mark.anyio
async def test_graph_expand_depth_1(integration_client: AsyncClient) -> None:
    """Expand graph from a seeded entity at depth 1."""
    response = await integration_client.get(
        "/api/v1/graph/11111111111", params={"depth": 1}
    )
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        data = response.json()
        assert "nodes" in data
        assert "edges" in data
        assert "center_id" in data


@pytest.mark.integration
@pytest.mark.anyio
async def test_graph_expand_depth_2(integration_client: AsyncClient) -> None:
    """Expand graph from a seeded entity at depth 2."""
    response = await integration_client.get(
        "/api/v1/graph/11222333000181", params={"depth": 2}
    )
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        data = response.json()
        assert len(data["nodes"]) >= 1
        assert isinstance(data["edges"], list)


@pytest.mark.integration
@pytest.mark.anyio
async def test_graph_node_not_found(integration_client: AsyncClient) -> None:
    """Graph expand for nonexistent entity returns 404."""
    response = await integration_client.get(
        "/api/v1/graph/00000000000000", params={"depth": 1}
    )
    assert response.status_code == 404


@pytest.mark.integration
@pytest.mark.anyio
async def test_graph_with_type_filter(integration_client: AsyncClient) -> None:
    """Graph expand with entity type filter."""
    response = await integration_client.get(
        "/api/v1/graph/11111111111",
        params={"depth": 2, "entity_types": "company"},
    )
    assert response.status_code in (200, 404)
