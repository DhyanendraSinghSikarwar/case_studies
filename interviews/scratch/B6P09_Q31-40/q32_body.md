**Say this first (1 line):** About 400 of the 1,000 flagged sellers are fraudulent as a projection (the audit is a sample, so roughly 300 to 500), the queue takes 5 weeks at 200 a week, and random order finds about 80 in week 1; I would order by expected fraud harm per review, not at random.

**Clarifying questions:**
- Was the audit of 100 truly random among the 1,000 flagged, and who judged "fraudulent" (the same investigators)? A non-random or inconsistent audit breaks the 40%.
- Do I have the model score for each audited seller? It lets me measure how precision changes with score.
- How long does fraud keep costing us while a seller waits (daily losses, buyer harm)? It sets the value of speed.
- Can a review be cheap (auto-triage) for some sellers? Review time per seller may differ.
- What is the action on a confirmed seller (suspend, hold funds, ask for documents), and what is the cost of wrongly suspending a good seller? It sets the cost of false positives.

**Approach:**
1. Compute the projection and its range. 40 of 100 is 40%, so 0.40 x 1,000 = 400 fraudulent among the flagged. A 95% interval on 40 of 100 is 30.4% to 49.6%, so 304 to 496 sellers.
2. Weeks to clear: 1,000 / 200 = 5 weeks.
3. Random order, week 1: 200 reviews x 40% = 80 fraudulent expected (hypergeometric, standard deviation about 6.2). If the true number is 304 or 496 the week-1 mean is 60.8 or 99.2.
4. Better order: rank by expected harm avoided per review minute = P(fraud) x exposure (money at risk, buyers affected, growth rate of sales) / expected review time. Use the model score only after checking it is calibrated on the audited sample.
5. Use the audit to calibrate: tabulate fraud rate by score band. With an invented split (high band 21 of 30, middle 13 of 35, low 6 of 35) the high band is 70% and reviewing it first gives 140 expected in week 1 instead of 80.
6. Keep a random slice of each week's review (for example 10%) so the model is evaluated on a fair sample and the labels do not become biased.
7. Fast actions for the top of the queue (hold payouts or limit listings pending review) can reduce damage before the investigator arrives; ask the trust and policy team what actions are allowed.
8. Re-score the queue daily as new signals arrive; the order is not fixed for 5 weeks.

**Metrics:**
- Precision of review = confirmed fraud / sellers reviewed.
- Fraud found per investigator-hour, and expected loss prevented per week (sum of P(fraud) x exposure for reviewed sellers).
- Time to action for confirmed fraud (median days from flag to action).
- Guardrails: false-suspension rate (good sellers actioned / sellers actioned), appeals overturned, and fraud rate in the random slice.

**Risks:**
- Projection from 100 audits has a wide range, about +/- 10 points.
- Ordering by score only finds what the model already likes; sellers it misses are never audited (keep the random slice).
- If fraudsters adapt to the order, the top band becomes less pure.
- Optimising fraud counts alone can starve large exposure sellers; use harm, not count.

**What the interviewer scores:**
- Strong: 400, 5 weeks, 80 in week 1, and says "sample, projection, range".
- Strong: orders by expected harm per review and keeps a random audit slice.
- Strong: separates fraud count from money at risk.
- Weak: "review in order of arrival"; no mention of uncertainty; ignores false suspensions.

**Example:** Illustrative numbers. In the run below the projection is 400 (304 to 496), 5 weeks, 80 expected in week 1 under random order and 140 when the high-score band goes first. Ordering by probability times exposure finds fewer fraudsters in week 1 (about 110 versus 140 in my simulated exposures) but stops about 440,000 of expected loss instead of about 246,000.
- Weak: "We have 400 frauds, so we need 2 weeks of work."
- Strong: "The audit suggests about 400, plausibly 300 to 500. At 200 reviews a week that is 5 weeks, and random order finds about 80 in week 1. I would rank by fraud probability times money at risk per review minute, and keep a random 10% slice so the model stays honest."

<<CODE>>

<<OUTPUT>>

**Follow-ups:**
- *Is the 40% the precision of the model?* Only for the flagged group at the audit threshold; it tells nothing about unflagged sellers.
- *What if two weeks of delay matters a lot?* Add a time-decay weight, or take low-effort holds on the top band at once.
- *How do you get labels without bias if you only review the top?* The random slice plus periodic reviews of the unflagged.

**Common mistakes:**
- Saying "400 are fraudulent" as a fact.
- Reviewing in random order because it is "fair".
- Optimising count rather than harm.
- Forgetting the cost of wrongly acting on honest sellers.
