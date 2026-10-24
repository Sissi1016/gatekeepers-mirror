# First look at the ICLR records (2026-10-24)

Data: `berenslab/iclr-dataset`, file `iclr26v1.parquet` (MIT), downloaded 2026-10-24, SHA-256 in
`data/raw/MANIFEST.json`. 55,906 submissions, 2017–2026; 2026 has no decisions and hidden author names.
No outcome data beyond ICLR itself have been used; the OpenAlex queries that supply later publication
and citations for accepted and rejected papers await the author's approval.

## What the record shows by group (`01_group_gaps.md`, `01_group_gaps.csv`)

- **Newcomer teams** (no author with an earlier ICLR submission, matched by name): acceptance rates are
  14 to 24 percentage points lower than for other submissions in every year from 2018 to 2025 (standard
  errors about 2 points), mean standardized reviewer scores are 0.5 to 0.75 standard deviations lower, and
  withdrawal rates are 3 to 10 points higher. Newcomer teams are the group with a large and stable gap in
  this record. The gap mixes any difference in the bar with differences in quality; without random
  assignment of reviewers the record cannot separate them.
- **Novel submissions** (top quartile of TF-IDF novelty against the two previous years, excluding
  co-authored neighbours): no systematic acceptance gap (between −4 and +4.5 points across years). With this
  measure, the record shows no penalty on novelty.
- **Placebo groups** (paper-number parity; title initial A–M): of 16 year-by-group gaps, none exceeds about
  1.8 standard errors, as expected if these groups face the same bar.

## Decision-page learners (`02_iclr_resub_2023_*`)

Trained on 2018–2022 titles, abstracts and keywords (TF-IDF), evaluated on 2023:
- D (predicts acceptance): AUC 0.648.
- D_J (predicts the mean reviewer score): R² 0.107.

## The rejected side cannot yet be scored

The only outcome available without external data is resubmission within ICLR (`07_resub_outcomes.py`):
of 17,232 rejected submissions in 2017–2025, 588 were matched to a later ICLR resubmission, 320 of them to one
with a decision, and 105 of those were accepted. For the 2023 evaluation year only 77 of 2,226 rejected
submissions have such an outcome (6 from newcomer teams). Signed errors computed against this channel are
reported in `02_iclr_resub_2023_summary.md` for completeness but are not interpretable: the matched-only
estimates have intervals of about ±0.3, and the lower bound treats almost every rejected paper as a failure.
The outcome is also a later set of reviewers' judgment, observed only for authors who chose to resubmit.
Scoring the learners on the rejected side requires the protocol's outcome channel A (later publication
and citations from OpenAlex).

## Changes to the pipeline made today (logged in `docs/decisions.md`)

- The mirror stores authors as one comma-separated string; the newcomer flag now splits names and uses
  names for all years (OpenReview IDs exist only from 2021). 2017 is excluded from newcomer analyses because
  it has no earlier year.
- "Invite to Workshop Track" (136 submissions, 2017–2018) is coded as reject from the main conference.
- Novelty uses TF-IDF rather than the sentence encoder in protocol v0, and excludes neighbours that share an
  author, so that a resubmission is not counted as unoriginal.
- Resubmission links require a shared author and cosine ≥ 0.5 or title similarity ≥ 90 (2026: cosine ≥ 0.6 or
  title ≥ 95, since authors are hidden). A random sample of 12 links all matched the same paper; recall is
  unknown and probably low, since many rejected papers move to other venues or change substantially.
