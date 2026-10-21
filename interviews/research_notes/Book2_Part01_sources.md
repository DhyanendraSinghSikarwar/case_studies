# Book 2 Part 01 — Sources & research notes (Transformer internals)

Date: 2026-10-21. WebSearch worked (US-only, standard mode), 3 searches. WebFetch was blocked in this environment (DNS failure for www.techinterview.org), so no page was opened. Everything below comes from search-result snippets only.

## Honest caveat
Results were mostly prep-site question banks, not first-hand 2025-26 interview reports. Stars are a blend of topic presence across banks and expert judgement. "Asked at" tags are company types, except where a report names the company.

## Sources seen (snippets only, not opened)
| Source | URL | Used for |
|---|---|---|
| techinterview.org: What LLM interviewers ask about transformers | https://www.techinterview.org/post/3233476821/what-llm-interviewers-ask-about-transformers/ | attention, KV cache, GQA/MQA, prefill vs decode, memory growth |
| prachub: Transformer attention, Q/K/V and KV cache | https://prachub.com/interview-questions/transformer-attention-computing-q-k-and-v-and-how-a-kv-cache-speeds-up-decoding | Q/K/V computation, KV cache speed-up |
| Educative: Flash attention | https://www.educative.io/courses/ai-engineer-interview-prep/flash-attention | FlashAttention: same output, less memory |
| DataCamp LLM interview questions | https://www.datacamp.com/blog/llm-interview-questions | RoPE, GQA, general LLM architecture |
| Devinterview llms-interview-questions (GitHub) | https://github.com/Devinterview-io/llms-interview-questions | question list only (its sample attention code has errors; not reused) |
| Glassdoor Capgemini review (May 2024, one candidate) | https://www.glassdoor.co.uk/Interview/Capgemini-Interview-E3803-RVW99746333.htm | transformer vs RNN/LSTM, self-attention (the same review is mirrored on many country domains; counted once) |
| Dataford LTIMindtree / Hexaware GenAI guides | https://dataford.io/interview-guides/ltimindtree/genai-engineer , https://dataford.io/interview-guides/hexaware/genai-engineer | transformer vs RNN, skip connections (prep guides, not candidate reports) |
| Netflix MLE screen (single candidate report, seen via search snippet) | not opened | MQA/GQA cache shrinkage, decode memory-bound, long-context cache not fitting in GPU memory |

## Question provenance
| Questions | Provenance |
|---|---|
| Q1, Q2, Q3, Q4, Q6, Q7, Q10, Q11, Q8, Q14 | found in sources (multiple banks) |
| Q5, Q9, Q12, Q13, Q15, Q16-Q22 | partly found, partly expert gap-check |
| Q23-Q47 | expert gap-check, reflecting 2025-26 topics (MLA, MoE, prefix caching, long-context, diffusion LMs, multi-token prediction) |

## AI-era notes
- Loops now test inference-cost maths (KV-cache memory, tokens/sec) alongside concepts.
- Attention-code reading/debugging of LLM-written snippets is a plausible round (Q41).

## Not found / blocked
No first-hand reports for Flipkart, Swiggy, PhonePe, Spotify, Zalando, Booking, Klarna. AmbitionBox and Medium returned nothing relevant.
