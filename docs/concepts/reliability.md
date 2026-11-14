# Reliability

_Last updated: 2026-11-14_

> **In one sentence:** Accuracy tells you how often a model is right *on average*. Reliability asks the questions that matter when you actually depend on it: does it get it right *every* time, does it know when it might be wrong, and can you trust the score in the first place?

"Reliability" covers two different things in AI evaluation:

1. **Is the model reliable?** Is it consistent, aware of its own uncertainty, and robust to small changes?
2. **Is the benchmark reliable?** Is the score stable, and are the answer keys trustworthy?

Both matter. An unreliable benchmark can't measure a model's reliability.

---

## Why accuracy isn't enough

Imagine two models that each score **80%** on a test.

- **Model A** gets the same 80% of questions right every time you ask, and says "I'm not sure" on the rest.
- **Model B** is right 80% of the time *on each attempt*, but which questions it gets wrong changes from run to run, and it sounds equally confident either way.

They have the same accuracy, but you'd trust A far more. Suppose you need B to complete a task correctly on **all of 8 tries** (an assistant handling the same kind of request eight times a day, say). If each try were an independent 80% chance, it would manage that only 0.8⁸ ≈ **17%** of the time. In practice, a model's attempts at the same task are correlated, so the real number is measured directly instead of calculated. That is exactly what the first metric below does.

## Part 1: Is the model reliable?

### Does it succeed every time? (pass^k)

**[pass^k](../glossary.md#passk)** ("pass-hat-k") is the chance a model succeeds on **all k** independent attempts at the same task. Plain accuracy (pass^1) asks whether it succeeds once. pass^8 asks whether you could count on it eight times in a row.

The metric was introduced with **τ-bench**, a benchmark where AI agents handle customer-service tasks such as changing an airline booking or processing a retail return, using tools and following company policy. In the original 2024 results, even GPT-4o succeeded on fewer than half the tasks, and its **pass^8 in the retail setting was below 25%**. [1] A model that looks "usually fine" in a demo can be unreliable at scale.

*Ask of any score:* is this one attempt, or success across repeated attempts?

### Does it know when it might be wrong? (calibration)

**[Calibration](../glossary.md#calibration)** compares a model's stated confidence with how often it's actually right. If it says "90% sure" on 100 answers, about 90 should be correct. **Calibration error** measures the gap: 0% is perfect, and higher is worse.

Our [Humanity's Last Exam card](../benchmarks/knowledge-reasoning/hle.md#calibration-do-models-know-when-they-dont-know) tracks this. GPT-4o had a calibration error of **89%** in January 2025, meaning it was confidently wrong almost everywhere. By September 2026, Claude Fable 5.1 was down to **20%**. The most accurate model isn't the best calibrated one, so the two need to be checked separately. [2]

*Ask of any score:* is calibration reported? A model that knows which answers to double-check is more useful than a slightly more accurate one that doesn't.

### Does it say "I don't know"? (abstention and hallucination)

A **[hallucination](../glossary.md#hallucination)** is a confident but false answer. One way to measure it is to let the model **[abstain](../glossary.md#abstention)** ("I don't know") and score three outcomes separately: correct, incorrect and not attempted.

**SimpleQA** (OpenAI, 2024) does exactly this with short factual questions that each have one indisputable answer. The authors frame the ideal model as one that answers as many questions correctly as possible while declining the ones it isn't confident about. In other words, it "knows what it knows". [3] A model that abstains on 30% and gets the rest right is more reliable than one that answers everything and is wrong 30% of the time, even though both are "70% correct".

*Ask of any score:* were wrong answers and abstentions counted separately, or lumped together as "not correct"?

### Does it hold up when the question changes slightly? (robustness)

**[Robustness](../glossary.md#robustness)** is how much performance drops when a question is reworded, its names or numbers are changed, or an irrelevant detail is added.

- **GSM-Symbolic** rewrote grade-school math problems with new names and numbers. Every model tested did worse, and adding one irrelevant sentence cut accuracy by **up to 65%**. [4] (See the [GSM8K card](../benchmarks/knowledge-reasoning/gsm8k.md#construct-validity).)
- **Prompt sensitivity:** on MMLU, simply changing the prompt wording moves scores by about **4–5 points**. The harder MMLU-Pro cut that to about 2 points. [5] (See the [MMLU card](../benchmarks/knowledge-reasoning/mmlu.md#label-and-metric-flaws).)

*Ask of any score:* was it measured on one fixed phrasing, or checked across variations?

### Does it fail on easy things? (platinum benchmarks)

Headline benchmarks hide simple mistakes behind flawed questions. **Platinum benchmarks** remove ambiguous or mislabeled questions, so any remaining error is a genuine model mistake. On the cleaned-up GSM8K, two models that each made 45 errors on the original made **2** and **17**, and frontier models still failed some elementary problems. [6] (See the [GSM8K card](../benchmarks/knowledge-reasoning/gsm8k.md#label-and-metric-flaws).)

*Ask of any score:* on questions known to be clean, how many does the model still get wrong?

### How long a task can it handle before it breaks? (time horizon)

METR measures a model's **time horizon**: the length of task (measured in how long it takes a skilled human) that the model completes with a given success rate. Their headline uses **50% success**. By that measure, frontier models' horizons have roughly doubled every seven months since 2019. [7] METR also publishes horizons at **80% success**, which by definition are shorter: if you insist the model succeeds more often, it can only handle shorter tasks. [8]

*Ask of any score:* at what success rate? "Can do hour-long tasks" at 50% success is a much weaker claim than at 80%.

## Part 2: Is the benchmark reliable?

Even a perfect model gets an unreliable score from an unreliable test. Our metric cards check these under "Label and metric flaws":

| Question | Metric | Example from our cards |
|----------|--------|------------------------|
| **How much would the score move by chance?** | [Standard error](../glossary.md#standard-error) or confidence interval. Statisticians recommend reporting error bars on every evaluation result. [9] | GPQA Diamond has only 198 questions, so top scores carry about **±1–2 points** ([card](../benchmarks/knowledge-reasoning/gpqa-diamond.md#how-its-scored)) |
| **Are the answer keys right?** | Label error rate: the share of questions that are wrong or ambiguous | MMLU ~6.5%, GSM8K ~9%, HLE: errors in **22 of 48** sampled questions ([HLE card](../benchmarks/knowledge-reasoning/hle.md#label-and-metric-flaws)) |
| **Do experts agree on the answers?** | Inter-annotator agreement (how often independent experts reach the same answer) | GPQA: experts agreed with the question writer about **74%** of the time across all questions ([card](../benchmarks/knowledge-reasoning/gpqa-diamond.md#label-and-metric-flaws)) |
| **Does the evaluation code matter?** | Implementation sensitivity | The same model scored **63.7%** or **48.8%** on MMLU depending on how its answer was read ([card](../benchmarks/knowledge-reasoning/mmlu.md#how-its-scored)) |
| **Does a re-run give the same score?** | Test–retest stability, from repeated runs | Epoch AI runs GPQA Diamond many times per model and reports the spread ([card](../benchmarks/knowledge-reasoning/gpqa-diamond.md)) |

## Quick reference

| You want to know… | Look for | A warning sign |
|-------------------|----------|----------------|
| Will it work *every* time? | pass^k, repeated-run consistency | Only a single-run accuracy is reported |
| Does it know when it's unsure? | Calibration error | No confidence or calibration data at all |
| Will it make things up? | Hallucination rate; abstentions scored separately | "Accuracy" with no count of confidently wrong answers |
| Does it hold up to rewording? | Scores on perturbed or paraphrased versions | One fixed prompt; big drops on rephrased variants |
| Is the score itself trustworthy? | Error bars, label error rate, independent re-runs | No error bars; a known-flawed benchmark; self-reported only |

## How our metric cards cover reliability

- **Benchmark reliability** is covered on every card, under *Label and metric flaws* (answer-key errors, implementation sensitivity, standard errors) and through the **effective ceiling**.
- **Model reliability** is covered only in parts so far: calibration (HLE), robustness (GSM8K, MMLU) and platinum-style error counts (GSM8K). A future card for a reliability benchmark (SimpleQA Verified for hallucination, or τ-bench for pass^k) would measure it directly.

## Sources

1. Yao, S. et al. (2024). *τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains.* https://arxiv.org/abs/2406.12045
2. Epoch AI, Benchmarking Hub, HLE "external runs" (official HLE evaluation with calibration errors), and Phan, L. et al. (2025), *Humanity's Last Exam*, Table 1. See the [HLE card](../benchmarks/knowledge-reasoning/hle.md#sources).
3. Wei, J. et al. (2024). *Measuring short-form factuality in large language models* (SimpleQA). https://arxiv.org/abs/2411.04368
4. Mirzadeh, I. et al. (2024). *GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models.* https://arxiv.org/abs/2410.05229
5. Wang, Y. et al. (2024). *MMLU-Pro: A More Robust and Challenging Multi-Task Language Understanding Benchmark.* https://arxiv.org/abs/2406.01574
6. Vendrow, J. et al. (2025). *Do Large Language Model Benchmarks Test Reliability?* https://arxiv.org/abs/2502.03461, and Gradient Science (2025), *GSM8K-Platinum*, https://gradientscience.org/gsm8k-platinum/
7. Kwa, T. et al. (2025). *Measuring AI Ability to Complete Long Software Tasks.* https://arxiv.org/abs/2503.14499
8. METR (2025-03-19). *Measuring AI Ability to Complete Long Tasks* (shows 50% and 80% success horizons). https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/
9. Miller, E. (2024). *Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations.* https://arxiv.org/abs/2411.00640
