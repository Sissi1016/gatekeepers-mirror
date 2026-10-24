#!/usr/bin/env python3
"""Assemble the submission-level table for the ICLR prototype.

Inputs : data/raw/iclr26v1.parquet (berenslab/iclr-dataset; see 01_download.py).
Outputs: data/processed/iclr_submissions.csv  (one row per submission; no abstracts)
         data/processed/iclr_submissions.columns.md  (column dictionary)
         results/00_schema_report.md  (columns, year counts, decision values, score coverage)

Steps: inspect the schema (printed and saved, so that column-name assumptions are visible);
normalize decisions into accept / reject / withdrawn / other; mean reviewer score; newcomer-team
flag (no author seen in an earlier ICLR year); placebo groups (paper-number parity, title initial).
Topic novelty needs an embedding model and is computed in 03_novelty.py.
"""
from __future__ import annotations

import pathlib
import re
import sys

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "iclr26v1.parquet"
OUT = ROOT / "data" / "processed" / "iclr_submissions.csv"
OUT_DICT = ROOT / "data" / "processed" / "iclr_submissions.columns.md"
REPORT = ROOT / "results" / "00_schema_report.md"


def normalize_decision(x) -> str:
    s = str(x).lower()
    if "withdraw" in s:
        return "withdrawn"
    if "desk" in s:
        return "desk_reject"
    if "workshop" in s:
        return "reject"  # "Invite to Workshop Track" (2017-2018): not accepted to the main conference
    if "reject" in s:
        return "reject"
    if "accept" in s or "oral" in s or "poster" in s or "spotlight" in s:
        return "accept"
    if s in ("nan", "none", "", "unknown"):
        return "unknown"
    return "other"


def first_col(df: pd.DataFrame, candidates) -> str | None:
    for c in candidates:
        if c in df.columns:
            return c
    return None


def mean_score(v):
    try:
        vals = [float(s) for s in list(v) if s is not None and str(s) != "nan"]
    except TypeError:
        return float("nan")
    return sum(vals) / len(vals) if vals else float("nan")


def main() -> int:
    if not RAW.exists():
        print(f"missing {RAW}; run 01_download.py --yes first")
        return 1
    df = pd.read_parquet(RAW)
    lines = ["# Schema report for iclr26v1.parquet", "", f"rows: {len(df)}", "", "## columns", ""]
    for c in df.columns:
        lines.append(f"- `{c}`: {df[c].dtype}; example: {str(df[c].iloc[0])[:80]!r}")

    col_year = first_col(df, ["year", "Year"])
    col_id = first_col(df, ["id", "openreview_id", "paper_id"])
    col_title = first_col(df, ["title", "Title"])
    col_abs = first_col(df, ["abstract", "Abstract"])
    col_dec = first_col(df, ["decision", "Decision"])
    col_scores = first_col(df, ["scores", "ratings", "review_scores"])
    col_authors = first_col(df, ["authors", "author_names"])
    col_author_ids = first_col(df, ["author_ids", "authorids", "author_openreview_ids"])
    col_keywords = first_col(df, ["keywords", "Keywords"])
    col_label = first_col(df, ["label", "labels"])
    lines += ["", "## column mapping used", ""]
    for k, v in dict(year=col_year, id=col_id, title=col_title, abstract=col_abs, decision=col_dec,
                     scores=col_scores, authors=col_authors, author_ids=col_author_ids,
                     keywords=col_keywords, label=col_label).items():
        lines.append(f"- {k}: `{v}`")

    out = pd.DataFrame({
        "openreview_id": df[col_id] if col_id else range(len(df)),
        "year": df[col_year].astype(int) if col_year else -1,
        "title": df[col_title] if col_title else "",
    })
    out["decision_raw"] = df[col_dec].astype(str) if col_dec else "unknown"
    out["decision"] = out["decision_raw"].map(normalize_decision)
    out["mean_score"] = df[col_scores].map(mean_score) if col_scores else float("nan")
    out["n_scores"] = df[col_scores].map(lambda v: len(list(v)) if v is not None and not isinstance(v, float) else 0) if col_scores else 0
    out["abstract_chars"] = df[col_abs].astype(str).str.len() if col_abs else 0
    out["label"] = df[col_label].astype(str) if col_label else "unlabeled"

    # newcomer team: no author seen in an earlier ICLR year. The mirror stores authors as one comma-separated
    # string; OpenReview IDs exist only from 2021, so names (lower-cased) are used for every year to keep the
    # comparison consistent. Name collisions make the flag conservative (some newcomers counted as returning).
    def split_names(v):
        if v is None or isinstance(v, float):
            return []
        items = v.split(",") if isinstance(v, str) else list(v)
        return [" ".join(str(a).split()).lower() for a in items if str(a).strip()]
    names = df[col_authors].map(split_names) if col_authors else pd.Series([[]] * len(df))
    seen: set = set()
    flags = [None] * len(out)
    for y in sorted(out["year"].unique()):
        idx = out.index[out["year"] == y]
        year_names = [names.iloc[i] for i in idx]
        for i, ns in zip(idx, year_names):
            flags[i] = int(len(ns) > 0 and not any(a in seen for a in ns))
        for ns in year_names:
            seen.update(ns)
    out["newcomer_team"] = flags
    out["newcomer_basis"] = "names, all years"
    out["n_authors"] = names.map(len)

    # placebo groups
    num = out["openreview_id"].astype(str).map(lambda s: sum(ord(ch) for ch in s))  # deterministic pseudo-parity
    out["placebo_parity"] = (num % 2).astype(int)
    out["placebo_title_am"] = out["title"].astype(str).str.strip().str[:1].str.upper().map(lambda ch: int(bool(re.match(r"[A-M]", ch or ""))))

    lines += ["", "## year counts", "", out["year"].value_counts().sort_index().to_string(), "",
              "## decision (normalized) by year", "",
              pd.crosstab(out["year"], out["decision"]).to_string(), "",
              "## raw decision values (top 30)", "", out["decision_raw"].value_counts().head(30).to_string(), "",
              "## score coverage", "", f"rows with >=1 score: {(out['n_scores'] > 0).sum()}",
              "", "## newcomer teams by year", "", out.groupby("year")["newcomer_team"].mean().round(3).to_string()]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)
    OUT_DICT.write_text(
        "| column | meaning |\n|---|---|\n"
        "| openreview_id | OpenReview forum/note id from the mirror |\n"
        "| year | ICLR year |\n| title | submission title |\n"
        "| decision_raw | decision string as in the mirror |\n"
        "| decision | accept / reject / withdrawn / desk_reject / other / unknown |\n"
        "| mean_score | mean of reviewer ratings (final scores as mirrored) |\n"
        "| n_scores | number of reviewer ratings |\n| n_authors | number of listed authors |\n"
        "| abstract_chars | abstract length |\n| label | topic label from the mirror (keyword-based) |\n"
        "| newcomer_team | 1 if no author appeared in an earlier ICLR year of the dataset |\n"
        "| newcomer_basis | whether newcomer flag used author ids or names |\n"
        "| placebo_parity | deterministic pseudo-random group (placebo) |\n"
        "| placebo_title_am | title starts with A-M (placebo) |\n",
        encoding="utf-8")
    print(f"wrote {OUT} ({len(out)} rows), {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
