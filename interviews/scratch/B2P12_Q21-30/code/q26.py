# Q26 toy LLM re-ranking. SYNTHETIC users/items; the "LLM" is a mock scorer = true utility + less noise than the candidate model.
import numpy as np
rng = np.random.default_rng(0)
U, N, K_TOP = 400, 200, 10
util = rng.normal(0, 1, (U, N))                         # true utility (hidden)
cand_score = util + rng.normal(0, 1.2, (U, N))          # classic candidate model: noisy
llm_score = util + rng.normal(0, 0.6, (U, N))           # mock LLM: less noisy but costly
def ndcg(order, u):                                     # gain = relevant if utility in top 10% of that user's items
    rel = (util[u] >= np.quantile(util[u], 0.9)).astype(float)
    g = rel[order[:K_TOP]] / np.log2(np.arange(2, K_TOP + 2)); ideal = np.sort(rel)[::-1][:K_TOP] / np.log2(np.arange(2, K_TOP + 2))
    return g.sum() / ideal.sum()
def rerank(u, k):                                       # LLM sees only top-k candidates; the rest keep candidate order
    order = np.argsort(-cand_score[u]); head = order[:k]
    head = head[np.argsort(-llm_score[u, head])]
    return np.concatenate([head, order[k:]])
print("COST MODEL (ASSUMED): 1 LLM unit per 10 candidates scored; latency grows with k")
for k in (0, 10, 20, 50, 100):
    n = np.mean([ndcg(rerank(u, k) if k else np.argsort(-cand_score[u]), u) for u in range(U)])
    print(f"k={k:3d}  NDCG@10={n:.3f}  LLM cost units/request={k / 10:.1f}")
# selective use: only for the 30% of users flagged 'high value' (ASSUMED rule), k=50
hv = rng.random(U) < 0.3
n_sel = np.mean([ndcg(rerank(u, 50) if hv[u] else np.argsort(-cand_score[u]), u) for u in range(U)])
print(f"LLM only for 30% of users (k=50): NDCG@10={n_sel:.3f}, cost units/request={0.3 * 5:.1f} average")
# offline evaluation from logged clicks: logging policy = candidate ranker, clicks have position bias 1/rank
def logs(policy_orders, n_sess=40):
    L = []
    for _ in range(n_sess):
        for u in range(U):
            o = policy_orders[u]
            for pos in range(K_TOP):
                it = o[pos]; rel = util[u, it] >= np.quantile(util[u], 0.9)
                if rng.random() < (1 / (pos + 1)) * (0.9 if rel else 0.1): L.append((u, it, pos))
    return L
old = [np.argsort(-cand_score[u]) for u in range(U)]
log = logs(old)
new = [rerank(u, 50) for u in range(U)]
def true_ctr(orders):  # ground truth expected clicks under the same click model
    return np.mean([sum((1 / (p + 1)) * (0.9 if util[u, o[p]] >= np.quantile(util[u], 0.9) else 0.1) for p in range(K_TOP)) for u, o in enumerate(orders)])
def naive(orders):     # count logged clicks on items that the new policy also puts in its top 10
    top = [set(o[:K_TOP]) for o in orders]; return sum(1 for u, it, _ in log if it in top[u]) / (U * 40)
def ips(orders):
    tot = 0.0
    pos_new = [{it: p for p, it in enumerate(o[:K_TOP])} for o in orders]
    for u, it, p_old in log:
        if it in pos_new[u]: tot += (1 / (pos_new[u][it] + 1)) / (1 / (p_old + 1))
    return tot / (U * 40)
print("expected clicks per session, old ranker (truth):", round(true_ctr(old), 3), "| new ranker (truth):", round(true_ctr(new), 3))
print("replay of logs, naive click count on new top-10:", round(naive(new), 3), "(compare to logged old CTR", round(len(log) / (U * 40), 3), ")")
print("replay with inverse-propensity weights:", round(ips(new), 3))
ov = np.mean([len(set(new[u][:K_TOP]) & set(old[u][:K_TOP])) / K_TOP for u in range(U)])
print("share of the new top-10 that the old ranker ever showed in its top-10:", round(ov, 2))
