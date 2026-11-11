"""Shared loaders for metric-history data (one per source type).

Each loader returns rows in the standard schema (metric_history.SCHEMA).
A metric's build script (scripts/build_<metric>_scores.py) picks the loaders
and settings it needs, then calls write_scores().

Source roles (the `source` column):
  Primary     - hand-checked scores (data/<metric>/primary.csv)
  Independent - one organization re-ran every model the same way:
                Stanford CRFM HELM, Epoch AI's own runs
  Compiled    - reported scores collected in one place: Epoch AI's
                "external runs" (CC-BY)
  Unverified  - aggregator scores not checked by us (data/<metric>/unverified.csv)
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


def load_epoch(csv_name: str, exclude_link_substrings: tuple[str, ...] = (), *,
               score_col: str = "EM", role: str = "Compiled",
               original_source: str | None = None, source_url: str | None = None,
               stderr_col: str | None = None, extra_note_cols: tuple[str, ...] = (),
               setup_detail: str | None = None) -> list[dict]:
    """Rows from one Epoch "external runs" CSV (e.g. 'mmlu_external.csv').

    Usually these are reported scores Epoch collected (role "Compiled", the
    row's own Source column naming where each came from). Some files instead
    mirror one evaluator's same-setup leaderboard - pass role="Independent"
    and original_source to say whose.

    exclude_link_substrings drops rows whose source link contains any of the
    given strings - used to drop Epoch's copies of HELM runs, which we load
    directly (or exclude as not comparable).
    """
    text = _epoch_zip().read(csv_name).decode("utf-8")
    rows = []
    for r in csv.DictReader(io.StringIO(text)):
        link = r.get("Source link", "")
        if any(s in link for s in exclude_link_substrings):
            continue
        if not r["Release date"] or not r.get(score_col):
            continue
        score = float(r[score_col])
        setup = setup_detail or _epoch_setup(r.get("Shots", "").strip(), r.get("Notes", ""))
        if stderr_col and r.get(stderr_col):
            setup += f"; stderr ±{float(r[stderr_col]) * 100:.1f}"
        notes = "; ".join(f"{c}: {r[c]}" for c in extra_note_cols if r.get(c))
        rows.append({
            "model": r.get("Name") or r["Model version"],
            "date": r["Release date"],
            "date_basis": "release",
            "score": round(score * 100 if score <= 1 else score, 2),
            "setup_detail": setup,
            "source": role,
            "original_source": original_source or r.get("Source", "").strip(),
            "source_url": source_url or link,
            "notes": notes,
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
            "source": "Independent",
            "original_source": f"Stanford CRFM HELM ({project}) {release}",
            "source_url": page_url,
            "notes": "",
        })
    return rows


def load_epoch_runs(csv_name: str, page_url: str, best_per_model: bool = True) -> list[dict]:
    """Epoch AI's own benchmark runs (e.g. 'gpqa_diamond.csv').

    Epoch often runs one model at several settings (reasoning effort, token
    budget), encoded as a suffix after the last "_" in the model version.
    With best_per_model, keep only each model's best setting - matching how
    labs usually report a single headline number.
    """
    text = _epoch_zip().read(csv_name).decode("utf-8")
    rows = []
    for r in csv.DictReader(io.StringIO(text)):
        if not r["Release date"] or not r["mean_score"]:
            continue
        version = r["Model version"]
        base, _, setting = version.rpartition("_") if "_" in version else (version, "", "")
        stderr = r.get("stderr") or ""
        rows.append({
            "model": base,
            "date": r["Release date"],
            "date_basis": "release",
            "score": round(float(r["mean_score"]) * 100, 2),
            "setup_detail": f"Epoch AI harness; setting: {setting or 'default'}"
                            + (f"; stderr ±{float(stderr) * 100:.1f}" if stderr else ""),
            "source": "Independent",
            "original_source": "Epoch AI Benchmarking Hub (Epoch's own runs)",
            "source_url": page_url,
            "notes": "",
        })
    if best_per_model:
        best: dict[str, dict] = {}
        for r in rows:
            if r["model"] not in best or r["score"] > best[r["model"]]["score"]:
                best[r["model"]] = r
        rows = list(best.values())
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
