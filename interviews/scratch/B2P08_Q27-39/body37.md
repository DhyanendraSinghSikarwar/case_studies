**Say this first (1 line):** Agent cost is mostly tokens times calls, so you control it with budgets and early stopping, cut the price per token with caching and model routing, and cut wall-clock time with parallelism, while remembering that quality and tokens are coupled, so every saving needs an eval to prove quality held.

**Then explain:**
- **Budgets:** a token, cost and step budget per agent and per run, enforced in code (Q4); on exhaustion, stop launching new work and answer with what you have, flagged partial.
- **Caching:** put static content (system prompt, tool definitions, fixed instructions) first so the provider's prefix cache can reuse it. Part 1 Q24 and Part 3 Q36 cover how caching works and its caveats; also cache tool results that are deterministic.
- **Model routing:** a stronger model for the lead and planning, cheaper models for narrow sub-tasks. Anthropic's research-system post reports a lead agent with sub-agents; the cost split in my demo is assumed, so benchmark your own pair.
- **Parallelism:** independent sub-tasks run together, so latency is about the slowest task, but total tokens and cost stay the same (the demo shows this). Dependent steps cannot be parallelised.
- **Early stopping:** stop when the evidence is sufficient (Part 7 Q13), when returns diminish, or at a hard cap; scale the number of workers to query difficulty (Q35).
- **The coupling (reported):** in Anthropic's post, token usage alone explained 80% of the variance in BrowseComp performance, and with tool calls and model choice 95% (their data, their setting). The same post reports about 4x tokens for agents versus chat and about 15x for multi-agent versus chat. Reading: spending more tokens often buys quality, so cuts can cost accuracy. They suit tasks valuable enough to pay for.
- **Measure:** cost per successful task, not cost per call (Q38 gives the data).

**Example:** (ASSUMED numbers, not measurements) lead plus 5 sub-agent tasks of 20k tokens each. Sequential on a big model: 110k tokens, $1.65, 48 s. Parallel: same tokens and cost, 16 s. Small workers: $0.45, 11 s. Small workers plus a 60%-cached prefix (assumed half price for cached tokens): 80k effective tokens, $0.36. A 70k-token budget stops after 3 tasks: cheaper, but you only get 3 of 5 answers, which is the quality trade.

**Code:** (run; every price, latency and token count is an ASSUMPTION for illustration)
@@CODE@@

**Follow-ups:**
- *Does routing hurt quality?* It can; test the cheap model on the sub-task alone with a labelled set before switching.
- *Parallel is faster, so always parallel?* Only for independent work; it also spikes rate limits and spend rate.
- *What would you alert on?* Cost per task P95, steps per run, budget-exhaustion rate (Q38).

**Common mistakes:** optimising latency while ignoring token cost; cutting budgets without an eval; routing by guess; parallelising dependent steps; cached prefix broken by a timestamp at the top of the prompt.
