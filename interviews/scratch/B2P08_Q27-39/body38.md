**Say this first (1 line):** Trace every run as nested spans (run, step, LLM call, tool call), each with latency, tokens, cost, hashed or redacted inputs, tool arguments and results and errors, so you can see where time and money go, replay a failing run from its recorded tool results, and sample and redact to respect privacy and storage.

**Then explain:**
- **Span tree:** `run` contains `step`s; each step contains `llm` and `tool` spans. Parent ids let you rebuild the path and answer "which step was slow or costly".
- **Attributes to record:** model and version, prompt template version, prompt hash (or redacted text), token counts, cost, latency, tool name, arguments, result (or its size and hash), retry count, stop reason, error type. Anthropic's post says full production tracing helped them diagnose why agents failed (reported).
- **Replay:** save each tool result keyed by tool name and arguments. Re-running the agent logic with those results stubbed reproduces the downstream behaviour without side effects or live-API drift. The demo replays a run where the one tool span is served from the recording instead of a live call. The LLM is non-deterministic in real life, so also store its raw responses to replay exactly (Q39).
- **Sampling and cost of tracing:** trace everything for errors and expensive runs; sample the rest. Keep summaries longer than raw payloads.
- **Privacy:** hash or redact prompts and results, restrict access, set retention. Anthropic reports monitoring agent decision patterns and interaction structure without reading individual conversations; that is their stated approach, not a rule for you. LLMOps and security monitoring depth belongs to Part 11.
- **What to alert and debug on:** cost per task and steps per run (P95), tool error rate, stop-reason mix (max_steps, budget), repeated identical tool calls (loop sign, Q4), and thumbs-down runs linked to their trace.

**Example:** (mock, fake clock, assumed price) a two-step weather agent. Step 1 took 1.9 s and $0.0040 (an LLM call plus the tool call); step 2 took 1.6 s and $0.0060. The prompt appears only as a hash. A replay with recorded tool results returns the same answer with no real tool call. A tool timeout is recorded on its span as an error, so you can find it without reading the transcript.

**Code:** (run; MOCK model and tools; time comes from a fake clock; the price per 1k tokens is assumed)
@@CODE@@

**Follow-ups:**
- *OpenTelemetry or custom?* Standard tracing infrastructure works if you add LLM attributes; the span model above maps onto it. Check your vendor's current conventions.
- *How do you debug a wrong answer with no error?* Open the trace, find the first step whose tool result or retrieved evidence is wrong, then replay from there.
- *Do hashes help debugging?* Only for matching duplicates; keep redacted text for a sampled subset under access control.

**Common mistakes:** logging only the final answer; storing raw PII in traces; no parent ids, so steps cannot be tied together; replaying with live tools and getting different data; no cost attribution per step.
