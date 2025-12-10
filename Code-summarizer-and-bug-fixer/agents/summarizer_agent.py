import google.generativeai as genai
from prompts.summarizer_agent_prompt import (
    CODE_SUMMARIZER_SYSTEM_PROMPT,
    CODE_SUMMARIZER_PROMPT_TEMPLATE
)

genai.configure(api_key="YOUR_KEY")

model = genai.GenerativeModel(
    "models/gemini-2.5-flash",
    system_instruction=CODE_SUMMARIZER_SYSTEM_PROMPT
)

def summarize_code(code_text: str):
    prompt = CODE_SUMMARIZER_PROMPT_TEMPLATE.format(code_snippet=code_text)
    response = model.generate_content(prompt)
    return response.text
