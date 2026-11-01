# Book 2 Part 03 review (Wave C)

Date: 2026-10-22. Reviewer: lead session (independent of the four answer agents). Scope: 44 questions, Q1-Q44. Target band per plan.md: Rs 30-80 LPA.

## Process change that worked
Part 2 lost a heading (Q29) when four agents edited one file concurrently. For Part 3 each agent wrote its range to its own scratch file and the lead merged by question number with a script that refuses any block whose heading or "Asked at" line differs from the frozen list. Result: 44 of 44 merged, 0 skipped, no clobbering.

## Structure checks (scripted)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q44 | pass |
| Star order and counts 12 / 24 / 8 | pass (matches header) |
| Required fields (Say this first, Then explain, Example, Follow-ups, Common mistakes) | pass |

## Code
- 34 Python blocks extracted with the proper line-start fence rule and run standalone with `python3 -I` (torch 2.14 CPU, pydantic 2.13, jsonschema 4.26): all exit 0. All LLM calls are deterministic mocks, labelled as mock or synthetic. Prompt-text-only snippets (Q14, Q19, Q20, Q41, Q43) are marked `not executed`.
- My first extractor mis-cut Q12 because the code contains literal triple backticks mid-line inside strings (valid in markdown, since a fence closes only on a line starting with backticks). Extractor fixed; Q12 runs and its output matches the text. Q7's agent used `chr(96)*3` for the same reason.
- Printed numbers compared with the text: Q12 (success after 1 retry; fail-closed after 3 calls), Q22 (0/2000 valid unconstrained vs 2000/2000 constrained), Q32 (synthetic pass rates 0.617 and 0.758, paired bootstrap interval about +0.075 to +0.208), Q38 (policy tests pass; duplicate and already-refunded denials), Q40 (hit rates 0 / 43.7 / 88.7 / 94.7 percent; 265 distinct schemas in the synthetic stream; latencies are synthetic assumptions). All match. I did not diff every other block's output; for those I relied on exit codes and the agents' reports.

## Fixes made by the lead
- Q26: replaced the unverified claim "order of results does not matter" with what Anthropic's parallel-tool-use docs say (one tool_result per tool_use block, all in the next user message, before any text, skipped calls answered with is_error true, execution order not prescribed).
- Q2: added that OpenAI's `developer` role support has varied by model (forum reports conflict for some models).

## Facts verified this session
| Claim | Result |
|---|---|
| OpenAI function calling fields, tool_choice modes, parallel_tool_calls, strict-mode rules (additionalProperties false, all properties required, optional via null), call loop with call_id, advice to keep fewer than about 20 functions | confirmed from the OpenAI docs page opened 2026-10-21 |
| Anthropic tool use: input_schema, tool_use/tool_result, stop_reason tool_use, disable_parallel_tool_use, strict true | confirmed from the Anthropic docs pages opened 2026-10-21 |
| Anthropic parallel results returned together in the next user message | confirmed (parallel tool use page) |
| OpenAI developer role replaces system for newer reasoning models | consistent with SDK docs seen via search; support varies by model and the official reference page was not retrieved, so the text is hedged |
| structured-output article claims (XGrammar default backend in several engines, Outlines slow compile, retries capped at 1-2, fail closed) | from one prep article opened; kept as "reported" |

## Not verified (written from memory, hedged in the text)
Provider rejection lists for JSON-schema keywords (pattern, format, minItems, oneOf); idempotency-key behaviour of payment APIs; judge biases (length, self-preference, position) stated as commonly reported; canary and shadow rollout practice; DSPy-style optimiser descriptions; reasoning-model prompting advice and the reasoning-effort setting; the research claims on prompt, order and format sensitivity; that constrained decoding can reduce quality on some tasks; provider discounts for cached input and batching (marked check the docs); the tokens-per-word proxy (rule of thumb, labelled illustrative); Q3's roughly 15x output-token example (arithmetic 300 vs 20 tokens, illustrative).

## Evidence limits (unchanged)
- No first-hand candidate reports for Indian product companies or big-tech labs; the Dataford aggregate (127 reports) could not be opened (429), so its figures are snippet-level and used only for star ratings. Capgemini Glassdoor reports and DataCamp's unnamed-candidate anecdote are anonymous topic signals. No source states a salary band.
- Provider API details drift quickly; answers cite the docs opened on 2026-10-21 and tell the reader to re-check.
- Q7/Q22/Q39/Q40 constrained-decoding specifics rest on one prep article plus provider docs.

## Unresolved
- Prompt-injection depth is in Part 11, agents/MCP in Part 8, evaluation depth in Part 9 (pointers only here).
