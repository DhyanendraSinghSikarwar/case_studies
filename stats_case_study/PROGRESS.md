# Build progress

Cases are built strictly one at a time. A case is **COMPLETE** only after its notebook executed end-to-end without
errors, its figures, tables and deck were regenerated from that run, and its content was reviewed for statistical,
code, business, educational and presentation correctness.

Statuses: NOT STARTED · IN PROGRESS · ANALYSIS COMPLETE · PRESENTATION COMPLETE · VALIDATION IN PROGRESS · COMPLETE

| Case | Title | Status | Notebook | Data | Figures | Presentation | Validation |
|---|---|---|---|---|---|---|---|
| 01 | Personal-loan portfolio health check | COMPLETE | ✅ | ✅ | ✅ (8) | ✅ (15 slides) | ✅ |
| 02 | Do higher earners default less? | COMPLETE | ✅ | ✅ | ✅ (5) | ✅ (14 slides) | ✅ |
| 03 | Did the email campaign increase conversions? | COMPLETE | ✅ | ✅ | ✅ (5) | ✅ (12 slides) | ✅ |
| 04 | Designing and reading a checkout A/B test | COMPLETE | ✅ | ✅ | ✅ (5) | ✅ (13 slides) | ✅ |
| 05 | Card utilisation and spending: correlation | COMPLETE | ✅ | ✅ | ✅ (6) | ✅ (11 slides) | ✅ |
| 06 | Predicting loan amount from income | COMPLETE | ✅ | ✅ | ✅ (6) | ✅ (9 slides) | ✅ |
| 07 | What drives the loan amount a customer requests? | COMPLETE | ✅ | ✅ | ✅ (5) | ✅ (11 slides) | ✅ |
| 08 | Why did "work experience" stop mattering? | COMPLETE | ✅ | ✅ | ✅ (10) | ✅ (12 slides) | ✅ |
| 09 | Overlapping risk signals: multicollinearity | COMPLETE | ✅ | ✅ | ✅ (8) | ✅ (10 slides) | ✅ |
| 10 | Modelling insurance claim cost | COMPLETE | ✅ | ✅ | ✅ (10) | ✅ (12 slides) | ✅ |
| 11 | Which customers are about to churn? | COMPLETE | ✅ | ✅ | ✅ (6) | ✅ (11 slides) | ✅ |
| 12 | Card transaction fraud detection | COMPLETE | ✅ | ✅ | ✅ (6) | ✅ (11 slides) | ✅ |
| 13 | Is a machine-learning model worth it? | COMPLETE | ✅ | ✅ | ✅ (8) | ✅ (14 slides) | ✅ |
| 14 | Which acquisition channel brings the most valuable customers? | COMPLETE | ✅ | ✅ | ✅ (5) | ✅ (10 slides) | ✅ |
| 15 | Branch loan processing times and a new workflow | COMPLETE | ✅ | ✅ | ✅ (4) | ✅ (10 slides) | ✅ |
| 16 | Payment processing outliers | COMPLETE | ✅ | ✅ | ✅ (6) | ✅ (12 slides) | ✅ |
| 17 | The missing income problem | COMPLETE | ✅ | ✅ | ✅ (6) | ✅ (12 slides) | ✅ |
| 18 | Customer satisfaction survey: who did we hear from? | COMPLETE | ✅ | ✅ | ✅ (5) | ✅ (12 slides) | text checked against outputs; all slides visually reviewed and layout issues fixed |
| 19 | Testing a campaign across 40 segments | COMPLETE | ✅ | ✅ | ✅ (5) | ✅ (11 slides) | text checked against outputs; all slides visually reviewed and layout issues fixed |
| 20 | Did the new approval policy hurt approval rates? | COMPLETE | ✅ | ✅ | ✅ (4) | ✅ (10 slides) | ✅ |
| 21 | Does cashback reduce churn? | COMPLETE | ✅ | ✅ | ✅ (3) | ✅ (11 slides) | text checked against outputs; all slides visually reviewed and layout issues fixed |
| 22 | Significant but irrelevant; non-significant but promising | COMPLETE | ✅ | ✅ | ✅ (6) | ✅ (12 slides) | text checked against outputs; all slides visually reviewed and layout issues fixed |
| 23 | Credit-limit increase and spend: bootstrap | COMPLETE | ✅ | ✅ | ✅ (4) | ✅ (11 slides) | text checked against outputs; all slides visually reviewed and layout issues fixed |
| 24 | A fraud alert fired: Bayes and base rates | COMPLETE | ✅ | ✅ | ✅ (5) | ✅ (11 slides) | text checked against outputs; all slides visually reviewed and layout issues fixed |
| 25 | Monthly digital-payments volume: time series | NOT STARTED | - | - | - | - | - |
| 26 | Collections and SLA: time-to-event | NOT STARTED | - | - | - | - | - |
| 27 | Capstone: loan default drivers | NOT STARTED | - | - | - | - | - |
| — | Final summary (cheat sheet, decision framework) | NOT STARTED | - | - | - | - | - |

## Log

- **2026-10-04:** Repository scaffolding, roadmap README, shared resources. Case 01 started.
- **2026-10-04:** Case 01 COMPLETE. Notebook (93 cells) executed end-to-end with no errors or warnings; data
  generator verified byte-for-byte reproducible; every number quoted in markdown, README and deck cross-checked
  against executed outputs (deck numbers are read from saved tables); all 95% CIs contain the answer-key truth;
  figures visually reviewed (label collisions fixed); deck proofread and checked for text overflow.
- **2026-10-04:** Case 02 COMPLETE. Notebook (56 cells) executed end-to-end, no errors/warnings; data reproducible;
  markdown, README and deck cross-checked against outputs (band rates, chi-square, Welch/log/MW results, floor
  economics, bootstrap CI, sensitivity grid); recommendation made explicitly conditional on Finance's margin
  assumption after the sensitivity grid showed the floor pays at a 9% margin.
- **2026-10-04:** Case 03 COMPLETE. Notebook (47 cells) executed cleanly; data reproducible. The design was
  recalibrated to a documented 86%-power setting, and the random stream was chosen by a documented,
  outcome-neutral rule (most typical realised lift; rationale in the generator). Numbers cross-checked against
  outputs; figure overlaps fixed; deck rounding artefact fixed. Shared `save_table` now keeps 10 decimals.
- **2026-10-13:** Case 04 COMPLETE. Notebook (43 cells) executed cleanly; data reproducible; numbers cross-checked
  (sample size, peeking FPR, SRM diagnosis, v5+ lift and CI, guardrail, revenue); figure overlaps fixed.
- **2026-10-13:** New **Case 13 "Is a machine-learning model worth it?"** added at the user's request; former
  cases 13–26 renumbered 14–27 (README, PROGRESS and cross-references in cases 01–04 updated).
- **2026-10-13:** Case 13 COMPLETE (built ahead of 05–12 at the user's request). Notebook (78 cells) executed cleanly
  with no warnings (robust logit fitting added after a convergence warning); data reproducible; tests recovered the
  true structure (splines, interaction, proxy, noise, leakage); interpretation corrected after review, so the GBM's value
  gain is reported as "about equal to its cost, coin-flip" rather than "far below"; deck proofread.
  Shared module gained `delong_test`, `corrected_resampled_ttest` and `psi`.
- **2026-10-13:** Case 05 COMPLETE. Notebook (43 cells) executed cleanly; data reproducible; generator adjusted twice
  during design so the limit genuinely binds for a minority (revolvers), giving the naive vs true limit-effect contrast
  (+27% vs +1.5%, via a teaching answer key); text corrected against outputs (0.91 levels r; age as the
  "significant but negligible" example).
- **2026-10-13:** Case 06 COMPLETE. Notebook (46 cells) executed cleanly; data reproducible; diagnostic-helper indexing
  bug fixed; interpretation corrected after review (only 2 of 4 capped earners in training; raw-model holdout coverage
  is 90% overall, not "similar"; elasticity 0.92). Kernel start-up timeout raised because another project's processes
  were loading the machine.
- **2026-10-13:** Case 07 COMPLETE. Notebook (41 cells) executed cleanly; data reproducible; log income centred at ₹50k
  after review (so interaction-model dummies are interpretable); profile-prediction alignment bug fixed; text
  corrected against outputs. Shared deck builder now renders minus signs properly.
- **2026-10-14:** Case 08 COMPLETE. Notebook (45 cells) executed cleanly; data reproducible; numbers cross-checked
  against outputs (postgraduate premium corrected to +21%/+9%; government/PSU metro gap reported honestly as surviving
  Bonferroni). Within-grade figure switched to salary adjusted for tenure etc., because raw within-grade slopes are
  negative (tenure is omitted there): itself documented as a teaching point.
- **2026-10-14:** Case 09 COMPLETE. Notebook (34 cells) executed cleanly; data reproducible; text cross-checked
  against outputs. Review found that CV-tuned ridge does NOT stabilise the coefficients here (small penalty), that
  statsmodels silently returns ±34-billion coefficients for an exactly redundant column, and that the 6% gap between
  quarterly predictions is ordinary refitting noise (same for a collinearity-free model); all now taught explicitly.
- **2026-10-16:** Case 10 COMPLETE. Notebook (39 cells) executed cleanly; data reproducible; text cross-checked
  against outputs. Review corrected the draft: Box-Cox picks λ ≈ 0.15 (not 0; gamma-like data), raw OLS's holdout total
  is no worse than uncapped gamma, and the decisive improvement is applying the sum-insured cap (total error −0.1%).
- **2026-10-16:** Case 11 COMPLETE. Notebook (37 cells) executed cleanly; data reproducible; text cross-checked
  against outputs. Review changed the draft: the complaints × salary-account interaction is not significant
  (LR p = 0.09) and was dropped from the final model; the "adjusted vs raw" complaint effect is explained as
  non-collapsibility of odds ratios (no confounding), with percentage-point effects unchanged.
- **2026-10-17:** Case 12 COMPLETE. Notebook (34 cells) executed cleanly; data reproducible; text cross-checked
  against outputs. Review fixed a bug in the prevalence experiment (negatives were capped, so the "0.1%" row was really
  0.5%), an f-string incompatible with the kernel's Python, and the drift chart (now excess counts, not ratios on tiny
  groups). Text now states that the expected-loss policy's edge over probability ranking is within noise.
- **2026-10-17:** Case 14 COMPLETE. Notebook (33 cells) executed cleanly; data reproducible; text cross-checked against
  outputs. Review corrected the draft: the planned contrast (digital vs offline) is NOT significant (CI includes 0), the
  partner channel is significantly better than branch at the same income, and the aggregator's raw advantage is not
  statistically reliable.
- **2026-10-17:** Case 15 COMPLETE. Notebook (24 cells) executed cleanly; data reproducible; text cross-checked against
  outputs. Review corrected the draft count (18, not 19, of 20 officers faster) and the power-simulation wording (the
  t-test is conservative, not just weak, with outliers).
- **2026-10-17:** Case 16 COMPLETE. Notebook (38 cells) executed cleanly; data reproducible; text cross-checked against
  outputs. Review corrected the draft: the dashboard's flags are 60% harmless (not "a third"), iterated z-scores show both
  masking and swamping, VIP/festival "recall" is low by design (they should not alert), each robust estimator is now
  compared with its own clean-sample target, and a deck bug (wrong correlation column) was caught by reading the slides.
- **2026-10-17:** Case 20 COMPLETE. Notebook executed cleanly; text cross-checked against outputs. Review found that the Breslow-Day test rejects a common odds ratio (the effect looks stronger in band A on the odds scale) while the risk-difference effect is homogeneous (Cochran Q p = 0.71); both are now taught as a scale-dependence lesson.
- **2026-10-17:** Case 17 COMPLETE. Notebook executed cleanly; text cross-checked against outputs. Review found that a single dataset misled (complete cases and MI-with-outcome both covered the truth), so a 150-dataset repeated-sampling simulation was added: only MI with the outcome in the imputation model keeps near-nominal coverage (91%).
- **2026-10-19:** Case 18 notebook re-executed cleanly (no errors/warnings). Its commentary had been drafted before the outputs existed (NPS +18, weighted mean about 7.5, design effect 2–3, two "written after" placeholders); rewritten against the executed numbers. Key honest finding: weighting removes only ~30% of the bias (+0.80 → +0.55), no interval covers the truth, and the reachable 60% of the phone follow-up (7.28) is happier than all non-respondents (7.03). README and 12-slide deck added. **Housekeeping:** cases 19, 22, 23, 24 have executed notebooks, figures and tables on disk but no README/deck (19, 22 and 23 have no or partial decks) and have not been through this review; case 21 has data only. PROGRESS rows for those stay NOT STARTED until reviewed.
- **2026-10-20:** Cases 19, 22, 23, 24 reviewed. 19: commentary rewritten (7 winners not 9; pooled uplift +0.22 pp not +0.6; BH 5% keeps 2 not 8; MDE 1.65/2.4 pp; grading table written), notebook re-executed, deck text fixed, README added. 22: SRM/rate wording and two recommendation errors fixed (cheaper-build break-even is about ₹10 lakh, not ₹20 lakh; a 4,000-per-arm follow-up is not powered for the break-even lift, about 7,000 is needed). 23: the pending grading text written (BCa covers 7 of 7 in the main test, 4 of 7 in the pilot). 24: numbers verified as consistent, README and deck added. Decks and READMEs created for all four.
- **2026-10-20:** Case 21 built from the existing data and generator: notebook (35 cells) executed cleanly, README and 11-slide deck added. Findings: naive gap −19.4 pp; adjustment ladder −16.1 → −9.6 → −7.0 and propensity weighting −6.2 (all with intervals that miss the true −4.3); pilot complier effect −4.1 (CI −6.1 to −2.0) and ITT −2.3 both cover their truths; at a 7.5 pp break-even cashback is profitable on the naive number and loss-making on the real one.
- **2026-10-21:** Cases 18, 19, 21, 22, 23, 24 visually reviewed slide by slide (68 slides rendered through PowerPoint). Fixed: overlapping figure labels (18, 21), aliasing histogram bins (22), minor tick labels and an over-broad title (23), clearer takeaways (18, 19, 24), pandas warning in 23. Notebooks 18, 21, 22, 23 re-executed cleanly with the figure fixes (the kernel launch failure was the Windows Store python alias; fixed with a dedicated kernel spec), decks rebuilt. All six marked COMPLETE.
