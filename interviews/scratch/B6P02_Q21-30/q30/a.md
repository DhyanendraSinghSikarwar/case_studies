**Say this first (1 line):** It is concept drift when the inputs look the same but the link between inputs and churn has changed; I confirm it by comparing the fitted relationship before and after on labelled data, and I fix it with newer data, regime-aware features and a shorter or weighted training window.

**Clarifying questions:**
- When exactly was the price change, and was it for all customers or a subset? That defines the regimes and a clean before/after split.
- How long until churn labels mature after the change? It tells me how much post-change labelled data exists.
- Did the price change come with other changes (plans, bundles, competitors)? Concept drift has many possible causes.
- How is lift measured (top-decile lift, precision at a retention budget)? I need a metric for the before/after comparison.
- Is price or plan information available as a feature? A model that can see price can learn the new relationship.

**Approach:**
1. Rule out data drift: compare input distributions (means, sds, PSI) before and after; also train a classifier to tell before from after inputs; if it cannot (AUC near 0.5), inputs have not moved.
2. Confirm concept drift on labelled data: evaluate the old model on post-change data and compare with its pre-change performance; then fit a fresh model on post-change data and compare coefficients (or partial dependence) with the old one.
3. Test the change formally: the usage coefficient differs by more than its sampling error, or an interaction between usage and a post-change flag is significant.
4. Check where the relationship changed: by plan, tenure, price band. The price change may bite only some customers.
5. Try fixes in order: add price or plan features and a post-change indicator with interactions; retrain on post-change data when there is enough (otherwise combine old and new with a regime flag or recency weights); shorten the training window; consider separate models per regime.
6. Validate on a post-change time split, not a random split.
7. Monitor: labelled lift weekly once labels mature, a drift check on the model's partial dependence, and a rule that major price or product changes trigger a model review.

**Metrics:**
- Top-decile lift = churn rate in the top 10% by score / overall churn rate.
- AUC on a post-change holdout.
- Usage coefficient and its standard error before and after; PSI per input.
- Guardrails: retention-campaign cost per saved customer, calibration of predicted churn.

**Risks:**
- Few post-change labels, so new models are noisy.
- The new regime may still be settling (customers react over weeks).
- Fixing with a random-split validation hides the problem.
- Retention offers based on the old relationship waste budget.

**What the interviewer scores:**
- Strong: separates covariate (data) drift from concept drift with a test for each. Weak: "distribution changed".
- Strong: confirms with labelled data and shows the changed relationship. Weak: assumes it.
- Strong: proposes regime features and window choices with trade-offs. Weak: "retrain".
- Strong: uses a time-based validation. Weak: random split.

**Example:** (illustrative simulation) Churn depends on usage with a slope of -1.0 before the price change and about -0.2 after, with a higher base level. The estimated usage coefficients are -1.00 (plus or minus 0.03) and -0.21 (plus or minus 0.02): far outside noise. The input means and sds of both features are unchanged (0.01 and -0.01 means, sd 1.0). The old model's AUC falls from 0.753 to 0.574 and its top-decile lift from 2.55 to 1.37 on post-change data; a model refit on the new regime gets AUC 0.604 and lift 1.49 on the same test, which is about the best this noisy relationship allows. With only 3,000 post-change rows, a model fit on just those reaches 0.603, so a small amount of fresh data already recovers most of the loss in this toy. Weak: "The inputs did not change, so the model should be fine." Strong: "Inputs same, relationship different: that is concept drift, and the old model's ranking is what broke."

**Code:**
