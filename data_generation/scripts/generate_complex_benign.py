import os
import sys
import json
import requests
import argparse

from tokens import load_auth_token

# Define safety types
SAFETY_TYPES = [
    "homonyms",
    "figurative language",
    "safe targets",
    "safe contexts",
    "definitions",
    "real discrimination/nonsense group",
    "nonsense discrimination/real group",
    "historical events",
    "public privacy",
    "fictional privacy"
]

ASSISTANT_RESPONSE = "This is a safe request."

# Load authentication token
TOKEN = load_auth_token()
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Load template
TEMPLATE_PATH = "data_generation/templates/complex_benign.template"
def load_template(template_path):
    with open(template_path, 'r') as f:
        return json.load(f)

template = load_template(TEMPLATE_PATH)

# HF API URL
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"

# Extract Requests from Generated Text
def extract_requests(generated_text):
    """
    Extracts lines starting with 'Request:' from the generated text.

    Parameters:
    - generated_text: str, the full response from the model.

    Returns:
    - list: List of extracted requests.
    """
    return [line.strip() for line in generated_text.splitlines() if line.strip().startswith("Request:")]

# Generate safety requests using the HF API
def generate_requests(num_requests, safety_type):
    """
    Generate requests using Hugging Face's inference API based on the specified safety type and number of requests.

    Parameters:
    - num_requests: int, number of requests to generate.
    - safety_type: str, the safety type to focus on.

    Returns:
    - list: List of formatted user/assistant JSON objects.
    """
    prompt = (f"{template['task_description'].replace('{num_requests}', str(num_requests)).replace('{safety_type}', safety_type)}\n\n"
             f"Examples:\n"
             + "\n".join([f"Request: {example}" for example in template['examples']]) + "\n\n"
             f"{template['format'].replace('{num_requests}', str(num_requests)).replace('{safety_type}', safety_type)}")

    payload = {"inputs": prompt}

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        raise Exception(f"HF API Error: {response.status_code} - {response.text}")

    generated_texts = response.json()
    if isinstance(generated_texts, list):
        generated_text = '\n'.join(text.get('generated_text', '').strip() for text in generated_texts)
    else:
        generated_text = generated_texts.get('generated_text', '').strip()
    if not generated_text:
        raise ValueError("No generated text returned by the API.")

    # Extract requests from the generated text
    requests_list = extract_requests(generated_text)

    # Format for fine-tuning
    fine_tuning_data = [
        {
            "user": f"<user> {request.replace('Request: ', '')} </user>",
            "assistant": f"<assistant> {ASSISTANT_RESPONSE}</assistant>",
            "safety_type": safety_type
        }
        for request in requests_list
    ]
    return fine_tuning_data

# Main script
def main():
    parser = argparse.ArgumentParser(description="Generate safety requests for fine-tuning.")
    parser.add_argument("--num_requests", type=int, default=10, help="Number of requests to generate per safety type.")
    parser.add_argument("--output_file", type=str, default="fine_tuning_data.jsonl", help="Output file for the generated requests.")
    args = parser.parse_args()

    num_requests = args.num_requests
    output_file = args.output_file

    if os.path.exists(output_file):
        os.remove(output_file)  # Clear the output file if it already exists

    all_data = []
    for safety_type in SAFETY_TYPES:
        print(f"Generating requests for safety type: {safety_type}")
        fine_tuning_data = generate_requests(num_requests, safety_type)
        all_data.extend(fine_tuning_data)
        print(f"Finished generating requests for: {safety_type}")

    # Write to JSONL with metadata
    with open(output_file, "w") as file:
        for entry in all_data:
            file.write(json.dumps(entry) + "\n")

    print(f"Data written to {output_file}")

if __name__ == "__main__":
    main()
