"""Build data/gpqa_diamond/scores.csv from Primary, Independent and Unverified sources.

Independent = Epoch AI's own GPQA Diamond runs (same harness for every model;
best setting per model kept). There is no Compiled source for GPQA Diamond:
Epoch publishes its own runs here instead of collecting reported scores.

Usage:  python3 scripts/build_gpqa_diamond_scores.py
"""

from sources import load_curated, load_epoch_runs, write_scores

METRIC = "gpqa_diamond"


def main() -> None:
    write_scores(METRIC, {
        "Primary": load_curated(METRIC, "primary"),
        "Independent": load_epoch_runs("gpqa_diamond.csv", "https://epoch.ai/benchmarks/gpqa-diamond"),
        "Unverified": load_curated(METRIC, "unverified"),
    })


if __name__ == "__main__":
    main()
