**Say this first (1 line):** The typical run is 4 x 1.5 + 3 x 0.4 = 7.2 seconds, leaving 4.8 seconds under 12, but 7.2 is a typical figure and the budget is a 95th-percentile one, so I would measure the tail (retries and slow tools push it up) and design the agent as a bounded workflow with a human approval path outside the chat clock.

**Clarifying questions:**
- Which refunds can the agent finish alone, and what does a wrong refund cost? That fixes the autonomy level and the approval rule above 2,000 rupees.
- Are the 1.5 and 0.4 second figures means, medians or 95th percentiles? The slack of 4.8 seconds is only valid for typical runs.
- Can any of the 3 tool calls run in parallel (order lookup, payment status, policy check)? Parallel calls cut the 1.2 seconds of tool time.
- What happens after the agent's answer: does a human approval make the customer wait, or is the customer told "we will confirm"? Approval waits do not fit a 12-second chat budget.
- What fraud and abuse patterns exist for refunds (repeat claimants, new accounts)? The agent must not be the only control.

**Approach:**
1. Clarify and frame. Goal: resolve refund requests safely and quickly. Define the outcome classes: refund approved, refused with reason, handed to a human.
2. Metrics and guardrails. Correct-resolution rate against a human-reviewed standard, wrong-refund rate (the guardrail), handoff rate, time to answer (p95), cost per resolved request, customer satisfaction.
3. Data and labels. Collect past refund tickets with the final human decision and the policy version. Build a golden set of cases, including tricky ones (partial refunds, expired windows, abuse patterns), reviewed by a policy owner.
4. Baseline first. A rules-and-forms flow: look up the order, check policy, return a decision or hand off. Add the language model only for understanding the request and writing the reply.
5. Model and trade-offs. Keep the LLM out of the decision where a rule can decide: the model extracts the request, tools fetch facts, a policy engine decides, the model drafts. Typical latency 7.2 seconds as given; to cut it, run independent tool calls in parallel, use a smaller model for the easy steps, and stream the first message. Refunds above 2,000 rupees go to a human approval queue; the customer is told it is pending.
6. Evaluation. Offline replay on the golden set (decision accuracy, wrong-refund rate, tool-call correctness). Then shadow mode (agent proposes, human decides) before any live action. A clean test run of 299 independent cases with no wrong refund bounds the error rate under 1% at 95% confidence (see the code).
7. Launch and experiment plan. Shadow, then agent-assisted (human clicks approve), then autonomous only under 2,000 rupees on a small traffic share, with a kill switch. Ramp only if the wrong-refund guardrail holds.
8. Monitoring, retraining and risks. Log every step and tool call; sample audits weekly; alert on handoff rate, wrong-refund rate and p95 latency; re-run the golden set whenever the prompt, model or policy changes.

Indicative pacing for a 45-minute round (minutes per step 1 to 8): 4, 4, 5, 5, 11, 6, 5, 5.

**Metrics:**
- Typical latency = sum of sequential step times = 4 x 1.5 + 3 x 0.4 = 7.2 s; slack = 12 - 7.2 = 4.8 s (a typical figure, not a p95 figure).
- p95 end-to-end latency = 95th percentile of total time across requests, measured from logs, including retries.
- Wrong-refund rate = refunds that policy owners judge wrong / refunds issued by the agent. Guardrail with a hard ceiling set by the business.
- Handoff rate = requests passed to a human / all requests; correct-resolution rate = correct final outcomes / all requests.
- Cost per resolved request = model plus tool cost / resolved requests.

**Risks:**
- Treating mean latency as the 95th percentile: in my illustrative simulation the p95 was higher than 7.2 seconds (see output), and retries make it worse.
- Prompt injection or customer text that tries to talk the agent into a refund; the policy engine, not the model, must authorise money.
- Wrong refunds are expensive and hard to undo; autonomy limits and audits are the control.
- Tool failures and partial actions (refund issued, reply failed) need idempotent calls and clear state.
- Customer data in prompts and logs, and any legal rules on refunds: ask compliance and legal.

**What the interviewer scores:**
- Strong: 7.2 seconds and 4.8 seconds slack, then says that is typical, not p95, and tests the tail.
- Strong: a bounded workflow with a policy engine, approval above 2,000 rupees, shadow mode and a kill switch.
- Strong: evaluation by golden set, wrong-refund rate and a sample-size argument.
- Weak: "give the LLM the tools and let it decide", with no limits, approvals or tail latency.

**Example:** Illustrative numbers from the question. Weak versus strong:
- Weak: "It takes 7.2 seconds against a 12 second budget, so latency is fine."
- Strong: "7.2 seconds is the typical sequential path, so 4.8 seconds of slack, but the budget is a 95th percentile. I would measure the tail from logs, and in a simple simulation with variable step times and some retries the p95 moves up toward the budget. So I would parallelise the tool calls, keep the money decision in a policy engine, send refunds over 2,000 rupees to a human with a 'pending' message, and run shadow mode first."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- What if the p95 is over 12 seconds? Cut sequential steps (parallel tools, smaller model for routing, cached policy), stream a first reply, or move slow cases to an asynchronous "we will email you" path.
- How do you choose the approval threshold? Start from the cost of a wrong refund and the audit results; 2,000 rupees is the question's rule, and I would lower or raise it with the business based on the wrong-refund rate in shadow mode.
- How do you evaluate multi-step runs? Score the final outcome and each tool call (right tool, right arguments), since a right answer can come from a wrong action.

**Common mistakes:**
- Comparing a mean latency with a percentile budget.
- Letting the model decide money movement with no deterministic policy check.
- Skipping shadow mode and launching autonomous.
- Forgetting idempotency when a refund call is retried.
