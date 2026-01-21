import os

from agent.tools_and_schemas import SearchQueryList, Reflection
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langgraph.types import Send
from langgraph.graph import StateGraph
from langgraph.graph import START, END
from langchain_core.runnables import RunnableConfig

from agent.state import (
    OverallState,
    QueryGenerationState,
    ReflectionState,
    WebSearchState,
)
from agent.configuration import Configuration
from agent.prompts import (
    get_current_date,
    query_writer_instructions,
    reflection_instructions,
    answer_instructions,
)
from langchain_groq import ChatGroq
from agent.utils import get_research_topic
import glob
import re
from pathlib import Path

load_dotenv()

if os.getenv("GROQ_API_KEY") is None:
    raise ValueError("GROQ_API_KEY is not set")


# Nodes
def generate_query(state: OverallState, config: RunnableConfig) -> QueryGenerationState:
    """LangGraph node that generates search queries based on the User's question.

    Uses Groq (llama-3.3-70b-versatile) to create optimized search queries for web
    research based on the User's question.

    Args:
        state: Current graph state containing the User's question
        config: Configuration for the runnable, including LLM provider settings

    Returns:
        Dictionary with state update, including search_query key containing the generated queries
    """
    configurable = Configuration.from_runnable_config(config)

    # Limit query count to reduce token usage
    state["initial_search_query_count"] = 2

    # init Groq LLM
    llm = ChatGroq(
        model=configurable.query_generator_model,
        temperature=0,
        max_retries=2,
        api_key=os.getenv("GROQ_API_KEY"),
    )
    structured_llm = llm.with_structured_output(SearchQueryList)

    current_date = get_current_date()
    formatted_prompt = query_writer_instructions.format(
        current_date=current_date,
        research_topic=get_research_topic(state["messages"]),
        number_queries=state["initial_search_query_count"],
    )
    # Generate the search queries
    result = structured_llm.invoke(formatted_prompt)
    return {"search_query": result.query}


def continue_to_web_research(state: QueryGenerationState):
    """LangGraph node that sends the search queries to the web research node.

    This is used to spawn n number of web research nodes, one for each search query.
    """
    return [
        Send(
            "web_research",
            {
                "search_query": search_query,
                "id": idx,
                "docs_dir": state.get("docs_dir"),
            },
        )
        for idx, search_query in enumerate(state["search_query"])
    ]


def web_research(state: WebSearchState, config: RunnableConfig) -> OverallState:
    """LangGraph node that performs local markdown search instead of Google Search."""
    docs_dir = state.get("docs_dir")
    if not docs_dir:
        return {
            "sources_gathered": [],
            "web_research_result": [
                "Web search skipped: no docs_dir provided for local markdown search."
            ],
            "search_query": [state.get("search_query", "")],
        }

    search_query = state["search_query"]
    snippets = _search_markdown_directory(docs_dir, search_query, top_k=2)

    if not snippets:
        return {
            "sources_gathered": [],
            "web_research_result": [
                f"No local markdown results found for query: {search_query}"
            ],
            "search_query": [search_query],
        }

    sources = []
    result_chunks = []
    for idx, (rel_path, snippet) in enumerate(snippets):
        marker = f"[S{idx}]"
        sources.append({"short_url": marker, "value": rel_path})
        result_chunks.append(f"{marker} {rel_path}\n{snippet}")

    return {
        "sources_gathered": sources,
        "web_research_result": ["\n\n---\n\n".join(result_chunks)],
        "search_query": [search_query],
    }


def reflection(state: OverallState, config: RunnableConfig) -> ReflectionState:
    """LangGraph node that identifies knowledge gaps and generates potential follow-up queries.

    Analyzes the current summary to identify areas for further research and generates
    potential follow-up queries. Uses structured output to extract
    the follow-up query in JSON format.

    Args:
        state: Current graph state containing the running summary and research topic
        config: Configuration for the runnable, including LLM provider settings

    Returns:
        Dictionary with state update including is_sufficient, knowledge_gap, follow_up_queries, research_loop_count, and number_of_ran_queries
    """
    configurable = Configuration.from_runnable_config(config)
    # Increment the research loop count and get the reasoning model
    state["research_loop_count"] = state.get("research_loop_count", 0) + 1
    reasoning_model = state.get("reasoning_model", configurable.reflection_model)

    current_date = get_current_date()
    formatted_prompt = reflection_instructions.format(
        current_date=current_date,
        research_topic=get_research_topic(state["messages"]),
            summaries="\n\n---\n\n".join(state["web_research_result"]),
    )
    llm = ChatGroq(
        model=reasoning_model,
        temperature=1.0,
        max_retries=2,
        api_key=os.getenv("GROQ_API_KEY"),
    )
    result = llm.with_structured_output(Reflection).invoke(formatted_prompt)

    return {
        "is_sufficient": result.is_sufficient,
        "knowledge_gap": result.knowledge_gap,
        "follow_up_queries": result.follow_up_queries,
        "research_loop_count": state["research_loop_count"],
        "number_of_ran_queries": len(state.get("search_query", [])),
    }


def evaluate_research(
    state: ReflectionState,
    config: RunnableConfig,
) -> OverallState:
    """LangGraph routing function that determines the next step in the research flow.

    Controls the research loop by deciding whether to continue gathering information
    or to finalize the summary based on the configured maximum number of research loops.

    Args:
        state: Current graph state containing the research loop count
        config: Configuration for the runnable, including max_research_loops setting

    Returns:
        String "finalize_answer" or list of Send objects for "web_research" nodes
    """
    configurable = Configuration.from_runnable_config(config)
    max_research_loops = (
        state.get("max_research_loops")
        if state.get("max_research_loops") is not None
        else configurable.max_research_loops
    )
    if state["is_sufficient"] or state["research_loop_count"] >= max_research_loops:
        return "finalize_answer"
    else:
        return [
            Send(
                "web_research",
                {
                    "search_query": follow_up_query,
                    "id": state["number_of_ran_queries"] + idx,
                    "docs_dir": state.get("docs_dir"),
                },
            )
            for idx, follow_up_query in enumerate(state["follow_up_queries"])
        ]


def finalize_answer(state: OverallState, config: RunnableConfig):
    """LangGraph node that finalizes the research summary.

    Prepares the final output by deduplicating and formatting sources, then
    combining them with the running summary to create a well-structured
    research report with proper citations.

    Args:
        state: Current graph state containing the running summary and sources gathered

    Returns:
        Dictionary with state update, including running_summary key containing the formatted final summary with sources
    """
    configurable = Configuration.from_runnable_config(config)
    reasoning_model = state.get("reasoning_model") or configurable.answer_model

    current_date = get_current_date()

    # Filter out error messages and keep only valid content chunks
    all_results = state.get("web_research_result", [])
    valid_chunks = [
        r for r in all_results
        if not ("No local markdown results found" in r or "no docs_dir provided" in r or "Web search skipped" in r)
        and r.strip()
    ]

    if not valid_chunks:
        formatted_prompt = (
            "I could not find sufficient information in the provided documentation to answer this question."
        )
    else:
        # Normal prompt with citations if sources exist
        formatted_prompt = answer_instructions.format(
            current_date=current_date,
            research_topic=get_research_topic(state["messages"]),
            summaries="\n---\n\n".join(valid_chunks),
        )

    llm = ChatGroq(
        model=reasoning_model,
        temperature=0,
        max_retries=2,
        api_key=os.getenv("GROQ_API_KEY"),
    )
    result = llm.invoke(formatted_prompt)

    fallback_msg = "I could not find sufficient information in the provided documentation to answer this question."
    content = result.content if hasattr(result, "content") else ""
    content = content.strip() if isinstance(content, str) else ""

    if content != fallback_msg and not re.search(r"\[S\d+\]", content):
        content = fallback_msg

    if content == fallback_msg:
        return {"messages": [AIMessage(content=fallback_msg)], "sources_gathered": []}
    if not content:
        return {"messages": [AIMessage(content=fallback_msg)], "sources_gathered": []}

    source_map: dict[str, str] = {}
    for source in state.get("sources_gathered", []):
        if not isinstance(source, dict):
            continue
        key = source.get("short_url")
        val = source.get("value")
        if isinstance(key, str) and isinstance(val, str) and key not in source_map:
            source_map[key] = val
    used_markers = []
    for marker in re.findall(r"\[S\d+\]", content):
        if marker in source_map and marker not in used_markers:
            used_markers.append(marker)

    if not used_markers:
        return {"messages": [AIMessage(content=fallback_msg)], "sources_gathered": []}

    sources_lines = [
        f"- {m} -> [{source_map[m]}]({source_map[m]})"
        for m in used_markers
    ]
    content = f"{content}\n\nSources:\n" + "\n".join(sources_lines)

    return {"messages": [AIMessage(content=content)], "sources_gathered": state.get("sources_gathered", [])}


def _search_markdown_directory(base_dir: str, query: str, top_k: int = 5):
    """Search recursively for markdown files and return top-k relevant snippets.

    Scores files based on keyword and phrase matching in both file paths and content.
    Uses a weighted scoring system: path matches (3x), phrase matches (3x), term matches (1x).
    Requires minimum score threshold (2 term matches or 1 phrase match) to include results.
    Extracts line-based snippets around the best match position for deterministic grounding.

    Args:
        base_dir: Base directory path (resolved to absolute) to search recursively for .md files.
        query: Search query string to match against file content and paths.
        top_k: Maximum number of results to return (default: 5).

    Returns:
        List of tuples (relative_path, snippet) sorted by relevance score descending.
    """
    base_path = Path(base_dir).resolve()
    if not base_path.exists():
        return []

    # Collect files
    md_files = [Path(p) for p in glob.glob(str(base_path / "**" / "*.md"), recursive=True)]
    if not md_files:
        return []

    # Small set of common English stopwords for filtering
    STOPWORDS = {
        "the", "a", "an", "in", "on", "of", "for", "to", "and", "or", "is", "are", "was", "were", "with", "by",
        "at", "it", "as", "that", "from", "be", "this", "which"
    }

    query_lower = query.lower()
    # Extract individual terms, filter stopwords
    terms = [t.lower() for t in re.findall(r"\w+", query) if t]
    terms = [t for t in terms if t not in STOPWORDS]

    # Extract multi-word phrases (2-3 words)
    phrases = []
    words = [w for w in re.findall(r"\w+", query_lower) if w not in STOPWORDS]
    for i in range(len(words) - 1):
        phrases.append(f"{words[i]} {words[i+1]}")
    for i in range(len(words) - 2):
        phrases.append(f"{words[i]} {words[i+1]} {words[i+2]}")

    def score_and_snippet(path: Path):
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            return 0, ""

        rel_path = str(path.relative_to(base_path))
        path_lower = rel_path.lower()
        text_lower = text.lower()

        # Score file path matches (boost)
        path_score = sum(path_lower.count(t) * 3 for t in terms) + sum(path_lower.count(p) * 5 for p in phrases)

        # Score content matches
        term_score = sum(text_lower.count(t) for t in terms) if terms else 0
        phrase_score = sum(text_lower.count(p) * 3 for p in phrases)

        # Require at least 2 term matches or 1 phrase match
        total_score = path_score + term_score + phrase_score
        if total_score < 2 and phrase_score == 0:
            return 0, ""

        # Find best match position (prefer phrase matches, then term matches)
        best_idx = len(text)
        best_token = None
        for p in phrases:
            idx = text_lower.find(p)
            if idx != -1:
                best_idx = min(best_idx, idx)
                if best_token is None or idx == best_idx:
                    best_token = p
        if best_idx == len(text):
            for t in terms:
                idx = text_lower.find(t)
                if idx != -1:
                    best_idx = min(best_idx, idx)
                    if best_token is None or idx == best_idx:
                        best_token = t

        # Extract line-based snippet around the best match for more deterministic grounding
        lines = text.splitlines()
        if best_token:
            match_line = 0
            for i, line in enumerate(lines):
                if best_token in line.lower():
                    match_line = i
                    break
            # Capture 20 lines before and 100 lines after to ensure we get the full code example
            start_line = max(0, match_line - 20)
            end_line = min(len(lines), match_line + 100)
        else:
            start_line, end_line = 0, min(len(lines), 120)
        snippet = "\n".join(lines[start_line:end_line]).strip()
        return total_score, snippet

    scored = []
    for path in md_files:
        score, snippet = score_and_snippet(path)
        if score > 0 and snippet:
            rel_path = str(path.relative_to(base_path))
            scored.append((score, rel_path, snippet))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [(rel_path, snippet) for _, rel_path, snippet in scored[:top_k]]


# Create our Agent Graph
builder = StateGraph(OverallState, config_schema=Configuration)

# Define the nodes we will cycle between
builder.add_node("generate_query", generate_query)
builder.add_node("web_research", web_research)
builder.add_node("reflection", reflection)
builder.add_node("finalize_answer", finalize_answer)

# Set the entrypoint as `generate_query`
# This means that this node is the first one called
builder.add_edge(START, "generate_query")
# Add conditional edge to continue with search queries in a parallel branch
builder.add_conditional_edges(
    "generate_query", continue_to_web_research, ["web_research"]
)
# Reflect on the web research
builder.add_edge("web_research", "reflection")
# Evaluate the research
builder.add_conditional_edges(
    "reflection", evaluate_research, ["web_research", "finalize_answer"]
)
# Finalize the answer
builder.add_edge("finalize_answer", END)

graph = builder.compile(name="pro-search-agent")
