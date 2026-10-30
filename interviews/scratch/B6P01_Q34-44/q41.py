# Q41 LLM re-ranker: query-level success ratio, delta method vs naive SE, guardrails (illustrative simulation)
import numpy as np
rng = np.random.default_rng(41)
n = 20_000
def arm(p_succ, p_click, mean_q=4.0, lat_mu=5.0, lat_sigma=0.35):
    # per-user query counts and a user-level propensity so queries within a user are correlated
    q = 1 + rng.poisson(mean_q - 1, n)
    prop = np.clip(rng.normal(p_succ, 0.12, n), 0.02, 0.98)
    succ = rng.binomial(q, prop)
    clicks = rng.binomial(q, np.clip(prop * p_click / p_succ, 0, 1))
    return q, succ, clicks
qc, sc, cc = arm(0.50, 0.50)
qt, st, ct = arm(0.52, 0.47)           # more queries succeed, fewer end in a click
def ratio(num, den):
    r = num.sum()/den.sum()
    m = den.mean()
    resid = num - r*den
    se_delta = np.sqrt(resid.var(ddof=1)/n)/m               # users are the unit
    return r, se_delta
rc, sec = ratio(sc, qc); rt, set_ = ratio(st, qt)
diff = rt - rc; se = np.hypot(sec, set_)
print(f"success per query: control {rc:.3f} treatment {rt:.3f} diff {diff:+.4f} CI [{diff-1.96*se:+.4f}, {diff+1.96*se:+.4f}] (user-level delta method)")
# naive SE treats every query as independent
p_c, p_t = rc, rt
nq_c, nq_t = qc.sum(), qt.sum()
se_naive = np.sqrt(p_c*(1-p_c)/nq_c + p_t*(1-p_t)/nq_t)
print(f"naive per-query SE {se_naive:.5f} vs delta-method SE {se:.5f}")
assert se > se_naive
# click-based view moves the other way
clc, clt = cc.sum()/qc.sum(), ct.sum()/qt.sum()
print(f"click per query: control {clc:.3f} treatment {clt:.3f} diff {clt-clc:+.4f}")
assert clt < clc and rt > rc
# latency guardrail p95 and cost per query (invented)
lat_c = rng.lognormal(np.log(180), 0.4, 50_000); lat_t = lat_c * 1.0 + rng.lognormal(np.log(90), 0.5, 50_000)
print(f"p95 latency ms: control {np.percentile(lat_c,95):.0f} treatment {np.percentile(lat_t,95):.0f}")
cost_per_query = 0.0020; budget = 0.0025
print(f"cost per query {cost_per_query} vs budget {budget}: ok = {cost_per_query <= budget}")
assert np.percentile(lat_t, 95) > np.percentile(lat_c, 95)
