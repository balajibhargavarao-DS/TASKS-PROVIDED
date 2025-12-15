from llm.llm_client import call_llm
from llm.prompts import RESPONSE_SYSTEM_PROMPT




def generate_response(email_text: str, classification: dict) -> str:
    prompt = f"""
    Customer Email:
    {email_text}


    Category: {classification.get('category')}
    Sentiment: {classification.get('sentiment')}


    Generate an appropriate response.
    """


    return call_llm(RESPONSE_SYSTEM_PROMPT, prompt)