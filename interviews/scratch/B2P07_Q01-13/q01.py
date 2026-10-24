# Failure-tagged recall@k on a small invented golden set: which failure class is hurting?
# Retrieval results are hard-coded stand-ins (mock logs), not outputs of a real system.
from collections import defaultdict
# (query tag, rank of the gold chunk in the retriever's list; None = not retrieved in top 20)
log = [
 ("exact_token", 14), ("exact_token", None), ("exact_token", 9), ("exact_token", 2),
 ("paraphrase", 1), ("paraphrase", 3), ("paraphrase", 2), ("paraphrase", 1),
 ("context_free_chunk", 17), ("context_free_chunk", None), ("context_free_chunk", 6),
 ("multi_hop", None), ("multi_hop", None), ("multi_hop", 12),
 ("conversational", None), ("conversational", 5), ("conversational", 11),
]
FIX = {"exact_token": "hybrid (BM25 + dense)", "paraphrase": "nothing needed",
       "context_free_chunk": "contextual chunks / rerank", "multi_hop": "decomposition or agent loop",
       "conversational": "query rewriting (Part 6 Q28)"}
by = defaultdict(list)
for tag, r in log: by[tag].append(r)
print(f"{'failure class':20s} n  recall@5 recall@20  fix to try")
for tag, rs in by.items():
    r5 = sum(r is not None and r <= 5 for r in rs) / len(rs)
    r20 = sum(r is not None and r <= 20 for r in rs) / len(rs)
    print(f"{tag:20s} {len(rs)}  {r5:7.2f} {r20:8.2f}   {FIX[tag]}")
