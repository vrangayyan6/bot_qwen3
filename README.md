# Local Research Agent with Ollama and Streamlit

This project is a local research agent powered by [LangGraph](https://langchain-ai.github.io/langgraph/), [Ollama](https://ollama.com/), and [DuckDuckGo](https://duckduckgo.com/). It features a Streamlit UI for interacting with the agent.  Used [Google Jules](https://jules.google.com/) coding agent with starting point as [gemini-fullstack-langgraph-quickstart](https://github.com/google-gemini/gemini-fullstack-langgraph-quickstart).

## Features

- 🕵️ **Autonomous Research**: Generates search queries, reads web pages, and reflects on findings.
- 🏠 **Local LLMs**: Uses local models via Ollama (default: `qwen3:4b`, supports `gemma3:4b`, etc.).
- 🌐 **DuckDuckGo Search**: Integrates with DuckDuckGo for free, real-time web research (no API key required).
- 💬 **Streamlit UI**: Simple chat interface to run research tasks and view progress.

## Prerequisites

1.  **Ollama**: Install [Ollama](https://ollama.com/) and pull your desired model:
    ```bash
    ollama pull qwen3:4b
    ollama pull gemma3:4b
    ```

## Getting Started

### Option 1: Run Locally (Recommended for dev)

1.  **Clone the repository.**

2.  **Install Backend Dependencies:**
    ```bash
    cd backend
    pip install -e .
    ```

3.  **Install Streamlit Dependencies:**
    ```bash
    cd ../streamlit_app
    pip install -r requirements.txt
    ```

4.  **Configure Environment (Optional):**
    You can set `OLLAMA_BASE_URL` if your Ollama instance is not at `http://localhost:11434`.
    ```bash
    # backend/.env
    OLLAMA_BASE_URL="http://localhost:11434"
    ```

5.  **Run the App:**
    ```bash
    # From streamlit_app directory
    streamlit run app.py
    ```

    or notebook
    ```bash
     jupyter notebook .\backend\langgraph_ollama.ipynb
    ```

### Option 2: Run with Docker

1.  **Build and Run:**
    ```bash
    docker-compose up --build
    ```
    *Note: Linux users may need to ensure `host.docker.internal` is accessible for Ollama.*

2.  **Access the App:**
    Open `http://localhost:8501` in your browser.

## Architecture

-   **Backend (`backend/`)**: Contains the LangGraph agent logic (`agent/graph.py`) and configuration.
-   **Frontend (`streamlit_app/`)**: A Streamlit application that imports the backend graph and runs it directly.

## License

MIT
