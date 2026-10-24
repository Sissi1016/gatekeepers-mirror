# Signed error by group on the rejected side (02_iclr_resub_2023)

Train years 2018-2022; evaluation year 2023; rejected submissions in evaluation year: 2226; share matched to a later outcome: 0.035. Seed 20261023; bootstrap 500.

Truth on the rejected side: acceptance at a later ICLR (2024 or 2025) among rejected 2023 submissions that were resubmitted; a later reviewers' judgment, selected by authors' persistence.

Signed error = mean percentile rank of the learner's score in the group minus mean percentile rank of the realized outcome in the group, among rejected submissions of the evaluation year. Positive: the learner places the group higher than its realized outcomes warrant. Columns are the truth bounds.

```
truth                     lower(unmatched=0)  matched_only  upper(unmatched~matched)
group            learner                                                            
newcomer_team    D                    -0.074        -0.059                    -0.023
                 D_J                  -0.105        -0.130                    -0.054
novel_q4         D                    -0.001         0.007                    -0.004
                 D_J                  -0.014         0.023                    -0.017
placebo_parity   D                    -0.002         0.016                     0.014
                 D_J                  -0.001         0.030                     0.015
placebo_title_am D                    -0.005         0.030                     0.038
                 D_J                  -0.004         0.102                     0.038
```

## Fit on the page each learner was trained on

```
learner                    metric  value
      D    AUC accept (eval year)  0.648
    D_J R2 mean score (eval year)  0.107
```
