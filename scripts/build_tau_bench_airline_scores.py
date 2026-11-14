"""Build data/tau_bench_airline/scores.csv (τ-bench airline, original 50 tasks, pass^1).

Primary     = the original τ-bench paper's Table 2 (gpt-4-0613 user simulator).
Independent = Princeton HAL's runs with the TAU-bench Tool Calling scaffold
              (hand-entered: HAL has no download). HAL Generalist Agent rows
              are excluded (HAL calls them a lower bound), and so are HAL's
              results on the cleaned 26-task subset (a different task set).
Unverified  = self-reported scores listed on llm-stats.

Usage:  python3 scripts/build_tau_bench_airline_scores.py
"""

from sources import load_curated, write_scores

METRIC = "tau_bench_airline"


def main() -> None:
    write_scores(METRIC, {
        "Primary": load_curated(METRIC, "primary"),
        "Independent": load_curated(METRIC, "independent"),
        "Unverified": load_curated(METRIC, "unverified"),
    })


if __name__ == "__main__":
    main()
