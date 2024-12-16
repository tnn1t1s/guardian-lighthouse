import json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def load_prompts(file_path):
    """Load prompts from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def score_guardian_hap(device, data, model, tokenizer, batch_size=128):
    """
    Scores input data for HAP using sequence classification models.

    Parameters:
    - device: torch.device
    - data: List of prompts
    - model: Sequence classification model
    - tokenizer: Tokenizer for the model
    - batch_size: Batch size for inference

    Returns:
    - List of HAP scores (probabilities of unsafe content)
    """
    hap_scores = []
    with torch.no_grad():
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            inputs = tokenizer(batch, max_length=512, padding=True, truncation=True, return_tensors="pt").to(device)
            logits = model(**inputs).logits
            # HAP score = softmax logits, [1] = probability of "harmful"
            hap_scores.extend(torch.softmax(logits, dim=1)[:, 1].detach().cpu().numpy().tolist())
    return hap_scores

def score_guardian_xl(device, data, model, tokenizer, batch_size=128):
    """
    Scores input data for HAP using causal language models.
    
    Parameters:
    - device: torch.device
    - data: List of prompts
    - model: Causal language model
    - tokenizer: Tokenizer for the model
    - batch_size: Batch size for inference

    Returns:
    - List of HAP scores (probabilities of unsafe content)
    """
    hap_scores = []
    with torch.no_grad():
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            inputs = tokenizer(batch, max_length=512, padding=True, truncation=True, return_tensors="pt").to(device)
            
            # Generate logits for the next token
            output = model.generate(
                inputs["input_ids"], 
                max_new_tokens=1,  # Generate only the next token
                return_dict_in_generate=True,
                output_scores=True
            )
            # Get logits for the last generated token
            logits = output.scores[-1]
            
            # Extract probabilities for "Yes" (unsafe) and "No" (safe)
            yes_id = tokenizer.convert_tokens_to_ids("Yes")
            yes_prob = torch.softmax(logits, dim=-1)[:, yes_id]
            hap_scores.extend(yes_prob.detach().cpu().numpy().tolist())
    return hap_scores

def aggregate_score(hap_scores, threshold=0.6):
    """
    Aggregates scores for HAP models using the maximum score approach.
    
    Parameters:
    - hap_scores: List of probabilities for unsafe content
    - threshold: Decision threshold for classification (default=0.75)
    
    Returns:
    - label: 1 if max score >= threshold (Unsafe), else 0 (Safe)
    - max_score: Maximum probability score from hap_scores
    """
    max_score = max(hap_scores)  # Maximum score across all sentences
    return 1 if max_score >= threshold else 0, max_score


