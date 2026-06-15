import os
import json
from dotenv import load_dotenv
from google import genai


def load_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def build_prompt(task_description):
    examples = load_text_file("examples.txt")
    prompt_template = load_text_file("prompt_template.txt")

    final_prompt = prompt_template.replace("{examples}", examples)
    final_prompt = final_prompt.replace("{task_description}", task_description)

    return final_prompt


def clean_json_response(response_text):
    response_text = response_text.strip()

    if response_text.startswith("```json"):
        response_text = response_text.replace("```json", "").replace("```", "").strip()
    elif response_text.startswith("```"):
        response_text = response_text.replace("```", "").strip()

    return response_text


def generate_rca(task_description):
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please add it in the .env file.")

    client = genai.Client(api_key=api_key)

    prompt = build_prompt(task_description)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    cleaned_response = clean_json_response(response.text)

    try:
        rca_data = json.loads(cleaned_response)
        return rca_data

    except json.JSONDecodeError:
        print("\nGemini did not return valid JSON. Raw response:\n")
        print(response.text)
        raise


def print_rca(rca_data):
    for analysis_key, analysis_value in rca_data.items():
        print("\n" + "=" * 60)
        print(analysis_key.upper().replace("_", " "))
        print("=" * 60)

        for i in range(1, 6):
            print(f"\nWhy {i}: {analysis_value.get(f'why_{i}', '')}")
            print(f"Response {i}: {analysis_value.get(f'response_{i}', '')}")

        print("\nRoot Cause:")
        print(analysis_value.get("root_cause", ""))

        print("\nCorrective Action:")
        print(analysis_value.get("corrective_action", ""))


if __name__ == "__main__":
    task_description = input("Provide the task description: ")

    try:
        result = generate_rca(task_description)
        print_rca(result)

        with open("output.json", "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

        print("\nOutput saved successfully in output.json")

    except Exception as error:
        print(f"\nError: {error}")