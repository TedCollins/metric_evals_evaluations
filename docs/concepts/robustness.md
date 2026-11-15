# Robustness

_Last updated: 2026-11-15_

> **In one sentence:** Robustness asks whether a model keeps performing when something changes that *shouldn't* matter, such as the wording of a question, the order of the options, an irrelevant sentence, a new kind of data or a deliberate attack.

## Robustness vs. reliability

Robustness is one part of [reliability](reliability.md), and it's easy to confuse with consistency:

| | Consistency (e.g. [pass^k](../metrics/pass-k.md)) | Robustness |
|---|---|---|
| **The test** | The **same** task, repeated | A **slightly changed** version of the task |
| **The question** | Does it succeed *every time*? | Does it still succeed *when things change*? |
| **Example failure** | Solves a math problem on 3 tries out of 4 | Solves it, but fails when the names and numbers change |

A model can be consistent but fragile: it always gives the same answer, but a reworded question flips that answer. It can also be robust but inconsistent: rewording doesn't matter much, but every run is a coin flip. You need both.

---

## Six kinds of robustness

### 1. Wording and format

**What changes:** paraphrases, typos, the prompt template, the answer format, or the order of multiple-choice options. None of these change the correct answer.

**What happens:**
- On MMLU, changing only the prompt wording moves scores by about **4–5 points**. The harder MMLU-Pro reduced that to about 2. [1] (See the [MMLU card](../benchmarks/knowledge-reasoning/mmlu.md#label-and-metric-flaws).)
- Shuffling the order of answer options, or changing how the answer is picked, moved models **up to 8 places** on a leaderboard. [2]
- Formatting alone (spacing, separators, capitalization in the prompt) produced differences of **up to 76 accuracy points** for one open model (LLaMA-2-13B) in a 2023 study. The sensitivity didn't go away with larger models, more examples or instruction tuning. [3]

*Ask of any score:* was it measured with one fixed prompt, or across several reasonable phrasings? The same study proposes reporting the **range** of scores across formats, not a single number. [3]

### 2. Changed values, same problem

**What changes:** the names, numbers or details of a problem, with the same reasoning still required.

**What happens:**
- GSM-Symbolic rewrote grade-school math problems from templates. Every model tested did worse when **only the numbers** changed, and scores varied noticeably between versions of the same question. [4]
- GSM1k, a fresh set of look-alike math problems, showed drops of **up to 8 points** for some model families. [5] (See the [GSM8K card](../benchmarks/knowledge-reasoning/gsm8k.md#construct-validity).)

This kind of test doubles as a **[contamination](contamination.md)** check: a big drop on fresh variants suggests the model memorized the originals.

*Ask of any score:* does the model hold up on new versions of the questions, or only on the published ones?

### 3. Irrelevant or distracting information

**What changes:** an unneeded sentence is added, or the key fact is buried in a long document.

**What happens:**
- Adding one plausible-sounding but irrelevant clause to math problems cut accuracy by **up to 65%**. [4]
- In long inputs, models use information best when it's near the **beginning or end**, and worse when it's in the **middle**, even models built for long contexts. [6]

*Ask of any score:* were the test inputs clean and short, or realistic and cluttered?

### 4. Distribution shift

**What changes:** the test data comes from a different source, time, domain or population than the data the model learned from. Examples include new kinds of documents, other languages, rare subgroups and events after the training cutoff.

**How it's measured:**
- **Out-of-distribution accuracy:** the score on the shifted data, compared with the original.
- **Worst-group accuracy:** the score on the weakest subgroup (a language, dialect or topic). It shows who the model fails.
- **Effective robustness:** whether a model does better on shifted data than its ordinary accuracy would predict. Many models simply lose a predictable amount, and genuine robustness means beating that trend.

**What happens:** a large study of image classifiers (204 models, 213 test conditions) found that robustness to **artificial** changes (added noise or blur) usually **didn't carry over** to **natural** shifts in real-world data. Training on more diverse data helped most, but large gaps remained. [7]

*Ask of any score:* was it tested on data like the training data, or on genuinely new situations?

### 5. Adversarial attacks

**What changes:** someone deliberately crafts inputs to make the model fail, for example a **[jailbreak](../glossary.md#jailbreak)** that tricks it into producing harmful content, or an injected instruction hidden in a document.

**How it's measured:**
- **[Attack success rate](../glossary.md#attack-success-rate-asr)**: the share of attack attempts that succeed. *Lower is better.*
- **Robust accuracy**: accuracy when inputs are under attack.

**Example:** HarmBench, a standard framework for automated red-teaming, compared **18** attack methods against **33** models and defenses. [8]

*Ask of any score:* which attacks were tried, and were they strong ones? A low attack success rate against weak attacks proves little.

### 6. Environment faults (for agents)

**What changes:** for AI agents, the world around the model. A tool returns an error, a website changes its layout, an interface changes, or instructions arrive worded differently.

**How it's measured:** success rate when faults are deliberately injected, compared with success without them. Princeton HAL's agent reliability dashboard reports separate robustness scores for **fault** handling, **structural** changes and **prompt** changes on τ-bench airline. [9] (See the [τ-bench card](../benchmarks/agents/tau-bench.md).)

*Ask of any score:* was the agent tested only in a perfect environment?

---

## Measuring robustness well

Most robustness metrics come down to a few simple calculations:

| Metric | How it's calculated | What it tells you |
|--------|--------------------|-------------------|
| **Absolute drop** | Original score − score on the changed version | How many points are lost |
| **Relative drop** | Absolute drop ÷ original score | The share of performance lost. Fairer when comparing strong and weak models. |
| **Spread** | Highest − lowest score across variants (e.g. prompt formats) | How much a reported number depends on arbitrary choices |
| **[Worst-case accuracy](../glossary.md#worst-case-accuracy)** | Share of questions answered correctly in **every** variant | The strictest test, and the robustness version of pass^k |
| **Agreement rate** | Share of questions where the model gives the same answer across variants | Stability, whether the answer is right or wrong |
| **Attack success rate** | Successful attacks ÷ attempts | Resistance to deliberate misuse |

### Worked example: average vs. worst case

Five questions, each asked in **3 different phrasings** (✓ = correct):

| Question | Phrasing 1 | Phrasing 2 | Phrasing 3 | Right in all three? |
|----------|-----------|-----------|-----------|---------------------|
| Q1 | ✓ | ✓ | ✓ | Yes |
| Q2 | ✓ | ✓ | ✓ | Yes |
| Q3 | ✓ | ✓ | ✗ | No |
| Q4 | ✓ | ✗ | ✓ | No |
| Q5 | ✗ | ✓ | ✓ | No |

- **Average accuracy across phrasings:** 12 of 15 = **80%**.
- **Worst-case accuracy:** 2 of 5 questions = **40%**.

Averaged over phrasings, this model looks fine. But for three of the five questions, how you word the question decides whether it gets the right answer. Worst-case accuracy shows that, and the average hides it.

---

## Is the *evaluation* robust?

Robustness also applies to the test itself: does the score survive reasonable changes to how the evaluation is run? Our metric cards check this under *Label and metric flaws*:

| Change to the evaluation | Example from our cards |
|--------------------------|------------------------|
| How the answer is read from the model's output | The same model scored **63.7%** or **48.8%** on MMLU ([MMLU card](../benchmarks/knowledge-reasoning/mmlu.md#how-its-scored)) |
| The agent setup (scaffold) | o3 scored **54%** or **20%** on τ-bench airline ([τ-bench card](../benchmarks/agents/tau-bench.md#how-its-scored)) |
| Reasoning setting | GPT-5.6 Luna scored **63.6%** or **91.6%** on GPQA Diamond ([GPQA card](../benchmarks/knowledge-reasoning/gpqa-diamond.md#how-its-scored)) |
| Tools allowed or not | Self-reported HLE scores run up to about 18 points above the official no-tools evaluation ([HLE card](../benchmarks/knowledge-reasoning/hle.md#how-its-scored)) |

If a small change to the evaluation moves the score more than the gap between two models, the ranking of those models isn't robust.

## Quick reference

| You want to know… | Look for | A warning sign |
|-------------------|----------|----------------|
| Does wording matter? | Spread across prompts; worst-case accuracy | One fixed prompt; no range reported |
| Did it memorize the test? | Scores on fresh variants of the questions | Big drop on new versions |
| Can it ignore noise? | Scores with distractors or long inputs | Tested only on short, clean inputs |
| Will it work on new kinds of data? | Out-of-distribution and worst-group accuracy | Only tested on data like the training data |
| Can it be tricked? | Attack success rate under strong attacks | Only weak or few attacks tried |
| Will an agent cope with things going wrong? | Success with injected faults | Only tested in a perfect environment |

## How our metric cards cover robustness

- **Covered:** wording and format (MMLU), changed values and distractors (GSM8K), and evaluation robustness on every card.
- **Partly covered:** environment faults (τ-bench card, via HAL's dashboard).
- **Not yet covered:** distribution shift and adversarial attacks. A card for a red-teaming or jailbreak benchmark would fill the second gap.

## Sources

1. Wang, Y. et al. (2024). *MMLU-Pro: A More Robust and Challenging Multi-Task Language Understanding Benchmark.* https://arxiv.org/abs/2406.01574
2. Alzahrani, N. et al. (2024). *When Benchmarks are Targets: Revealing the Sensitivity of Large Language Model Leaderboards.* ACL 2024. https://arxiv.org/abs/2402.01781
3. Sclar, M., Choi, Y., Tsvetkov, Y. & Suhr, A. (2023). *Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design* (FormatSpread). ICLR 2024. https://arxiv.org/abs/2310.11324
4. Mirzadeh, I. et al. (2024). *GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models.* https://arxiv.org/abs/2410.05229
5. Zhang, H. et al. (2024). *A Careful Examination of Large Language Model Performance on Grade School Arithmetic* (GSM1k). https://arxiv.org/abs/2405.00332
6. Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL. https://arxiv.org/abs/2307.03172
7. Taori, R. et al. (2020). *Measuring Robustness to Natural Distribution Shifts in Image Classification.* https://arxiv.org/abs/2007.00644
8. Mazeika, M. et al. (2024). *HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal.* https://arxiv.org/abs/2402.04249
9. Princeton HAL, *Reliability: τ-bench (airline, clean)* (fault, structural and prompt robustness scores; accessed 2026-11-15). https://hal.cs.princeton.edu/reliability/benchmark/taubench_airline
