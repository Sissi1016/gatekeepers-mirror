# The Gatekeeper's Mirror — ICLR prototype

Prototype and protocol for **validating what AI learns about the rejected from organizational records**.
A gatekeeping record contains a decision for everyone but an outcome only for those admitted. A model
that learns the *decisions* inherits the gatekeepers' preferences; a model that learns the *outcomes of
the admitted* can reverse them; both pass the checks organizations usually run. This repository builds
the public, reproducible testbed on ICLR peer review (OpenReview data via licensed mirrors) and
implements the scoring protocol: train several learners on the same records, score each against what
rejected submissions actually went on to do, and report signed error with bounds.

Companion to a Stage 1 proposal for the *Organization Science* special issue "AI-Enabled Frontiers in
Organizational Science". Author: Huaxi Gao (Ross School of Business, University of Michigan).

## Status
Scaffold (2026-10-23). No results yet. See `protocol/prototype_iclr_v0.md` for the design and
`docs/decisions.md` for the running log of human decisions.

## Layout
- `protocol/` — the scoring protocol and the prototype design (what is a learner, what is ground truth,
  how signed error and bounds are reported, placebo groups).
- `code/` — numbered scripts; each states its inputs and outputs at the top.
- `data/raw/` — never committed; `MANIFEST.json` records every download.
- `data/processed/` — small derived tables, committed.
- `results/` — tables and figures.
- `logs/` — one line per model call (input hash, prompt and model versions, output, cost).
- `docs/` — decision log and AI-use statement.

## Data and licenses
- ICLR submissions, decisions and scores: berenslab/iclr-dataset (MIT).
- Reviews and full text: Samarth0710/reviewarena (CC BY 4.0), used where needed.
- Later outcomes: OpenAlex (CC0).
Redistribution of derived tables follows the source licenses; nothing here goes beyond what OpenReview
already publishes.

## License
Code and documents in this repository: MIT. Data retain their source licenses.
