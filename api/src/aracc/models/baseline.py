from pydantic import BaseModel

from aracc.models.entity import SourceAttribution


class BaselineMetrics(BaseModel):
    company_name: str
    company_cuit: str
    company_id: str
    contract_count: int
    total_value: float
    peer_count: int
    peer_avg_contracts: float
    peer_avg_value: float
    contract_ratio: float
    value_ratio: float
    comparison_dimension: str
    comparison_key: str
    sources: list[SourceAttribution]


class BaselineResponse(BaseModel):
    entity_id: str
    comparisons: list[BaselineMetrics]
    total: int
