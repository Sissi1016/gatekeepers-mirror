# Signed error by group on the rejected side (sim_hifi_noprivate)

Train years 2017-2023; evaluation year 2024; rejected submissions in evaluation year: 1050; share matched to a later outcome: 0.305. Seed 20261023; bootstrap 200.

Signed error = mean percentile rank of the learner's score in the group minus mean percentile rank of the realized outcome in the group, among rejected submissions of the evaluation year. Positive: the learner places the group higher than its realized outcomes warrant. Columns are the truth bounds.

```
truth                   lower(unmatched=0)  matched_only  upper(unmatched~matched)
group          learner                                                            
newcomer_team  D                    -0.046        -0.132                    -0.126
               D_J                   0.021        -0.040                    -0.059
               O+                    0.104         0.032                     0.023
               O-                    0.025        -0.047                    -0.055
               O_m+                  0.322         0.242                     0.242
               O_m-                  0.078         0.017                    -0.002
placebo_parity D                    -0.017        -0.006                    -0.029
               D_J                  -0.009        -0.021                    -0.021
               O+                    0.013        -0.009                     0.001
               O-                    0.010        -0.012                    -0.002
               O_m+                 -0.018        -0.040                    -0.030
               O_m-                  0.003        -0.020                    -0.009
```

## Fit on the page each learner was trained on

```
learner                             metric  value
      D             AUC accept (eval year)  0.969
    D_J          R2 mean score (eval year)  0.780
     O- R2 log cites, accepted (eval year)  0.537
   O_m- R2 log cites, accepted (eval year) -0.087
```
