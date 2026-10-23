# Signed error by group on the rejected side (sim_noprivate)

Train years 2017-2023; evaluation year 2024; rejected submissions in evaluation year: 1050; share matched to a later outcome: 0.297. Seed 20261023; bootstrap 200.

Signed error = mean percentile rank of the learner's score in the group minus mean percentile rank of the realized outcome in the group, among rejected submissions of the evaluation year. Positive: the learner places the group higher than its realized outcomes warrant. Columns are the truth bounds.

```
truth                   lower(unmatched=0)  matched_only  upper(unmatched~matched)
group          learner                                                            
newcomer_team  D                    -0.077        -0.122                    -0.150
               D_J                  -0.072        -0.129                    -0.145
               O+                    0.251         0.174                     0.177
               O-                    0.124         0.031                     0.050
               O_m+                  0.354         0.289                     0.281
               O_m-                  0.111         0.063                     0.038
placebo_parity D                     0.005         0.010                     0.002
               D_J                  -0.000         0.026                    -0.003
               O+                    0.025         0.003                     0.022
               O-                    0.012        -0.009                     0.010
               O_m+                  0.005        -0.020                     0.002
               O_m-                  0.013        -0.013                     0.010
```

## Fit on the page each learner was trained on

```
learner                             metric  value
      D             AUC accept (eval year)  0.916
    D_J          R2 mean score (eval year)  0.561
     O- R2 log cites, accepted (eval year)  0.136
   O_m- R2 log cites, accepted (eval year) -0.308
```
