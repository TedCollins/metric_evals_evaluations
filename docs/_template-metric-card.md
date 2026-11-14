<!-- Metric card template. Copy to docs/benchmarks/<area>/<metric>.md.
     Like a model card, but for a benchmark or metric: what it tests, how far to trust it, and how its scores have moved.
     For a scoring rule rather than a benchmark (e.g. pass^k), put it in docs/metrics/, use "What it claims to measure",
     replace Example items with a worked example, and replace the history chart with evidence tables. See docs/metrics/pass-k.md. -->

# <Benchmark name>

_Last updated: YYYY-MM-DD · Area: <e.g. Knowledge & reasoning>_

> **In one sentence:** <What this benchmark is, in plain words.>

| | |
|---|---|
| **Released** | <Year, authors / organization> |
| **Size** | <Number of questions / tasks> |
| **Format** | <e.g. 4-option multiple choice> |
| **Metric** | <e.g. accuracy> |
| **Random guessing** | <score> |
| **Human baseline** | <score, and who the humans were> |
| **Top score (as of <date>)** | <best verified score, model> [ref]; <best unverified score, model> [ref] |
| **Status** | <Active / Near saturation / Saturated> |

## What it claims to test

<The skill the authors set out to measure, and why they cared. Use their framing, cited.>

## What it actually tests

<What a model really needs in order to score well. Where does this differ from the claim?>

## Example items

<2–3 real items with the correct answers. Note where each one came from (split, subject).>

## How it's scored

<The metric, the prompt setup (zero-shot / few-shot / chain-of-thought), and how answers are extracted.
Explain what the score means in plain terms.>

## History and scores

![<Alt text: what the chart shows, and its main takeaway in one or two sentences.>](../../img/<metric>-history-light.svg)

_Dark-theme version: [<metric>-history-dark.svg](../../img/<metric>-history-dark.svg)_

**How to read this chart.** <Use the standard wording: one point per reported score, color = kind of source (Primary / Independent / Compiled), hollow gray = unverified, step line = best score so far. Then name which organizations fill each role for this metric.>

What stands out:
- <2–4 bullets, each tied to something visible in the chart.>

Data: [`data/<metric>/scores.csv`](../../../data/<metric>/scores.csv). Rebuild with `python3 scripts/build_<metric>_scores.py`, then `python3 scripts/metric_history.py <metric>`.

| When | What happened |
|------|---------------|
| <date> | <milestone, cited> |

<details>
<summary>Standard chart: data and settings</summary>

Every metric card uses the same chart, made by `scripts/metric_history.py` from two files:

**`data/<metric>/scores.csv`**: one row per reported score.

| Column | Meaning |
|--------|---------|
| `model` | Model name as the source gives it |
| `date` | YYYY-MM-DD |
| `date_basis` | `release` (model release date), `evaluated` (release unknown; first independent evaluation date) or `reported` (release unknown; earliest date an aggregator listed the score) |
| `score` | 0–100 |
| `setup_detail` | How the test was run (shots, chain-of-thought…). Recorded here, not shown on the chart |
| `source` | The *kind* of number: `Primary` (checked by us) · `Independent` (one organization re-ran every model the same way, e.g. Stanford HELM or Epoch AI's own runs) · `Compiled` (reported scores collected in one place, e.g. Epoch AI's external runs) · `Unverified` (aggregators, not checked). Who published it goes in `original_source`. |
| `original_source`, `source_url` | Where the number comes from |
| `notes` | Anything unusual: outliers, conflicting reports |

**`data/<metric>/chart.json`**: `title`, `y_label`, `y_range`, `x_start`, `as_of`, an optional `ceiling` band, `source_labels` (optional legend text per role, naming the organization), `reference_lines` (random guessing, human baselines), `pairs` (one model with two conflicting scores), and up to ~4 `annotations`. See `data/mmlu/chart.json` for an example.

</details>

## Known issues

Each issue is tagged by evidence level: **[documented]** (published analysis) · **[reported]** (credible informal source) · **[suspected]** (our own reasoning).

### Contamination and saturation
### Construct validity
### Label and metric flaws
### Real-world gap

<Write "No known issues" under a heading when that is the case.>

## How to read a score

<Practical bullets: what a reported number does and doesn't tell you.>

## Related benchmarks

<Variants, successors, alternatives.>

## Sources

1. <Original paper>
2. <Dataset link>
3. <Critiques>
