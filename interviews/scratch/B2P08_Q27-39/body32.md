**Say this first (1 line):** Start with plain code and direct API calls; adopt a framework when you genuinely need what it gives (durable checkpoints, human-in-the-loop pauses, explicit graph control, shared tooling) and the cost in hidden prompts, lock-in and debugging is worth paying.

**Then explain:**
- **Anthropic's caution (opened post):** frameworks make it easy to start, but can add layers that obscure prompts and responses and tempt you into extra complexity. Start with direct API calls, and make sure you understand what a framework does underneath.
- **LangGraph-style state graphs (from the DEV guide and search snippets; docs not opened):** nodes do work, edges connect them, a shared typed state flows through, conditional edges choose the next node, a checkpointer saves state so a thread can resume, and the graph can pause for a human. Framework API names change, so check the docs.
- **CrewAI-style (guide):** you define agents by role and goal, give them tasks, and pick a process: sequential, hierarchical (a manager delegates) or consensual. Fast to prototype, but the role prompts are generated for you, so inspect them.
- **Decision criteria:**

| Criterion | Plain code wins | Framework wins |
|---|---|---|
| Control flow | one loop, few branches | many branches, cycles, retries |
| Persistence | none or simple | resume after crash or approval, many threads |
| Human-in-the-loop | none | pause-approve-resume is core |
| Debuggability | you see every prompt | needs good tracing (Q38) |
| Lock-in / upgrades | none | API churn risk |
| Team onboarding | anyone reads it | shared vocabulary |

- **Middle path:** write your own small runner first (the demo is about 25 lines). If you find yourself rebuilding checkpoints and pausing, that is the signal to use a framework.

**Example:** a refund flow: draft, check, approve, send. Amounts up to 100 skip to approval; larger ones are rejected; approval pauses until a human says yes. In the run, the first call stops before `approve` with a saved checkpoint, a second call resumes from it with `human_ok=True` and sends. That pause-and-resume is the feature that justifies a framework in production, where state must survive a restart and live in a database.

**Code:** (run; MINI runner I wrote to show the idea; it makes no claim about any real framework's API; nodes are mocks)
@@CODE@@

**Follow-ups:**
- *Is a graph just a workflow?* Yes: fixed nodes, with a model choosing branches at some points. See Q3 for workflows vs agents.
- *How do you avoid lock-in?* Keep tools, prompts and business logic in plain functions; use the framework only for orchestration.
- *What about debugging?* Log each node's input and output state (Q38); if the framework hides the final prompt, that is a red flag.

**Common mistakes:** reaching for a framework for a three-step chain; not reading the prompts it generates; storing non-serialisable objects in state; no step limit on cycles; treating framework choice as the architecture.
