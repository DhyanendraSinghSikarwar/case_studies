# Book 2 — Part 12: GenAI system design and coding (capstone: end-to-end designs, estimation, build-from-scratch with mocked LLMs)

**Topic:** the integrated view of Parts 1-11: a framework for GenAI system design rounds, back-of-envelope token, QPS, GPU and cost estimation, model selection and routing, prompt vs RAG vs fine-tune decisions, end-to-end designs (enterprise knowledge assistant, text-to-SQL analytics, document extraction for BFSI, voice agent, shopping assistant, bank chatbot, multilingual Indian-language assistant, code reviewer, meeting summariser, legal and medical RAG, moderation, batch enrichment, LLM re-ranking, multi-tenant SaaS, agent-assist), production readiness, incident and failure-mode reviews, and coding from scratch in plain Python or numpy with mocked LLMs (mini-RAG, agent with budgets, text-to-SQL on sqlite3, semantic cache, streaming with cancellation, memory manager, router, resilient call harness, template engine, eval run, ACL-aware retrieval, batch runner)
**Target:** 40  |  **Actual:** 40 (⭐⭐⭐ 13, ⭐⭐ 15, ⭐ 12)  |  **Date:** 2026-10-24  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this is the last part of Book 2 and integrates rather than repeats. Question numbers cited were checked against the headings of Parts 1-11 on 2026-10-24. Fundamentals: Part 1 (KV cache Q6, parameter and KV maths Q15, stakeholder explanation Q36), Part 2 (token maths Q5, Indian-language token cost Q17), Part 3 (structured output Q7 and Q12, support-bot design Q41, refund-agent reliability Q38), Part 4 (prompt vs RAG vs fine-tune Q1, small model vs API Q25, extraction fine-tune design Q43), Part 5 (guardrail layers Q8, safety classifiers Q24, refund-bot guardrails Q39). RAG: Part 6 (pipeline Q2, ingestion Q17 and Q19, ACLs Q15, citations Q26, abstention Q27, latency Q31, cost Q32, multilingual Q35, security Q42, support design Q50, financial PDFs Q51) and Part 7 (hybrid Q2, reranking Q5, routing Q23, SQL with RAG Q40, multi-hop enterprise design Q43). Agents: Part 8 (workflows vs agents Q3, termination Q4, HITL Q24, cost Q37, observability Q38, designs Q45 IT helpdesk, Q46 coding agent, Q47 deep research). Evaluation: Part 9 (golden sets Q2, judges Q4, CI gates Q14, A/B Q30, harness Q40, launch strategy Q46, platform Q44). Serving: Part 10 (capacity Q3 and Q4, cost per token Q13, self-host vs API Q18, streaming Q19, routing and caching Q28, serving platform Q44, cost cutting Q45). LLMOps and security: Part 11 (tracing Q2, rollout Q6, trifecta Q9, PII Q11, gateway Q14, reliability Q15, budgets Q16, isolation Q26, compliance Q30, platform Q39, email-agent defence Q40, enterprise rollout Q42). Part 12 therefore avoids re-asking the IT-helpdesk, coding-agent, deep-research, eval-platform, serving-platform, LLMOps-platform and email-agent designs and instead picks different products or the cross-cutting integrated view; where a related question exists, the text says how this one differs. Book 6 owns GenAI business scenarios and Book 4 generic MLOps, so answers here stay on engineering design.

Verification notes for Wave B: no benchmark, price, latency, regulatory or vendor figure should be stated as fact unless re-read from the primary page. Seen via fetch: BIRD (arXiv 2305.03111: 12,751 question-SQL pairs, 95 databases, 37 domains, 33.4 GB; the best model in that 2023 paper reached 40.08 per cent execution accuracy vs 92.96 per cent for humans, now dated) and Spider (arXiv 1809.08887: 10,181 questions, 5,693 unique SQL, 200 databases, 138 domains). Later leaderboard numbers (about 67 per cent on BIRD, about 88 per cent on Spider in 2024 papers) are from search snippets and differ by system and split. Voice-agent per-stage latency figures are a single blog's estimates and vendor claims; the same page's own totals do not add up without assuming overlap. RouteLLM and FrugalGPT savings figures are authors' claims or secondary summaries. Semantic-cache error rates (about 30 per cent mismatches at 0.9 in one paper, from a snippet) and threshold advice conflict between sources. The Stanford legal-RAG hallucination figures (17 to 33 per cent for two commercial tools, 43 per cent for GPT-4) come from secondary reports of a study its vendors disputed. RBI FREE-AI (press release 13 Aug 2025: seven principles called Sutras, 26 recommendations, six pillars; page opened) and DPDP Rules 2025 (notified 13 Nov 2025, phased commencement with core duties about 13 May 2027, 72-hour breach report; from law-firm snippets, official Gazette text not read) must stay general and defer to counsel. IDP accuracy and savings claims are vendor figures. Any number shown in a Wave B answer must come from that answer's own code run or from explicit assumptions labelled as such.

Evidence limits: no candidate-reported system-design or coding questions (Glassdoor, Blind, AmbitionBox, LeetCode Discuss) were found; the search returned prep guides, vendor blogs, course pages and papers. The "Asked at" tags are company types, and 'expert gap-check' marks questions chosen from practice rather than a source. Question lists in guides (chatbot, document Q&A, coding assistant, voice assistant, support bot, content moderation, e-commerce hybrid search, meeting summariser, legal summarisation, text-to-image and inference platforms) support the design list; the Indian BFSI and Indic-language scenarios come from regulator and vendor material, not from reported interviews. Star ratings blend guide frequency with judgement. See research_notes/Book2_Part12_sources.md for which pages were opened.

---

### Q1 ⭐⭐⭐ 🟡 Give your framework for a GenAI system design interview: how do you spend the first ten minutes on requirements (users, inputs and outputs, data sources and sensitivity, latency, quality bar, volume, build vs buy), when do you decide which parts are deterministic code and which need a model, and how do you then cover architecture, evaluation, failure modes, safety, cost and rollout? Show it on a one-line prompt such as 'design an assistant for our company documents'. (This is the capstone view over Parts 1-11.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟡 Back-of-envelope for a GenAI launch: 2 million monthly users, 20 per cent daily active, 6 questions each, a RAG prompt of about 3,000 input tokens and 400 output tokens. Estimate QPS and peak QPS, tokens per day, API cost or GPU count under stated assumptions, KV-cache memory and embedding or index size, and say which numbers you would verify first. (Part 6 Q32 and Q33, Part 10 Q3, Q4 and Q13 give the building blocks; prices and GPU throughput must be stated as assumptions.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟡 Model selection, build-vs-buy and routing for a product: given a support, a coding and a document-extraction workload, how do you choose between a frontier API, a mid-size hosted model and a self-hosted small model, using your own eval set, latency, cost, data-residency and lock-in, and when do you add a router or cascade? (Part 4 Q25, Part 9 Q35, Part 10 Q18 and Q28 cover the pieces; this question is the decision across a whole product.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟡 Prompting vs RAG vs fine-tuning vs long context, applied: for (a) an HR-policy assistant, (b) a tone-and-format-sensitive marketing writer and (c) a claims-ticket classifier with 50,000 labelled examples, which do you pick first, what evidence would make you change, and in what order do you spend engineering effort? (Part 4 Q1, Part 6 Q13 and Part 7 Q36 give the framework; this applies it to concrete products.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🔴 Design an enterprise knowledge assistant over millions of documents in many systems (drive, wiki, tickets, chat) where each user may see only what they are permitted to see: connectors and ACL sync, ingestion and freshness, deletes and permission changes, hybrid retrieval with rerank, citations, evaluation, security and rollout. Focus on the integrated view: what breaks when a document's permissions change at 10:02 and a user asks at 10:03? (Part 6 Q15, Q19, Q20, Q42, Part 7 Q2 and Q5, Part 11 Q26 hold the parts; Part 6 Q50 and Part 7 Q43 are narrower designs.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🔴 Design a text-to-SQL analytics assistant for business users over a warehouse with hundreds of tables: schema retrieval and linking, a semantic layer or metric definitions, generation, validation (parse, read-only, allowlist, row and cost limits, dry run), execution, answer explanation, ambiguity handling, per-user access control, and evaluation by execution accuracy on your own questions. Why are public benchmark scores a poor guide? (Part 7 Q40 covers SQL as a tool inside RAG; this is the full product.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🔴 Design a document-extraction (IDP) pipeline for loan applications, KYC documents and invoices in an Indian bank or fintech: ingestion of scans and PDFs, OCR and layout parsing, LLM or vision-LLM extraction into a schema, rule-based cross-checks (checksums, format rules, cross-document consistency), confidence and human review queues, audit trail, PII handling, and accuracy measured per field. When does the LLM make it worse than OCR plus rules? (Part 6 Q17, Part 3 Q7, Part 9 Q32 and Part 11 Q11 are the building blocks.)
**Asked at:** BFSI and fintech GenAI teams, GCCs and product companies (company-type tag from guides and regulator material, not a candidate report)
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🔴 Design a real-time voice agent (phone or app) for a support use case: streaming ASR, turn-taking and barge-in, LLM with tool calls, streaming TTS, and the latency budget from the user finishing speech to first audio. Where does time go, what can overlap or be speculated, what fails on noisy telephony audio, and how do you evaluate and cap cost per minute? (Part 10 Q19 covers streaming; treat quoted per-stage millisecond figures as vendor or blog targets, not measured facts.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🔴 Design a conversational shopping and search assistant for a large e-commerce catalogue: query understanding, hybrid retrieval over products, hard constraints (price, size, stock) enforced by code rather than by the model, grounding every product claim in live catalogue data, multi-turn preference memory, ranking and personalisation, handling out-of-catalogue questions, and evaluating relevance, conversion and hallucinated claims. (Part 7 Q23, Q40 and Part 6 Q28 are the building blocks.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🔴 Design a customer-facing chatbot for a bank under regulatory constraints: scope (information vs transactions), grounding in approved content, no advice outside policy, authentication before account data, human handoff, PII redaction, audit logs and retention, model-risk governance, vendor and data-residency choices, red-team and rollout gates. Keep regulatory references general: which RBI and DPDP obligations would you ask compliance to confirm rather than assert? (Part 5 Q39, Part 11 Q11, Q30 and Q42 cover the building blocks.)
**Asked at:** BFSI and fintech GenAI teams, GCCs and product companies (company-type tag from guides and regulator material, not a candidate report)
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Demo to production: a prototype RAG or agent demo impresses stakeholders. List what changes before launch (data and permissions, evaluation set and quality bar, latency and cost at real volume, abuse and injection, fallbacks, monitoring, ownership), and how do you present 'what could go wrong' and a go or no-go criterion? (Part 9 Q46 is an evaluation strategy for launch; this question is the whole readiness review.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🔴 Design a multilingual assistant for Indian users (Hindi, English, Hinglish and a few regional languages, text and voice): language detection and code-mixed input, tokenizer cost, embedding and retrieval across languages, answering language and script, translation vs native generation, ASR errors on code-mixed audio, safety and tone, and per-language evaluation so averages do not hide weak languages. (Part 2 Q17, Part 6 Q35 and Part 9 Q34 cover the pieces; ASR error figures differ widely by vendor and test set.)
**Asked at:** BFSI and fintech GenAI teams, GCCs and product companies (company-type tag from guides and regulator material, not a candidate report)
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🔴 Code: build a mini-RAG pipeline end to end in plain Python with numpy only and a mocked LLM: chunking with metadata, BM25 plus a toy dense retriever, reciprocal-rank fusion, a simple reranker, prompt assembly with a token budget, a citation checker that rejects claims without a supporting retrieved chunk, abstention on weak retrieval, and a tiny eval (recall@k and citation precision) on a handwritten set. (Part 6 Q14 and Part 7 Q15 build pieces; this question is the integrated, tested pipeline.)
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐ 🟡 Code: write a tool-calling agent loop with a mocked model: tool registry with schema validation, step, token and wall-clock budgets, loop detection, structured error feedback, a trace of every step, and tests for a runaway loop and a hallucinated tool name. (Part 3 Q11 and Part 8 Q15 are simpler loops; this adds budgets and tracing from Part 8 Q4 and Q38.)
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐ 🟡 Code: build a text-to-SQL harness against an in-memory sqlite3 database with a mocked generator: schema-to-prompt, SQL validation (single SELECT only, parsed table and column allowlist, LIMIT injection, timeout), a repair retry using the error message, and an execution-accuracy evaluator that compares result sets rather than SQL strings.
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟡 Code: implement a semantic cache for LLM answers with a toy embedding: similarity threshold, tenant and model in the cache key, TTL, exclusion of personalised or time-sensitive queries, and a false-hit audit that measures wrong-answer rate on paraphrase and near-miss pairs. Why are published threshold values not transferable? (Part 10 Q28 covers caching strategy; Part 11 Q26 covers isolation.)
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟡 Code: write a streaming response generator (SSE-style framing) over a mocked token stream with cancellation when the client disconnects, a server-side timeout, backpressure through a bounded queue, a final usage event, and tests that a cancelled request stops consuming tokens. (Part 10 Q19 explains the path.)
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟡 Code: implement a conversation memory manager with a token budget: keep the system prompt and recent turns, summarise older turns through a mocked summariser, pin facts the user stated, drop stale tool outputs first, and test that the prompt never exceeds the budget and that pinned facts survive. (Part 8 Q8 and Part 6 Q28 are the concepts.)
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 Code: implement a router and cascade with a mocked small and large model: a cheap difficulty heuristic or confidence score, escalation on low confidence or failed validation, cost and latency accounting per request, and an offline evaluation that reports the quality-cost frontier against always-large. Name when the router itself costs more than it saves. (Part 10 Q28 is the strategy.)
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 Code: write an LLM-call harness with per-call timeout, retry with exponential backoff and jitter on retryable errors only, retry-after handling, an idempotency key, a circuit breaker with half-open probing, and a fallback model, tested with a fault-injecting fake client. (Part 11 Q15 is the concept.)
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 Design an AI code-review assistant for pull requests: diff and repository context retrieval, per-file and cross-file checks, comment ranking to avoid noise, confidence and suppression, running linters and tests as tools, posting comments safely (no secrets echoed, prompt injection from code comments), and measuring usefulness (accepted comments, false positives). (Part 8 Q46 is a coding agent that edits; this reviewer only comments.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 Design a meeting summariser: transcript with speaker labels, very long inputs, chunked or hierarchical summarisation, action items and decisions with owners, attribution without invention, multilingual and code-mixed speech, privacy and consent, and evaluation without a single gold summary. (Part 7 Q35 and Part 9 Q31 cover long-document handling and summary evaluation.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 Design semantic search plus RAG for legal or medical documents: structure-aware chunking, domain embeddings, hybrid retrieval and rerank, mandatory citations to the passage, abstention, conflicting or superseded sources, and review by a professional. What does published evidence say about hallucination in retrieval-based legal research tools, and why must you not assume RAG removes it? (Part 6 Q26, Q27, Q37 and Q38 cover the mechanisms; the study figures are contested and must be hedged.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 Design a content moderation pipeline for user posts at high volume: rules and hash lists, a cheap classifier, an LLM tier with the policy in the prompt, a human review queue, thresholds and the fail-open vs fail-closed choice, appeals, audit logs, drift as attackers adapt, and how you measure precision and recall per category. (Part 5 Q24, Q28 and Q29 cover safety classifiers and guardrail cost.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Design batch enrichment of 20 million product or ticket rows with an LLM (categories, attributes, summaries): model choice per field, prompt and schema, batching, idempotent checkpointed processing, retries and poison rows, sampling-based quality audits, cost estimate and budget stop, and re-runs when the prompt changes. (Part 10 Q34 covers batch serving; this is the application-level pipeline.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Design LLM re-ranking for personalised recommendations or search: candidate generation by classic models, what the LLM sees and returns, latency and cost limits (which candidates, which users), cold start, offline evaluation against logged clicks and its biases, online A/B tests, and fallbacks when the LLM is slow. (Part 7 Q19 and Part 9 Q30 are related.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Design a multi-tenant SaaS 'chat with your data' product: per-tenant ingestion, shared vs dedicated indexes by tenant size, isolation tests, per-tenant configuration and prompts, noisy-neighbour limits, per-tenant cost attribution and budgets, offboarding and deletion, and tenant-level quality reporting. (Part 6 Q42, Part 10 Q49 and Part 11 Q16 and Q26 are the parts.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 Design an agent-assist copilot for human support agents (suggested replies, retrieved policy snippets, case summaries, next-best action) rather than an autonomous bot: what the human sees, edit and accept signals as free labels, latency in a live chat, when it must stay silent, risk of automation bias, and measuring handle time and quality. (Part 3 Q41 designs an autonomous support bot; this is the assist variant.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
<!-- ANSWER_PENDING -->

### Q29 ⭐ 🔴 Design the data flywheel after launch: capture feedback and implicit signals, turn failures into eval cases and fine-tuning data, privacy and consent for using logs, bias in feedback, what to automate and what to review by hand, and how you stop the loop from locking in errors. (Part 11 Q20, Part 9 Q15 and Part 4 Q47 hold the pieces.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
<!-- ANSWER_PENDING -->

### Q30 ⭐ 🔴 AI code review: this LLM-written RAG service (FastAPI-style) has bugs: tenant filter applied after top-k, the embedding model name read from a mutable global, no request timeout, unbounded context, streaming that ignores client disconnect, cache key without tenant, citations built from model text instead of chunk IDs, API key logged, blocking embedding calls inside an async handler. Find the bugs, rank them by risk, and describe the fixes and the tests you would add. (Part 6 Q43 reviews ingestion and retrieval code; this reviews the serving layer.)
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
<!-- ANSWER_PENDING -->

### Q31 ⭐ 🔴 Incident review: after a nightly reindex, answers about refund policy became subtly wrong with no errors and no alert. Walk through the investigation (retrieval traces, chunk diffs, embedding or parser version change, stale duplicates, prompt version), the immediate rollback, the blameless write-up and the three controls that would have caught it. (Part 6 Q11 and Q21, Part 11 Q4 and Q21, and Part 9 Q42 give the tools.)
**Asked at:** senior GenAI roles; expert gap-check, no candidate report found
<!-- ANSWER_PENDING -->

### Q32 ⭐ 🟡 Code: build a prompt-template engine with versioned templates, typed variables, escaping of untrusted inserted content, a token-length check, rendering tests, and a changelog diff between versions; show how a template change is evaluated before promotion. (Part 11 Q33 builds the registry; this builds rendering and safety.)
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
<!-- ANSWER_PENDING -->

### Q33 ⭐ 🟡 Code: build a mini RAG evaluation run: a golden set, retrieval metrics, a deterministic faithfulness proxy and a mocked judge, per-slice breakdown, a bootstrap confidence interval, and an ablation comparing BM25, dense and hybrid retrieval on the same questions, with a statement of what the sample size can and cannot show. (Part 9 Q40 and Q38 cover the harness and bootstrap.)
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
<!-- ANSWER_PENDING -->

### Q34 ⭐ 🔴 Design a GenAI assistant for an air-gapped or on-premise deployment (a regulated customer cannot use external APIs): open-weight model choice and licence checks, quantisation and hardware sizing, an offline update process for models, indexes and prompts, observability without sending data out, evaluation and security patching. (Part 10 Q3, Q8 and Q35 and Part 11 Q17 are the inputs.)
**Asked at:** senior GenAI roles; expert gap-check, no candidate report found
<!-- ANSWER_PENDING -->

### Q35 ⭐ 🔴 Design an agentic workflow for insurance claims or loan underwriting support: document intake, tool calls to internal systems, a plan with approval gates, evidence packs with citations, human sign-off for decisions, audit trail, fairness and explainability concerns, and what the agent must never decide alone. (Part 8 Q24, Q40 and Q49 and Part 11 Q24 cover controls.)
**Asked at:** BFSI and fintech GenAI teams, GCCs and product companies (company-type tag from guides and regulator material, not a candidate report)
<!-- ANSWER_PENDING -->

### Q36 ⭐ 🔴 Critique exercise: a candidate proposes 'LangChain agent + GPT-class API + vector database' for an internal HR assistant. List the questions you would ask, the five biggest risks they have not addressed (permissions, evaluation, injection, cost, freshness), and the simplest design you would try first. What does 'simplest thing that could work' look like here? (Part 8 Q3 covers workflows vs agents.)
**Asked at:** senior GenAI roles; expert gap-check, no candidate report found
<!-- ANSWER_PENDING -->

### Q37 ⭐ 🔴 Design the degradation and fallback ladder for a GenAI feature: provider outage, slow retrieval, reranker down, cache poisoned, budget exhausted, guardrail service failing, and what the user sees at each step (full answer, answer without rerank, cached answer, search-only results, graceful refusal). How do you test the ladder and decide fail-open vs fail-closed per layer? (Part 11 Q14 and Q15 and Part 10 Q29 and Q46 cover the components.)
**Asked at:** senior GenAI roles; expert gap-check, no candidate report found
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🔴 Explain a GenAI launch decision to a non-technical executive: the risk register (hallucination, leakage, injection, cost overrun, vendor change, regulation), what evidence you would show (eval results with intervals, red-team results, cost model, rollout plan), what you would not promise, and the go, staged-go or no-go call. (Part 11 Q42 covers the compliance rollout; Part 1 Q36 explains transformers to stakeholders.)
**Asked at:** senior GenAI roles; expert gap-check, no candidate report found
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🔴 Code: build ACL-aware retrieval into a mini-RAG: documents with owner and group permissions, a permission-aware filter applied inside the search (not after), permission changes and deletions propagating to the index, and a leakage test suite that proves a user never gets a forbidden chunk even through the cache and the citations. (Part 6 Q15 and Q44 and Part 11 Q26 give the theory.)
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🔴 Code: build an idempotent, checkpointed batch-enrichment runner for an LLM over a CSV or sqlite table: deterministic row keys, resume after a crash, bounded concurrency with rate limiting, retries with a dead-letter table, a cost budget stop, schema-validated outputs, and a sample-audit report. Test with a fault-injecting mock model.
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
<!-- ANSWER_PENDING -->
