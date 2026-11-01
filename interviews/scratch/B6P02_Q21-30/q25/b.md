**Follow-ups:**
- Why is the FPR staying flat informative? It suggests the good-traffic score distribution did not move, so the model is not broadly miscalibrated; the missed cases are a new fraud subpopulation.
- How would you know an adversary is probing? Many small-amount attempts or new accounts testing the threshold, followed by a change in pattern after each rule or model update.
- What if fraud is also reaching you through a channel with no labels? The random audit slice and downstream signals (disputes, customer reports) are the only way to size it.

**Common mistakes:**
- Retraining on flagged-only data.
- Judging the newest cohorts before chargebacks have arrived.
- Fixing with a single rule that fraudsters route around in a week.
- Reporting only overall catch rate and missing the tactic split.
- Having no random audit, so the blind spot cannot be measured.
