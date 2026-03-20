# Gemini CLI Project Context: Local Research Agent

This file provides context and instructions for Gemini CLI when working in this workspace.

## Project Overview
A local research agent powered by **LangGraph**, **Ollama**, and **DuckDuckGo**. It allows users to perform autonomous research tasks, generate search queries, read web pages, and reflect on findings using local LLMs.

### Core Architecture
- **Agent (`agent/`)**: Logic for the LangGraph state machine.
  - `graph.py`: Defines the state graph (nodes, edges, and flow).
  - `state.py`: Typed definitions for the graph's state (Overall, Reflection, QueryGeneration, etc.).
  - `configuration.py`: Pydantic model for runtime configuration (models, loop counts, etc.).
  - `prompts.py`: System instructions for different agent roles.
  - `utils.py`: Shared utilities (tracing, formatting, trimming).
- **UI (`app.py`)**: Streamlit application for interactive research.
- **CLI (`cli_research.py`)**: Command-line entry point for headless research.

## Tech Stack
- **Framework**: [LangGraph](https://langchain-ai.github.io/langgraph/)
- **LLM Provider**: [Ollama](https://ollama.com/) (default: `gemma3:1b`, `gemma3:4b` for sub-tasks)
- **Search**: [DuckDuckGo](https://duckduckgo.com/) (via `ddgs`)
- **UI**: [Streamlit](https://streamlit.io/)
- **Configuration**: [Pydantic](https://docs.pydantic.dev/)

## Development Workflow

### Setup
1. `pip install -e .[dev,ui]`
2. `ollama pull gemma3:1b && ollama pull gemma3:4b` (or other models specified in `.env`)
3. `cp .env.example .env` and configure `OLLAMA_BASE_URL` if needed.

### Running
- **UI**: `streamlit run app.py`
- **CLI**: `python cli_research.py "Your topic"`
- **Notebook**: `langgraph_ollama.ipynb`

### Linting & Formatting
- **Ruff**: Configured in `pyproject.toml`. Run with `ruff check` and `ruff format`.

## Coding Standards

### Python Style
- Follow **Google-style docstrings**.
- Use **type hints** for all function signatures and complex variables.
- Prefer **Pydantic** for configuration and data validation.
- Use `TraceLogger.log` in `agent/utils.py` for consistent tracing across nodes.

### LangGraph Patterns
- Keep nodes small and focused.
- Define explicit state types in `agent/state.py`.
- Use `Configuration.from_runnable_config(config)` within nodes to access settings.

## Gemini CLI Instructions
- **Local First**: Prioritize local execution and testing. Assume Ollama is running at `http://localhost:11434` unless told otherwise.
- **Surgical Changes**: When modifying `graph.py`, ensure that state transitions and edge logic remain consistent with `state.py`.
- **Tracing**: Always add `TraceLogger.log` calls when adding new nodes or complex logic to maintain visibility in the Streamlit UI.
- **Dependency Management**: Check `pyproject.toml` before suggesting new libraries.
