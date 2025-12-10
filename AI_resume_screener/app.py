import os
import json
import time
import re
import PyPDF2
import google.generativeai as genai

from prompts import SYSTEM_PROMPT, EXTRACTION_PROMPT_TEMPLATE

# --------------------------
# CONFIGURE GEMINI
# --------------------------
genai.configure(api_key="Your-Api-Key")
MODEL_NAME = "models/gemini-2.5-flash"


# --------------------------
# CLEAN JSON OUTPUT
# --------------------------
def clean_json_output(text: str) -> str:
    if not text:
        return ""

    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE)

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        return match.group(0)

    return text.strip()


# --------------------------
# CALL GEMINI
# --------------------------
def call_gemini(system_prompt: str, user_prompt: str, retries: int = 3) -> str:
    for attempt in range(1, retries + 1):
        try:
            model = genai.GenerativeModel(
                model_name=MODEL_NAME,
                system_instruction=system_prompt
            )

            response = model.generate_content(user_prompt)

            if not response or not response.text:
                raise ValueError("Empty response from Gemini")

            return response.text

        except Exception as e:
            print(f"[Attempt {attempt}] Gemini error: {e}")
            time.sleep(1)

    raise RuntimeError("Gemini failed after retries")


# --------------------------
# EXTRACT TEXT FROM PDF
# --------------------------
def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        reader = PyPDF2.PdfReader(pdf_path)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as e:
        print(f"ERROR reading PDF {pdf_path}: {e}")
        return ""


# --------------------------
# PROCESS ONE RESUME
# --------------------------
def process_resume(resume_path: str, jd_text: str) -> dict:
    print(f"Processing: {resume_path}")

    resume_text = extract_text_from_pdf(resume_path)

    if resume_text.strip() == "":
        return {"error": "Resume text could not be extracted"}

    extraction_prompt = EXTRACTION_PROMPT_TEMPLATE.format(
        resume_text=resume_text,
        jd_text=jd_text
    )

    raw_output = call_gemini(SYSTEM_PROMPT, extraction_prompt)
    cleaned_json = clean_json_output(raw_output)

    try:
        return json.loads(cleaned_json)
    except Exception:
        print("\n--- INVALID JSON RECEIVED ---")
        print(raw_output)
        print("------------------------------\n")
        return {"error": "Invalid JSON returned by model"}


# --------------------------
# BATCH PROCESS
# --------------------------
def batch_process():
    resume_dir = "./data/resume"
    jd_path = "./data/jd.txt"

    # Load Job Description
    with open(jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    results = []

    for file in os.listdir(resume_dir):
        if file.lower().endswith(".pdf"):
            resume_path = os.path.join(resume_dir, file)

            result = process_resume(resume_path, jd_text)
            results.append({file: result})

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print("\nProcessing complete! Results saved to results.json")


# --------------------------
# MAIN
# --------------------------
if __name__ == "__main__":
    batch_process()