QS = [
(3,'🟢',"What are zero-shot, one-shot and few-shot prompting? Why do examples often beat a longer description, and how do you pick them?","all types; service-company, GCC and product GenAI loops"),
(3,'🟢',"System, user and assistant messages: what is each role for, what goes where, and what happens when instructions conflict?","all types; product, GCC, API-heavy teams"),
(3,'🟢',"What is chain-of-thought prompting? When does it help, what does it cost in latency and tokens, and when does it hurt?","all types"),
(3,'🟡',"How do you structure a complex prompt (sections, delimiters or XML tags, ordering, where to put key instructions, what to do when a condition is not met)?","all types; product, GCC, GenAI startups"),
(3,'🟡',"How do you design prompts to reduce hallucinations (grounding, permission to say \"I don't know\", citations, temperature)? What are the limits of prompting here?","all types; Glassdoor reports for Capgemini GenAI roles list prompt engineering and hallucination management among topics"),
(3,'🟡',"How do you iterate on a prompt systematically? How do you know a prompt change did not make things worse (golden set, one change at a time, regression runs)?","product, GenAI startups, GCC, evaluation-focused rounds"),
(3,'🟡',"How do you get reliable JSON from an LLM? Compare prompt-only, JSON mode, schema-based structured outputs, function calling and constrained decoding.","all types; product, GenAI startups, API-heavy teams"),
(3,'🟡',"Explain function calling end to end: tool definitions, the model emitting a call, your code executing it, returning the result, and the final answer.","all types; agentic-AI and GenAI-engineer loops"),
(3,'🟡',"How do you design good tool or function definitions (names, descriptions, parameter schemas, enums, how many tools)?","product, GenAI startups, agent-building teams"),
(3,'🟡',"Your agent returns valid JSON but the numbers are sometimes wrong. Where do you look first? Why is valid not the same as correct?","product, GenAI startups, agent-building teams"),
(3,'🟡',"Code: implement a function-calling loop against a mocked model: parse the call, validate arguments, execute, return the result, with a maximum number of steps.","product, big tech, live-coding rounds"),
(3,'🟡',"Code: validate LLM JSON output against a schema, repair or retry with a bounded budget, and fail closed when retries run out.","product, GenAI startups, live-coding rounds"),
(2,'🟡',"How do you select and order few-shot examples (coverage, label balance, recency bias, dynamic selection by retrieval)?","product, GenAI startups, GCC"),
(2,'🟡',"Zero-shot CoT, few-shot CoT, self-consistency and reasoning models: when does explicit \"think step by step\" prompting help, and when is it counter-productive?","product, big tech, GenAI startups"),
(2,'🟡',"What is ReAct prompting (thought, action, observation) and how does it differ from plain chain-of-thought?","all types; agentic-AI loops"),
(2,'🟡',"Task decomposition and prompt chaining versus one big prompt: when do you split, and how do you choose the decomposition?","product, GenAI startups, GCC"),
(2,'🟡',"How should a prompt handle ambiguity and missing information (fallback behaviour, clarifying questions, defaults, missing tool parameters)?","product, GCC, customer-facing assistants"),
(2,'🟡',"What is context engineering? How do you decide what goes into the context window, and how do you manage long-running conversations (rolling summary vs retrieval)?","product, GenAI startups, big tech"),
(2,'🟡',"Does role or persona prompting (\"you are an expert...\") help? How do you control tone and style reliably?","all types"),
(2,'🟡',"Negative constraints and instruction following: why do \"do not\" instructions fail, how do you resolve conflicting instructions, and what works better?","product, GenAI startups"),
(2,'🟡',"How do you control output length and format (explicit specs, examples, stop sequences, max tokens)? What goes wrong with truncation?","product, GCC, API-heavy teams"),
(2,'🟡',"What does constrained decoding do at the logit level? How does a schema become a grammar or state machine, and what does it guarantee and not guarantee?","product, GenAI startups, inference/platform teams"),
(2,'🟡',"What does a provider's strict structured-output mode require of your JSON schema (additionalProperties, required fields, optional fields), and what are the limits of the supported schema subset?","product, API-heavy teams"),
(2,'🟡',"Does forcing a structured format hurt answer quality? How do field order and a free-text reasoning field help?","product, GenAI startups, research-leaning teams"),
(2,'🟡',"What are the tool_choice options (auto, required, forced function, none, allowed tools) and when do you use each?","product, agent-building teams"),
(2,'🟡',"Parallel tool calls: when can the model make several calls in one turn, how do you return results, and when do you disable it?","product, agent-building teams"),
(2,'🟡',"What are the common tool-calling failure modes (wrong tool, hallucinated arguments, unnecessary calls, loops, timeouts) and how do you debug them?","product, GenAI startups, agent-building teams; a DataCamp article opens with a reported tool-calling agent stuck in a loop"),
(2,'🟡',"Retries, idempotency and side effects in tool calls: how do you avoid duplicate refunds or double writes, and when do you require human approval?","product, fintech, GCC, agent-building teams"),
(2,'🟡',"How should tool results and errors be returned to the model (compact structured errors, truncating large results, untrusted content)?","product, agent-building teams"),
(2,'🟡',"What happens when an agent has too many tools? Discuss selection accuracy, the token cost of tool definitions, grouping and tool search or deferred loading.","product, GenAI startups, agent-building teams"),
(2,'🟡',"JSON mode vs structured outputs vs function calling vs prompt-only: how do they differ in guarantees, and when would you pick each?","product, API-heavy teams"),
(2,'🟡',"How do you evaluate prompts (metrics by task type, rubrics for subjective outputs)? What are the limits of LLM-as-judge for this?","product, GenAI startups, GCC, evaluation-focused rounds"),
(2,'🟡',"How do you version, test and roll out prompts in production (prompt store, canary, A/B, rollback)? Where should prompts live?","product, GCC, platform teams"),
(2,'🟡',"What is prompt injection (direct vs indirect), why do prompt-only defences fall short, and what structural defences help (separation, least privilege)?","product, GCC, security-conscious teams"),
(2,'🟡',"How sensitive are LLMs to prompt wording, format and example order, and how do you test a prompt's robustness?","product, GenAI startups, evaluation-focused rounds"),
(2,'🟡',"How do you cut cost and latency through prompt design (shorter prompts, caching-friendly structure, smaller models, routing)?","product, GCC, API-heavy teams"),
(1,'🟡',"AI code review: this LLM-written tool-calling loop has bugs (no step limit, wrong tool_use_id, unvalidated arguments, ignored stop reason or parallel calls, swallowed exceptions). Find and fix them.","product, big tech, AI-era code-review rounds"),
(1,'🔴',"Design a reliability stack for an agent that issues refunds or changes account settings (schema validation, business rules, retries, approval, idempotency, audit).","senior roles at product companies, fintech, GCCs"),
(1,'🔴',"When would you choose not to force a strict schema on a model, and what do you do instead?","product, GenAI startups, senior roles"),
(1,'🔴',"A schema is generated per request and grammar compilation is slow. How do you keep p99 latency acceptable?","inference/platform teams, GenAI startups, senior roles"),
(1,'🔴',"Design the prompts, tools, guardrails, escalation and evaluation for a production customer-support assistant.","senior roles at product companies, GCCs, GenAI startups"),
(1,'🔴',"Automatic prompt optimisation (DSPy-style compilation, meta-prompting, search over prompts): how does it work and when is it worth it?","research-leaning teams, GenAI startups, big tech"),
(1,'🔴',"How does prompting a reasoning model differ from prompting a standard chat model (reasoning effort or budget, less hand-holding, no step-by-step instructions)?","big tech, GenAI startups, product"),
(1,'🔴',"How would you evaluate tool use: tool-selection accuracy, argument accuracy, multi-turn calls, public function-calling benchmarks, and an in-house eval set?","big tech, GenAI startups, evaluation-focused rounds"),
]
n=len(QS)
c=[sum(1 for q in QS if q[0]==s) for s in (3,2,1)]
assert [q[0] for q in QS]==sorted([q[0] for q in QS],reverse=True)
hdr=f"""# Book 2 — Part 03: Prompt Engineering, Structured Outputs and Function Calling

**Topic:** zero/few-shot and chain-of-thought prompting, roles and system prompts, prompt structure and iteration, structured outputs (JSON mode, strict schemas, constrained decoding), function/tool calling (loop, schemas, tool_choice, parallel calls, failure modes, retries and idempotency), prompt evaluation and production management.
**Target:** 40  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-21  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 1 owns prompt/prefix caching (Q24) and lost-in-the-middle (Q19); Part 2 owns decoding parameters (Q4, Q13), stop conditions (Q22), logprobs (Q23), self-consistency and test-time compute (Q42, Q43) and decoding settings per product (Q44), so cross-reference them. Agents, planning, memory and MCP belong to Part 8; evaluation depth (RAGAS, LLM-as-judge) to Part 9; prompt-injection security depth to Part 11; RAG to Parts 6-7; fine-tuning to Part 4. Book 1 only frames prompting vs RAG vs fine-tuning (B1P09-Q14) and LLM-vs-classic-NLP choice (B1P09-Q13); depth here. Provider API details (OpenAI function calling, Anthropic tool use) change quickly: answers must cite field names from the docs opened on 2026-10-21 and tell the reader to check current docs.

---
"""
out=[hdr]
for i,(s,d,q,a) in enumerate(QS,1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
open('Book2_GenAI/Book2_GenAI_Part03.md','w',encoding='utf-8',newline='\n').write(''.join(out))
open('scratch/B2P03_wavea/index_rows.txt','w',encoding='utf-8',newline='\n').write(''.join(f"| B2P03-Q{i} | 3 | {q} |\n" for i,(s,d,q,a) in enumerate(QS,1)))
print(n,c)
