import logging
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query
from neo4j import AsyncSession

from aracc.constants import PEP_ROLES
from aracc.dependencies import get_session
from aracc.models.entity import SourceAttribution
from aracc.models.graph import GraphEdge, GraphNode, GraphResponse
from aracc.services.neo4j_service import execute_query, sanitize_props
from aracc.services.public_guard import (
    enforce_entity_lookup_enabled,
    enforce_person_access_policy,
    has_person_labels,
    infer_exposure_tier,
    sanitize_public_properties,
    should_hide_person_entities,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/graph", tags=["graph"])

_GRAPH_PROPS = {
    "name", "razao_social", "cuit", "cuil", "value", "date",
    "type", "uf", "cargo", "partido",
}

_DEFAULT_LABEL_FILTER = "-User|-Investigation|-Annotation|-Tag"

_LABEL_MAP: dict[str, str] = {
    "person": "Person",
    "company": "Company",
    "contract": "Contract",
    "sanction": "Sanction",
    "election": "Election",
    "amendment": "Amendment",
    "finance": "Finance",
    "embargo": "Embargo",
    "health": "Health",
    "education": "Education",
    "convenio": "Convenio",
    "laborstats": "LaborStats",
}


def _is_pep(properties: dict[str, Any]) -> bool:
    role = str(properties.get("role", "")).lower()
    return any(keyword in role for keyword in PEP_ROLES)


def _extract_label(node: Any, labels: list[str]) -> str:
    props = dict(node)
    entity_type = labels[0].lower() if labels else ""
    if entity_type == "company":
        return str(props.get("razao_social", props.get("name", props.get("nome_fantasia", ""))))
    if entity_type == "finance":
        if props.get("value"):
            return f"Finance: R$ {props.get('value', 0):,.2f}"
        return str(props.get("type", "Finance"))
    if entity_type == "embargo":
        return str(props.get("description", props.get("uf", "Embargo")))
    if entity_type == "convenio":
        return str(props.get("object", props.get("convenio_id", "Convenio")))
    return str(props.get("name", str(props.get("id", ""))))


def _slim_props(node_props: dict[str, Any]) -> dict[str, str | float | int | bool | None]:
    """Return only essential properties for graph rendering, with scalar values."""
    return sanitize_props({k: v for k, v in node_props.items() if k in _GRAPH_PROPS})


def _build_label_filter(type_list: list[str] | None) -> str:
    """Build APOC labelFilter string from requested entity types.

    When types are specified, include only those labels (with +) and
    exclude internal labels. When no types, use negative-only filter.
    """
    if not type_list:
        return _DEFAULT_LABEL_FILTER

    parts: list[str] = []
    for t in type_list:
        neo4j_label = _LABEL_MAP.get(t)
        if neo4j_label:
            parts.append(f"+{neo4j_label}")

    if not parts:
        return _DEFAULT_LABEL_FILTER

    # APOC labelFilter: +Label = whitelist, -Label = blacklist.
    # The start node is always included in subgraphAll results.
    return "|".join(parts) + "|-User|-Investigation|-Annotation|-Tag"


@router.get("/{entity_id}", response_model=GraphResponse)
async def get_graph(
    entity_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
    depth: Annotated[int, Query(ge=1, le=4)] = 2,
    entity_types: Annotated[str | None, Query()] = None,
) -> GraphResponse:
    enforce_entity_lookup_enabled()
    type_list = [t.strip().lower() for t in entity_types.split(",")] if entity_types else None

    # Degree guard: cap depth to 1 for supernodes to prevent explosion
    degree_records = await execute_query(
        session, "node_degree", {"entity_id": entity_id}, timeout=5,
    )
    if not degree_records:
        raise HTTPException(status_code=404, detail="Entity not found")

    degree = degree_records[0]["degree"] if degree_records else 0
    if degree > 500:
        logger.info(
            "Supernode detected (degree=%d) for %s, capping depth to 1",
            degree, entity_id,
        )
        depth = min(depth, 1)

    label_filter = _build_label_filter(type_list)

    records = await execute_query(
        session,
        "graph_expand",
        {"entity_id": entity_id, "label_filter": label_filter, "depth": depth},
        timeout=5,
    )

    if not records:
        raise HTTPException(status_code=404, detail="Entity not found")

    record = records[0]
    raw_nodes = record["nodes"]
    raw_rels = record["relationships"]
    center_id = record["center_id"]

    # Parse nodes
    nodes: list[GraphNode] = []
    node_ids: set[str] = set()

    for node in raw_nodes:
        node_id = node.element_id
        labels = list(node.labels)
        if should_hide_person_entities() and has_person_labels(labels):
            if node_id == center_id:
                enforce_person_access_policy(labels)
            continue

        node_ids.add(node_id)
        props = dict(node)
        source_val = props.pop("source", None)
        sources: list[SourceAttribution] = []
        if isinstance(source_val, str):
            sources = [SourceAttribution(database=source_val)]
        elif isinstance(source_val, list):
            sources = [SourceAttribution(database=s) for s in source_val]

        doc_id = (
            props.get("cuil")
            or props.get("cuit")
            or props.get("contract_id")
            or props.get("sanction_id")
            or props.get("amendment_id")
            or props.get("cnes_code")
            or props.get("finance_id")
            or props.get("embargo_id")
            or props.get("school_id")
            or props.get("convenio_id")
            or props.get("stats_id")
        )
        document_id = str(doc_id) if doc_id else None

        nodes.append(GraphNode(
            id=node_id,
            label=_extract_label(node, labels),
            type=labels[0].lower() if labels else "unknown",
            document_id=document_id,
            properties=sanitize_public_properties(_slim_props(props)),
            sources=sources,
            is_pep=_is_pep(props),
            exposure_tier=infer_exposure_tier(labels),
        ))

    # Parse edges — only between accepted nodes
    edges: list[GraphEdge] = []
    seen_edges: set[str] = set()

    for rel in raw_rels:
        rel_id = rel.element_id
        if rel_id in seen_edges:
            continue
        seen_edges.add(rel_id)

        source_id = rel.start_node.element_id
        target_id = rel.end_node.element_id

        if source_id not in node_ids or target_id not in node_ids:
            continue

        rel_props = dict(rel)
        confidence = float(rel_props.pop("confidence", 1.0))
        rel_source_val = rel_props.pop("source", None)
        rel_sources: list[SourceAttribution] = []
        if isinstance(rel_source_val, str):
            rel_sources = [SourceAttribution(database=rel_source_val)]
        elif isinstance(rel_source_val, list):
            rel_sources = [SourceAttribution(database=s) for s in rel_source_val]

        edges.append(GraphEdge(
            id=rel_id,
            source=source_id,
            target=target_id,
            type=rel.type,
            properties=sanitize_public_properties(sanitize_props(rel_props)),
            confidence=confidence,
            sources=rel_sources,
            exposure_tier="public_safe",
        ))

    return GraphResponse(nodes=nodes, edges=edges, center_id=center_id)
