# LangGraph Interrupt Example

LangGraph is a Python library for building stateful LLM applications
using graphs or functional workflows.

This document shows how interrupts can be implemented
using both the Functional API and the Graph API.

## Functional API

The Functional API allows defining agent logic as a Python function.
Interrupts are typically implemented using control flow statements.

```python
from langgraph.functional import agent

def my_agent():
    while True:
        inp = input(">>> ")
        if inp == "STOP":
            return "Interrupted"
        print(f"Echo: {inp}")
