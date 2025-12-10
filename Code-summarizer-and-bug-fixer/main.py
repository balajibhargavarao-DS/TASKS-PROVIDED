from agents.summarizer_agent import summarize_code
from agents.bug_fixer_agent import fix_code

code_to_analyze = """
def add(a, b)
    return a + b

result = add(5)
print(result)
"""

# Step 1 — Summarizer Agent
summary = summarize_code(code_to_analyze)
print("\n--- LINE-BY-LINE SUMMARY ---")
print(summary)

# Step 2 — Bug Fixer Agent
fixed = fix_code(code_to_analyze)
print("\n--- BUG FIXER OUTPUT ---")
print(fixed)
