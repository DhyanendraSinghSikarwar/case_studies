# Standalone, standard library only. EVERY input is an ASSUMPTION for a capacity sketch, not a measurement or a benchmark.
docs, chunks_per_doc, tok_per_chunk, dim = 5_000_000, 12, 400, 768
churn_per_day, peak_qps, avg_qps = 0.02, 60, 15
topk_retrieve, topk_rerank, prompt_ctx_tok, out_tok = 50, 6, 3000, 350
n = docs * chunks_per_doc
print(f"chunks: {n/1e6:.0f}M ; corpus tokens: {n*tok_per_chunk/1e9:.1f}B")
raw = n * dim * 4; print(f"raw fp32 vectors: {raw/1e9:.0f} GB ; with HNSW links (ASSUMED M=16 -> ~32 links x 4 B): {(raw + n*32*4)/1e9:.0f} GB ; fp16 vectors: {n*dim*2/1e9:.0f} GB")
print(f"IVF-PQ at 96 B/vector: {n*96/1e9:.1f} GB codes + {n*8/1e9:.1f} GB ids")
new_chunks = docs * churn_per_day * chunks_per_doc
print(f"daily churn: {docs*churn_per_day:,.0f} docs -> {new_chunks/1e6:.1f}M chunks to re-embed/day = {new_chunks*tok_per_chunk/1e9:.2f}B tokens/day, {new_chunks/86400:.0f} chunks/s average")
q_day = avg_qps * 86400 * 0.4                                  # ASSUMED: traffic is busy 40% of the day at avg_qps
print(f"queries/day ~{q_day/1e6:.2f}M ; LLM prompt tokens/day ~{q_day*prompt_ctx_tok/1e9:.1f}B, output ~{q_day*out_tok/1e9:.2f}B")
budget = {"auth+ACL lookup": 20, "query embed": 30, f"search top-{topk_retrieve} (filtered)": 60, f"rerank to {topk_rerank}": 120, "LLM time-to-first-token": 700}
print("ASSUMED latency budget to first token (ms):", budget, "-> total", sum(budget.values()), "ms")
cache_hit = 0.20
print(f"if a semantic/answer cache (keyed by ACL scope) hit {cache_hit:.0%} (ASSUMED), LLM prompt tokens/day drop to ~{q_day*(1-cache_hit)*prompt_ctx_tok/1e9:.1f}B")
print(f"rerank load at peak: {peak_qps*topk_retrieve:,} passages/s scored by the reranker")
