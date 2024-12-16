# Guardian Model Evaluation Framework

## Scope Definition

This benchmark framework specifically evaluates IBM's Guardian model's capabilities for harmful and adversarial prompt (HAP) detection, deliberately focusing on model-level evaluation rather than system-level vulnerabilities.

### What We Test
- Core detection capabilities of the Guardian model
- Direct prompt evaluation performance
- Classification accuracy across various harm categories
- Model robustness against single-prompt attacks
- Performance on established HAP detection benchmarks

### What We Don't Test
- System-level vulnerabilities
- Multi-request attack patterns
- Stateful attack vectors
- Deployment architecture exploits
- Rate limiting or caching behaviors
- Infrastructure-level security concerns

### Rationale
This scope limitation is a deliberate choice to:
1. Ensure clear separation between model capabilities and deployment considerations
2. Enable fair comparison with other HAP detection models
3. Provide reproducible benchmarking results independent of deployment choices
4. Focus on fundamental detection capabilities rather than implementation-specific vulnerabilities

### Future Work
While system-level evaluation is crucial for production deployments, it represents a separate research direction that would require different evaluation methodologies and benchmarking approaches.
