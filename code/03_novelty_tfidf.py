#!/usr/bin/env python3
"""Topic novelty of each submission, and links from a submission to its later resubmission within ICLR.

Inputs : data/raw/iclr26v1.parquet (id, year, title, abstract, authors)
Outputs: data/processed/iclr_novelty.csv   (openreview_id, year, novelty, max_sim_prev2, novel_q4)
         data/processed/iclr_resub_links.csv (earlier_id, earlier_year, later_id, later_year, sim, title_ratio, shared_author)

Novelty = 1 - maximum TF-IDF cosine similarity between a submission's title+abstract and any submission in
the two preceding years written by none of the same authors (so that a paper's own earlier version does not
make it look unoriginal). novel_q4 = top quartile within year. Years 2019-2026.

Resubmission link: an earlier submission and a later one (one or two years apart) that share at least one
author name and have cosine >= 0.5 or title similarity >= 90 (rapidfuzz token_sort_ratio). 2026 author names
are hidden during review, so for 2026 a link requires cosine >= 0.6 or title similarity >= 95 without the author
condition. Thresholds were set before inspecting outcomes and are checked by printing a sample of links.

Deviation from protocol v0 (section 4): TF-IDF instead of an open-weight sentence encoder, whose download has
not been approved. Logged in docs/decisions.md.
"""
import pathlib
import sys
import warnings

import numpy as np
import pandas as pd
from rapidfuzz import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer

warnings.filterwarnings("ignore", message=".*encountered in matmul", category=RuntimeWarning)
ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "iclr26v1.parquet"
OUT_NOV = ROOT / "data" / "processed" / "iclr_novelty.csv"
OUT_LINK = ROOT / "data" / "processed" / "iclr_resub_links.csv"
K = 30  # neighbours kept per submission


def names(v):
    if not isinstance(v, str):
        return set()
    return {" ".join(a.split()).lower() for a in v.split(",") if a.strip()}


def main() -> int:
    df = pd.read_parquet(RAW, columns=["id", "year", "title", "abstract", "authors"]).reset_index(drop=True)
    df["text"] = df["title"].fillna("") + ". " + df["abstract"].fillna("")
    auth = df["authors"].map(names).values
    titles = df["title"].fillna("").str.lower().values
    vec = TfidfVectorizer(min_df=3, max_df=0.5, ngram_range=(1, 2), sublinear_tf=True, stop_words="english")
    X = vec.fit_transform(df["text"])
    nov_rows, links = [], []
    for y in range(2019, int(df["year"].max()) + 1):
        cur = np.where(df["year"].values == y)[0]
        prev = np.where(df["year"].isin([y - 1, y - 2]).values)[0]
        P = X[prev].T.tocsc()
        best = np.zeros(len(cur))
        for s in range(0, len(cur), 1500):
            block = (X[cur[s:s + 1500]] @ P).toarray()
            top = np.argpartition(-block, K, axis=1)[:, :K]
            for r in range(block.shape[0]):
                i = cur[s + r]
                cand = top[r][np.argsort(-block[r, top[r]])]
                b = 0.0
                for c in cand:
                    j = prev[c]
                    sim = block[r, c]
                    shared = bool(auth[i] & auth[j])
                    if not shared and b == 0.0:
                        b = sim  # most similar prior paper by other authors
                    if sim >= 0.3:
                        tr = fuzz.token_sort_ratio(titles[i], titles[j])
                        if y < 2026:
                            is_link = shared and (sim >= 0.5 or tr >= 90)
                        else:
                            is_link = sim >= 0.6 or tr >= 95
                        if is_link:
                            links.append((df["id"][j], int(df["year"][j]), df["id"][i], y, round(float(sim), 3),
                                          round(tr, 1), int(shared)))
                best[s + r] = b
        nov = 1 - best
        q = np.quantile(nov, 0.75)
        nov_rows.append(pd.DataFrame({"openreview_id": df["id"].values[cur], "year": y, "max_sim_prev2": best.round(4),
                                      "novelty": nov.round(4), "novel_q4": (nov >= q).astype(int)}))
        print(y, len(cur), "median max-sim (other authors)", round(float(np.median(best)), 3), "links so far", len(links))
    pd.concat(nov_rows).to_csv(OUT_NOV, index=False)
    L = pd.DataFrame(links, columns=["earlier_id", "earlier_year", "later_id", "later_year", "sim", "title_ratio",
                                     "shared_author"])
    L.to_csv(OUT_LINK, index=False)
    print(f"wrote {OUT_NOV} and {OUT_LINK} ({len(L)} links)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
