from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_health_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert "default-src 'none'" in response.headers["content-security-policy"]


@pytest.mark.anyio
async def test_meta_health_has_security_headers(client: AsyncClient) -> None:
    with patch(
        "aracc.routers.meta.execute_query_single",
        new_callable=AsyncMock,
        return_value={"ok": 1},
    ):
        response = await client.get("/api/v1/meta/health")

    assert response.status_code == 200
    assert response.json() == {"neo4j": "connected"}
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"


@pytest.mark.anyio
async def test_meta_sources(client: AsyncClient) -> None:
    response = await client.get("/api/v1/meta/sources")
    assert response.status_code == 200
    data = response.json()
    assert "sources" in data
    if len(data["sources"]) == 0:
        pytest.skip("Source registry CSV not found — skip until AR registry is created")
    first = data["sources"][0]
    assert "status" in first
    assert "implementation_state" in first
    assert "load_state" in first
    assert "in_universe_v1" in first
    assert "discovery_status" in first
    assert "last_seen_url" in first
    assert "public_access_mode" in first
    assert "quality_status" in first


@pytest.mark.anyio
async def test_meta_stats(client: AsyncClient) -> None:
    mock_record = {
        "total_nodes": 87_500_000,
        "total_relationships": 53_100_000,
        "person_count": 2_450_000,
        "company_count": 58_500_000,
        "health_count": 602_000,
        "finance_count": 24_000_000,
        "contract_count": 1_080_000,
        "sanction_count": 69_000,
        "election_count": 17_000,
        "amendment_count": 98_000,
        "embargo_count": 79_000,
        "education_count": 224_000,
        "convenio_count": 67_000,
        "laborstats_count": 29_500,
        "offshore_entity_count": 810_000,
        "offshore_officer_count": 500_000,
        "global_pep_count": 15_000,
        "cvm_proceeding_count": 5_000,
        "expense_count": 2_000_000,
        "pep_record_count": 100_000,
        "expulsion_count": 10_000,
        "leniency_count": 34,
        "international_sanction_count": 12_000,
        "gov_card_expense_count": 500_000,
        "gov_travel_count": 150_000,
        "bid_count": 2_000_000,
        "fund_count": 30_000,
        "dou_act_count": 50_000,
        "tax_waiver_count": 800_000,
        "municipal_finance_count": 100_000,
        "declared_asset_count": 5_000_000,
        "party_membership_count": 15_000_000,
        "barred_ngo_count": 5_000,
        "bcb_penalty_count": 10_000,
        "labor_movement_count": 2_000_000,
        "legal_case_count": 100_000,
        "judicial_case_count": 50_000,
        "cpi_count": 500,
        "inquiry_requirement_count": 2_500,
        "inquiry_session_count": 1_400,
        "municipal_bid_count": 8_000_000,
        "municipal_contract_count": 6_000_000,
        "municipal_gazette_act_count": 4_000_000,
    }

    # Reset the stats cache between tests
    import aracc.routers.meta as meta_module
    meta_module._stats_cache = None
    meta_module._stats_cache_time = 0.0

    with patch(
        "aracc.routers.meta.execute_query_single",
        new_callable=AsyncMock,
        return_value=mock_record,
    ):
        response = await client.get("/api/v1/meta/stats")

    assert response.status_code == 200
    data = response.json()

    assert data["total_nodes"] == 87_500_000
    assert data["total_relationships"] == 53_100_000
    assert data["person_count"] == 2_450_000
    assert data["company_count"] == 58_500_000
    assert data["health_count"] == 602_000
    assert data["finance_count"] == 24_000_000
    assert data["contract_count"] == 1_080_000
    assert data["sanction_count"] == 69_000
    assert data["election_count"] == 17_000
    assert data["amendment_count"] == 98_000
    assert data["embargo_count"] == 79_000
    assert data["education_count"] == 224_000
    assert data["convenio_count"] == 67_000
    assert data["laborstats_count"] == 29_500
    assert data["offshore_entity_count"] == 810_000
    assert data["offshore_officer_count"] == 500_000
    assert data["global_pep_count"] == 15_000
    assert data["cvm_proceeding_count"] == 5_000
    assert data["expense_count"] == 2_000_000
    assert data["pep_record_count"] == 100_000
    assert data["expulsion_count"] == 10_000
    assert data["leniency_count"] == 34
    assert data["international_sanction_count"] == 12_000
    assert data["gov_card_expense_count"] == 500_000
    assert data["gov_travel_count"] == 150_000
    assert data["bid_count"] == 2_000_000
    assert data["fund_count"] == 30_000
    assert data["dou_act_count"] == 50_000
    assert data["tax_waiver_count"] == 800_000
    assert data["municipal_finance_count"] == 100_000
    assert data["declared_asset_count"] == 5_000_000
    assert data["party_membership_count"] == 15_000_000
    assert data["barred_ngo_count"] == 5_000
    assert data["bcb_penalty_count"] == 10_000
    assert data["labor_movement_count"] == 2_000_000
    assert data["legal_case_count"] == 100_000
    assert data["judicial_case_count"] == 50_000
    assert data["cpi_count"] == 500
    assert data["inquiry_requirement_count"] == 2_500
    assert data["inquiry_session_count"] == 1_400
    assert data["municipal_bid_count"] == 8_000_000
    assert data["municipal_contract_count"] == 6_000_000
    assert data["municipal_gazette_act_count"] == 4_000_000
    assert data["source_document_count"] == 0
    assert data["ingestion_run_count"] == 0
    assert data["temporal_violation_count"] == 0
    assert data["data_sources"] >= 0
    assert data["implemented_sources"] >= 0
    assert data["loaded_sources"] >= 0
    assert data["healthy_sources"] >= 0
    assert data["stale_sources"] >= 0
    assert data["blocked_external_sources"] >= 0
    assert data["quality_fail_sources"] >= 0
    assert data["discovered_uningested_sources"] >= 0
