"""Build data/mmlu/scores.csv (standard metric-history schema) from four sources.

Sources (column `source`):
  Primary    - hand-checked scores from original papers and model reports
               (data/mmlu/primary.csv, curated by hand).
  Epoch      - Epoch AI Benchmarking Hub, "external runs": scores reported in
               papers and announcements, collected by Epoch (CC-BY).
               Epoch's copies of HELM *Lite* rows are dropped: HELM Lite uses
               only 5 of the 57 MMLU subjects, so it isn't comparable.
  HELM       - Stanford CRFM HELM MMLU leaderboard: every model run by
               Stanford with the same setup (5-shot, all 57 subjects).
  Unverified - scores from secondary aggregators that we have not checked
               against an original source (data/mmlu/unverified.csv).

Usage:  python3 scripts/build_mmlu_scores.py
"""

import csv
import io
import json
import sys
import urllib.request
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from metric_history import SCHEMA  # noqa: E402

DIR = ROOT / "data" / "mmlu"

EPOCH_ZIP_URL = "https://epoch.ai/data/benchmark_data.zip"
HELM_RELEASE = "v1.13.0"
HELM_BASE = (
    "https://storage.googleapis.com/crfm-helm-public/mmlu/benchmark_output/"
    f"releases/{HELM_RELEASE}"
)
HELM_PAGE = "https://crfm.stanford.edu/helm/mmlu/latest/"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "metric-history-script"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def load_curated(path: Path, source: str) -> list[dict]:
    with open(path, newline="") as f:
        return [{
            "model": r["model"],
            "date": r["date"],
            "date_basis": r["date_basis"],
            "score": float(r["score"]),
            "setup_detail": r["setup_detail"],
            "source": source,
            "original_source": r["source_title"],
            "source_url": r["source_url"],
            "notes": r["notes"],
        } for r in csv.DictReader(f)]


def epoch_setup(shots: str, notes: str) -> str:
    if "cot" in notes.lower():
        return f"{shots}-shot chain-of-thought" if shots else "chain-of-thought"
    return f"{shots}-shot" if shots else "not reported"


def load_epoch() -> list[dict]:
    z = zipfile.ZipFile(io.BytesIO(fetch(EPOCH_ZIP_URL)))
    text = z.read("mmlu_external.csv").decode("utf-8")
    rows = []
    for r in csv.DictReader(io.StringIO(text)):
        if "crfm.stanford.edu/helm/lite" in r["Source link"]:
            continue  # HELM Lite = 5-subject subset; not comparable
        if not r["Release date"] or not r["EM"]:
            continue
        rows.append({
            "model": r["Name"] or r["Model version"],
            "date": r["Release date"],
            "date_basis": "release",
            "score": round(float(r["EM"]) * 100, 2),
            "setup_detail": epoch_setup(r["Shots"].strip(), r["Notes"]),
            "source": "Epoch",
            "original_source": r["Source"].strip(),
            "source_url": r["Source link"],
            "notes": "",
        })
    return rows


def load_helm() -> list[dict]:
    schema = json.loads(fetch(f"{HELM_BASE}/schema.json"))
    dates = {m["display_name"]: m.get("release_date") for m in schema["models"]}
    table = json.loads(fetch(f"{HELM_BASE}/groups/mmlu.json"))[0]  # "All Subjects"
    em = [h["value"] for h in table["header"]].index("EM")
    rows = []
    for row in table["rows"]:
        name, score = row[0]["value"], row[em].get("value")
        if not dates.get(name) or score is None:
            continue
        rows.append({
            "model": name,
            "date": dates[name],
            "date_basis": "release",
            "score": round(score * 100, 2),
            "setup_detail": "5-shot, HELM standard prompt",
            "source": "HELM",
            "original_source": f"Stanford CRFM HELM MMLU {HELM_RELEASE}",
            "source_url": HELM_PAGE,
            "notes": "",
        })
    return rows


def is_duplicate(e: dict, primary: list[dict]) -> bool:
    """An Epoch row that repeats a hand-checked primary score."""
    ed = date.fromisoformat(e["date"])
    return any(
        abs(e["score"] - p["score"]) < 0.15
        and abs((ed - date.fromisoformat(p["date"])).days) <= 30
        for p in primary
    )


def main() -> None:
    primary = load_curated(DIR / "primary.csv", "Primary")
    unverified = load_curated(DIR / "unverified.csv", "Unverified")
    epoch = [e for e in load_epoch() if not is_duplicate(e, primary)]
    helm = load_helm()
    rows = sorted(primary + epoch + helm + unverified, key=lambda r: (r["date"], r["source"]))
    out = DIR / "scores.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows to {out.relative_to(ROOT)} (Primary {len(primary)}, "
          f"Epoch {len(epoch)}, HELM {len(helm)}, Unverified {len(unverified)})")


if __name__ == "__main__":
    main()
