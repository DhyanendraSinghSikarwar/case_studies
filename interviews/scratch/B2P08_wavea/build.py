QS = [
(3,'🟢',"What is an AI agent? Distinguish an agent from a chatbot and from a fixed workflow, describe the agent loop, and say when you should not use an agent.","all types; agentic-AI and GenAI-engineer loops"),
(3,'🟢',"What is ReAct, and why does interleaving reasoning with actions beat reasoning-only or acting-only? Go beyond the prompt format.","all types; agentic-AI and GenAI-engineer loops"),
(3,'🟡',"Workflows vs agents: explain prompt chaining, routing, parallelisation, orchestrator-workers and evaluator-optimizer, and when each is the right choice.","all types; product, GenAI startups, agent-building teams"),
(3,'🟡',"How does an agent loop terminate? Cover stop conditions, step and token budgets, loop detection and what to do when the budget runs out.","all types; agentic-AI loops; a Codemia guide for an Amazon agentic-AI loop lists an agent-stuck-in-a-loop prompt (a guide, not a candidate report)"),
(3,'🟡',"Planning in agents: ReAct vs plan-then-execute vs a hybrid with re-planning checkpoints. What are the trade-offs?","all types; agentic-AI loops"),
(3,'🟡',"How do you design tools for agents (the agent-computer interface): granularity, names, descriptions, error messages, and mistake-proofing?","product, GenAI startups, agent-building teams"),
(3,'🟡',"Memory in agents: short-term vs long-term, and episodic, semantic and procedural memory. What is the difference between state, memory and checkpointing?","all types; agentic-AI loops"),
(3,'🟡',"How do you manage context in a long-running agent (summarisation, trimming, offloading to notes or files, tiered memory)?","product, GenAI startups, agent-building teams"),
(3,'🟡',"What is the Model Context Protocol (MCP)? Explain the problem it solves, the host-client-server architecture, JSON-RPC messaging and the connection lifecycle.","all types; agentic-AI and GenAI-engineer loops"),
(3,'🟡',"What are MCP's tools, resources and prompts, who controls each, and how do you decide which to use?","all types; agentic-AI and GenAI-engineer loops"),
(3,'🟡',"MCP vs function calling vs a plain REST API: how do they differ and when would you use each?","all types; product, GenAI startups"),
(3,'🟡',"When do you use multiple agents instead of one? Cover orchestrator-worker designs, the token cost, and the main multi-agent failure modes.","all types; agentic-AI loops; a Codemia guide lists this as an Amazon agentic-AI depth question (a guide, not a candidate report)"),
(3,'🟡',"How do agents handle tool errors, hallucinated tool calls and retries (validation, feeding errors back, retry caps, circuit breakers)?","product, GenAI startups, agent-building teams"),
(3,'🟡',"How do you evaluate an agent: outcome vs trajectory, success rate, steps and cost, LLM judges, and where do you start?","product, GenAI startups, GCC, evaluation-focused rounds"),
(3,'🟡',"Code: implement a ReAct agent from scratch (prompt scratchpad, parser, tool registry, stop conditions) with a mocked LLM.","product, big tech, live-coding rounds"),
(2,'🟡',"What are ReAct's failure modes (format errors, hallucinated observations, loops, bloated scratchpads), and how do you mitigate each?","product, GenAI startups, agent-building teams"),
(2,'🟡',"What are Reflexion and self-reflection in agents? How does verbal reinforcement with an episodic memory work, and when does it help or hurt?","product, GenAI startups, research-leaning teams"),
(2,'🟡',"What is Tree of Thoughts, and when is branching, evaluating and backtracking worth its cost compared with a single chain of thought?","product, GenAI startups, research-leaning teams"),
(2,'🟡',"How do plan-and-execute agents work (planner, executor, re-planner), and how do you represent, validate and approve a plan?","product, GenAI startups, agent-building teams"),
(2,'🟡',"How do you decompose a task into sub-tasks with dependencies, and when can tool calls or sub-agents run in parallel?","product, GenAI startups, agent-building teams"),
(2,'🟡',"How do you implement long-term agent memory (what to write, retrieval, deduplication, forgetting, conflicts)?","product, GenAI startups, agent-building teams"),
(2,'🟡',"What are the risks of agent memory (poisoning with wrong or injected facts, privacy, staleness), and how do you control them?","product, GCC, security-conscious teams"),
(2,'🟡',"How do checkpointing and resumability work for agents (persisted state, threads, resuming after a crash or an approval)?","product, GenAI startups, platform teams"),
(2,'🟡',"How do you design human-in-the-loop controls for agents (approval gates, interrupt and resume, escalation)?","product, GCC, regulated-industry teams"),
(2,'🟡',"Walk through the MCP lifecycle and capability negotiation (initialize, tools/list, tools/call, shutdown) and what the spec requires of implementations.","product, GenAI startups, agent-building teams"),
(2,'🟡',"MCP transports: when do you use stdio and when Streamable HTTP, and what is the classic stdio bug?","product, GenAI startups, platform teams"),
(2,'🟡',"What does an MCP tool definition contain (name, description, input schema, output schema, annotations), and how are errors reported at the protocol and application levels?","product, GenAI startups, agent-building teams"),
(2,'🟡',"MCP security: what are tool poisoning, rug pulls and the confused-deputy problem, and how do authorisation and least privilege apply?","product, GCC, security-conscious teams"),
(2,'🟡',"Code: build a minimal MCP-style server (JSON-RPC handling initialize, tools/list and tools/call) and a client that calls it, in plain Python.","product, big tech, live-coding rounds"),
(2,'🟡',"How does an MCP host manage many servers (connections, tool aggregation, name collisions, context bloat), and how does deferred tool loading help?","product, GenAI startups, platform teams"),
(2,'🟡',"A2A vs MCP: what does each connect, what are agent cards and the task lifecycle, and when would you need agent-to-agent communication?","product, GenAI startups, platform teams"),
(2,'🟡',"When do you use an orchestration framework (LangGraph-style state graphs, CrewAI-style roles) versus plain code?","product, GenAI startups, agent-building teams"),
(2,'🟡',"Multi-agent communication patterns: sequential pipeline, hierarchical supervisor, peer-to-peer and blackboard. When does each fit, and supervisor vs router?","product, GenAI startups, agent-building teams"),
(2,'🟡',"How do you resolve conflicts between agents (voting, a supervisor, debate with a judge, confidence scores, human escalation), and what can go wrong?","product, GenAI startups, research-leaning teams"),
(2,'🟡',"Delegation and context passing between agents: why does vague delegation cause duplicated work, and how do you write good task handoffs?","product, GenAI startups, agent-building teams"),
(2,'🟡',"Why do multi-agent systems fail (the MAST failure taxonomy: system design, inter-agent misalignment, task verification), and how do you mitigate?","product, GenAI startups, research-leaning teams"),
(2,'🟡',"How do you control the cost and latency of agents (token budgets, caching, model routing, parallelism)?","product, GCC, platform teams"),
(2,'🟡',"How do you make agents observable (traces per step, tool calls, tokens, cost, latency, replay) and debug them in production?","product, GCC, platform teams"),
(2,'🟡',"How do you test and regression-test an agent (mocked tools, golden trajectories, non-determinism, sandboxes)?","product, GenAI startups, GCC"),
(2,'🟡',"What guardrails does an agent need (permission tiers, allowlists, sandboxing, output validation), and how do they differ from model-level safety?","product, GCC, security-conscious teams"),
(2,'🟡',"How do you build agents that write and run code safely (sandboxes, resource limits, filesystem and network isolation, secrets)?","product, GenAI startups, platform teams"),
(2,'🟡',"Browser and computer-use agents: what are the observation and action spaces, why are they unreliable, and what safety issues arise?","product, GenAI startups, research-leaning teams"),
(2,'🟡',"Reactive vs proactive and event-driven agents: how do triggers, scheduling and idempotent handlers change the design?","product, GenAI startups, platform teams"),
(1,'🟡',"AI code review: this LLM-written agent loop has bugs (no step cap, swallowed tool errors, unbounded scratchpad, ignored parse failures, unvalidated tool names, untrusted text written to memory). Find and fix them.","product, big tech, AI-era code-review rounds"),
(1,'🔴',"Design question: an internal IT-helpdesk agent with read and write tools across chat, ticketing and a database exposed through MCP servers.","senior roles at product companies, GCCs, enterprise teams"),
(1,'🔴',"Design question: a coding agent (repository navigation, edits, a test loop, a sandbox, evaluation and cost control).","senior roles at product companies, GenAI startups, big tech"),
(1,'🔴',"Design question: a multi-agent deep-research system (orchestrator and parallel sub-agents, citations, budgets, evaluation).","senior roles at product companies, GenAI startups, big tech"),
(1,'🔴',"An agent loops forever on a failing tool call. Diagnose it, and design detection, budgets and escalation to prevent it.","senior roles; a Codemia guide for an Amazon agentic-AI loop lists this design prompt (a guide, not a candidate report)"),
(1,'🔴',"How do you run long-running agents in production (resumability, queues, asynchronous execution, rolling deployments of agent versions)?","platform teams, senior roles at product companies"),
(1,'🔴',"How would you run MCP in an enterprise (gateway, server registry, authorisation, per-tool scopes, audit, rate limits, supply-chain risk of third-party servers)?","platform teams, security-conscious teams, senior roles"),
(1,'🔴',"How do you build an evaluation suite for a non-deterministic agent (outcome and trajectory graders, repeated runs, variance, cost-aware metrics, small-sample starts)?","product, GenAI startups, senior roles, evaluation-focused rounds"),
(1,'🔴',"Design defences for agents that read untrusted tool outputs and tool descriptions (privilege separation, taint tracking, confirmation, dual-model patterns).","security-conscious teams, research-leaning teams, senior roles"),
]
n=len(QS)
c=[sum(1 for q in QS if q[0]==s) for s in (3,2,1)]
assert [q[0] for q in QS]==sorted([q[0] for q in QS],reverse=True)
hdr=f"""# Book 2 — Part 08: Agents (ReAct, tool use, planning, memory, MCP, multi-agent)

**Topic:** what an agent is and when to use one, ReAct and other reasoning-action patterns (Reflexion, Tree of Thoughts, plan-and-execute), workflow patterns, loop control and failure handling, tool design, memory and context management, checkpointing and human-in-the-loop, the Model Context Protocol (architecture, primitives, lifecycle, transports, security), A2A, orchestration frameworks, multi-agent patterns and failure modes, evaluation, observability, cost, code-executing and computer-use agents, and agent system design.
**Target:** 50  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-24  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 3 already covers ReAct prompting basics (Q15), the function-calling loop and its code (Q8, Q11), tool_choice and parallel calls (Q25, Q26), tool failure modes, retries and idempotency (Q27, Q28), too many tools (Q30), the refund reliability stack (Q38), the support-assistant design (Q41) and tool-use evaluation (Q44); Part 5 covers guardrail layers and the refund guardrail architecture (Q8, Q39); Part 7 covers agentic RAG basics (Q13), multi-hop loops (Q31), the multi-hop assistant design (Q43) and safe agentic RAG (Q47); Part 6 covers indirect injection through retrieved documents (Q36). Answers here must go deeper at the agent level and cross-reference, not repeat. Evaluation depth (RAGAS, LLM-as-judge, benchmarks) belongs to Part 9, serving to Part 10, security, LLMOps and monitoring depth to Part 11, and building a mini agent end to end to Part 12. The protocol and framework landscape changes quickly (MCP spec versions, A2A, framework APIs): answers must cite the MCP 2025-06-18 base-protocol page that was opened, hedge later-version claims reported by interview guides, and tell the reader to check the current spec. Headline numbers (Anthropic's multi-agent gains and token multipliers, Reflexion's HumanEval result, ToT's Game of 24 result, ReAct's benchmark gains) are authors' or vendor-reported claims and must be labelled with their setting.

---
"""
out=[hdr]
for i,(s,d,q,a) in enumerate(QS,1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
open('Book2_GenAI/Book2_GenAI_Part08.md','w',encoding='utf-8',newline='\n').write(''.join(out))
open('scratch/B2P08_wavea/index_rows.txt','w',encoding='utf-8',newline='\n').write(''.join(f"| B2P08-Q{i} | 8 | {q} |\n" for i,(s,d,q,a) in enumerate(QS,1)))
print(n,c)
