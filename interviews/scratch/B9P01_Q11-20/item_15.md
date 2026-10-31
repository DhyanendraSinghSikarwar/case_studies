**Say this first (1 line):** I stay factual and own it: I contain the damage first, tell the right people early, find the cause with evidence, and then fix both the problem and the process that let it through.

**Structure:** STAR with a diagnosis thread (see "STAR and CARL" above); keep the technical reasoning visible.
- Situation and Task: what you owned, what failed or underperformed, how you found out, and the impact.
- Action: contain (roll back, pause, add a fallback), tell (who, when, what you said), diagnose (what you checked and ruled out: data drift, pipeline change, label delay, a bug), fix.
- Result: what recovered, what did not, the cost.
- Learning: a prevention you added, for example monitoring, a data check or a rollback plan.

**Strong sample answer (spoken):** Illustrative; replace with your own. "A model I owned started giving worse predictions after a pipeline change upstream. A monitoring alert showed the score distribution had shifted. First I paused the automatic use of the score and told my manager and the product owner what I knew and did not know. Then I compared recent inputs with training data and found one feature had changed its units. I fixed the mapping, backfilled the affected days, and told the same people the cause and the impact. Afterwards I added a data check on that input and a short runbook, and asked the upstream team to tell us about schema changes. The part I own is that I had no check on that feature before. That is what I changed."

**Weak version (and why it fails):** "The model failed because the data team changed something." Blame with no ownership, no sign you told anyone, and no prevention. Or the opposite: a failure so small it is not a failure, which looks like avoiding the question.

**What the interviewer scores:**
- Ownership without blame.
- Speed and order: contain, communicate, diagnose.
- Technical diagnosis, with evidence and ruled-out causes.
- Honest communication to the right people.
- Prevention: monitoring, tests, process.

**Make it yours:**
- Use a real failure you owned, even a modest one. Do not invent a dramatic one.
- Write the timeline: how you found out, who you told, what you did first.
- Be exact about the cause and what you did not know at the time.
- State the real impact, and only numbers you can back.
- Name the prevention you actually put in place.

**Follow-ups:**
- How did you tell stakeholders? "Short message: what happened, impact, what we are doing, next update time; no jargon."
- How could you have caught it earlier? "A distribution check on inputs and an alert on prediction drift."
- Was it your fault? "The cause was upstream, but not having a check was mine to fix, and I did."

**Common mistakes:**
- Starting with the cause and skipping containment.
- Blaming another team.
- Technical depth with no communication.
- Claiming the fix without evidence it worked.
- No change to the process afterwards.
