from typing import Any, Dict, List
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage
import datetime
import threading

# A global, thread-safe list to hold trace logs across the app and background tasks
GLOBAL_TRACE_LOGS = []
_log_lock = threading.Lock()

class TraceLogger:
    """
    A utility to log tracing information to both console and a global list
    that the Streamlit UI can read from, avoiding thread-context issues.
    """
    @staticmethod
    def log(message: str):
        # 1. Print to console (always)
        print(message)

        # 2. Append to global list safely
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        with _log_lock:
            GLOBAL_TRACE_LOGS.append(f"[{timestamp}] {message}")

    @staticmethod
    def clear():
        with _log_lock:
            GLOBAL_TRACE_LOGS.clear()


def get_research_topic(messages: List[AnyMessage]) -> str:
    """
    Get the research topic from the messages.
    """
    TraceLogger.log("--- Entering get_research_topic ---")
    # check if request has a history and combine the messages into a single string
    if len(messages) == 1:
        research_topic = messages[-1].content
    else:
        research_topic = ""
        for message in messages:
            if isinstance(message, HumanMessage):
                research_topic += f"User: {message.content}\n"
            elif isinstance(message, AIMessage):
                research_topic += f"Assistant: {message.content}\n"
    TraceLogger.log("--- Exiting get_research_topic ---")
    return research_topic


def format_search_results(search_results: Any) -> str:
    """
    Format search results into a string for the LLM.

    Args:
        search_results: Search results, either a list of dicts (Google) or a string (DuckDuckGo).

    Returns:
        Formatted string of search results.
    """
    TraceLogger.log("--- Entering format_search_results ---")
    if isinstance(search_results, str):
        TraceLogger.log("--- Exiting format_search_results (string) ---")
        return search_results

    formatted_results = ""
    if isinstance(search_results, list):
        for i, result in enumerate(search_results):
            formatted_results += f"Source [{i+1}]:\n"
            formatted_results += f"Title: {result.get('title', 'No Title')}\n"
            formatted_results += f"URL: {result.get('link', 'No URL')}\n"
            formatted_results += f"Snippet: {result.get('snippet', 'No Snippet')}\n\n"

    TraceLogger.log("--- Exiting format_search_results (list) ---")
    return formatted_results


def trim_to_token_limit(text: str, limit: int = 3000) -> str:
    """
    Trim text to a specific token limit using a simple character approximation.
    Assumes approx 4 characters per token.

    Args:
        text: The text to trim.
        limit: The maximum number of tokens allowed.

    Returns:
        The trimmed text.
    """
    TraceLogger.log(f"--- Entering trim_to_token_limit (limit={limit}) ---")
    if not text:
        TraceLogger.log("--- Exiting trim_to_token_limit (empty) ---")
        return ""

    # Approx 4 chars per token
    char_limit = limit * 4

    if len(text) > char_limit:
        TraceLogger.log(f"--- Exiting trim_to_token_limit (truncated from {len(text)} to {char_limit} chars) ---")
        return text[:char_limit] + "... [TRUNCATED]"
    TraceLogger.log("--- Exiting trim_to_token_limit (no truncation) ---")
    return text
