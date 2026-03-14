import math

from neo4j import AsyncSession

from aracc.models.entity import ExposureFactor, ExposureResponse, SourceAttribution
from aracc.services.neo4j_service import execute_query_single

# Weights for each factor in the exposure index formula
FACTOR_WEIGHTS = {
    "connections": 0.25,
    "sources": 0.25,
    "financial": 0.20,
    "patterns": 0.20,
    "baseline": 0.10,
}


def _conn_percentile(count: int) -> float:
    """Heuristic percentile for connection count (power-law distribution)."""
    if count == 0:
        return 0.0
    if count <= 2:
        return 25.0
    if count <= 5:
        return 50.0
    if count <= 15:
        return 75.0
    if count <= 50:
        return 90.0
    return min(99.0, 90.0 + math.log10(count) * 3)


def _fin_percentile(volume: float) -> float:
    """Heuristic percentile for financial volume (log-normal distribution)."""
    if volume <= 0:
        return 0.0
    log_v = math.log10(volume + 1)
    # 100K = 5, 1M = 6, 10M = 7, 100M = 8, 1B = 9
    if log_v < 5:
        return min(25.0, log_v * 5)
    if log_v < 6:
        return 25.0 + (log_v - 5) * 25
    if log_v < 7:
        return 50.0 + (log_v - 6) * 25
    if log_v < 8:
        return 75.0 + (log_v - 7) * 15
    return min(99.0, 90.0 + (log_v - 8) * 5)


async def compute_exposure(
    session: AsyncSession,
    entity_id: str,
) -> ExposureResponse:
    """Compute the exposure index for a given entity."""
    record = await execute_query_single(
        session, "entity_score", {"entity_id": entity_id}
    )
    if record is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Entity not found")

    connection_count = int(record["connection_count"])
    source_count = int(record["source_count"])
    financial_volume = float(record["financial_volume"])
    entity_labels: list[str] = record["entity_labels"]
    cnae = record["cnae_principal"]

    is_company = "Company" in entity_labels

    # Determine peer group label
    if is_company and cnae:
        peer_group = f"CNAE {cnae}"
    elif is_company:
        peer_group = "Company (all)"
    else:
        entity_type = entity_labels[0] if entity_labels else "Unknown"
        peer_group = f"Person ({entity_type})"

    # Heuristic percentiles — avoids 20s peer sampling query on 56M nodes
    conn_percentile = _conn_percentile(connection_count)
    fin_percentile = _fin_percentile(financial_volume)

    # Source percentile: scale 0-4 sources to 0-100
    source_percentile = min(source_count * 25.0, 100.0)

    # Pattern and baseline factors — defaults until pattern count is available
    pattern_percentile = 0.0
    baseline_percentile = 0.0

    # Build factors
    factors: list[ExposureFactor] = [
        ExposureFactor(
            name="connections",
            value=float(connection_count),
            percentile=conn_percentile,
            weight=FACTOR_WEIGHTS["connections"],
            sources=["neo4j_graph"],
        ),
        ExposureFactor(
            name="sources",
            value=float(source_count),
            percentile=source_percentile,
            weight=FACTOR_WEIGHTS["sources"],
            sources=["neo4j_graph"],
        ),
        ExposureFactor(
            name="financial",
            value=financial_volume,
            percentile=fin_percentile,
            weight=FACTOR_WEIGHTS["financial"],
            sources=["transparencia", "tse"],
        ),
        ExposureFactor(
            name="patterns",
            value=0.0,
            percentile=pattern_percentile,
            weight=FACTOR_WEIGHTS["patterns"],
            sources=["neo4j_analysis"],
        ),
        ExposureFactor(
            name="baseline",
            value=0.0,
            percentile=baseline_percentile,
            weight=FACTOR_WEIGHTS["baseline"],
            sources=["neo4j_analysis"],
        ),
    ]

    # Compute weighted exposure index
    total_weight = sum(f.weight for f in factors)
    if total_weight > 0:
        exposure_index = sum(f.percentile * f.weight for f in factors) / total_weight
    else:
        exposure_index = 0.0

    # Clamp to 0-100
    exposure_index = max(0.0, min(100.0, round(exposure_index, 2)))

    return ExposureResponse(
        entity_id=entity_id,
        exposure_index=exposure_index,
        factors=factors,
        peer_group=peer_group,
        peer_count=0,
        sources=[SourceAttribution(database="neo4j_analysis")],
    )
