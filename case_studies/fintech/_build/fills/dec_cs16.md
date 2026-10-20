---

# Case Study 16 — Merchant QR lending and KYC name matching (BharatPe) · `cs16_merchant_qr_lending.ipynb`

## D-16-01: Data source — synthetic merchants, loans and labelled name pairs

- Date: 2026-10-16
- Case: 16
- Context / question: We need QR settlement histories, loan outcomes and KYC name pairs.
- Options considered: public data (none; NPCI aggregates only); synthetic data.
- Decision: 40k merchants × 15 months; 12k legacy loans; 30k labelled name pairs.
- Why: Confidential data; there are no labelled Indian name-pair datasets.
- Assumption checks / evidence: Legacy default 14.8%; median burden 0.175.
- Impact if wrong / mitigation: The method transfers; magnitudes are illustrative.

## D-16-02: Synthetic parameters — burden-driven default, shocks, name variants

- Date: 2026-10-16
- Case: 16
- Context / question: How do sizing and naming behave?
- Options considered: discrete legacy multipliers (tried first: no low-burden loans, so the curve could not be estimated); continuous 0.25–1.7×.
- Decision: Continuous multipliers. Default = f(true burden, quality, volatility). 6% future shocks. Name variants: initials, order, spelling, typos, honorifics, shop names; impostors with shared names.
- Why: Realistic spread and naming variety.
- Assumption checks / evidence: Burden bands from 3.6% to 31% default.
- Impact if wrong / mitigation: The true default function drives the digital twin (flagged).

## D-16-03: Forecasting — naive vs GBM vs quantile P20; Diebold–Mariano; coverage test

- Date: 2026-10-16
- Case: 16
- Context / question: How should future QR inflow be forecast?
- Options considered: last-3-month average; with trend; GBM; GBM quantile.
- Decision: All four, on a merchant hold-out.
- Why: The loan is repaid from future inflow; P20 expresses downside risk.
- Assumption checks / evidence: MdAPE 9.3% vs 10.8% (DM p ≈ 1e-146); P20 coverage 78.5%.
- Impact if wrong / mitigation: Shocks are unforecastable → daily monitoring.

## D-16-04: Burden–default curve and default model

- Date: 2026-10-16
- Case: 16
- Context / question: What drives merchant-loan default?
- Options considered: turnover; burden; full model.
- Decision: Burden bands with Wilson CIs + Cochran–Armitage; hinge logistic; GBM default model with DeLong vs burden.
- Why: Burden is the natural sizing lever.
- Assumption checks / evidence: Trend z = 21; no significant kink; model AUC 0.713 vs 0.673.
- Impact if wrong / mitigation: None.

## D-16-05: Limit policy — digital twin with bootstrap

- Date: 2026-10-16
- Case: 16
- Context / question: Which limit rule should be used?
- Options considered: legacy 1× QR; 10% naive cap; 10% P20 cap; P20 + risk tiers.
- Decision: Evaluate on all test-half merchants with the hidden true default function; profit = (1 − PD)·12%·A − PD·60%·A.
- Why: Counterfactuals require a twin; in production, a randomised test.
- Assumption checks / evidence: Risk-tiered +₹1,593 per merchant (CI 1,324–1,886); default 6.0%.
- Impact if wrong / mitigation: Validate with a randomised burden-cap test.

## D-16-06: Name matching — four matchers; two-zone policy (auto-accept / review)

- Date: 2026-10-16
- Case: 16
- Context / question: Which matcher and threshold should be used?
- Options considered: exact; token-sort; token-set (FuzzyWuzzy-style, re-implemented with difflib); hybrid with Jaro–Winkler + initials; three-zone with auto-reject (dropped).
- Decision: Auto-accept at the lowest threshold with ≤ 0.5% false accepts; review otherwise; no auto-reject.
- Why: A name mismatch should prompt checking, not refusal.
- Assumption checks / evidence: Hybrid AUC 0.984, 82.7% auto-accept, FA 0.05%; token-set scores 35 impostors at 100.
- Impact if wrong / mitigation: Re-tune on real penny-drop outcomes.

## D-16-07: ₹ translation

- Date: 2026-10-16
- Case: 16
- Context / question: How should results be expressed in ₹?
- Options considered: per merchant; scaled.
- Decision: Profit per 1 lakh merchants per cycle; name-check cost per 1 lakh disbursals (₹40 review, 5% drop-out, 60% wrong-payee loss).
- Why: Comparable business figures.
- Assumption checks / evidence: +₹15.9 crore vs legacy; hybrid ₹84 lakh vs exact ₹208 lakh.
- Impact if wrong / mitigation: Assumptions are explicit.
