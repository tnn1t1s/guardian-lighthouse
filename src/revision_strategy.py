import os
import sys
import json
import argparse
import requests

from tokens import load_auth_token

# Load authentication token
TOKEN = load_auth_token()
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Load template
TEMPLATE_DIR = "data_generation/templates/"
def load_template(template_name):
    with open(os.path.join(TEMPLATE_DIR, template_name), 'r') as f:
        return f.read()

# HF API URL
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"

# Function to apply a revision strategy
def apply_revision_strategy(prompt_dict, template):
    """
    Apply a revision strategy to the given prompt dictionary using the specified template.

    Parameters:
    - prompt_dict: dict, the input prompt dictionary.
    - template_name: str, the name of the revision strategy template.

    Returns:
    - str: The revised adversarial prompt.
    """
    # Format the template with the prompt details
    prompt = template.format(
        simple_prompt=prompt_dict["user"],
        revision_strategy="payload splitting",
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

