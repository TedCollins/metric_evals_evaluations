"""Standard metric-history chart for metric cards.

Every metric card uses the same chart, driven by two files in data/<metric>/:

  scores.csv  - one row per reported score, columns = SCHEMA below
  chart.json  - per-metric settings: title, axis, reference lines, ceiling
                band, and a few labeled points

Visual standard:
  * x = date, y = score. `date_basis` says what the date is: "release"
    (model release date), "evaluated" (release unknown; date of first
    independent evaluation) or "reported" (release unknown; earliest date
    an aggregator listed the score)
  * color = source of the number; Unverified = hollow gray ring
  * gray step line = best score reported so far (all sources)
  * dashed reference lines (random, human baselines...) and a shaded
    ceiling band where scores stop being meaningful
  * light and dark SVGs written to docs/img/<metric>-history-{light,dark}.svg

Usage:  python3 scripts/metric_history.py mmlu [--png DIR]
"""

import argparse
import csv
import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SCHEMA = [
    "model",            # model name as given by the source
    "date",             # YYYY-MM-DD
    "date_basis",       # "release" | "evaluated" | "reported" (see docstring)
    "score",            # 0-100
    "setup_detail",     # how the test was run (shots, chain-of-thought...)
    "source",           # Primary | Epoch | HELM | Unverified
    "original_source",  # paper / report / leaderboard title
    "source_url",
    "notes",
]

# Reference palette (dataviz skill): categorical slots 1-3 validated
# all-pairs for scatter in both modes. Unverified uses neutral ink, hollow.
THEMES = {
    "light": {
        "surface": "#fcfcfb", "text": "#0b0b0b", "text2": "#52514e",
        "muted": "#898781", "grid": "#e1e0d9", "axis": "#c3c2b7", "band": "#f1f0ec",
        "series": {"Primary": "#2a78d6", "Epoch": "#eb6834", "HELM": "#1baf7a",
                   "Unverified": "#52514e"},
    },
    "dark": {
        "surface": "#1a1a19", "text": "#f0efec", "text2": "#c3c2b7",
        "muted": "#898781", "grid": "#2c2c2a", "axis": "#383835", "band": "#242423",
        "series": {"Primary": "#3987e5", "Epoch": "#d95926", "HELM": "#199e70",
                   "Unverified": "#c3c2b7"},
    },
}

SOURCES = {  # draw order = list order (later on top)
    "Unverified": "Unverified: secondary aggregators, not checked by us",
    "Epoch": "Epoch AI: reported scores collected by Epoch",
    "HELM": "HELM: Stanford re-ran every model the same way",
    "Primary": "Primary: original paper / model report, checked by us",
}
LEGEND_ORDER = ["Primary", "HELM", "Epoch", "Unverified"]


def load_scores(metric: str) -> list[dict]:
    with open(ROOT / "data" / metric / "scores.csv", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["d"] = date.fromisoformat(r["date"])
        r["y"] = float(r["score"])
    return rows


def frontier(rows):
    pts, best = [], None
    for r in sorted(rows, key=lambda r: r["d"]):
        if best is None or r["y"] > best:
            best = r["y"]
            pts.append((r["d"], best))
    return pts


def plot(metric: str, rows: list[dict], cfg: dict, mode: str, out_paths: list[Path]) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    t = THEMES[mode]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "svg.fonttype": "path", "text.color": t["text"]})
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=110)
    fig.patch.set_facecolor(t["surface"])
    ax.set_facecolor(t["surface"])

    as_of = date.fromisoformat(cfg.get("as_of", date.today().isoformat()))
    x0 = date.fromisoformat(cfg["x_start"])
    x1 = as_of + timedelta(days=75)
    y0, y1 = cfg.get("y_range", [0, 100])

    if "ceiling" in cfg:
        c = cfg["ceiling"]
        ax.axhspan(c["value"], y1, color=t["band"], zorder=0, lw=0)
        ax.text(x0, y1 - (y1 - y0) * 0.014, "  " + c["label"], va="top", ha="left",
                fontsize=8.5, color=t["text2"], zorder=1)

    for ref in cfg.get("reference_lines", []):
        ax.axhline(ref["value"], color=t["muted"], lw=1, ls=(0, (4, 3)), zorder=1)
        left = ref.get("side", "right") == "left"
        ax.text(x0 if left else x1, ref["value"] + (y1 - y0) * 0.008,
                ("  " + ref["label"]) if left else (ref["label"] + "  "),
                ha="left" if left else "right", va="bottom", fontsize=8.5,
                color=t["text2"], zorder=1)

    fx, fy = zip(*frontier(rows))
    ax.step(list(fx) + [as_of], list(fy) + [fy[-1]], where="post",
            color=t["text2"], lw=1.25, alpha=0.6, zorder=2)

    for src in SOURCES:
        pts = [r for r in rows if r["source"] == src]
        if not pts:
            continue
        col = t["series"][src]
        hollow = src == "Unverified"
        ax.scatter([r["d"] for r in pts], [r["y"] for r in pts],
                   s=80 if src == "Primary" else 46, marker="o",
                   facecolors=t["surface"] if hollow else col,
                   edgecolors=col if hollow else t["surface"],
                   linewidths=1.3 if hollow else 1.2,
                   zorder={"Unverified": 3, "Epoch": 4, "HELM": 5, "Primary": 6}[src])

    def find(model, source):
        return [r for r in rows if r["model"] == model and r["source"] == source]

    for p in cfg.get("pairs", []):
        pts = sorted(find(p["model"], p["source"]), key=lambda r: r["y"])
        if len(pts) < 2:
            continue
        ax.plot([pts[0]["d"]] * 2, [pts[0]["y"], pts[-1]["y"]], color=t["text2"], lw=1, zorder=5)
        tx, ty = p["text_at"]
        ax.annotate(p["text"], xy=(pts[0]["d"], pts[0]["y"] - 1.5),
                    xytext=(date.fromisoformat(tx), ty), fontsize=8.5, color=t["text"],
                    ha="left", va="center",
                    arrowprops=dict(arrowstyle="-", color=t["muted"], lw=0.8))

    for a in cfg.get("annotations", []):
        for r in find(a["model"], a["source"]):
            ax.annotate(a["text"], (r["d"], r["y"]), xytext=a.get("offset", [8, 0]),
                        textcoords="offset points", fontsize=8.5, color=t["text"],
                        ha=a.get("ha", "left"), va="center", zorder=7)

    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_ylabel(cfg["y_label"], color=t["text2"])
    ax.set_xlabel("Model release date (or first-seen date if unknown)", color=t["text2"])
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.grid(axis="y", color=t["grid"], lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(t["axis"])
    ax.tick_params(colors=t["muted"], labelcolor=t["text2"], length=0)

    fig.suptitle(cfg["title"], x=0.06, y=0.975, ha="left", fontsize=13,
                 fontweight="bold", color=t["text"])
    fig.text(0.06, 0.925,
             "Each point is one reported score; color shows where the number came from.\n"
             "Gray step line = best score reported so far (all sources, any test setup).",
             ha="left", va="top", fontsize=9, color=t["text2"])

    handles = []
    for s in LEGEND_ORDER:
        col = t["series"][s]
        hollow = s == "Unverified"
        handles.append(Line2D([], [], ls="", marker="o", ms=8,
                              markerfacecolor=t["surface"] if hollow else col,
                              markeredgecolor=col if hollow else t["surface"],
                              markeredgewidth=1.3, label=SOURCES[s]))
    leg = fig.legend(handles=handles, title="Source", loc="lower left",
                     bbox_to_anchor=(0.055, 0.0), ncol=2, frameon=False, fontsize=8.5,
                     labelcolor=t["text"], title_fontsize=9, alignment="left",
                     columnspacing=2.0, handletextpad=0.4)
    leg.get_title().set_color(t["text2"])
    fig.text(0.98, 0.975, f"Data as of {as_of.isoformat()}\ndata/{metric}/scores.csv",
             ha="right", va="top", fontsize=8, color=t["muted"], linespacing=1.4)

    fig.subplots_adjust(left=0.07, right=0.98, top=0.85, bottom=0.22)
    for p in out_paths:
        fig.savefig(p, facecolor=t["surface"])
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("metric", help="folder name under data/, e.g. mmlu")
    ap.add_argument("--png", type=Path, help="also write PNG previews to this directory")
    args = ap.parse_args()

    cfg = json.loads((ROOT / "data" / args.metric / "chart.json").read_text())
    rows = load_scores(args.metric)
    out_dir = ROOT / "docs" / "img"
    out_dir.mkdir(parents=True, exist_ok=True)
    for mode in THEMES:
        paths = [out_dir / f"{args.metric}-history-{mode}.svg"]
        if args.png:
            args.png.mkdir(parents=True, exist_ok=True)
            paths.append(args.png / f"{args.metric}-history-{mode}.png")
        plot(args.metric, rows, cfg, mode, paths)
        print("Wrote", ", ".join(str(p) for p in paths))


if __name__ == "__main__":
    main()
