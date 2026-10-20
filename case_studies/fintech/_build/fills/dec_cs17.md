---

# Case Study 17 — Non-inferiority of 10-second pre-approved loans (HDFC Bank) · `cs17_preapproved_pl_noninferiority.ipynb`

## D-17-01: Data source — synthetic customers, observational loans and a randomised pilot

- Date: 2026-10-16
- Case: 17
- Context / question: We need loans by channel with outcomes, plus a causal comparison.
- Options considered: observational only; observational + randomised pilot.
- Decision: 200k customers; ~9.3k observational loans; a 16k pilot randomised 1:1 among eligible applicants.
- Why: Branch vs instant selection makes observational comparison unreliable.
- Assumption checks / evidence: SRM p = 0.94; max |SMD| 0.016.
- Impact if wrong / mitigation: The design transfers; magnitudes are illustrative.

## D-17-02: Synthetic parameters — small hidden channel effect; officers screen on unobservables

- Date: 2026-10-16
- Case: 17
- Context / question: What is the truth to recover?
- Options considered: no channel effect; a small effect (+0.12 log-odds) with branch screening on latent quality.
- Decision: The second. Physical selection was tuned so raw rates look "on par".
- Why: It reproduces the documented "on a par" claim while making the inference problem realistic.
- Assumption checks / evidence: Raw +0.6 pp; truth +0.46 pp for eligible customers.
- Impact if wrong / mitigation: None.

## D-17-03: P27 layers — drop-one LR tests (Holm)

- Date: 2026-10-16
- Case: 17
- Context / question: Does each layer add value?
- Options considered: combined score only; layer-wise LR tests.
- Decision: Logit on four layer scores + log amount; drop each layer in turn.
- Why: The "social" layer needs justification.
- Assumption checks / evidence: Bureau and behaviour significant; ability ns (after amount); social p = 0.07.
- Impact if wrong / mitigation: Range restriction lowers all AUCs.

## D-17-04: Non-inferiority design — 1 pp margin, one-sided α = 0.025, Newcombe CI; RR and HR margins 1.25

- Date: 2026-10-16
- Case: 17
- Context / question: How should "on a par" be operationalised?
- Options considered: two-sided equality test; NI with a pre-set margin.
- Decision: NI with δ = 1 pp, justified by the break-even (0.96 pp).
- Why: The business accepts a small deterioration for cost and speed.
- Assumption checks / evidence: Pilot +0.22 pp, upper bound 0.81 → non-inferior; Cox HR upper bound 1.24.
- Impact if wrong / mitigation: Pilots need ≥ 16k per arm for a +0.4 pp true difference.

## D-17-05: Observational analyses — raw, IPW (ATT), eligible-only, E-value

- Date: 2026-10-16
- Case: 17
- Context / question: What would the bank conclude without a pilot?
- Options considered: report raw only; adjust and test sensitivity.
- Decision: All four estimates plus E-values.
- Why: To show why observational evidence is insufficient.
- Assumption checks / evidence: Raw not NI (upper 1.43); IPW +2.0 pp (overstated; truth +0.46); E-value ≈ 3.
- Impact if wrong / mitigation: Use pilots as the decision basis.

## D-17-06: Survival analysis — KM, log-rank, Cox; missing-month sensitivity

- Date: 2026-10-16
- Case: 17
- Context / question: Does timing matter?
- Options considered: 12-month rate only; time to event.
- Decision: KM curves, log-rank, adjusted Cox HR; imputed months set to 6, with an exclusion sensitivity.
- Why: Vintage curves are standard credit monitoring.
- Assumption checks / evidence: HR 1.056 (0.90–1.24); 1.057 excluding imputed.
- Impact if wrong / mitigation: None.

## D-17-07: ₹ translation — processing saving vs extra credit loss

- Date: 2026-10-16
- Case: 17
- Context / question: Is non-inferior good enough economically?
- Options considered: TAT only; ₹ net with scenarios.
- Decision: ₹2,500 vs ₹150 processing; 35% loss on extra 30+ DPD; ₹2,000 crore/month instant disbursals.
- Why: It ties the margin to economics.
- Assumption checks / evidence: Net +₹5.2 crore/month (point), +₹1.05 crore (upper bound); break-even 0.96 pp.
- Impact if wrong / mitigation: Assumptions are explicit.
