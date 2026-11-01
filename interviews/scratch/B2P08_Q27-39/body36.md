**Say this first (1 line):** MAST (Multi-Agent System Failure Taxonomy, expansion from memory; an arXiv paper) is an annotated study of why multi-agent LLM systems fail, grouping 14 failure modes into three categories (system design issues, inter-agent misalignment, task verification); the practical lesson is that most failures are organisational, so you fix them with roles, handoffs, verification and stopping rules, not just a better model.

**Then explain (from the abstract I opened; I did not read the full paper):**
- **The study:** more than 1,600 annotated traces across 7 multi-agent frameworks; the taxonomy was built from 150 traces. The authors report inter-annotator agreement of kappa 0.88 and an LLM-as-judge pipeline for annotating at scale. The abstract reports that gains of multi-agent systems over single-agent ones are often minimal. It gives no failure rates, so do not quote any.
- **The three categories (names from the abstract):** system design issues, inter-agent misalignment, task verification. I will not list the 14 modes from memory. The symptoms in my demo are my own illustrative reading of what each category could look like.
- **Mitigations at category level (my reasoning, consistent with the abstract's framing):**
  - *System design:* clear role specifications, explicit termination criteria and step budgets (Q4), simple topologies (Q33).
  - *Inter-agent misalignment:* structured handoffs with objective, format, boundaries (Q35), shared state with schemas rather than free chat.
  - *Task verification:* an independent verifier that checks evidence or runs tests, not one that re-reads the author's summary; end-state checks (Q34, Q39).
- **Process:** log full traces (Q38), annotate a sample of failures, and tally by category to decide which fix to buy first. The paper's own approach of LLM-judge annotation can scale this, validated against human labels.
- **Why it matters for interviews:** it supports "start simple": if multi-agent gains are often minimal, you need a measured reason to add agents.

**Example:** in my toy tally of 8 synthetic traces, 2 look like system design, 3 like misalignment, 2 like verification, 1 unclassified (a tool timeout, which is not an agent-coordination failure). That tells a team to fix handoffs first and add a real verifier second. The numbers are made up to show the method, not MAST results.

**Code:** (run; TOY rules, synthetic traces, my illustrative reading, not the MAST modes)
@@CODE@@

**Follow-ups:**
- *Can the LLM judge annotate failures reliably?* The authors report using one with agreement figures; validate any judge you use against human labels (Part 9).
- *Is multi-agent worse than single-agent?* The abstract says gains are often minimal, not that they are negative; measure on your task.
- *First fix?* The category with the largest share in your own traces.

**Common mistakes:** quoting failure percentages that the paper's abstract does not give; assuming a stronger model fixes coordination problems; self-verification by the same agent; no termination criteria; adding agents without a baseline comparison.
