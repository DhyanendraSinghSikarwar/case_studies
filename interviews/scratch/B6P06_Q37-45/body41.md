**Say this first (1 line):** I cannot honestly promise 90% yet, because accuracy means nothing without the baseline and label quality, so I commit to a two-week discovery with a stated date for a target and a range.

**Clarifying questions:**
- What decision does the model drive and what do errors cost? Why: accuracy may be the wrong metric.
- What is the positive rate? Why: at 10% a model that says "no" always gets 90%.
- How are labels produced and how noisy are they? Why: noise caps measurable accuracy.
- What is today's baseline (rules, human)? Why: a target should be relative to it.
- When is the figure needed and for what purpose? Why: a date for the estimate may be all they need.

**Approach:**
1. In the meeting: "I want to hit a number we can defend, and I have not seen the data. I will give you a target and a range by a specific date."
2. Explain with one example: if only 10% are positive, a model that never flags anything scores 90%.
3. Commit to a short discovery: label audit, class balance, baseline, and a first simple model.
4. Propose the metric tied to the decision (for example recall at a review budget) and agree what "good" means.
5. Deliver the estimate with a range and the assumptions that would move it.
6. Put the agreed target, and the conditions for revisiting it, in writing.

**Metrics:** Baseline accuracy = max(p, 1-p) for positive rate p. Lift over baseline. Label noise ceiling: with 8% wrong labels a perfect model measures about 92%. Guardrail: report the metric on a time-split holdout.

**Risks:**
- Saying "no" with no alternative sounds obstructive.
- A target made up in the room becomes a promise.
- Discovery with no end date.

**What the interviewer scores:**
- Strong: refuses to commit politely, explains in one example, commits to a date and a process.
- Weak: caves to 90%, or lectures about accuracy.

**Example:** Illustrative: at positive rates of 1%, 5%, 10%, 50%, 90% the always-majority baseline is 99%, 95%, 90%, 50%, 90%. A perfect model scored against labels with 8% errors measures about 92%.
- Weak: "Sure, we will aim for 90%." / "Accuracy is a bad metric."
- Strong: "I will give you a committed target and range in two weeks, after I check labels and the baseline. If the positive rate is near 10%, 90% is what doing nothing scores."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- What if the VP insists? Offer a conditional: "90% if labels and baseline look like X; I will tell you at the two-week review if not."
- Is it ever fine to give a rough number early? Yes, as a labelled range with assumptions.

**Common mistakes:** Committing without data. Refusing with no date. Using jargon in the meeting. Forgetting the decision metric.
