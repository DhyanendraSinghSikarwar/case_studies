**Say this first (1 line):** Stop the bleeding first (freeze retraining, fix or quarantine the feed), then repair the 2 bad days in the training table and re-score what matters, and add a unit and range contract at ingestion so this cannot be silent again.

**Clarifying questions:**
- Did the change hit the serving path, the training table, or both? It decides whether users saw wrong predictions or only the next model is at risk.
- Is the bad window exactly known (a deploy timestamp, a schema version field)? An exact window makes repair (divide by 100) safe; a fuzzy window means exclude, not fix.
- Did a retrain or auto-deploy run during those 2 days? A model trained on the bad rows may already be live.
- Do predictions drive money or a regulated decision (credit, fraud)? That sets how loudly we notify and whether affected decisions are re-reviewed.
- Is there a raw immutable copy upstream (or a bronze/raw layer)? It lets us replay instead of patching.

**Approach:**
1. First 15 minutes: confirm with a query (daily median of order_value: about 850 for normal days, about 85,000 for the 2 bad days). Page the owner of the upstream table, pause scheduled retraining and any auto-deploy, and stop new bad rows (ask upstream to roll back the change, or add a divide-by-100 shim at our ingestion keyed on the change timestamp).
2. First 15 minutes, serving: if the model uses order_value as an input, compare score distributions for the bad days. If shifted, clamp or cap the feature at serving, or fall back to the previous model or a rule, until the feed is fixed. Escalate to the incident lead if decisions are money-bearing; roll back or fall back if the score distribution has shifted more than a pre-agreed amount (for example, mean score moved by more than 3 standard errors of a normal day).
3. First day, training table: tag the affected partitions, do not delete them. Repair by dividing by 100 only if the window is exact; otherwise exclude those days from training. Never leave them in: the 2 days are 2.2% of days, but they move the mean of order_value about 3x (see the run).
4. First day, predictions: list which decisions were served from bad inputs, re-score them with the repaired features, and decide with the business owner which need correcting or notifying. Check whether any model trained on the table in the window needs retraining or discarding.
5. Next quarter, contract: write a data contract for the feed. Name the field and unit (`order_value_inr`), type, a valid range, and a schema version. Enforce it in two places: producer CI (breaking change needs a version bump and consumer sign-off) and consumer ingestion (range and distribution checks that quarantine a partition, not just warn).
6. Blameless postmortem: the failure was a missing contract and slow detection, not a person. Timeline, detection delay (48 hours here), why no check existed, and action items with owners and dates (contract, distribution monitor, change-notice channel).

**Metrics:**
- Detection delay = time of first bad row to time of detection. Here 48 hours; target under 24 hours with a daily check, and under 1 hour with a per-batch check.
- Affected-row share = bad rows / all rows in the training table (exactly 2/90 of days = 2.2% only if volume per day is equal; use the real row count).
- Feature drift check: daily median of order_value divided by trailing 14-day median; alarm outside 0.2 to 5.
- Served-impact count = predictions made with bad inputs / all predictions in the window.
- Guardrails: no schema change merges without a consumer sign-off; quarantine, never silent drop.

**Risks:**
- Repairing with a divide when some rows in the window were already correct (a partial rollout) creates a new bug. Check by partition and by source.
- The 2.2% is a share of days, not of rows; busy days weigh more.
- A rules-only range check misses a small unit change (for example, 1.2x). Add a distribution test.
- Models trained during the window may still be serving.

**What the interviewer scores:**
- Strong: separates serving, training table and process; gives an order of actions; repairs without destroying evidence.
- Strong: contract has an owner, enforcement point and a consequence (quarantine), not only a document.
- Strong: measures detection delay and brings a blameless action list.
- Weak: "tell upstream to be careful"; deleting rows silently; only fixing the table and forgetting served predictions.

**Example:** Illustrative: 1,000 orders a day, 90 days. A typical order is 850. For 2 days the field is 85,000. Weak versus strong answer:
- Weak: "I would tell the upstream team to notify us next time and then retrain."
- Strong: "First I pause retraining and cap the feature at serving. Then I tag those two partitions, repair them by dividing by 100 because the window is exact, and re-score the affected decisions. The fix that matters is a contract with the unit in the column name plus a median check at ingestion that quarantines a partition, so detection goes from 48 hours to under a day. I would run a blameless review: nobody did anything unusual, we simply had no gate."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- What if you cannot tell exactly which rows changed? Exclude the whole window from training, keep the raw rows, and ask upstream for the deploy time.
- How strict should the contract be? Strict on name, unit, type and range at the producer; statistical checks at the consumer. Breaking changes need a version and a consumer sign-off.
- How do you stop a bad model that trained on this? Compare it to the previous model on a fixed holdout built before the window and block promotion if it is worse (see Book 4 Part 1, Q5, "How do you make a trained model reproducible six months later?", on what to record per run).

**Common mistakes:**
- Fixing the table but not the served predictions.
- Deleting bad rows instead of quarantining them.
- Treating "2.2%" as harmless; an outlier 100x large moves a mean far more than its share.
- Writing a contract nobody enforces.
