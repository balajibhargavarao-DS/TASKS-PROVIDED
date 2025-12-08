import google.generativeai as genai

# Add your Gemini API Key here
genai.configure(api_key="api_key")

# Fetch and display all available models
models = genai.list_models()

print("\n=== Models Available for Your API Key ===\n")
for model in models:
    print(f"Model Name : {model.name}")
    print(f"Supports   : {model.supported_generation_methods}")
    print("-" * 50)

