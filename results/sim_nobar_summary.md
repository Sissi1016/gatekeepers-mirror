# Signed error by group on the rejected side (sim_nobar)

Train years 2017-2023; evaluation year 2024; rejected submissions in evaluation year: 1050; share matched to a later outcome: 0.304. Seed 20261023; bootstrap 200.

Signed error = mean percentile rank of the learner's score in the group minus mean percentile rank of the realized outcome in the group, among rejected submissions of the evaluation year. Positive: the learner places the group higher than its realized outcomes warrant. Columns are the truth bounds.

```
truth                   lower(unmatched=0)  matched_only  upper(unmatched~matched)
group          learner                                                            
newcomer_team  D                    -0.004        -0.061                    -0.014
               D_J                  -0.007        -0.089                    -0.017
               O+                    0.013        -0.014                     0.003
               O-                    0.004        -0.022                    -0.006
               O_m+                 -0.170        -0.147                    -0.180
               O_m-                 -0.026        -0.004                    -0.036
placebo_parity D                     0.000        -0.034                    -0.020
               D_J                   0.005        -0.035                    -0.015
               O+                    0.004        -0.023                    -0.016
               O-                    0.002        -0.025                    -0.019
               O_m+                  0.046         0.023                     0.026
               O_m-                 -0.003        -0.025                    -0.023
```

## Fit on the page each learner was trained on

```
learner                             metric  value
      D             AUC accept (eval year)  0.764
    D_J          R2 mean score (eval year)  0.243
     O- R2 log cites, accepted (eval year)  0.017
   O_m- R2 log cites, accepted (eval year) -0.154
```
