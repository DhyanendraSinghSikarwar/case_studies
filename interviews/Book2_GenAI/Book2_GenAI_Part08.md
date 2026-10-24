# Book 2 — Part 08: Agents (ReAct, tool use, planning, memory, MCP, multi-agent)

**Topic:** what an agent is and when to use one, ReAct and other reasoning-action patterns (Reflexion, Tree of Thoughts, plan-and-execute), workflow patterns, loop control and failure handling, tool design, memory and context management, checkpointing and human-in-the-loop, the Model Context Protocol (architecture, primitives, lifecycle, transports, security), A2A, orchestration frameworks, multi-agent patterns and failure modes, evaluation, observability, cost, code-executing and computer-use agents, and agent system design.
**Target:** 50  |  **Actual:** 52 (⭐⭐⭐ 15, ⭐⭐ 28, ⭐ 9)  |  **Date:** 2026-10-24  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 3 already covers ReAct prompting basics (Q15), the function-calling loop and its code (Q8, Q11), tool_choice and parallel calls (Q25, Q26), tool failure modes, retries and idempotency (Q27, Q28), too many tools (Q30), the refund reliability stack (Q38), the support-assistant design (Q41) and tool-use evaluation (Q44); Part 5 covers guardrail layers and the refund guardrail architecture (Q8, Q39); Part 7 covers agentic RAG basics (Q13), multi-hop loops (Q31), the multi-hop assistant design (Q43) and safe agentic RAG (Q47); Part 6 covers indirect injection through retrieved documents (Q36). Answers here must go deeper at the agent level and cross-reference, not repeat. Evaluation depth (RAGAS, LLM-as-judge, benchmarks) belongs to Part 9, serving to Part 10, security, LLMOps and monitoring depth to Part 11, and building a mini agent end to end to Part 12. The protocol and framework landscape changes quickly (MCP spec versions, A2A, framework APIs): answers must cite the MCP 2025-06-18 base-protocol page that was opened, hedge later-version claims reported by interview guides, and tell the reader to check the current spec. Headline numbers (Anthropic's multi-agent gains and token multipliers, Reflexion's HumanEval result, ToT's Game of 24 result, ReAct's benchmark gains) are authors' or vendor-reported claims and must be labelled with their setting.

---

### Q1 ⭐⭐⭐ 🟢 What is an AI agent? Distinguish an agent from a chatbot and from a fixed workflow, describe the agent loop, and say when you should not use an agent.
**Asked at:** all types; agentic-AI and GenAI-engineer loops
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What is ReAct, and why does interleaving reasoning with actions beat reasoning-only or acting-only? Go beyond the prompt format.
**Asked at:** all types; agentic-AI and GenAI-engineer loops
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟡 Workflows vs agents: explain prompt chaining, routing, parallelisation, orchestrator-workers and evaluator-optimizer, and when each is the right choice.
**Asked at:** all types; product, GenAI startups, agent-building teams
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟡 How does an agent loop terminate? Cover stop conditions, step and token budgets, loop detection and what to do when the budget runs out.
**Asked at:** all types; agentic-AI loops; a Codemia guide for an Amazon agentic-AI loop lists an agent-stuck-in-a-loop prompt (a guide, not a candidate report)
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 Planning in agents: ReAct vs plan-then-execute vs a hybrid with re-planning checkpoints. What are the trade-offs?
**Asked at:** all types; agentic-AI loops
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 How do you design tools for agents (the agent-computer interface): granularity, names, descriptions, error messages, and mistake-proofing?
**Asked at:** product, GenAI startups, agent-building teams
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 Memory in agents: short-term vs long-term, and episodic, semantic and procedural memory. What is the difference between state, memory and checkpointing?
**Asked at:** all types; agentic-AI loops
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 How do you manage context in a long-running agent (summarisation, trimming, offloading to notes or files, tiered memory)?
**Asked at:** product, GenAI startups, agent-building teams
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 What is the Model Context Protocol (MCP)? Explain the problem it solves, the host-client-server architecture, JSON-RPC messaging and the connection lifecycle.
**Asked at:** all types; agentic-AI and GenAI-engineer loops
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 What are MCP's tools, resources and prompts, who controls each, and how do you decide which to use?
**Asked at:** all types; agentic-AI and GenAI-engineer loops
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 MCP vs function calling vs a plain REST API: how do they differ and when would you use each?
**Asked at:** all types; product, GenAI startups
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 When do you use multiple agents instead of one? Cover orchestrator-worker designs, the token cost, and the main multi-agent failure modes.
**Asked at:** all types; agentic-AI loops; a Codemia guide lists this as an Amazon agentic-AI depth question (a guide, not a candidate report)
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 How do agents handle tool errors, hallucinated tool calls and retries (validation, feeding errors back, retry caps, circuit breakers)?
**Asked at:** product, GenAI startups, agent-building teams
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 How do you evaluate an agent: outcome vs trajectory, success rate, steps and cost, LLM judges, and where do you start?
**Asked at:** product, GenAI startups, GCC, evaluation-focused rounds
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Code: implement a ReAct agent from scratch (prompt scratchpad, parser, tool registry, stop conditions) with a mocked LLM.
**Asked at:** product, big tech, live-coding rounds
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟡 What are ReAct's failure modes (format errors, hallucinated observations, loops, bloated scratchpads), and how do you mitigate each?
**Asked at:** product, GenAI startups, agent-building teams
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟡 What are Reflexion and self-reflection in agents? How does verbal reinforcement with an episodic memory work, and when does it help or hurt?
**Asked at:** product, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟡 What is Tree of Thoughts, and when is branching, evaluating and backtracking worth its cost compared with a single chain of thought?
**Asked at:** product, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 How do plan-and-execute agents work (planner, executor, re-planner), and how do you represent, validate and approve a plan?
**Asked at:** product, GenAI startups, agent-building teams
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 How do you decompose a task into sub-tasks with dependencies, and when can tool calls or sub-agents run in parallel?
**Asked at:** product, GenAI startups, agent-building teams
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 How do you implement long-term agent memory (what to write, retrieval, deduplication, forgetting, conflicts)?
**Asked at:** product, GenAI startups, agent-building teams
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 What are the risks of agent memory (poisoning with wrong or injected facts, privacy, staleness), and how do you control them?
**Asked at:** product, GCC, security-conscious teams
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 How do checkpointing and resumability work for agents (persisted state, threads, resuming after a crash or an approval)?
**Asked at:** product, GenAI startups, platform teams
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 How do you design human-in-the-loop controls for agents (approval gates, interrupt and resume, escalation)?
**Asked at:** product, GCC, regulated-industry teams
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Walk through the MCP lifecycle and capability negotiation (initialize, tools/list, tools/call, shutdown) and what the spec requires of implementations.
**Asked at:** product, GenAI startups, agent-building teams
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 MCP transports: when do you use stdio and when Streamable HTTP, and what is the classic stdio bug?
**Asked at:** product, GenAI startups, platform teams
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 What does an MCP tool definition contain (name, description, input schema, output schema, annotations), and how are errors reported at the protocol and application levels?
**Asked at:** product, GenAI startups, agent-building teams
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 MCP security: what are tool poisoning, rug pulls and the confused-deputy problem, and how do authorisation and least privilege apply?
**Asked at:** product, GCC, security-conscious teams
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 Code: build a minimal MCP-style server (JSON-RPC handling initialize, tools/list and tools/call) and a client that calls it, in plain Python.
**Asked at:** product, big tech, live-coding rounds
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 How does an MCP host manage many servers (connections, tool aggregation, name collisions, context bloat), and how does deferred tool loading help?
**Asked at:** product, GenAI startups, platform teams
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 A2A vs MCP: what does each connect, what are agent cards and the task lifecycle, and when would you need agent-to-agent communication?
**Asked at:** product, GenAI startups, platform teams
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 When do you use an orchestration framework (LangGraph-style state graphs, CrewAI-style roles) versus plain code?
**Asked at:** product, GenAI startups, agent-building teams
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 Multi-agent communication patterns: sequential pipeline, hierarchical supervisor, peer-to-peer and blackboard. When does each fit, and supervisor vs router?
**Asked at:** product, GenAI startups, agent-building teams
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 How do you resolve conflicts between agents (voting, a supervisor, debate with a judge, confidence scores, human escalation), and what can go wrong?
**Asked at:** product, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 Delegation and context passing between agents: why does vague delegation cause duplicated work, and how do you write good task handoffs?
**Asked at:** product, GenAI startups, agent-building teams
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 Why do multi-agent systems fail (the MAST failure taxonomy: system design, inter-agent misalignment, task verification), and how do you mitigate?
**Asked at:** product, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 How do you control the cost and latency of agents (token budgets, caching, model routing, parallelism)?
**Asked at:** product, GCC, platform teams
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 How do you make agents observable (traces per step, tool calls, tokens, cost, latency, replay) and debug them in production?
**Asked at:** product, GCC, platform teams
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 How do you test and regression-test an agent (mocked tools, golden trajectories, non-determinism, sandboxes)?
**Asked at:** product, GenAI startups, GCC
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 What guardrails does an agent need (permission tiers, allowlists, sandboxing, output validation), and how do they differ from model-level safety?
**Asked at:** product, GCC, security-conscious teams
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 How do you build agents that write and run code safely (sandboxes, resource limits, filesystem and network isolation, secrets)?
**Asked at:** product, GenAI startups, platform teams
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 Browser and computer-use agents: what are the observation and action spaces, why are they unreliable, and what safety issues arise?
**Asked at:** product, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🟡 Reactive vs proactive and event-driven agents: how do triggers, scheduling and idempotent handlers change the design?
**Asked at:** product, GenAI startups, platform teams
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🟡 AI code review: this LLM-written agent loop has bugs (no step cap, swallowed tool errors, unbounded scratchpad, ignored parse failures, unvalidated tool names, untrusted text written to memory). Find and fix them.
**Asked at:** product, big tech, AI-era code-review rounds
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🔴 Design question: an internal IT-helpdesk agent with read and write tools across chat, ticketing and a database exposed through MCP servers.
**Asked at:** senior roles at product companies, GCCs, enterprise teams
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🔴 Design question: a coding agent (repository navigation, edits, a test loop, a sandbox, evaluation and cost control).
**Asked at:** senior roles at product companies, GenAI startups, big tech
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🔴 Design question: a multi-agent deep-research system (orchestrator and parallel sub-agents, citations, budgets, evaluation).
**Asked at:** senior roles at product companies, GenAI startups, big tech
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🔴 An agent loops forever on a failing tool call. Diagnose it, and design detection, budgets and escalation to prevent it.
**Asked at:** senior roles; a Codemia guide for an Amazon agentic-AI loop lists this design prompt (a guide, not a candidate report)
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🔴 How do you run long-running agents in production (resumability, queues, asynchronous execution, rolling deployments of agent versions)?
**Asked at:** platform teams, senior roles at product companies
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🔴 How would you run MCP in an enterprise (gateway, server registry, authorisation, per-tool scopes, audit, rate limits, supply-chain risk of third-party servers)?
**Asked at:** platform teams, security-conscious teams, senior roles
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🔴 How do you build an evaluation suite for a non-deterministic agent (outcome and trajectory graders, repeated runs, variance, cost-aware metrics, small-sample starts)?
**Asked at:** product, GenAI startups, senior roles, evaluation-focused rounds
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🔴 Design defences for agents that read untrusted tool outputs and tool descriptions (privilege separation, taint tracking, confirmation, dual-model patterns).
**Asked at:** security-conscious teams, research-leaning teams, senior roles
<!-- ANSWER_PENDING -->
