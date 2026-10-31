**Say this first (1 line):** Correlated features make per-feature attributions unstable, so I would explain the decline in stable reason groups (income and tenure as one "income and job stability" reason), average attributions over many retrains, test the stability on declines before launch, and ask compliance whether the wording and grouping are acceptable.

**Clarifying questions:**
- Do the reasons have to reflect the real drivers of this model, or can they be mapped from a simpler scorecard? It decides whether grouping is enough or we need a different model form.
- Which wording is fixed by compliance (a reason-code library) and which can I change? It tells me where I can group features.
- Is the flip between two retrains, or between two runs on the same model? Retrain instability is a data issue; same-model instability is a method issue (for example sampling in the attribution).
- How was the 30 of 100 chosen (the first 100 declines, or random)? A sample of 100 gives a wide range.
- Are the 4 reasons ranked or just a set? A ranked list needs stable order; a set only needs stable membership.

**Approach:**
1. Size the problem. 30 of 100 is a sample. The 95% Wilson interval is about 22% to 40%, so the true flip rate is probably between a fifth and two fifths. Also measure the overlap of the whole 4-reason set, not only the top reason.
2. Find the cause. With a correlation of 0.85 the model can put credit on income or on tenure almost interchangeably. Check the spread of the two coefficients across bootstrap retrains: they move in opposite directions (negative correlation between the two coefficients).
3. Group correlated features into one reason group before ranking (income + tenure = "income and employment stability"). Rank groups, not single features.
4. Average attributions over many bootstrap retrains (bagging) and use the average for the reason, so one retrain does not decide the wording.
5. Map each group to a fixed reason code with plain wording written with compliance, so the text cannot change between retrains.
6. Validate: (a) stability: top-reason flip rate and 4-reason set overlap across retrains on a fixed set of reviewed declines; (b) fidelity: if you remove the named reason feature(s), does the score move in the right direction (counterfactual check); (c) human review: a reviewer reads 100 declines and says whether each reason is sensible for that applicant.
7. Put a stability gate in the retrain pipeline: do not promote a retrain if the flip rate on the reference declines is above an agreed limit.
8. Ask compliance (and legal, via the usual route) about: the exact reason wording, whether grouped reasons are acceptable, how many reasons and in what order, how reasons must relate to the model, and how long reason mappings must be kept. I do not assert any rule; I bring the evidence and ask.

**Metrics:**
- Top-reason flip rate = declines whose top reason differs between retrain A and B / declines reviewed (here 30 / 100 in the prompt).
- Set overlap = mean over declines of |A ∩ B| / |A ∪ B| for the 4-reason sets (Jaccard).
- Fidelity = share of declines where removing the cited feature group lowers risk (counterfactual check).
- Guardrails: model discrimination (AUC) must not fall when we regularise or group; reason coverage (declines with at least one valid reason).

**Risks:**
- Ranking by coefficient times deviation on a correlated pair is arbitrary; two retrains can both be "right".
- Grouping can hide a driver the applicant could act on (income versus tenure advice differs).
- Averaging over retrains gives stable but possibly less faithful reasons for a single model; document which model the reasons explain.
- Plain-language wording that sounds stable may still imply something untrue; get it reviewed.
- The 100-decline sample may not cover thin-file applicants.

**What the interviewer scores:**
- Strong: names correlated features as the cause, sizes the 30 of 100 with an interval, and proposes grouping plus averaging with a measured result.
- Strong: separates stability from fidelity and tests both.
- Strong: asks compliance about wording and does not state regulations as facts.
- Weak: "use SHAP" with no stability check; "drop one of the two features" without checking AUC; quoting legal rules from memory.

**Example:** Illustrative numbers, from the run below. A logistic model on 1,500 simulated applicants, income and tenure correlated at about 0.85, reasons for 100 highest-risk applicants from two bootstrap retrains.
- Raw top reason differs for 47 of 100 (the prompt's 30 of 100 is the same kind of number); grouped income and tenure: 12 of 100; bagged (60 resamples each): 17 of 100.
- Weak: "Income is the top reason for most people, we ship the SHAP output."
- Strong: "On 100 declines the top reason changes in 30, so the true rate could be 22% to 40%. Income and tenure are correlated at 0.85, so I would report them as one reason group and average over retrains. In my test that cut the flip rate from 47 to 12 of 100, and grouping changes only the explanation, so AUC is untouched. I would ask compliance to approve the group wording."

<<CODE>>

<<OUTPUT>>

**Follow-ups:**
- *Why not just drop tenure?* You lose information and AUC may fall; test it. Also the applicant loses an accurate reason. Grouping keeps both.
- *Could a monotone or scorecard model make this easier?* Often yes: constrained or additive models give fixed point contributions. Test AUC cost against reason stability.
- *How do you handle the reviewer who says the reason is wrong for this person?* Counterfactual check plus a log; repeated complaints become a test case in the stability gate.

**Common mistakes:**
- Treating one retrain's ranking as the truth.
- Reporting a flip rate from 100 declines with no interval.
- Grouping features without checking that the group wording is accurate for each member.
- Quoting legal requirements as facts instead of asking compliance.
