# Reciprocal rank fusion from scratch, with tests and the effect of k. No libraries needed.
def rrf(rankings, k=60, weights=None):
    """rankings: list of ranked lists of doc ids (best first). rank starts at 1.
    Returns [(doc, score)] best first. Ties broken by doc id for determinism."""
    weights = weights or [1.0] * len(rankings)
    score = {}
    for w, lst in zip(weights, rankings):
        seen = set()
        for rank, d in enumerate(lst, start=1):      # start=1: the off-by-one trap is using 0
            if d in seen: continue                    # a duplicate inside one list must not count twice
            seen.add(d)
            score[d] = score.get(d, 0.0) + w / (k + rank)
    return sorted(score.items(), key=lambda x: (-x[1], x[0]))

# test 1: hand-computed. 'a' is rank 1 in list A and rank 3 in list B, k=60
res = dict(rrf([["a", "b", "c"], ["x", "y", "a"]]))
assert abs(res["a"] - (1/61 + 1/63)) < 1e-12
# test 2: off-by-one trap. With 0-based ranks the top doc would get 1/60, not 1/61
assert abs(dict(rrf([["a"]]))["a"] - 1/61) < 1e-12
# test 3: scale robustness: only the order matters, so rescaling scores cannot change the result
s_bm25 = {"a": 12.0, "b": 9.0, "c": 3.0}; s_dense = {"a": 0.2, "b": 0.8, "c": 0.5}
order = lambda s: sorted(s, key=lambda d: -s[d])
scaled = {d: v * 1000 for d, v in s_bm25.items()}
assert rrf([order(s_bm25), order(s_dense)]) == rrf([order(scaled), order(s_dense)])
# test 4: a doc in both lists beats docs that top only one list (k=60)
top = rrf([["p", "q", "z"], ["r", "z", "s"]])[0][0]
assert top == "z", top
# test 5: duplicate in one list counted once
assert rrf([["a", "a", "b"]])[0][0] == "a" and abs(dict(rrf([["a", "a"]]))["a"] - 1/61) < 1e-12
print("all tests passed")

# effect of k: A says u is #1 and v is #5; B says v is #1 and u is #5; w is #2 in both
A = ["u", "w", "m", "n", "v"]; B = ["v", "w", "o", "p", "u"]
for k in (1, 10, 60, 1000):
    out = rrf([A, B], k=k)
    print(f"k={k:<5}", [(d, round(s, 5)) for d, s in out[:3]])
# weakness: scores ignore confidence. Same fused order whether ranker A was sure or barely separated
print("weighted (A trusted 3x), k=60:", [d for d, _ in rrf([A, B], weights=[3, 1])[:3]])
