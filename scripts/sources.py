"""Shared loaders for metric-history data (one per source type).

Each loader returns rows in the standard schema (metric_history.SCHEMA).
A metric's build script (scripts/build_<metric>_scores.py) picks the loaders
and settings it needs, then calls write_scores().

Source types:
  Primary    - hand-checked scores (data/<metric>/primary.csv)
  Epoch      - Epoch AI Benchmarking Hub "external runs" (CC-BY)
  HELM       - Stanford CRFM HELM leaderboards (independent, same setup)
  Unverified - aggregator scores not checked by us (data/<metric>/unverified.csv)
"""

import csv
import io
import json
import urllib.request
import zipfile
from datetime import date
from functools import lru_cache
from pathlib import Path

from metric_history import ROOT, SCHEMA

EPOCH_ZIP_URL = "https://epoch.ai/data/benchmark_data.zip"
HELM_GCS = "https://storage.googleapis.com/crfm-helm-public"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "metric-history-script"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def load_curated(metric: str, kind: str) -> list[dict]:
    """kind = 'primary' or 'unverified'."""
    source = {"primary": "Primary", "unverified": "Unverified"}[kind]
    path = ROOT / "data" / metric / f"{kind}.csv"
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


@lru_cache(maxsize=1)
def _epoch_zip() -> zipfile.ZipFile:
    return zipfile.ZipFile(io.BytesIO(fetch(EPOCH_ZIP_URL)))


def _epoch_setup(shots: str, notes: str) -> str:
    if "cot" in notes.lower():
        return f"{shots}-shot chain-of-thought" if shots else "chain-of-thought"
    return f"{shots}-shot" if shots else "not reported"


def load_epoch(csv_name: str, exclude_link_substrings: tuple[str, ...] = ()) -> list[dict]:
    """Rows from one Epoch external-runs CSV (e.g. 'mmlu_external.csv').

    exclude_link_substrings drops rows whose source link contains any of the
    given strings - used to drop Epoch's copies of HELM runs, which we load
    directly (or exclude as not comparable).
    """
    text = _epoch_zip().read(csv_name).decode("utf-8")
    rows = []
    for r in csv.DictReader(io.StringIO(text)):
        if any(s in r["Source link"] for s in exclude_link_substrings):
            continue
        if not r["Release date"] or not r["EM"]:
            continue
        rows.append({
            "model": r["Name"] or r["Model version"],
            "date": r["Release date"],
            "date_basis": "release",
            "score": round(float(r["EM"]) * 100, 2),
            "setup_detail": _epoch_setup(r["Shots"].strip(), r["Notes"]),
            "source": "Epoch",
            "original_source": r["Source"].strip(),
            "source_url": r["Source link"],
            "notes": "",
        })
    return rows


def load_helm(project: str, release: str, group: str, setup_detail: str,
              page_url: str, metric_col: str = "EM") -> list[dict]:
    """Rows from a HELM leaderboard group table, dated by model release date.

    project: e.g. 'mmlu' or 'lite'; group: e.g. 'mmlu' or 'gsm'.
    """
    base = f"{HELM_GCS}/{project}/benchmark_output/releases/{release}"
    schema = json.loads(fetch(f"{base}/schema.json"))
    dates = {m["display_name"]: m.get("release_date") for m in schema["models"]}
    table = json.loads(fetch(f"{base}/groups/{group}.json"))[0]
    col = [h["value"] for h in table["header"]].index(metric_col)
    rows = []
    for row in table["rows"]:
        name, score = row[0]["value"], row[col].get("value")
        if not dates.get(name) or score is None:
            continue
        rows.append({
            "model": name,
            "date": dates[name],
            "date_basis": "release",
            "score": round(score * 100, 2),
            "setup_detail": setup_detail,
            "source": "HELM",
            "original_source": f"Stanford CRFM HELM ({project}) {release}",
            "source_url": page_url,
            "notes": "",
        })
    return rows


def drop_duplicates_of(rows: list[dict], primary: list[dict]) -> list[dict]:
    """Remove rows that repeat a hand-checked primary score (same score, ±30 days)."""
    def dup(e):
        ed = date.fromisoformat(e["date"])
        return any(abs(e["score"] - p["score"]) < 0.15
                   and abs((ed - date.fromisoformat(p["date"])).days) <= 30
                   for p in primary)
    return [e for e in rows if not dup(e)]


def write_scores(metric: str, groups: dict[str, list[dict]]) -> Path:
    rows = sorted((r for g in groups.values() for r in g),
                  key=lambda r: (r["date"], r["source"]))
    out = ROOT / "data" / metric / "scores.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA)
        w.writeheader()
        w.writerows(rows)
    counts = ", ".join(f"{k} {len(v)}" for k, v in groups.items())
    print(f"Wrote {len(rows)} rows to {out.relative_to(ROOT)} ({counts})")
    return out
