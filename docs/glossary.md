# Glossary

Plain-language definitions of terms used across these docs.

### Accuracy
The percentage of questions a model answers correctly. On a 4-option multiple-choice test, random guessing gets 25%.

### Adversarial filtering
Keeping only the test questions that current AI models get wrong. It makes a benchmark hard at launch, but skews it toward whatever those particular models happened to be bad at.

### Answer key
The official list of correct answers for a benchmark. Keys can contain mistakes. See [MMLU](benchmarks/knowledge-reasoning/mmlu.md#label-and-metric-flaws).

### Benchmark
A fixed set of test questions or tasks, plus a scoring rule, used to compare AI models.

### Calibration
Whether a model's confidence matches how often it is actually right. A well-calibrated model that says "80% sure" is right about 80% of the time. **Calibration error** measures the gap (0% is perfect).

### Canary string
A unique random code placed inside a benchmark's files. Companies training AI models can search their training data for it and remove any text that contains it, which keeps the test questions out of what the model learns from.

### Chain-of-thought (CoT)
Prompting a model to reason step by step before giving its final answer. It usually raises scores on reasoning questions.

### Contamination
When test questions, or their answers, appear in the data a model was trained on, so the model can recall them instead of working them out. See [concepts/contamination](concepts/contamination.md).

### Construct validity
Whether a test measures the thing it claims to measure. A "reasoning" test that can be passed by memorizing has weak construct validity.

### Exact match
Scoring a response as correct only if its final answer matches the answer key exactly (for example, the same final number). The reasoning isn't graded.

### Few-shot
Showing the model a few solved examples ("shots") in the prompt before the real question. "5-shot" means five examples. **Zero-shot** means no examples.

### Judge model
An AI model used to grade another model's answers, for example to decide whether a free-text answer means the same as the answer key. Convenient, but it can make its own grading mistakes.

### Leaderboard
A public ranking of models by their benchmark scores.

### Majority vote (maj@k)
Asking the model the same question *k* times and counting the most common answer. "maj1@32" means a majority vote over 32 attempts. This usually raises scores, so it isn't comparable with a single-attempt score.

### Reasoning effort
A setting on many 2025–2026 models that controls how long the model "thinks" (how much hidden step-by-step reasoning it does) before answering. Higher effort usually means higher scores, so the same model can post very different numbers.

### Saturation
When the top models score close to the maximum possible on a benchmark, so it can no longer tell them apart.

### Standard error
A measure of how much a score would move by chance, for example if the test had a different random sample of questions or the model answered again. A score of 90% ± 2 means differences of a point or two aren't meaningful.

### Tool use
Letting a model call outside tools while answering, such as web search, a calculator or a code interpreter. Scores with tools are usually much higher than without, so the two aren't comparable.

### Training data
The large body of text (mostly from the web) that a model learns from before it is released.

### Verifier
A second model trained to judge whether a solution is correct. The main model generates many attempts, and the verifier picks the one it rates most likely to be right.
