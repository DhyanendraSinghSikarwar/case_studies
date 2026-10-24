# Book 2 Part 06 review (Wave C)

Date: 2026-10-24. Reviewer: lead session (independent of the four answer agents). Scope: 53 questions, Q1-Q53. Target band per plan.md: Rs 30-80 LPA.

## Process
Per-agent scratch files merged by heading with a script that refuses any block whose heading or "Asked at" line differs from the frozen list (53 of 53 merged, 0 skipped, no clobbering, no spend-limit stops this part). Lead edits were applied after the final merge. The Example field was mandatory in every brief, so no Example gaps appeared (the Part 4 problem).

## Structure checks (scripted)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q53 | pass |
| Star order and counts 15 / 27 / 11 | pass (matches header) |
| Required fields (Say this first, Then explain, Example, Follow-ups, Common mistakes) | pass for all 53 |
| Internal cross-references | all listed and checked against question titles; every one points to a topically correct question |

## Code
- 51 Python blocks extracted with the proper line-start fence rule and run standalone with `python3 -I` (numpy, torch single-thread, standard library; sklearn, faiss, rank_bm25 and sentence-transformers are not installed, so every demo uses TOY hashed bag-of-words or synthetic vectors, a from-scratch IVF index and a from-scratch BM25, all labelled toy or synthetic, and every LLM is mocked): all exit 0.
- Printed numbers compared with the text after re-running: Q8 (IVF recall@10 0.901 at nprobe 1, 0.990 at nprobe 2, 1.000 from nprobe 4; PQ 3,072 bytes vs 96 bytes, 32x; 100M x 768 fp32 = 307.2 GB), Q10 (recall@3 0.3333, precision@3 0.3333, MRR 0.5, nDCG@5 0.5784 equal to the hand computation DCG 2.7541 / IDCG 4.7619), Q23 (storage table; truncation recall 0.46 at 128 dims, 0.26 at 64, int8 0.98, 1-bit 0.41), Q33 (50M x 768: raw fp32 153.6 GB, int8 38.4 GB, HNSW over int8 45.2 GB, IVF-PQ 5.4 GB), Q43 (each of the six bugs shows its symptom, fixes pass), Q45 (800M x 768 raw about 2.46 TB; IVF-PQ at 96 B about 77 GB). Timings in Q8, Q34, Q46 and Q52 are machine-specific and labelled. I did not diff every other block's printed numbers; for those I relied on exit codes and the agents' reports.
- Honest toy results are kept: Q3 needs an exaggerated overlap of 6 to rescue the split fact, labelled as chosen only to make the effect visible; Q14's first query fails because the toy matches words, kept as a teaching point; Q17 shows the correct table row ranking 2nd without caption and header and 1st as row sentences; Q19's demo threshold is 0.6 because the mirror text scored 0.68; Q23 shows naive truncation collapsing recall (contrasted with models trained for truncation); Q29's paraphrase query scores zero in BM25 so its top document is just a tie, which is stated as a weakness of rank-only fusion; Q30's reranker is hand-written over synthetic data so the MRR jump from 0.857 to 1.0 shows the mechanism only; Q44's toy is IVF, so HNSW fragmentation under pre-filtering is stated as the guide's report; Q47 shows the chunk-level vs span-level metric pitfall and says toy results are not claims about real corpora; Q52's hard-negative gain is one seed and hedged; Q53's toy is explicitly not a real inversion attack.

## Source errors found and kept out of the answers
- The techinterview vector-search article says 100M x 768 float32 vectors need "the low terabytes"; the raw size is about 307 GB. Q8, Q23, Q33 and Q45 compute their own figures and say so.
- The unsupported "hybrid search gives 5-20% better recall" claim, embedding model prices and dimensions, and the "0.95 to 0.99 recall costs 3-5x latency" figure are not quoted as fact (the last is labelled reported and illustrative).

## Facts web-verified this session
| Claim | Result |
|---|---|
| RAG paper abstract: parametric plus non-parametric memory (dense vector index of Wikipedia through a pretrained retriever), state of the art on three open-domain QA tasks, two formulations without the RAG-Sequence/RAG-Token labels, provenance and updating as open problems | confirmed (arXiv 2005.11401 abstract opened) |
| HNSW abstract: stack of proximity graphs over nested subsets, random exponentially decaying layers, logarithmic complexity scaling stated without proof, beats earlier vector-only methods and NSW | confirmed (arXiv 1603.09320 abstract opened) |
| Reciprocal rank fusion: score = sum of 1/(k + rank) over rankers; k = 60 gave the best average result without tuning in the original SIGIR 2009 work (Cormack, Clarke, Buettcher) | confirmed via search (secondary descriptions; paper text not opened) |
| MMR: argmax of lambda*Sim(d, q) - (1 - lambda)*max Sim(d, selected) (Carbonell and Goldstein, SIGIR 1998) | confirmed via search (formula from secondary sources; original not opened) |
| Prep-guide facts (chunking starting points, HNSW/IVF knobs, filtering behaviour, evaluation split, debugging flow) | stated as reported guidance from the opened techinterview and Analytics Vidhya pages |

## Not verified (written from memory or reported guidance, hedged in the text)
BM25 constants (k1 = 1.5, b = 0.75 are common defaults); the Wilson interval formula (standard); Matryoshka-style training concentrating information in leading dimensions; MinHash with LSH for near-duplicate detection at scale; the HNSW base-layer link formula of about 2*M*4 bytes per vector (flagged as an assumption in Q33 and Q45); that efSearch is tunable on a live index while M and efConstruction need a rebuild (attributed to the prep article, check docs); some stores delete lazily and compact later; filter-aware search modes exist in some products; some embedding models expect different query and document prefixes (check the model card); Vec2Text-style inversion results; RAPTOR-style hierarchical summarisation; OPQ rotation helping recall; hard-negative mining practice and false-negative risk; NVMe IOPS ("commonly rated for hundreds of thousands", check the spec); the alternative nDCG gain formula with 2^gain - 1; prompt caching softening repeat long-context cost; lost-in-the-middle (reported, cross-referenced to Part 1 Q19, not re-verified); LoRA plus RAG as a reported pattern; a query-side transform as a way to avoid re-embedding (Q52).

## Evidence limits (unchanged)
- No candidate-reported RAG questions were found for any company; evidence is prep articles, LinkedIn interview-prep posts (not verified candidate reports) and two primary abstracts. The articles name no hiring companies or levels. No source states a salary band. Stars and "Asked at" tags are indicative.
- All hardware, latency, cost and capacity numbers are assumed or synthetic and labelled; demos use toy embeddings and mock LLMs, so none of them measures real semantic retrieval quality.
- Vector-store products, library parameter names and prices drift; answers hedge product claims and say to check current docs.

## Unresolved
- Hybrid-search fusion depth, reranker depth, GraphRAG, query rewriting and multi-hop belong to Part 7; evaluation depth (RAGAS, LLM-as-judge) to Part 9; injection, monitoring and LLMOps depth to Part 11; serving to Part 10 (pointers only here).
