# Guardian Lighthouse

Guardian Lighthouse is a repository that enhances the usability and understanding of IBM's Granite Guardian models. By providing tools for evaluation, testing, and risk detection, this project serves as a modular framework to shed light on the complexities of content safety in generative AI systems.

## Overview

As AI-generated content becomes ubiquitous, ensuring safety and ethical considerations in model outputs has emerged as a critical challenge. IBM's Granite Guardian models, particularly those aimed at detecting Hate, Abuse, and Profanity (HAP), represent a significant step forward in moderating unsafe content. However, their documentation and tooling are fragmented, making it difficult for developers to effectively integrate and test these models.

**Guardian Lighthouse** addresses this gap by:
- Providing utilities to test small HAP models and larger causal models (e.g., `granite-guardian-3.0-2b`).
- Streamlining risk detection for prompts across categories such as **safe**, **ambiguous**, and **unsafe**.
- Offering a centralized framework for evaluating and interpreting Granite Guardian outputs.

## Philosophy

The repository is grounded in the belief that **transparency, modularity, and extensibility** are key to understanding and improving content safety mechanisms in AI. By structuring the project around clear utilities and a shared prompt framework, Guardian Lighthouse ensures:
1. **Theoretical Insight**: Tools and scripts are designed not just for practical use but also to illuminate the underlying behavior of the models.
2. **Repeatability**: Shared prompts and utilities facilitate consistent testing and evaluation across diverse scenarios.
3. **Extensibility**: The project can evolve to incorporate new use cases, such as fine-tuning or deploying models in production pipelines.

## Model Scope

Guardian Lighthouse supports the following IBM Granite Guardian models:

### **1. Small HAP Models**
- **Models**: `granite-guardian-hap-38m`, `granite-guardian-hap-125m`.
- **Purpose**: Sequence classification models designed to identify Hate, Abuse, and Profanity in user prompts.
- **Key Features**:
  - Efficient inference with small model sizes.
  - Suitable for scenarios requiring low-latency decisions.

### **2. Large Guardian Models**
- **Models**: `granite-guardian-3.0-2b`.
- **Purpose**: Causal language models fine-tuned for detecting risks in generated responses.
- **Key Features**:
  - Ability to evaluate risks in both input prompts and generated outputs.
  - Advanced token-level probability analysis to distinguish between "safe" and "unsafe" outputs.

## Prompt Categorization

Prompts are categorized into three primary groups for evaluation:
- **Safe**: Benign prompts with no risk of unsafe content.
- **Ambiguous**: Prompts that may or may not lead to unsafe outputs depending on context.
- **Unsafe**: Explicitly harmful or policy-violating prompts designed to test model sensitivity.

This categorization allows systematic evaluation and comparison of model performance across varying levels of risk.

## Core Utilities

### **1. Testing Small Models**
- Script: `guardian-tiny.py`
- Functionality:
  - Tests HAP models for their ability to classify prompts into safe and unsafe categories.
  - Outputs maximum risk probability for each prompt.

### **2. Testing Large Models**
- Script: `guardian-2b.py`
- Functionality:
  - Evaluates the ability of causal language models to detect and respond to risky prompts.
  - Parses generated outputs and token-level probabilities to determine risk levels.

### **3. Shared Utilities**
- File: `utils.py`
- Components:
  - **Scoring Functions**:
    - `score_guardian_hap`: Evaluates sequence classification models.
    - `score_guardian_xl`: Evaluates causal language models.
  - **Aggregation**:
    - `aggregate_score`: Computes final risk labels and probabilities.
  - **Prompt Loader**:
    - `load_prompts`: Reads shared test prompts from a centralized JSON file.

## Theoretical Implications

Guardian Lighthouse provides a lens through which developers and researchers can explore:
1. **Sensitivity and Bias**:
   - Evaluate model thresholds for ambiguous or nuanced prompts.
   - Analyze potential biases in the models' training data and outputs.
2. **Risk Categorization**:
   - Investigate how the models differentiate between explicit and implicit risks.
   - Examine the influence of prompt engineering on risk detection accuracy.
3. **Scaling and Extensibility**:
   - Assess the trade-offs between small and large models in terms of latency, interpretability, and accuracy.

## Vision

Guardian Lighthouse aspires to become a benchmark for testing and evaluating content moderation systems. By combining theoretical rigor with practical tooling, the project serves as both a foundation for academic exploration and a bridge to real-world deployment.

We invite researchers, developers, and practitioners to build upon this work, contribute to its growth, and explore the uncharted territories of content safety in generative AI.

