**Say this first (1 line):** Test the deterministic parts exactly (mocked tools, recorded model responses, invariants such as budget and forbidden tools), test the non-deterministic parts statistically (repeated runs against a pass-rate threshold, golden trajectories with tolerance, end-state checks), and run integration tests only in a sandbox.

**Then explain:**
- **Mocked tools with fixtures:** replace every tool with a function returning fixed data, so a failure is the agent's logic, not the network. Add failing fixtures (timeout, empty result, malformed JSON) to test recovery (Part 3 Q27).
- **Record and replay LLM responses:** store model outputs from a real run and feed them back, so a regression test is exact and free. Re-record deliberately when prompts change. Same idea as trace replay in Q38.
- **Golden trajectories with tolerance:** assert the sequence of tools and the end state, not exact wording. Allow a step or two of slack. Anthropic's posts recommend end-state evaluation for agents that change state and starting with a small set of real queries (about 20, reported).
- **Property tests (invariants):** things that must hold on every run: tokens never exceed the budget, a forbidden tool is never executed, the loop always terminates (Q4), output matches the schema. Run them over many seeds and inputs.
- **Flaky behaviour:** real models vary. Run each case N times and assert a pass rate (for example at least 80%) with a threshold set from a baseline, not a single pass. For high-stakes cases require 100% on the invariants and a rate on the quality.
- **Sandboxed integration tests:** a few end-to-end runs against a disposable environment (test accounts, a scratch database, no real money), because side effects are real. Evaluation depth (rubrics, LLM judges, benchmarks) is in Part 9.

**Example:** a mock agent answers weather questions with a scripted policy. Over 200 runs (50 seeds x 4 budgets, including 0) the token count never exceeds the budget. A model that tries `delete_account` never gets it executed: the guard returns "blocked". A recorded run replays to an identical result. With a simulated 10% skip-the-tool wobble, the pass rate over 100 seeded runs is 0.89, so the test asserts at least 0.80 rather than demanding 100%.

**Code:** (run; plain asserts; the model is a mock scripted policy with a seeded wobble)
@@CODE@@

**Follow-ups:**
- *How do you pick the threshold?* Measure the baseline pass rate over many runs, then set the gate a little below it and watch for drift.
- *Do replay tests go stale?* Yes, when prompts or tools change; keep a small live smoke suite alongside.
- *How do you test guardrails?* Adversarial fixtures (injection text in tool results) must never trigger forbidden calls (Part 6 Q36, Part 5 Q8).

**Common mistakes:** exact-string assertions on LLM text; hitting live APIs in unit tests; one-shot pass/fail on a stochastic system; no invariant tests; skipping failure fixtures; integration tests with real side effects.
