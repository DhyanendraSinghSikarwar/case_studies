# Book 2 — Part 03: Prompt Engineering, Structured Outputs and Function Calling

**Topic:** zero/few-shot and chain-of-thought prompting, roles and system prompts, prompt structure and iteration, structured outputs (JSON mode, strict schemas, constrained decoding), function/tool calling (loop, schemas, tool_choice, parallel calls, failure modes, retries and idempotency), prompt evaluation and production management.
**Target:** 40  |  **Actual:** 44 (⭐⭐⭐ 12, ⭐⭐ 24, ⭐ 8)  |  **Date:** 2026-10-21  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 1 owns prompt/prefix caching (Q24) and lost-in-the-middle (Q19); Part 2 owns decoding parameters (Q4, Q13), stop conditions (Q22), logprobs (Q23), self-consistency and test-time compute (Q42, Q43) and decoding settings per product (Q44), so cross-reference them. Agents, planning, memory and MCP belong to Part 8; evaluation depth (RAGAS, LLM-as-judge) to Part 9; prompt-injection security depth to Part 11; RAG to Parts 6-7; fine-tuning to Part 4. Book 1 only frames prompting vs RAG vs fine-tuning (B1P09-Q14) and LLM-vs-classic-NLP choice (B1P09-Q13); depth here. Provider API details (OpenAI function calling, Anthropic tool use) change quickly: answers must cite field names from the docs opened on 2026-10-21 and tell the reader to check current docs.

---

### Q1 ⭐⭐⭐ 🟢 What are zero-shot, one-shot and few-shot prompting? Why do examples often beat a longer description, and how do you pick them?
**Asked at:** all types; service-company, GCC and product GenAI loops
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 System, user and assistant messages: what is each role for, what goes where, and what happens when instructions conflict?
**Asked at:** all types; product, GCC, API-heavy teams
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What is chain-of-thought prompting? When does it help, what does it cost in latency and tokens, and when does it hurt?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟡 How do you structure a complex prompt (sections, delimiters or XML tags, ordering, where to put key instructions, what to do when a condition is not met)?
**Asked at:** all types; product, GCC, GenAI startups
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 How do you design prompts to reduce hallucinations (grounding, permission to say "I don't know", citations, temperature)? What are the limits of prompting here?
**Asked at:** all types; Glassdoor reports for Capgemini GenAI roles list prompt engineering and hallucination management among topics
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 How do you iterate on a prompt systematically? How do you know a prompt change did not make things worse (golden set, one change at a time, regression runs)?
**Asked at:** product, GenAI startups, GCC, evaluation-focused rounds
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 How do you get reliable JSON from an LLM? Compare prompt-only, JSON mode, schema-based structured outputs, function calling and constrained decoding.
**Asked at:** all types; product, GenAI startups, API-heavy teams
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 Explain function calling end to end: tool definitions, the model emitting a call, your code executing it, returning the result, and the final answer.
**Asked at:** all types; agentic-AI and GenAI-engineer loops
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 How do you design good tool or function definitions (names, descriptions, parameter schemas, enums, how many tools)?
**Asked at:** product, GenAI startups, agent-building teams
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Your agent returns valid JSON but the numbers are sometimes wrong. Where do you look first? Why is valid not the same as correct?
**Asked at:** product, GenAI startups, agent-building teams
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Code: implement a function-calling loop against a mocked model: parse the call, validate arguments, execute, return the result, with a maximum number of steps.
**Asked at:** product, big tech, live-coding rounds
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Code: validate LLM JSON output against a schema, repair or retry with a bounded budget, and fail closed when retries run out.
**Asked at:** product, GenAI startups, live-coding rounds
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐ 🟡 How do you select and order few-shot examples (coverage, label balance, recency bias, dynamic selection by retrieval)?
**Asked at:** product, GenAI startups, GCC
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐ 🟡 Zero-shot CoT, few-shot CoT, self-consistency and reasoning models: when does explicit "think step by step" prompting help, and when is it counter-productive?
**Asked at:** product, big tech, GenAI startups
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐ 🟡 What is ReAct prompting (thought, action, observation) and how does it differ from plain chain-of-thought?
**Asked at:** all types; agentic-AI loops
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟡 Task decomposition and prompt chaining versus one big prompt: when do you split, and how do you choose the decomposition?
**Asked at:** product, GenAI startups, GCC
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟡 How should a prompt handle ambiguity and missing information (fallback behaviour, clarifying questions, defaults, missing tool parameters)?
**Asked at:** product, GCC, customer-facing assistants
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟡 What is context engineering? How do you decide what goes into the context window, and how do you manage long-running conversations (rolling summary vs retrieval)?
**Asked at:** product, GenAI startups, big tech
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 Does role or persona prompting ("you are an expert...") help? How do you control tone and style reliably?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 Negative constraints and instruction following: why do "do not" instructions fail, how do you resolve conflicting instructions, and what works better?
**Asked at:** product, GenAI startups
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 How do you control output length and format (explicit specs, examples, stop sequences, max tokens)? What goes wrong with truncation?
**Asked at:** product, GCC, API-heavy teams
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 What does constrained decoding do at the logit level? How does a schema become a grammar or state machine, and what does it guarantee and not guarantee?
**Asked at:** product, GenAI startups, inference/platform teams
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 What does a provider's strict structured-output mode require of your JSON schema (additionalProperties, required fields, optional fields), and what are the limits of the supported schema subset?
**Asked at:** product, API-heavy teams
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 Does forcing a structured format hurt answer quality? How do field order and a free-text reasoning field help?
**Asked at:** product, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 What are the tool_choice options (auto, required, forced function, none, allowed tools) and when do you use each?
**Asked at:** product, agent-building teams
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Parallel tool calls: when can the model make several calls in one turn, how do you return results, and when do you disable it?
**Asked at:** product, agent-building teams
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 What are the common tool-calling failure modes (wrong tool, hallucinated arguments, unnecessary calls, loops, timeouts) and how do you debug them?
**Asked at:** product, GenAI startups, agent-building teams; a DataCamp article opens with a reported tool-calling agent stuck in a loop
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 Retries, idempotency and side effects in tool calls: how do you avoid duplicate refunds or double writes, and when do you require human approval?
**Asked at:** product, fintech, GCC, agent-building teams
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 How should tool results and errors be returned to the model (compact structured errors, truncating large results, untrusted content)?
**Asked at:** product, agent-building teams
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 What happens when an agent has too many tools? Discuss selection accuracy, the token cost of tool definitions, grouping and tool search or deferred loading.
**Asked at:** product, GenAI startups, agent-building teams
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 JSON mode vs structured outputs vs function calling vs prompt-only: how do they differ in guarantees, and when would you pick each?
**Asked at:** product, API-heavy teams
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 How do you evaluate prompts (metrics by task type, rubrics for subjective outputs)? What are the limits of LLM-as-judge for this?
**Asked at:** product, GenAI startups, GCC, evaluation-focused rounds
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 How do you version, test and roll out prompts in production (prompt store, canary, A/B, rollback)? Where should prompts live?
**Asked at:** product, GCC, platform teams
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 What is prompt injection (direct vs indirect), why do prompt-only defences fall short, and what structural defences help (separation, least privilege)?
**Asked at:** product, GCC, security-conscious teams
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 How sensitive are LLMs to prompt wording, format and example order, and how do you test a prompt's robustness?
**Asked at:** product, GenAI startups, evaluation-focused rounds
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 How do you cut cost and latency through prompt design (shorter prompts, caching-friendly structure, smaller models, routing)?
**Asked at:** product, GCC, API-heavy teams
<!-- ANSWER_PENDING -->

### Q37 ⭐ 🟡 AI code review: this LLM-written tool-calling loop has bugs (no step limit, wrong tool_use_id, unvalidated arguments, ignored stop reason or parallel calls, swallowed exceptions). Find and fix them.
**Asked at:** product, big tech, AI-era code-review rounds
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🔴 Design a reliability stack for an agent that issues refunds or changes account settings (schema validation, business rules, retries, approval, idempotency, audit).
**Asked at:** senior roles at product companies, fintech, GCCs
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🔴 When would you choose not to force a strict schema on a model, and what do you do instead?
**Asked at:** product, GenAI startups, senior roles
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🔴 A schema is generated per request and grammar compilation is slow. How do you keep p99 latency acceptable?
**Asked at:** inference/platform teams, GenAI startups, senior roles
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🔴 Design the prompts, tools, guardrails, escalation and evaluation for a production customer-support assistant.
**Asked at:** senior roles at product companies, GCCs, GenAI startups
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🔴 Automatic prompt optimisation (DSPy-style compilation, meta-prompting, search over prompts): how does it work and when is it worth it?
**Asked at:** research-leaning teams, GenAI startups, big tech
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🔴 How does prompting a reasoning model differ from prompting a standard chat model (reasoning effort or budget, less hand-holding, no step-by-step instructions)?
**Asked at:** big tech, GenAI startups, product
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🔴 How would you evaluate tool use: tool-selection accuracy, argument accuracy, multi-turn calls, public function-calling benchmarks, and an in-house eval set?
**Asked at:** big tech, GenAI startups, evaluation-focused rounds
<!-- ANSWER_PENDING -->
