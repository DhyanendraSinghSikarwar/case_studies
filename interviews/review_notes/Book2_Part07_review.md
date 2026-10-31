# Book 2 Part 07 review (Wave C)

Date: 2026-10-24. Reviewer: lead session (independent of the four answer agents). Scope: 50 questions, Q1-Q50. Target band per plan.md: Rs 30-80 LPA.

## Process
Per-agent scratch files merged by heading with a script that refuses any block whose heading or "Asked at" line differs from the frozen list (50 of 50 merged, 0 skipped, no clobbering, no spend-limit stops this part). Lead edits (Q16, Q33 sourcing updates and the header status) were applied after the final merge. The Example field was mandatory in every brief.

## Structure checks (scripted)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q50 | pass |
| Star order and counts 15 / 26 / 9 | pass (matches header) |
| Required fields (Say this first, Then explain, Example, Follow-ups, Common mistakes) | pass for all 50 |
| Internal cross-references | all listed and checked against question titles; every one points to a topically correct question |

## Code
- 50 Python blocks extracted with the proper line-start fence rule and run standalone with `python3 -I` (numpy, one torch single-thread demo in Q20 and Q50, standard library incl. sqlite3; sklearn, faiss, rank_bm25, networkx are not installed, so BM25, RRF, k-means, label propagation and connected components are written from scratch; every demo uses TOY hashed embeddings or synthetic data, and every LLM is mocked): all exit 0.
- Printed numbers compared with the text after re-running: Q3 (RRF tests pass; k=1 three-way tie at 0.667; k=60 ranking w, u, v), Q5 (shortlist recall 0.28 / 0.98 / 1.00 at n = 5 / 20 / 50; MRR 0.112 to 0.283, 0.175 to 0.983), Q15 (recall@3 and MRR table for BM25, toy dense, RRF, RRF skip-zero and weighted fusion), Q42 (each of five bugs shows its symptom: rank-from-0 flip at k=1 and crash at k=0, mixed score scales, wrong rerank list, duplicates after fusion, dropped original query; fixes pass all checks), Q50 (storage fits/does-not-fit table at 64 GB; MaxSim 15.9 ms for 1,000 candidates on this machine, labelled machine-specific). I did not diff every other block's printed numbers; for those I relied on exit codes and the agents' reports.
- Honest toy results are kept: Q2 BM25 zero-score ties pollute RRF (kept as a printed trap); Q5 random tie-breaking exposes the shortlist ceiling; Q7 fusion ends slightly below rewrite-only on average (0.611 vs 0.667); Q9 a drifting variant adds noise without dropping recall; Q15 plain RRF loses to weighted fusion on paraphrase queries because BM25's all-zero list still votes, with the warning that 10 toy queries cannot rank the methods in general; Q19 most of the mock gain is averaging noise; Q20 NDCG@5 falls from 0.95 to about 0.55 under a shifted relevance rule; Q25's 0.38 to 1.00 lift is flagged as optimistic; Q35 hierarchical recall@5 is only 0.47 vs flat 0.20 and the text says stage-2 scoring is the weak part; Q37 shows overlapping failures giving different shares under nested-oracle and first-failure attribution; Q41's combined 1.0 is by construction of the hand-made toy; Q44 shows GraphRAG-style indexing about 2.8x map-reduce under assumed numbers and quotes no measured quality result; Q46 shows order-swapping removes position bias but not length bias.

## Facts web-verified this session
| Claim | Result |
|---|---|
| GraphRAG abstract (arXiv 2404.16130): entity graph, pre-generated community summaries, partial answers summarised into a final answer, gains on global questions around 1M tokens, judging details not in the abstract | confirmed (abstract opened) |
| GraphRAG docs: TextUnits, entity/relationship/claim extraction, Leiden clustering, community summaries; Global, Local, DRIFT and Basic search | confirmed (docs page opened; cost not discussed there) |
| HyDE abstract (arXiv 2212.10496): hypothetical document from an instruction-following LM, embedded by an unsupervised contrastive encoder; beats Contriever and is comparable to fine-tuned retrievers | confirmed (abstract opened) |
| ColBERT abstract (arXiv 2004.12832): late interaction, precomputed document representations, two orders of magnitude faster and four orders fewer FLOPs vs BERT rankers, competitive effectiveness | confirmed (abstract opened) |
| Self-RAG abstract (arXiv 2310.11511): reflection tokens, on-demand retrieval, critique, wins over ChatGPT and retrieval-augmented Llama2-chat (authors' claims) | confirmed (abstract opened) |
| RAPTOR abstract (arXiv 2401.18059): recursive embed-cluster-summarise tree, retrieval across levels, 20% absolute QuALITY gain with GPT-4 (authors' claim) | confirmed (abstract opened) |
| Anthropic Contextual Retrieval: 50-100 token chunk context, contextual embeddings plus contextual BM25, 35% / 49% / 67% failure-rate reductions (1 - recall@20, one embedding model, vendor-reported), under about 200,000 tokens skip RAG | confirmed (blog opened); stated as reported |
| CRAG abstract (arXiv 2401.15884): lightweight retrieval evaluator with a confidence score choosing actions, web search extension, decompose-then-recompose, plug-and-play, no numbers | confirmed (abstract opened after drafting; Q33 updated). T5-large and the three action names remain glossary-snippet level |
| SPLADE abstract (arXiv 2107.05720): explicit sparsity regularisation and log-saturation on term weights, competitive with dense and sparse methods, no numbers | confirmed (abstract opened after drafting; Q16 updated). Expansion mechanism and index serving remain from memory |
| RRF formula and k = 60 (Cormack, Clarke, Buettcher, SIGIR 2009) | confirmed via search in Part 6 review (secondary descriptions) |

## Not verified (written from memory or reported, hedged in the text)
BM25 defaults (k1 about 1.2-2.0, b = 0.75) and the Lucene-style IDF form; SPLADE expansion mechanism; doc2query-style question generation; step-back prompting origin; IRCoT-style interleaving; RAPTOR collapsed-tree vs top-down retrieval and clustering method; ColBERTv2 residual compression and the 2-bit plus 4-byte layout in Q50 (labelled ASSUMED); LITE's 0.25x storage ratio (paper snippet, not opened); CLIP-style joint embeddings and ColPali-style page-image retrieval (Q41); LLM-judge position, length and self-preference biases (reported, no sizes claimed); the "5-10x LLM calls" agentic claim (blog, illustrative); the "50+ labelled queries" alpha-tuning rule of thumb (a guide cited in the notes); provider caching multipliers and batch discounts in Q26 (ASSUMED; check provider docs); the 'Are LLM-based retrievers worth their cost?' paper (title only, no findings used).

## Evidence limits (unchanged)
- No candidate-reported advanced-RAG questions were found for any company; evidence is authors' abstracts, one vendor blog and practitioner blogs. No source states a salary band. Stars and "Asked at" tags are indicative.
- All hardware, latency, cost and price numbers are assumed or synthetic and labelled; demos use toy embeddings and mock LLMs, so none measures real semantic retrieval quality and no toy result is a claim about real systems.
- Product names and techniques change quickly; answers hedge product claims and say to check current docs.

## Unresolved
- Agents, planning and MCP belong to Part 8; evaluation depth (RAGAS, LLM-as-judge) to Part 9; serving to Part 10; injection, monitoring and LLMOps to Part 11 (pointers only here).
