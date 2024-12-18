import os
import json
import requests
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


# Generate safety requests using the HF API
def generate_requests(num_requests, safety_type, output_file):
    """
    Generate requests using Hugging Face's inference API based on the specified safety type and number of requests.

    Parameters:
    - num_requests: int, number of requests to generate.
    - safety_type: str, the safety type to focus on.
    - output_file: str, file path to save the generated requests.
    """
    prompt = (f"{template['task_description'].replace('{num_requests}', str(num_requests)).replace('{safety_type}', safety_type)}\n\n"
             f"Examples:\n"
             + "\n".join([f"Request: {example}" for example in template['examples']]) + "\n\n"
             f"{template['format']}")

    payload = {"inputs": prompt}

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        raise Exception(f"HF API Error: {response.status_code} - {response.text}")

    generated_text = response.json()[0]['generated_text']
    print(generated_text)
    if not generated_text:
        raise ValueError("No generated text returned by the API.")

    # Write responses to the output file
    with open(output_file, "a") as file:
        file.write(f"\n# Safety Type: {safety_type}\n")
        file.write(generated_text + "\n")

# Main script
def main():
    num_requests = 10  # Number of requests per safety type
    output_file = "generated_requests.txt"  # Output file for all requests

    if os.path.exists(output_file):
        os.remove(output_file)  # Clear the output file if it already exists

    for safety_type in SAFETY_TYPES:
        print(f"Generating requests for safety type: {safety_type}")
        generate_requests(num_requests, safety_type, output_file)
        print(f"Finished generating requests for: {safety_type}")

if __name__ == "__main__":
    main()

