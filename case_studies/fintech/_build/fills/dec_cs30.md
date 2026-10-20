---

# Case Study 30 — AI-first support: resolution vs reality and CSAT (PhonePe) · `cs30_support_automation_resolution.ipynb`

## D-30-01: Data source — synthetic contacts with a randomised holdout and a biased survey

- Date: 2026-10-17
- Case: 30
- Context / question: We need support contacts with true resolution (recontact), CSAT and an unbiased benchmark.
- Options considered: public ticket sets (no recontact/CSAT linkage); synthetic data.
- Decision: 120k contacts, 12 issue types, 4 languages, 95% AI-first and a random 5% human-only holdout.
- Why: Claimed and true resolution can differ, and only a holdout reveals it.
- Assumption checks / evidence: Bot closes 87.6% (documented "over 92%").
- Impact if wrong / mitigation: The design transfers; magnitudes are illustrative.

## D-30-02: Synthetic parameters — bot over-claiming, 7-day recontact, response bias

- Date: 2026-10-17
- Case: 30
- Context / question: How do the bot, customers and surveys behave?
- Options considered: bot only closes when it can fix; bot also closes with a generic article. Closure was first tuned to 75% then 85%, then 88% to approach the documented 92%.
- Decision: The second; unresolved customers recontact with probability 0.72; survey response ≈ 9% and higher for unhappy and delighted customers.
- Why: Documented "resolution rate vs CSAT" lesson.
- Assumption checks / evidence: CSAT top-2 62% (documented 70%).
- Impact if wrong / mitigation: Measure over-claiming on real data.

## D-30-03: Claimed vs true resolution — randomised AI vs holdout, non-inferiority

- Date: 2026-10-17
- Case: 30
- Context / question: Is "92% resolved" true?
- Options considered: bot-closed rate; true resolution (no 7-day recontact); randomised comparison.
- Decision: Newcombe CI vs a 3 pp non-inferiority margin; Mann–Whitney on time.
- Why: Closed ≠ fixed.
- Assumption checks / evidence: 80.2% vs 85.9% (−5.7 pp; not non-inferior); handling 2.5 vs 10.1 min.
- Impact if wrong / mitigation: None.

## D-30-04: Over-claiming by issue type; intent accuracy by language

- Date: 2026-10-17
- Case: 30
- Context / question: Where does the bot fail?
- Options considered: pooled; per issue type (Holm) and per language.
- Decision: One-sided tests of bot-closed true resolution vs holdout; χ² and an adjusted logistic for language.
- Why: Harm concentrates in a few issue types.
- Assumption checks / evidence: Fraud 35% vs 80%; regional OR 0.74.
- Impact if wrong / mitigation: None.

## D-30-05: CSAT non-response bias — response model and IPW

- Date: 2026-10-17
- Case: 30
- Context / question: Can ~9% survey response be trusted?
- Options considered: raw responders; inverse-probability weighting on observable predictors; compare with true latent satisfaction (simulation only).
- Decision: Logistic response model (language, issue, bot-closed, arm, wait, handling, recontact); IPW top-2-box with bootstrap CIs.
- Why: The documented 70% CSAT came from a self-selected sample.
- Assumption checks / evidence: Raw 61.9% → IPW 64.0% vs true 65.5%.
- Impact if wrong / mitigation: IPW only fixes bias explained by observed variables.

## D-30-06: Escalation policy — confidence threshold and high-stakes ring-fence on a cost curve

- Date: 2026-10-17
- Case: 30
- Context / question: When should the bot escalate?
- Options considered: threshold only; threshold plus never auto-closing high-stakes issues. The first cost formula multiplied the bot term by zero; replaced by an explicit ₹1 bot cost and unresolved escalations counted.
- Decision: Compare on cost per contact with Clopper–Pearson bounds on high-stakes false closures.
- Why: The right control is which issues, not only confidence.
- Assumption checks / evidence: Ring-fence at τ = 0.2: true resolution 84.2%, ₹34 per contact vs ₹87 as run.
- Impact if wrong / mitigation: Cost weights are illustrative; compliance sets them.

## D-30-07: ₹ translation

- Date: 2026-10-17
- Case: 30
- Context / question: What is it worth?
- Options considered: handling time only; full cost model.
- Decision: 3 crore contacts/month; ₹6/min human; ₹1 per bot-closed; ₹120 per unresolved; ₹900 per high-stakes false closure.
- Why: Time, quality and harm in one currency.
- Assumption checks / evidence: ≈ ₹103 crore/month (ring-fence) vs ₹233 crore (human-only) vs ₹262 crore (as run).
- Impact if wrong / mitigation: Ranking holds if the high-stakes penalty exceeds ≈ ₹150.
