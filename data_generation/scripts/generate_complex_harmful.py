import os
import sys
import json
import requests
import argparse

from tokens import load_auth_token

# Load authentication token
TOKEN = load_auth_token()
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Load taxonomy and template
TAXONOMY_PATH = "data_generation/taxonomies/risk_dimensions.json"
TEMPLATE_PATH = "data_generation/templates/complex_harmful.template"
def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

taxonomy = load_json(TAXONOMY_PATH)
template = load_json(TEMPLATE_PATH)

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
    requests = [
        line.strip().replace("Request: ", "")
        for line in generated_text.splitlines()
        if line.strip().startswith("Request:")
    ]
    # Debug: Print any blank requests
    for req in requests:
        if not req:
            print("Debug: Blank request detected in generated_text:\n", generated_text)
    return [req for req in requests if req]

# Generate harmful requests using the HF API
def generate_requests(num_requests, category, sub_category, leaf_topic, description):
    """
    Generate harmful requests using Hugging Face's inference API based on taxonomy dimensions.

    Parameters:
    - num_requests: int, number of requests to generate.
    - category: str, the main category of the taxonomy.
    - sub_category: str, the subcategory within the taxonomy.
    - leaf_topic: str, the fine-grained topic of the taxonomy.
    - description: str, the description of the leaf topic.

    Returns:
    - list: List of formatted user/assistant JSON objects.
    """
    prompt = (f"{template['task_description'].replace('{num_requests}', str(num_requests))}")
    prompt = prompt.replace("{category}", category)
    prompt = prompt.replace("{sub_category}", sub_category)
    prompt = prompt.replace("{leaf_topic}", leaf_topic)
    prompt = prompt.replace("{description}", description)
    prompt += f"\n\n{template['format']}"

    payload = {"inputs": prompt}

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        raise Exception(f"HF API Error: {response.status_code} - {response.text}")

    generated_texts = response.json()
    if isinstance(generated_texts, list):
        generated_text = '\n'.join(text.get('generated_text', '').strip() for text in generated_texts if text.get('generated_text'))
    else:
        generated_text = generated_texts.get('generated_text', '').strip()
    if not generated_text:
        raise ValueError("No generated text returned by the API.")

    # Debug: Print the raw generated_text
    #print("Debug: Raw generated_text:\n", generated_text)

    # Extract requests from the generated text
    requests_list = extract_requests(generated_text)

    # Format for fine-tuning with metadata
    fine_tuning_data = [
        {
            "user": f"<user> {request} </user>",
            "assistant": "<assistant> This request is harmful and should be refused. </assistant>",
            "category": category,
            "sub_category": sub_category,
            "leaf_topic": leaf_topic,
            "description": description
        }
        for request in requests_list
    ]
    return fine_tuning_data

# Main script
def main():
    parser = argparse.ArgumentParser(description="Generate harmful requests for fine-tuning.")
    parser.add_argument("--num_requests", type=int, default=5, help="Number of requests to generate per taxonomy leaf topic.")
    parser.add_argument("--output_file", type=str, default="harmful_requests.jsonl", help="Output file for the generated requests.")
    args = parser.parse_args()

    num_requests = args.num_requests
    output_file = args.output_file

    if os.path.exists(output_file):
        os.remove(output_file)  # Clear the output file if it already exists

    all_data = []

    for category, subcategories in taxonomy.items():
        for sub_category_key, sub_category_data in subcategories.items():
            sub_category_name = sub_category_data["subcat_name"]
            description = sub_category_data["description"]
            for leaf_topic in sub_category_data["leaf_topics"]:
                print(f"Generating requests for category: {category}, sub_category: {sub_category_name}, leaf_topic: {leaf_topic}")
                fine_tuning_data = generate_requests(num_requests, category, sub_category_name, leaf_topic, description)
                all_data.extend(fine_tuning_data)
                print(f"Finished generating requests for: {leaf_topic}")

    # Write to JSONL with metadata
    with open(output_file, "w") as file:
        for entry in all_data:
            file.write(json.dumps(entry) + "\n")

    print(f"Data written to {output_file}")

if __name__ == "__main__":
    main()
