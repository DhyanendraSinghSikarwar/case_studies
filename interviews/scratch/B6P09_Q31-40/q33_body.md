**Say this first (1 line):** I would define harm by clinical severity and by whether the error reached the patient record after the clinician signed, measure it with a blinded severity-graded audit compared with human-written summaries, and let clinical safety set the pass rate before wider rollout; 7% and 3% on 200 are samples with wide ranges.

**Clarifying questions:**
- What is the baseline: how often do human-written summaries omit a medication? It sets whether 7% is better or worse than today.
- Were the two clinicians blinded to source (human or LLM), and how often did they agree? Agreement shows whether the labels are reliable.
- Can one summary have both errors, and which medicines were missing? The 14 and the 6 may overlap, so any-error is between 7% and 10%.
- Did the reviewing clinicians use the same checking time as they will in production? A careful audit is slower than a busy ward sign-off.
- Who owns the decision (clinical safety officer, not the data team)? It decides who sets the threshold.

**Approach:**
1. State what the sample shows. 14 of 200 is 7.0% (95% Wilson 4.2% to 11.4%); 6 of 200 is 3.0% (1.4% to 6.4%). The "4 of 10 minutes" saving is what clinicians say; I treat it as a claim and measure it.
2. Define harm in tiers with clinical safety: omitted medication by drug class and by whether it matters (for example a stopped or new high-risk drug versus a minor supplement), invented detail by whether it changes a decision, and "reached the record" after sign-off versus caught in review. Weights belong to clinicians, not to me.
3. Measure per summary and per medication: errors / medications in the source (a per-medication denominator), and summaries with any error / summaries audited (per-summary).
4. Audit design: random sample stratified by ward and complexity, two blinded reviewers, adjudication of disagreements, human-written summaries mixed in as a baseline.
5. Rollout bar: ask clinical safety for the target. Show them what is testable: with zero errors seen, 299 clean audited summaries are needed to show the true rate is below 1% with 95% confidence, 149 for 2% and 59 for 5% (one-sided). Any error found raises the number. To pin a 7% rate within +/-1 point takes about 2,500 audits.
6. Staged rollout: shadow mode (draft not shown), then one ward with 100% audit, then widen; stop rules agreed in advance (any severe omission reaching the record pauses the rollout).
7. Product guards: show the medication list from the source side by side with the draft, flag medicines that appear in the record but not the draft, and make the clinician confirm the medication section explicitly.
8. Ask clinical safety and compliance (via their processes): who is accountable for a signed summary, how errors are reported and logged, patient-data handling for the drafting service, and what must be disclosed to patients. I make no claims about the rules.

**Metrics:**
- Medication omission rate (per summary) = summaries with at least one omitted medication / audited summaries (14 / 200).
- Per-medication omission rate = omitted medications / medications in the source (needs a count I do not have in the prompt).
- Invention rate = summaries with an invented detail / audited summaries (6 / 200), split by severity.
- Reached-the-record rate = errors still present after sign-off / audited summaries.
- Net time saved = (usual minutes - drafted-plus-review minutes) / usual minutes; compare with the claimed 4 of 10 (40%).
- Guardrails: reviewer agreement (kappa), error rate by ward and patient complexity.

**Risks:**
- Automation bias: clinicians sign what looks fluent, so signing is not a safety net by itself.
- Time saving can vanish if careful checking takes the saved minutes (4 saved minus 3 extra checking minutes leaves 1 minute, or 10%, in my illustration).
- Errors cluster in complex patients; an average hides them.
- Audit reviewers may be less careful after the first 50.

**What the interviewer scores:**
- Strong: severity-weighted harm, "reached the record" distinction, and a human baseline.
- Strong: honest about sample size and uses interval or zero-error sample sizes.
- Strong: hands the pass-rate decision to clinical safety and asks questions instead of asserting rules.
- Weak: "7% is low, ship"; "accuracy of the LLM" with no harm definition; claims about regulation.

**Example:** Illustrative numbers from the run. With the prompt's 200 audits: 7% omission (4.2% to 11.4%), 3% invention (1.4% to 6.4%). If signing clinicians catch 90% of errors, about 70 omissions and 30 inventions per 10,000 summaries reach the record; at a 50% catch rate, 350 and 150.
- Weak: "Only 3% hallucinate, and clinicians sign everything, so it is safe."
- Strong: "7% omission and 3% invention are samples with wide ranges. I would grade by severity, count what survives sign-off, compare with human summaries, and ask clinical safety for the rollout bar. To show under 1% with zero errors I would need about 300 clean audits."

<<CODE>>

<<OUTPUT>>

**Follow-ups:**
- *Is a lower error rate than humans enough?* Possibly not alone; different error types (fluent inventions) can be worse. Safety decides.
- *Why a per-medication denominator?* A summary with 15 medicines has more chances to miss one.
- *What if time savings are real but errors rise on complex patients?* Restrict to simple cases first.

**Common mistakes:**
- Treating the clinician signature as the safeguard.
- Reporting 7% and 3% as population rates without intervals.
- Adding 7% and 3% to get 10% (overlap unknown).
- Setting the acceptable threshold in the data team.
