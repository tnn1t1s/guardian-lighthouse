import os
import sys
import json
import argparse
import requests

# Ensure the src directory is in the Python path
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from token_loader import load_auth_token

# Load authentication token
TOKEN = load_auth_token()
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Load template
TEMPLATE_DIR = "data_generation/templates/revisions/"
def load_template(template_name):
    with open(os.path.join(TEMPLATE_DIR, template_name), 'r') as f:
        return f.read()

# HF API URL
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"

# Function to apply a revision strategy
def apply_revision_strategy(prompt_dict, template_name):
    """
    Apply a revision strategy to the given prompt dictionary using the specified template.

    Parameters:
    - prompt_dict: dict, the input prompt dictionary.
    - template_name: str, the name of the revision strategy template.

    Returns:
    - str: The revised adversarial prompt.
    """
    template = load_template(template_name)

    # Format the template with the prompt details
    prompt = template.format(
        simple_prompt=prompt_dict["user"],
        revision_strategies="Provide adversarial strategies based on the template logic.",
        category=prompt_dict["category"],
        sub_category=prompt_dict["sub_category"],
        leaf_topic=prompt_dict["leaf_topic"],
        description=prompt_dict["description"]
    )

    payload = {"inputs": prompt}

    # Make the API request
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        raise Exception(f"HF API Error: {response.status_code} - {response.text}")

    generated_texts = response.json()
    if isinstance(generated_texts, list):
        revised_prompt = '\n'.join(text.get('generated_text', '').strip() for text in generated_texts if text.get('generated_text'))
    else:
        revised_prompt = generated_texts.get('generated_text', '').strip()

    if not revised_prompt:
        raise ValueError("No revised prompt returned by the API.")

    return revised_prompt

# Main script
def main():
    parser = argparse.ArgumentParser(description="Apply revision strategies to prompts.")
    parser.add_argument("--input_file", type=str, required=True, help="Path to the input JSON file containing prompts.")
    parser.add_argument("--template_name", type=str, required=True, help="Name of the revision strategy template.")
    parser.add_argument("--output_file", type=str, default="revised_prompts.jsonl", help="Output file for the revised prompts.")
    args = parser.parse_args()

    input_file = args.input_file
    template_name = args.template_name
    output_file = args.output_file

    # Load prompts from the input file
    with open(input_file, 'r') as f:
        prompts = [json.loads(line) for line in f]

    if os.path.exists(output_file):
        os.remove(output_file)  # Clear the output file if it already exists

    # Apply the revision strategy to each prompt
    with open(output_file, "w") as file:
        for prompt_dict in prompts:
            print(f"Applying revision strategy to prompt: {prompt_dict['user']}")
            revised_prompt = apply_revision_strategy(prompt_dict, template_name)
            output = {
                "original_prompt": prompt_dict,
                "revised_prompt": revised_prompt
            }
            file.write(json.dumps(output) + "\n")
            print(f"Revised prompt generated: {revised_prompt}")

    print(f"Revised prompts written to {output_file}")

if __name__ == "__main__":
    main()

