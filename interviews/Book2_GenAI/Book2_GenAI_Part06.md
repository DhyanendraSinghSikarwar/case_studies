# Book 2 — Part 06: RAG Basics (chunking, embeddings, vector databases, retrieval)

**Topic:** why and how RAG works, the end-to-end pipeline, chunking, parsing and ingestion, embeddings and embedding-model choice, vector databases and ANN indexes (HNSW, IVF, PQ), retrieval basics (similarity, top-k, filtering, access control), prompting the generator, evaluation basics, debugging, cost and latency, index sizing and operations, and RAG security basics.
**Target:** 50  |  **Actual:** 53 (⭐⭐⭐ 15, ⭐⭐ 27, ⭐ 11)  |  **Date:** 2026-10-24  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Book 1 already covers general ANN indexes (B1P07-Q20), cosine vs dot product vs Euclidean (B1P07-Q16, B1P09-Q38), BM25 vs dense vs hybrid in search (B1P07-Q26), bi-encoder vs cross-encoder (B1P07-Q37, B1P09-Q45), embeddings for semantic search (B1P09-Q19) and embedding operations (B1P07-Q49); answers here must be RAG-specific, cross-reference those and not repeat them. Part 4 Q1 owns the prompting vs RAG vs fine-tuning ladder (Q13 here covers RAG vs long context and RAG-specific cases); Part 1 Q19 owns lost-in-the-middle; Part 3 owns prompt and tool design and prompt-injection basics (Q34); Part 5 covers guardrails. Advanced RAG (hybrid fusion, reranker depth, GraphRAG, query rewriting, multi-hop) is Part 7; evaluation depth (RAGAS, LLM-as-judge, benchmarks) is Part 9; injection, monitoring and LLMOps depth is Part 11; serving is Part 10. Vector-store products, prices and library parameter names change quickly: answers must hedge product claims and say to check current docs. Source articles contain errors that answers must not repeat (see the sources note: an HNSW memory figure that is wrong by an order of magnitude, an unsupported hybrid-search improvement claim, and embedding prices that will go stale).

---

### Q1 ⭐⭐⭐ 🟢 What problem does RAG solve that a standalone LLM cannot, and why is it preferred over frequent retraining?
**Asked at:** all types; service-company, GCC and product GenAI loops
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Walk through a basic RAG pipeline end to end (offline indexing and online retrieval and generation).
**Asked at:** all types; GenAI-engineer and RAG-design loops
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What is chunking, and why does chunk size matter for retrieval quality?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟡 How do you choose chunk size and overlap? Compare fixed-size, recursive, structure-aware, semantic and parent-document chunking.
**Asked at:** all types; product, GCC, GenAI startups
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 What is an embedding, why does dense retrieval work, and why must indexing and querying use the same embedding model?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 How do you choose an embedding model for RAG (domain, language, dimension, max input length, cost, evaluation on your own data)?
**Asked at:** product, GCC, GenAI startups
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 What does a vector database do, and how do you choose between a dedicated store, pgvector and an in-process library such as FAISS?
**Asked at:** all types; product, GCC, platform teams
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 How do approximate nearest-neighbour indexes work for RAG (HNSW, IVF, product quantization), and what are their recall and latency knobs?
**Asked at:** product, GenAI startups, platform teams
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Which similarity metric do you use for embeddings (cosine, dot product, L2), and how do you pick top-k or a similarity threshold?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 How do you evaluate retrieval separately from generation (recall@k, precision@k, MRR, nDCG, a golden set)?
**Asked at:** product, GenAI startups, GCC, evaluation-focused rounds
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 A RAG answer is wrong even though the right document exists. How do you debug it?
**Asked at:** all types; reported in interview-prep posts for GenAI-engineer loops
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 How do you prompt the generator in a RAG system (grounding, permission to say "I don't know", citations, context ordering)?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 RAG vs fine-tuning vs stuffing everything into a long context: how do you decide for a specific product?
**Asked at:** all types; product, GCC, GenAI startups
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 Code: build a minimal RAG pipeline from scratch (chunk, embed, retrieve by cosine similarity, assemble the prompt, call a mocked LLM).
**Asked at:** product, big tech, live-coding rounds
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 How do metadata filtering and access control work in RAG? Why does post-filtering fail, and how do you guarantee users never see documents they lack permission for?
**Asked at:** product, GCC, regulated-industry and enterprise teams
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟡 What pitfalls come with chunk size and overlap in practice (tokens vs characters, boundaries, chunk metadata, duplicated text)?
**Asked at:** product, GenAI startups, GCC
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟡 How do you ingest PDFs, tables, scans and HTML for RAG (parsing, OCR, layout-aware extraction, tables as text)?
**Asked at:** product, GCC, finance and enterprise teams
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟡 What is parent-document (small-to-big) retrieval, and when does returning a larger context around a hit help?
**Asked at:** product, GenAI startups
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 What does a good ingestion pipeline do (cleaning, boilerplate removal, deduplication, versioning, stable chunk IDs)?
**Asked at:** product, GCC, platform teams
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 How do you keep a RAG index fresh (incremental updates, deletes, tombstones), and what happens when deleted documents still surface?
**Asked at:** product, GCC, platform teams
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 What happens when you change the embedding model? How do you migrate an index safely?
**Asked at:** product, platform teams, GenAI startups
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 What are asymmetric query and document embeddings (instruction prefixes, query length, normalisation), and why do they matter?
**Asked at:** product, GenAI startups
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 How do embedding dimension, truncation and quantisation affect quality and storage? Work through the storage maths.
**Asked at:** product, platform teams, GenAI startups
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 How do you tune top-k: fixed vs adaptive k, similarity thresholds, deduplicating near-identical chunks, and MMR diversification?
**Asked at:** product, GenAI startups, GCC
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 How do you assemble the context for the prompt (ordering, token budget, truncation, the lost-in-the-middle effect)?
**Asked at:** product, GenAI startups, GCC
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 How do you produce reliable citations and attribution in RAG (chunk IDs, span-level citations, verifying that a citation supports the claim)?
**Asked at:** product, GCC, regulated-industry teams
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 What should a RAG system do when retrieval finds nothing relevant (abstaining, score thresholds, fallbacks)?
**Asked at:** product, GCC, customer-facing teams
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 How do you handle multi-turn conversations in RAG (standalone query rewriting, limited history, metadata filters)?
**Asked at:** product, GenAI startups, customer-facing teams
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 When does keyword search (BM25) beat dense retrieval in RAG, and why do teams combine them (hybrid search basics)?
**Asked at:** all types; product, GenAI startups
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 What does reranking add to RAG (retrieve about 50, rerank to about 5), and what does it cost in latency?
**Asked at:** product, GenAI startups, GCC
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 What is the latency budget of a RAG request across embedding, search, reranking and generation, and how do caching and streaming help?
**Asked at:** product, GCC, platform teams
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 How do you estimate the cost of a RAG system (indexing, storage, per-query embedding and generation tokens)? Work through an example.
**Asked at:** product, GCC, platform teams
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 Does a 50-million-chunk index fit in memory? Estimate the memory for HNSW vs IVF-PQ and decide.
**Asked at:** product, platform teams, GenAI startups
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 How do you tune recall against latency (efSearch, nprobe) and measure recall for a live index without ground truth?
**Asked at:** product, platform teams
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 How does multilingual data change a RAG design (multilingual embeddings, per-language indexes, translation)?
**Asked at:** India product companies, GCCs, GenAI startups
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 What is indirect prompt injection through retrieved documents, and what basic defences does a RAG system need?
**Asked at:** product, GCC, security-conscious teams
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 Why can RAG still hallucinate (retrieval miss, ignored context, conflicting documents, over-trust), and how do you reduce it?
**Asked at:** all types; product, GCC
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 What should a RAG system do when retrieved documents conflict or are out of date (recency, authority, showing both sides)?
**Asked at:** product, GCC, enterprise teams
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 How do you evaluate generation in RAG (faithfulness, answer relevance, correctness) and how do these map to retrieval failures?
**Asked at:** product, GenAI startups, GCC, evaluation-focused rounds
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 How do you build a golden evaluation set for RAG (real queries, relevance labels, synthetic questions and their pitfalls)?
**Asked at:** product, GenAI startups, evaluation-focused rounds
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 How do you monitor and debug a RAG system in production (retrieved chunk IDs and scores, per-stage latency, feedback loops)?
**Asked at:** product, GCC, platform teams
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 What are the security and privacy risks in enterprise RAG (access control at retrieval, tenant isolation, PII in the index, logging)?
**Asked at:** product, GCC, regulated-industry and enterprise teams
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🟡 AI code review: this LLM-written RAG ingestion and retrieval code has bugs (embedding-model mismatch, missing normalisation, filtering after top-k, deletes that leave vectors, off-by-one chunk overlap). Find and fix them.
**Asked at:** product, big tech, AI-era code-review rounds
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🔴 A strict metadata filter returns only 2 results when the user wanted 10. Why does it happen, and how do you fix it (pre-filtering, post-filtering, filter-aware ANN)?
**Asked at:** platform teams, product, GenAI startups, senior roles
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🔴 Design question: 800 million vectors and a 200 GB RAM budget. Which index do you choose, and how do you recover recall?
**Asked at:** platform teams, senior roles at product companies
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🔴 Recall is 0.90 and you need 0.97 without changing the embedding model. What do you change, and what does it cost?
**Asked at:** platform teams, product, senior roles
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🔴 How do you evaluate chunking strategies empirically (experiment design, retrieval metrics, ablations, confounders)?
**Asked at:** product, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🔴 How does semantic chunking work (similarity breakpoints), and what does the evidence say about when it beats simpler chunking?
**Asked at:** product, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🔴 How do you answer a question that needs information from 10 documents when they do not fit in the context window?
**Asked at:** product, GenAI startups, senior roles
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🔴 Design question: a RAG assistant for customer support over millions of documents with per-user permissions and fresh content.
**Asked at:** senior roles at product companies, GCCs, GenAI startups
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🔴 Design question: RAG over financial-report PDFs with tables (parsing pipeline, chunking, retrieval, evaluation).
**Asked at:** senior roles at fintech, GCCs, enterprise teams
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🔴 When and how do you fine-tune an embedding model for your domain (contrastive training, hard negatives, evaluation, risks)?
**Asked at:** research-leaning teams, GenAI startups, senior roles
<!-- ANSWER_PENDING -->

### Q53 ⭐ 🔴 What are embedding inversion and related privacy risks in vector stores, and what mitigations exist?
**Asked at:** security-conscious teams, regulated-industry teams, senior roles
<!-- ANSWER_PENDING -->
