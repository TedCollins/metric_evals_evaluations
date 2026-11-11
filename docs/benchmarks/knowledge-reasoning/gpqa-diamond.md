# GPQA Diamond (Graduate-Level Google-Proof Q&A)

_Last updated: 2026-11-11 · Area: Knowledge & reasoning_

> **In one sentence:** GPQA Diamond is 198 very hard multiple-choice questions in biology, physics and chemistry, written by PhD-level experts. It is designed so that skilled people *outside* the field can't answer the questions even with unlimited web search, and in 2025–2026 it became the headline "expert knowledge" benchmark that replaced MMLU.

| | |
|---|---|
| **Released** | November 2023, Rein et al. (NYU, Cohere, Anthropic) [1] |
| **Size** | 198 questions (the "Diamond" subset of 448 main / 546 extended GPQA questions) [1] |
| **Format** | Multiple choice, 4 options |
| **Metric** | Accuracy (% correct). Each question is worth about 0.5 points. |
| **Random guessing** | 25% |
| **Human baseline** | PhD experts answering in their own field: ~65%, or 74% after discounting clear slips. Skilled non-experts with web search: ~34% (both measured on all GPQA questions) [1] |
| **Top scores (as of 2026-11-11)** | 96.5% in Epoch AI's independent runs (Gemini 4 Carbon, Oct 2026) [6]; 83.4% in the newest score we checked by hand (o3, high effort, Apr 2025) [5]; 96.0% self-reported (GPT-6 Astra) [7] |
| **Status** | **Near saturation.** Top independent scores sit above Epoch's estimated ceiling of about 92% (see below). |

---

## What it claims to test

**Expert-level scientific knowledge and reasoning that you can't simply look up.** The authors hired 61 contractors who had completed or were in a PhD program to write questions in their own field. Each question went through two rounds of review by other experts, then three non-experts (PhD-level people from *other* fields) tried it with unrestricted web access, spending 37 minutes per question on average. [1]

The benchmark was also designed for **scalable oversight** research: how can people supervise AI systems on questions the people themselves can't answer? For that, you need questions where experts reliably know the answer and capable non-experts reliably don't. [1]

**Diamond** is the highest-quality slice. A question makes it in only when **both expert reviewers got it right** (or one did and the other made a clear, acknowledged mistake), **and** at most one of the three non-experts got it right. [1][3]

## What it actually tests

- **Deep, specialized science knowledge.** The questions sit at graduate-research level: organic reaction mechanisms, quantum mechanics, molecular biology.
- **Multi-step reasoning with that knowledge.** Most questions can't be answered by recalling one fact. You have to apply concepts across several steps.
- **Picking the right option out of four.** It is still multiple choice. A model can eliminate options, and a lucky guess counts the same as real understanding.

Coverage is **uneven**. Across the full extended set there are 227 physics, 214 chemistry and 105 biology questions [1]. Organic chemistry alone makes up about 36% of Diamond [4], and it is also where most of the remaining hard questions are (see [Known issues](#known-issues)).

What it **doesn't** test: doing science (designing experiments, reading papers, writing up results), explaining an answer, or knowing when a question is badly posed.

## Example items

> ⚠️ **We don't reproduce real GPQA questions.** The authors ask everyone *not* to publish examples "in plain text or images online", and the dataset requires agreeing to that before you can download it [1][2]. The point is to keep the questions out of the web text that AI models learn from (see [contamination](../../concepts/contamination.md)). The dataset files also carry a [canary string](../../glossary.md#canary-string) so that companies training AI models can find and remove them.

**An illustrative question we wrote ourselves, in the GPQA style.** It is much easier than a real GPQA question.

> A particle in a one-dimensional infinite square well of width *L* is prepared at t = 0 in the equal superposition of its ground state and first excited state, ψ = (ψ₁ + ψ₂)/√2. What is the probability of finding the particle in the left half of the well (0 ≤ x ≤ L/2) at t = 0?
>
> (A) 1/2 **(B) 1/2 + 4/(3π)** (C) 1/2 − 4/(3π) (D) 1/2 + 2/(3π)

The "obvious" answer is (A): each state on its own is symmetric, so it splits 50/50. But the cross term between the two states doesn't cancel over half the well, so the answer is about 0.92. Real GPQA questions use the same trick of making a plausible shortcut lead to a wrong option, but they need far more specialized knowledge. Experts take minutes, and outsiders with Google often still get them wrong.

The real questions cover topics like organic synthesis pathways, spectroscopy, quantum field theory and genetics (one example in the paper asks about cross-species fertilization). [1]

## How it's scored

1. The model sees the question and four options, usually with an instruction to think step by step ([chain-of-thought](../../glossary.md#chain-of-thought-cot)).
2. The final letter is extracted and compared with the key. Score = % correct out of 198.

Things that change the number:
- **[Reasoning effort](../../glossary.md#reasoning-effort).** Many 2025–2026 models can be told how long to "think". In Epoch AI's runs, the same model can score very differently. GPT-5.6 Luna scored **63.6%** with no extra reasoning and **91.6%** at maximum, and GPT-5.5 scored **77.3%** versus **94.0%**. [6] Labs usually report their best setting.
- **Answer extraction.** OpenAI notes it had to tweak its answer-matching pattern for GPQA [5]. A few Epoch runs score *below* random guessing (9–13%), which suggests the model's answers weren't being read correctly, not that it knew less than chance. **[suspected]**
- **A small test means noisy scores.** With only 198 questions, one more right answer adds 0.5 points. Epoch reports a [standard error](../../glossary.md#standard-error) of about **±1–2 points** for top models [6]. So two models a point apart are effectively tied.

## History and scores

![Scatter chart of GPQA Diamond scores by model release date, 2023 to late 2026. Scores rise from 38.8% for GPT-4 in the original 2023 paper, past the roughly 65% expert line with o1-preview in late 2024, to about 92% by late 2025. Epoch AI's independent runs then reach 96.5% (Gemini 4 Carbon, October 2026), above the shaded band that starts at about 92%, where questions are estimated to be invalid. Colors show the data source: primary reports, and Epoch AI's independent runs; self-reported scores are hollow gray rings, which mostly sit close to the independent runs.](../../img/gpqa_diamond-history-light.svg)

_Dark-theme version: [gpqa_diamond-history-dark.svg](../../img/gpqa_diamond-history-dark.svg)_

**How to read this chart.** Each point is one reported score. **Color shows what kind of source the number came from**:
- **Primary** (blue): checked by hand against the original paper or OpenAI's evaluation repo [1][5]. Claude and Llama scores in that repo are listed as the vendors reported them.
- **Independent: Epoch AI** (green): Epoch ran every model through the *same* evaluation setup [6]. When Epoch tested several reasoning settings for a model, we show its best one, which is how labs report too. This is the main source here, with 235 models up to November 2026.
- **Unverified** (hollow gray): self-reported scores listed on llm-stats, which we haven't checked against the labs' own reports [7]. They are dated by Epoch's release date for the same model.

There is no "Compiled" source for this benchmark. Epoch runs GPQA Diamond itself instead of collecting other people's reported scores.

The gray step line traces the best score reported so far.

What stands out:
- **It went from hard to nearly solved in about two years.** GPT-4 scored 38.8% at launch (Nov 2023). o1-preview passed the experts' ~65% in September 2024. Gemini 3 Pro reached 92.6% in independent runs by November 2025.
- **Top independent scores are now above the estimated ceiling.** Epoch estimated about 8% of questions are invalid, which leaves roughly 92% answerable. Fifteen models have since scored 94–96.5% in Epoch's own runs. See [Label and metric flaws](#label-and-metric-flaws) for what that might mean.
- **Self-reports mostly match independent runs, but not always.** Many are within about a point (Gemini 3.1 Pro: 94.3% self-reported vs 94.4% in Epoch's run; GPT-6 Astra: 96.0% vs 95.8%). Some are well above it (Claude Sonnet 4.6: 89.9% vs 83.3%; Claude Opus 4.7: 94.2% vs 90.2%; GPT-5.2: 92.4% vs 88.2%). [6][7]

Data: [`data/gpqa_diamond/scores.csv`](../../../data/gpqa_diamond/scores.csv), with one row per point and a source link on each row. Rebuild with `python3 scripts/build_gpqa_diamond_scores.py`, then `python3 scripts/metric_history.py gpqa_diamond`.

| When | What happened |
|------|---------------|
| Nov 2023 | Released. The best baseline is GPT-4 at **38.8%** (few-shot chain-of-thought), close to the non-experts' ~34%. [1] |
| 2024 (first half) | Claude 3 Opus (**50.4%**) and Claude 3.5 Sonnet (**59.4%**) push past 50%. [5] |
| May 2024 | After someone points out a flawed question online, an author replies that errors cap the ceiling but don't invalidate the benchmark. [3] |
| Sep–Dec 2024 | "Reasoning" models arrive: o1-preview scores **73.3%** and o1 scores **75.7%**, beating the experts' ~65%. [5] |
| Apr 2025 | o3 (high effort) reaches **83.4%**. [5] |
| May 2025 | Epoch AI reviews the questions models still miss and estimates about **8%** of Diamond is invalid. [4] |
| Nov 2025 | Gemini 3 Pro scores **92.6%** in Epoch's runs, at the estimated ceiling. [6] |
| 2026 | Independent scores reach **96.5%** (Gemini 4 Carbon, Oct 2026). [6] |

## Known issues

Evidence levels: **[documented]** published analysis · **[reported]** credible informal source · **[suspected]** our own reasoning.

### Contamination and saturation

- **[documented] Strong steps against contamination.** Downloading the dataset requires agreeing not to publish its questions, the files carry a canary string, and the authors ask that examples never appear online. [1][2] That is far more protection than MMLU or GSM8K have.
- **[suspected] But protection isn't immunity.** Every evaluation sends all 198 questions to the model provider's servers, over and over. The canary string only works if training pipelines actually filter for it. And with so few questions, even partial leakage would matter. There is no published contamination study for GPQA comparable to the ones for MMLU and GSM8K.
- **[documented] Near saturation.** Epoch found that 14 models scoring at least 70% together got the majority right on **158 of the 198 questions (80%)**, and their mistakes clustered on the remaining 40 [4]. Top independent scores have since reached 96.5% [6].

### Construct validity

- **[documented] "Google-proof" is defined narrowly.** It means skilled non-experts with web access (but no AI assistants) for about half an hour still mostly fail [1]. It doesn't mean the answers can't be found anywhere, and it doesn't test whether a model could find them with tools.
- **[documented] Multiple choice caps what it measures.** Epoch's review suggests future versions should drop the multiple-choice format and report results by skill area [4]. With four options, elimination and guessing still help.
- **[documented] Uneven topics.** Organic chemistry is about 36% of Diamond but **70%** of the 40 questions models still struggle with [4]. A single overall score hides that imbalance, and it may reflect a real weakness (spatial and diagram reasoning) or simply more flawed questions in that area.

### Label and metric flaws

- **[documented] Some questions are wrong or ambiguous.** Across all GPQA questions, expert validators agreed with the question writer only about 74% of the time, even after discounting their own clear mistakes [1][3]. Diamond's double-agreement filter removes most of these, but its true error rate was never measured directly. [3]
- **[documented] Epoch's estimate: about 8% invalid.** Epoch reviewed six of the seven questions on which top models score under 5%, judged about 2.25 of them invalid, and extrapolated that rate to the 40 hard questions. That gives roughly **15 of 198 (8%)** invalid, with "at least 90%" of the benchmark valid. [4] This is an estimate built on a small sample.
- **[suspected] Scores above the ceiling need explaining.** If ~8% of questions are invalid, a perfect model should top out near 92%, yet fifteen models score 94–96.5% in Epoch's runs [6]. The possible explanations:
  1. Fewer questions are invalid than estimated. The sample was small.
  2. Models have learned to predict the question writers' answers, mistakes included. One of the original authors notes that past the expert-agreement level, gains increasingly reflect "predicting writers' systematic mistakes" [3].
  3. Some contamination.

  We can't tell these apart with public data.
- **[documented] Small size makes scores noisy.** Standard errors of about 1–2 points [6] mean leaderboard gaps of a point or two at the top aren't meaningful.
- **[documented] Reasoning settings swing scores by up to ~30 points** for the same model [6]. A score without its setting is incomplete.

### Real-world gap

- **[suspected] Answering expert questions isn't doing expert work.** Picking the right option on a hard chemistry question is a long way from planning a synthesis or noticing that a question is badly posed. A model scoring 95% isn't therefore a working scientist.
- **[reported] Self-reports sometimes run higher.** In our comparison, several self-reported scores sit 4–7 points above the same model's best independent run [6][7]. When stakes are high, prefer independent numbers.

## How to read a score

- **Prefer independent runs.** For GPQA Diamond, Epoch AI's runs use the same setup for every model and report error bars. Use them over self-reports.
- **Ask which reasoning setting was used.** "Max effort" and "no reasoning" can differ by 20–30 points for the same model.
- **Treat gaps under ~2 points as ties.** With 198 questions, one or two questions decide them.
- **Above ~92%, scores say little about real ability.** The remaining questions are mostly flawed or hinge on disputed keys. Look at newer, harder benchmarks (such as Humanity's Last Exam) to tell frontier models apart.

## Related benchmarks

- **GPQA main / extended** [1]: the larger 448- and 546-question sets, with less strict quality filtering.
- **MMLU** ([card](mmlu.md)): broader but far easier, and saturated earlier.
- **Humanity's Last Exam** (page to come): expert-written frontier questions intended as GPQA's successor.

## Sources

1. Rein, D. et al. (2023). *GPQA: A Graduate-Level Google-Proof Q&A Benchmark.* https://arxiv.org/abs/2311.12022
2. GPQA dataset card (CC BY 4.0, gated: users agree not to reveal examples online), Hugging Face. https://huggingface.co/datasets/Idavidrein/gpqa
3. Rein, D. (2024-05-15). Blog post on GPQA question validity, NYU Alignment Research Group. https://wp.nyu.edu/arg/?p=139
4. Burnham, G. (2025-05-30). *GPQA Diamond: What's left?* Epoch AI, Gradient Updates. https://epoch.ai/gradient-updates/gpqa-diamond-whats-left
5. OpenAI, *simple-evals* (GPQA scores; README notes an answer-regex tweak for GPQA; o3/o4-mini run without tools). https://github.com/openai/simple-evals
6. Epoch AI, Benchmarking Hub, GPQA Diamond, Epoch's own runs with standard errors (CC-BY; downloaded 2026-11-11). https://epoch.ai/benchmarks/gpqa-diamond
7. llm-stats, GPQA leaderboard (262 of 265 results self-reported; accessed 2026-11-11). Not independently verified. https://llm-stats.com/benchmarks/gpqa
