**Say this first (1 line):** A sub-agent only knows what you put in its handoff, so a vague instruction makes it guess scope, and parallel sub-agents guess the same thing and duplicate work; a good handoff gives an objective, an output format, tool guidance and task boundaries, and scales effort to the query.

**Then explain:**
- **What Anthropic reported (their multi-agent research post, their setting):** early lead agents gave short vague instructions, sub-agents duplicated work or left gaps, and the system spawned about 50 sub-agents for simple queries. The fixes they describe: each sub-agent gets an objective, an output format, guidance on tools and sources, and clear task boundaries; and embed rules that scale effort to query complexity (a simple fact needs one agent and a few calls; heavy research needs more).
- **Why vagueness duplicates:** "research IT companies" given to three workers means each picks the obvious companies and the obvious sources. Nobody owns a slice.
- **A good handoff has:**
  - *Objective:* specific, with scope, entities and date range.
  - *Output format:* a schema the parent can merge without re-reading prose (Part 3 on structured outputs).
  - *Tools and sources:* which to use, which to avoid.
  - *Boundaries:* what is out of scope, what a sibling covers, when to stop (a call or token limit).
  - *Context:* only what the task needs; the parent summarises instead of dumping history (Q37 on cost).
- **Check handoffs in code:** reject incomplete handoffs before launching workers. It is cheap and catches the failure at its source.
- **Effort scaling:** decide the number of workers from the query (one for a fact, a few for a comparison), with a hard cap.

**Example:** vague: "research IT companies" produces no format, no tools, no limit, and a second worker told "research IT firms" overlaps with it. Good: "List the 2023 and 2024 annual revenue of each of the three largest listed Indian IT services firms", with a JSON output format, tool guidance, "only these three firms; stop after 10 searches; a sibling handles headcount". The validator below rejects the first on four counts and accepts the second. The firms and fields are illustrative.

**Code:** (run; TOY checks I wrote, not Anthropic's method)
@@CODE@@

**Follow-ups:**
- *How much context should the worker get?* The task-relevant slice plus references (ids, file paths) it can fetch; not the whole conversation.
- *How do you catch duplicates at run time?* Log each worker's queries (Q38) and compare; the parent can drop repeats.
- *Who verifies worker output?* An independent check, not the worker (Q36).

**Common mistakes:** one-line delegations; no output schema, so the parent re-reads prose; no stop rule; spawning many workers for simple questions; passing the entire history to every worker.
