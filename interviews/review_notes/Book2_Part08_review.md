# Book 2 Part 08 review (Wave C)

Date: 2026-10-24. Reviewer: lead session (independent of the four answer agents). Scope: 52 questions, Q1-Q52. Target band per plan.md: Rs 30-80 LPA.

## Process
Per-agent scratch files merged by heading with a script that refuses any block whose heading or "Asked at" line differs from the frozen list (52 of 52 merged, 0 skipped, 0 pending). Lead edits (MCP spec verification notes in Q9, Q25-Q27 areas and the header status) were applied after the final merge.

## Structure checks (scripted)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q52 | pass |
| Star order and counts 15 / 28 / 9 | pass (matches header) |
| Required fields incl. Example | pass for all 52 |

## Code
52 Python blocks extracted with the line-start fence rule and run standalone with `python3 -I`: all exit 0. Every LLM, tool, MCP server and agent is a scripted mock or toy; synthetic or assumed inputs are labelled (Q5, Q12, Q14, Q34, Q37, Q38, Q42, Q43, Q49, Q51). Q41 is Linux-only (resource.setrlimit) and states that rlimits are not a real sandbox. Honest weak results are kept (Q17 built-in mock improvement, Q18 toy beam search 11/40 greedy vs 33/40 width 10 vs 40/40 width 40 at rising node counts, Q21 irrelevant second hit, Q23 same-transaction caveat).

## Facts web-verified this session (opened after drafting)
| Claim | Result |
|---|---|
| MCP 2025-06-18 lifecycle: initialize params, notifications/initialized, ping-only before init, version negotiation, shutdown (stdio: close stdin, SIGTERM, SIGKILL; HTTP: close connection), timeouts and cancellation, -32602 version error example | confirmed (spec page opened); Q25 updated |
| MCP 2025-06-18 tools: field list, outputSchema and structuredContent, annotations untrusted, pagination cursor, protocol errors vs isError | confirmed (spec page opened); Q27 updated |
| MCP 2025-06-18 transports: stdio rules, Streamable HTTP single endpoint, POST/GET, SSE, Mcp-Session-Id, MCP-Protocol-Version, Origin validation, replaces HTTP+SSE from 2024-11-05 | confirmed (spec page opened); Q26 updated |
Earlier (Wave A): ReAct, Reflexion, ToT, MemGPT and MAST abstracts, Anthropic "Building effective agents" and multi-agent research posts, MCP basic page.

## Not verified (written from memory or reported, hedged in the text)
MCP origin date (guide); version in which outputSchema was added (the 2025-06-18 page lists it but history not checked); OAuth 2.1 details and later-spec enterprise claims (not used as fact); A2A agent-card fields and task states (DEV guide); LangGraph and CrewAI details (snippet level); MAST failure-mode names (deliberately not listed); semantic/episodic/procedural memory vocabulary; sandbox options (containers, gVisor-style, micro-VMs); computer-use details; dual-model and taint-tracking defences; Anthropic judge rubric dimensions in Q47; retry cap of about three and "5-10x calls" figures (guide snippets); Anthropic 90.2%, ~4x/15x tokens, ~20 starting queries (vendor-reported, labelled).

## Evidence limits (unchanged)
No candidate-reported agent questions were found for any company; evidence is paper abstracts, vendor docs and posts, and prep guides. No source states a salary band. Stars and "Asked at" tags are indicative.
