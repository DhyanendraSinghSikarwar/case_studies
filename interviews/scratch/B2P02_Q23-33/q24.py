import math
# P(next | prev). Greedy takes A (0.6) then is stuck with weak continuations; B path is better overall.
T = {"<s>": {"A": 0.6, "B": 0.4},
     "A": {"x": 0.4, "y": 0.3, "<eos>": 0.3},
     "B": {"<eos>": 0.9, "x": 0.1},
     "x": {"<eos>": 1.0}, "y": {"<eos>": 1.0}}
# make A's continuations flat so A-path total is low
T["A"] = {"x": 0.35, "y": 0.35, "<eos>": 0.30}
def greedy():
    seq, lp, cur = [], 0.0, "<s>"
    while cur != "<eos>":
        nxt, p = max(T[cur].items(), key=lambda kv: kv[1])
        seq.append(nxt); lp += math.log(p); cur = nxt
    return seq, lp
def beam(k, alpha=0.0):
    beams, done = [(["<s>"], 0.0)], []
    while beams:
        cand = []
        for s, lp in beams:
            for n, p in T[s[-1]].items():
                cand.append((s + [n], lp + math.log(p)))
        cand.sort(key=lambda c: c[1], reverse=True)
        beams = []
        for s, lp in cand[:k]:
            (done if s[-1] == "<eos>" else beams).append((s, lp))
    score = lambda c: c[1] / (len(c[0]) - 1) ** alpha
    return max(done, key=score)
g = greedy(); print("greedy", g[0], round(math.exp(g[1]), 3))
for k in (1, 2):
    b = beam(k); print("beam", k, b[0][1:], round(math.exp(b[1]), 3))
