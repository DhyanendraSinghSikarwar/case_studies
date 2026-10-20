---

# Case Study 26 — Chat vs conversion: self-selection and an encouragement experiment (Policybazaar) · `cs26_chat_conversion_causal.ipynb`

## D-26-01: Data source — synthetic visitors with self-selection, a randomised pop-up and a bot era

- Date: 2026-10-17
- Case: 26
- Context / question: We need visitor-level chat and purchase data with a known truth.
- Options considered: public insurance sets (Kaggle, no chat channel); synthetic data.
- Decision: 300k visitors over 8 weeks; hidden intent drives both chatting and buying; a randomised proactive pop-up from week 3; bot era from week 5.
- Why: Only simulation allows comparing observational, IV and true effects.
- Assumption checks / evidence: Chat share 9.7% (documented 8–9%); raw RR 2.15 (documented ~2×).
- Impact if wrong / mitigation: The method transfers.

## D-26-02: Synthetic parameters — modest true effect, partly unobserved intent

- Date: 2026-10-17
- Case: 26
- Context / question: How much of the 2× is real?
- Options considered: all real; all selection; partly each.
- Decision: True chat effect +0.35 log-odds (≈ +2.5 pp for chatters); an unobserved intent component also drives both behaviours.
- Why: The reference file itself flags self-selection.
- Assumption checks / evidence: True average effect +1.60 pp (all), +2.49 pp (chatters).
- Impact if wrong / mitigation: None.

## D-26-03: Observational adjustment — PS matching, IPW, AIPW

- Date: 2026-10-17
- Case: 26
- Context / question: How much does adjustment help?
- Options considered: raw; matching; IPW; doubly robust.
- Decision: All three adjusted ATT estimates with bootstrap CIs (100 resamples, to keep runtime reasonable); balance by SMD; pop-up excluded from the score.
- Why: Show that adjustment removes only observed confounding.
- Assumption checks / evidence: +4.76 → +3.6 to +3.8 pp.
- Impact if wrong / mitigation: None.

## D-26-04: Sensitivity analysis — Rosenbaum Γ and E-value

- Date: 2026-10-17
- Case: 26
- Context / question: Could hidden intent explain the remainder?
- Options considered: ignore; quantify.
- Decision: Γ on matched discordant pairs; E-values for raw and AIPW.
- Why: Honest uncertainty about unobserved confounding.
- Assumption checks / evidence: Γ ≈ 1.75; E-value 2.8.
- Impact if wrong / mitigation: Use the experiment.

## D-26-05: Encouragement design — ITT, first stage, Wald/2SLS LATE

- Date: 2026-10-17
- Case: 26
- Context / question: What is the causal effect of chat?
- Options considered: observational only; randomise the pop-up.
- Decision: ITT, first stage, Wald and covariate-adjusted 2SLS with bootstrap CIs (120 resamples).
- Why: Chat cannot be forced on visitors.
- Assumption checks / evidence: ITT +0.32 pp (p = 0.0002); LATE +3.5 pp (CI +1.2 to +5.2) vs truth +1.6–2.5.
- Impact if wrong / mitigation: A placebo pop-up arm would test the exclusion restriction.

## D-26-06: Speed analysis — and a bug fixed

- Date: 2026-10-17
- Case: 26
- Context / question: Did faster bot replies matter?
- Options considered: delay effect within chats.
- Decision: Adjusted logistic on first-response delay (capped at 30 minutes). The first run reported an odds ratio of 1.74 per minute (the wrong sign) because the coefficient was picked by position and patsy lists categorical dummies first. The term is now looked up by name: OR 0.944 per minute.
- Why: Report the right coefficient.
- Assumption checks / evidence: Delays > 5 min fell 45.5% → 5.9%; OR 0.944 (CI 0.935–0.953).
- Impact if wrong / mitigation: None.

## D-26-07: ₹ translation

- Date: 2026-10-17
- Case: 26
- Context / question: What does "push everyone to chat" earn?
- Options considered: raw 2×; adjusted; experimental.
- Decision: 30 lakh visitors/month; chat share 9.7% → 30%; average premium ₹11,005; commission 15%.
- Why: Shows how the choice of estimate changes the business case.
- Assumption checks / evidence: Raw ≈ 29,000 policies; LATE ≈ 21,000 (range 7,500–31,900); truth ≈ 12,000.
- Impact if wrong / mitigation: Plan with the conservative end.
