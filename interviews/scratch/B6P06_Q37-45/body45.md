**Say this first (1 line):** I agree that routine query answering and boilerplate should be automated, so I volunteer those, and I defend the work that decides what to measure and whether results can be trusted, because unsupervised AI answers are still wrong too often.

**Clarifying questions:**
- What outcome does leadership want: cost, speed, or fewer requests queued? Why: automation can serve each differently.
- What share of team time is routine versus judgement? Why: sizes the real saving.
- What does a wrong answer cost in these workflows? Why: it sets how much review is needed.
- What accuracy have the tools shown on our tasks? Why: Q40 of this part shows a 74% text-to-SQL result, well below a 95% bar.
- Who is accountable when an automated answer is wrong? Why: accountability is the part that stays human.

**Approach:**
1. Agree with the premise where it is right: much routine work will be automated.
2. Volunteer a list: routine query answering on certified metrics, dashboard refreshes, boilerplate code, first-draft EDA and documentation.
3. Quantify net savings after review: for example 213.75 of 1,000 hours a month (21%).
4. Defend: problem framing, metric definitions, experiment and causal design, validation and monitoring of models, data quality, and being accountable for decisions.
5. Propose a one-year plan: automate in tiers, measure error, promote a task only when its measured accuracy meets the bar.
6. Reframe the team as the owner of quality and decisions, with AI as a tool.

**Metrics:** Net hours freed = hours x automated share x (1 - review overhead). Error rate of automated outputs on an audit sample. Time to answer. Guardrails: wrong-answer rate, incidents from unreviewed output.

**Risks:**
- Cutting the review layer and shipping confident wrong answers.
- Sounding defensive, which reads as protecting jobs.
- Losing the people who define metrics and catch errors.

**What the interviewer scores:**
- Strong: concedes what is true, offers a concrete automation list with numbers, defends specific tasks with reasons, uses evidence.
- Weak: "AI cannot do what we do", or giving up the whole scope.

**Example:** Illustrative mix of 1,000 hours: routine queries 350, boilerplate 150, design and causal work 250, modelling and validation 200, advice 50. Automate 60% of routine and 50% of boilerplate with a 25% review overhead: net saved 157.5 + 56.25 = 213.75 hours, 21.4%. Half the work remains: judgement and accountability.
- Weak: "Agents cannot replace data scientists."
- Strong: "I would automate the routine query and boilerplate work, which frees about a fifth of our time after review. I would keep metric design, experiments and validation, because the tool is wrong 26 times in 100 on our test."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- What if the tools improve fast? Re-test quarterly and promote tasks as they pass.
- How do you show value? Decisions improved and errors prevented, with measured examples.

**Common mistakes:** Denying the change. Offering to cut without a plan. Citing no numbers. Treating review as free.
