from difflib import SequenceMatcher

def validate_response(response: str, context: str) -> float:
    """
    Returns a similarity score between response and context.
    Lower score => potential hallucination.
    """
    matcher = SequenceMatcher(None, response.lower(), context.lower())
    return matcher.ratio()

def is_hallucinated(score: float, threshold: float) -> bool:
    return score < threshold