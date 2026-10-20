---

# Case Study 5 — Evaluating an AI-agent merchant reviewer (Razorpay Bumblebee) · `cs05_merchant_review_automation.ipynb`

## D-5-01: Data source — synthetic reviews, analysts, agent outputs, gold panel, outcomes

- Date: 2026-10-16
- Case: 5
- Context / question: We need decisions from humans and the agent with ground truth.
- Options considered: none public; synthetic data.
- Decision: 36k merchants; 40 analysts; agent decisions + confidence; 3k gold panel; 6-month outcomes.
- Why: Evaluating "accuracy" needs several references.
- Assumption checks / evidence: Agent vs gold 98.8%; analysts 88.7% (documented 99% / 88%).
- Impact if wrong / mitigation: The evaluation framework transfers; magnitudes are illustrative.

## D-5-02: Synthetic parameters — variable analysts; consistent agent; half of fraud invisible at onboarding

- Date: 2026-10-16
- Case: 5
- Context / question: How should humans and the agent be modelled?
- Options considered: equal skill; analysts with strictness and attention variation.
- Decision: The second; the agent uses the same evidence with small noise and 0.8% fetch failures. True risk is only partly visible in the evidence.
- Why: Documented inconsistency; realistic limits of onboarding evidence.
- Assumption checks / evidence: Analyst reject rates 1.5–31.6%; truth sensitivity ≈ 50% for everyone.
- Impact if wrong / mitigation: Real LLM failure modes differ, so evaluate the real system.

## D-5-03: Scope — evaluate decisions, not reproduce LLM agents

- Date: 2026-10-16
- Case: 5
- Context / question: Should the agents be rebuilt?
- Options considered: call an LLM API; simulate outputs.
- Decision: Simulate outputs (decision, confidence, latency, tokens).
- Why: The brief's library list; the evaluation is the data-science task.
- Assumption checks / evidence: Section 8 lists the extra checks needed for real agents.
- Impact if wrong / mitigation: None.

## D-5-04: Agreement and accuracy — κ, accuracy vs 3 references, sensitivity/specificity, McNemar

- Date: 2026-10-16
- Case: 5
- Context / question: What does "accuracy" mean?
- Options considered: accuracy vs analysts; vs gold panel; vs truth.
- Decision: All three, plus the always-approve baseline and class-specific metrics.
- Why: The documented metric's reference is ND.
- Assumption checks / evidence: vs single analyst 87.9%; vs gold 98.8%; always-approve 92.8%; sensitivity 91% vs 64%.
- Impact if wrong / mitigation: None.

## D-5-05: Selective automation — confidence threshold with a Clopper–Pearson bound ≤ 1%

- Date: 2026-10-16
- Case: 5
- Context / question: When may the agent decide alone?
- Options considered: all; none; threshold.
- Decision: The largest coverage with a 95% upper error bound ≤ 1% → confidence ≥ 0.3 (96% coverage).
- Why: Human-in-the-loop with explicit risk.
- Assumption checks / evidence: Error 0.35% (UB 0.59%); 2.8% of risky auto-approved; 53% of errors are contested cases.
- Impact if wrong / mitigation: Use ≥ 0.5 if risk appetite is lower.

## D-5-06: Outcome validation — 6-month bad rate non-inferiority (+0.5 pp)

- Date: 2026-10-16
- Case: 5
- Context / question: Do agent-approved merchants go bad more often?
- Options considered: decisions only; outcomes.
- Decision: Newcombe CI on bad rate among approved.
- Why: The final arbiter of quality.
- Assumption checks / evidence: 3.85% vs 4.16% (non-inferior); same bad merchants let through, ~800 fewer good merchants rejected per 12k.
- Impact if wrong / mitigation: Outcomes are seen only for approved merchants.

## D-5-07: ₹ and operations — latency, tokens, analyst hours, cost model

- Date: 2026-10-16
- Case: 5
- Context / question: What is it worth?
- Options considered: hours only; full cost model.
- Decision: ₹600/hour; ₹1.5 lakh per bad merchant; ₹20k per lost good merchant; ₹0.0004/token.
- Why: Leaders weigh speed, cost and risk together.
- Assumption checks / evidence: v2 median 10 s, −60% tokens; ≈ ₹2.3 crore/month saved; ₹8.3 crore/month fraud untouched by onboarding.
- Impact if wrong / mitigation: Assumptions are explicit.
