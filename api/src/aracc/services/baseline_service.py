from typing import Any

from neo4j import AsyncSession, Record

from aracc.models.baseline import BaselineMetrics
from aracc.models.entity import SourceAttribution
from aracc.services.neo4j_service import execute_query

BASELINE_QUERIES: dict[str, str] = {
    "sector": "baseline_sector",
    "region": "baseline_region",
}


def _record_to_metrics(
    record: Record, dimension: str, key_field: str,
) -> BaselineMetrics:
    data: dict[str, Any] = {}
    for key in record:
        data[key] = record[key]

    return BaselineMetrics(
        company_name=data.get("company_name", ""),
        company_cuit=data.get("company_cuit", ""),
        company_id=data.get("company_id", ""),
        contract_count=int(data.get("contract_count", 0)),
        total_value=float(data.get("total_value", 0)),
        peer_count=int(data.get(f"{dimension}_companies", 0)),
        peer_avg_contracts=float(data.get(f"{dimension}_avg_contracts", 0)),
        peer_avg_value=float(data.get(f"{dimension}_avg_value", 0)),
        contract_ratio=float(data.get("contract_ratio", 0)),
        value_ratio=float(data.get("value_ratio", 0)),
        comparison_dimension=dimension,
        comparison_key=str(data.get(key_field, "")),
        sources=[SourceAttribution(database="neo4j_analysis")],
    )


async def run_baseline(
    session: AsyncSession,
    dimension: str,
    entity_id: str | None = None,
) -> list[BaselineMetrics]:
    if dimension not in BASELINE_QUERIES:
        return []

    query_name = BASELINE_QUERIES[dimension]
    records = await execute_query(session, query_name, {"entity_id": entity_id})

    key_field = "sector_cnae" if dimension == "sector" else "region"

    return [
        _record_to_metrics(record, dimension, key_field)
        for record in records
    ]


async def run_all_baselines(
    session: AsyncSession,
    entity_id: str | None = None,
) -> list[BaselineMetrics]:
    all_results: list[BaselineMetrics] = []
    for dimension in BASELINE_QUERIES:
        results = await run_baseline(session, dimension, entity_id)
        all_results.extend(results)
    return all_results
