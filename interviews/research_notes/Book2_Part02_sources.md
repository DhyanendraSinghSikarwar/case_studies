# Book 2 Part 02 — Sources & research notes (Tokenization, pretraining, scaling laws, decoding)

Date: 2026-10-21. Target band per plan.md: Rs 30-80 LPA roles. No source states a salary band, so band fit is NOT verified for any report. WebSearch ran 11 queries (standard mode, US-only); WebFetch opened 6 pages (some sites return 403/429). Stars blend topic frequency across prep banks with judgement; "Asked at" tags are company types unless a report names the company.

## Pages actually OPENED (WebFetch)
| Page | URL | Evidence type | Used for |
|---|---|---|---|
| techinterview.org: NLP interview questions, tokenization, embeddings, BERT | https://www.techinterview.org/post/3233460092/nlp-interview-questions-tokenization-embeddings-and-bert/ | prep guide, no company tied to a question | subword vs word/char, BPE/WordPiece/Unigram, multilingual, number fragmentation, the page (as relayed by the fetch summary) says 1,000 words ~ 750 tokens (~1,200 for code); NOTE this is the ratio backwards, the usual rule of thumb is ~0.75 words per token, i.e. 1,000 words ~ 1,300 tokens, and Q5 uses that corrected ratio, OOV in production. Q1, Q5, Q6, Q17 |
| pyshine: LLM sampling and decoding strategies | https://pyshine.com/LLM-Sampling-Decoding-Strategies-Temperature-TopK-TopP/ | prep blog | temperature, top-k, top-p, min-p, greedy, beam (cost x beam width, no sampling), repetition/frequency/presence penalties, sampler order, determinism caveats. Q2, Q4, Q19, Q20, Q21, Q24 |
| InterviewBit: LLM interview questions | https://www.interviewbit.com/llm-interview-questions-answers/ | prep bank, no levels or companies | tokenization (BPE/WordPiece/SentencePiece), pretraining vs fine-tuning, perplexity, temperature/top-k/top-p, context window. Q1, Q3, Q4, Q7, Q8 |
| Analytics Vidhya: Chinchilla scaling law | https://www.analyticsvidhya.com/blog/2024/09/chinchilla-scaling-law/ | explainer | 400+ models, 70B/1.4T tokens vs Gopher 280B, ~20 tokens/param, MMLU 67.5 vs 60, critiques (tight confidence intervals). Page does NOT state C ~ 6ND. Q10, Q11, Q32 |
| ZeroEntropy: perplexity | https://www.zeroentropy.dev/concepts/perplexity/ | explainer | perplexity = exp(avg per-token cross-entropy), not comparable across tokenizers, bits-per-byte, limitations. Q7 |
| (earlier session) techinterview.org: what LLM interviewers ask about transformers | https://www.techinterview.org/post/3233476821/what-llm-interviewers-ask-about-transformers/ | prep guide | "strawberry" letter counting, byte-level BPE/SentencePiece, token cost reduction, sampling knobs, temperature 0 = greedy. Q4-Q6 |

## Seen via search results only (NOT opened)
| Item | URL | Evidence type | Used for |
|---|---|---|---|
| PracHub: Implement a BPE tokenizer: threshold training, encode, decode | https://prachub.com/interview-questions/implement-a-byte-pair-encoding-tokenizer-threshold-training-encode-and-decode | candidate report (Glean, Software Engineer, onsite) per search snippet | Q12: train/encode/decode, threshold, lexicographic tie-break, example "abababa" with threshold 2 |
| PracHub: Implement a BPE tokenizer (technical screen version) | https://prachub.com/interview-questions/implement-a-byte-pair-encoding-bpe-tokenizer | candidate report (technical screen), snippet | Q12: non-overlapping left-to-right pair counting |
| Codemia: Implement a ByteTokenizer | https://codemia.io/practice/implement-a-bytetokenizer | listing described as a Perplexity online assessment, snippet | Q12, Q15: UTF-8 byte-level tokenization with BPE-style merges |
| Glitch Tokens in LLMs (arXiv 2404.09894); incomplete tokens in byte-level BPE (arXiv 2410.23684) | https://arxiv.org/pdf/2404.09894 , https://arxiv.org/html/2410.23684v1 | research papers, not interview reports | Q18 |
| D4 (arXiv 2308.12284), Oasis (arXiv 2311.12537), SoftDedup (ACL 2024) | https://arxiv.org/pdf/2308.12284 | research | Q9, Q25 (dedup is O(n^2) exactly, LSH approximates; selection beyond dedup helped ~20% at 6.7B) |
| Chinchilla replication attempt (arXiv 2404.10102) | https://arxiv.org/html/2404.10102v2 | research | Q32, Q41 (refit puts optimal ratio in the teens, not exactly 20; contested) |
| Schaeffer et al., "Are emergent abilities a mirage?" (arXiv 2304.15004) | https://ar5iv.org/html/2304.15004 | research | Q40 |
| Community training-recipe pages (tessl.io, mlx.void.app etc.) | e.g. https://tessl.io/registry/skills/github/OpenRaiser/NanoResearch/ml-training-recipes | community notes, low authority | Q26, Q27 (warmup 1-10%, cosine or WSD, AdamW betas, clip at 1.0, bf16 no scaler). Treat as practice notes, not primary |
| Estimating contamination via perplexity (arXiv 2309.10677) | https://arxiv.org/pdf/2309.10677 | research | Q30; a later study reportedly found perplexity methods near random for seen-vs-unseen, so claims need care |

## Question provenance
| Tag | Questions |
|---|---|
| candidate-reported (single reports, aggregator listings) | Q12 |
| prep-guide (opened, one or more guides) | Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q10, Q11, Q19, Q20, Q21, Q24 |
| research-paper / snippet level (topic confirmed, not an interview report) | Q9, Q15, Q18, Q25, Q26, Q27, Q30, Q32, Q40, Q41 |
| expert gap-check (no source found; plan topic coverage and judgement) | Q13, Q14, Q16, Q17, Q22, Q23, Q28, Q29, Q31, Q33-Q39, Q42-Q44 |

## AI-era notes
- Token cost and context budgeting now appear in product/GCC loops (Q5, Q17); decoding-parameter judgement is a common practical question (Q4, Q21, Q44).
- Coding rounds ask for tokenizer or sampler from scratch (Q12, Q13); reviewing LLM-written sampling code is a plausible round (Q35).
- Test-time compute and reasoning models make decoding-time sampling a cost topic (Q43).

## Not found / blocked (honest)
- No first-hand reports for Indian product companies (Flipkart, Swiggy, PhonePe), or for NVIDIA/Google/Meta, on tokenization, pretraining or scaling laws. Glassdoor and Blind were not reachable; no LeetCode Discuss post found.
- Search found nothing on: vocabulary-size trade-offs, critical batch size, pretraining quality-filtering specifics, logprobs and stop-sequence interview questions. Those questions are expert gap-check and their answers must rely on well-known facts and runnable demos, not claims about what interviewers ask.
- The Chinchilla page does not state C ~ 6ND; that relation (from Kaplan et al. and Hoffmann et al.) will be stated in the answer as a standard approximation and checked by arithmetic, not attributed to the page.
