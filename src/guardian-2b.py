import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from utils import load_prompts
from utils2b import test_risk

# Model configuration
model_path_name = "ibm-granite/granite-guardian-3.0-2b"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path_name)
model = AutoModelForCausalLM.from_pretrained(model_path_name).to(device).eval()

# Load prompts
prompts = load_prompts("prompts.json")

# Testing prompts
results = {category: [] for category in prompts.keys()}

for category, prompt_list in prompts.items():
    print(f"\nTesting {category.upper()} prompts:")
    for prompt in prompt_list:
        messages = [{"role": "user", "content": prompt}]
        label, prob = test_risk(messages, model, tokenizer, device)
        results[category].append({
            "prompt": prompt,
            "label": label,
            "probability": f"{prob:.3f}" if prob else "N/A"
        })
        print(f"- Prompt: {prompt}")
        print(f"  Risk detected: {label}")
        print(f"  Probability of risk: {prob:.3f}" if prob else "  Probability of risk: N/A")

# Display Results
print("\nSummary of Results:")
for category, test_results in results.items():
    print(f"\nCategory: {category.upper()}")
    for res in test_results:
        print(f"Prompt: {res['prompt']}")
        print(f"Risk Detected: {res['label']}")
        print(f"Probability of Risk: {res['probability']}")

