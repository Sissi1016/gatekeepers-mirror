#!/usr/bin/env python3
"""Rerun the six simulation scenarios over many seeds (Appendix C).

Outputs: results/sim_seeds_signed_error.csv (one row per seed x scenario x group x learner; matched-only truth)
         results/sim_seeds_summary.md (mean, 2.5th and 97.5th percentiles across seeds)
"""
import argparse
import pathlib
import subprocess
import sys

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[2]
PY = sys.executable
SCEN = {"base": (0.6, 0.5, 0.8, "low"), "noprivate": (0.6, 0.0, 0.8, "low"), "hifi_base": (0.6, 0.5, 0.8, "high"),
        "hifi_noprivate": (0.6, 0.0, 0.8, "high"), "masked": (0.6, 0.5, 0.0, "low"), "nobar": (0.0, 0.5, 0.8, "low")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=30)
    ap.add_argument("--n-per-year", type=int, default=1000)
    a = ap.parse_args()
    tmp = ROOT / "data/synthetic/seeds"
    rows = []
    for seed in range(1, a.seeds + 1):
        for name, (bar, priv, marker, fid) in SCEN.items():
            subprocess.run([PY, str(ROOT / "code/sim/make_synthetic.py"), "--out", str(tmp), "--bar", str(bar),
                            "--private", str(priv), "--marker", str(marker), "--fidelity", fid, "--seed", str(seed),
                            "--n-per-year", str(a.n_per_year)], check=True, capture_output=True)
            subprocess.run([PY, str(ROOT / "code/05_learners.py"), "--texts", str(tmp / "texts.parquet"),
                            "--submissions", str(tmp / "submissions.csv"), "--outcomes", str(tmp / "outcomes.csv"),
                            "--groups", "newcomer_team,placebo_parity", "--bootstrap", "0", "--prefix", "_seedtmp"],
                           check=True, capture_output=True)
            d = pd.read_csv(ROOT / "results/_seedtmp_signed_error.csv")
            d = d[d.truth == "matched_only"].assign(seed=seed, scenario=name)
            rows.append(d)
        print(f"seed {seed} done", flush=True)
        out = pd.concat(rows)
        out.to_csv(ROOT / "results/sim_seeds_signed_error.csv", index=False)
    for f in ROOT.glob("results/_seedtmp_*"):
        f.unlink()
    g = out.groupby(["group", "learner", "scenario"])["signed_error"]
    s = pd.DataFrame({"mean": g.mean(), "p2.5": g.quantile(0.025), "p97.5": g.quantile(0.975), "seeds": g.size()}).round(3)
    cell = (s["mean"].map("{:+.3f}".format) + " [" + s["p2.5"].map("{:+.2f}".format) + ", " + s["p97.5"].map("{:+.2f}".format) + "]")
    tab = cell.unstack("scenario")[list(SCEN)]
    md = ["# Simulation across seeds (Appendix C)", "",
          f"{a.seeds} seeds per scenario; {a.n_per_year} submissions a year; matched-only truth; cells = mean signed error "
          "[2.5th, 97.5th percentile across seeds]. Scenario settings as in `sim_v0_summary.md`.", "", "```", tab.to_string(), "```", ""]
    (ROOT / "results/sim_seeds_summary.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
