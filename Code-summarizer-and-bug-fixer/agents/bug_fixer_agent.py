import google.generativeai as genai
from prompts.bug_fixer_prompt import (
    BUG_FIXER_SYSTEM_PROMPT,
    BUG_FIXER_PROMPT_TEMPLATE
)

genai.configure(api_key="YOUR_KEY")

bug_model = genai.GenerativeModel(
    "models/gemini-2.5-flash",
    system_instruction=BUG_FIXER_SYSTEM_PROMPT
)

def fix_code(code_text: str):
    prompt = BUG_FIXER_PROMPT_TEMPLATE.format(code_snippet=code_text)
    response = bug_model.generate_content(prompt)
    return response.text
