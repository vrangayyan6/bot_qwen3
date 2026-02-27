from typing import Any, Dict, List
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage


def get_research_topic(messages: List[AnyMessage]) -> str:
    """
    Get the research topic from the messages.
    """
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
    return research_topic


def format_search_results(search_results: Any) -> str:
    """
    Format search results into a string for the LLM.

    Args:
        search_results: Search results, either a list of dicts (Google) or a string (DuckDuckGo).

    Returns:
        Formatted string of search results.
    """
    if isinstance(search_results, str):
        return search_results

    formatted_results = ""
    if isinstance(search_results, list):
        for i, result in enumerate(search_results):
            formatted_results += f"Source [{i+1}]:\n"
            formatted_results += f"Title: {result.get('title', 'No Title')}\n"
            formatted_results += f"URL: {result.get('link', 'No URL')}\n"
            formatted_results += f"Snippet: {result.get('snippet', 'No Snippet')}\n\n"

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
    if not text:
        return ""

    # Approx 4 chars per token
    char_limit = limit * 4

    if len(text) > char_limit:
        return text[:char_limit] + "... [TRUNCATED]"
    return text
