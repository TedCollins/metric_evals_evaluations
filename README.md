# Metric cards for AI benchmarks

**A plain-language reader's guide to AI benchmarks: what each one actually tests, and how far to trust the numbers people quote from it.**

When a lab announces "92% on GPQA" or "state of the art on Humanity's Last Exam", most readers can't tell what that means or whether it's comparable with anything else. This project writes one **metric card** per benchmark (a standard page, like a model card but for a benchmark) that answers those questions for readers without an ML background.

## Metric cards so far

| Benchmark | What it tests (in short) | Status | Best independent score | Effective ceiling* |
|-----------|--------------------------|--------|------------------------|--------------------|
| [MMLU](docs/benchmarks/knowledge-reasoning/mmlu.md) | Exam-style multiple choice across 57 subjects | Saturated | 87.3% (Stanford HELM, Oct 2024) | ~93.5% |
| [GSM8K](docs/benchmarks/knowledge-reasoning/gsm8k.md) | Grade-school math word problems | Saturated | 95.6% (Stanford HELM, Oct 2024) | ~96.6% |
| [GPQA Diamond](docs/benchmarks/knowledge-reasoning/gpqa-diamond.md) | PhD-level science questions you can't simply look up | Near saturation | 96.5% (Epoch AI, Oct 2026) | ~92% |
| [Humanity's Last Exam](docs/benchmarks/knowledge-reasoning/hle.md) | Expert questions chosen because 2024's AI models failed them | **Not saturated** | 54.8% (official evaluation, Sep 2026) | ~75% |
| [τ-bench](docs/benchmarks/agents/tau-bench.md) (airline) | AI agents doing customer service with tools and policies | Superseded | 56% (Princeton HAL, 2025) | n/a: only 26 of 50 tasks pass quality review |

\* The score above which, by our estimate, gains mostly reflect flawed questions or answer keys rather than real ability. Each card explains its estimate and how uncertain it is. Scores are as of November 2026.

**Metric cards for scoring rules** (not benchmarks):

| Metric | What it measures |
|--------|------------------|
| [pass^k](docs/metrics/pass-k.md) | The chance a system succeeds on **all** k attempts at a task, i.e. reliability rather than average success |

New to the topic? Start with the [glossary](docs/glossary.md) and the explainers on [reliability](docs/concepts/reliability.md), [contamination](docs/concepts/contamination.md) and [multiple-choice scoring](docs/concepts/multiple-choice-scoring.md).

## What makes this different

Good benchmark *data* already exists. [Epoch AI's Benchmarking Hub](https://epoch.ai/benchmarks) tracks scores for about 100 benchmarks and 400+ models, and [Stanford HELM](https://crfm.stanford.edu/helm/) runs models under consistent conditions. This project depends on both, and isn't trying to replace either. It adds the layer they don't aim to provide:

1. **Plain-language explanation for general readers.** Each card sets out what the benchmark *claims* to test next to what it *actually* tests, with example questions and no assumed ML background.
2. **Checking score claims.** Every chart puts the same models' scores from different kinds of source side by side, so the gaps are visible:
   - **Primary:** checked by us against the original paper or report.
   - **Independent:** one organization re-ran every model the same way.
   - **Compiled:** reported scores collected in one place.
   - **Unverified:** self-reported scores from aggregator sites.

   These comparisons surface things a single table hides. On Humanity's Last Exam, several self-reported scores run about 18 points above the official evaluation of the same model. One headline MMLU "90%" used a different method from the number it was compared against.
3. **One evidence-graded verdict per benchmark.** Each card pulls together the critiques we can find (from the benchmark authors, independent audits, academic papers and Epoch AI's own reviews) and tags every claim as **documented**, **reported** or **suspected**. Every card checks the same four areas: contamination and saturation, construct validity, label and metric flaws, and the real-world gap.
4. **An "effective ceiling" for every benchmark.** We estimate where scores stop meaning much, so readers know when a benchmark has run out of road.
5. **A reusable format.** The [metric card template](docs/_template-metric-card.md), the standard data format and the chart script are meant to be adopted for other benchmarks, including by benchmark authors themselves.

**What this project is not:** a leaderboard, a score database or an evaluation harness. For raw scores and per-question logs, go to the sources below.

## How it's built

Each card has a folder under `data/<metric>/`:
- `primary.csv`: hand-checked scores.
- `unverified.csv`: aggregator scores not yet checked.
- `chart.json`: chart settings for this metric.
- `scores.csv`: the merged data, built by script.

To rebuild a card's data and chart:

```bash
python3 scripts/build_hle_scores.py
```

```bash
python3 scripts/metric_history.py hle
```

The build scripts download current data from Epoch AI and Stanford HELM. The chart script writes light and dark SVGs to `docs/img/`. The requirements and design decisions are in [REQUIREMENTS.md](REQUIREMENTS.md).

## Data sources and credits

These cards stand on other people's data and research. Each card cites its sources inline; the main ones are:

| Source | Used for | Terms |
|--------|----------|-------|
| [Epoch AI Benchmarking Hub](https://epoch.ai/benchmarks) | Epoch's own runs (GPQA Diamond), collected reported scores (MMLU, GSM8K), and its copy of the official HLE results | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Cite as: Epoch AI, "Capabilities & benchmarking", https://epoch.ai/benchmarks |
| [Stanford CRFM HELM](https://crfm.stanford.edu/helm/) | Independent runs for MMLU (HELM MMLU v1.13.0) and GSM8K (HELM Lite v1.13.0) | Public leaderboard results, credited to Stanford CRFM |
| Official benchmark papers and leaderboards ([HLE](https://lastexam.ai/), [OpenAI simple-evals](https://github.com/openai/simple-evals) and others) | Primary scores, checked by hand | Cited per score in each card's data |
| [MMLU](https://huggingface.co/datasets/cais/mmlu) and [GSM8K](https://huggingface.co/datasets/openai/gsm8k) datasets | Example questions quoted in those cards | MIT license |
| [GPQA](https://huggingface.co/datasets/Idavidrein/gpqa) and [HLE](https://huggingface.co/datasets/cais/hle) datasets | Facts only: **no questions are reproduced** | Gated; users agree not to publish examples. Those cards use questions we wrote ourselves. |
| Aggregators: [llm-stats](https://llm-stats.com/), [BenchLM](https://benchlm.ai/) (including Kaggle Open Benchmarks results), [benchmarklist](https://benchmarklist.com/) | Recent self-reported scores | Shown as **Unverified**. Not checked by us. |

If you maintain one of these sources and see something misattributed or misrepresented, please open an issue.
