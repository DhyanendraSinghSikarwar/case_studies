import numpy as np

both_abn, both_norm, a_only, b_only = 150, 750, 60, 40
n = both_abn + both_norm + a_only + b_only
assert n == 1000
po = (both_abn + both_norm) / n
a_abn, b_abn = both_abn + a_only, both_abn + b_only
assert po == 0.90 and a_abn == 210 and b_abn == 190
pe = (a_abn / n) * (b_abn / n) + (1 - a_abn / n) * (1 - b_abn / n)
kappa = (po - pe) / (1 - pe)
assert abs(pe - 0.6798) < 1e-9 and abs(kappa - 0.6877) < 5e-4
print("raw agreement", po, "chance agreement", round(pe, 4), "kappa", round(kappa, 4))
pos_agree = 2 * both_abn / (a_abn + b_abn)
neg_agree = 2 * both_norm / (2 * both_norm + a_only + b_only)
print("positive agreement", round(pos_agree, 3), "negative agreement", round(neg_agree, 3))
assert round(pos_agree, 3) == 0.75
# Baseline: a model that says everything is normal scores this against A
print("all-normal accuracy vs reader A:", 1 - a_abn / n)
assert abs((1 - a_abn / n) - 0.79) < 1e-12

# Bootstrap interval for kappa (seeded)
rng = np.random.default_rng(15)
cells = np.array([both_abn, a_only, b_only, both_norm])
def kap(c):
    t = c.sum(); o = (c[0] + c[3]) / t
    a = (c[0] + c[1]) / t; b = (c[0] + c[2]) / t
    e = a * b + (1 - a) * (1 - b)
    return (o - e) / (1 - e)
bs = [kap(rng.multinomial(n, cells / n)) for _ in range(4000)]
lo, hi = np.percentile(bs, [2.5, 97.5])
print("bootstrap 95% interval for kappa:", round(float(lo), 3), round(float(hi), 3))
assert lo < kappa < hi

# Why accuracy against A has a ceiling. Illustrative generative model: prevalence 20%, readers independent given truth.
prev, sens, spec = 0.20, 0.90, 0.96
def reader_accuracy(): return prev * sens + (1 - prev) * spec
acc_A = reader_accuracy()
# a perfect model (equals truth) scored against reader A has accuracy = reader A's accuracy
truth = rng.random(200_000) < prev
ra = np.where(truth, rng.random(truth.size) < sens, rng.random(truth.size) > spec)
rb = np.where(truth, rng.random(truth.size) < sens, rng.random(truth.size) > spec)
print("sim: perfect model accuracy vs A:", round(float((truth == ra).mean()), 3), "reader A vs B agreement:", round(float((ra == rb).mean()), 3))
assert abs((truth == ra).mean() - acc_A) < 0.003
assert (truth == ra).mean() < 1.0 and abs((ra == rb).mean() - 0.90) < 0.02
