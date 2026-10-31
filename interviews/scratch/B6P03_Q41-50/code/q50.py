# Q50: user flags as labels, a coordinated flagging group, and real precision. Illustrative.
import numpy as np
from math import sqrt
N, F = 1_000_000, 30_000
assert F / N == 0.03
n_rev, n_fine = 500, 200
prec = (n_rev - n_fine) / n_rev
se = sqrt(prec * (1 - prec) / n_rev)
print(f"precision of flags = {n_rev-n_fine}/{n_rev} = {prec:.0%}, 95% interval +/- {1.96*se*100:.1f} points")
assert prec == 0.60 and round(1.96 * se, 3) == 0.043
print(f"implied harmful among flagged: {prec*F:,.0f}; false flags: {(1-prec)*F:,.0f}")
assert prec * F == 18_000

# Stratified view: 20% of flags sit in the suspect topic (illustrative strata precisions)
s_share, s_prec, o_prec = 0.20, 0.20, 0.70
overall = s_share * s_prec + (1 - s_share) * o_prec
print(f"suspect stratum {s_share*F:,.0f} flags at {s_prec:.0%}, rest {(1-s_share)*F:,.0f} at {o_prec:.0%} -> overall {overall:.0%}")
assert abs(overall - 0.60) < 1e-12
# a random 500 contains 100 suspect + 400 other flags: 20 + 280 = 300 fine? (harmful)
print(f"expected harmful in a random 500: {100*s_prec + 400*o_prec:.0f} -> fine {500 - (100*s_prec + 400*o_prec):.0f}")
assert 100 * s_prec + 400 * o_prec == 300

# Stratified sample, 250 per stratum, with stratum weights
rng = np.random.default_rng(50)
a = rng.random(250) < s_prec; b = rng.random(250) < o_prec
ea, eb = a.mean(), b.mean()
est = s_share * ea + (1 - s_share) * eb
se_s = sqrt(s_share**2 * ea*(1-ea)/250 + (1-s_share)**2 * eb*(1-eb)/250)
print(f"stratified: suspect {ea:.3f}, rest {eb:.3f}, overall {est:.3f} +/- {1.96*se_s:.3f}")
assert abs(est - 0.60) < 0.08

# Detecting coordinated flaggers: co-flag overlap in a small flag graph (scaled down)
posts, honest, coord = 5_000, 1_500, 100
M = np.zeros((honest + coord, posts), np.float32)
viral = rng.choice(posts, 60, replace=False)              # genuinely harmful posts many honest users flag
for u in range(honest):                                   # honest: 3 viral + 3 random posts
    M[u, rng.choice(viral, 3, replace=False)] = 1
    M[u, rng.choice(posts, 3, replace=False)] = 1
target = rng.choice(posts, 300, replace=False)            # the topic under attack
for u in range(honest, honest + coord):                   # coordinated: 30 of the same 300 posts
    M[u, rng.choice(target, 30, replace=False)] = 1
C = M @ M.T; np.fill_diagonal(C, 0)
truth = np.arange(honest + coord) >= honest
res = {}
for t in (1, 2, 3, 4):
    suspect = (C >= t).sum(1) >= 5                        # >=5 partners sharing >=t flagged posts
    tp = int((suspect & truth).sum()); fp = int((suspect & ~truth).sum())
    res[t] = (tp, fp)
    print(f"shared posts >= {t}: caught {tp}/{coord}, false alarms {fp}/{honest}")
assert res[4][0] >= 95 and res[4][1] <= 2
assert res[1][1] > 100 and res[1][1] > res[2][1] >= res[3][1] >= res[4][1]   # a loose rule flags honest users
