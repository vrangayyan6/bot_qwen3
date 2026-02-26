import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Add backend source to path so we can import the agent
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend/src'))

from agent.graph import graph
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv('../backend/.env')

st.set_page_config(page_title="Research Agent", page_icon="🕵️")

st.title("🕵️ Research Agent")
st.caption("Powered by LangGraph, Ollama, and DuckDuckGo")

# Sidebar Configuration
with st.sidebar:
    st.header("Configuration")

    ollama_base_url = st.text_input("Ollama Base URL", value=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))

    # Updated model options with gemma3n:e2b as default
    model_options = ["gemma3n:e2b", "gemma3:1b", "qwen3:4b", "gemma3:4b", "llama3.2", "mistral"]
    selected_model = st.selectbox(
        "Select Model",
        options=model_options,
        index=0
    )
    custom_model = st.text_input("Or enter custom model name (e.g., 'phi3:mini')")
    final_model = custom_model if custom_model else selected_model

    if ollama_base_url:
        os.environ["OLLAMA_BASE_URL"] = ollama_base_url

    st.divider()
    st.markdown("### About")
    st.markdown(
        "This agent performs comprehensive web research using local LLMs and DuckDuckGo."
    )

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to research?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Prepare state
        initial_state = {
            "messages": [HumanMessage(content=prompt)],
            "initial_search_query_count": 3,  # Default
            "max_research_loops": 2,         # Default
            "reasoning_model": final_model    # Use selected model
        }

        # Configure run with dynamic model selection
        config = {"configurable": {"query_generator_model": final_model, "reflection_model": final_model, "answer_model": final_model}}

        with st.status("Thinking...", expanded=True) as status:
            try:
                # Stream updates from the graph
                for chunk in graph.stream(initial_state, config=config):
                    for node, values in chunk.items():
                        if node == "generate_query":
                            status.write(f"Generated queries: {values['search_query']}")
                            with st.expander("Details: Query Generation"):
                                st.json(values)
                        elif node == "web_research":
                            status.write(f"Researched: {values['search_query'][0]}")
                            with st.expander("Details: Web Research & Sources"):
                                st.write("### Raw Result")
                                st.write(values.get("web_research_result", ["No result"])[0])
                                st.write("### Sources")
                                for source in values.get("sources_gathered", []):
                                    st.write(f"- [{source.get('title')}]({source.get('link')})")
                                    st.caption(source.get("snippet"))
                        elif node == "reflection":
                            if values.get("is_sufficient"):
                                status.write("Information is sufficient.")
                            else:
                                status.write(f"Identifying knowledge gaps: {values.get('knowledge_gap')}")
                                status.write(f"Follow-up queries: {values.get('follow_up_queries')}")
                            with st.expander("Details: Reflection"):
                                st.json(values)
                        elif node == "finalize_answer":
                            status.update(label="Research Complete!", state="complete", expanded=False)
                            full_response = values['messages'][0].content
                            message_placeholder.markdown(full_response)
                            with st.expander("Details: Final Answer"):
                                st.write(full_response)
                                st.write("### Sources Used")
                                for source in values.get("sources_gathered", []):
                                    st.write(f"- [{source.get('title')}]({source.get('link')})")
            except Exception as e:
                status.update(label="Error occurred", state="error")
                st.error(f"An error occurred: {str(e)}")

        # Save interaction
        if full_response:
            st.session_state.messages.append({"role": "assistant", "content": full_response})
