SYSTEM_PROMPT = """
You are an expert AI system that extracts structured data from resumes.
Return ONLY valid JSON.
No explanations.
No markdown.
No extra text.
"""

EXTRACTION_PROMPT_TEMPLATE = """
Extract structured info from the following resume.

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}

Return ONLY JSON using this EXACT structure:

{{
  "name": "",
  "experience_years": 0,
  "skills": [],
  "match_score": 0
}}

Strict rules:
- "skills" must be a JSON list of strings.
- "experience_years" must be a number.
- "match_score" must be a number (0–100).
- DO NOT add comments, words, or text outside the JSON.
"""
