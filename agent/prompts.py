from datetime import datetime


# Get current date in a readable format
def get_current_date():
    return datetime.now().strftime("%B %d, %Y")


query_writer_instructions = """Your goal is to generate web search queries for an automated research tool.

IMPORTANT: You MUST generate EXACTLY {number_queries} search query. No more, no less.

Instructions:
- Generate exactly {number_queries} search query that best captures the user's question.
- The query should be specific and include the current year if relevant. The current date is {current_date}.
- Do NOT generate multiple queries. Only {number_queries}.

Format:
- Format your response as a JSON object with these exact keys:
   - "rationale": Brief explanation of why this query is relevant
   - "query": A list containing exactly {number_queries} search query

Example:

Topic: What is the best programming language for web development
```json
{{
    "rationale": "A single comprehensive query to find current expert opinions on web development languages.",
    "query": ["best programming language for web development 2025"]
}}
```

Context: {research_topic}"""


web_searcher_instructions = """Summarize the following search results for the topic "{research_topic}".

Instructions:
- The current date is {current_date}.
- Synthesize the provided search results into a concise and informative summary.
- You must cite the sources using the markdown format [Source Title](URL).
- Do not make up information. Only use the provided search results.
- If the search results are not relevant, state that.

Search Results:
{search_results}
"""

reflection_instructions = """You are an expert research assistant analyzing summaries about "{research_topic}".

Instructions:
- Identify knowledge gaps or areas that need deeper exploration and generate a follow-up query. (1 or multiple).
- If provided summaries are sufficient to answer the user's question, don't generate a follow-up query.
- If there is a knowledge gap, generate a follow-up query that would help expand your understanding.
- Focus on technical details, implementation specifics, or emerging trends that weren't fully covered.

Requirements:
- Ensure the follow-up query is self-contained and includes necessary context for web search.

Output Format:
- Format your response as a JSON object with these exact keys:
   - "is_sufficient": true or false
   - "knowledge_gap": Describe what information is missing or needs clarification
   - "follow_up_queries": Write a specific question to address this gap

Example:
```json
{{
    "is_sufficient": true, // or false
    "knowledge_gap": "The summary lacks information about performance metrics and benchmarks", // "" if is_sufficient is true
    "follow_up_queries": ["What are typical performance benchmarks and metrics used to evaluate [specific technology]?"] // [] if is_sufficient is true
}}
```

Reflect carefully on the Summaries to identify knowledge gaps and produce a follow-up query. Then, produce your output following this JSON format:

Summaries:
{summaries}
"""

answer_instructions = """Generate a high-quality answer to the user's question based on the provided summaries.

Instructions:
- The current date is {current_date}.
- You are the final step of a multi-step research process, don't mention that you are the final step. 
- You have access to all the information gathered from the previous steps.
- You have access to the user's question.
- Generate a high-quality answer to the user's question based on the provided summaries and the user's question.
- Include the sources you used from the Summaries in the answer correctly, use markdown format [Source Title](URL). THIS IS A MUST.

User Context:
- {research_topic}

Summaries:
{summaries}"""
