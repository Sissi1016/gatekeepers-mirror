# Decision log (human decisions, dated)

- 2026-10-22 — Main testbed for the project is drunk-driving probation in courts with random case
  assignment (not public here); ICLR is the fully public testbed. Decision by the author.
- 2026-10-22 — Submit this project, not a sister project, to the special issue; start the ICLR
  prototype and this public repository. Decision by the author.
- 2026-10-23 — Data via licensed mirrors (berenslab, reviewarena) because the OpenReview API returns
  `ChallengeRequiredError` to scripts; confirmed by direct test on 2026-10-23.
- 2026-10-23 — Novelty boundary to be re-checked before results are framed: Arnold, Dobbie & Hull (2025, AER: Insights 7(2)) already score an outcome-trained bail model against selection-corrected ground truth by race and find inheritance. The prototype's headline will be set after the citation-chain check.
- 2026-10-23 — Download of `iclr26v1.parquet`, OpenAlex outcome queries and the sentence-encoder weights not yet
  approved by the author; the learners and scoring were written and tested on synthetic data only
  (`code/sim/make_synthetic.py`, `results/sim_v0_summary.md`). No ICLR data have been read.
- 2026-10-23 — Novelty boundary checked against citation chains of Arnold, Dobbie & Hull (2025) and Rambachan &
  Roth (2020). Additions v0.1 to the protocol (O+/O-, common rank scale, reader as a factor) proposed by the AI
  assistant and pending the author's review (protocol section 10).
- 2026-10-24 — Author approved downloading `iclr26v1.parquet` (stored in data/raw, copied to the project's
  Dropbox). OpenAlex queries and the sentence-encoder download remain unapproved.
- 2026-10-24 — Pipeline fixes after reading the data (proposed by the AI assistant; see
  `results/03_first_look.md`): author strings split into names; newcomer flag by name for all years, 2017
  excluded; "Invite to Workshop Track" coded as reject; TF-IDF novelty excluding co-authored neighbours
  (protocol deviation pending approval of the encoder); ICLR-internal resubmission matcher with thresholds fixed
  before inspecting outcomes. The resubmission channel proved too thin to score learners (77 matched rejected
  papers in 2023), so no signed-error result is reported yet.
