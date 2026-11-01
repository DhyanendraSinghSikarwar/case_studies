# Q54: deflation 70% vs true resolution, estimated by stratified human labelling (illustrative, seeded)
import numpy as np
rng = np.random.default_rng(54)

N = 100_000
deflated = 70_000                                  # 70% not handed to a human
assert deflated / N == 0.70
# truth (unknown to the analyst): by topic, share of deflated conversations really resolved
topics = {"billing": dict(n=28_000, p_resolved=0.45), "faq": dict(n=42_000, p_resolved=0.70)}
assert sum(t["n"] for t in topics.values()) == deflated
true_resolved = sum(t["n"] * t["p_resolved"] for t in topics.values())
print("true resolved among deflated:", true_resolved / deflated, "| true resolution rate over all conversations:", true_resolved / N)
assert true_resolved / deflated == 0.60 and true_resolved / N == 0.42

# human labelling: 200 per topic, stratified, then reweight by topic size
est = 0.0; var = 0.0
for name, t in topics.items():
    k = rng.binomial(200, t["p_resolved"])
    p = k / 200
    w = t["n"] / deflated
    est += w * p
    var += w * w * p * (1 - p) / 200
half = 1.96 * np.sqrt(var)
print(f"labelled estimate among deflated: {est:.3f} +/- {half:.3f}  -> resolution rate over all: {est*0.70:.3f} +/- {half*0.70:.3f}")
assert abs(est - 0.60) < 3 * np.sqrt(var)
assert half < 0.05

# reported vs real
print(f"reported deflation {deflated/N:.0%} vs estimated true resolution about {est*0.70:.0%}")

# a second signal: recontact within 7 days on the same issue
recontact_deflated, recontact_human = 0.28, 0.10
print("recontact within 7 days: deflated", recontact_deflated, "vs human-handled", recontact_human)
assert round(recontact_deflated / recontact_human, 1) == 2.8
