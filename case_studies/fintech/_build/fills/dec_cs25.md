---

# Case Study 25 — Evaluating an AI claims copilot (ICICI Lombard) · `cs25_claims_copilot_evaluation.ipynb`

## D-25-01: Data source — simulated evaluation records for three study parts

- Date: 2026-10-16
- Case: 25
- Context / question: What data does an evaluation of the copilot need?
- Options considered: public medical-text sets (US, restricted); simulate evaluation records.
- Decision: Extraction audit (4k claims × 8 fields), randomised productivity study (6k claims, 60 adjudicators, 10% gold audit), guideline-flag check (1.5k).
- Why: Confidential claims data; the evaluation design is what transfers.
- Assumption checks / evidence: Extraction 92%; time ratio 0.56.
- Impact if wrong / mitigation: Re-run on real pilot data.

## D-25-02: Synthetic parameters — document-quality errors, summary errors, automation bias

- Date: 2026-10-16
- Case: 25
- Context / question: What are the realistic failure modes?
- Options considered: uniform errors; quality-driven extraction errors plus summary errors that anchor adjudicators.
- Decision: The second.
- Why: Documented "decision support" risk.
- Assumption checks / evidence: Wrong-summary accuracy 74% vs 86%.
- Impact if wrong / mitigation: Effects assumed.

## D-25-03: Extraction audit — Wilson CIs, logistic LR test, confidence and selective review

- Date: 2026-10-16
- Case: 25
- Context / question: How accurate is extraction, and can the model flag its own errors?
- Options considered: accuracy only; per-field with calibration of confidence.
- Decision: Per-field Wilson CIs; error model on quality/pages; confidence AUC and flag thresholds.
- Why: Human checking effort must be targeted.
- Assumption checks / evidence: 92.1% per field; only 56.9% of claims fully correct; AUC 0.92; flag < 0.7 → 21% flagged, 84% of errors caught.
- Impact if wrong / mitigation: None.

## D-25-04: Randomised time comparison — mixed model with adjudicator effect

- Date: 2026-10-16
- Case: 25
- Context / question: Is the time saving real?
- Options considered: before/after; unadjusted t-test; randomised, clustered mixed model.
- Decision: Log-time mixed model with adjudicator random intercept; Mann–Whitney and bootstrap medians as checks.
- Why: Adjudicators differ in speed.
- Assumption checks / evidence: Ratio 0.56 (CI 0.55–0.57); 1.8× productivity; SRM p = 0.036 handled by adjustment.
- Impact if wrong / mitigation: None.

## D-25-05: Decision quality — non-inferiority at 2 pp (gold sample and full truth)

- Date: 2026-10-16
- Case: 25
- Context / question: Are decisions as good?
- Options considered: accuracy vs gold; vs hidden truth.
- Decision: Newcombe CI vs a −2 pp margin on both; by complexity; disputes (Holm).
- Why: Quality is the regulator's concern.
- Assumption checks / evidence: Gold sample CI −5.2 to +7.2 (not shown); full truth −1.7 to +2.0 (non-inferior).
- Impact if wrong / mitigation: Larger audits needed (≈ 4,000/arm).

## D-25-06: Automation bias and guideline check

- Date: 2026-10-16
- Case: 25
- Context / question: What are the risks?
- Options considered: ignore; measure accuracy when the summary is wrong; sensitivity/specificity of the flags.
- Decision: Fisher/Newcombe for wrong vs right summaries; sensitivity/specificity with Wilson CIs and cut-off table.
- Why: Decision-support risk.
- Assumption checks / evidence: −11.7 pp when wrong (p ≈ 3e-6); guideline sensitivity 74%, 28% of flags false.
- Impact if wrong / mitigation: Source-check steps and audits.

## D-25-07: ₹ translation

- Date: 2026-10-16
- Case: 25
- Context / question: What is it worth?
- Options considered: hours; ₹ with wrong-decision cost.
- Decision: 2 lakh claims/month; ₹900/hour; ₹6,000 per wrong decision; ₹45 copilot cost.
- Why: Time and quality in one currency.
- Assumption checks / evidence: ≈ 125,500 hours freed; net ≈ ₹10.6 crore/month.
- Impact if wrong / mitigation: Assumptions are explicit.
