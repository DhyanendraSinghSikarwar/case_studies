---

# Case Study 10 — BNPL fraud rings via graph communities (Simpl) · `cs10_bnpl_fraud_rings_graph.ipynb`

## D-10-01: Data source — synthetic BNPL onboarding with identity attributes

- Date: 2026-10-16
- Case: 10
- Context / question: We need applicants with shared identity attributes, rings and genuine sharing.
- Options considered: public credit data (no links); Elliptic (crypto, unrelated); synthetic data.
- Decision: 120k users over 13 weeks; 70 rings; lone fraud; families, Zipf-sized address hubs, carrier IP blocks; FPD label.
- Why: Only synthetic data provides both rings and "good-user" sharing.
- Assumption checks / evidence: Fraud 0.98%; FPD 3.9% (22% of it fraud).
- Impact if wrong / mitigation: The method transfers; magnitudes are illustrative.

## D-10-02: Synthetic parameters — ring behaviour and realism fixes

- Date: 2026-10-16
- Case: 10
- Context / question: How realistic should rings be?
- Options considered: rings recruited from consecutive sign-ups; rings spread over 3–20 days with mixed SIM ages.
- Decision: The second option. The first calibration made all rings form within minutes and gave SIM age alone an AUC of 0.95.
- Why: Real gangs onboard over days, and genuine users also have new SIMs (15%).
- Assumption checks / evidence: SIM age alone now gives AUC 0.78; ring members link to ≈ 6 earlier users.
- Impact if wrong / mitigation: Burst rings favour real-time features (see D-10-05).

## D-10-03: Permutation test and hub pruning

- Date: 2026-10-16
- Case: 10
- Context / question: Is there graph signal, and how should the graph be built without collateral damage?
- Options considered: no pruning; prune attributes shared by more than D users.
- Decision: Label-permutation test (500 shuffles); D sweep 3–∞ measuring ring coverage vs genuine users in communities of 4+; choose D = 10.
- Why: Hostels, offices and families create genuine hubs.
- Assumption checks / evidence: 45% vs 9% co-default (p = 0.002); D = 10 keeps 98% of rings at 4.8% genuine collateral (vs 12.9% unpruned).
- Impact if wrong / mitigation: Re-tune D on investigated cases.

## D-10-04: As-of graph features and feature tiers

- Date: 2026-10-16
- Case: 10
- Context / question: What does each information layer add at onboarding?
- Options considered: static full graph (leaks the future); time-respecting snapshots.
- Decision: Features built only from users onboarded earlier. Tiers: individual → 1-hop counts → communities → day-7 behaviour. DeLong + Holm; recall at a 1% decline budget.
- Why: The production constraint and the cost of each layer.
- Assumption checks / evidence: 1-hop +0.098 AUC (p < 1e-4); communities +0.009 (p = 0.19); behaviour +0.15 but late.
- Impact if wrong / mitigation: None.

## D-10-05: Real time vs nightly batch; label choice; cluster-robust precision

- Date: 2026-10-16
- Case: 10
- Context / question: Do architecture and label choices matter?
- Options considered: hourly vs daily snapshots; FPD vs confirmed-fraud labels; naive vs cluster bootstrap CIs.
- Decision: Test each (exact McNemar; DeLong; community bootstrap).
- Why: Documented Flink vs Airflow; FPD mixes credit stress with fraud; declines are clustered.
- Assumption checks / evidence: Real time is not significant overall (p = 0.36) but better for same-day ring-mates (90% vs 84%). Fraud label +0.048 AUC. Cluster CI 39–62% vs naive 48–57%.
- Impact if wrong / mitigation: None.

## D-10-06: Cost model and decline threshold

- Date: 2026-10-16
- Case: 10
- Context / question: Where should the decline line be drawn?
- Options considered: fixed budget; cost-minimising sweep.
- Decision: Fraud approved = 90% of limit; genuine defaulter = 50% of limit; good user declined = ₹1,200 lifetime value. Sweep 0–8%.
- Why: The documented "impact on good users".
- Assumption checks / evidence: Optimum at 0.5% (₹7.1 lakh saved over 5 weeks; 1 good user declined); above ≈ 2.5% it costs money.
- Impact if wrong / mitigation: The optimum moves with the LTV assumption; recompute.

## D-10-07: ₹ translation

- Date: 2026-10-16
- Case: 10
- Context / question: How should results be expressed in ₹?
- Options considered: test-period savings; scaled monthly.
- Decision: Savings per applicant × 5 lakh sign-ups per month (assumption).
- Why: Comparable monthly figure.
- Assumption checks / evidence: ≈ ₹0.77 crore/month at 0.5%; tiers: individual −₹0.49 crore, 1-hop +₹0.58 crore.
- Impact if wrong / mitigation: Linear in volume.
