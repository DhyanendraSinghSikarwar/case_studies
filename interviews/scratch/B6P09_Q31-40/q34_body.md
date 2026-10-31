**Say this first (1 line):** Predicted loss is 3,000,000 and the loss from observed defaults at the assumed 50% is 4,500,000, a shortfall of 1,500,000 (observed is 1.5 times predicted); ranking is intact (AUC 0.80), so this is a level problem, and I would first diagnose the cause, then recalibrate under model-governance sign-off unless the miss differs by segment.

**Clarifying questions:**
- Is the 4.5% measured on the same 12-month window and the same default definition used in training? A changed definition makes a model look wrong without being wrong.
- Is the portfolio mix the same as in development (new products, channels, score bands)? A mix shift changes the average PD even if the model is fine.
- Were macro conditions different this year? One year is one draw of the economy, so a common shock can move all defaults together.
- Is the 50% loss given default a policy number or something we have observed on recoveries? The loss figures use it only as an input, so realised recoveries should be checked separately.
- What does the model feed (approval cut-off, pricing, provisioning)? It sets urgency and who has to sign off.

**Approach:**
1. Do the arithmetic. Predicted defaults = 20,000 x 3.0% = 600; observed 900 (4.5%). Expected loss predicted = 20,000 x 0.03 x 10,000 x 0.5 = 3,000,000. Loss from observed defaults at the assumed LGD = 900 x 10,000 x 0.5 = 4,500,000. Shortfall = 1,500,000 (33.3% of observed, observed is 1.5x predicted).
2. Is it noise? If defaults were independent, the standard deviation of the count at 3% is about 24, so 900 is about 12 standard deviations above 600. But defaults are not independent. With a small pairwise default correlation of 0.001 the gap is only about 2.7 design-effect units, so a common economic shock is plausible. Do not call it noise and do not call it proof of a broken model.
3. Check calibration by score band and by segment, not only the average. Plot predicted versus observed default rate by decile and by product and vintage.
4. List causes and test each: macro shock, mix shift towards riskier applicants, drift in a key feature, changed default or label definition, data pipeline change, selection effect from approvals (reject inference), seasoning (young loans default later), underwriting policy changes.
5. Decide. If the ratio is similar across bands (a level shift) and AUC holds, recalibrate: fit a new intercept (and maybe a slope) on recent matured outcomes; in a simulation with an AUC of about 0.80 recalibration leaves AUC unchanged. If some segments are far off, or a key feature drifted, rebuild or add segment-specific calibration.
6. Governance: this is a model-risk event. Write up the issue, the evidence and the proposed fix; the model validation function reviews, the owner approves, and the change is logged with before and after metrics. Ask the risk, finance and governance teams about provisioning impact, thresholds for when a recalibration needs formal approval, and documentation; I do not state the rules.
7. Interim: use a conservative overlay or tighter cut-off if the business agrees, and monitor monthly.
8. Monitoring afterwards: predicted versus observed by band monthly, population stability on key features, and a trigger (for example a ratio outside an agreed band for two quarters).

**Metrics:**
- Calibration ratio = observed default rate / mean predicted PD = 4.5% / 3.0% = 1.5.
- Expected loss = sum over loans of PD x EAD x LGD; observed-default loss = defaults x EAD x LGD at the assumed LGD (not realised losses).
- Calibration by band = observed / predicted per decile.
- Discrimination: AUC (0.80 before and after recalibration).
- Guardrails: approval rate, provisioning change, stability of ranking after recalibration.

**Risks:**
- Recalibrating on one bad year bakes the shock in; use a long-run anchor or overlay.
- A single intercept shift will not fix band-specific errors (in my simulation the ratio was 2.4 in the safest decile and 1.35 in the riskiest under a pure logit shift).
- LGD is assumed; the 4,500,000 is not a realised loss.
- Immature loans can understate defaults; confirm outcomes are matured.

**What the interviewer scores:**
- Strong: gets 3.0M, 4.5M and 1.5M, and states LGD is an assumption.
- Strong: separates ranking (AUC) from level (calibration) and checks by band.
- Strong: gives a decision rule between recalibrating and rebuilding, and a governance path.
- Weak: "AUC is fine so the model is fine"; "retrain from scratch immediately"; legal claims.

**Example:** Illustrative numbers from the run. A simulated model with AUC about 0.80 and mean PD 3.0% faced 890 defaults; after an intercept recalibration its mean PD was 4.45% and AUC stayed 0.804, with expected loss 4,450,000.
- Weak: "The model underpredicts, so we need a new model."
- Strong: "Expected loss is 3.0M predicted against 4.5M from observed defaults at an assumed 50% LGD. AUC is unchanged, so ranking works; the level is off by a factor of 1.5. I would check by decile and by vintage, recalibrate if the miss is a level shift, and take it through model validation with the finance and risk teams."

<<CODE>>

<<OUTPUT>>

**Follow-ups:**
- *How would you tell macro from model failure?* Compare with peer portfolios or lenders, check the same-vintage behaviour across segments, and see whether the miss is uniform across bands.
- *Is a 1.5x miss bad if provisioning already covers it?* Ask finance and risk; it still needs documenting and monitoring.
- *Would you also recalibrate LGD?* Check realised recoveries separately; do not hide a PD miss inside an LGD change.
- See also Book 6 Part 2, Q14 (a classifier with stable AUC 0.82 whose probabilities have drifted) for the generic recalibration-versus-retrain argument.

**Common mistakes:**
- Calling the observed-default loss "the realised loss" when LGD is assumed.
- Declaring significance without a design effect for correlated defaults.
- Recalibrating without checking bands or segments.
- Skipping the governance step.
