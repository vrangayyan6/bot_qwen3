# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A local research agent powered by LangGraph that autonomously performs web research using DuckDuckGo and reasoning with local LLMs (Ollama). The agent iteratively generates search queries, performs web research, reflects on findings to identify knowledge gaps, and generates follow-up queries until sufficient research is completed.

## Architecture

### High-Level Flow

The research agent is defined in `agent/graph.py` as a LangGraph state machine with the following flow:

1. **generate_query** - Takes user's question, generates initial search queries using `query_generator_model`
2. **continue_to_web_research** - Routes each query to web_research node in parallel (map/reduce pattern)
3. **web_research** - Searches DuckDuckGo for each query, summarizes results using `answer_model`
4. **reflection** - Evaluates if research is sufficient, identifies knowledge gaps, generates follow-up queries using `reflection_model`
5. **evaluate_research** - Conditional router: either finalize answer or loop back to web_research
6. **finalize_answer** - Generates final comprehensive answer using `reasoning_model`

### State Management

The `OverallState` (defined in `agent/state.py`) accumulates data across the graph:
- `messages` - Chat history (user question + agent responses)
- `search_query` - List of all queries run (accumulates across loops)
- `web_research_result` - List of summarized search results
- `sources_gathered` - Metadata about sources found (title, link, snippet)
- `research_loop_count` - Current iteration number
- `initial_search_query_count` - Number of initial queries to generate
- `max_research_loops` - Max iterations before stopping
- `reasoning_model` - Can override the model for a specific run

### Configuration

Configuration is defined in `agent/configuration.py` and supports three resolution levels (lowest to highest priority):
1. Default values in Configuration class
2. Environment variables (uppercase, e.g., `QUERY_GENERATOR_MODEL`)
3. Runtime config passed to `graph.invoke(config={"configurable": {...}})`

Key configuration fields:
- `query_generator_model` - Model for initial query generation (default: `qwen3:4b`)
- `reflection_model` - Model for gap analysis and follow-ups (default: `qwen3:4b`)
- `answer_model` - Model for search result summarization and final answer (default: `qwen3:4b`)
- `number_of_initial_queries` - Starting query count (default: 1)
- `max_research_loops` - Maximum research iterations (default: 2)
- `max_context_tokens` - Token limit for search results trimming (default: 3000)
- `ollama_base_url` - Ollama server URL (default: `http://localhost:11434`)

## Entry Points

### CLI
```bash
python cli_research.py "Your research question" \
  --initial-queries 2 \
  --max-loops 3 \
  --reasoning-model gemma3n:e2b
```
Simple command-line interface for batch processing.

### Streamlit UI
```bash
streamlit run streamlit_app.py
```
Interactive chat interface (implied from README; check if `streamlit_app.py` exists).

### FastAPI Server
The `agent/app.py` defines a FastAPI application that serves the LangGraph agent via the LangGraph API. The graph is registered in `langgraph.json`:
- Graph: `./agent/graph.py:graph` (exposed as `/graph/agent`)
- HTTP app: `./agent/app.py:app`

### Jupyter Notebooks
- `langgraph_ollama.ipynb` - Development/testing notebook for the research agent
- `langgraph_nova.ipynb` - Alternative/experimental version (possibly using a different model)

## Common Development Commands

### Linting and Formatting

```bash
make format         # Format all code (ruff)
make lint           # Run all linters (ruff + mypy)
make spell_check    # Check spelling with codespell
make spell_fix      # Auto-fix spelling
```

Check specific file:
```bash
uv run ruff format agent/graph.py
uv run ruff check --select I agent/
```

### Testing

```bash
make test                                # Run unit tests
make test TEST_FILE=tests/unit_tests/test_graph.py  # Run specific test
make test_watch                          # Watch mode (requires pytest-watcher)
```

Tests should be placed in `tests/unit_tests/` (directory structure implied by Makefile).

### Installation

```bash
pip install -e .[ui]     # Install with UI dependencies (Streamlit, dotenv, ddgs)
pip install -e .[dev]    # Install with dev dependencies (mypy, ruff)
```

For using `uv` (faster package manager used in Makefile):
```bash
uv sync --with-editable .
```

## Key Files and Modules

### Core Agent Files
- `agent/graph.py` - LangGraph definition with all nodes and edges
- `agent/state.py` - TypedDict definitions for graph state
- `agent/configuration.py` - Configuration schema and resolution
- `agent/prompts.py` - System prompts for each node (query generation, reflection, etc.)
- `agent/tools_and_schemas.py` - Pydantic models for structured outputs (SearchQueryList, Reflection)
- `agent/utils.py` - Utility functions: TraceLogger, research topic extraction, token trimming

### External Integrations
- **DuckDuckGo**: Used for web search via `ddgs` library in `web_research()` node
- **Ollama**: Local LLM inference for all reasoning tasks
- **LangChain**: Core abstractions (ChatOllama, messages, state graphs)

### Configuration Files
- `langgraph.json` - LangGraph framework configuration (graph and HTTP app registration)
- `pyproject.toml` - Python project metadata, dependencies, tool configs (ruff, mypy)
- `Makefile` - Development task automation
- `.env` / `.env.example` - Environment variable configuration (Ollama URL, etc.)

## Important Considerations

### Error Handling
- The graph catches LLM invocation failures and raises informative RuntimeError messages indicating which model/service failed (e.g., "Failed to connect to Ollama")
- DuckDuckGo search failures are caught and return "Search failed or returned no results" gracefully
- A random sleep (0.1-1.5s) is added before DuckDuckGo calls to prevent Windows concurrency deadlocks

### Token Limiting
Search results and summaries are trimmed to `max_context_tokens` to prevent context overflow. This is critical since web search can return large amounts of text. The `trim_to_token_limit()` utility handles this.

### Parallel Execution
The `continue_to_web_research()` node uses LangGraph's `Send()` to dispatch queries in parallel. Multiple web_research invocations run concurrently, then results are accumulated back into state via the `operator.add` reducer on relevant state fields.

### Tracing and Logging
The `TraceLogger` class logs to both console and a global thread-safe list for UI consumption. This avoids cross-thread issues in Streamlit/FastAPI contexts. Max 1000 log entries are kept.

## Development Workflow

1. **Make changes**: Edit agent logic in `agent/graph.py`, prompts in `agent/prompts.py`, or configuration in `agent/configuration.py`
2. **Format**: `make format` before committing
3. **Lint**: `make lint` to catch issues
4. **Test locally**: Run `cli_research.py` with test questions or use Jupyter notebooks for interactive debugging
5. **Environment setup**: Ensure Ollama is running (`ollama serve`) and your desired model is pulled (e.g., `ollama pull gemma3n:e2b`)
