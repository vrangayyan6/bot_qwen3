import argparse
from langchain_core.messages import HumanMessage
from agent.graph import graph


def main() -> None:
    """Run the research agent from the command line."""
    parser = argparse.ArgumentParser(description="Run the LangGraph research agent")
    parser.add_argument("question", help="Research question")
    parser.add_argument(
        "--initial-queries",
        type=int,
        default=3,
        help="Number of initial search queries",
    )
    parser.add_argument(
        "--max-loops",
        type=int,
        default=2,
        help="Maximum number of research loops",
    )
    parser.add_argument(
        "--reasoning-model",
        default="gemini-2.5-pro-preview-05-06",
        help="Model for the final answer",
    )
    args = parser.parse_args()

    state = {
        "messages": [HumanMessage(content=args.question)],
        "initial_search_query_count": args.initial_queries,
        "max_research_loops": args.max_loops,
        "reasoning_model": args.reasoning_model,
    }

    result = graph.invoke(state)
    messages = result.get("messages", [])
    if messages:
        print(messages[-1].content)
    
    token_records = result.get("token_usage_records", [])
    if token_records:
        print("\n" + "=" * 80)
        print("TOKEN USAGE SUMMARY")
        print("=" * 80)
        
        total_input = 0
        total_output = 0
        
        for record in token_records:
            print(f"\n{record['node_name'].upper():<20} ({record['model']})")
            print(f"  Input tokens:  {record['input_tokens']:,}")
            print(f"  Output tokens: {record['output_tokens']:,}")
            total_input += record['input_tokens']
            total_output += record['output_tokens']
        
        print("\n" + "-" * 80)
        print(f"{'TOTAL':<20}")
        print(f"  Input tokens:  {total_input:,}")
        print(f"  Output tokens: {total_output:,}")
        print(f"  Total tokens:  {(total_input + total_output):,}")
        print("=" * 80)


if __name__ == "__main__":
    main()
