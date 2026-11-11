"""Build data/hle/scores.csv from Primary, Independent and Unverified sources.

Independent = the official HLE evaluation run by its creators (CAIS and
Scale AI: no tools, same prompt and o3-mini judge for every model), as
mirrored in Epoch AI's "external runs" file with standard and calibration
errors. There is no Compiled source: most self-reported HLE scores don't say
whether tools (web search, code) were used, so they are kept as Unverified.

Usage:  python3 scripts/build_hle_scores.py
"""

from sources import drop_duplicates_of, load_curated, load_epoch, write_scores

METRIC = "hle"


def main() -> None:
    primary = load_curated(METRIC, "primary")
    official = load_epoch(
        "hle_external.csv", score_col="Accuracy", role="Independent",
        original_source="CAIS / Scale AI official HLE evaluation (via Epoch AI)",
        source_url="https://lastexam.ai/", stderr_col="Accuracy Standard Error",
        extra_note_cols=("Calibration Error",),
        setup_detail="no tools; official HLE prompt and judge")
    write_scores(METRIC, {
        "Primary": primary,
        "Independent": drop_duplicates_of(official, primary),
        "Unverified": load_curated(METRIC, "unverified"),
    })


if __name__ == "__main__":
    main()
