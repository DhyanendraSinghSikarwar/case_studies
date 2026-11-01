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

---

## Addendum (Wave B prep, 2026-10-21): pages actually OPENED with WebFetch
WebFetch worked in this later session (the original note's "blocked" remark applied to the earlier session). Target band is the plan's Rs 30-80 LPA, not a higher cut-off. No page states a salary band, so band is NOT verified for any report.

| Page | URL | Opened? | Evidence type | What it confirmed |
|---|---|---|---|---|
| Amazon MLE onsite: "Implement MHA with a KV cache and cached GQA" (prachub, posted Jan 3 2026) | https://prachub.com/interview-questions/implement-multi-head-attention-with-a-kv-cache-and-cached-grouped-query-attention | yes | single candidate report (aggregator, level not stated) | 3-part coding task: causal MHA, then KV cache (prefill+decode, cached == uncached check), then GQA; follow-ups: ragged batches, cache before/after RoPE, sliding window, why GQA helps decode more than prefill. Supports Q13, Q35, Q10, Q23, Q29, Q42 |
| techinterview.org: What LLM interviewers ask about transformers | https://www.techinterview.org/post/3233476821/what-llm-interviewers-ask-about-transformers/ | yes | prep guide, no companies named | sqrt(d_k) follow-up, MHA, causal mask, O(n^2), RoPE, encoder/decoder variants, KV cache memory estimate, prefill vs decode, GQA/MQA, int8 KV cache. Supports Q1, Q3-Q11, Q15, Q17, Q23 |
| DataCamp LLM interview questions | https://www.datacamp.com/blog/llm-interview-questions | yes | prep guide | transformer, RoPE, attention, long dependencies, sparse attention, Mamba vs transformer (no KV cache question). Supports Q8, Q18, Q27, Q29 |
| datainterview.org: Top 32 LLMs and Transformers questions | https://www.datainterview.com/blog/llms-and-transformers-interview-questions | yes | prep guide ("not proprietary questions from any company"); claims NVIDIA/DeepMind go deep on architecture without attributing questions | sqrt(d_k), MHA/MQA/GQA, FlashAttention tiling, KV cache + MLA, prompt caching, sinusoidal vs RoPE vs ALiBi, MoE routing/collapse, lost-in-the-middle. Supports Q10, Q11, Q19, Q24, Q33, Q34, Q38 |
| ombharatiya Mistral page (GitHub) | https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/14-company-interview-questions/mistral.md | yes | self-described "synthesised", not candidate-reported | only shows KV-cache/GQA/sliding-window/MoE are plausible for LLM-lab loops |
| Glassdoor NVIDIA reviews (search snippets only) | e.g. https://www.glassdoor.co.in/Interview/NVIDIA-Interview-E7633-RVW94057186.htm | NO (403 on open) | candidate reports, snippet only | two Santa Clara reports ask to implement multi-head self-attention; one hiring-manager round covers recent transformer architectures |
| Netflix MLE screen (prachub snippet) | n/a | NO | single report, snippet | Q/K/V computation and KV cache asked in a screen |

## Blocked / thin (honest)
- Medium "100+ real interviews" article: 403. Glassdoor NVIDIA page: 403. letsdatascience: 429. No Blind or LeetCode Discuss post found.
- Still no first-hand Indian-company (Flipkart, Swiggy, PhonePe etc.) report for transformer internals.

## Revised provenance (replaces the table above where different)
| Tag | Questions |
|---|---|
| candidate-reported (single reports, aggregator/Glassdoor) | Q1, Q3, Q6, Q10, Q13, Q35 (Amazon onsite, Netflix screen, NVIDIA Glassdoor, Capgemini Glassdoor) |
| prep-guide (opened, multiple guides) | Q2, Q4, Q5, Q7, Q8, Q9, Q11, Q15, Q17, Q18, Q19, Q23, Q24, Q27, Q29, Q33, Q34, Q38 |
| expert gap-check (no source found; plan/topic coverage) | Q12, Q14, Q16, Q20-Q22, Q25, Q26, Q28, Q30-Q32, Q36, Q37, Q39-Q47 |
