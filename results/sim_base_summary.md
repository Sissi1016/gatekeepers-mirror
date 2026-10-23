# Signed error by group on the rejected side (sim_base)

Train years 2017-2023; evaluation year 2024; rejected submissions in evaluation year: 1050; share matched to a later outcome: 0.322. Seed 20261023; bootstrap 200.

Signed error = mean percentile rank of the learner's score in the group minus mean percentile rank of the realized outcome in the group, among rejected submissions of the evaluation year. Positive: the learner places the group higher than its realized outcomes warrant. Columns are the truth bounds.

```
truth                   lower(unmatched=0)  matched_only  upper(unmatched~matched)
group          learner                                                            
newcomer_team  D                    -0.125        -0.152                    -0.139
               D_J                  -0.095        -0.096                    -0.109
               O+                    0.267         0.246                     0.253
               O-                    0.110         0.091                     0.096
               O_m+                  0.332         0.307                     0.318
               O_m-                  0.083         0.046                     0.069
placebo_parity D                     0.004        -0.009                     0.040
               D_J                   0.001        -0.008                     0.038
               O+                    0.000         0.014                     0.037
               O-                   -0.010         0.004                     0.027
               O_m+                  0.099         0.122                     0.136
               O_m-                 -0.012         0.014                     0.024
```

## Fit on the page each learner was trained on

```
learner                             metric  value
      D             AUC accept (eval year)  0.750
    D_J          R2 mean score (eval year)  0.236
     O- R2 log cites, accepted (eval year)  0.015
   O_m- R2 log cites, accepted (eval year) -0.146
```
