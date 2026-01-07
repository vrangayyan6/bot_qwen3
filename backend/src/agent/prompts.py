from datetime import datetime

# Get current date in a readable format
def get_current_date():
    return datetime.now().strftime("%B %d, %Y")

query_writer_instructions = """Your goal is to generate technical keywords and short phrases to search within local documentation files (.md). 
Instead of broad web queries, focus on specific terms, function names, class names, or API concepts that are likely to appear in the documentation.

Instructions:
- Generate keywords or very short technical phrases (e.g., 'interrupt', 'StateGraph', 'entrypoint', 'asm_graph').
- Don't produce more than {number_queries} queries.
- Each query should be a single term or a 2-3 word phrase that matches technical content.
- Avoid natural language questions; use technical vocabulary relevant to the topic.

Format: 
- Format your response as a JSON object with these exact keys:
   - "rationale": Brief explanation of why these keywords are relevant
   - "query": A list of search terms/keywords

Example:
Topic: How to use interrupts in Functional API
```json
{{
    "rationale": "I am looking for technical implementation of interrupts specifically within the functional approach of the framework.",
    "query": ["interrupt", "functional_api", "@entrypoint", "human-in-the-loop"]
}}