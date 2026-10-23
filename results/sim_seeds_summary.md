# Simulation across seeds (Appendix C)

30 seeds per scenario; 1000 submissions a year; matched-only truth; cells = mean signed error [2.5th, 97.5th percentile across seeds]. Scenario settings as in `sim_v0_summary.md`.

```
scenario                                 base              noprivate              hifi_base         hifi_noprivate                 masked                  nobar
group          learner                                                                                                                                          
newcomer_team  D        -0.156 [-0.22, -0.10]  -0.113 [-0.19, -0.04]  -0.096 [-0.15, -0.06]  -0.100 [-0.17, -0.04]  -0.019 [-0.10, +0.09]  +0.012 [-0.07, +0.08]
               D_J      -0.126 [-0.18, -0.05]  -0.099 [-0.18, -0.04]  -0.064 [-0.12, -0.02]  -0.029 [-0.08, +0.03]  -0.012 [-0.09, +0.09]  +0.010 [-0.05, +0.08]
               O+       +0.216 [+0.15, +0.28]  +0.214 [+0.15, +0.27]  +0.240 [+0.20, +0.33]  -0.009 [-0.15, +0.13]  +0.226 [+0.15, +0.30]  +0.001 [-0.08, +0.10]
               O-       +0.044 [-0.03, +0.12]  +0.071 [+0.00, +0.13]  +0.032 [-0.01, +0.10]  -0.062 [-0.16, +0.06]  -0.016 [-0.10, +0.07]  -0.000 [-0.07, +0.09]
               O_m+     +0.293 [+0.25, +0.34]  +0.296 [+0.25, +0.35]  +0.303 [+0.25, +0.36]  +0.204 [+0.03, +0.30]  +0.304 [+0.24, +0.36]  +0.019 [-0.22, +0.25]
               O_m-     +0.037 [-0.05, +0.10]  +0.050 [-0.01, +0.16]  +0.026 [-0.04, +0.10]  -0.017 [-0.10, +0.09]  -0.023 [-0.12, +0.06]  +0.001 [-0.09, +0.09]
placebo_parity D        +0.003 [-0.06, +0.06]  +0.003 [-0.06, +0.04]  +0.011 [-0.03, +0.05]  +0.002 [-0.03, +0.05]  +0.004 [-0.05, +0.04]  -0.000 [-0.05, +0.06]
               D_J      +0.002 [-0.05, +0.04]  -0.005 [-0.05, +0.04]  +0.012 [-0.04, +0.06]  +0.004 [-0.03, +0.04]  +0.004 [-0.05, +0.05]  -0.000 [-0.05, +0.05]
               O+       -0.002 [-0.06, +0.06]  +0.003 [-0.05, +0.06]  +0.009 [-0.07, +0.07]  -0.004 [-0.06, +0.07]  +0.001 [-0.06, +0.05]  -0.001 [-0.05, +0.07]
               O-       -0.000 [-0.05, +0.04]  +0.002 [-0.03, +0.03]  +0.014 [-0.06, +0.07]  -0.004 [-0.07, +0.07]  +0.003 [-0.04, +0.04]  +0.004 [-0.04, +0.06]
               O_m+     +0.014 [-0.12, +0.15]  +0.039 [-0.10, +0.15]  +0.009 [-0.13, +0.13]  -0.024 [-0.11, +0.09]  -0.012 [-0.14, +0.12]  +0.016 [-0.14, +0.21]
               O_m-     +0.001 [-0.05, +0.06]  +0.009 [-0.04, +0.06]  +0.020 [-0.04, +0.07]  -0.002 [-0.08, +0.08]  +0.010 [-0.04, +0.07]  +0.002 [-0.04, +0.06]
```
## Reading across seeds
- Base (higher bar, private information): D ranks the group too low (-0.16), O+ too high (+0.22); placebo means are
  within ±0.02 for every learner in every scenario.
- Private information is relative to the reader. With a coarse reading of the text, removing reviewers' private
  information leaves the reversal intact (noprivate: +0.21). With a near-exact reading it disappears
  (hifi_noprivate: -0.01, range -0.15 to +0.13); with private information it remains (hifi_base: +0.24).
- Group invisible to the learner (masked): O- shows no reversal (-0.02), the configuration of Arnold, Dobbie &
  Hull (2025). No bar gap (nobar): every learner is within ±0.02.
- O_m+ reverses even with no private information and a near-exact reading (+0.20). Training only on accepted
  papers with low reviewer scores conditions on a rating that is itself biased against the group, which reopens the
  collider. O_m therefore remains a diagnostic and is not a correction.
