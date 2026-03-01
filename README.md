# Local Research Agent with Ollama and Streamlit

This project is a local research agent powered by [LangGraph](https://langchain-ai.github.io/langgraph/), [Ollama](https://ollama.com/), and [DuckDuckGo](https://duckduckgo.com/). It features a Streamlit UI for interacting with the agent.  Used [Claude Code](https://code.claude.com/docs/en/overview) and [Google Jules](https://jules.google.com/) coding agent with starting point as [gemini-fullstack-langgraph-quickstart](https://github.com/google-gemini/gemini-fullstack-langgraph-quickstart).

## Features

- 🕵️ **Autonomous Research**: Generates search queries, reads web pages, and reflects on findings.
- 🏠 **Local LLMs**: Uses local models via Ollama (default: `gemma3n:e2b`).
- 🌐 **DuckDuckGo Search**: Integrates with DuckDuckGo for free, real-time web research (no API key required).
- 💬 **Streamlit UI**: Simple chat interface to run research tasks and view progress.

## Prerequisites

1.  **Ollama**: Install [Ollama](https://ollama.com/) and pull your desired model:
    ```bash
    ollama pull gemma3n:e2b    
    ```

## Getting Started

### Option 1: Run Locally (Recommended for dev)

1.  **Clone the repository.**

2.  **Install Dependencies:**
    ```bash
    pip install -e .[ui]
    ```

3.  **Configure Environment (Optional):**
    You can set `OLLAMA_BASE_URL` if your Ollama instance is not at `http://localhost:11434`.
    Copy `.env.example` to `.env` and configure:
    ```bash
    OLLAMA_BASE_URL="http://localhost:11434"
    ```

4.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

    or via notebook:
    ```bash
    jupyter notebook langgraph_ollama.ipynb
    ```

5.  **Or run via CLI (no UI):**
    ```bash
    python cli_research.py "What are the latest advances in quantum computing?"
    ```

    CLI options:
    | Flag | Default | Description |
    |------|---------|-------------|
    | `--initial-queries` | `1` | Number of search queries to generate |
    | `--max-loops` | `2` | Maximum research loops |
    | `--reasoning-model` | `qwen3:4b` | Ollama model to use |

### Option 2: Run with Docker

1.  **Build and Run:**
    ```bash
    docker-compose up --build
    ```
    *Note: Linux users may need to ensure `host.docker.internal` is accessible for Ollama.*

2.  **Access the App:**
    Open `http://localhost:8501` in your browser.

## Architecture

-   **Agent (`agent/`)**: Contains the LangGraph agent logic (`graph.py`) and configuration.
-   **Streamlit UI (`app.py`)**: A Streamlit application that imports the graph and runs it directly.
-   **CLI (`cli_research.py`)**: A command-line interface for running research queries without the UI.

## License

MIT
