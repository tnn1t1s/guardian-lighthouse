import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from utils import load_prompts, score_guardian_hap, aggregate_score

# Model configuration
model_id = "ibm-granite/granite-guardian-hap-38m"  # HAP small model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id).to(device).eval()

# Load prompts
prompts = load_prompts("prompts.json")

# Set the threshold for classification
threshold = 0.75  # Default threshold for small HAP models

# Process and score prompts
results = {}
for category, prompt_list in prompts.items():
    results[category] = []
    for prompt in prompt_list:
        # Score the prompt using the HAP model
        hap_scores = score_guardian_hap(device, [prompt], model, tokenizer)
        # Aggregate the score
        label, max_score = aggregate_score(hap_scores, threshold=threshold)
        # Store the results
        results[category].append({
            "prompt": prompt,
            "hap_label": "Unsafe" if label == 1 else "Safe",
            "max_hap_score": max_score
        })

# Print results
for category, test_results in results.items():
    print(f"\nCategory: {category.upper()}")
    for res in test_results:
        print(f"Prompt: {res['prompt']}")
        print(f"HAP Label: {res['hap_label']}")
        print(f"Max HAP Score: {res['max_hap_score']:.3f}")

