import argparse
import asyncio
import os
from dotenv import load_dotenv
from agent.graph import graph

load_dotenv()

async def main():
    # Setup command line arguments
    parser = argparse.ArgumentParser(description="Local Research CLI")
    parser.add_argument("topic", help="The topic to research")
    parser.add_argument(
        "--dir", 
        required=True, 
        help="Path to the local directory containing .md files for research"
    )
    args = parser.parse_args()

    # Configure the graph with the local search directory
    config = {
        "configurable": {
            "search_dir": args.dir,
            "max_research_loops": 2 # Efficient looping for documentation analysis
        }
    }

    # Initialize the research with the user's topic
    inputs = {"messages": [("user", args.topic)]}
    
    print(f"Starting research in: {args.dir}")
    print("-" * 30)

    # Stream the results from the graph
    async for event in graph.astream(inputs, config=config, stream_mode="values"):
        message = event.get("messages")
        if message:
            if isinstance(message, list):
                print(message[-1].content)
            else:
                print(message.content)

if __name__ == "__main__":
    asyncio.run(main())