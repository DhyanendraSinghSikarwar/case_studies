**Say this first (1 line):** An AUC of 0.82 on one team's data and 0.83 on another's cannot be compared, so I propose one shared holdout, scored by a neutral party with both teams agreeing the rules first.

**Clarifying questions:**
- What decision will the model drive (who is contacted, what is offered)? Why: it sets the metric, for example lift at a contact budget instead of AUC.
- Do the two teams define churn the same way (window, label, population)? Why: different definitions make AUC meaningless to compare.
- Can both models score the same recent customers? Why: a common out-of-time holdout is the fair test.
- What are cost, latency and maintenance for each? Why: if they tie on accuracy, these decide.
- Who has the authority to pick one? Why: the process needs a decision owner agreed in advance.

**Approach:**
1. Agree the rules with both leads before anyone sees results: label definition, population, time split, metric, and tie-break rules.
2. Build one holdout neither team trained on, from a later time window than all training data.
3. Both teams submit scores. A third person computes the metrics.
4. Report AUC plus the business metric (for example churners caught in the top 10%), with a paired bootstrap interval on the gap.
5. If the gap is inside the noise, decide on cost, simplicity, explainability and ownership, or blend them.
6. Give both teams credit in the readout. Keep the best features and ideas of each.

**Metrics:** AUC on the shared holdout = probability a random churner scores above a random non-churner. Gap CI = percentile interval of the paired AUC difference over bootstrap resamples. Business metric = churners in the top 10% of scores / all churners. Guardrails: same label definition, no tuning on the holdout, calibration check if scores drive offers.

**Risks:**
- Each team's data has a different population, so its AUC reflects its own mix.
- A holdout one team helped build looks rigged. Use a neutral owner.
- Declaring a winner on a 0.01 gap that is noise.

**What the interviewer scores:**
- Strong: agrees rules before results, uses a shared out-of-time holdout, shows a paired interval, and treats the politics as a process problem.
- Strong: recommends a blend or a cost-based tie-break when the gap is noise.
- Weak: "pick the higher AUC", or ignores the people involved.

**Example:** Illustrative: on a shared test set of 5,000 customers with 479 churners, A scores 0.823 and B 0.831, gap 0.008, 95% interval [-0.005, 0.021]. That includes zero, so I do not declare a winner on accuracy.
- Weak: "0.83 beats 0.82, so team B wins."
- Strong: "Those numbers come from different data. On one shared holdout the gap is under a point and the interval includes zero, so let us decide on cost and maintainability and keep the best parts of both."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- How big a gap would count? One whose interval excludes zero and that moves the business metric enough to matter, agreed before the test.
- What if the teams refuse the shared holdout? Ask the sponsor to mandate it, and offer them a say in its design.

**Common mistakes:** Comparing numbers from different datasets. Letting one team build the test. Choosing on AUC alone. Embarrassing the losing team publicly.
