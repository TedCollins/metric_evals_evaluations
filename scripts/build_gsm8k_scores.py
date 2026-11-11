"""Build data/gsm8k/scores.csv from Primary, Epoch, HELM and Unverified sources.

Epoch's copies of HELM (Classic) rows are dropped; HELM rows come directly
from HELM Lite's GSM8K leaderboard (5-shot worked examples, 1,000 of the
1,319 test problems, exact match on the final number).

Usage:  python3 scripts/build_gsm8k_scores.py
"""

from sources import drop_duplicates_of, load_curated, load_epoch, load_helm, write_scores

METRIC = "gsm8k"


def main() -> None:
    primary = load_curated(METRIC, "primary")
    epoch = load_epoch("gsm8k_external.csv", exclude_link_substrings=("crfm.stanford.edu/helm",))
    helm = load_helm("lite", "v1.13.0", "gsm",
                     "5-shot worked examples; 1,000 of 1,319 test problems; final-number exact match",
                     "https://crfm.stanford.edu/helm/lite/latest/")
    write_scores(METRIC, {
        "Primary": primary,
        "Epoch": drop_duplicates_of(epoch, primary),
        "HELM": helm,
        "Unverified": load_curated(METRIC, "unverified"),
    })


if __name__ == "__main__":
    main()
