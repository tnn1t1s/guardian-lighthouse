import torch
import math
from torch.nn.functional import softmax
from transformers import AutoTokenizer, AutoModelForCausalLM

import torch
import math
from torch.nn.functional import softmax

def parse_output(output, input_len, tokenizer, safe_token="No", unsafe_token="Yes", nlogprobs=20):
    """
    Parses the model's output to determine the risk label and probability.

    Parameters:
    - output: Model output from the `generate` function.
    - input_len: Length of the input token sequence.
    - tokenizer: Tokenizer used for decoding.
    - safe_token: Token representing "safe" content.
    - unsafe_token: Token representing "unsafe" content.
    - nlogprobs: Number of top probabilities to consider.

    Returns:
    - label: "Yes", "No", or "Failed" based on the generated token.
    - prob_of_risk: Probability of risk (unsafe content).
    """
    label, prob_of_risk = None, None
    if nlogprobs > 0:
        logprobs = [
            torch.topk(token, k=nlogprobs, largest=True, sorted=True)
            for token in output.scores[:-1]
        ]
        if logprobs:
            prob = get_probabilities(logprobs, tokenizer, safe_token, unsafe_token)
            prob_of_risk = prob[1]

    generated_text = tokenizer.decode(output.sequences[:, input_len:][0], skip_special_tokens=True).strip()
    if unsafe_token.lower() == generated_text.lower():
        label = unsafe_token
    elif safe_token.lower() == generated_text.lower():
        label = safe_token
    else:
        label = "Failed"

    return label, prob_of_risk.item() if prob_of_risk else None

def get_probabilities(logprobs, tokenizer, safe_token="No", unsafe_token="Yes"):
    """
    Calculates probabilities for safe and unsafe tokens.

    Parameters:
    - logprobs: List of top probabilities for each token in the sequence.
    - tokenizer: Tokenizer for token ID conversion.
    - safe_token: Token representing "safe" content.
    - unsafe_token: Token representing "unsafe" content.

    Returns:
    - probabilities: Softmax-normalized probabilities for safe and unsafe tokens.
    """
    safe_token_prob = 1e-50
    unsafe_token_prob = 1e-50
    for token_probs in logprobs:
        for logprob, index in zip(token_probs.values.tolist()[0], token_probs.indices.tolist()[0]):
            token = tokenizer.convert_ids_to_tokens(index)
            if token.strip().lower() == safe_token.lower():
                safe_token_prob += math.exp(logprob)
            elif token.strip().lower() == unsafe_token.lower():
                unsafe_token_prob += math.exp(logprob)

    probabilities = torch.softmax(
        torch.tensor([math.log(safe_token_prob), math.log(unsafe_token_prob)]), dim=0
    )
    return probabilities

def test_risk(messages, model, tokenizer, device, guardian_config=None, max_new_tokens=20):
    """
    Runs the model to evaluate risk for a given message.

    Parameters:
    - messages: List of messages (prompt) to evaluate.
    - model: Pretrained model (causal LM).
    - tokenizer: Tokenizer for the model.
    - device: Device to run the model on (CPU/GPU).
    - guardian_config: Optional configuration for the model.
    - max_new_tokens: Maximum number of tokens to generate.

    Returns:
    - label: "Yes", "No", or "Failed" based on the generated token.
    - prob_of_risk: Probability of risk (unsafe content).
    """
    input_ids = tokenizer.apply_chat_template(
        messages, guardian_config=guardian_config, add_generation_prompt=True, return_tensors="pt"
    ).to(device)
    input_len = input_ids.shape[1]

    with torch.no_grad():
        output = model.generate(
            input_ids,
            do_sample=False,
            max_new_tokens=max_new_tokens,
            return_dict_in_generate=True,
            output_scores=True,
        )

    return parse_output(output, input_len, tokenizer)

