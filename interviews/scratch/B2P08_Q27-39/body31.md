**Say this first (1 line):** MCP connects an agent to tools and context; A2A (reported by a guide as a Google-originated protocol) connects an agent to other agents that are opaque, possibly built by other teams or vendors; you only need agent-to-agent communication when agents live in separate systems or organisations, and inside one codebase plain function calls are simpler.

**Then explain:**
- **Different jobs:** MCP is the plug between a model-driven host and capabilities (tools, resources, prompts: Q27, Q30). A2A is a way for one agent to hand a task to another agent and follow it. They complement each other: an agent can use MCP for its own tools and A2A to delegate.
- **Agent card (from the DEV guide, primary spec not opened):** a JSON description of an agent: name, skills, endpoint and how to authenticate. A client reads it to discover who can do a job.
- **Task lifecycle (guide):** Submitted, Working, Input Required, Completed, Failed, Canceled. Input Required is the interesting one: the remote agent asks for more information instead of guessing. Long jobs need such states because an agent task may take minutes, unlike a function call.
- **When you need it:** the other agent belongs to another team or company, runs on another framework, must keep its internals private, or runs long and asynchronously. **When you do not:** all agents are in one process or repo; calling a Python function or one sub-agent is cheaper, easier to debug and has no network or auth surface.
- **Cost of interop:** each hop adds latency, auth, versioning and a new trust boundary (treat remote agent output as untrusted: Q28, Part 6 Q36).
- **Hedge:** protocol details move fast; check the current A2A specification before relying on field names or state names.

**Example:** an expense assistant agent needs a vendor's invoice-checking agent. It fetches the vendor's agent card, sees a `match_po` skill and an auth scheme, submits a task, receives Input Required ("which PO number?"), answers, and later reads Completed. The toy below validates a card and enforces which state changes are legal. The transition table is my own design for illustration, not the spec's.

**Code:** (run; TOY, my own state table and field checks, not the real protocol)
@@CODE@@

**Follow-ups:**
- *Why not give the remote agent as an MCP tool?* You can, for simple request-response. A2A-style tasks add states, long-running work and agent-to-agent negotiation; whether you need that depends on the job.
- *How do you secure it?* Authenticate with the scheme on the card, scope what the remote agent may receive, validate its output like any untrusted input.
- *Is A2A required for multi-agent systems?* No; most multi-agent systems are inside one process (Q33).

**Common mistakes:** treating A2A and MCP as competitors; adding network agents where a function call would do; assuming the card is trustworthy; ignoring terminal states and timeouts; quoting protocol details as settled facts.
