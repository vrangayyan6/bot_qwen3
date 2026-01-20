from __future__ import annotations

from typing import TypedDict, List
from typing_extensions import Annotated
from langgraph.graph import add_messages
import operator


class OverallState(TypedDict):
    messages: Annotated[list, add_messages]

    search_query: Annotated[List[dict], operator.add]
    web_research_result: Annotated[List[str], operator.add]
    sources_gathered: Annotated[List[str], operator.add]

    initial_search_query_count: int
    max_research_loops: int
    research_loop_count: int

    reasoning_model: str
    search_dir: str
