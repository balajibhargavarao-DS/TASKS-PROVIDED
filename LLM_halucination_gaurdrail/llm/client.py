def generate_response(query: str, context: str) -> str:
    """
    Mock LLM response generator.
    Replace with OpenAI / Gemini / Azure OpenAI client in real systems.
    """
    if "low-level" in query.lower():
        return "Yes, Python is a low-level language written directly in binary."
    return "Python is a high-level interpreted language."