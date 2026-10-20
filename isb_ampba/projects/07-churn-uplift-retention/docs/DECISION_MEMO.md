# Decision memo - Who should get the retention offer?

**Decision requested:** Replace "contact the highest-risk customers" with "contact customers with the highest expected
incremental profit".

**Recommendation:** Run a 50/50 randomised pilot on real offers, fit an uplift model, then contact customers whose predicted
uplift x value exceeds the offer cost. Until a real pilot exists, treat every number below that depends on the offer's
effect as simulated.

**Impact (SIMULATED pilot; assumptions: gross margin 30%, offer cost ₹250, value horizon
12 months, INR/GBP 105; 30% budget for budgeted policies):**
- Uplift targeting earns ₹2,584,617 (92.3% of the oracle ceiling
  ₹2,801,136); risk-only top-30% earns ₹1,275,673 (45.5%);
  random ₹802,532 (28.7%).
- Honest caveat: at this low offer cost contacting *everybody* earns ₹2,751,518 (98.2% of
  oracle) - targeting matters when the offer is expensive relative to customer value (see the cost sweep in the README).
- Churn model: champion `logit`, test AUC 0.747 (target 0.75). Cost-optimal risk-only threshold
  0.01 contacts 1,374 of 1,471 customers.

**Evidence on real treatment data (Hillstrom e-mail test, 64000 customers):** Qini for 'visit' with the S-learner is 3,292,377 (95% CI 1,661,194 to 4,923,580; random 359,120). IPW profit per 1,000 customers (USD): uplift top-30% 21.8 (CI -25.4 to 65.6) vs random 3.1 (CI -64.7 to 57.0); the intervals overlap, so the real data do not separate these policies.

**Why "target the highest-risk" can lose money:** churn probability measures baseline risk, not responsiveness. Incremental
profit is `tau x value - cost`; the riskiest customers include inactive ("Hibernating") and low-value customers whose true
effect is small (mean true tau 0.023 vs 0.080 for mid-frequency customers in the
simulator). At offer costs of ₹5,000, ₹10,000 (base margin and CLV horizon) risk-top-30% has negative incremental profit; at the highest swept cost (₹10,000) risk-top-30% earns
₹-3.02m, contact-all ₹-11.59m, uplift targeting
₹0.10m. At the base cost risk-only is positive but captures only
46% of the oracle. All of this is *by construction of the simulator*: when the response
pattern is moved to high-frequency customers, risk-top-30% earns ₹488,714 (random: ₹508,049) while uplift targeting earns ₹942,597
(55% of that world's oracle), so the ranking of policies depends on the response
pattern, which only a real randomised pilot can reveal.

**Risks & limitations:**
- Pilot results are simulated (Track A); the 70%-of-oracle result holds only inside the simulator.
- Hillstrom is an e-mail experiment for a different business; effects are small and the CIs are wide.
- Margin, offer cost, FX and the 12-month value horizon are assumptions; seasonality moves churn between snapshots
  (calibration drifted: mean prediction 0.319 vs observed
  0.285) and test AUC is 0.747, below the 0.75 target.
- Test cohort has ~1,471 customers; uplift Qini intervals include zero.

**Next steps:** run a real 50/50 pilot (owner: CRM), log offers and outcomes, refit quarterly, monitor holdout Qini and
calibration, re-estimate the economics (offer cost, margin) before scaling.
