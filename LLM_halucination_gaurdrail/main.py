from llm.client import generate_response
from guardrails.validator import validate_response
from guardrails.reprompt import reprompt_if_needed
from config import MAX_REPROMPTS

CONTEXT = """
Python is a high-level, interpreted programming language.
It supports multiple programming paradigms.
"""

def run(query: str):
    response = generate_response(query, CONTEXT)
    final_response = reprompt_if_needed(
        query=query,
        context=CONTEXT,
        response=response,
        max_attempts=MAX_REPROMPTS
    )
    print("\nFinal Answer:\n", final_response)

if __name__ == "__main__":
    user_query = "Is Python a low-level language written in binary?"
    run(user_query)