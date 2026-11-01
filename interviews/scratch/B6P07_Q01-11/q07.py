import math
from scipy import stats
n = 500
before, after = 430, 445
lost, gained = 40, 55
assert before - lost + gained == after and before/n == 0.86 and after/n == 0.89
stay_pass = before - lost; stay_fail = (n - before) - gained
print(f"stay pass {stay_pass}, lost {lost}, gained {gained}, stay fail {stay_fail}; changed {lost+gained} of {n} = {(lost+gained)/n:.0%}")
assert (stay_pass, stay_fail) == (390, 15) and (lost+gained)/n == 0.19
# Paired test (McNemar): among the 95 discordant prompts, is 55 vs 40 different from 47.5 vs 47.5?
d = lost + gained
p_exact = stats.binomtest(gained, d, 0.5).pvalue
z = (gained - lost) / math.sqrt(d)
print(f"net +{gained-lost} ({(gained-lost)/n:.1%}); exact McNemar p = {p_exact:.3f}; z = {z:.2f}")
assert round(p_exact, 3) == 0.151 and round(z, 2) == 1.54
# 95% interval on the net change in pass rate (paired, normal approx)
diff = (gained - lost) / n
se = math.sqrt(((gained + lost) / n - diff**2) / n)
print(f"paired 95% CI for change in pass rate: {diff-1.96*se:+.1%} to {diff+1.96*se:+.1%}")
assert diff - 1.96*se < 0 < diff + 1.96*se
# Noise floor: if the OLD model re-run on the same 500 flips about 8% of prompts by itself (illustrative), churn of 19% is only partly new
flip = 0.08
print(f"illustrative self-flip {flip:.0%} = {flip*n:.0f} prompts; observed churn {d} prompts")
# Regression severity: weight by importance (illustrative): 8 of the 40 lost prompts are 'critical' (policy, safety, refunds)
crit_lost, crit_total = 8, 100
print(f"critical prompts failing: {crit_lost} of {crit_total} critical in the suite = {crit_lost/crit_total:.0%}; each critical regression blocks a full rollout")
assert crit_lost/crit_total == 0.08
# Canary sizing: 5% canary on 20,000 requests/day = 1,000 requests/day
print("canary requests per day at 5% of 20,000:", int(0.05*20000)); assert int(0.05*20000) == 1000
