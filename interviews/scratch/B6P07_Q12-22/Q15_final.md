### Q15 ⭐⭐⭐ 🔴 An agent task is capped at 25 steps, and 600 of 20,000 tasks (3%) hit the cap while the other 19,400 average 6 steps. Compute the share of all steps spent by the capped tasks, and explain how you would find why they loop and what hard controls you would add beyond the cap.
**Asked at:** Agent cost and loop-control material (solo.io and getmaxim pages on iteration and token ceilings for agent loops, a Towards Data Science article on agent token costs, an Exponent-sourced 2026 guide that mentions a candidate-reported agent-with-RAG token-cost design prompt); commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** The capped 3% of tasks burn 15,000 of 131,400 steps, which is 11.4%, and probably more of the token cost because each step re-sends a longer history; I would read the capped traces, find the loop pattern, and add budgets that stop it early.

**Clarifying questions:**
- Does a step mean one model call, or one tool call? Why it matters: cost scales with model calls.
- Does each step re-send the full history? Why it matters: it makes long tasks cost much more than their step share.
- Do capped tasks end with a wrong answer, a partial answer, or a user retry? Why it matters: sets the cost of failure.
- Do any steps write to external systems? Why it matters: loops with side effects are a safety issue, not only cost.
- Is 25 a design limit or a guess? Why it matters: some tasks may legitimately need more.

**Approach:**
1. Steps: capped 600 x 25 = 15,000. Others 19,400 x 6 = 116,400. Total 131,400. Capped share = 11.4% (they are 3% of tasks).
2. Cost share is larger if history is re-sent. If each step adds equal tokens and the whole history is re-sent, a k-step task costs about k(k+1)/2 units: 325 for 25 steps against 21 for 6 steps (15.5x). Capped share of input tokens is then at most about 32%. This is a model, not a measurement; spread in the other tasks' step counts lowers it (about 29.5% in a simulation).
3. Pull the 600 traces. Cluster them: same tool called with the same arguments, a tool that keeps erroring, a plan that never converges, ambiguous user goal, a missing tool.
4. Compare with 100 normal traces to see where they diverge (first repeated step).
5. Add hard controls beyond the step cap: a token and cost budget per task, a wall-clock limit, a repeat detector (same tool and arguments hash twice), a cap per tool, a no-progress check, a circuit breaker that stops and escalates to a human or a fixed fallback answer, and idempotency or approval for any write action.
6. Fix the root cause: better tool error messages, a clearer stop condition, an "I cannot finish" action the agent can choose.
7. Alert on the capped share per day and the cost of the top 1% of tasks.

**Metrics:**
- Capped rate = tasks that hit the cap / all tasks (3.0%).
- Step share = steps in capped tasks / all steps (11.4%).
- Token cost share = input plus output tokens of capped tasks / all tokens (measured, not modelled).
- Cost per resolved task = total cost / tasks resolved.
- Guardrails: resolution rate must not fall when budgets tighten; repeated-write incidents = 0.

**Risks:**
- A tighter cap cuts off tasks that are legitimately long.
- Repeat detection misses loops that vary the arguments slightly.
- Budgets end the task but leave a half-finished write.
- Fixing the symptom: the agent loops on a missing capability.

**What the interviewer scores:**
- Strong: correct 11.4%, notices cost share differs from step share, reads traces, lists several hard controls.
- Strong: treats loops with writes as a safety matter.
- Weak: "lower the cap to 10" with no trace review.
- Weak: ignores history growth.

**Example:** Illustrative. Weak: "Only 3% of tasks hit the cap, ignore it." Strong: "Those 3% are 11.4% of steps, and if the context is re-sent each step, up to about 32% of input tokens. I would pull the 600 traces, find that most repeat one failing tool call, add a repeat detector and a per-task token budget, and make the tool return a clear error so the agent can stop."

**Code:**
```python
tasks, capped, cap, avg_other = 20_000, 600, 25, 6
other = tasks - capped
assert other == 19_400 and capped / tasks == 0.03
s_cap, s_oth = capped * cap, other * avg_other
share = s_cap / (s_cap + s_oth)
print(f"steps: capped {s_cap:,}, others {s_oth:,}, total {s_cap+s_oth:,}; capped share {share*100:.1f}%")
assert (s_cap, s_oth) == (15_000, 116_400) and round(share * 100, 1) == 11.4
# If every step re-sends the whole history (equal tokens added per step), input tokens of a k-step task ~ k(k+1)/2 units.
tri = lambda k: k * (k + 1) // 2
c_cap, c_oth = capped * tri(cap), other * tri(6)
sh2 = c_cap / (c_cap + c_oth)
print(f"history-resend model: capped task {tri(cap)} units vs 6-step task {tri(6)} units = {tri(cap)/tri(6):.1f}x")
print(f"capped share of input tokens <= {sh2*100:.1f}% (treats 'average 6' as exactly 6; spread would lower this share)")
assert (tri(25), tri(6)) == (325, 21) and round(tri(25) / tri(6), 1) == 15.5 and round(sh2 * 100, 1) == 32.4
# Convexity check: spreading steps around a mean of 6 raises others' cost, so the capped share only falls.
import numpy as np
rng = np.random.default_rng(3)
steps = rng.poisson(6, other)
steps = np.clip(steps, 1, 24)
c_oth2 = float((steps * (steps + 1) // 2).sum())
sh3 = c_cap / (c_cap + c_oth2)
print(f"with Poisson(6) spread: others' mean steps {steps.mean():.2f}, capped share {sh3*100:.1f}%")
assert sh3 < sh2
```

**Output (my run):**
```
steps: capped 15,000, others 116,400, total 131,400; capped share 11.4%
history-resend model: capped task 325 units vs 6-step task 21 units = 15.5x
capped share of input tokens <= 32.4% (treats 'average 6' as exactly 6; spread would lower this share)
with Poisson(6) spread: others' mean steps 6.00, capped share 29.5%
```

**Follow-ups:**
- How do you set the cap? From the distribution of steps in successful tasks, for example above the 99th percentile of successful runs, and review it as tasks change.
- What if the agent writes to a database in the loop? Require idempotency keys and a confirmation step, and alert on repeated identical writes.
- Is a loop always a bug? No. Some tasks are long; separate "long and progressing" from "repeating".

**Common mistakes:**
- Treating step share as cost share.
- Raising or lowering the cap without looking at traces.
- Only a step cap and no token or cost cap.
- No fallback when the budget is hit.

