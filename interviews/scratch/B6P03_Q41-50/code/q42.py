# Q42: recursive training on model output. Toy: a categorical "topic" distribution. Illustrative.
import numpy as np

N, SYN, REAL = 1_000_000, 600_000, 400_000
assert SYN + REAL == N and REAL / N == 0.40 and SYN / N == 0.60

K = 5_000                                   # topics, Zipf-like true distribution
ranks = np.arange(1, K + 1)
p_true = 1.0 / ranks; p_true /= p_true.sum()
TAIL = ranks > 500                          # tail = topics ranked below 500
print(f"true tail mass (rank>500): {p_true[TAIL].sum():.3f}")

def sharpen(p, a=1.15):                     # sampling with temperature < 1 favours common topics
    q = p ** a
    return q / q.sum()

def run(real_share, quarters=8, seed=7):
    rng = np.random.default_rng(seed)
    p = p_true.copy()                       # quarter-0 model = true distribution
    rows = []
    for q in range(1, quarters + 1):
        n_real = int(N * real_share); n_syn = N - n_real
        c = rng.multinomial(n_real, p_true) + rng.multinomial(n_syn, sharpen(p))
        p = c / c.sum()                     # next model = empirical mix it was trained on
        rows.append((q, p[TAIL].sum(), int((p == 0).sum())))
    return rows

for share in (0.40, 0.0):
    print(f"real share {share:.0%}:")
    rows = run(share)
    for q, tail, dead in rows:
        if q in (1, 2, 4, 8):
            print(f"  quarter {q}: tail mass {tail:.3f}  topics with zero probability {dead}")
    if share == 0.40: r40 = rows
    else: r0 = rows

# deterministic fixed point for the 40% case (expected value, no sampling noise)
p = p_true.copy()
for _ in range(200):
    p = 0.4 * p_true + 0.6 * sharpen(p)
print(f"40% real, long-run expected tail mass: {p[TAIL].sum():.3f} (true {p_true[TAIL].sum():.3f})")

assert r0[-1][1] < r40[-1][1] < p_true[TAIL].sum()   # more real data -> less tail loss; still below truth
assert r0[-1][2] > r40[-1][2]                        # fewer extinct topics with real data
assert r0[0][1] > r0[-1][1]                          # tail shrinks over quarters without real data
