"""Build data/gpqa_diamond/scores.csv from Primary, Independent and Unverified sources.

Independent = Epoch AI's own GPQA Diamond runs (same harness for every model;
best setting per model kept). Epoch's "-fallback" model versions are
excluded: Epoch doesn't document what "fallback" means (it may route requests
to another model), and they score well above the same models' plain runs.
There is no Compiled source for GPQA Diamond:
Epoch publishes its own runs here instead of collecting reported scores.

Usage:  python3 scripts/build_gpqa_diamond_scores.py
"""

from sources import load_curated, load_epoch_runs, write_scores

METRIC = "gpqa_diamond"


def main() -> None:
    write_scores(METRIC, {
        "Primary": load_curated(METRIC, "primary"),
        "Independent": load_epoch_runs("gpqa_diamond.csv", "https://epoch.ai/benchmarks/gpqa-diamond",
                                       exclude_version_substrings=("-fallback",)),
        "Unverified": load_curated(METRIC, "unverified"),
    })


if __name__ == "__main__":
    main()
