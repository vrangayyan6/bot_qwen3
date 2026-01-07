import os
from agent.tools_and_schemas import SearchQueryList, Reflection
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, SystemMessage
from langgraph.types import Send
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
from langchain_groq import ChatGroq

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
from agent.utils import get_research_topic

load_dotenv()

# Initialize Groq LLM with Llama 3.3 70B
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_query(state: OverallState, config: RunnableConfig) -> QueryGenerationState:
    """Generate search queries based on the user question."""
    configurable = Configuration.from_runnable_config(config)
    
    if state.get("initial_search_query_count") is None:
        state["initial_search_query_count"] = configurable.number_of_initial_queries

    structured_llm = llm.with_structured_output(SearchQueryList)
    
    formatted_prompt = query_writer_instructions.format(
        current_date=get_current_date(),
        research_topic=get_research_topic(state["messages"]),
        number_queries=state["initial_search_query_count"],
    )
    
    result = structured_llm.invoke(formatted_prompt)
    return {"search_query": result.query}

def continue_to_local_research(state: QueryGenerationState):
    """Route to parallel local search nodes."""
    return [
        Send("local_research", {"search_query": q, "id": int(i)})
        for i, q in enumerate(state["search_query"])
    ]

def local_research(state: WebSearchState, config: RunnableConfig) -> OverallState:
    """Search for keywords within local markdown documentation."""
    search_dir = config.get("configurable", {}).get("search_dir")
    
    if not search_dir:
        return {"messages": [SystemMessage(content="Error: Search directory not provided.")]}

    results = []
    # Split the query into keywords for flexible matching
    query_keywords = state.get("search_query", "").lower().split()

    try:
        for root, _, files in os.walk(search_dir):
            for file in files:
                # Target .md files for documentation research
                if file.endswith(".md"):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            content_lower = content.lower()
                            # Match if at least 2 keywords from the query exist in the file
                            match_count = sum(1 for word in query_keywords if word in content_lower)
                            if match_count >= 2: 
                                # Using 2000 characters to capture enough code for comparison
                                results.append(f"Source: {path}\nContent: {content[:2000]}\n")
                    except:
                        continue
    except Exception as e:
        return {"messages": [SystemMessage(content=f"FileSystem Error: {str(e)}")]}

    final_content = "\n".join(results) if results else "No relevant information found."

    return {
        "sources_gathered": [], 
        "search_query": [state["search_query"]],
        "web_research_result": [final_content],
    }

def reflection(state: OverallState, config: RunnableConfig) -> ReflectionState:
    """Analyze search results and identify knowledge gaps."""
    state["research_loop_count"] = state.get("research_loop_count", 0) + 1

    formatted_prompt = reflection_instructions.format(
        current_date=get_current_date(),
        research_topic=get_research_topic(state["messages"]),
        summaries="\n\n---\n\n".join(state["web_research_result"]),
    )
    
    result = llm.with_structured_output(Reflection).invoke(formatted_prompt)

    return {
        "is_sufficient": result.is_sufficient,
        "knowledge_gap": result.knowledge_gap,
        "follow_up_queries": result.follow_up_queries,
        "research_loop_count": state["research_loop_count"],
        "number_of_ran_queries": len(state["search_query"]),
    }

def evaluate_research(state: ReflectionState, config: RunnableConfig):
    """Determine whether to continue research or finalize the answer."""
    configurable = Configuration.from_runnable_config(config)
    max_loops = state.get("max_research_loops", configurable.max_research_loops)
    
    if state["is_sufficient"] or state["research_loop_count"] >= max_loops:
        return "finalize_answer"
    
    return [
        Send("local_research", {
            "search_query": q, 
            "id": state["number_of_ran_queries"] + i
        })
        for i, q in enumerate(state["follow_up_queries"])
    ]

def finalize_answer(state: OverallState, config: RunnableConfig):
    """Generate final response based on all gathered information."""
    formatted_prompt = answer_instructions.format(
        current_date=get_current_date(),
        research_topic=get_research_topic(state["messages"]),
        summaries="\n---\n\n".join(state["web_research_result"]),
    )

    result = llm.invoke(formatted_prompt)
    return {"messages": [AIMessage(content=result.content)]}

# Build the StateGraph
builder = StateGraph(OverallState, config_schema=Configuration)

builder.add_node("generate_query", generate_query)
builder.add_node("local_research", local_research)
builder.add_node("reflection", reflection)
builder.add_node("finalize_answer", finalize_answer)

builder.add_edge(START, "generate_query")
builder.add_conditional_edges("generate_query", continue_to_local_research, ["local_research"])
builder.add_edge("local_research", "reflection")
builder.add_conditional_edges("reflection", evaluate_research, ["local_research", "finalize_answer"])
builder.add_edge("finalize_answer", END)

graph = builder.compile(name="pro-search-agent")