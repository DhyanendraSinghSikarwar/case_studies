---

# Case Study 28 — Speed-to-lead: delay, AI first touch and routing (Policybazaar / Ringg AI) · `cs28_speed_to_lead.ipynb`

## D-28-01: Data source — synthetic leads with RM queue delays and a randomised AI window

- Date: 2026-10-17
- Case: 28
- Context / question: We need first-contact delays and outcomes, plus a causal comparison.
- Options considered: public CRM sets (no first-contact times); synthetic data.
- Decision: ≈ 148k leads over 6 weeks; days 22–35 randomise 30% of leads to an AI call within a minute.
- Why: Delay is confounded in normal data.
- Assumption checks / evidence: SRM p = 0.85; median RM delay 10 min (documented 8–12).
- Impact if wrong / mitigation: The design transfers; magnitudes are illustrative.

## D-28-02: Synthetic parameters — decay with delay; hot leads called first; calibrated routing

- Date: 2026-10-17
- Case: 28
- Context / question: How do delay, quality and queues interact?
- Options considered: delay as random; delay shaped by queues and lead priority.
- Decision: The second. The qualification step was recalibrated from 17.5% to 6.1% of reached leads after the first run missed the documented 5–7%.
- Why: Realistic confounding and the documented routing mix.
- Assumption checks / evidence: Routing 68/26/6 vs documented 67/26/7.
- Impact if wrong / mitigation: None.

## D-28-03: Observational curve and confounding

- Date: 2026-10-17
- Case: 28
- Context / question: What does the raw delay curve say?
- Options considered: bands only; adjusted logistic including an oracle for quality.
- Decision: Wilson CIs by band, Cochran–Armitage, odds ratio per doubling with and without controls.
- Why: Shows that more than half the raw effect is lead quality.
- Assumption checks / evidence: OR 0.57 → 0.54 (hour, product) → 0.80 (true quality).
- Impact if wrong / mitigation: None.

## D-28-04: Randomised ITT; valid heterogeneity only on pre-treatment covariates

- Date: 2026-10-17
- Case: 28
- Context / question: What did the AI first touch do, and for whom?
- Options considered: compare the AI group with control leads grouped by delay (selection); subgroups by hour and product.
- Decision: The second, with Holm.
- Why: Delay bands among controls are post-treatment-style selection (hot leads called fast).
- Assumption checks / evidence: Reach +12.8 pp; conversion +1.16 pp (+28%); peak hours +40%.
- Impact if wrong / mitigation: A second arm (human within a minute) would separate speed from voice.

## D-28-05: Observational vs experimental benchmark

- Date: 2026-10-17
- Case: 28
- Context / question: Can the raw curve forecast the benefit?
- Options considered: trust the curve; compare with the experiment.
- Decision: Re-score RM leads at a 0.7-minute delay and compare with the randomised lift.
- Why: Tests the extrapolation.
- Assumption checks / evidence: Predicted +298% vs actual +28%.
- Impact if wrong / mitigation: Never size projects from raw delay curves.

## D-28-06: Queue simulation — waits and utilisation only

- Date: 2026-10-17
- Case: 28
- Context / question: What happens to RM capacity?
- Options considered: simulate conversions via the observational model; use the arms for conversions and simulate only the queue.
- Decision: The second. A conversion model driven by simulated waits gave 251 a day vs an observed 144, because simulated waits are shorter than real delays.
- Why: Avoid reporting an uncalibrated number.
- Assumption checks / evidence: FCFS utilisation 83% vs 4% with AI first touch.
- Impact if wrong / mitigation: Replace the stylised queue with real call durations and rosters.

## D-28-07: ₹ translation

- Date: 2026-10-17
- Case: 28
- Context / question: What is it worth?
- Options considered: observational value of a minute; randomised lift.
- Decision: 4.5 lakh leads/month × randomised lift × ₹1,800 margin; the observational ₹74 lakh/min is flagged as overstated.
- Why: Credible numbers only.
- Assumption checks / evidence: ≈ 5,200 policies and ₹0.9 crore a month (CI ₹0.6–1.3 crore).
- Impact if wrong / mitigation: Assumptions are explicit.
