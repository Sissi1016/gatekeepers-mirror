#!/usr/bin/env python3
"""Outcome channel B: what rejected ICLR submissions did at later ICLR meetings.

Inputs : data/processed/iclr_submissions.csv, data/processed/iclr_resub_links.csv (03_novelty_tfidf.py)
Outputs: data/processed/iclr_outcomes_resub.csv  (openreview_id, matched, cites, resub_any)
         in the 05_learners.py layout: matched = 1 if the rejected submission reappeared at ICLR within two years
         with a decision; cites = 1 if any such reappearance was accepted, 0 otherwise. Accepted papers get no
         outcome here, so 05_learners.py skips the outcome-trained learners for this channel.

This outcome is a later set of reviewers' judgment, and it is observed only for authors who chose to resubmit
to ICLR and whose resubmission the matcher found. It sits at the judgment end of the label line and is
selected by the authors' persistence; it is not the outcome the protocol targets (citations from OpenAlex,
whose queries await approval).
"""
import pathlib
import sys

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main() -> int:
    sub = pd.read_csv(ROOT / "data/processed/iclr_submissions.csv")
    links = pd.read_csv(ROOT / "data/processed/iclr_resub_links.csv")
    dec = dict(zip(sub["openreview_id"].astype(str), sub["decision"]))
    links["later_decision"] = links["later_id"].astype(str).map(dec)
    decided = links[links["later_decision"].isin(["accept", "reject"])]
    later_acc = decided.groupby("earlier_id")["later_decision"].apply(lambda s: int((s == "accept").any()))
    rej = sub[sub["decision"] == "reject"][["openreview_id"]].copy()
    rej["openreview_id"] = rej["openreview_id"].astype(str)
    rej["resub_any"] = rej["openreview_id"].isin(links["earlier_id"].astype(str)).astype(int)
    rej["cites"] = rej["openreview_id"].map(later_acc)
    rej["matched"] = rej["cites"].notna().astype(int)
    rej.to_csv(ROOT / "data/processed/iclr_outcomes_resub.csv", index=False)
    print(f"rejected submissions: {len(rej)}; resubmitted (any): {rej.resub_any.sum()}; "
          f"resubmitted with a decision: {rej.matched.sum()}; of those accepted: {int(rej.cites.sum())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
