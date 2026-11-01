# Q29: 20 regions, one holds 30% of revenue (illustrative simulation, seeded)
import numpy as np

rng = np.random.default_rng(29)
share = np.r_[0.30, np.full(19, 0.70 / 19)]
print("other 19 regions each:", round(0.70 / 19 * 100, 2), "% (19 x 3.7 = 70.3 so the prompt's 3.7 is rounded)")
assert abs(share.sum() - 1) < 1e-12

PRE, POST, SD, LIFT = 8, 4, 0.05, 0.02           # weeks; weekly noise 5% per region; true campaign lift +2% in treated regions
def one(assign):
    mult = np.where(assign == 1, 1 + LIFT, 1.0)      # assign: 1 treated, 0 control, -1 left out
    pre = share[:, None] * (1 + rng.normal(0, SD, (20, PRE)))
    post = share[:, None] * mult[:, None] * (1 + rng.normal(0, SD, (20, POST)))
    T, C = assign == 1, assign == 0
    naive = post[T].sum() / post[C].sum() - 1                                    # compare post-period levels
    did = (post[T].sum() / pre[T].sum() * PRE / POST) / (post[C].sum() / pre[C].sum() * PRE / POST) - 1   # change vs own history
    return naive, did, pre[T].sum() / pre[T | C].sum()

# the actual draw in the prompt: big region (index 0) landed in treatment, 9 of the other 19 join it
a = np.zeros(20, int); a[0] = 1; a[1 + rng.permutation(19)[:9]] = 1
base_share = share[a == 1].sum()
print(f"treated regions hold {base_share*100:.1f}% of revenue before the test (control {100-base_share*100:.1f}%)")
assert abs(base_share - (0.30 + 9 * 0.70 / 19)) < 1e-9 and base_share > 0.6
print("lift if no effect existed would be read as", round(base_share / (1 - base_share) - 1, 3), "by a naive level comparison")

R = 4000
out = np.array([one(a) for _ in range(R)])
print(f"this assignment, true lift +2.0%: naive level comparison {out[:,0].mean()*100:+.1f}% ; change-vs-own-history {out[:,1].mean()*100:+.2f}% (sd {out[:,1].std()*100:.2f})")
assert out[:, 0].mean() > 0.5 and abs(out[:, 1].mean() - LIFT) < 0.005

# all random 10/10 assignments: how often does the big region land in treatment, and how lopsided is the baseline?
res = []
for _ in range(R):
    g = np.zeros(20, int); g[rng.permutation(20)[:10]] = 1
    res.append((g[0], share[g == 1].sum()))
res = np.array(res)
print(f"big region in treatment in {res[:,0].mean()*100:.0f}% of random splits; baseline share of treated regions ranges {res[:,1].min()*100:.0f}% to {res[:,1].max()*100:.0f}%")
# options: random 10/10; or run the big region on its own and randomize the other 19 (9 treated, 9 control, 1 spare)
def rand():
    g = np.zeros(20, int); g[rng.permutation(20)[:10]] = 1
    return g
def without_big():
    g = -np.ones(20, int); idx = 1 + rng.permutation(19)
    g[idx[:9]] = 1; g[idx[9:18]] = 0
    return g
sds = {}
for name, f in (("random 10/10", rand), ("big region left out", without_big)):
    d = np.array([one(f()) for _ in range(3000)])
    sds[name] = d[:, 1].std()
    print(f"{name:19s}: treated share of baseline revenue {d[:,2].min()*100:.0f}%-{d[:,2].max()*100:.0f}%; estimate mean {d[:,1].mean()*100:+.2f}%, sd {d[:,1].std()*100:.2f} points")
assert sds["big region left out"] < sds["random 10/10"]
sd_b = sds["big region left out"]
print(f"smallest lift detectable with about 80% power is 2.8 x sd = {2.8*sd_b*100:.1f}% , so a true +2% would not be detected either way")
assert 2.8 * sd_b > LIFT
