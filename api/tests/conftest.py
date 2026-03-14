from collections.abc import AsyncIterator
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient

from aracc.main import app
from aracc.services.auth_service import create_access_token


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    # Mock Neo4j driver so tests don't need a running database
    mock_driver = MagicMock()
    mock_driver.verify_connectivity = AsyncMock()
    mock_driver.close = AsyncMock()
    mock_session = AsyncMock()
    mock_driver.session.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_driver.session.return_value.__aexit__ = AsyncMock(return_value=None)
    app.state.neo4j_driver = mock_driver

    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def auth_headers() -> dict[str, str]:
    token = create_access_token("test-user-id")
    return {"Authorization": f"Bearer {token}"}
