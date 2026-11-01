import numpy as np

rng = np.random.default_rng(39)
stars = np.arange(1, 6)
# true rating distribution among titles watched (invented), probability of rating given the star level (invented)
pmf = np.array([0.06, 0.10, 0.28, 0.30, 0.26]); p_rate = np.array([0.004, 0.006, 0.012, 0.025, 0.050]) * 0.81
true_mean = float((pmf * stars).sum())
rate_overall = float((pmf * p_rate).sum())
obs_pmf = pmf * p_rate / rate_overall
obs_mean = float((obs_pmf * stars).sum())
print("true mean among watched:", round(true_mean, 3), " rating rate:", round(rate_overall, 4), " mean among rated:", round(obs_mean, 3))
assert abs(true_mean - 3.6) < 0.05 and abs(rate_overall - 0.02) < 0.003 and abs(obs_mean - 4.3) < 0.05

# simulate: 200,000 users x 10 watched titles in the natural world; 1,000 users x 10 titles in the random prompt
n_nat = 2_000_000
r = rng.choice(stars, n_nat, p=pmf)
seen = rng.random(n_nat) < p_rate[r - 1]
print("natural ratings observed:", int(seen.sum()), " share:", round(float(seen.mean()), 4), " mean:", round(float(r[seen].mean()), 3))
n_probe = 10_000
rp = rng.choice(stars, n_probe, p=pmf)
print("random prompt: n =", n_probe, " mean:", round(float(rp.mean()), 3), " (se about", round(float(rp.std() / np.sqrt(n_probe)), 3), ")")

# the gap is selection, not noise: observed mean 4.3 vs probe 3.6
gap = r[seen].mean() - rp.mean()
assert gap > 0.6

# correct with inverse-propensity weights estimated from the probe: P(rated | star) is proportional to obs_pmf / probe_pmf
obs_counts = np.bincount(r[seen], minlength=6)[1:] / seen.sum()
probe_pmf = np.bincount(rp, minlength=6)[1:] / n_probe
w = probe_pmf / obs_counts                         # relative weight per star = 1 / relative propensity
ipw_mean = (w[r[seen] - 1] * r[seen]).sum() / w[r[seen] - 1].sum()
print("IPW-corrected mean of observed ratings:", round(float(ipw_mean), 3), "(probe", round(float(rp.mean()), 3), ")")
assert abs(ipw_mean - rp.mean()) < 0.05
print("weights per star (relative):", np.round(w / w[0], 2))

# a model trained on observed ratings only: item-level offset learned from observed mean; evaluate on probe
# (every title has a quality q; rating = clip(round(q + noise))); rating propensity rises with the star level
n_items = 500
q = rng.normal(3.6, 0.5, n_items)
def draw(items):
    return np.clip(np.rint(q[items] + rng.normal(0, 0.9, len(items))), 1, 5).astype(int)
watch_items = rng.integers(0, n_items, 3_000_000)
rating = draw(watch_items)
got = rng.random(len(watch_items)) < p_rate[rating - 1]
tr_i, tr_r = watch_items[got], rating[got]
mu_obs = np.array([tr_r[tr_i == i].mean() if (tr_i == i).any() else tr_r.mean() for i in range(n_items)])
probe_items = rng.integers(0, n_items, 20_000); probe_r = draw(probe_items)
pred = mu_obs[probe_items]
print("model trained on observed ratings: mean prediction on probe", round(float(pred.mean()), 3), " probe mean", round(float(probe_r.mean()), 3))
print("RMSE on observed ratings (last 20,000 rated rows, rated-only view):", round(float(np.sqrt(((mu_obs[tr_i[-20000:]] - tr_r[-20000:]) ** 2).mean())), 3),
      " RMSE on the random probe:", round(float(np.sqrt(((pred - probe_r) ** 2).mean())), 3))
assert pred.mean() - probe_r.mean() > 0.4
# fix: weight training rows by 1/propensity (star level) so training matches the probe; compare probe RMSE
probe_all = draw(rng.integers(0, n_items, 10_000))      # a random prompt, as in the scenario
pp = np.bincount(probe_all, minlength=6)[1:] / len(probe_all); oo = np.bincount(tr_r, minlength=6)[1:] / len(tr_r)
wt = (pp / oo)[tr_r - 1]                                # weights estimated from the probe, not from the hidden propensities
mu_w = np.array([(wt[tr_i == i] * tr_r[tr_i == i]).sum() / wt[tr_i == i].sum() if (tr_i == i).any() else tr_r.mean() for i in range(n_items)])
pw = mu_w[probe_items]
print("IPW model: mean prediction on probe", round(float(pw.mean()), 3), " RMSE on probe", round(float(np.sqrt(((pw - probe_r) ** 2).mean())), 3))
assert np.sqrt(((pw - probe_r) ** 2).mean()) < np.sqrt(((pred - probe_r) ** 2).mean())
