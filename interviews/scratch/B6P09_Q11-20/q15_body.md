**Say this first (1 line):** Kappa is about 0.69, not 90%: raw agreement looks high because 79% to 81% of scans are normal, so the readers agree by chance a lot; reader A is a noisy reference, so I would build an adjudicated or outcome-based reference standard and report accuracy against that.

**Clarifying questions:**
- Were the readers blinded to each other, and to clinical history? Non-independent readers inflate agreement.
- What is the clinical task (any abnormal finding, one specific finding)? The label definition drives what disagreement means.
- Is there an outcome truth available (biopsy, follow-up imaging, clinical course)? That is a better reference than any reader.
- How were the 1,000 scans sampled? If they are enriched for abnormal, kappa and prevalence are not those of the clinic.
- What are the readers' experience levels and the site? A reference should reflect the intended users.

**Approach:**
1. Compute agreement. Matrix: both abnormal 150, both normal 750, A-only 60, B-only 40. Observed agreement = 900 / 1,000 = 0.90. A calls 210 abnormal and B 190. Chance agreement = 0.21 x 0.19 + 0.79 x 0.81 = 0.6798. Kappa = (0.90 - 0.6798) / (1 - 0.6798) = 0.688. A bootstrap interval in the run is about 0.63 to 0.74.
2. Read it correctly. Kappa near 0.69 is moderate to substantial agreement on a common scale; the thresholds are conventions, not rules. Specific agreement is more informative: positive agreement 0.75 (when one reader says abnormal, the other agrees 75% of the time) and negative agreement 0.94.
3. Say what it implies for the ceiling. If A's labels are noisy, a model cannot be reliably better than A as measured against A. In an illustrative model with 20% prevalence and readers of 90% sensitivity and 96% specificity, even a perfect model scores only about 0.947 accuracy against reader A, and two readers agree about 90% of the time (see the run). A model that is more accurate than A will look worse than it is.
4. Beware accuracy as a headline. Everything-normal scores 79% accuracy against A. Report sensitivity, specificity and positive predictive value at the intended prevalence, with intervals.
5. Build a better reference. Options in order of strength: outcome truth (pathology or follow-up), then adjudication (a third senior reader resolves the 100 disagreements, or a panel), then a consensus of three or more readers. Keep the disagreement cases as a separate set: they show where the model and humans differ.
6. Evaluate with the uncertainty. Report model versus adjudicated reference, plus model versus each reader, and compare the model's agreement with a reader to reader-reader agreement (a model agreeing with A at kappa 0.7 is performing at human level, not 70% of the way).

**Metrics:**
- Observed agreement = (both abnormal + both normal) / all = 0.90.
- Kappa = (observed - chance) / (1 - chance) = 0.688; positive and negative specific agreement = 0.75 and 0.94.
- Model sensitivity, specificity and PPV against the adjudicated reference, each with a confidence interval, and calibration at the clinic's prevalence.
- Guardrails: label-noise estimate per class, and model-reader kappa compared with reader-reader kappa.

**Risks:**
- Training on A's labels teaches the model A's habits, including bias; the model inherits A's miss rate.
- Quoting accuracy against A as accuracy in the clinic.
- Adjudicating only disagreements makes the reference depend on the readers' disagreement pattern; spot-check some agreed cases.
- Kappa depends on prevalence, so it is not comparable across sites with different mixes.

**What the interviewer scores:**
- Strong: computes kappa 0.69 with chance agreement shown, and quotes positive agreement.
- Strong: explains the ceiling and why a better-than-A model looks worse.
- Strong: proposes an adjudicated or outcome-based reference and reports against it with intervals.
- Weak: "90% agreement is great, so use A as ground truth".

**Example:** Using the question's counts. Weak versus strong:
- Weak: "The readers agree 90% of the time, so reader A's labels are reliable and we can report accuracy against them."
- Strong: "Agreement is 90% but chance alone gives 68%, so kappa is about 0.69, and when one reader says abnormal the other agrees only 75% of the time. A model cannot be shown better than A against A's own labels, and an all-normal model already scores 79%. I would have a third reader adjudicate the 100 disagreements, or use pathology or follow-up where it exists, and report sensitivity, specificity and PPV with intervals."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- How many readers do you need? Three gives a majority vote and shows which cases are contested; more adds cost with diminishing gain. Ask the clinical lead.
- Does a high kappa mean the labels are correct? No; readers can share a bias. Only outcomes can show that.
- How do you present the model's performance? Against the adjudicated reference with intervals, and next to reader performance on the same scans.

**Common mistakes:**
- Treating raw agreement as reliability.
- Calling one reader "ground truth".
- Forgetting prevalence when interpreting kappa or accuracy.
- Reporting no uncertainty on 1,000 scans, 210 of them abnormal.
