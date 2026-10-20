---

# Case Study 29 — Penny-stock nudge: pre/post vs ITS vs DiD vs holdout (Zerodha) · `cs29_penny_stock_nudge_causal.ipynb`

## D-29-01: Data source — synthetic daily series with a control group, plus a user holdout

- Date: 2026-10-16
- Case: 29
- Context / question: We need penny trades by platform over time with a market confounder.
- Options considered: exchange aggregates (no broker or experience split); synthetic data.
- Decision: 386 trading days × web/Android/iOS + other brokers; 120k-user holdout study.
- Why: Lets the four methods be compared against a known truth.
- Assumption checks / evidence: Naive −62.5% vs truth −30%.
- Impact if wrong / mitigation: Method ranking transfers; magnitudes are illustrative.

## D-29-02: Synthetic parameters — boom-and-fade market, staggered rollout, −30% truth

- Date: 2026-10-16
- Case: 29
- Context / question: How should the confounding be built in?
- Options considered: stable market; boom then fade.
- Decision: Market peaks ~day 200 and fades. Launches at day 230/262/300. Effect −30%, ramping over 10 days.
- Why: It mirrors the 2020–21 small-cap cycle around the documented Aug 2020 launch.
- Assumption checks / evidence: Other brokers −46.8% over the same windows.
- Impact if wrong / mitigation: None.

## D-29-03: Pre/post and ITS — quasi-Poisson RR; segmented regression with Newey–West

- Date: 2026-10-16
- Case: 29
- Context / question: What do the simpler methods give?
- Options considered: report pre/post only; add ITS with and without a market control.
- Decision: All three.
- Why: To show the bias and the conditions under which ITS works.
- Assumption checks / evidence: Pre/post −62.5%; ITS −72% (no control); −20% (with control).
- Impact if wrong / mitigation: Never use pre/post through market turns.

## D-29-04: DiD and event study — each platform vs the never-treated control; date FE; cluster-by-week SEs

- Date: 2026-10-16
- Case: 29
- Context / question: What is the credible quasi-experimental estimate?
- Options considered: TWFE on all platforms (biased with staggered timing); per-platform vs never-treated, pooled by inverse variance.
- Decision: The second option, plus an event study with joint pre-trend tests and a platform-trend robustness check.
- Why: Avoids forbidden comparisons and absorbs the market completely.
- Assumption checks / evidence: Pooled −28.3% (−30.0, −26.5); pre-wobbles ≤ 6.4% (formal test rejects for Android/iOS); with trends −25% to −27%.
- Impact if wrong / mitigation: Report deviation sizes with p-values.

## D-29-05: Placebo tests

- Date: 2026-10-16
- Case: 29
- Context / question: Would the methods find fake effects?
- Options considered: none; fake launch dates; pre/post on the control.
- Decision: 9 DiD placebos and pre/post on other brokers.
- Why: A falsification check.
- Assumption checks / evidence: 8/9 ≈ 0 (one iOS +9.8% with a short pre-period); pre/post on the control finds −46.8%.
- Impact if wrong / mitigation: None.

## D-29-06: Randomised 5% holdout — ITT, RR, losses; MDE by holdout size

- Date: 2026-10-16
- Case: 29
- Context / question: What is the gold-standard estimate?
- Options considered: no holdout (documented); a small randomised holdout.
- Decision: Two-proportion z, Newcombe CI, log-RR CI, bootstrap loss difference; MDE table.
- Why: Removes all confounding; measures investor-protection ₹ directly.
- Assumption checks / evidence: −31.9% (−35.1, −28.6); ₹280 per user per quarter; a 2% holdout detects ~10%.
- Impact if wrong / mitigation: Keep holdouts small and time-limited (ethics).

## D-29-07: ₹ translation — investor losses avoided

- Date: 2026-10-16
- Case: 29
- Context / question: How much did investors save?
- Options considered: broker revenue; investor losses.
- Decision: 20 lakh first-time investors; average 90-day loss of penny traders from the holdout; ×4 quarters.
- Why: The documented "tens of crores saved" refers to investors.
- Assumption checks / evidence: Holdout ≈ ₹219 crore/yr; DiD ₹194 crore; pre/post ₹428 crore (≈ 2× overstated).
- Impact if wrong / mitigation: Linear in the assumptions.
