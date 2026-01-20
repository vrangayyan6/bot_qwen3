import json
import re
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()


class GroqLLM:
    def __init__(self, model="llama-3.3-70b-versatile"):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = model

    def invoke(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return response.choices[0].message.content

    def invoke_structured(self, prompt: str, schema):
        structured_prompt = f"""
You MUST return ONLY valid JSON.
Do NOT include explanations, markdown, or extra text.

JSON schema:
{schema.model_json_schema()}

User request:
{prompt}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": structured_prompt}],
            temperature=0,
        )

        content = response.choices[0].message.content.strip()

        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            raise ValueError(
                f"Groq did not return JSON.\nRaw output:\n{content}"
            )

        json_str = match.group(0)

        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON from Groq:\n{json_str}"
            ) from e

        return schema.model_validate(data)
