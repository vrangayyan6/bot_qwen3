from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AIMessage

from agent.state import OverallState
from agent.tools_and_schemas import SearchQueryList, Reflection
from agent.llm.groq import GroqLLM

from .search.local_markdown import search_markdown

llm = GroqLLM()


# ---------- NODES ----------

def generate_search_queries(state: OverallState):
    question = state["messages"][-1].content

    prompt = f"Generate search queries for: {question}"
    queries = llm.invoke_structured(prompt, SearchQueryList)

    return {
        "search_query": [q.model_dump() for q in queries.query]
    }


def web_research(state: OverallState):
    all_results = []

    search_dir = state.get("search_dir")
    if not search_dir:
        return {"web_research_result": [], "sources_gathered": []}

    for q in state["search_query"]:
        query_text = q["query"]
        matches = search_markdown(search_dir, query_text)
        all_results.extend(matches)

    return {
        "web_research_result": all_results,
        "sources_gathered": []
    }


def reflect(state: OverallState):
    prompt = (
        f"Question:\n{state['messages'][-1].content}\n\n"
        f"Research:\n" + "\n".join(state["web_research_result"])
    )

    reflection = llm.invoke_structured(prompt, Reflection)

    return {
        "is_sufficient": reflection.is_sufficient,
        "follow_up_queries": [
            q.model_dump() for q in reflection.follow_up_queries
        ]
    }


def finalize(state: OverallState):
    prompt = (
        f"Answer the question:\n"
        f"{state['messages'][-1].content}\n\n"
        f"Using:\n" + "\n".join(state["web_research_result"])
    )

    answer = llm.invoke(prompt)

    return {
        "messages": [AIMessage(content=answer)]
    }


# ---------- GRAPH ----------

def build_graph():
    graph = StateGraph(OverallState)

    graph.add_node("generate_queries", generate_search_queries)
    graph.add_node("research", web_research)
    graph.add_node("reflect", reflect)
    graph.add_node("finalize", finalize)

    graph.add_edge(START, "generate_queries")
    graph.add_edge("generate_queries", "research")
    graph.add_edge("research", "reflect")

    graph.add_conditional_edges(
        "reflect",
        lambda state: "finalize"
    )

    graph.add_edge("finalize", END)

    return graph.compile()


graph = build_graph()
