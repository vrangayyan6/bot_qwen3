import os
import argparse
from agent.graph import graph
from agent.state import OverallState
from langchain_core.messages import HumanMessage

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("question", nargs="?", default=None, help="Question to ask")
    parser.add_argument("--dir", required=True, help="Directory for local Markdown sources")
    parser.add_argument("--loops", type=int, default=3, help="Max research loops")
    args = parser.parse_args()

    state = OverallState(
        messages=[HumanMessage(content=args.question or "")],
        search_dir=args.dir,
        max_research_loops=args.loops,
        research_loop_count=0,
        is_sufficient=False,
    )

    result = graph.invoke(state)

    for msg in result["messages"]:
        print("\n" + msg.content)


if __name__ == "__main__":
    main()
