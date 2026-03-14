from pydantic import BaseModel

from aracc.models.entity import SourceAttribution


class SearchResult(BaseModel):
    id: str
    type: str
    name: str
    score: float
    document: str | None = None
    properties: dict[str, str | float | int | bool | None]
    sources: list[SourceAttribution]
    exposure_tier: str = "public_safe"


class SearchResponse(BaseModel):
    results: list[SearchResult]
    total: int
    page: int
    size: int
