# Signed error by group on the rejected side (sim_hifi_base)

Train years 2017-2023; evaluation year 2024; rejected submissions in evaluation year: 1050; share matched to a later outcome: 0.297. Seed 20261023; bootstrap 200.

Signed error = mean percentile rank of the learner's score in the group minus mean percentile rank of the realized outcome in the group, among rejected submissions of the evaluation year. Positive: the learner places the group higher than its realized outcomes warrant. Columns are the truth bounds.

```
truth                   lower(unmatched=0)  matched_only  upper(unmatched~matched)
group          learner                                                            
newcomer_team  D                    -0.067        -0.061                    -0.044
               D_J                  -0.024        -0.013                    -0.000
               O+                    0.301         0.305                     0.325
               O-                    0.087         0.086                     0.110
               O_m+                  0.358         0.373                     0.382
               O_m-                  0.071         0.106                     0.094
placebo_parity D                     0.014         0.038                     0.026
               D_J                   0.015         0.039                     0.028
               O+                    0.020         0.052                     0.032
               O-                    0.012         0.044                     0.024
               O_m+                  0.056         0.065                     0.068
               O_m-                  0.008         0.017                     0.020
```

## Fit on the page each learner was trained on

```
learner                             metric  value
      D             AUC accept (eval year)  0.810
    D_J          R2 mean score (eval year)  0.367
     O- R2 log cites, accepted (eval year)  0.107
   O_m- R2 log cites, accepted (eval year) -0.244
```
