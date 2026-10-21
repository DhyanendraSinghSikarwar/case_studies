# Wave A brief — Book 2 (GenAI / LLM / RAG / Agentic AI + Deployment) research agents

Read fully, plus plan.md §3, §4, §5 (Book 2 table), §11 and style_guide.md. Audience: Data Scientist / ML Engineer / GenAI Engineer candidates (₹30–80 LPA India MNCs/product cos/GCCs + Europe/global), 2025–2026 loops.

## Book 2 parts (stay in your lane; check question_index.md "Book 2" section before adding)
1 Transformer internals: attention, positional encoding, KV cache (45)
2 Tokenization, pretraining, scaling laws, decoding strategies (40)
3 Prompt engineering, structured outputs, function calling (40)
4 Fine-tuning: SFT, LoRA/QLoRA, PEFT, distillation (45)
5 Alignment: RLHF, DPO, safety, guardrails (35)
6 RAG basics: chunking, embeddings, vector DBs, retrieval (50)
7 Advanced RAG: hybrid search, reranking, GraphRAG, query rewriting (45)
8 Agents: ReAct, tool use, planning, memory, MCP, multi-agent (50)
9 LLM evaluation: RAGAS, LLM-as-judge, hallucination, benchmarks (45)
10 Deployment: vLLM, TGI, quantization, batching, latency/cost (45)
11 LLMOps: monitoring, tracing, prompt versioning, security/prompt injection (40)
12 GenAI system design + coding (mini-RAG/agent from scratch) (40)
(Book 1 Part 9 already covers light NLP/transformer intro and GenAI-in-classical-loop; Book 4 owns generic MLOps/Docker/K8s; Book 6 owns GenAI scenarios. Don't duplicate those; Book 2 is the deep treatment.)

## Steps
1. Web research for 2025–2026 interview questions on your topic: Glassdoor, AmbitionBox, LeetCode Discuss, Blind, GfG experiences, Medium/LinkedIn/dev.to write-ups, Interview Query/Prepfully/Dataford-type banks, company engineering blogs; India (Flipkart, Swiggy, PhonePe, Amazon India, Microsoft IDC, Walmart/JPMC/GS GCCs, Sarvam/Krutrim-type startups) and Europe (Spotify, Zalando, Booking, Klarna, SAP). Previous Book 1 agents only read search snippets: this time use WebFetch on promising pages where allowed (pages that return 403/429 — note it). NEVER invent sources/URLs; label what you did not open.
2. Save `research_notes/Book2_PartNN_sources.md`: question → sources (real URLs seen/opened) → frequency → recency; mark each question 'found in sources' vs 'expert gap-check'; AI-era notes; blocked/thin sources stated honestly.
3. Merge duplicates; stars by frequency/importance (⭐⭐⭐ most loops, ⭐⭐ regular, ⭐ senior/niche); sort ⭐⭐⭐→⭐ (within star easy→hard); meet/exceed the part target (add important missing questions). Include current-state topics (reasoning models, MCP, long context, prompt caching, speculative decoding, structured outputs, agentic frameworks, eval of agents) where relevant to your topic.
4. Write `Book2_GenAI/Book2_GenAI_PartNN.md`: header (title, topic, target, actual, star counts), then questions in EXACT format:
### Q12 ⭐⭐⭐ 🟡 <Question text>
**Asked at:** <companies / company types>
<!-- ANSWER_PENDING -->
Numbered Q1..Qn continuous. No answers. 'Asked at' = company types unless a real report names the company.
5. Append rows once (single shell `>>`, no read-modify-write; other agents append concurrently) to question_index.md: `| B2PNN-Q1 | N | canonical question |`.
6. Edit ONLY your own files + that append. Scratch files: only under a uniquely named folder in the local temp dir, never generic names like gen.py. Writing files via the Write tool is more reliable than bash heredocs on this machine.
FINAL REPORT (short): question count, star breakdown, top 10 ⭐⭐⭐ questions, what web access worked/was blocked, issues.
