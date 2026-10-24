**Say this first (1 line):** Pick the simplest topology that fits: a sequential pipeline for fixed stages, a router when one specialist can answer, a hierarchical supervisor when a task needs several specialists and combining, and peer-to-peer or blackboard only when agents truly need to react to each other's work, because each step up adds calls, tokens and ways to fail.

**Then explain (patterns as listed by the DEV guide):**
- **Sequential pipeline:** A then B then C, each passing output on. Predictable, easy to test, no dynamic choices. Fits extract, then validate, then format. This is prompt chaining from Q3.
- **Hierarchical supervisor:** a lead agent plans, delegates to workers, collects and combines, and can loop. Fits tasks that split into parts decided at run time. This is the orchestrator-workers idea in Q3. Anthropic's research system uses a lead plus parallel sub-agents (reported).
- **Peer-to-peer:** agents message each other directly. Flexible but hard to bound and debug; conversation can wander.
- **Blackboard or broadcast:** agents read from and write to a shared space, or one message goes to all. Good when contributions are independent and opportunistic; needs rules about who writes what and when to stop.
- **Supervisor vs router:** a router makes one decision and hands off (cheap, cannot combine). A supervisor loops: decide, delegate, observe, decide again, then combine.
- **Trade-offs:**

| | Control | Latency | Token cost | Failure isolation |
|---|---|---|---|---|
| Pipeline | high | sum of stages | low | a stage failure is easy to locate |
| Router | high | 2 calls | lowest | one specialist at risk |
| Supervisor | medium | rounds x calls (parallel workers help) | high | supervisor is a single point |
| Peer / blackboard | low | unbounded without limits | highest | errors spread through shared state |

- **Use multi-agent sparingly:** Anthropic reports multi-agent systems used about 15x the tokens of chat and suit parallelisable, high-value tasks; tasks needing shared context or many dependencies, such as most coding, fit poorly (their post, their setting). See Q37 for cost.

**Example:** support questions with mock specialists. "wrong invoice charge" needs only billing: the router uses 2 calls, the supervisor 4. "invoice charge, contract dispute and an error" spans three specialists: the router answers only billing (2 calls, incomplete), the supervisor covers all three with 8 calls. That is the trade: coverage and combining against calls.

**Code:** (run; every agent and policy is a deterministic mock; the call counts are for this script only)
@@CODE@@

**Follow-ups:**
- *Can a supervisor run workers in parallel?* Yes; the call count stays but latency drops (Q37).
- *Router misroutes, now what?* Add a fallback or a confidence threshold that escalates to the supervisor.
- *When does a single agent with tools beat all this?* Most of the time, until context or tool count overflows.

**Common mistakes:** choosing peer-to-peer because it sounds advanced; no stop rule on supervisor loops (Q4); a supervisor that rewrites worker output without checking it; counting only latency and ignoring tokens.
