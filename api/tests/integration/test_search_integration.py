import pytest
from httpx import AsyncClient


@pytest.mark.integration
@pytest.mark.anyio
async def test_fulltext_search(integration_client: AsyncClient) -> None:
    """Search for a seeded entity name."""
    response = await integration_client.get("/api/v1/search", params={"q": "CARLOS ALBERTO"})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "total" in data


@pytest.mark.integration
@pytest.mark.anyio
async def test_search_type_filter(integration_client: AsyncClient) -> None:
    """Search with entity type filter."""
    response = await integration_client.get(
        "/api/v1/search", params={"q": "SILVA", "type": "company"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "results" in data


@pytest.mark.integration
@pytest.mark.anyio
async def test_search_empty_results(integration_client: AsyncClient) -> None:
    """Search for a nonexistent entity returns empty results."""
    response = await integration_client.get(
        "/api/v1/search", params={"q": "XYZNONEXISTENT"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["results"] == []


@pytest.mark.integration
@pytest.mark.anyio
async def test_search_pagination(integration_client: AsyncClient) -> None:
    """Search with pagination parameters."""
    response = await integration_client.get(
        "/api/v1/search", params={"q": "SILVA", "page": 1, "size": 5}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["size"] == 5
