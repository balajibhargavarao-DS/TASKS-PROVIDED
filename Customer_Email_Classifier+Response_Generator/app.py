from pipelines.classifier import classify_email
from pipelines.responder import generate_response
from utils.parser import load_email


def main():
    email_text = load_email("sample_data/sample_email.txt")


    classification = classify_email(email_text)
    response = generate_response(email_text, classification)


    print("=== INPUT EMAIL ===")
    print(email_text)


    print("\n=== CLASSIFICATION ===")
    for k, v in classification.items():
        
        
        print(f"{k}: {v}")


    print("\n=== AUTO-GENERATED RESPONSE ===")
    print(response)


if __name__ == "__main__":
    main()