---

# Case Study 29 — Support automation: containment vs CSAT (Zomato Zia and Nugget) · `cs29_support_automation_resolution.ipynb`

## D-29-01: Data source: synthetic tickets with hidden truth and a randomised holdout

- Date: 2026-10-20
- Case: 29
- Context / question: We need tickets with known resolution, abuse and safety labels plus a randomised control.
- Options considered: public support corpora (no order data, not Indian food delivery, no truth); synthetic data.
- Decision: About 180,000 tickets over 56 days in three regimes (legacy tree, LLM-only, LLM plus policy) with a 5% human-first holdout.
- Why: The documented story has no experiment design; a holdout is the only way to test CSAT and resolution effects, and hidden labels let us audit proxies.
- Assumption checks / evidence: Clean data 176,572 tickets; holdout 4,459; max |SMD| 0.024, intent-mix chi-square p = 0.85.
- Impact if wrong / mitigation: Hidden labels are assumed; real resolution must be estimated from re-contact, human grading and LLM-as-judge.

## D-29-02: Define containment three ways and report true resolution

- Date: 2026-10-20
- Case: 29
- Context / question: What does containment mean, and how far is it from resolution?
- Options considered: naive (bot last handler); proxy (no abandon, no re-contact in 72 h); true (resolved).
- Decision: Report all three; make true resolution the headline KPI.
- Why: Naive containment is 69.0% in the policy regime but true containment is 60.8%; 6.6% of kept tickets are abandoned and 11.4% re-contact.
- Assumption checks / evidence: Wilson CIs; proxy 59.5% tracks truth 60.8% here.
- Impact if wrong / mitigation: Proxy quality depends on re-contact behaviour; validate it with sampled human grading.

## D-29-03: Keep a deterministic policy layer around the LLM

- Date: 2026-10-20
- Case: 29
- Context / question: Is the policy layer needed for stability and safety?
- Options considered: LLM-only escalation; LLM plus policy rules.
- Decision: Keep the policy layer.
- Why: Daily containment SD 2.2 vs 12.6 points (ratio 5.8, CI 3.9 to 7.7, Levene p < 1e-6); safety tickets kept by the bot 4.5% vs 37.6%; abusive refunds approved 43.0% vs 74.7%.
- Assumption checks / evidence: Mix explains only 10% of the LLM-only swings; days roughly independent (lag-1 +0.14, -0.19). Cost: mean containment 71.1% to 68.9%.
- Impact if wrong / mitigation: Remaining 27 safety tickets are keyword misses; add a second detector and review rules after each model change.

## D-29-04: Judge CSAT against the randomised holdout, not before/after

- Date: 2026-10-20
- Case: 29
- Context / question: Did CSAT really improve (vendor claim: roughly doubled)?
- Options considered: legacy vs policy before/after; policy vs human-first holdout; raw vs IPW.
- Decision: Report top-2-box with non-response weights and always compare to the holdout.
- Why: Top-2-box 53.2% (legacy) vs 59.4% (policy), risk ratio 1.12 (CI 1.08 to 1.15); vs holdout +11.4 pp (CI 8.0 to 15.1) after IPW; only 13% respond and the holdout answers more often (16.9%).
- Assumption checks / evidence: IPW only fixes non-response explained by observables; holdout has 754 responders (MDE about 10.5 pp).
- Impact if wrong / mitigation: Do not quote a CSAT multiple without a control; collect more survey responders or use LLM-judge scores.

## D-29-05: Route payment issues and weak intents to humans first

- Date: 2026-10-20
- Case: 29
- Context / question: Where does the bot pipeline lose to humans?
- Options considered: bot for all intents; human-first for chosen intents.
- Decision: Human-first for payment issues, safety keywords and rider behaviour; review account, food-quality and missing-item thresholds.
- Why: Holdout resolution gaps: payment -9.0 pp (Holm p = 0.0003), account -5.4, food quality -5.3, missing item -4.6; overall -3.0 pp (CI -3.8 to -2.2).
- Assumption checks / evidence: Holm over nine intents; holdout detects 2.3 pp overall; where-is-order gap -0.7 pp (not significant).
- Impact if wrong / mitigation: Per-intent CSAT is untestable with this holdout size; keep the holdout permanent.

## D-29-06: Pilot model-based extra escalation at about 5%, in shadow mode

- Date: 2026-10-20
- Case: 29
- Context / question: Should a failure model escalate the riskiest bot-kept tickets?
- Options considered: none; 5% to 30% extra escalation by model vs random.
- Decision: Pilot about 5% extra escalation, shadow mode first.
- Why: AUC 0.642 (logistic 0.645, no gain from boosting); at 5% true resolution 91.0% vs 89.6% random, cost ₹39.30 vs ₹41.41 per ticket; cost rises beyond 10%.
- Assumption checks / evidence: Time-ordered split (train days 14-41, test 42-55); escalated tickets assumed to get observed human outcomes.
- Impact if wrong / mitigation: Queue growth and weak AUC; roll out only if a live test confirms; worst-case 10% extra loses ₹3.5 crore a year.

## D-29-07: ₹ business case assumptions

- Date: 2026-10-20
- Case: 29
- Context / question: What is the annual value and how robust is it?
- Options considered: best, base and worst unit costs.
- Decision: 1 crore contacts a month, human ₹55, bot ₹4, ₹120 lost per unresolved ticket; worst ₹40, ₹60 and double leakage.
- Why: Policy layer saves about ₹148 crore a year in the base case (₹93 to ₹231 crore) vs ₹124 crore for LLM-only; positive in every scenario.
- Assumption checks / evidence: Assumed unit costs; rates from simulated regimes.
- Impact if wrong / mitigation: Rely on the ranking, not the rupee level; replace with measured cost per ticket and margin loss.
