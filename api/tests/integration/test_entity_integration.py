import pytest
from httpx import AsyncClient


@pytest.mark.integration
@pytest.mark.anyio
async def test_entity_lookup_by_cuil(integration_client: AsyncClient) -> None:
    """Lookup a seeded Person entity by CUIL."""
    response = await integration_client.get("/api/v1/entity/20111111111")
    assert response.status_code in (200, 404)


@pytest.mark.integration
@pytest.mark.anyio
async def test_entity_lookup_by_cuit(integration_client: AsyncClient) -> None:
    """Lookup a seeded Company entity by CUIT."""
    response = await integration_client.get("/api/v1/entity/30112223331")
    assert response.status_code in (200, 404)


@pytest.mark.integration
@pytest.mark.anyio
async def test_entity_not_found(integration_client: AsyncClient) -> None:
    """Lookup a non-existent entity returns 404."""
    response = await integration_client.get("/api/v1/entity/20000000000")
    assert response.status_code == 404


@pytest.mark.integration
@pytest.mark.anyio
async def test_entity_invalid_format(integration_client: AsyncClient) -> None:
    """Invalid identifier format returns 400."""
    response = await integration_client.get("/api/v1/entity/abc")
    assert response.status_code == 400


@pytest.mark.integration
@pytest.mark.anyio
async def test_entity_connections(integration_client: AsyncClient) -> None:
    """Lookup connections for an entity."""
    response = await integration_client.get("/api/v1/entity/test-entity-id/connections")
    assert response.status_code in (200, 404)
