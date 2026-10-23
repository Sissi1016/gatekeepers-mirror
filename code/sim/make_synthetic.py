#!/usr/bin/env python3
"""Synthetic ICLR-like records with known truth, for testing 05_learners.py and for the Appendix C simulation.

Outputs (into --out, default data/synthetic/): texts.parquet (id, year, title, abstract, keywords),
submissions.csv (02_assemble.py layout), outcomes.csv (04_outcomes.py layout), truth.csv (latent quality).

Data-generating process. Quality Q ~ N(0,1) is independent of group G (true group effect on outcomes = 0).
The text reveals Q only partly: a share `private` of Q's variance is seen by reviewers but absent from the
text. Reviewers accept when Q + noise exceeds a cutoff that is `bar` higher for G = 1 (a higher bar).
Group-marker words appear in G = 1 texts with probability `marker` (0 = the group is invisible in the text).
Outcomes (citations) depend on Q only. Rejected papers are matched to a later outcome with probability
`match`. A placebo flag is drawn independently of everything.
Expected: D places G below its truth (inheritance); O+ places G above it (reversal) when private > 0 and
bar > 0; the reversal shrinks as private -> 0; placebo shows no error.
"""
import argparse
import pathlib

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "data/synthetic"))
    ap.add_argument("--n-per-year", type=int, default=1500)
    ap.add_argument("--bar", type=float, default=0.6)
    ap.add_argument("--private", type=float, default=0.5)
    ap.add_argument("--marker", type=float, default=0.8)
    ap.add_argument("--match", type=float, default=0.3)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--fidelity", choices=["low", "high"], default="low",
                    help="low: word counts give a coarse, noisy reading of q_text; high: 20 graded bins, near-exact")
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    qual_words = [f"q{i:03d}" for i in range(150)]
    filler = [f"w{i:03d}" for i in range(800)]
    markers = [f"novel{i:02d}" for i in range(30)]
    rows, outs, truth = [], [], []
    k = 0
    for year in range(2017, 2025):
        n = a.n_per_year
        G = (rng.random(n) < 0.25).astype(int)
        placebo = (rng.random(n) < 0.5).astype(int)
        q_text = np.sqrt(1 - a.private) * rng.normal(size=n)   # part of quality the text reveals
        q_priv = np.sqrt(a.private) * rng.normal(size=n)       # part seen by reviewers only
        Q = q_text + q_priv
        latent = Q + 0.3 * rng.normal(size=n) - a.bar * G
        cutoff = np.quantile(latent, 0.70)
        acc = (latent > cutoff).astype(int)
        score = np.clip(5 + 1.5 * (Q + 0.5 * rng.normal(size=n)) - a.bar * G, 1, 10)
        cites = np.round(np.exp(1.5 + 0.9 * Q + 0.5 * rng.normal(size=n))).astype(int)
        for i in range(n):
            if a.fidelity == "low":
                nq = int(np.clip(rng.poisson(max(0.5, 6 + 4 * q_text[i])), 0, 30))
                words = list(rng.choice(qual_words[:75] if q_text[i] > 0 else qual_words[75:], size=nq))
            else:
                b = int(np.clip(np.floor((q_text[i] + 2.5) / 0.25), 0, 19))   # 20 graded bins of the text-visible quality
                words = list(rng.choice(qual_words[b * 7:(b + 1) * 7], size=20))
            words += list(rng.choice(filler, size=60))
            if G[i] and rng.random() < a.marker:
                words += list(rng.choice(markers, size=4))
            rng.shuffle(words)
            pid = f"syn{k:06d}"
            k += 1
            rows.append(dict(id=pid, year=year, title=" ".join(words[:8]), abstract=" ".join(words[8:]), keywords=[]))
            matched = 1 if acc[i] else int(rng.random() < a.match)
            outs.append(dict(openreview_id=pid, matched=matched, cites=float(cites[i]) if matched else np.nan))
            truth.append(dict(openreview_id=pid, year=year, G=G[i], Q=Q[i], q_private=q_priv[i], cites_true=cites[i],
                              accept=acc[i], decision="accept" if acc[i] else "reject", mean_score=score[i],
                              newcomer_team=G[i], placebo_parity=placebo[i]))
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_parquet(out / "texts.parquet", index=False)
    pd.DataFrame(outs).to_csv(out / "outcomes.csv", index=False)
    t = pd.DataFrame(truth)
    t.to_csv(out / "truth.csv", index=False)
    sub = t[["openreview_id", "year", "decision", "mean_score", "newcomer_team", "placebo_parity"]].copy()
    sub["placebo_title_am"] = (np.random.default_rng(a.seed + 1).random(len(sub)) < 0.5).astype(int)
    sub.to_csv(out / "submissions.csv", index=False)
    print(f"wrote {len(t)} synthetic submissions to {out} (bar={a.bar}, private={a.private}, marker={a.marker})")


if __name__ == "__main__":
    main()
