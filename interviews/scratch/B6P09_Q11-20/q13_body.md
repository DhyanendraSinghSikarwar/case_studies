**Say this first (1 line):** Training on approved applicants only teaches the model about the people the old policy liked, so it is biased and overconfident on the 70,000 rejects; reject inference can narrow the gap but not close it, and the clean fix is a small, capped, randomised approval of near-cutoff rejects to get real outcomes.

**Clarifying questions:**
- How were approvals decided: a score cutoff, rules, manual overrides? A deterministic rule on observed features is much easier to correct than a human override on unobserved information.
- Were defaults on rejects ever observed elsewhere, for example through a credit bureau record of loans they took at another lender? Whether we may use that is a question for compliance and the privacy team.
- Is the 12-month default definition fixed? A different window changes the 4% and the scenario.
- What is the downside budget: how much loss are we willing to carry for learning? It sizes the experiment.
- Which decisions will the new model drive: approve, limit, price? Each needs a different part of the risk range.

**Approach:**
1. State the arithmetic. Approved: 30,000 (30%), 1,200 defaults, 4%. If rejects defaulted at 3 times that, 12% of 70,000 = 8,400 defaults, and the population rate = (1,200 + 8,400) / 100,000 = 9.6%. That is one scenario: the ratio is not measured. With a ratio of 1 the population rate is 4%, with 5 it is 15.2% (see the run).
2. Explain the bias. The approved set is truncated on the old score, so the model sees only the low-risk end. Two consequences: its measured AUC and bad rate are for approved customers, not applicants, and it extrapolates into a region it has never seen. In the simulation a linear fit on approved applicants predicts a 6.0% default for rejects when the real rate is 10.9%.
3. List the reject-inference options and their limits. Treat rejects as bad: crude, inflates risk. Extrapolation or parcelling (score rejects with the approved-trained model and assign outcomes by band): assumes the thing you are trying to learn, so it adds no information. Augmentation or reweighting by approval probability: fixes bias only if approval depended on observed variables (a missing-at-random assumption). Use of outside outcomes (bureau data on rejects): helps if allowed and relevant. All of these need testing on a period where outcomes are known; none replaces data.
4. Run the low-risk experiment. For a small random share of near-cutoff rejects (not the riskiest), approve with a small limit and a cap on total exposure. Randomisation makes the outcomes unbiased for that band. In the run: 500 people at a limit of 1,000 is an upper bound of 500,000 of exposure and gives about +/- 1.2 points of default-rate precision at a 1.8% observed rate (illustrative).
5. Get approvals for the experiment from credit risk and compliance (fairness review, any rule on random approvals is for them to say). Pre-agree a stop rule on cumulative losses.
6. Use the results: refit on approved plus the experiment (weight the experiment by 1 / probability of selection), re-check calibration on the experimental band, and re-run the cutoff analysis. Do not extrapolate beyond the band you sampled.

**Metrics:**
- Default rate = defaults within 12 months / accounts opened, for matured cohorts only.
- Calibration by score band on the experimental slice: predicted defaults / observed defaults.
- Population AUC on a fair holdout (approved plus experimental slice, weighted), not approved-only AUC.
- Experiment guardrails: exposure = accounts x limit (upper bound, all drawn, no recovery); realised loss versus pre-agreed cap.

**Risks:**
- Treating 9.6% as the answer. It is one scenario from an assumed ratio of 3.
- The experiment covers only near-cutoff rejects; it says little about the worst 50,000.
- Selection by hidden information (an underwriter's note) cannot be corrected by reweighting on model features.
- Economic conditions change between the matured cohort and today, so a cohort result may not transfer.

**What the interviewer scores:**
- Strong: computes 9.6% and says it is one scenario with a sensitivity range.
- Strong: names truncation and extrapolation, and says inference methods rest on assumptions they cannot test alone.
- Strong: proposes a bounded, randomised exploration with a loss cap and compliance sign-off.
- Weak: "label rejects as bad" or "use the model to label rejects" without noting the circularity.

**Example:** Illustrative. Weak versus strong:
- Weak: "I would score the rejects with the model and use those as labels."
- Strong: "Scoring the rejects with a model trained on approvals just returns what the model already believes. The 9.6% is a scenario from an assumed ratio of 3; at a ratio of 1 it is 4% and at 5 it is 15.2%. I would approve a small random slice of near-cutoff rejects at a low limit, cap the total exposure at 500,000 for 500 people, and agree the design with credit risk and compliance first. Then I would refit using weights and check calibration on that slice."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- Can you validate a reject-inference method? Only on a setting where you know the outcomes, for example a period where the cutoff was temporarily relaxed, or the experimental slice; otherwise you cannot.
- What if the experiment is not allowed? Use the approved data with a conservative, monotone model, do not extrapolate the cutoff downward, and monitor early-arrears on any new approvals.
- Does the bias affect fairness reviews? Yes, the group mix of rejects is unobserved; raise it with the compliance and model-risk teams.

**Common mistakes:**
- Reporting approved-only AUC as the model's AUC.
- Treating the 3x ratio as a measured fact.
- Running the experiment on the riskiest rejects, or with no loss cap.
- Reweighting on features when approval used information the model does not have.
