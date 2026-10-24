# Standalone, stdlib only. EVERY number below is an ASSUMPTION for a back-of-envelope comparison, not a benchmark or a real price.
import math
A = dict(corpus_tok=1_000_000, chunk_tok=600,
         prompt_overhead=800,            # instructions + few-shot per LLM call (assumed)
         extract_out=400, gleaning_passes=1,          # GraphRAG-style entity/relation extraction output per chunk; extra "did you miss any" pass(es)
         comm_frac=0.10,                 # communities ~10% of chunks (assumed); one summary call each
         comm_in=3000, comm_out=500,
         mr_sum_out=150, mr_group=10, mr_reduce_out=200,    # map-reduce: chunk summary, group size, reduce output
         q_global_comm=120, q_map_in=500+300, q_map_out=150, q_reduce_in=6000, q_reduce_out=600,   # per GLOBAL query: map over community summaries then reduce
         price_in=1.0, price_out=4.0,    # ASSUMED generic units per 1M tokens (not a real price list)
         ctx_window=1_000_000)           # ASSUMED long-context limit: CHECK current model limits, they change
n_chunks = math.ceil(A["corpus_tok"] / A["chunk_tok"])
def cost(tin, tout): return (tin * A["price_in"] + tout * A["price_out"]) / 1e6

# GraphRAG-style index: extraction on every chunk (+gleaning) + community summaries
calls_ex = n_chunks * (1 + A["gleaning_passes"])
tin_ex = calls_ex * (A["chunk_tok"] + A["prompt_overhead"]); tout_ex = calls_ex * A["extract_out"]
n_comm = math.ceil(n_chunks * A["comm_frac"]); tin_c = n_comm * A["comm_in"]; tout_c = n_comm * A["comm_out"]
g = dict(calls=calls_ex + n_comm, tin=tin_ex + tin_c, tout=tout_ex + tout_c)

# Map-reduce over chunk summaries: summarise each chunk, then reduce in groups until one summary remains
calls_m, tin_m, tout_m, n = n_chunks, n_chunks * (A["chunk_tok"] + A["prompt_overhead"]), n_chunks * A["mr_sum_out"], n_chunks
sz = A["mr_sum_out"]
while n > 1:
    groups = math.ceil(n / A["mr_group"]); calls_m += groups; tin_m += groups * (A["mr_group"] * sz + A["prompt_overhead"]); tout_m += groups * A["mr_reduce_out"]; n = groups; sz = A["mr_reduce_out"]
m = dict(calls=calls_m, tin=tin_m, tout=tout_m)

# Per global question
q_g = dict(calls=A["q_global_comm"] + 1, tin=A["q_global_comm"] * A["q_map_in"] + A["q_reduce_in"], tout=A["q_global_comm"] * A["q_map_out"] + A["q_reduce_out"])
q_m = dict(calls=1, tin=(n_chunks // A["mr_group"]) * A["mr_reduce_out"] + 500, tout=600)   # map-reduce: answer from the top-level summaries kept at index time (assumed ~170 summaries of 200 tok)
q_long = dict(calls=1, tin=A["corpus_tok"] + 500, tout=600)                                                       # long context: put the whole corpus in the prompt

print(f"chunks: {n_chunks}, communities: {n_comm}")
print(f"{'option':22s}{'index calls':>12s}{'index tok in':>14s}{'index tok out':>15s}{'index cost':>12s}{'query calls':>13s}{'query tok in':>14s}{'query cost':>12s}")
rows = [("GraphRAG-style", g, q_g), ("map-reduce summaries", m, q_m), ("long context (no index)", dict(calls=0, tin=0, tout=0), q_long)]
for name, i, q in rows:
    print(f"{name:22s}{i['calls']:>12,d}{i['tin']:>14,d}{i['tout']:>15,d}{cost(i['tin'], i['tout']):>12.2f}{q['calls']:>13,d}{q['tin']:>14,d}{cost(q['tin'], q['tout']):>12.4f}")
print("(costs in ASSUMED units: 1.0 per 1M input tokens, 4.0 per 1M output tokens)")
print("fits in assumed context window:", A["corpus_tok"] + 500 <= A["ctx_window"], "(zero headroom: real limits and answer quality at that length must be checked)")

def total(i, q, nq): return cost(i["tin"], i["tout"]) + nq * cost(q["tin"], q["tout"])
for nq in (10, 100, 1000, 10000):
    best = min(rows, key=lambda r: total(r[1], r[2], nq)); print(f"{nq:>6d} global queries -> cheapest: {best[0]:22s} totals:", {r[0][:9]: round(total(r[1], r[2], nq), 1) for r in rows})
for nq in range(1, 100000):
    if total(g, q_g, nq) < total(dict(calls=0, tin=0, tout=0), q_long, nq): print("GraphRAG-style beats long-context on cost after about", nq, "global queries (with these assumptions)"); break
chg = 0.05            # ASSUMED: 5% of chunks change per week
touched = 0.15        # ASSUMED: those edits touch 15% of communities (summaries must be redone)
r_g = cost(chg * tin_ex + touched * tin_c, chg * tout_ex + touched * tout_c)
r_m = cost(chg * n_chunks * (A["chunk_tok"] + A["prompt_overhead"]) + 0.10 * tin_m, chg * n_chunks * A["mr_sum_out"] + 0.10 * tout_m)   # changed chunks + ~10% of the reduce path (assumed)
print("weekly refresh (ASSUMED 5 percent of chunks change):  GraphRAG-style %.2f units | map-reduce %.2f units | long context 0 (no index)" % (r_g, r_m))
