# Glossary

Plain-language definitions of terms used across these docs.

### Accuracy
The percentage of questions a model answers correctly. On a 4-option multiple-choice test, random guessing gets 25%.

### Answer key
The official list of correct answers for a benchmark. Keys can contain mistakes. See [MMLU](benchmarks/knowledge-reasoning/mmlu.md#label-and-metric-flaws).

### Benchmark
A fixed set of test questions or tasks, plus a scoring rule, used to compare AI models.

### Calibration
Whether a model's confidence matches how often it is actually right. A well-calibrated model that says "80% sure" is right about 80% of the time.

### Chain-of-thought (CoT)
Prompting a model to reason step by step before giving its final answer. It usually raises scores on reasoning questions.

### Contamination
When test questions, or their answers, appear in the data a model was trained on, so the model can recall them instead of working them out. See [concepts/contamination](concepts/contamination.md).

### Construct validity
Whether a test measures the thing it claims to measure. A "reasoning" test that can be passed by memorizing has weak construct validity.

### Few-shot
Showing the model a few solved examples ("shots") in the prompt before the real question. "5-shot" means five examples. **Zero-shot** means no examples.

### Leaderboard
A public ranking of models by their benchmark scores.

### Saturation
When the top models score close to the maximum possible on a benchmark, so it can no longer tell them apart.

### Training data
The large body of text (mostly from the web) that a model learns from before it is released.
