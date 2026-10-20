---

# Case Study 7 — Real-time fraud screening: velocity, graph, anomaly (Cashfree RiskShield) · `cs07_velocity_graph_fraud_screening.ipynb`

## D-7-01: Data source — synthetic merchant transactions with seven signal groups

- Date: 2026-10-16
- Case: 7
- Context / question: We need transactions with device, IP, contact, negative-list, velocity and graph signals plus fraud labels.
- Options considered: ULB / IEEE-CIS (Kaggle, anonymised, no entities); PaySim (no device/IP); synthetic data.
- Decision: ≈ 279k transactions over 8 weeks, 3 business lines, 3 attack types, delayed chargeback labels.
- Why: Linkable entity tokens are needed for velocity and graph features.
- Assumption checks / evidence: Fraud 1.35%. Attack fingerprints are distinct but overlapping.
- Impact if wrong / mitigation: Real attack mixes differ. The method transfers.

## D-7-02: Synthetic parameters and hard negatives

- Date: 2026-10-16
- Case: 7
- Context / question: How do we avoid an unrealistically easy problem?
- Options considered: clean attacks; attacks plus genuine look-alikes.
- Decision: Households sharing devices (8%), 20% genuine IP/card-state mismatch, ₹1 verification charges, new phones, fraudsters on residential/same-state proxies, shared carrier IP pools.
- Why: The first calibration gave AUC 0.999; the recalibrated version gives 0.974.
- Assumption checks / evidence: Single-signal precision 5–99%, matching typical rule hit rates.
- Impact if wrong / mitigation: Absolute AUCs are illustrative.

## D-7-03: As-of feature engineering and the leakage test

- Date: 2026-10-16
- Case: 7
- Context / question: How should velocity and graph features be built without look-ahead?
- Options considered: aggregate over the full period; trailing windows plus label-date-aware graph.
- Decision: Sorted-search trailing counts. 1-hop flags only for entities whose fraud was confirmed before the transaction. Daily component snapshots. A hindsight variant is built only to measure the leak.
- Why: Production can only use past information.
- Assumption checks / evidence: Hindsight AUC 0.9999 vs 0.974 as-of (DeLong p ≈ 1e-18).
- Impact if wrong / mitigation: None.

## D-7-04: Signal and family evaluation — lift + Holm; window DeLong; drop-one-family DeLong + Holm

- Date: 2026-10-16
- Case: 7
- Context / question: Which signals and families are worth building?
- Options considered: feature importance; drop-one out-of-time comparison.
- Decision: Lift with Katz CIs on the training weeks; per-attack window AUCs with DeLong; drop-one-family test-weeks AUC, PR-AUC and recall@1%.
- Why: Paired, out-of-time and business-readable.
- Assumption checks / evidence: Velocity −0.082 AUC; graph and geo/IP non-significant on AUC.
- Impact if wrong / mitigation: ₹ value per family is assessed separately (D-7-07).

## D-7-05: Anomaly detection — Isolation Forest plus a never-seen-attack test

- Date: 2026-10-16
- Case: 7
- Context / question: Do anomaly scores add value for unknown attacks?
- Options considered: report AUC only; hold out one attack type from supervised training.
- Decision: Train supervised models without promo abuse, add the anomaly score, and compare promo recall (exact McNemar).
- Why: This tests the documented role of anomaly scores honestly.
- Assumption checks / evidence: 5.7% → 8.1% (p = 0.29). Anomaly catches 83% of card testing.
- Impact if wrong / mitigation: New collective attacks need analyst-written velocity rules.

## D-7-06: Decision thresholds — cost-optimal allow/review/block, per-line vs global, guardrail

- Date: 2026-10-16
- Case: 7
- Context / question: Should thresholds differ by business line?
- Options considered: hand rules; one global pair; per-line pairs.
- Decision: Grid search on week 5 minimising cost (fraud loss by type, margin by line + ₹100 goodwill, ₹30 review, 90% review catch, 5% abandonment), subject to ≤ 0.5% genuine blocked. Evaluate weeks 6–8 with a paired bootstrap.
- Why: Documented line-tuned rules; costs make the trade-off explicit.
- Assumption checks / evidence: Per-line vs global −₹0.02 lakh (CI −0.21 to +0.13). Rules block 0.91% of genuine customers.
- Impact if wrong / mitigation: Re-tune with real margins; the cost model is parameterised.

## D-7-07: Post-processing, feedback loop, explanations and ₹

- Date: 2026-10-16
- Case: 7
- Context / question: Which documented add-ons help, and what is the ₹ value?
- Options considered: none; trusted allowlist; weekly retraining; logistic reason codes.
- Decision: Test each. ₹ scaled to 10× simulated traffic (≈ 15 lakh transactions/month). Family value = extra cost if dropped, with a bootstrap CI.
- Why: Leaders fund families and processes, not AUC.
- Assumption checks / evidence: Allowlist −25% genuine reviews. Weekly retraining no gain (p = 0.51). Reason codes V = 0.54. Model + allowlist ≈ ₹2.5 crore/month vs allow-all (+₹96 lakh vs rules).
- Impact if wrong / mitigation: Family CIs exclude threshold-tuning uncertainty.
