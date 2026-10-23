#!/usr/bin/env python3
"""Train the decision and outcome learners on one set of records and score each, by group, on the rejected side.

Inputs : --texts        parquet with id, year, title, abstract, keywords (default: data/raw/iclr26v1.parquet)
         --submissions  data/processed/iclr_submissions.csv (02_assemble.py): decision, mean_score, groups
         --outcomes     data/processed/iclr_outcomes.csv (04_outcomes.py, OpenAlex; not yet written): openreview_id, matched (0/1),
                        cites (citations in a fixed window from the decision date; NaN if unmatched)
         --groups       group columns to score (0/1 flags in submissions or in --extra-groups)
         --extra-groups optional csv with openreview_id and more 0/1 group columns (e.g. novelty quartile)
Outputs: results/<prefix>_signed_error.csv   one row per learner x group x truth bound
         results/<prefix>_decision_page.csv  AUC / R^2 of each learner on the page it was trained on
         results/<prefix>_summary.md         the same tables in readable form, with settings

Learners (protocol section 5): D (acceptance), D_J (mean reviewer score), O (log citations, accepted only),
O_m (O on the bottom score quartile of accepted papers). O is run twice: O+ sees the group flag as an
explicit input, O- does not (the configuration of Arnold, Dobbie & Hull 2025). All learners read the same
text features (TF-IDF of title, abstract and keywords); none sees reviews or decisions at prediction time.

Scoring (protocol section 7). Every learner's score and the true outcome are converted to percentile ranks
among the evaluation year's rejected submissions, so that decision and outcome learners share a scale.
Signed error for group g = mean rank of the learner's score in g - mean rank of the true outcome in g.
Positive = the learner places g higher than g's realized outcomes warrant. Truth is bounded: unmatched
rejected papers are set to zero citations (lower bound) or drawn from the matched rejected papers in the
same group (upper bound). Bootstrap intervals resample submissions.
"""
import argparse
import pathlib
import sys
import warnings

import numpy as np
import pandas as pd
from scipy.stats import rankdata
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import r2_score, roc_auc_score

ROOT = pathlib.Path(__file__).resolve().parents[1]
SEED = 20261023
# numpy 2.0 with Apple Accelerate emits spurious divide/overflow warnings on finite matmuls
# (checked 2026-10-23: results identical to einsum to 1e-14); silence only those.
warnings.filterwarnings("ignore", message=".*encountered in matmul", category=RuntimeWarning)


def load(args):
    sub = pd.read_csv(args.submissions)
    txt = pd.read_parquet(args.texts)
    idc = next(c for c in ["id", "openreview_id", "paper_id"] if c in txt.columns)
    kw = txt["keywords"].map(lambda v: " ".join(map(str, v)) if v is not None and not isinstance(v, (float, str)) else str(v or "")) \
        if "keywords" in txt.columns else ""
    txt = pd.DataFrame({"openreview_id": txt[idc].astype(str),
                        "text": txt.get("title", "").astype(str) + ". " + txt.get("abstract", "").astype(str) + ". " + kw})
    sub["openreview_id"] = sub["openreview_id"].astype(str)
    df = sub.merge(txt, on="openreview_id", how="left")
    out = pd.read_csv(args.outcomes)
    out["openreview_id"] = out["openreview_id"].astype(str)
    df = df.merge(out[["openreview_id", "matched", "cites"]], on="openreview_id", how="left")
    if args.extra_groups:
        eg = pd.read_csv(args.extra_groups)
        eg["openreview_id"] = eg["openreview_id"].astype(str)
        df = df.merge(eg, on="openreview_id", how="left")
    df = df[df["decision"].isin(["accept", "reject"])].copy()
    df["accept"] = (df["decision"] == "accept").astype(int)
    df["log_cites"] = np.log1p(df["cites"])
    return df


def features(train_text, all_text):
    vec = TfidfVectorizer(min_df=3, max_df=0.5, ngram_range=(1, 2), max_features=50000, sublinear_tf=True)
    vec.fit(train_text.fillna(""))
    return vec.transform(all_text.fillna(""))


def with_group(X, flag):
    from scipy.sparse import hstack, csr_matrix
    return hstack([X, csr_matrix(flag.reshape(-1, 1).astype(float))]).tocsr()


def train_predict(df, train, test, groups):
    X = features(df.loc[train, "text"], df["text"])
    pred, page = {}, []
    # D: decisions, all decided submissions
    m = LogisticRegression(C=4.0, max_iter=2000).fit(X[train.values], df.loc[train, "accept"])
    pred["D"] = m.predict_proba(X)[:, 1]
    page.append(("D", "AUC accept (eval year)", roc_auc_score(df.loc[test, "accept"], pred["D"][test.values])))
    # D_J: the gatekeepers' rating as label
    tj = train & df["mean_score"].notna()
    m = Ridge(alpha=3.0, solver="lsqr").fit(X[tj.values], df.loc[tj, "mean_score"])
    pred["D_J"] = m.predict(X)
    ej = test & df["mean_score"].notna()
    page.append(("D_J", "R2 mean score (eval year)", r2_score(df.loc[ej, "mean_score"], pred["D_J"][ej.values])))
    # O and O_m: outcomes of the admitted only
    to = train & (df["accept"] == 1) & df["log_cites"].notna()
    q = df.loc[to].groupby("year")["mean_score"].transform(lambda s: s <= s.quantile(0.25))
    tom = to.copy()
    tom.loc[to] = q.fillna(False).astype(bool).values
    eo = test & (df["accept"] == 1) & df["log_cites"].notna()
    for name, mask in [("O", to), ("O_m", tom)]:
        m = Ridge(alpha=3.0, solver="lsqr").fit(X[mask.values], df.loc[mask, "log_cites"])
        pred[f"{name}-"] = m.predict(X)
        page.append((f"{name}-", "R2 log cites, accepted (eval year)", r2_score(df.loc[eo, "log_cites"], pred[f"{name}-"][eo.values])))
        for g in groups:
            flag = df[g].fillna(0).values
            Xg = with_group(X, flag)
            m = Ridge(alpha=3.0, solver="lsqr").fit(Xg[mask.values], df.loc[mask, "log_cites"])
            pred[f"{name}+[{g}]"] = m.predict(Xg)
    return pred, page


def truth_bounds(rej, group, rng):
    y = rej["cites"].values.astype(float)
    matched = rej["matched"].fillna(0).values.astype(bool) & ~np.isnan(y)
    lower = np.where(matched, y, 0.0)
    upper = lower.copy()
    for gv in (0, 1):
        pool = y[matched & (group == gv)]
        idx = ~matched & (group == gv)
        if pool.size:
            upper[idx] = rng.choice(pool, size=idx.sum(), replace=True)
    return {"lower(unmatched=0)": lower, "upper(unmatched~matched)": upper, "matched_only": np.where(matched, y, np.nan)}


def pct(v):
    ok = ~np.isnan(v)
    r = np.full(v.shape, np.nan)
    r[ok] = (rankdata(v[ok]) - 0.5) / ok.sum()
    return r


def signed_error(score, truth, group, rng, B):
    s, t = pct(score), pct(truth)
    ok = ~np.isnan(t)
    s, t, g = s[ok], t[ok], group[ok]
    est = s[g == 1].mean() - t[g == 1].mean()
    boots = []
    n = len(s)
    for _ in range(B):
        i = rng.integers(0, n, n)
        si, ti, gi = s[i], t[i], g[i]
        if (gi == 1).sum() > 1:
            boots.append(si[gi == 1].mean() - ti[gi == 1].mean())
    lo, hi = np.percentile(boots, [2.5, 97.5]) if boots else (np.nan, np.nan)
    return est, lo, hi, int((g == 1).sum()), int(n)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--texts", default=str(ROOT / "data/raw/iclr26v1.parquet"))
    ap.add_argument("--submissions", default=str(ROOT / "data/processed/iclr_submissions.csv"))
    ap.add_argument("--outcomes", default=str(ROOT / "data/processed/iclr_outcomes.csv"))
    ap.add_argument("--extra-groups", default=None)
    ap.add_argument("--groups", default="newcomer_team,placebo_parity,placebo_title_am")
    ap.add_argument("--train-years", default="2017-2023")
    ap.add_argument("--eval-year", type=int, default=2024)
    ap.add_argument("--bootstrap", type=int, default=500)
    ap.add_argument("--prefix", default="01_iclr")
    args = ap.parse_args()
    for p in (args.texts, args.submissions, args.outcomes):
        if not pathlib.Path(p).exists():
            print(f"missing {p}")
            return 1
    rng = np.random.default_rng(SEED)
    groups = [g.strip() for g in args.groups.split(",") if g.strip()]
    df = load(args).reset_index(drop=True)
    y0, y1 = map(int, args.train_years.split("-"))
    train = df["year"].between(y0, y1)
    test = df["year"] == args.eval_year
    pred, page = train_predict(df, train, test, groups)

    rej = test & (df["accept"] == 0)
    rows = []
    for g in groups:
        gv = df.loc[rej, g].fillna(0).values.astype(int)
        bounds = truth_bounds(df.loc[rej], gv, rng)
        acc_gap = df.loc[test & (df[g] == 1), "accept"].mean() - df.loc[test & (df[g] == 0), "accept"].mean()
        for learner, score in pred.items():
            if "+[" in learner and not learner.endswith(f"[{g}]"):
                continue
            for bname, truth in bounds.items():
                est, lo, hi, ng, n = signed_error(score[rej.values], truth, gv, rng, args.bootstrap)
                rows.append(dict(group=g, learner=learner.replace(f"[{g}]", ""), truth=bname, signed_error=est,
                                 ci_lo=lo, ci_hi=hi, n_group_rejected=ng, n_rejected=n,
                                 acceptance_gap_eval_year=acc_gap))
    res = pd.DataFrame(rows)
    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)
    res.to_csv(out_dir / f"{args.prefix}_signed_error.csv", index=False)
    pg = pd.DataFrame(page, columns=["learner", "metric", "value"])
    pg.to_csv(out_dir / f"{args.prefix}_decision_page.csv", index=False)
    match_rate = df.loc[rej, "matched"].fillna(0).mean()
    wide = res.pivot_table(index=["group", "learner"], columns="truth", values="signed_error").round(3)
    md = [f"# Signed error by group on the rejected side ({args.prefix})", "",
          f"Train years {args.train_years}; evaluation year {args.eval_year}; rejected submissions in evaluation year: {int(rej.sum())}; "
          f"share matched to a later outcome: {match_rate:.3f}. Seed {SEED}; bootstrap {args.bootstrap}.", "",
          "Signed error = mean percentile rank of the learner's score in the group minus mean percentile rank of the realized outcome "
          "in the group, among rejected submissions of the evaluation year. Positive: the learner places the group higher than its "
          "realized outcomes warrant. Columns are the truth bounds.", "", "```\n" + wide.to_string() + "\n```", "",
          "## Fit on the page each learner was trained on", "", "```\n" + pg.round(3).to_string(index=False) + "\n```", ""]
    (out_dir / f"{args.prefix}_summary.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
