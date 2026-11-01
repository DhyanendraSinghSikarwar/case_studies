**Say this first (1 line):** Vectors from two different embedding models live in two different geometries, so their similarity scores cannot be compared in one index; I would prove it by splitting the hit rate by old and new documents, then re-embed everything with one model (blue-green) and version the index.

**Clarifying questions:**
- Which model embeds the query today, the old one, the new one, or both? This decides which documents become unreachable.
- Do the two models have different dimensions or normalisation? A dimension mismatch would fail loudly; same dimension fails silently.
- How big is the corpus and what does a full re-embed cost and take? It decides between a full re-embed and a gradual migration.
- Is there a fixed query set with labelled relevant documents (the 82% to 71% measurement)? I need to slice it by which model embedded the answer document.
- Can the system keep two indexes side by side? That allows a safe cutover.

**Approach:**
1. Slice the hit-rate query set by the embedding version of the target document (old-embedded versus new-embedded). A mixed index shows old and new targets behaving differently.
2. Check query-side behaviour: which model embeds the query, and what are the top-1 cosine scores for old-document and new-document hits? Different score scales mean the merged ranking is biased.
3. Verify the mechanism offline: re-embed a sample of old documents with the new model and compare hit rate, or embed the same documents with both models and measure cross-model cosine (it will be near chance).
4. Fix: re-embed the whole corpus with the new model into a fresh index, build it in the background, compare hit rate on the fixed query set, then switch traffic; keep the old index for rollback.
5. Prevent: store the embedding model name and version on every vector and on the index; refuse inserts whose version differs from the index; make "model change" mean "new index"; add a retrieval hit-rate check to the deploy gate.

**Metrics:**
- Hit rate at k = queries whose labelled relevant document appears in the top k / all queries. Report by target embedding version.
- Mean reciprocal rank as a second view; mean top-1 cosine by index segment.
- Guardrails: query latency, index build cost, answer-quality score on the fixed set.

**Risks:**
- Normalising or rescaling scores per model can hide the problem without fixing it.
- Dual-querying both models and merging by raw cosine looks reasonable but ranks by score scale, not relevance.
- Partial re-embedding leaves a long tail of old vectors that are quietly unreachable.
- Re-embedding costs money and time; the fixed query set must be representative of real traffic.

**What the interviewer scores:**
- Strong: explains that embedding spaces are model-specific, so cross-model cosine is meaningless. Weak: "the new model is probably worse".
- Strong: verifies with a slice and a controlled re-embed. Weak: just reverts.
- Strong: version metadata plus blue-green index as the prevention. Weak: "tell the team to be careful".

**Example:** (illustrative toy, 2,000 documents, 400 queries, 15% of documents embedded by a new model, whose cosines sit higher because it has a large shared direction). The baseline with everything in the old model finds the target in the top 5 for 100% of queries (the toy is easy on purpose). In the mixed index: querying with the old model gives 0.91 overall but 0.00 for new-embedded targets; querying with the new model gives 0.10 overall and 0.00 for old-embedded targets; querying both and merging by raw cosine gives 0.33, because new-model cosines are larger (mean top-1 cosine 0.93 versus 0.78) and crowd out the old documents. Re-embedding everything with the new model returns 1.00. The prompt's 82% to 71% is a milder version of the same effect, probably because other signals (keyword search, a reranker) rescue part of the loss; I would not claim which. Weak: "retrieval got worse, add more documents." Strong: "Slice by embedding version, show old and new targets behave differently, rebuild one index."

**Code:**
