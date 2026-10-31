# Q50: noisy conversion counts (prompt numbers; true-conversion Poisson variation and pooling are illustrative)
import math
import numpy as np
sd_day, mean_day = 5.0, 8
print("noise sd / daily count:", sd_day / mean_day)
assert sd_day / mean_day == 0.625
sd7 = sd_day * math.sqrt(7)
print("7-day noise sd:", round(sd7, 2), " as share of 56:", round(sd7 / 56, 4))
assert mean_day * 7 == 56 and round(sd7, 2) == 13.23 and round(sd7 / 56, 3) == 0.236

# true conversions also vary (Poisson, invented): add that variance
pois7 = math.sqrt(56)
tot = math.sqrt(56 + sd7 ** 2)
print("Poisson sd of true 7-day total:", round(pois7, 2), " combined sd with noise:", round(tot, 2), " share:", round(tot / 56, 3))
assert round(tot / 56, 3) == 0.271

# days to get noise (alone) to 10% of the total: 5*sqrt(n)/(8n) = 0.1
n_days = (sd_day / (mean_day * 0.1)) ** 2
print("days for noise alone to reach 10%:", round(n_days, 1))
assert round(n_days, 1) == 39.1

# simulate: reported 7-day totals, noise can even go negative per day
rng = np.random.default_rng(2)
true = rng.poisson(8, size=(100_000, 7))
rep = true + rng.normal(0, 5, size=true.shape)
print("share of reported daily counts that are negative:", round((rep < 0).mean(), 3))
assert 0.03 < (rep < 0).mean() < 0.10
tot_rep, tot_true = rep.sum(1), true.sum(1)
print("sd of (reported - true) 7-day total:", round((tot_rep - tot_true).std(), 2))
assert abs((tot_rep - tot_true).std() - 13.23) < 0.3

# pooling: 20 similar small campaigns (invented). Pooled daily sd of the mean across campaigns:
k = 20
print("noise sd on the average daily count across 20 campaigns, one day:", round(5 / math.sqrt(k), 2), "vs mean 8 ->", round(5 / math.sqrt(k) / 8, 3))
assert round(5 / math.sqrt(k) / 8, 3) == 0.14

# shrinkage: posterior mean for a campaign with a 7-day reported total, prior from the pool (invented prior mean 56, sd 20)
prior_mu, prior_sd = 56.0, 20.0
obs = 70.0                                   # a reported total (invented)
w = prior_sd ** 2 / (prior_sd ** 2 + tot ** 2)
post = prior_mu + w * (obs - prior_mu)
print("weight on the campaign's own reading:", round(w, 2), " shrunk estimate:", round(post, 1), "(reported", obs, ")")
assert 0.6 < w < 0.7 and 64 < post < 66
