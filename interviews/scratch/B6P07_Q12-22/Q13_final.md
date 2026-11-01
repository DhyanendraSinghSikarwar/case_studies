### Q13 ⭐⭐⭐ 🟡 Each query could stuff a 100,000-token document set into the prompt or retrieve 6,000 tokens, at an illustrative 3 per million input tokens and 20,000 queries a day. Compute the daily input cost of each approach, and say what accuracy and latency evidence you would want before choosing.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to long-context versus RAG topics in GenAI guides; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Stuffing costs 6,000 a day against 360 for retrieval, a gap of 5,640 a day, so I would only stuff if tests show retrieval loses enough accuracy to be worth that gap.

**Clarifying questions:**
- Is the 100,000-token set the same on every query? Why it matters: an identical prefix can be cached at a lower rate, which changes the comparison.
- What is the model's context window and its price for long inputs? Why it matters: some limits and prices change with length.
- Are the answers found in one passage or spread across many documents? Why it matters: spread-out questions favour stuffing; single-passage questions favour retrieval.
- What is the latency target? Why it matters: long prompts take longer to process before the first token.
- How often does the document set change? Why it matters: stuffing needs no index, but caching breaks on every change.

**Approach:**
1. Compute the input cost. Stuffing: 100,000 x 20,000 = 2 billion tokens a day, at 3 per million = 6,000. Retrieval: 6,000 x 20,000 = 120 million tokens, = 360. Ratio about 16.7x.
2. Add what the prompt left out: output tokens (same in both), and the retrieval pipeline (embeddings, vector store, reranker). The saving is 5,640 a day (about 2.06 million a year, illustrative), so the pipeline must cost more than that to lose.
3. Check the cached case. If the 100k set is identical every call and cached reads cost 10% of the input rate (invented), stuffing costs 600 a day. That is still above retrieval's 360.
4. Build a labelled question set from real traffic, including multi-document questions.
5. Run both approaches, plus retrieval with a bigger top-k, on the same questions. Measure correctness, citation accuracy, and refusals.
6. Measure latency end to end: p50 and p95 time to first token and total time. Stuffing pays a long prefill; retrieval pays a retrieval hop.
7. Choose by the cheapest approach that meets the accuracy bar. Consider a hybrid: retrieve a larger slice (say 20,000 tokens) for hard questions only.

**Metrics:**
- Daily input cost = input tokens per query x queries per day x price per token.
- Accuracy = correct answers / graded questions, with an interval and a slice for multi-document questions.
- Retrieval recall@k = questions whose needed passage is in the top k / all questions.
- Latency p95 of time to first token and of total response time.
- Guardrails: citation correctness, refusal rate, cost per correct answer.

**Risks:**
- Long-context accuracy may drop for facts buried in the middle (Book 2 Part 01 Q19 covers the "lost in the middle" heading: "What is the context window, and why is the effective context often shorter than the advertised one").
- Retrieval may miss the passage and answer confidently anyway.
- Costing only input and forgetting the retrieval infrastructure.
- Evaluating on easy questions only.

**What the interviewer scores:**
- Strong: correct arithmetic, names cached stuffing as the fair comparison, asks for accuracy and latency evidence.
- Strong: cost per correct answer, not cost alone.
- Weak: "long context is always better" or "RAG is always cheaper so use it" with no test.
- Weak: ignoring latency.

**Example:** Illustrative. Retrieval answers 82% correctly at 360 a day; stuffing answers 86% at 6,000 a day. Weak: "Stuffing is more accurate, use it." Strong: "Four points of accuracy cost 5,640 a day, which is about 1,410 per accuracy point per day. I would first try retrieving 20,000 tokens or a reranker to close the gap, and stuff only the questions retrieval cannot answer."

**Code:**
```python
queries = 20_000
price = 3.0                                        # illustrative, per million input tokens
stuff, rag = 100_000, 6_000
cost = lambda tok: tok * queries * price / 1e6
c_stuff, c_rag = cost(stuff), cost(rag)
print(f"stuffing: {stuff*queries/1e9:.1f} billion tokens/day -> {c_stuff:,.0f} per day")
print(f"retrieval: {rag*queries/1e6:.0f} million tokens/day -> {c_rag:,.0f} per day")
assert c_stuff == 6000 and c_rag == 360
print(f"ratio {c_stuff/c_rag:.1f}x, gap {c_stuff-c_rag:,.0f} per day = {(c_stuff-c_rag)*365:,.0f} per year")
assert round(c_stuff / c_rag, 1) == 16.7 and (c_stuff - c_rag) * 365 == 2_058_600
# If the 100k set is identical every call and cached reads cost 10% of the input rate (invented).
c_cached = cost(stuff) * 0.10
print(f"stuffing with 100% cached prefix at 10% rate: {c_cached:,.0f} per day (still above retrieval {c_rag:,.0f})")
assert c_cached == 600 and c_cached > c_rag
# Break-even: what retrieval pipeline overhead per day would erase the saving?
print(f"retrieval overhead (embedding, vector DB, reranker) would need to exceed {c_stuff-c_rag:,.0f} per day to lose")
```

**Output (my run):**
```
stuffing: 2.0 billion tokens/day -> 6,000 per day
retrieval: 120 million tokens/day -> 360 per day
ratio 16.7x, gap 5,640 per day = 2,058,600 per year
stuffing with 100% cached prefix at 10% rate: 600 per day (still above retrieval 360)
retrieval overhead (embedding, vector DB, reranker) would need to exceed 5,640 per day to lose
```

**Follow-ups:**
- Does caching make stuffing win? Not here. At the invented 10% rate it is 600 against 360, and the cache needs an identical prefix and recent traffic. See Book 2 Part 01 Q24 ("What are prompt/prefix caching in LLM APIs, and how do they relate to the KV cache? How do you structure prompts to benefit?").
- What if answers need many documents? Use a larger retrieval budget, multi-step retrieval, or stuff for that class only.
- What about the price for very long inputs? Check the provider's current price sheet; I do not assume it is linear.

**Common mistakes:**
- Comparing cost without accuracy.
- Forgetting output tokens and pipeline costs.
- Using average questions and missing the hard multi-document ones.
- Quoting vendor limits from memory.

