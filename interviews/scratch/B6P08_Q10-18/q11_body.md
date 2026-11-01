**Say this first (1 line):** 216 minutes minus 205 used, counting the current outage, leaves 11 minutes (5.1%), and it burns one minute per minute while we are down, so freeze every non-essential release and ship the fix only with a fast rollback and a small first step.

**Clarifying questions:**
- Is the objective measured on a rolling 30 days or the calendar month? On a rolling window the 95-minute outage ages out later; on a calendar month the budget resets on the first.
- Is the outage a full outage or partial (some requests failing)? Partial downtime counts in proportion, so the burn is slower.
- What does the fix change: config, a model version, infrastructure? A risky fix can add a second outage.
- Who owns the budget policy (a freeze rule written down, or only a norm)? It decides whether I can say "no release" or can only advise.
- Is there a contractual SLA with credits behind the 99.5%? The internal objective is a goal; the contract is a promise.

**Approach:**
1. First 15 minutes: mitigate before diagnosing. Roll back the last change, fail over, or serve a fallback. Open an incident channel, name an incident lead and a communicator, and post a first status line.
2. Do the math in the open: budget 216 min, used 70 + 95 + 40 = 205, left 11. At full outage the budget runs out at outage minute 51, in 11 minutes. After that, every minute is over objective.
3. Release policy: freeze feature and model releases until the budget recovers or the leadership explicitly accepts the risk. Only fixes for the outage, security fixes and rollbacks go out.
4. The fix you are about to ship: ship it, because staying down costs 1 minute of budget per minute; but ship it small and reversible. First step to 5 to 10% of traffic or one replica, watch error rate for a pre-agreed time (for example 10 minutes), then widen. Roll back if the error rate is above the pre-outage baseline by more than a set margin, or latency p99 doubles. Escalate to the engineering lead if the first step does not work or the fix needs a risky data or schema change.
5. First day: restore service, write a customer note, and keep the freeze until a review. Confirm the real downtime from monitoring, not from memory.
6. Next quarter: look at what repeats across 3 outages in a month (70, 95, 40+ minutes): bad deploys, a single dependency, or slow detection. Fund the top cause. Add burn-rate alerts (fast and slow) so we get paged at 2% of budget gone in an hour, not at 100%.
7. Blameless postmortem: three outages in a month is a system signal. Ask what made each outage long (detection, diagnosis, rollback time), not who pushed the change.

**Metrics:**
- Error budget = (1 - objective) x window minutes = 0.005 x 43,200 = 216 minutes.
- Budget remaining = budget - downtime so far (70 + 95 + 40) = 11 minutes.
- Burn rate = observed bad-minute rate / allowed rate; a full outage is 200x (1 / 0.005).
- Time to detect and time to mitigate per outage (the two parts we can shorten).
- Guardrail: change-failure rate of releases during a freeze must be zero for non-essential changes.

**Risks:**
- Shipping a rushed fix to "save budget" can create a longer outage.
- The numbers are only as good as the outage clock: when did it start, when did users see it?
- A freeze with no end date makes teams hide risky work. Write the exit rule (budget back above a level, for example 20%).
- An internal objective is not an SLA; do not promise customers more than the contract says.

**What the interviewer scores:**
- Strong: gets 11 minutes, 5.1%, and notices the current outage is still burning budget.
- Strong: balances speed and caution: small, reversible fix with explicit rollback criteria.
- Strong: freeze with owner and exit rule; blameless review of a pattern of three outages.
- Weak: "we have budget left, so keep releasing"; or "fix it immediately for everyone" with no rollback plan.

**Example:** Illustrative. Weak versus strong:
- Weak: "We have used 165 minutes, so we are fine, I will push the fix to everyone."
- Strong: "Counting the live outage we have used 205 of 216, so 11 minutes are left, about 5%. At full outage that is gone in 11 minutes. I would stop all other releases, push the fix to 10% first, and roll back if errors rise above baseline. After this, we hold a blameless review of the three outages together."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- The budget is gone; what now? Freeze non-essential releases, spend engineering time on reliability work, and report the breach, until the window recovers.
- Is a partial outage counted? Yes, in proportion to failing requests; use a request-based SLI if you can.
- Should the model be rolled back if only the fix is uncertain? Roll back when the previous version is known good and the outage began after the change; otherwise fix forward in small steps.

**Common mistakes:**
- Forgetting to include the outage still in progress.
- Treating a 30-day budget as resetting weekly.
- Shipping the fix to 100% with no rollback criteria.
- Blaming the engineer who deployed.
