# Q26 survey nonresponse bias (illustrative simulation tuned to 250,000 users and about 4% response)
import numpy as np
rng = np.random.default_rng(26)
N = 250_000
eng = rng.normal(size=N)                                   # engagement (observable: sessions per week)
sat_true = np.clip(np.round(3.6 + 0.35 * eng + rng.normal(0, 0.9, N)), 1, 5)

def run(label, logit):
    p = 1 / (1 + np.exp(-logit))
    resp = rng.random(N) < p
    return resp

# Case A (MAR): response depends on engagement only
respA = run("A", -3.6 + 1.0 * eng)
# Case B (MNAR): response also depends on satisfaction itself
respB = run("B", -6.55 + 0.8 * eng + 0.75 * sat_true)
for name, resp in [("A response depends on engagement", respA), ("B response also depends on satisfaction", respB)]:
    print(f"{name}: responders {resp.sum():,} ({resp.mean():.1%}), responder mean {sat_true[resp].mean():.2f}, population mean {sat_true.mean():.2f}")

# IPW using only the observable (engagement decile) -> estimate response propensity per bin
def ipw_mean(resp):
    bins = np.digitize(eng, np.quantile(eng, np.linspace(0.1, 0.9, 9)))
    num = den = 0.0
    for b in range(10):
        m = bins == b
        rate = resp[m].mean()
        r = m & resp
        num += (sat_true[r] / rate).sum(); den += (r.sum() / rate)
    return num / den
for name, resp in [("A", respA), ("B", respB)]:
    print(f"case {name}: naive {sat_true[resp].mean():.2f}, engagement-weighted {ipw_mean(resp):.2f}, truth {sat_true.mean():.2f}")
assert abs(ipw_mean(respA) - sat_true.mean()) < 0.05          # MAR: weighting works
assert abs(ipw_mean(respB) - sat_true.mean()) > 0.15           # MNAR: weighting on engagement is not enough
assert sat_true[respA].mean() - sat_true.mean() > 0.2

# Worst-case bounds with the prompt's own numbers: 10,000 responders at 4.4, 240,000 silent users in [1, 5]
lo = (10_000 * 4.4 + 240_000 * 1) / 250_000
hi = (10_000 * 4.4 + 240_000 * 5) / 250_000
print(f"bounds on the population mean without any assumption: {lo:.3f} to {hi:.3f}")
assert (round(lo, 3), round(hi, 3)) == (1.136, 4.976)
# Follow-up sample: 600 randomly chosen non-responders contacted with an incentive
follow = rng.choice(np.where(~respB)[0], 600, replace=False)
rr = respB.mean(); est = rr * sat_true[respB].mean() + (1 - rr) * sat_true[follow].mean()
print(f"double sampling estimate {est:.2f} vs truth {sat_true.mean():.2f}")
assert abs(est - sat_true.mean()) < 0.12
