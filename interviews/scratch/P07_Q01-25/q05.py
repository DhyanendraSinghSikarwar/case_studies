import numpy as np
def dcg(rel, k):
    rel = np.asarray(rel, float)[:k]
    return ((2**rel - 1) / np.log2(np.arange(2, rel.size + 2))).sum()
def ndcg(rel, k, ideal=None):
    ideal = rel if ideal is None else ideal
    idcg = dcg(np.sort(ideal)[::-1], k)
    return 0.0 if idcg == 0 else dcg(rel, k) / idcg
rel = [3, 2, 3, 0, 1, 2]
print("DCG@6", round(dcg(rel, 6), 4))
print("IDCG@6", round(dcg(sorted(rel, reverse=True), 6), 4))
print("NDCG@6", round(ndcg(rel, 6), 4))
print("NDCG@3", round(ndcg(rel, 3), 4))
print("all zero ->", ndcg([0,0,0], 3))
# binary metrics
b = np.array([1,0,1,0,0,1]); tot = 4
k=5
print("P@5", b[:k].mean(), "R@5", b[:k].sum()/tot)
print("MRR rr", 1/(np.argmax(b)+1))
prec = np.cumsum(b)/np.arange(1,b.size+1)
print("AP", round((prec*b).sum()/tot, 4))
