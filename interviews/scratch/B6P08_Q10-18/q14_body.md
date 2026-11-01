**Say this first (1 line):** The gap is borderline (z = 2.37, Fisher p about 0.04, with a lower interval end barely above zero), so I do not promote and do not panic: I hold the canary at 5%, inspect the errors, and decide by the rollback rule that should have been written before the canary started.

**Clarifying questions:**
- What kind of errors are they (5xx, timeouts, invalid output, wrong predictions)? A crash is a stop; a rare validation error may be a data issue.
- Are errors independent requests or clustered by customer, region or one bad input? Clusters shrink the real sample size.
- Is the control the same hour and traffic mix as the canary? Differences in mix create gaps without any model effect.
- What threshold did we agree before the canary started, and how long should it run? It decides whether this hour is a signal.
- How costly is one error (an annoyed user versus a failed payment)? It sets how tight the limit is.

**Approach:**
1. Compute the gap: canary 9 / 2,000 = 0.45%, control 76 / 38,000 = 0.20%, a difference of 0.25 percentage points, relative risk 2.25. The expected canary errors if it were the same as control: 2,000 x 0.002 = 4.
2. Test it: pooled z = 2.37, two-sided p about 0.018; Fisher exact p about 0.039 (better with small counts). A 95% interval for the gap (Newcombe-style) is 0.03 to 0.66 points: the lower end barely clears zero. So: probably real, imprecise, and 9 errors is a small count.
3. Be careful about looking: one test is at 5% false alarm; six hourly looks give about 26% chance of at least one false alarm if you act on every p below 0.05. Use the pre-agreed rule rather than the first p-value.
4. Action now (first 15 minutes): do not ramp to 25%. Hold at 5%, pull the 9 error logs and see their type, customer and input. Page the model owner. If any error is a crash, wrong-data or safety-relevant, roll back immediately; a statistical test is not needed for that.
5. If the errors look random (timeouts), extend the canary for a pre-agreed time (for example 4 more hours, or until about 20 expected control-rate errors) and decide by the written rule: roll back if the canary error rate is above control by more than 0.3 points absolute with the interval above zero, or if p99 latency worsens by more than 20%.
6. All errors in one segment: test within the segment (the run uses an illustrative segment that is 2% of traffic: 9 of 40 canary requests failed, 22.5%, against 4 of 760 for control, 0.53%, p about 5e-10), while the rest of the traffic shows 0 canary errors against 3.8 expected. This is a segment bug, not a diffuse increase. Action: route that segment to control, keep the canary elsewhere, and fix. If the segment is a key customer or regulated, roll the whole canary back.
7. First day: root-cause the errors and decide fix-and-retry or discard. Next quarter: automatic canary analysis with stratified checks, minimum sample size, and a rule template.
8. Blameless postmortem angle: the issue is not who shipped the model; it is whether the rule existed and was followed. Note what the rule did not say (segment checks, duration).

**Metrics:**
- Error rate = errors / requests per arm; absolute and relative gap with an interval.
- Written before: minimum requests per arm, metrics (error rate, p99, business metric), maximum acceptable absolute gap, segments to check, duration, who decides, and rollback criteria.
- Guardrails: p99 latency, timeout rate, a prediction-distribution check, and a segment breakdown.

**Risks:**
- Significance is not importance: 0.25 points may be tolerable, or may be a failed payment each.
- With 9 events, the pooled z and exact test can disagree; the unpooled Wald interval would include zero. Say so.
- Requests from one user or retry loop are not independent.
- Peeking and many segments produce false alarms; control with a pre-set plan.

**What the interviewer scores:**
- Strong: computes both rates, z and an exact check, and says "borderline, imprecise" instead of over-claiming.
- Strong: says what is written before: thresholds, sample size, segments, duration, owner.
- Strong: handles the segment case by stratifying and routing the segment, not averaging.
- Weak: "p is below 0.05 so roll back" or "0.45% is tiny so ramp up".

**Example:** Illustrative. Weak versus strong:
- Weak: "0.45% versus 0.2% is small, so I would go to 25%."
- Strong: "That is 9 against 4 expected, a gap of 0.25 points, z about 2.4. It is borderline with a tiny count, so I hold at 5% and read the 9 errors. If they are one segment, I route that segment back and fix it; if they look like noise I extend until the written sample size and decide by the pre-agreed rule."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- Why not just roll back to be safe? You may; the cost of a rollback is low. But you need a rule so you do not roll back on noise every time, and you need the root cause either way.
- How big a sample is needed? Large enough to detect the gap you care about (for 0.2% versus 0.3%, tens of thousands of requests per arm; compute with a power calculation).
- What about a business metric? Errors are a guardrail; the decision also needs the primary metric over a full cycle.

**Common mistakes:**
- Trusting one p-value after one hour.
- Averaging over segments and hiding a localised failure.
- No pre-written rollback criteria.
- Treating requests as independent when one customer causes many.
