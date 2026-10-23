# Simulation v0: does the pipeline recover the predicted signs?

Date 2026-10-23. Synthetic data from `code/sim/make_synthetic.py` (one seed per scenario; 1,500 submissions a year,
2017–2024; train 2017–2023, score the 2024 rejected). True group effect on outcomes is zero in every scenario.
Learners and scoring from `code/05_learners.py`; the column shown uses matched rejected papers only (about 30%).
Cells: signed error on the percentile-rank scale with a 95% bootstrap interval (200 draws). Positive = the
learner ranks the group above its realized outcomes. O+ sees the group flag; O- does not.

| scenario | bar gap | private share | group visible in text | text fidelity |
|---|---|---|---|---|
| base | 0.6 | 0.5 | 0.8 | low |
| noprivate | 0.6 | 0.0 | 0.8 | low |
| hifi_base | 0.6 | 0.5 | 0.8 | high |
| hifi_noprivate | 0.6 | 0.0 | 0.8 | high |
| masked | 0.6 | 0.5 | 0.0 | low |
| nobar | 0.0 | 0.5 | 0.8 | low |

```
scenario                                 base              noprivate              hifi_base         hifi_noprivate                 masked                  nobar
group          learner                                                                                                                                          
newcomer_team  D        -0.152 [-0.21, -0.08]  -0.122 [-0.19, -0.05]  -0.061 [-0.14, +0.00]  -0.132 [-0.19, -0.08]  -0.007 [-0.10, +0.07]  -0.061 [-0.15, +0.02]
               D_J      -0.096 [-0.15, -0.03]  -0.129 [-0.18, -0.08]  -0.013 [-0.08, +0.06]  -0.040 [-0.08, -0.00]  -0.021 [-0.08, +0.04]  -0.089 [-0.16, +0.01]
               O+       +0.246 [+0.20, +0.30]  +0.174 [+0.12, +0.24]  +0.305 [+0.25, +0.37]  +0.032 [-0.09, +0.13]  +0.253 [+0.20, +0.30]  -0.014 [-0.10, +0.06]
               O-       +0.091 [+0.03, +0.16]  +0.031 [-0.05, +0.09]  +0.086 [+0.02, +0.17]  -0.047 [-0.16, +0.05]  +0.007 [-0.05, +0.08]  -0.022 [-0.10, +0.06]
               O_m+     +0.307 [+0.26, +0.36]  +0.289 [+0.23, +0.35]  +0.373 [+0.32, +0.42]  +0.242 [+0.18, +0.31]  +0.337 [+0.27, +0.38]  -0.147 [-0.22, -0.08]
               O_m-     +0.046 [-0.03, +0.11]  +0.063 [-0.01, +0.12]  +0.106 [+0.03, +0.18]  +0.017 [-0.07, +0.12]  -0.005 [-0.08, +0.06]  -0.004 [-0.08, +0.08]
placebo_parity D        -0.009 [-0.07, +0.04]  +0.010 [-0.04, +0.06]  +0.038 [-0.01, +0.09]  -0.006 [-0.05, +0.04]  -0.033 [-0.09, +0.03]  -0.034 [-0.09, +0.02]
               D_J      -0.008 [-0.06, +0.04]  +0.026 [-0.02, +0.06]  +0.039 [+0.00, +0.09]  -0.021 [-0.05, +0.00]  -0.020 [-0.07, +0.04]  -0.035 [-0.09, +0.03]
               O+       +0.014 [-0.04, +0.06]  +0.003 [-0.04, +0.05]  +0.052 [+0.01, +0.10]  -0.009 [-0.07, +0.06]  -0.025 [-0.09, +0.03]  -0.023 [-0.08, +0.04]
               O-       +0.004 [-0.05, +0.07]  -0.009 [-0.05, +0.04]  +0.044 [-0.00, +0.10]  -0.012 [-0.07, +0.05]  -0.025 [-0.07, +0.03]  -0.025 [-0.10, +0.04]
               O_m+     +0.122 [+0.07, +0.18]  -0.020 [-0.07, +0.04]  +0.065 [+0.02, +0.13]  -0.040 [-0.11, +0.03]  -0.097 [-0.14, -0.05]  +0.023 [-0.04, +0.08]
               O_m-     +0.014 [-0.05, +0.07]  -0.013 [-0.07, +0.03]  +0.017 [-0.04, +0.07]  -0.020 [-0.09, +0.05]  -0.031 [-0.08, +0.03]  -0.025 [-0.09, +0.05]
```

## Reading
- With a higher bar and private information (base), the decision learner D ranks the group too low (inheritance)
  and the outcome learner O+ ranks it too high (reversal); in that scenario the placebo group shows no error for
  D, D_J, O+ or O-. Across all six scenarios, 2 of these 24 placebo cells have intervals that just exclude zero
  (hifi_base: D_J +0.039, O+ +0.052), which a single seed cannot distinguish from chance.
- With the group invisible to the learner (masked), O- shows no reversal although O+ still does. This is the
  configuration of Arnold, Dobbie & Hull (2025), who found that correcting for selection left the racial gap nearly unchanged.
- Without a bar gap (nobar), O+ shows no reversal.
- Removing reviewers' private information is not enough when the learner reads the text coarsely (noprivate: O+ still
  +0.17). When the text is read nearly exactly (hifi_noprivate), the reversal disappears (+0.03, interval includes zero);
  with private information it remains (hifi_base: +0.31). Private information is relative to what the learner can read,
  not to what the record contains. Implication for the condition test: holding the record fixed, a better reader
  should shrink the reversal.
- O_m (trained only on the bottom score quartile of accepted papers) is unstable with an explicit group flag (placebo
  errors of up to ±0.12); it stays a diagnostic, as the protocol says.

## Limits
One seed per scenario; a bag-of-words generator; truth known exactly. Before any table enters the proposal,
each scenario is rerun over at least 50 seeds.
