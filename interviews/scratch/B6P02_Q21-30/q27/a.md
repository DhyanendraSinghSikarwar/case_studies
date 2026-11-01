**Say this first (1 line):** With no outcomes yet, I split the fall in mean score into a change in who is applying and a change in score within each type of applicant, then check pipeline, model and feature health to see which part is real; I tell the business what we know, what we do not, and when labels will tell us.

**Clarifying questions:**
- Was there any change to the model, its features, the scoring service or the data feeds this month? A deployment calendar answers part of this at once.
- Did the applicant source mix change (new partner, marketing channel, product, city)? Mix is the first non-model cause.
- Did the policy upstream of the model change (pre-filters, eligibility rules, cut-offs)? It changes who reaches the model.
- Is the score a probability of default, and is it calibrated? A mean-score fall only means lower risk if calibrated.
- Do we have partial early signals (first-payment default, early delinquency)? They give a weak read before full labels.

**Approach:**
1. Rule out a plain bug: null rates, ranges, units and schema checks on every input feature; compare feature distributions to last month with PSI; check the scoring service version and that the model hash is unchanged.
2. Replay test: re-score last month's applications through the current pipeline. If scores differ, the pipeline or model changed; if not, the inputs changed.
3. Decompose the fall: segment applicants (for example prime, near-prime, subprime, or by channel) and split the change into a mix effect (shares changed) and a within-segment effect (scores moved inside a segment).
4. If it is mostly mix, check whether the new mix is plausible (marketing, partner, policy change). If within-segment, find which features moved and why (new data source, changed bureau fields, income capture).
5. Look at early indicators: first-payment default, early delinquency and application-level proxies, with caution about their power.
6. Communicate: "Mean score fell 0.08; about half is a change in applicant mix; the rest is inside segments and I am checking features. No evidence of a bug if the replay matches. Risk is unconfirmed until outcomes mature; here are the early indicators and the date to re-check." Avoid declaring that risk improved.
7. Put in place: a feature and score-drift dashboard with alerts and a rule that applicant-mix changes are announced to the model team.

**Metrics:**
- Mean score = sum of scores / number of applicants, by month and by segment.
- Mix effect = sum over segments of (share_this - share_last) x mean_last; within-segment effect = sum of share_this x (mean_this - mean_last). They add exactly to the total change.
- PSI by feature and for the score; null rate; replay score difference.
- Guardrails: approval rate, early delinquency, rejection reasons.

**Risks:**
- A lower mean score is not lower risk unless the model is calibrated and the mix is understood.
- Reweighting by observed segments assumes the segments are stable definitions.
- Early indicators are weak and biased by who was approved.
- Acting on the score (for example loosening cut-offs) before outcomes mature locks in losses.

**What the interviewer scores:**
- Strong: lists competing hypotheses and a check for each that needs no labels. Weak: "the model must be fine/broken".
- Strong: mix versus rate decomposition and a replay test. Weak: only PSI.
- Strong: honest communication that risk is unconfirmed. Weak: tells the business risk improved.
- Strong: asks about deployments and policy changes. Weak: jumps to modelling.

**Example:** (illustrative) Segments last month: prime 40% (mean score 0.12), near-prime 30% (0.30), subprime 30% (0.54), mean 0.30. This month: prime 50% (0.092), near-prime 30% (0.26), subprime 20% (0.48), mean 0.22. The change is -0.08. The mix effect is (0.10)(0.12) + 0 + (-0.10)(0.54) = -0.042, which is 52% of it; the within-segment effect is 0.5(-0.028) + 0.3(-0.04) + 0.2(-0.06) = -0.038, or 48%. All three segments' scores fell, which a mix change alone cannot explain, so something also moved inside segments: pipeline, model, feature data, or real improvement. Weak: "The score fell, so risk improved." Strong: "Half is mix; the other half is inside every segment, so I replay and check features before saying anything about risk."

**Code:**
