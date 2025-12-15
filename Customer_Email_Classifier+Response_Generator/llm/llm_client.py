import google.generativeai as genai
from config.settings import GEMINI_API_KEY, MODEL_NAME

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(MODEL_NAME)

def call_llm(system_prompt: str, user_prompt: str) -> str:
    response = model.generate_content(
        f"SYSTEM:\n{system_prompt}\n\nUSER:\n{user_prompt}",
        generation_config={"temperature": 0.3}
    )
    return response.text
