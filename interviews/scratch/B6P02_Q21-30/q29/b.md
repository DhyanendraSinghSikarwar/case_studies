**Follow-ups:**
- What if the patch has uncertain recovery? Use a range and decide on the worst case you can accept; stage the rollout to learn the real recovery in days.
- How would you shorten the retrain? Reduce scope (refit recent data on the same features), reuse the validation pipeline, and parallelise tasks.
- Who approves? The model owner and risk or compliance for decisions affecting customers, with a written change record.

**Common mistakes:**
- Shipping a patch with no backtest.
- No kill switch, owner or end date.
- Counting the patch benefit without its customer-side costs.
- Letting the patch live beside the new model unreviewed.
- Ignoring the days before the patch is live.
