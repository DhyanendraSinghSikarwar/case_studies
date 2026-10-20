---

# Case Study 26 — Size and fit prediction from reviews (Flipkart) · `cs26_size_fit_returns.ipynb`

## D-26-01: Data source — synthetic orders, returns and reviews with a hidden fit mechanism

- Date: 2026-10-20
- Case: 26
- Context / question: We need orders, return reasons and review text, plus a known truth to measure label noise and the effect of a tip.
- Options considered: public fit-review sets (ModCloth and similar; US, no returns, no truth); synthetic data calibrated to the paper's Table 1.
- Decision: 476,048 clean orders over four categories, hidden body size and product offset, 50% of mismatches returned.
- Why: Label noise and a counterfactual tip test both need a hidden truth.
- Assumption checks / evidence: Simulated class shares within about 0.1 percentage point of the documented ones; 9.84% of orders truly mismatched.
- Impact if wrong / mitigation: The review signal strength and return share are assumptions; re-measure on real data.

## D-26-02: Label construction and noise — 'not returned = fit' is a noisy label

- Date: 2026-10-20
- Case: 26
- Context / question: How much does the reason-code label hide?
- Options considered: use reason codes as they are; audit with exchange data or a survey.
- Decision: Use the codes, report the noise, and plan a sampled audit.
- Why: 5.2% of the 'fit' class is truly mismatched, 4.0% of size returns have the wrong direction, labels carry the right class for 48% of true mismatches.
- Assumption checks / evidence: Chi-square across categories 1,648 (Cramér's V 0.042): class mix differs but little.
- Impact if wrong / mitigation: Real noise is unknown; every score has a ceiling set by it.

## D-26-03: Metric — rank with mAP and calibration, report macro-F1 with CIs

- Date: 2026-10-20
- Case: 26
- Context / question: Which metric when small and large are 2% to 5% of orders?
- Options considered: accuracy; macro-F1 on the argmax; mean average precision over small and large.
- Decision: mAP as the primary metric, macro-F1 for comparability with the paper, bootstrap CIs and Holm correction.
- Why: Always-fit scores macro-F1 0.325 and logistic regression 0.323; boosting with reviews 0.356 (CI 0.352 to 0.359) and mAP 0.175 against about 0.025 for random.
- Assumption checks / evidence: The class-balanced argmax predicts many false positives, so macro-F1 barely separates models.
- Impact if wrong / mitigation: Paper's macro-F1 (35.6 to 38.3) is on other data and not comparable.

## D-26-04: Model — gradient boosting with review features, no tuning

- Date: 2026-10-20
- Case: 26
- Context / question: Which model and feature set?
- Options considered: logistic and boosting, each with and without reviews; reviews only.
- Decision: Boosting on customer history, size gap, brand, fabric and review features.
- Why: Reviews add +0.008 mAP (CI +0.004 to +0.011; Holm p = 0.040); boosting beats logistic by +0.011 mAP.
- Assumption checks / evidence: Permutation: history and size gap 0.111, brand and fabric 0.088, ordered size 0.065, reviews 0.029.
- Impact if wrong / mitigation: Gain is under 5% relative; defaults only, so a tuned model may differ.

## D-26-05: Reviews and cold start — text helps only where reviews exist

- Date: 2026-10-20
- Case: 26
- Context / question: Do reviews help new customers and new products?
- Options considered: assume yes (the paper's claim); test by segment.
- Decision: Use review features only where a product has informative reviews; use history and brand otherwise.
- Why: Gain +0.014 with 5+ reviews, +0.016 with 1 to 4, -0.0003 with none; new customers +0.004 (CI -0.001 to +0.009), difference to returning p = 0.20.
- Assumption checks / evidence: Cold-start benefit for new customers not confirmed on this data.
- Impact if wrong / mitigation: Simulated reviews are cleaner than real text; check on real data.

## D-26-06: Review classifier — fit on platform tags, not public data

- Date: 2026-10-20
- Case: 26
- Context / question: Can a public labelled set train the review classifier?
- Options considered: public-only transfer; platform tags; both.
- Decision: Platform-trained classifier on cross-fitted tags.
- Why: Macro-F1 0.724 (public) vs 0.838 (platform); McNemar p = 4.6e-63; English-style text equal (0.789 vs 0.788).
- Assumption checks / evidence: Boosting with public-trained reviews has a higher macro-F1 (+0.0024) but lower mAP (-0.0037, Holm p = 0.050): a mixed picture.
- Impact if wrong / mitigation: The Hinglish gap (0.40 vs 1.00) is exaggerated by clean templates.

## D-26-07: Tip policy and ₹ case — calibrated cut-off, twin effect, pilot first

- Date: 2026-10-20
- Case: 26
- Context / question: How many ₹ crore does the tip save?
- Options considered: cut-off by validation net value; top 5% to 10% for trust.
- Decision: Platt-calibrate, pick the cut-off on validation, pilot at a higher cut-off.
- Why: Cut-off 0.06 flags 25.9% of orders at precision 12.7%; flagged size returns fall from 13.4% to 2.3% if followed; base ₹3.7 crore, worst -₹2.2 crore, best +₹10.6 crore a year.
- Assumption checks / evidence: Calibration ECE 0.0026 (small) and 0.0022 (large); top 1% precision 36.1%.
- Impact if wrong / mitigation: Costs, follow rate and the twin response are assumptions; the sign of the worst case is negative.

## D-26-08: A/B test — analyse triggered orders

- Date: 2026-10-20
- Case: 26
- Context / question: How do we prove it with a live test?
- Options considered: all orders; triggered orders only.
- Decision: Randomise among orders that would be flagged and analyse those.
- Why: A 20% relative drop in the flagged rate (24.3% control at top 5%) needs 1,131 flagged orders per arm (825 customers); all-order analysis needs 122,646.
- Assumption checks / evidence: Sample size cut by about a factor of five.
- Impact if wrong / mitigation: Real follow rate may be lower; check it in the pilot.
