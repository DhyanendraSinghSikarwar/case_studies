# Measure three judge biases in a MOCK judge with PLANTED (assumed) bias parameters,
# then check that the probes recover them and that swap-and-agree removes position bias.
import random
random.seed(11)
POS_BONUS, LEN_BONUS_PER_100, SELF_BONUS = 0.25, 0.30, 0.40   # planted, ASSUMED

def judge(a, b, judge_model="J"):
    """a, b = dict(q=quality, words=int, gen=model name). Returns 'first' or 'second'."""
    def score(x, first):
        s = x["q"] + random.gauss(0, 0.5)
        s += LEN_BONUS_PER_100 * x["words"] / 100
        s += SELF_BONUS * (x["gen"] == judge_model)
        return s + (POS_BONUS if first else 0)
    return "first" if score(a, True) > score(b, False) else "second"

N = 20000
def pair(): q = random.uniform(2, 4); return q, q      # equal quality pairs: any preference is bias

# 1) position probe: same two answers, both orders. Equal quality, equal length.
first = sum(judge({"q": q, "words": 100, "gen": "X"}, {"q": q, "words": 100, "gen": "Y"}) == "first"
            for q, _ in (pair() for _ in range(N)))
print(f"position: picks first slot {first/N:.2f} (0.50 = no bias)")

# 2) verbosity probe: equal quality, one answer padded (+150 words); randomise slots
pad_wins = 0
for _ in range(N):
    q, _ = pair(); long_first = random.random() < 0.5
    L, S = {"q": q, "words": 250, "gen": "X"}, {"q": q, "words": 100, "gen": "Y"}
    r = judge(L, S) if long_first else judge(S, L)
    pad_wins += (r == "first") == long_first
print(f"verbosity: padded answer wins {pad_wins/N:.2f}")

# 3) self-preference probe: equal quality, judge J's own output vs another model's; randomise slots
self_wins = 0
for _ in range(N):
    q, _ = pair(); own_first = random.random() < 0.5
    O, T = {"q": q, "words": 100, "gen": "J"}, {"q": q, "words": 100, "gen": "Y"}
    r = judge(O, T) if own_first else judge(T, O)
    self_wins += (r == "first") == own_first
print(f"self-preference: own output wins {self_wins/N:.2f}")

# mitigation: judge both orders, keep the verdict only if it agrees; else call it a tie
def swap_judge(x, y):
    r1 = judge(x, y); r2 = judge(y, x)
    if r1 == "first" and r2 == "second": return "x"
    if r1 == "second" and r2 == "first": return "y"
    return "tie"
res = {"x": 0, "y": 0, "tie": 0}
for _ in range(N):
    q, _ = pair(); res[swap_judge({"q": q, "words": 100, "gen": "X"}, {"q": q, "words": 100, "gen": "Y"})] += 1
print("swap-and-agree on equal pairs:", {k: round(v / N, 2) for k, v in res.items()})
