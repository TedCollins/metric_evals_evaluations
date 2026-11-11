# GSM8K (Grade School Math 8K)

_Last updated: 2026-11-11 · Area: Knowledge & reasoning_

> **In one sentence:** GSM8K is a set of about 8,500 grade-school math word problems, each needing 2–8 steps of basic arithmetic. It became the standard "can this AI reason step by step?" test, and it is the benchmark on which chain-of-thought prompting made its name.

| | |
|---|---|
| **Released** | October 2021, Cobbe et al. (OpenAI) [1] |
| **Size** | 8,792 problems: 7,473 for training and 1,319 for testing [2] |
| **Format** | Word problem in, a written solution out. Only the **final number** is graded. |
| **Metric** | Accuracy: % of test problems where the final number matches the answer key |
| **Random guessing** | ~0% (answers are open-ended numbers, so there are no options to guess from) |
| **Human baseline** | No published human score. The authors estimate fewer than 2% of problems contain "breaking errors" [1]. |
| **Top scores (as of 2026-11-11)** | 94.4% verified (Gemini Ultra, majority vote over 32 tries, Dec 2023) [4]; 95.6% in Stanford's independent re-runs (Claude 3.5 Sonnet, Oct 2024) [11]; up to 99.6% unverified (MiMo-V2.5-Pro, 2026) [13] |
| **Status** | **Saturated.** Top models miss almost nothing except flawed questions (see below). |

---

## What it claims to test

**Multi-step mathematical reasoning.** In 2021, large language models could write fluent text but often fell apart on problems that needed several steps of reasoning in a row. One small mistake early on sinks the whole answer. The authors built GSM8K as problems that are *conceptually easy* (a bright middle-schooler could solve all of them) so that failures would show a reasoning breakdown, not a lack of advanced knowledge. [1]

Problems were written by human contractors (first freelancers on Upwork, then through Surge AI), and each comes with a worked solution in plain language. [1]

## What it actually tests

- **Turning a short story into arithmetic, and doing the arithmetic accurately.** Every problem needs only addition, subtraction, multiplication and division, across 2 to 8 steps. [1] There is no algebra, geometry or proof.
- **Keeping track of steps.** Most failures come from losing a quantity, misreading "half as much", or slipping on arithmetic partway through.
- **Following a familiar template.** The problems share a recognizable style: a named person, everyday objects, prices or times. Research shows models do worse when the same problems are reworded or the numbers are changed, so part of what GSM8K measures is familiarity with this style (see [Construct validity](#construct-validity)).

What it **doesn't** test: math beyond about 8th grade, word problems that need real-world judgment, or whether a model can explain *why* its method works.

## Example items

Real items from the GSM8K test split [2]. The answer key gives a worked solution and then the final number. Calculator annotations like `<<16-3-4=9>>` are removed here.

**The classic first item**
> Janet's ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in dollars does she make every day at the farmers' market?
>
> *Key:* 16 − 3 − 4 = 9 eggs; 9 × $2 = **$18**.

This is typical: two steps, everyday framing, one number out.

**A two-step item**
> A robe takes 2 bolts of blue fiber and half that much white fiber. How many bolts in total does it take?
>
> *Key:* 2 / 2 = 1 bolt of white; 2 + 1 = **3**.

**A questionable item**
> Josh decides to try flipping a house. He buys a house for $80,000 and then puts in $50,000 in repairs. This increased the value of the house by 150%. How much profit did he make?
>
> *Key:* the value goes up by 150% of the **$80,000 purchase price** ($120,000), to $200,000. Profit = $200,000 − $130,000 = **$70,000**.

"Increased the value by 150%" doesn't say 150% *of what*. A reader could just as reasonably apply it to the $130,000 spent in total, which gives a value of $325,000 and a profit of $195,000. A model that reads it that way gets marked wrong. **[suspected]** We don't know whether this item was among those removed from GSM8K-Platinum, but ambiguity like this is exactly what that clean-up targeted (see [Label and metric flaws](#label-and-metric-flaws)).

## How it's scored

1. The model gets the problem, usually after a few worked examples ([few-shot](../../glossary.md#few-shot)), and writes out a solution.
2. The evaluator extracts the **final number** from the response and checks it against the key ([exact match](../../glossary.md#exact-match)). The reasoning itself is not graded.

The headline number depends heavily on *how* the model is asked:

| Setup | What it means | Example |
|-------|---------------|---------|
| **Direct answer** | The model gives just the number | PaLM 540B: **17.9%** [3] |
| **[Chain-of-thought](../../glossary.md#chain-of-thought-cot)** | The model writes out its steps first | Same PaLM 540B: **56.9%** [3] |
| **[Majority vote](../../glossary.md#majority-vote-majk)** ("maj1@32") | The model answers 32 times and the most common answer counts | Gemini Ultra: **94.4%** [4] |
| **[Verifier](../../glossary.md#verifier)** | Many attempts are generated, and a second model picks the one it thinks is right | GPT-3 175B: **55%** [1][3] |

There are other variations too: the number of worked examples (0, 4, 5 or 8 are all common), whether the model may use a calculator or code, and how strictly the final number is pulled out of the text ("18", "$18" and "18 dollars" all need to count). Stanford's HELM, for example, uses 5 worked examples on 1,000 of the 1,319 test problems [11].

## History and scores

![Scatter chart of reported GSM8K scores by model release date, late 2021 to late 2026. Scores climb from 55% for GPT-3 with a verifier in 2021 to 92% for GPT-4 in March 2023, then bunch up between 90% and 97% from 2024 on. Stanford HELM's independent re-runs reach 95.6%, and the highest unverified score is 99.6% for MiMo-V2.5-Pro in 2026. PaLM 540B appears twice, at 17.9% answering directly and 56.9% with chain-of-thought prompting. Colors show the data source: primary reports, Stanford HELM and Epoch AI; unverified scores are hollow gray rings.](../../img/gsm8k-history-light.svg)

_Dark-theme version: [gsm8k-history-dark.svg](../../img/gsm8k-history-dark.svg)_

**How to read this chart.** Each point is one reported score. **Color shows where the number came from**:
- **Primary** (blue): taken by hand from the original paper or a model report, and checked by us [1][3][4][5].
- **HELM** (green): Stanford re-ran every model itself with the *same* setup: 5 worked examples, 1,000 test problems, exact match on the final number [11]. These points are truly comparable with each other.
- **Epoch AI** (orange): scores from papers and announcements, compiled by Epoch AI's Benchmarking Hub [10]. These are self-reported, and the setups vary.
- **Unverified** (hollow gray): self-reported scores listed by aggregator sites that we haven't checked against an original source [12][13]. Three 2026 models have no known release date, so they sit at the date an aggregator first listed them (`date_basis = reported` in the data).

The gray step line traces the best score reported so far across all sources and setups.

What stands out:
- **Prompting moved scores as much as new models did.** The same PaLM model scores 17.9% or 56.9% depending only on whether it is asked to show its working.
- **The climb took 18 months.** Scores went from 55% (the original paper's best, Oct 2021) to 92% (GPT-4, Mar 2023). Since 2024, almost every serious model scores between 90% and 97%.
- **Independent re-runs land a little lower.** HELM's best is 95.6%, while self-reported and aggregator scores reach 97–99.6%.
- **Outliers point to scoring problems.** ERNIE 4.5 is listed at 25.2% (unverified), far below models of similar size. That looks more like a data-entry or answer-parsing error than a real result.

Data: [`data/gsm8k/scores.csv`](../../../data/gsm8k/scores.csv), with one row per point and a source link on each row. Rebuild with `python3 scripts/build_gsm8k_scores.py`, then `python3 scripts/metric_history.py gsm8k`.

| When | What happened |
|------|---------------|
| Oct 2021 | Released by OpenAI. The best result in the paper is **55%**: a fine-tuned GPT-3 175B plus a verifier model that picks the best of many attempts. [1][3] |
| 2022 | Chain-of-thought prompting lifts PaLM 540B from **17.9%** to **56.9%** with no extra training, beating the fine-tuned approach. [3] GSM8K becomes the standard showcase for reasoning prompts. |
| Mar 2023 | GPT-4 reaches **92.0%** (5-shot chain-of-thought). [4][5] |
| Dec 2023 | Gemini Ultra reports **94.4%**, using a majority vote over 32 attempts. [4] |
| May 2024 | *GSM1k*, a fresh set of look-alike problems, shows some model families drop up to 8 points on it, a sign they had partly memorized GSM8K. [6] |
| Oct 2024 | *GSM-Symbolic* shows that changing names and numbers, or adding an irrelevant sentence, can sharply lower scores. [7] |
| Mar 2025 | *GSM8K-Platinum* removes or fixes 120 flawed test questions. [8][9] |
| 2025–2026 | Labs mostly stop reporting GSM8K. Aggregators list scores of 95–99.6%. [12][13] |

## Known issues

Evidence levels: **[documented]** published analysis · **[reported]** credible informal source · **[suspected]** our own reasoning.

### Contamination and saturation

- **[documented] Signs of memorization.** Researchers at Scale AI wrote GSM1k, a new set of problems carefully matched to GSM8K in style and difficulty. Several model families scored lower on GSM1k, by **up to 8 points**, and the overfitting showed up across almost all model sizes in those families. The size of the drop was correlated with how likely a model was to reproduce GSM8K questions (r² = 0.36), which suggests partial memorization. Frontier models showed **minimal** signs of overfitting. [6] (See [contamination](../../concepts/contamination.md).)
- **[documented] Saturation.** Stanford's independent re-runs top out at 95.6% [11]. On the cleaned-up GSM8K-Platinum, one model's error count fell from 45 to **2** [9]. So almost all of the remaining "errors" for top models are flawed questions, not model mistakes.

### Construct validity

- **[documented] Sensitive to surface changes.** Apple researchers built GSM-Symbolic, which generates many versions of the same GSM8K-style problems with different names and numbers. Every model they tested did worse when *only the numbers* changed, and scores varied noticeably between versions of the same question. Adding one plausible-sounding but irrelevant sentence cut accuracy by **up to 65%**. [7] This suggests part of a high GSM8K score reflects familiarity with these particular problems, not a general ability to reason.
- **[suspected] A narrow slice of "math".** Four operations at grade-school level is a reasonable test of careful step-tracking. It says little about mathematical ability more broadly. Harder benchmarks like MATH exist for that.

### Label and metric flaws

- **[documented] Flawed and ambiguous questions.** The original authors estimated fewer than 2% of problems have breaking errors. When contractors re-solved them, 1.7% ended in disagreement [1]. A 2025 review went further: of 219 test questions flagged by model disagreement, **110 were removed** (ambiguous or logically inconsistent) and **10 had wrong answer keys**. That is about 9% of the 1,319-question test set. [9]
- **[documented] Label noise hid real differences between models.** On the original test set, Claude 3.7 Sonnet (extended thinking) and Llama 405B each made **45 errors**. On the cleaned-up version, they made **2** and **17**, an eight-fold gap the noise had hidden. [9]
- **[documented] Setup changes the score dramatically.** The same model scored 17.9% answering directly and 56.9% with chain-of-thought [3]. Reported numbers mix direct answers, chain-of-thought, majority votes over up to 32 tries, and verifiers (see [How it's scored](#how-its-scored)).
- **[suspected] Answer extraction can fail.** Only the final number is graded, so a correct answer written in an unexpected format can be marked wrong. Implausibly low outliers, like ERNIE 4.5's listed 25.2%, are more likely extraction or data-entry failures than real results.

### Real-world gap

- **[documented] High scores don't mean full reliability.** Even after the clean-up, frontier models still fail some elementary math word problems [8]. A 97% score still means roughly 1 in 30 simple problems goes wrong, which matters if you rely on a model for routine calculations.
- **[suspected] Neat textbook problems are easier than real ones.** Real-world arithmetic tasks, like splitting bills, estimating or reading a spreadsheet, come with messy context and unstated assumptions. GSM8K's tidy, self-contained problems don't test that.

## How to read a score

- **Check the setup.** Chain-of-thought, majority vote (maj@k) and verifiers can each add tens of points. A "maj1@32" score isn't comparable to a single-attempt score.
- **Above ~95%, ignore small gaps.** Most of the remaining misses are flawed questions. If a model reports results on GSM8K-Platinum, use that number instead.
- **Distrust surprisingly low scores for large models.** They often point to answer-extraction or data-entry problems, not weak reasoning.
- **For a real test of math reasoning, look elsewhere.** GSM1k and GSM-Symbolic check for memorization. MATH and competition benchmarks test harder math.

## Related benchmarks

- **GSM8K-Platinum** [8][9]: the same test set with 110 flawed questions removed and 10 answer keys fixed.
- **GSM1k** [6]: new problems written to match GSM8K, used to detect memorization.
- **GSM-Symbolic** [7]: templates that generate fresh variants of GSM8K-style problems, including versions with an irrelevant sentence added.
- **MATH** (page to come): competition-level math problems.

## Sources

1. Cobbe, K. et al. (2021). *Training Verifiers to Solve Math Word Problems.* https://arxiv.org/abs/2110.14168
2. GSM8K dataset card (MIT license), Hugging Face. https://huggingface.co/datasets/openai/gsm8k
3. Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models.* https://arxiv.org/abs/2201.11903
4. Gemini Team, Google (2023). *Gemini: A Family of Highly Capable Multimodal Models*, Table 2. https://arxiv.org/abs/2312.11805
5. OpenAI (2023). *GPT-4 Technical Report.* https://arxiv.org/abs/2303.08774
6. Zhang, H. et al. (2024). *A Careful Examination of Large Language Model Performance on Grade School Arithmetic.* https://arxiv.org/abs/2405.00332
7. Mirzadeh, I. et al. (2024). *GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models.* https://arxiv.org/abs/2410.05229
8. Vendrow, J. et al. (2025). *Do Large Language Model Benchmarks Test Reliability?* https://arxiv.org/abs/2502.03461
9. Gradient Science (2025-03-06). *GSM8K-Platinum.* https://gradientscience.org/gsm8k-platinum/
10. Epoch AI, Benchmarking Hub, LLM benchmark data, "external runs", GSM8K (CC-BY; downloaded 2026-11-11). https://epoch.ai/benchmarks/use-this-data
11. Stanford CRFM, HELM Lite leaderboard, GSM8K, release v1.13.0 (2025-01-10). https://crfm.stanford.edu/helm/lite/latest/
12. llm-stats, GSM8K leaderboard (self-reported scores; accessed 2026-11-11). Not independently verified. https://llm-stats.com/benchmarks/gsm8k
13. benchmarklist.com, GSM8K (sampled 2026-05-06). Not independently verified. https://benchmarklist.com/benchmarks/gsm8k/
