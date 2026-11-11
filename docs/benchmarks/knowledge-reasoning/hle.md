# Humanity's Last Exam (HLE)

_Last updated: 2026-11-11 · Area: Knowledge & reasoning_

> **In one sentence:** Humanity's Last Exam is 2,500 expert-written questions across more than a hundred subjects, each chosen because the best AI models of late 2024 got it wrong. It was built to be the hard test that replaces saturated benchmarks like MMLU, and as of November 2026 it is **not yet saturated**: the best independently measured score is 54.8%.

| | |
|---|---|
| **Released** | January 2025, Phan et al., Center for AI Safety (CAIS) and Scale AI, with about 1,000 expert contributors [1][2] |
| **Size** | 2,500 public questions, plus a private held-out set used to detect overfitting [1][2] |
| **Format** | About 76% short exact answers and 24% multiple choice. About 14% include an image. [1] |
| **Metric** | Accuracy (% correct, graded by a judge model). The official evaluation also reports **calibration error**. [1][2] |
| **Random guessing** | ~4.8% (Epoch AI's estimate, since most questions aren't multiple choice) [5] |
| **Human baseline** | None published for the whole test. Each question was written by a subject expert. |
| **Top scores (as of 2026-11-11)** | 54.8% on the official no-tools evaluation (GPT-6 Astra, Sep 2026) [5]; 73.2% self-reported, tool use not stated (Claude Fable 5.2, Nov 2026) [6] |
| **Status** | **Not saturated**, but a large share of the remaining questions may be unanswerable as written (see below). |

---

## What it claims to test

**The frontier of expert human knowledge.** The authors argue that popular benchmarks like MMLU had become too easy to measure progress, so they built a test from questions at the edge of what specialists know. Questions came from nearly 1,000 contributors (mostly professors, researchers and people with graduate degrees) at more than 500 institutions in 50 countries. Each question has a single, verifiable answer that can't be found quickly online. [1][2]

**How questions were chosen** [1]:
1. **Tested against AI first.** Every submitted question was tried on several frontier models. Exact-answer questions were kept only if *all* the models failed. Multiple-choice questions were kept if all but one failed. Over 70,000 attempts produced about 13,000 candidate questions.
2. **Expert review in two rounds.** First, 1–3 reviewers refined each question. Then organizers and reviewers approved the final set.
3. **Prizes.** A $500,000 pool ($5,000 for each of the top 50 questions and $500 for the next 500) encouraged hard, high-quality submissions.

## What it actually tests

- **Highly specialized knowledge.** Answers often depend on knowing an obscure fact, a niche technique or a recent research result.
- **Questions that *2024's* models got wrong.** Because questions were filtered against specific models, the set is skewed toward what those models happened to be bad at, which isn't necessarily what's hardest in general (see [Construct validity](#construct-validity)).
- **Producing an exact answer.** Most questions need a short final answer, such as a number, a name or a formula. That rules out guessing among options, but makes the grading rules matter.
- **Knowing when you don't know.** Models are also asked how confident they are, which gives a [calibration](../../glossary.md#calibration) score.

Math is the most heavily represented subject [1]. Other questions span the humanities, natural sciences, engineering and computer science.

## Example items

> ⚠️ **We don't reproduce real HLE questions.** Downloading the dataset requires accepting conditions, and the creators ask people not to share or redistribute it. Its files carry a [canary string](../../glossary.md#canary-string) so that companies training AI models can filter them out. [3]

**An illustrative exact-answer question we wrote ourselves.** It is far easier than a real HLE question.

> Up to isomorphism, how many groups of order 16 are there? Give a single integer.
>
> *Answer:* **14**

This shows the format: a short, checkable answer and no options to choose from. Real HLE questions are much harder and often combine several obscure steps. The paper says the questions span mathematics, the humanities and the natural sciences. [1]

## How it's scored

1. The model answers each question and states its confidence (0–100%).
2. A **[judge model](../../glossary.md#judge-model)** (o3-mini on the official leaderboard) decides whether the answer matches the key [2]. That's needed because a correct answer can be phrased in many ways.
3. **Accuracy** = % judged correct. **Calibration error** (root-mean-square) measures how far stated confidence is from actual accuracy. Lower is better, and 0% means perfectly calibrated.

Things that change the number:
- **[Tool use](../../glossary.md#tool-use).** The official evaluation allows **no tools**. Many labs report HLE scores with web search or code execution. A score that doesn't say which isn't comparable.
- **Text-only versus full set.** Models that can't read images are scored on the text-only questions [1].
- **Reasoning settings and judge choice.** Like GPQA, the same model can score very differently at different [reasoning effort](../../glossary.md#reasoning-effort) levels, and a different judge model can grade borderline answers differently.

## History and scores

![Scatter chart of Humanity's Last Exam scores by model release date, mid-2024 to late 2026. Models tested in the January 2025 paper score between 2.7% (GPT-4o) and 13.4% (o3-mini). Official no-tools scores by the HLE team then rise to 54.8% (GPT-6 Astra, September 2026). Self-reported scores, shown as hollow rings, mostly sit 5–20 points higher and reach 73.2% (Claude Fable 5.2, November 2026), just under a shaded band from 75% marking questions estimated to be impossible as written. Colors show the data source.](../../img/hle-history-light.svg)

_Dark-theme version: [hle-history-dark.svg](../../img/hle-history-dark.svg)_

**How to read this chart.** Each point is one reported score. **Color shows what kind of source the number came from**:
- **Primary** (blue): the eight models tested in the original paper, all without tools, checked by us against the paper [1].
- **Independent: CAIS / Scale AI** (green): the official HLE evaluation, run by the benchmark's creators with the same no-tools prompt and judge for every model [2]. We take these from Epoch AI's copy of the official results, which includes a standard error and calibration error for each [5].
- **Unverified** (hollow gray): self-reported scores listed on llm-stats, which doesn't say whether tools were used [6]. They are dated by Epoch AI's release date for the same model.

There is no "Compiled" source here. Self-reported HLE scores rarely say whether tools were used, so we keep them as Unverified rather than treating them as comparable.

The gray step line traces the best score reported so far, including self-reports.

What stands out:
- **It's still climbing.** Official scores rose from single digits in January 2025 to 54.8% by September 2026, with no sign yet of leveling off.
- **Self-reports run well above official scores.** For the same model: Claude Opus 4.7 is **54.7%** self-reported vs **36.2%** official; Claude Opus 4.6 is 53.1% vs 34.4%; Muse Spark is 58.4% vs 40.6%; Claude Fable 5.1 is 65.0% vs 46.5%. Others are closer, such as Gemini 3.1 Pro at 51.4% vs 46.4% and GPT-5.4 at 39.8% vs 36.2%. [5][6] Tool use is the most likely reason. **[suspected]**
- **The best self-report is nearing the estimated ceiling.** Claude Fable 5.2's self-reported 73.2% is just under the ~75% line, above which Epoch's review suggests questions are impossible as written (see [Label and metric flaws](#label-and-metric-flaws)).

Data: [`data/hle/scores.csv`](../../../data/hle/scores.csv), with one row per point, a source link on each row, and the calibration error in `notes` where available. Rebuild with `python3 scripts/build_hle_scores.py`, then `python3 scripts/metric_history.py hle`.

### Calibration: do models know when they don't know?

The official evaluation also measures calibration error. This is a second dimension that accuracy alone misses. Lower is better.

| Model | Released | Accuracy | Calibration error |
|-------|----------|----------|-------------------|
| GPT-4o | Nov 2024 | 2.7% | 89% [1] |
| o1 | Dec 2024 | 8.0% | 83% [1] |
| Gemini 3 Pro (preview) | Nov 2025 | 37.5% | 57% [5] |
| Gemini 3.1 Pro (preview, high) | Feb 2026 | 46.4% | 51% [5] |
| GPT-6 Astra | Sep 2026 | 54.8% | 39% [5] |
| Claude Fable 5.1 (xhigh) | Sep 2026 | 46.5% | **20%** [5] |

Early models were confidently wrong on almost everything. Newer models are far better calibrated, but calibration and accuracy don't move together: the most accurate model isn't the best calibrated.

| When | What happened |
|------|---------------|
| Jan 2025 | Released by CAIS and Scale AI. The best model in the paper, o3-mini (high), scores **13.4%** (text-only). GPT-4o scores **2.7%**. [1] |
| Apr 2025 | Dataset update (the official leaderboard uses the April 3, 2025 version). [2] |
| Jul 2025 | FutureHouse audit: about **29%** of chemistry and biology answers conflict with published research. [4] |
| Nov 2025 | Gemini 3 Pro reaches **37.5%** on the official evaluation. [5] |
| Feb 2026 | Gemini 3.1 Pro reaches **46.4%**. [5] |
| Aug 2026 | Epoch AI's benchmark review rates HLE **"Flawed"**: errors in 22 of 48 sampled questions. [7] |
| Sep 2026 | GPT-6 Astra reaches **54.8%** on the official evaluation, the best so far. [5] |
| Nov 2026 | Claude Fable 5.2 self-reports **73.2%** (tool use not stated). [6] |

## Known issues

Evidence levels: **[documented]** published analysis · **[reported]** credible informal source · **[suspected]** our own reasoning.

### Contamination and saturation

- **[documented] Strong steps against contamination.** Downloading the dataset requires accepting conditions, the creators ask people not to share it, the files carry a canary string, and a **private held-out set** lets the creators check whether models do suspiciously better on public questions than on hidden ones. [1][2][3] That is the strongest protection of any benchmark in this series.
- **[documented] Not saturated, as of November 2026.** The best official score is 54.8% [5].

### Construct validity

- **[documented] Questions were filtered to stump specific models.** A question was kept only if the frontier models of late 2024 failed it [1]. FutureHouse argues this pushed writers toward convoluted "gotcha" questions that hinge on edge-case readings [4].
- **[suspected] That filter also distorts progress.** Questions were selected *because* particular 2024 models got them wrong, so those models' scores are pushed down by design. Later models weren't part of the filter, so part of their apparent jump is a selection effect, not only real progress.
- **[suspected] "Last exam" overclaims.** A test of obscure, single-answer questions measures recall and narrow problem-solving at the expert level. It doesn't measure open-ended research ability, and it won't be the "last" benchmark.

### Label and metric flaws

- **[documented] Many answer keys look wrong in chemistry and biology.** FutureHouse checked the 321 text-only chemistry and biology questions with an AI literature-search tool, then had experts review a sample. They estimate **29.3% ± 3.7%** have answers that directly conflict with published research. Reviewers had not been required to verify rationales that would take more than 5 minutes to check. [4]
- **[documented] The HLE team's own follow-up found fewer problems, but not none.** About **18%** of a chemistry and biology subset was judged problematic, and at least one of three expert reviewers disagreed on about 25% of items. [4]
- **[documented] Epoch AI rates HLE "Flawed".** In a sample of 48 questions (6 from each of 8 categories), **22 (46%)** had errors that would change accuracy, above Epoch's 20% threshold for "Flawed". **12** were impossible as written: missing assumptions, contradictory premises, more than one valid reading, or a key that doesn't match the question. **10** risked marking correct answers wrong, 5 of which also risked marking wrong answers right. Engineering was worst (5 of 6 flawed), and math best (1 of 6). [7] It's a small sample, and Epoch stopped once the threshold was passed.
- **[suspected] So the real ceiling is well below 100%.** If roughly a quarter of questions are impossible as written (12 of 48 in Epoch's sample), the highest meaningful score is around 75%. With a sample of 48, the uncertainty on that estimate is wide, roughly ±12 points.
- **[suspected] Judge-model grading adds noise.** An AI judge decides whether each answer matches the key, so borderline phrasings can be graded inconsistently, especially when the key itself is disputed.

### Real-world gap

- **[suspected] Self-reported scores aren't comparable.** Self-reports run 4–19 points above the official no-tools evaluation for the same model [5][6]. Tool use is the likely reason, but rarely stated. A headline "HLE score" without "with tools" or "no tools" can't be compared with anything.
- **[suspected] Obscure exam answers aren't the same as useful expertise.** A model that can name an obscure fact may still be unreliable on the everyday expert tasks people actually use it for.
- **[documented] Calibration is improving but uneven.** The best-calibrated model in our table (calibration error 20%) isn't the most accurate one [5]. For real use, knowing when a model is unsure matters as much as raw accuracy.

## How to read a score

- **Look for "no tools" or "with tools".** Only compare like with like. Official leaderboard scores are no-tools.
- **Prefer the official evaluation** over self-reports. The creators run every model the same way and publish calibration error.
- **Remember the ceiling.** Somewhere around 25% of questions may be impossible as written, so scores in the 70s are near the top of what's meaningful.
- **Treat small gaps as ties.** Standard errors on the official evaluation are around ±1–2 points for top models [5].
- **Check calibration too.** A model that is right 50% of the time but knows which half is more useful than one that is confidently wrong.

## Related benchmarks

- **GPQA Diamond** ([card](gpqa-diamond.md)): fewer, more carefully validated expert science questions, now near saturation.
- **MMLU** ([card](mmlu.md)): the broad knowledge benchmark HLE was built to replace.
- **FutureHouse's corrected chemistry and biology subset** [4]: a re-checked version of the questions they audited.

## Sources

1. Phan, L. et al. (2025). *Humanity's Last Exam.* arXiv:2501.14249 (v1 Jan 2025; v12 Oct 2026). https://arxiv.org/abs/2501.14249
2. Center for AI Safety & Scale AI, *Humanity's Last Exam*, official site and leaderboard (no tools; o3-mini judge; dataset version April 3, 2025). https://lastexam.ai/
3. HLE dataset card (MIT license, gated; includes canary string), Hugging Face. https://huggingface.co/datasets/cais/hle
4. FutureHouse (2025-07-23, updated 2025-09-16). *About 30% of Humanity's Last Exam chemistry/biology answers are likely wrong.* https://www.futurehouse.org/research/hle-exam
5. Epoch AI, Benchmarking Hub, HLE "external runs": the official HLE evaluation results with standard and calibration errors (CC-BY; downloaded 2026-11-11). https://epoch.ai/benchmarks/use-this-data
6. llm-stats, Humanity's Last Exam leaderboard (all 118 results self-reported; tool use not stated; accessed 2026-11-11). Not independently verified. https://llm-stats.com/benchmarks/humanity's-last-exam
7. Epoch AI (2026-08-11). *Humanity's Last Exam: Benchmark Review*, verdict "Flawed". https://epoch.ai/benchmarks/hle/review
