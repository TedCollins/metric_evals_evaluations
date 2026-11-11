# Requirements — metric_evals_evaluations

_Draft v0.2 · 2026-11-11_

## 1. Purpose

Write a **plain-language overview of AI evaluations** that:

1. explains clearly and in depth **what each benchmark actually tests**: the task, the data, how it is scored, and what a score means;
2. **points out the problems** with each benchmark or metric, so readers know how far to trust a headline number.

The goal is to learn the field and then share it. The output is Markdown docs in this repo.

## 2. Audience

**General readers with no ML background.** So the docs must:
- define every technical term the first time it appears, and link to a glossary;
- show real example questions instead of describing them abstractly;
- explain *why it matters* before *how it works*;
- avoid assuming the reader knows math notation or the ML literature.

## 3. Scope

### First phase: knowledge and reasoning benchmarks
Candidate list, to be trimmed to the first batch:

| Benchmark | What it claims to measure |
|-----------|---------------------------|
| MMLU / MMLU-Pro | Broad academic knowledge across 57 subjects |
| GPQA (Diamond) | Graduate-level science questions designed so web search doesn't help |
| ARC (AI2 Reasoning Challenge) | Grade-school science reasoning |
| ARC-AGI | Abstract pattern puzzles meant to test general intelligence (unrelated to the line above, despite the shared name) |
| HellaSwag | Commonsense: choosing the sensible ending to a story |
| WinoGrande | Commonsense: figuring out what a pronoun refers to |
| BIG-Bench / BIG-Bench Hard | A large mix of tasks chosen to be hard for models |
| GSM8K | Grade-school math word problems |
| MATH | Competition-level math |
| Humanity's Last Exam | Expert-written questions at the edge of human knowledge |

### Later phases (out of scope for now)
- Coding and agent benchmarks (HumanEval, SWE-bench, tool-use suites)
- Chat quality and human preference (Chatbot Arena, MT-Bench, LLM-as-judge)
- Safety and truthfulness (TruthfulQA, refusal and jailbreak suites)

## 4. Benchmark page: required sections

Every benchmark gets its own page with these sections, in this order:

| Section | What it must contain |
|---------|----------------------|
| **In one sentence** | What the benchmark is, in plain words. |
| **What it claims to test** | The skill the authors set out to measure, and why they cared. |
| **What it actually tests** | The construct as it really is: the task format, its sources, and what a model needs in order to score well. |
| **Example items** | Two or three real questions, with the correct answers. |
| **How it's scored** | The metric (e.g. accuracy, pass@k), the setup (few-shot, chain-of-thought), and what random-guess and human-expert scores look like. |
| **History and scores** | When and by whom it was released, how top scores have moved over time, and whether it is saturated. |
| **Known issues** | See §5. Every claim must cite a source. |
| **How to read a score** | Practical advice: what a reported number does and doesn't tell you. |
| **Sources** | The original paper, critiques, and the dataset link. |

## 5. Issues checklist

Each page must check the benchmark against all four categories, and say "no known issues" explicitly where that applies:

| Category | Questions to answer |
|----------|---------------------|
| **Contamination and saturation** | Has the test data leaked into training sets? Are top models at or near the ceiling? Are there signs of overfitting, such as a drop on rephrased variants? |
| **Construct validity** | Does it measure what its name says? Can it be solved through shortcuts, such as answer-option artifacts or pattern matching? |
| **Label and metric flaws** | Are there wrong or ambiguous answers in the key, and at what estimated error rate? Is the scoring brittle, for example sensitive to prompt format or answer parsing? |
| **Real-world gap** | Do gains on this benchmark track usefulness in real tasks? Who relies on it, and for what decisions? |

Sort each issue into one of three evidence levels: **documented** (published analysis), **reported** (credible informal sources), or **suspected** (our own reasoning, labeled as such).

## 6. Cross-cutting docs

- **`docs/overview.md`**: the entry point. Covers what an evaluation is, why benchmarks exist, how to read a leaderboard, and a comparison table of every benchmark covered.
- **`docs/concepts/`**: short explainers on ideas that recur across benchmarks: contamination, saturation, construct validity, few-shot prompting, multiple-choice scoring, and pass@k.
- **`docs/glossary.md`**: every term defined in one place.

## 7. Quality bar

- **Q1** A general reader can explain, after one read, what the benchmark tests and one reason to be skeptical of it.
- **Q2** Every factual claim about scores, errors or contamination links to a source.
- **Q3** Pages use the same section structure (§4), so readers can compare benchmarks.
- **Q4** Pages are dated, and scores carry an "as of" date, because the field moves quickly.

## 8. First milestone: done when

- [ ] `docs/overview.md` is drafted.
- [ ] 3–5 benchmark pages are complete. Suggested starters, because they are widely cited and have well-documented issues: **MMLU, GSM8K, HellaSwag, GPQA**.
- [ ] The concept explainers needed by those pages are written.
- [ ] A glossary covers every term used.

## 9. Repo layout

```
docs/
  overview.md
  benchmarks/
    knowledge-reasoning/
      mmlu.md
      gsm8k.md
      ...
  concepts/
    contamination.md
    saturation.md
    ...
  glossary.md
  img/<metric>-history-{light,dark}.svg   # standard charts (generated)
  _template-metric-card.md                # each benchmark page is a "metric card"
data/
  <metric>/
    scores.csv      # standard schema: one row per reported score, with source
    chart.json      # per-metric chart settings (reference lines, ceiling)
    primary.csv     # hand-checked scores
    unverified.csv  # aggregator scores not yet checked
scripts/
  build_<metric>_scores.py   # merges that metric's sources into scores.csv
  metric_history.py          # standard chart, shared by every metric card
REQUIREMENTS.md
```

## 10. Open questions

- ~~Should model scores be kept in a small data file (CSV) so tables stay consistent across pages?~~ Yes: `data/<metric>/scores.csv`, using the standard schema in the metric card template.
- Which other standard charts should every metric card have, e.g. verified vs. unverified spread, or a score distribution per year?
- Should the earlier idea of a **criteria taxonomy** come back later as a capstone, i.e. "what makes a good benchmark", drawn from the issues found?
- How should the docs handle benchmarks with several versions (MMLU vs. MMLU-Pro vs. MMLU-Redux): one page or several?
