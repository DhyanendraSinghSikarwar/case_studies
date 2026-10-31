import numpy as np

# Illustrative numbers from the prompt
t_small, t_large, accept, budget = 0.8, 2.5, 0.60, 3.0
esc = 1 - accept

mean_cascade = accept * t_small + esc * (t_small + t_large)   # escalated pay both calls in series
print(f"mean cascade {mean_cascade:.2f} s vs always-large {t_large:.2f} s")
assert round(mean_cascade, 2) == 1.80 and round(mean_cascade - t_large, 2) == -0.70

t_esc = t_small + t_large
print(f"escalated request {t_esc:.2f} s vs budget {budget:.1f} s -> over by {t_esc - budget:.2f} s")
assert round(t_esc, 2) == 3.30 and t_esc > budget

# p95 with fixed latencies: 40% of requests take 3.3 s, so the 95th percentile sits in that group
lat = np.array([t_small] * 60 + [t_esc] * 40)
p95 = np.percentile(lat, 95)
print("p95 of cascade with fixed latencies:", round(p95, 2), "| always-large p95:", t_large)
assert round(p95, 2) == 3.30
# How rare must escalation be for the p95 to stay at 0.8 s?
print("escalation rate must be at most 5% for p95 = small-model latency")

# Same with noise (seeded, lognormal sigma 0.25 around each mean): cascade p95 is above 3.3 and above always-large
rng = np.random.default_rng(7)
n = 200_000
def ln(mu, size): return mu * rng.lognormal(-0.25**2 / 2, 0.25, size)
is_esc = rng.random(n) < esc
sim = ln(t_small, n) + np.where(is_esc, ln(t_large, n), 0.0)
sim_large = ln(t_large, n)
print(f"simulated: cascade mean {sim.mean():.2f}, p95 {np.percentile(sim, 95):.2f}; always-large mean {sim_large.mean():.2f}, p95 {np.percentile(sim_large, 95):.2f}")
assert np.percentile(sim, 95) > np.percentile(sim_large, 95) > budget   # with noise both break 3.0, the cascade more

# Speculative parallel variant: fire both at once, use small if accepted, else wait for large
par = accept * t_small + esc * t_large
print(f"parallel variant: mean {par:.2f} s, escalated latency {t_large:.2f} s (but you pay for large on 100% of requests)")
assert round(par, 2) == 1.48
