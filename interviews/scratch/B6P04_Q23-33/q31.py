# Q31: heavy-tailed revenue per user (illustrative simulation, seeded)
import numpy as np
from scipy import stats

rng = np.random.default_rng(31)
def population(n):
    """80% buy nothing, 19.9% ordinary buyers (lognormal), 0.1% whales (lognormal, very large)."""
    kind = rng.choice(3, n, p=[0.80, 0.199, 0.001])
    lvl = np.where(kind == 1, rng.lognormal(np.log(55), 0.8, n), np.where(kind == 2, rng.lognormal(np.log(3650), 0.8, n), 0.0))
    return lvl
big = population(4_000_000)
srt = np.sort(big)[::-1]
top_share = srt[:4000].sum() / big.sum()
print(f"mean revenue per user {big.mean():.1f}; top 0.1% of users hold {top_share*100:.1f}% of revenue; p99.9 = {np.quantile(big, .999):.0f}")
assert abs(big.mean() - 20) < 2 and abs(top_share - 0.25) < 0.04

N, REPS, LIFT = 100_000, 300, 0.03
def trial():
    L0 = population(2 * N)                           # each user's spend level
    pre = L0 * rng.gamma(4, 0.25, 2 * N)              # pre-period revenue, correlated with post
    post = L0 * rng.gamma(4, 0.25, 2 * N)
    arm = np.r_[np.zeros(N, int), np.ones(N, int)]
    post = post * (1 + LIFT * arm)
    cap = np.quantile(post, 0.999)                   # cap set from pooled data, blind to arm
    res = {}
    for name, y in (("raw mean", post), ("capped at p99.9", np.minimum(post, cap))):
        d = y[arm == 1].mean() - y[arm == 0].mean()
        se = np.sqrt(y[arm == 1].var(ddof=1) / N + y[arm == 0].var(ddof=1) / N)
        res[name] = (d / y[arm == 0].mean(), abs(d / se) > 1.96)
    th = np.cov(post, pre)[0, 1] / pre.var()          # CUPED
    adj = post - th * (pre - pre.mean())
    d = adj[arm == 1].mean() - adj[arm == 0].mean()
    se = np.sqrt(adj[arm == 1].var(ddof=1) / N + adj[arm == 0].var(ddof=1) / N)
    res["CUPED (pre revenue)"] = (d / adj[arm == 0].mean(), abs(d / se) > 1.96)
    res["log(1+x)"] = (None, abs(stats.ttest_ind(np.log1p(post[arm == 1]), np.log1p(post[arm == 0])).statistic) > 1.96)
    return res
R = [trial() for _ in range(REPS)]
print(f"true effect +3% on every user's revenue, {N:,} users per arm, {REPS} simulated tests")
print(f"{'method':22s} {'power':>6s} {'mean est. lift':>15s} {'sd of est.':>11s}")
pw = {}
for k in R[0]:
    power = np.mean([r[k][1] for r in R])
    pw[k] = power
    if R[0][k][0] is None:
        print(f"{k:22s} {power:6.2f} {'(log scale)':>15s}"); continue
    e = np.array([r[k][0] for r in R])
    print(f"{k:22s} {power:6.2f} {e.mean()*100:14.2f}% {e.std()*100:10.2f}")
assert pw["CUPED (pre revenue)"] > pw["raw mean"]
assert pw["raw mean"] < 0.3 and pw["capped at p99.9"] > pw["raw mean"]
print("capped lift is read lower than the true +3% because whales' extra spend above the cap is thrown away: the cap changes the estimand")
