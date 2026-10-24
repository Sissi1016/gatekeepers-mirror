# Group gaps on the decision page (ICLR 2018-2025)

Acceptance-rate gap = acceptance rate in the group minus outside it, among submissions with an accept or
reject decision. Withdrawal gap = withdrawal rate in the group minus outside it, among all submissions.
Gaps describe the record a learner sees; without random assignment they do not identify a threshold.
novel_q4 uses the provisional TF-IDF novelty (protocol deviation). Placebo groups should show no gap.

## Acceptance-rate gap

```
group  newcomer_team  novel_q4  placebo_parity  placebo_title_am
year                                                            
2018          -0.238       NaN          -0.013             0.006
2019          -0.176    -0.036           0.042             0.022
2020          -0.150    -0.016          -0.001            -0.003
2021          -0.136    -0.003          -0.017             0.009
2022          -0.209     0.045          -0.035            -0.034
2023          -0.216     0.015          -0.019            -0.003
2024          -0.205     0.037          -0.007            -0.016
2025          -0.201     0.002           0.003            -0.018
```

## Withdrawal-rate gap

```
group  newcomer_team  novel_q4  placebo_parity  placebo_title_am
year                                                            
2018           0.060       NaN          -0.011             0.036
2019           0.029    -0.009          -0.003             0.018
2020           0.066     0.010          -0.002             0.002
2021           0.028     0.004          -0.012            -0.000
2022           0.097    -0.021           0.012             0.010
2023           0.087    -0.022           0.020             0.002
2024           0.059    -0.012           0.006            -0.006
2025           0.070    -0.012          -0.005             0.003
```

Full table with standard errors and standardized scores: `01_group_gaps.csv`.
