# Q34: summary rating slipped 4.3 -> 3.9 after an unversioned prompt edit (illustrative simulation)
import numpy as np

rng = np.random.default_rng(34)
assert round(4.3 - 3.9, 1) == 0.4 and round((4.3 - 3.9) / 4.3, 3) == 0.093

# 1. No version was logged: find WHEN it changed from daily mean ratings (60 days, 40 rated per day)
days, per_day, change_day = 60, 40, 33
daily_mean = []
for d in range(days):
    mu = 4.3 if d < change_day else 3.9
    r = np.clip(np.round(rng.normal(mu, 0.9, per_day)), 1, 5)
    daily_mean.append(r.mean())
daily_mean = np.array(daily_mean)
def sse(k):  # two-level fit with a break before day k
    return ((daily_mean[:k] - daily_mean[:k].mean()) ** 2).sum() + ((daily_mean[k:] - daily_mean[k:].mean()) ** 2).sum()
best = min(range(5, days - 5), key=sse)
print(f"estimated change day {best} (true {change_day});  mean before {daily_mean[:best].mean():.2f}  after {daily_mean[best:].mean():.2f}")
assert abs(best - change_day) <= 2
# the date is only a lead: match it against deploy logs / git history of the template

# 2. Frozen regression set: 150 fixed inputs in 5 categories, same judge, old vs new prompt (paired)
cats = ["complaint-type", "short", "long", "technical", "legal"]
cat_of = np.repeat(np.arange(5), 30)
base = rng.normal(4.3, 0.5, 150)                    # item difficulty carried across prompts
effect = np.array([+0.6, -0.5, -0.9, -0.7, -0.6])   # the edit helps one case, hurts four
old = np.clip(base + rng.normal(0, 0.3, 150), 1, 5)
new = np.clip(base + effect[cat_of] + rng.normal(0, 0.3, 150), 1, 5)
diff = new - old
boot = [rng.choice(diff, 150).mean() for _ in range(4000)]
lo, hi = np.percentile(boot, [2.5, 97.5])
print(f"paired mean change {diff.mean():+.2f}  95% bootstrap [{lo:+.2f}, {hi:+.2f}]")
for c in range(5):
    print(f"  {cats[c]:15} {diff[cat_of == c].mean():+.2f}")
assert hi < 0 and diff[cat_of == 0].mean() > 0 and diff[cat_of == 2].mean() < -0.5
# average of the effects: (0.6 - 0.5 - 0.9 - 0.7 - 0.6) / 5
assert abs(effect.mean() - (-0.42)) < 1e-9

# 3. Why a frozen set beats waiting for live ratings: sample sizes for a 0.4 shift
sd = 0.9
n_live = 2 * (1.96 + 0.8416) ** 2 * sd ** 2 / 0.4 ** 2    # independent groups
sd_diff = diff.std(ddof=1)                                 # paired: only the prompt effect + noise
n_paired = (1.96 + 0.8416) ** 2 * sd_diff ** 2 / 0.4 ** 2
print(f"ratings needed for 80% power at a 0.4 shift: unpaired {n_live:.0f} per group, paired {n_paired:.0f} items")
assert n_live > 4 * n_paired

# 4. Ship gate: block a prompt version if any category drops more than 0.3 or the mean drops at all
def gate(d, cat, tol=0.3):
    worst = min(d[cat == c].mean() for c in range(5))
    return bool(d.mean() >= 0 and worst >= -tol)
print("gate passes for the edited prompt:", gate(diff, cat_of))
assert gate(diff, cat_of) is False and gate(np.zeros(150), cat_of) is True
