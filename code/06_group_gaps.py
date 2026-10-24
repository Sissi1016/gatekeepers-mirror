#!/usr/bin/env python3
"""Decision-page descriptives by group and year: how high is each group's bar, as far as the record shows?

Inputs : data/processed/iclr_submissions.csv (02_assemble.py), data/processed/iclr_novelty.csv (03_novelty_tfidf.py)
Outputs: results/01_group_gaps.csv  one row per year x group: shares and gaps with standard errors
         results/01_group_gaps.md   readable table and notes

For each group flag g (newcomer_team, novel_q4, and the two placebo flags) and each year with decisions
(2018-2025; 2017 has no prior years for the newcomer flag), among submissions that received a decision:
  - acceptance rate in g and outside g, and the gap (g minus rest), with a binomial standard error;
  - mean reviewer score standardized within year, in g and outside g (scales changed across years);
  - withdrawal rate among all submissions: withdrawal is the authors' own exit after reviews.
These gaps mix differences in thresholds with differences in quality; without random assignment of
reviewers they do not identify a bar. They describe the record that a learner would see.
"""
import pathlib
import sys

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
GROUPS = ["newcomer_team", "novel_q4", "placebo_parity", "placebo_title_am"]


def main() -> int:
    sub = pd.read_csv(ROOT / "data/processed/iclr_submissions.csv")
    nov = pd.read_csv(ROOT / "data/processed/iclr_novelty.csv")[["openreview_id", "novel_q4"]]
    sub = sub.merge(nov, on="openreview_id", how="left")
    sub = sub[sub["year"].between(2018, 2025)].copy()
    sub["z_score"] = sub.groupby("year")["mean_score"].transform(lambda s: (s - s.mean()) / s.std())
    rows = []
    for y, d in sub.groupby("year"):
        dec = d[d["decision"].isin(["accept", "reject"])]
        for g in GROUPS:
            if d[g].isna().all():
                continue
            a1, a0 = dec.loc[dec[g] == 1, "decision"].eq("accept"), dec.loc[dec[g] == 0, "decision"].eq("accept")
            w1, w0 = d.loc[d[g] == 1, "decision"].eq("withdrawn"), d.loc[d[g] == 0, "decision"].eq("withdrawn")
            se = np.sqrt(a1.var(ddof=1) / len(a1) + a0.var(ddof=1) / len(a0))
            rows.append(dict(year=y, group=g, n_in=int(len(a1)), n_out=int(len(a0)), accept_in=a1.mean(), accept_out=a0.mean(),
                             accept_gap=a1.mean() - a0.mean(), accept_gap_se=se,
                             zscore_in=dec.loc[dec[g] == 1, "z_score"].mean(), zscore_out=dec.loc[dec[g] == 0, "z_score"].mean(),
                             withdraw_in=w1.mean(), withdraw_out=w0.mean()))
    res = pd.DataFrame(rows).round(4)
    res.to_csv(ROOT / "results/01_group_gaps.csv", index=False)
    piv = res.pivot_table(index="year", columns="group", values="accept_gap").round(3)
    pivw = (res.assign(wgap=res.withdraw_in - res.withdraw_out)
            .pivot_table(index="year", columns="group", values="wgap").round(3))
    md = ["# Group gaps on the decision page (ICLR 2018-2025)", "",
          "Acceptance-rate gap = acceptance rate in the group minus outside it, among submissions with an accept or",
          "reject decision. Withdrawal gap = withdrawal rate in the group minus outside it, among all submissions.",
          "Gaps describe the record a learner sees; without random assignment they do not identify a threshold.",
          "novel_q4 uses the provisional TF-IDF novelty (protocol deviation). Placebo groups should show no gap.", "",
          "## Acceptance-rate gap", "", "```", piv.to_string(), "```", "",
          "## Withdrawal-rate gap", "", "```", pivw.to_string(), "```", "",
          "Full table with standard errors and standardized scores: `01_group_gaps.csv`.", ""]
    (ROOT / "results/01_group_gaps.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
