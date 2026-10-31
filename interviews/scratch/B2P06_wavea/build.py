QS = [
(3,'🟢',"What problem does RAG solve that a standalone LLM cannot, and why is it preferred over frequent retraining?","all types; service-company, GCC and product GenAI loops"),
(3,'🟢',"Walk through a basic RAG pipeline end to end (offline indexing and online retrieval and generation).","all types; GenAI-engineer and RAG-design loops"),
(3,'🟢',"What is chunking, and why does chunk size matter for retrieval quality?","all types"),
(3,'🟡',"How do you choose chunk size and overlap? Compare fixed-size, recursive, structure-aware, semantic and parent-document chunking.","all types; product, GCC, GenAI startups"),
(3,'🟡',"What is an embedding, why does dense retrieval work, and why must indexing and querying use the same embedding model?","all types"),
(3,'🟡',"How do you choose an embedding model for RAG (domain, language, dimension, max input length, cost, evaluation on your own data)?","product, GCC, GenAI startups"),
(3,'🟡',"What does a vector database do, and how do you choose between a dedicated store, pgvector and an in-process library such as FAISS?","all types; product, GCC, platform teams"),
(3,'🟡',"How do approximate nearest-neighbour indexes work for RAG (HNSW, IVF, product quantization), and what are their recall and latency knobs?","product, GenAI startups, platform teams"),
(3,'🟡',"Which similarity metric do you use for embeddings (cosine, dot product, L2), and how do you pick top-k or a similarity threshold?","all types"),
(3,'🟡',"How do you evaluate retrieval separately from generation (recall@k, precision@k, MRR, nDCG, a golden set)?","product, GenAI startups, GCC, evaluation-focused rounds"),
(3,'🟡',"A RAG answer is wrong even though the right document exists. How do you debug it?","all types; reported in interview-prep posts for GenAI-engineer loops"),
(3,'🟡',"How do you prompt the generator in a RAG system (grounding, permission to say \"I don't know\", citations, context ordering)?","all types"),
(3,'🟡',"RAG vs fine-tuning vs stuffing everything into a long context: how do you decide for a specific product?","all types; product, GCC, GenAI startups"),
(3,'🟡',"Code: build a minimal RAG pipeline from scratch (chunk, embed, retrieve by cosine similarity, assemble the prompt, call a mocked LLM).","product, big tech, live-coding rounds"),
(3,'🟡',"How do metadata filtering and access control work in RAG? Why does post-filtering fail, and how do you guarantee users never see documents they lack permission for?","product, GCC, regulated-industry and enterprise teams"),
(2,'🟡',"What pitfalls come with chunk size and overlap in practice (tokens vs characters, boundaries, chunk metadata, duplicated text)?","product, GenAI startups, GCC"),
(2,'🟡',"How do you ingest PDFs, tables, scans and HTML for RAG (parsing, OCR, layout-aware extraction, tables as text)?","product, GCC, finance and enterprise teams"),
(2,'🟡',"What is parent-document (small-to-big) retrieval, and when does returning a larger context around a hit help?","product, GenAI startups"),
(2,'🟡',"What does a good ingestion pipeline do (cleaning, boilerplate removal, deduplication, versioning, stable chunk IDs)?","product, GCC, platform teams"),
(2,'🟡',"How do you keep a RAG index fresh (incremental updates, deletes, tombstones), and what happens when deleted documents still surface?","product, GCC, platform teams"),
(2,'🟡',"What happens when you change the embedding model? How do you migrate an index safely?","product, platform teams, GenAI startups"),
(2,'🟡',"What are asymmetric query and document embeddings (instruction prefixes, query length, normalisation), and why do they matter?","product, GenAI startups"),
(2,'🟡',"How do embedding dimension, truncation and quantisation affect quality and storage? Work through the storage maths.","product, platform teams, GenAI startups"),
(2,'🟡',"How do you tune top-k: fixed vs adaptive k, similarity thresholds, deduplicating near-identical chunks, and MMR diversification?","product, GenAI startups, GCC"),
(2,'🟡',"How do you assemble the context for the prompt (ordering, token budget, truncation, the lost-in-the-middle effect)?","product, GenAI startups, GCC"),
(2,'🟡',"How do you produce reliable citations and attribution in RAG (chunk IDs, span-level citations, verifying that a citation supports the claim)?","product, GCC, regulated-industry teams"),
(2,'🟡',"What should a RAG system do when retrieval finds nothing relevant (abstaining, score thresholds, fallbacks)?","product, GCC, customer-facing teams"),
(2,'🟡',"How do you handle multi-turn conversations in RAG (standalone query rewriting, limited history, metadata filters)?","product, GenAI startups, customer-facing teams"),
(2,'🟡',"When does keyword search (BM25) beat dense retrieval in RAG, and why do teams combine them (hybrid search basics)?","all types; product, GenAI startups"),
(2,'🟡',"What does reranking add to RAG (retrieve about 50, rerank to about 5), and what does it cost in latency?","product, GenAI startups, GCC"),
(2,'🟡',"What is the latency budget of a RAG request across embedding, search, reranking and generation, and how do caching and streaming help?","product, GCC, platform teams"),
(2,'🟡',"How do you estimate the cost of a RAG system (indexing, storage, per-query embedding and generation tokens)? Work through an example.","product, GCC, platform teams"),
(2,'🟡',"Does a 50-million-chunk index fit in memory? Estimate the memory for HNSW vs IVF-PQ and decide.","product, platform teams, GenAI startups"),
(2,'🟡',"How do you tune recall against latency (efSearch, nprobe) and measure recall for a live index without ground truth?","product, platform teams"),
(2,'🟡',"How does multilingual data change a RAG design (multilingual embeddings, per-language indexes, translation)?","India product companies, GCCs, GenAI startups"),
(2,'🟡',"What is indirect prompt injection through retrieved documents, and what basic defences does a RAG system need?","product, GCC, security-conscious teams"),
(2,'🟡',"Why can RAG still hallucinate (retrieval miss, ignored context, conflicting documents, over-trust), and how do you reduce it?","all types; product, GCC"),
(2,'🟡',"What should a RAG system do when retrieved documents conflict or are out of date (recency, authority, showing both sides)?","product, GCC, enterprise teams"),
(2,'🟡',"How do you evaluate generation in RAG (faithfulness, answer relevance, correctness) and how do these map to retrieval failures?","product, GenAI startups, GCC, evaluation-focused rounds"),
(2,'🟡',"How do you build a golden evaluation set for RAG (real queries, relevance labels, synthetic questions and their pitfalls)?","product, GenAI startups, evaluation-focused rounds"),
(2,'🟡',"How do you monitor and debug a RAG system in production (retrieved chunk IDs and scores, per-stage latency, feedback loops)?","product, GCC, platform teams"),
(2,'🟡',"What are the security and privacy risks in enterprise RAG (access control at retrieval, tenant isolation, PII in the index, logging)?","product, GCC, regulated-industry and enterprise teams"),
(1,'🟡',"AI code review: this LLM-written RAG ingestion and retrieval code has bugs (embedding-model mismatch, missing normalisation, filtering after top-k, deletes that leave vectors, off-by-one chunk overlap). Find and fix them.","product, big tech, AI-era code-review rounds"),
(1,'🔴',"A strict metadata filter returns only 2 results when the user wanted 10. Why does it happen, and how do you fix it (pre-filtering, post-filtering, filter-aware ANN)?","platform teams, product, GenAI startups, senior roles"),
(1,'🔴',"Design question: 800 million vectors and a 200 GB RAM budget. Which index do you choose, and how do you recover recall?","platform teams, senior roles at product companies"),
(1,'🔴',"Recall is 0.90 and you need 0.97 without changing the embedding model. What do you change, and what does it cost?","platform teams, product, senior roles"),
(1,'🔴',"How do you evaluate chunking strategies empirically (experiment design, retrieval metrics, ablations, confounders)?","product, GenAI startups, research-leaning teams"),
(1,'🔴',"How does semantic chunking work (similarity breakpoints), and what does the evidence say about when it beats simpler chunking?","product, GenAI startups, research-leaning teams"),
(1,'🔴',"How do you answer a question that needs information from 10 documents when they do not fit in the context window?","product, GenAI startups, senior roles"),
(1,'🔴',"Design question: a RAG assistant for customer support over millions of documents with per-user permissions and fresh content.","senior roles at product companies, GCCs, GenAI startups"),
(1,'🔴',"Design question: RAG over financial-report PDFs with tables (parsing pipeline, chunking, retrieval, evaluation).","senior roles at fintech, GCCs, enterprise teams"),
(1,'🔴',"When and how do you fine-tune an embedding model for your domain (contrastive training, hard negatives, evaluation, risks)?","research-leaning teams, GenAI startups, senior roles"),
(1,'🔴',"What are embedding inversion and related privacy risks in vector stores, and what mitigations exist?","security-conscious teams, regulated-industry teams, senior roles"),
]
n=len(QS)
c=[sum(1 for q in QS if q[0]==s) for s in (3,2,1)]
assert [q[0] for q in QS]==sorted([q[0] for q in QS],reverse=True)
hdr=f"""# Book 2 — Part 06: RAG Basics (chunking, embeddings, vector databases, retrieval)

**Topic:** why and how RAG works, the end-to-end pipeline, chunking, parsing and ingestion, embeddings and embedding-model choice, vector databases and ANN indexes (HNSW, IVF, PQ), retrieval basics (similarity, top-k, filtering, access control), prompting the generator, evaluation basics, debugging, cost and latency, index sizing and operations, and RAG security basics.
**Target:** 50  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-24  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Book 1 already covers general ANN indexes (B1P07-Q20), cosine vs dot product vs Euclidean (B1P07-Q16, B1P09-Q38), BM25 vs dense vs hybrid in search (B1P07-Q26), bi-encoder vs cross-encoder (B1P07-Q37, B1P09-Q45), embeddings for semantic search (B1P09-Q19) and embedding operations (B1P07-Q49); answers here must be RAG-specific, cross-reference those and not repeat them. Part 4 Q1 owns the prompting vs RAG vs fine-tuning ladder (Q13 here covers RAG vs long context and RAG-specific cases); Part 1 Q19 owns lost-in-the-middle; Part 3 owns prompt and tool design and prompt-injection basics (Q34); Part 5 covers guardrails. Advanced RAG (hybrid fusion, reranker depth, GraphRAG, query rewriting, multi-hop) is Part 7; evaluation depth (RAGAS, LLM-as-judge, benchmarks) is Part 9; injection, monitoring and LLMOps depth is Part 11; serving is Part 10. Vector-store products, prices and library parameter names change quickly: answers must hedge product claims and say to check current docs. Source articles contain errors that answers must not repeat (see the sources note: an HNSW memory figure that is wrong by an order of magnitude, an unsupported hybrid-search improvement claim, and embedding prices that will go stale).

---
"""
out=[hdr]
for i,(s,d,q,a) in enumerate(QS,1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
open('Book2_GenAI/Book2_GenAI_Part06.md','w',encoding='utf-8',newline='\n').write(''.join(out))
open('scratch/B2P06_wavea/index_rows.txt','w',encoding='utf-8',newline='\n').write(''.join(f"| B2P06-Q{i} | 6 | {q} |\n" for i,(s,d,q,a) in enumerate(QS,1)))
print(n,c)
