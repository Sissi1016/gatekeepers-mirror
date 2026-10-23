# ICLR prototype v0 — design

Date: 2026-10-23. Status: design fixed before any data is read; deviations are logged in `docs/decisions.md`.

## 1. Purpose
Show, on fully public data, that what a learner infers about rejected submissions depends on which page of the record it learns from, and score each learner against what the rejected submissions actually went on to do. The court testbed (random assignment of cases to judges) supplies clean ground truth but cannot be published; ICLR supplies weaker ground truth but can be rerun by anyone.

## 2. Data
- **Submissions, decisions, reviewer scores**: `berenslab/iclr-dataset`, file `iclr26v1.parquet` (ICLR 2017–2026; title, abstract, authors, OpenReview author IDs from 2021, decision, list of reviewer scores, keywords, topic label). License MIT.
- **Reviews, meta-reviews, full text** (only if a step below needs them): `Samarth0710/reviewarena`, ICLR split (CC BY 4.0).
- **Later outcomes**: OpenAlex API (CC0 metadata), queried by title; requests carry a contact e-mail and are cached.
- The OpenReview API itself returns `ChallengeRequiredError` to scripts (tested 2026-10-19 and 2026-10-23), so the mirrors are the source of record; every row keeps its OpenReview ID for audit.

## 3. Units, years, and the record's two pages
- Unit: one submission.
- **Decision page** (exists for every submission): accept / reject / withdrawn, plus reviewer scores. Withdrawn submissions are kept as a separate category and excluded from the main comparison.
- **Outcome page** (exists only for the admitted, in the organization's own record): for accepted papers, citations within a fixed window after the conference. For the prototype we also observe, outside the record, what rejected papers did later (section 6); that is the ground truth the organization never sees.
- Decision years used for learners: 2017–2023 for training, 2024 for evaluation (2025 as a second evaluation year once outcome windows allow; 2026 decisions only, no outcomes).

## 4. Groups ("the kind of applicant held to a higher bar")
The mirrors carry no affiliations, and rejected submissions' author identities are not guaranteed, so institution type and region are **v1** targets (requires matching authors to affiliations; feasibility to be reported). v0 uses two groups computable for every submission from the submission itself:
- **Topic novelty**: distance of the abstract embedding from the previous two years' ICLR corpus (nearest-neighbor distance, open-weight sentence encoder); top quartile = "novel". This is the group the organizational literature predicts is held to a higher bar.
- **Newcomer teams**: no author appears in any earlier ICLR submission in the dataset (author IDs from 2021; names before). Proxy for low status.
- **Placebo groups** (must show no reversal): parity of the OpenReview paper number; first letter of the title in A–M vs N–Z.

## 5. Learners (all trained on the same records, 2017–2023)
- **D — decision learner**: predicts acceptance from pre-decision content only (title, abstract, keywords). Two implementations: TF-IDF + logistic regression (baseline); sentence-embedding + logistic regression.
- **D_J — judgment-label learner**: same inputs plus the mean reviewer score as label (predicts the gatekeepers' rating rather than the decision). This is the "outcome that is itself a judgment" case.
- **O — outcome learner**: trained on accepted papers only, predicts the later outcome (citations within the window, log scale, and a binary "above median") from content.
- **O_m — near-margin outcome learner**: O trained only on accepted papers whose mean score lies in the bottom quartile of accepted papers that year — the ICLR analogue of "what lenient gatekeepers let in". Not random; reported as a diagnostic, not as ground truth.
- **L — zero-shot language model** (optional in v0): an open-weight model prompted with title and abstract to estimate the probability that the paper will be above the citation median; token probabilities, five paraphrased prompts, every call logged. Only submissions after the model's release date.

## 6. Ground truth for the rejected (outside the record)
- **Channel A — later publication and citations**: title match (exact, then normalized, then fuzzy with manual check of a sample) against OpenAlex; outcome = citations within the same window as accepted papers, measured from the ICLR decision date, not from the later publication date.
- **Channel B — resubmission inside ICLR**: a rejected paper whose title (or near-duplicate abstract) reappears in a later ICLR year, with its later decision. Observable without external data; selective, reported separately.
- **Never reappears**: about 71% of rejected papers never reappear in an indexed venue (Huang 2026). These are bounded: lower bound sets their outcome to zero citations; upper bound sets it to the outcome distribution of matched reappearing papers. Every headline number is reported as an interval between the two.

## 7. Scoring
- For each group g and learner, **signed error** = mean predicted outcome for rejected papers in g − observed (or bounded) outcome for rejected papers in g. Reported with bootstrap intervals and with the bound interval of section 6.
- **Decision learners** are scored on the decision page as usual (AUC) *and* on the rejected side: the share of rejected-in-g papers that D would also reject, compared with the share whose later outcome exceeds the accepted median — the organization's false-negative rate as D would reproduce it.
- **Dose**: by year, the gap between acceptance rates of group g and the rest (the height of the bar) is plotted against O's signed error for g.
- **Label line**: D vs D_J vs O ordering of signed error for the novel group.
- **Placebo**: the same table for the placebo groups.
- **Breakdown**: the share of never-reappearing papers that would have to exceed the accepted median for the sign of O's error to flip.

## 8. Reproducibility and logging
Scripts are numbered and declare inputs and outputs. `data/raw/MANIFEST.json` records every download (URL, license, date, size, SHA-256). Every model call writes one JSON line to `logs/`. Random seeds fixed. Derived tables under 10 MB are committed.

## 9. What v0 does not claim
No random assignment exists at ICLR, so O_m is not ground truth; the novelty and newcomer groups are proxies for the groups named in the proposal; and all outcome measures depend on title matching, whose failure rate is reported.

## 10. Additions v0.1 (2026-10-23; proposed by the AI assistant, pending author review)
- **O+ and O-.** The outcome learner is run with the group flag as an explicit input (O+) and without it (O-).
  O- is the configuration of Arnold, Dobbie & Hull (2025, *AER: Insights* 7(2):231–249), who scored an
  outcome-trained bail model against quasi-experimental ground truth and found that correcting for selection
  left the racial gap nearly unchanged. Theory (Rambachan & Roth 2020) locates reversal where the learner can see the group.
- **Common scale.** Decision and outcome learners are compared on percentile ranks among the evaluation year's
  rejected submissions (section 7 left the scale open).
- **Private information is relative to the reader.** In simulation (`results/sim_v0_summary.md`), removing reviewers'
  private information did not remove the reversal when the learner read the text coarsely; it did when the text was
  read nearly exactly. The condition test therefore also varies the reader (TF-IDF, sentence embeddings, a language
  model) on the same records: a better reader should shrink the reversal.
- Implemented in `code/05_learners.py`; `03_novelty.py` (embedding-based novelty) and `04_outcomes.py` (OpenAlex)
  are not yet written and wait on the author's approval of the downloads they require.
