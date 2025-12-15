from llm.client import generate_response
from guardrails.validator import validate_response, is_hallucinated
from config import HALLUCINATION_THRESHOLD

def reprompt_if_needed(query: str, context: str, response: str, max_attempts: int):
    attempt = 0
    score = validate_response(response, context)

    while is_hallucinated(score, HALLUCINATION_THRESHOLD) and attempt < max_attempts:
        attempt += 1
        correction_prompt = (
            f"Answer strictly using the following context:\n{context}\n\nQuestion: {query}"
        )
        response = generate_response(correction_prompt, context)
        score = validate_response(response, context)

    return response