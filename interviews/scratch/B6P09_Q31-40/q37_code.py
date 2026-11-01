import numpy as np

F = np.array([0.50, 0.70, 0.80, 0.90, 0.95, 0.98, 1.00])
ages = np.arange(7)
avg = F.mean()
print("sum of shares", round(F.sum(), 2), "| average observed share", round(avg, 4), "| relative underestimate", round(1 - avg, 4))
assert round(F.sum(), 2) == 5.83 and round(avg, 4) == 0.8329 and round(1 - avg, 4) == 0.1671

# simulate: true conversion rate 5%, delay distribution implied by F; labels as seen at training time
rng = np.random.default_rng(37)
clicks_per_age, cvr = 200_000, 0.05
inc = np.diff(np.r_[0, F])                           # share of eventual conversions arriving on each delay day
obs_conv = np.zeros(7); true_conv = np.zeros(7)
for a in ages:
    conv = rng.random(clicks_per_age) < cvr
    # delay day d with probability inc[d] (d = 0..6); observed if d <= age
    d = rng.choice(7, size=clicks_per_age, p=inc)
    true_conv[a] = conv.sum()
    obs_conv[a] = (conv & (d <= a)).sum()
naive = obs_conv.sum() / (7 * clicks_per_age)
print("true rate", round(true_conv.sum() / (7 * clicks_per_age), 4), "| naive training rate", round(naive, 4), "| ratio", round(naive / cvr, 3))
assert abs(naive / cvr - avg) < 0.01
# fix A: train only on mature clicks (age 6): unbiased but only 1/7 of the volume and a week stale
print("mature-only (age 6) rate", round(obs_conv[6] / clicks_per_age, 4), "| rows used", clicks_per_age, "of", 7 * clicks_per_age)
# fix B: inverse-maturity correction per age bucket (estimating F from older cohorts, known here)
corr = (obs_conv / F).sum() / (7 * clicks_per_age)
print("rate after dividing each age bucket by its observed share", round(corr, 4))
assert abs(corr - cvr) < 0.003
# per-age naive rates: shows where the bias sits
print("naive rate by age", np.round(obs_conv / clicks_per_age, 4))
# fix C: label-time correction on click-level probabilities: p_true ~= p_seen / F(age)  (calibration intuition)
print("age-0 clicks look like", round(0.5 * cvr, 4), "instead of", cvr, "-> a model that ignores age learns", round(avg * cvr, 4), "on average")
assert round(avg * cvr, 4) == 0.0416
# a delayed-feedback style model: P(conv seen at age a) = p * F(a); fit p by maximum likelihood on (age, seen)
seen = []; ag = []
for a in ages:
    conv = rng.random(clicks_per_age) < cvr
    d = rng.choice(7, size=clicks_per_age, p=inc)
    seen.append(conv & (d <= a)); ag.append(np.full(clicks_per_age, a))
seen = np.concatenate(seen); ag = np.concatenate(ag)
grid = np.linspace(0.02, 0.08, 601)
ll = [(seen * np.log(p * F[ag]) + (~seen) * np.log(1 - p * F[ag])).sum() for p in grid]
p_hat = grid[int(np.argmax(ll))]
print("maximum-likelihood p with known F(age):", round(p_hat, 4))
assert abs(p_hat - cvr) < 0.002
