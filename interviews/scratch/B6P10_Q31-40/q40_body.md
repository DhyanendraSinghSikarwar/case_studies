**Say this first (1 line):** The best subset that fits 36 person-weeks is projects A and B (34 weeks, 70 lakh projected), but it leaves only 2 weeks of slack, so I would present it with a buffered alternative and say which risks would flip the choice.

**Clarifying questions:**
- Are the benefits projections or measured, and by whom? They are illustrative projections, so each carries a range.
- Are person-weeks interchangeable between people (skills, data access)? A project that needs one skill cannot absorb spare weeks from another.
- What else takes time (on-call, maintenance of live models, reviews)? Planning at 100% is a common failure.
- Are there dependencies between projects (shared data pipeline)? A cheap project may unlock a big one.
- When do benefits start and what is the cost of delay? Annual benefit in year one may be much lower.

**Approach (spoken framework, about 45 minutes: clarify 5, metrics 4, data 4, baseline 4, selection model 10, evaluation of risks 7, plan and launch 6, monitoring and cost 5):**
1. Clarify and frame: a portfolio choice under a capacity limit, a knapsack problem.
2. Metrics and guardrails: projected benefit, benefit per person-week, probability of delivery, and a buffer for existing models.
3. Data: ask owners for the evidence behind each benefit number and the data readiness.
4. Baseline first: rank by benefit per person-week (B 2.14, A 2.0, E 2.0, D 1.75, C 1.6).
5. Selection: capacity 3 x 12 = 36; all five cost 58. Test every subset: A + B = 34 weeks, 70 (best); A + C + E = 36 weeks, 68; A + D + E = 34, 66; B + C + D = 32, 60. At 80% planned capacity (28.8) the best is B + D + E, 28 weeks, 56 lakh. Also note that A (20 weeks) and B (14 weeks) each need at least two people in a 12-week calendar.
6. Evaluation of risk: if A delivers only half its benefit (20 instead of 40), the best subset becomes B + C + D (32 weeks, 60); if the data for A is not ready, the best set without A is B + C + D (32 weeks, 60).
7. Plan: stage gates at week 4 and week 8 (a data check and a baseline result) and a pre-agreed rule for dropping a project.
8. Monitoring and cost: weekly burn against the plan, measured benefit after launch to correct future estimates; the cut list is written down in advance.

**Metrics:**
- Total projected benefit of the chosen set = sum of benefits (70 lakh per year for A + B), a projection.
- Capacity used = person-weeks planned / 36 (94% for A + B).
- Benefit per person-week = benefit / cost; guardrail: planned buffer for maintenance (for example 20%).

**Risks:**
- Benefit projections are optimistic and uncorrelated with effort.
- Zero slack: any slip drops a project.
- Dependencies and skills: weeks are not interchangeable.
- Large projects carry more delivery risk than the point estimate shows.

**What the interviewer scores:**
- Strong: checks all subsets, gets A + B at 70, and then argues against planning at 100%.
- Strong: names which risk changes the choice (A halves, data not ready).
- Weak: picks by benefit alone or by gut, with no capacity arithmetic or buffer.

**Example:** Illustrative numbers. 3 x 12 = 36 weeks; A + B = 20 + 14 = 34 weeks, 40 + 30 = 70 lakh; A + C + E = 36 weeks, 68 lakh.
- Weak: "Take the two biggest ones, they have the most benefit."
- Strong: "A plus B uses 34 of 36 weeks for 70 lakh projected, the best fit. But that is 94% of capacity, so I would propose B, D, E at 28 weeks and 56 lakh as the safer plan, and start A only if the week-4 data check passes."

<<CODE>>

<<OUTPUT>>

**Follow-ups:**
- *What would make you drop A?* Data not ready by week 4, or evidence the benefit is under about half of its projection.
- *How do you handle a new urgent request?* Use the buffer; if it is larger, drop the lowest benefit-per-week project and tell stakeholders.

**Common mistakes:** Ranking only by benefit. Planning at 100% capacity. Treating projections as certain. Forgetting that a 20-week project cannot be done by one person in 12 weeks.
