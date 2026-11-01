import math
T = {"<s>": {"A": 0.6, "B": 0.4},
     "A": {"x": 0.35, "y": 0.35, "<eos>": 0.30},
     "B": {"<eos>": 0.9, "x": 0.1},
     "x": {"<eos>": 1.0}, "y": {"<eos>": 1.0}}
def beam(k, alpha=0.0):
    beams, done = [(["<s>"], 0.0)], []
    while beams:
        cand = [(s + [n], lp + math.log(p))
                for s, lp in beams for n, p in T[s[-1]].items()]
        cand.sort(key=lambda c: c[1], reverse=True)
        beams = []
        for s, lp in cand[:k]:
            (done if s[-1] == "<eos>" else beams).append((s, lp))
    return max(done, key=lambda c: c[1] / (len(c[0]) - 1) ** alpha)
for k in (1, 2):
    s, lp = beam(k); print(k, s[1:], round(math.exp(lp), 3))
