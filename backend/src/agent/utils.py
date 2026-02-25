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


def format_search_results(search_results: List[Dict[str, Any]]) -> str:
    """
    Format search results into a string for the LLM.

    Args:
        search_results: List of dictionaries containing 'title', 'link', 'snippet'.

    Returns:
        Formatted string of search results.
    """
    formatted_results = ""
    for i, result in enumerate(search_results):
        formatted_results += f"Source [{i+1}]:\n"
        formatted_results += f"Title: {result.get('title', 'No Title')}\n"
        formatted_results += f"URL: {result.get('link', 'No URL')}\n"
        formatted_results += f"Snippet: {result.get('snippet', 'No Snippet')}\n\n"

    return formatted_results
