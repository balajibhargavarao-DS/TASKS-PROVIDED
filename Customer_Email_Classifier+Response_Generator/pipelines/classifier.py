import json
from llm.llm_client import call_llm
from llm.prompts import CLASSIFIER_SYSTEM_PROMPT

def classify_email(email_text: str) -> dict:
    raw_output = call_llm(
        CLASSIFIER_SYSTEM_PROMPT,
        f"Email:\n{email_text}"
        )

    try:
        return json.loads(raw_output)

    except json.JSONDecodeError:
        return {
            "category": "unknown",
            "sentiment": "unknown"
            }