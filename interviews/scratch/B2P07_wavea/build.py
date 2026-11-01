QS = [
(3,'🟢',"Why does basic vector RAG fall short, and what does the standard advanced-RAG stack (hybrid search, reranking, query transformation) add?","all types; GenAI-engineer and RAG-design loops"),
(3,'🟡',"Hybrid search in depth: how do lexical (BM25), learned-sparse and dense retrievers differ, and how do you fuse their results?","all types; product, GenAI startups, GCC"),
(3,'🟡',"Explain reciprocal rank fusion: the formula, the role of k, its strengths and weaknesses, and code it.","all types; product, GenAI startups"),
(3,'🟡',"Weighted (alpha) fusion of retrieval scores: why raw scores cannot be mixed, how do you normalise, and how do you tune alpha?","product, GenAI startups, search teams"),
(3,'🟡',"How does cross-encoder reranking work in a RAG pipeline? Cover candidate counts, latency, fine-tuning and how you prove it helps.","all types; product, GenAI startups, GCC"),
(3,'🟡',"What is late interaction (ColBERT)? Explain MaxSim, what is precomputed, the storage cost, and when to prefer it over a bi-encoder or a cross-encoder.","product, GenAI startups, search and research-leaning teams"),
(3,'🟡',"When does query rewriting help or hurt RAG, and how do you route queries to the right transformation?","all types; product, GenAI startups"),
(3,'🟡',"What is HyDE (hypothetical document embeddings)? How does it work, when does it help, and what does it cost?","all types; product, GenAI startups"),
(3,'🟡',"What are multi-query retrieval and query expansion, and how do you combine the results of several query variants?","product, GenAI startups"),
(3,'🟡',"How do you handle multi-hop questions with query decomposition? Walk through the design, the ordering of sub-questions and the failure modes.","product, GenAI startups, agent-building teams"),
(3,'🟡',"What is contextual retrieval? Explain contextual embeddings and contextual BM25, the reported gains, and the cost.","product, GenAI startups, GCC"),
(3,'🟡',"What is GraphRAG? When would you choose it over plain vector RAG, and when not?","all types; product, GenAI startups, enterprise teams"),
(3,'🟡',"Agentic RAG vs single-pass RAG: when is an agent loop worth its cost, and how do you bound it?","all types; product, GenAI startups, agent-building teams"),
(3,'🟡',"How do you evaluate each advanced-RAG component (hybrid, reranker, rewriting) with ablations, and what do you report besides accuracy?","product, GenAI startups, GCC, evaluation-focused rounds"),
(3,'🟡',"Code: implement hybrid retrieval from scratch (BM25 plus a toy dense retriever) with RRF and weighted fusion, and compare them on a toy query set.","product, big tech, live-coding rounds"),
(2,'🟡',"What does learned sparse retrieval (SPLADE-style) add over BM25, and where does it fit in a hybrid stack?","product, search teams, research-leaning teams"),
(2,'🟡',"Which score-normalisation methods exist for fusion (min-max, z-score, rank-based), and how does each fail?","product, search teams"),
(2,'🟡',"How do you choose the candidate counts in retrieve-then-rerank (n from the first stage, k after reranking)? What is the recall ceiling?","product, GenAI startups, GCC"),
(2,'🟡',"LLM-based rerankers (pointwise, pairwise, listwise) vs cross-encoder rerankers for RAG: quality, cost, position bias and when to use each.","product, GenAI startups, big tech"),
(2,'🟡',"How do you train or fine-tune a reranker (hard negatives from the first stage, distillation from an LLM, evaluation)?","product, GenAI startups, research-leaning teams"),
(2,'🟡',"How do you serve a reranker at production latency (batching, truncation, caching, early exit, hardware)?","product, platform teams, GCC"),
(2,'🟡',"What is step-back prompting for retrieval, and how does it differ from HyDE and decomposition?","product, GenAI startups"),
(2,'🟡',"How do you route queries to different retrieval strategies (FAQ lookup, multi-hop, global summary), and how do you evaluate the router?","product, GenAI startups, platform teams"),
(2,'🟡',"Conversational RAG: how do you handle coreference, history compression and query rewriting across turns, and how do you evaluate it?","product, GenAI startups, customer-facing teams"),
(2,'🟡',"What is index-time enrichment (hypothetical questions per chunk, summaries, entity and keyword extraction, metadata), and what are its trade-offs?","product, GenAI startups, GCC"),
(2,'🟡',"Contextual retrieval in practice: how do you generate chunk context cheaply (prompt caching, lighter alternatives) and what can go wrong?","product, GenAI startups, platform teams"),
(2,'🟡',"What is RAPTOR (hierarchical summary trees)? How is the tree built, how is it queried, and how does it compare with GraphRAG?","product, GenAI startups, research-leaning teams"),
(2,'🟡',"Walk through the GraphRAG indexing pipeline (text units, entity and relationship extraction, community detection, community summaries) and its cost.","product, GenAI startups, enterprise teams"),
(2,'🟡',"What are GraphRAG's query modes (global, local, DRIFT, basic), and which question types suit each?","product, GenAI startups, enterprise teams"),
(2,'🟡',"Knowledge-graph retrieval vs GraphRAG-style summaries: when do graph databases, entity linking and text-to-Cypher help, and what are the risks?","product, enterprise teams, search teams"),
(2,'🟡',"Multi-hop retrieval strategies: iterative retrieval that interleaves reasoning and search, stopping conditions, and how to avoid drifting off-topic.","product, GenAI startups, research-leaning teams"),
(2,'🟡',"What are adaptive and self-reflective retrieval (Self-RAG, reflection tokens), and what simpler prompt-based alternatives exist?","product, GenAI startups, research-leaning teams"),
(2,'🟡',"What is corrective RAG (CRAG)? Explain the retrieval evaluator, the fallback actions, and how production systems approximate it.","product, GenAI startups, GCC"),
(2,'🟡',"How do you compress or filter retrieved context (extractive compression, LLM filtering, token budgets), and what is the risk of dropping evidence?","product, GenAI startups, GCC"),
(2,'🟡',"How do you answer questions over very long documents or many documents (hierarchical retrieval, map-reduce, iterative refinement)?","product, GenAI startups, enterprise teams"),
(2,'🟡',"When is RAG unnecessary because the corpus fits in the context window? Work through the cost and quality trade-off at scale.","product, GenAI startups, GCC"),
(2,'🟡',"Build a failure taxonomy for an advanced RAG pipeline: where does each component help, where can it hurt, and how do you attribute an error to a stage?","product, GenAI startups, GCC"),
(2,'🟡',"What is the latency and cost budget of an advanced RAG pipeline (rewriting, multiple searches, reranking, contextualisation, agent loops), and how do you control it?","product, GCC, platform teams"),
(2,'🟡',"How do you keep citations and provenance intact across rewriting, fusion, reranking and compression steps?","product, GCC, regulated-industry teams"),
(2,'🟡',"How do you combine retrieval with structured data (SQL or API tools, tables) in a RAG assistant, and how do you choose between them?","product, GCC, enterprise teams"),
(2,'🟡',"Multimodal RAG basics: how do you retrieve over images, charts and slides (captions vs multimodal embeddings), and what changes in evaluation?","product, GenAI startups, enterprise teams"),
(1,'🟡',"AI code review: this LLM-written hybrid-plus-rerank pipeline has bugs (RRF rank off by one, mixed score scales, reranking the wrong list, duplicates after fusion, dropping the original query). Find and fix them.","product, big tech, AI-era code-review rounds"),
(1,'🔴',"Design question: an enterprise assistant that must answer multi-hop analytical questions over many documents, with an agent loop, budgets and fallbacks.","senior roles at product companies, GCCs, GenAI startups"),
(1,'🔴',"Design question: global sensemaking over a corpus of about a million tokens (GraphRAG vs map-reduce vs RAPTOR vs long context). Choose and defend.","senior roles at product companies, enterprise and research teams"),
(1,'🔴',"When does reranking hurt? Discuss calibration, domain shift, truncation, flipping a correct top-1, and how you detect it.","product, GenAI startups, senior roles"),
(1,'🔴',"How do you evaluate GraphRAG against vector RAG fairly (question types, comprehensiveness and diversity judging, judge bias, cost)?","research-leaning teams, GenAI startups, senior roles"),
(1,'🔴',"How do you make agentic RAG safe (tool permissions, injection through multi-hop tool results, budgets, audit)?","security-conscious teams, product, senior roles"),
(1,'🔴',"Design question: a query-understanding layer (router, rewriter, decomposer) with fallbacks, and how you measure each part's value.","product, GenAI startups, senior roles"),
(1,'🔴',"Are LLM-based retrievers worth their cost compared with a tuned hybrid-plus-rerank stack? How do you decide?","research-leaning teams, GenAI startups, senior roles"),
(1,'🔴',"Late-interaction storage and latency maths: estimate the index size for 10 million passages with token-level vectors and compare it with single-vector and PQ-compressed options.","platform teams, search teams, senior roles"),
]
n=len(QS)
c=[sum(1 for q in QS if q[0]==s) for s in (3,2,1)]
assert [q[0] for q in QS]==sorted([q[0] for q in QS],reverse=True)
hdr=f"""# Book 2 — Part 07: Advanced RAG (hybrid search, reranking, GraphRAG, query rewriting)

**Topic:** hybrid retrieval and fusion (BM25, learned sparse, dense, RRF, weighted fusion), reranking (cross-encoders, late interaction, LLM rerankers, serving), query transformation (rewriting, HyDE, multi-query, step-back, decomposition, routing), contextual retrieval and index-time enrichment, hierarchical and graph-based retrieval (RAPTOR, GraphRAG, knowledge graphs), multi-hop, agentic, adaptive and corrective RAG, context compression, long-document strategies, evaluation, cost and safety of advanced pipelines.
**Target:** 45  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-24  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 6 already covers RAG basics, including hybrid search basics (Q29), reranking basics (Q30), multi-turn query rewriting (Q28), semantic chunking (Q48), answering from 10 documents (Q49) and embedding fine-tuning (Q52); answers here must go deeper and cross-reference, not repeat. Book 1 covers hybrid search in general search (B1P07-Q26), bi-encoder vs cross-encoder (B1P07-Q37, B1P09-Q45) and LLM reranking for recommendation (B1P07-Q43). Agents, planning and MCP belong to Part 8; evaluation depth (RAGAS, LLM-as-judge, benchmarks) to Part 9; serving to Part 10; injection, monitoring and LLMOps to Part 11. Many headline numbers in this area come from vendor blogs or authors' own abstracts (for example the Contextual Retrieval percentages, GraphRAG's judged comprehensiveness, RAPTOR's QuALITY gain): answers must label them as reported claims with their setting and must not quote blog figures such as HyDE's latency overhead as facts. Techniques and product names change quickly: hedge product claims and say to check current docs.

---
"""
out=[hdr]
for i,(s,d,q,a) in enumerate(QS,1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
open('Book2_GenAI/Book2_GenAI_Part07.md','w',encoding='utf-8',newline='\n').write(''.join(out))
open('scratch/B2P07_wavea/index_rows.txt','w',encoding='utf-8',newline='\n').write(''.join(f"| B2P07-Q{i} | 7 | {q} |\n" for i,(s,d,q,a) in enumerate(QS,1)))
print(n,c)
