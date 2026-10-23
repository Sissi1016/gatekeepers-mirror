# Signed error by group on the rejected side (sim_masked)

Train years 2017-2023; evaluation year 2024; rejected submissions in evaluation year: 1050; share matched to a later outcome: 0.302. Seed 20261023; bootstrap 200.

Signed error = mean percentile rank of the learner's score in the group minus mean percentile rank of the realized outcome in the group, among rejected submissions of the evaluation year. Positive: the learner places the group higher than its realized outcomes warrant. Columns are the truth bounds.

```
truth                   lower(unmatched=0)  matched_only  upper(unmatched~matched)
group          learner                                                            
newcomer_team  D                     0.003        -0.007                    -0.026
               D_J                   0.008        -0.021                    -0.021
               O+                    0.268         0.253                     0.239
               O-                    0.028         0.007                    -0.001
               O_m+                  0.346         0.337                     0.317
               O_m-                  0.005        -0.005                    -0.024
placebo_parity D                    -0.022        -0.033                    -0.015
               D_J                  -0.015        -0.020                    -0.007
               O+                   -0.010        -0.025                    -0.002
               O-                   -0.010        -0.025                    -0.002
               O_m+                 -0.083        -0.097                    -0.075
               O_m-                 -0.018        -0.031                    -0.010
```

## Fit on the page each learner was trained on

```
learner                             metric  value
      D             AUC accept (eval year)  0.741
    D_J          R2 mean score (eval year)  0.211
     O- R2 log cites, accepted (eval year)  0.078
   O_m- R2 log cites, accepted (eval year) -0.227
```
