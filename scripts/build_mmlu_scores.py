"""Build data/mmlu/scores.csv from Primary, Epoch, HELM and Unverified sources.

Epoch's copies of HELM *Lite* rows are dropped: HELM Lite uses only 5 of the
57 MMLU subjects, so it isn't comparable. HELM rows come from Stanford's full
MMLU leaderboard instead (5-shot, all 57 subjects).

Usage:  python3 scripts/build_mmlu_scores.py
"""

from sources import drop_duplicates_of, load_curated, load_epoch, load_helm, write_scores

METRIC = "mmlu"


def main() -> None:
    primary = load_curated(METRIC, "primary")
    epoch = load_epoch("mmlu_external.csv", exclude_link_substrings=("crfm.stanford.edu/helm/lite",))
    helm = load_helm("mmlu", "v1.13.0", "mmlu", "5-shot, HELM standard prompt",
                     "https://crfm.stanford.edu/helm/mmlu/latest/")
    write_scores(METRIC, {
        "Primary": primary,
        "Compiled": drop_duplicates_of(epoch, primary),
        "Independent": helm,
        "Unverified": load_curated(METRIC, "unverified"),
    })


if __name__ == "__main__":
    main()
