**Say this first (1 line):** A falling catch rate with a flat false-positive rate means fraud changed, not the model, so I show it with confirmed-fraud cohorts split by tactic, refuse to retrain only on flagged cases because they hide the new tactic, and respond in layers with random audits, rules, features and a retrain on proper labels.

**Clarifying questions:**
- How is "confirmed fraud" labelled, and how late? Chargebacks lag, so recent months are under-counted and the 70% may still move.
- Did the transaction mix or approval policy change, or was a rule that used to catch fraud removed? Those drop catch rate without any adversary.
- Is the catch rate measured at a fixed score threshold, and is the threshold unchanged?
- Which analyst signals say tactics changed: new merchant types, device patterns, small-amount probing, mule accounts?
- Is there a random audit sample today? It is the clean way to measure fraud the model never flags.

**Approach:**
1. Confirm the drop is real and not label lag: compare catch rate for equal-maturity cohorts (same days since transaction) and report a confidence interval.
2. Split confirmed fraud by "tactic" using features and analyst tags: old patterns versus new. Compute the catch rate in each.
3. Look at the score distribution of confirmed fraud: new fraud clusters just below the threshold or at low scores, and its features (new devices, merchants, amount patterns) are unlike the training data.
4. Check what stayed the same: false-positive rate flat and good-traffic distribution stable point to the fraud side moving, not the model decaying everywhere.
5. Avoid the naive retrain: a training set of recent flagged cases contains mostly the old tactic, because the new one was not flagged; unflagged new fraud is labelled legitimate unless the chargeback arrives. That reinforces the blind spot.
6. Layered response: a random audit slice for unbiased labels; fast rules and velocity or device-linking features for the new tactic; a retrain on confirmed outcomes with recency weights and the new features; consider a second model or anomaly score for novelty; keep an analyst feedback loop.
7. Monitor catch rate per tactic and per segment, not only overall, and track adversary signals (probing, reaction after each rule change).

**Metrics:**
- Catch rate (recall) = confirmed fraud cases flagged / confirmed fraud cases, by matured cohort.
- False-positive rate = legitimate transactions flagged / legitimate transactions.
- Catch rate by tactic = flagged cases of that tactic / all confirmed cases of that tactic.
- Guardrails: approval rate, customer friction (declines of good users), analyst queue size and review time.

**Risks:**
- Label delay makes the latest cohorts look better or worse than they are.
- Selection bias: labels exist mainly where the system or analysts looked.
- Adversaries adapt to each fix; rules decay.
- A new rule raises false positives and customer friction.
- A random audit costs reviewer time and lets some fraud through, by design.

**What the interviewer scores:**
- Strong: separates "fraud changed" from "model broke" with a tactic split. Weak: assumes drift and retrains.
- Strong: explains why flagged-only training data is biased. Weak: "retrain on the last three months".
- Strong: layered response with time scales (rules now, model later) and the audit slice. Weak: one fix.
- Strong: mentions label maturity. Weak: treats the 70% as final.

**Example:** (illustrative) Take 1,000 confirmed fraud cases. If the old tactic is caught 85% of the time and the new one 10%, a 70% overall catch rate needs the new tactic to be 20% of fraud: 800 old cases (680 caught) and 200 new (20 caught), 700 of 1,000. A z-test with 1,000 cases in each period gives z = 8.0 for 85% versus 70%, so the drop is not noise. Among flagged fraud, the new tactic is only 20 of 700 = 2.9%, against 20% of real fraud, and 180 new-tactic fraud cases look like normal traffic. A flagged-only retrain would learn almost nothing about the new tactic. A random audit of 2,000 transactions at a 0.5% fraud base rate finds about 10 fraud cases (12 in my seeded run), enough to start measuring the blind spot. Weak: "Retrain on the recent fraud we caught." Strong: "Split by tactic first; recent flagged cases are the cases the model already knew."

**Code:**
