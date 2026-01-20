from typing import List
from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    query: str
    rationale: str


class SearchQueryList(BaseModel):
    query: List[SearchQuery]


class Reflection(BaseModel):
    is_sufficient: bool = Field(..., description="Is research sufficient?")
    knowledge_gap: str = Field(..., description="What is missing?")
    follow_up_queries: List[SearchQuery] = Field(default_factory=list)
