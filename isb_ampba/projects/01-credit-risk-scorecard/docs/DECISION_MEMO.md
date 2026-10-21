# Decision memo - Card approval cut-off and limit policy
_Generated 2026-10-21 by `analysis/make_docs.py` from `outputs/summary.json` and `outputs/metrics.json`._

**Decision requested:** Approve the PD cut-off and limit actions below for new/review decisions on the card book.

**Recommendation:** Approve customers with PD <= 0.19 (score >= 529); apply the band actions A-F in the limit table.

**Impact (test set, 6,000 customers, assumptions margin 0.18, LGD 0.65, NT$->INR 2.6):**
- Approval rate 65.5%; bad rate among approved 10.7% vs 22.1% for approve-all.
- Expected profit INR 49.9 mn vs INR 2.8 mn approve-all -> uplift INR 47.0 mn (INR 7,841,063 per 1,000 applicants). Using actual outcomes the same policy earns INR 48.7 mn vs INR -4.1 mn for approve-all, so expected and realised profit agree in direction.
- Across LGD 0.45-0.85 x margin 0.10-0.26 the optimal cut-off ranges 0.11-0.36; the uplift stays positive in every cell (minimum INR 23.0 mn).
- Applying the band limit actions (A/B increase, C hold, D decrease, E/F decline) changes expected profit by INR 52.0 mn on the test book under the config assumptions (most of it from declining bands E/F; the pd_mult/limit-change effects are assumptions).

**Evidence:** champion xgb test AUC 0.7907, KS 0.4498, Gini 0.5815 vs baseline logit AUC 0.7243 and WOE scorecard AUC 0.7720; Brier 0.1312 (base-rate predictor 0.1723); calibration slope 1.012; top drivers max_delay, PAY_0, n_months_delayed, PAY_AMT1, LIMIT_BAL. Benchmark R1: AUC 0.783 / KS 0.424.

**Risks & limitations:** Taiwan 2005 data and a random split, so no out-of-time validation; margin and LGD are assumptions, not observed; only approved customers have outcomes in real life (no reject inference); fairness: disparate-impact minimum 0.952 (sex) and 0.853 (age) - both above the 0.8 screening threshold (heuristic, not a legal finding); age and limit remain possible proxies - review before use.

**Next steps:** 3-month shadow run on recent data; PSI monitor with alert at 0.2 (a -20% LIMIT_BAL shift gives feature PSI 0.222 for LIMIT_BAL, while the score PSI is only 0.019, so monitor features as well as the score); recalibrate quarterly.
