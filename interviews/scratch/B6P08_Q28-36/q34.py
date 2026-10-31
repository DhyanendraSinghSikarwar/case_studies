# Illustrative numbers only. Why KS at 2,000,000 rows flags tiny shifts, and a calibrated effect-size alert rule.
import math, numpy as np
from scipy import stats
rng = np.random.default_rng(34)
n = 2_000_000
shift = 0.05
# 1. Critical KS statistic: smallest D that is "significant" at alpha = 0.001.
def d_crit(n1, n2, alpha=0.001):
    return math.sqrt(-math.log(alpha / 2) / 2) * math.sqrt((n1 + n2) / (n1 * n2))
dc = d_crit(n, n)
print('critical D at n=m=2,000,000, alpha=0.001:', round(dc, 5))
assert round(dc, 5) == 0.00195
print('observed D=0.02 is', round(0.02 / dc, 1), 'x the critical value')
assert 10 < 0.02 / dc < 11
print('critical D if the reference has only 100,000 rows:', round(d_crit(n, 100_000), 4))
assert round(d_crit(n, 100_000), 4) == 0.0063
print('critical D for 5,000 rows each:', round(d_crit(5000, 5000), 4))
assert d_crit(5000, 5000) > 0.02        # a 5,000-row subsample would NOT flag D=0.02
# 2a. One feature at the full 2,000,000 rows: a 0.05 sd shift gives D near 0.02 and a p-value that underflows to zero.
one = stats.ks_2samp(rng.standard_normal(n), rng.standard_normal(n) + 0.05)
print('2,000,000 rows, shift 0.05 sd: D', round(one.statistic, 4), 'p', one.pvalue)
assert 0.018 < one.statistic < 0.022 and one.pvalue < 0.001
# 2b. Scan of 40 features (300,000 rows each to keep the run short): 38 shifted by 0.05 sd, 2 untouched.
k = 300_000
flag, Ds = 0, []
for j in range(40):
    cur = rng.standard_normal(k) + (shift if j < 38 else 0.0)
    r = stats.ks_2samp(rng.standard_normal(k), cur)
    Ds.append(r.statistic); flag += r.pvalue < 0.001
print('flagged', flag, 'of 40 (', flag / 40, '), max D', round(max(Ds), 4))
assert flag == 38 and flag / 40 == 0.95 and max(Ds) < 0.03
# 3. Does a 0.05 sd shift hurt the model? Fixed logistic score on 5 features, labels from the true relation.
m = 200_000
w = np.array([0.8, 0.6, 0.5, 0.4, 0.3])
def auc(score, y):
    r = stats.rankdata(score); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
X0 = rng.standard_normal((m, 5)); X1 = rng.standard_normal((m, 5)) + shift
y0 = (rng.random(m) < 1 / (1 + np.exp(-(X0 @ w)))).astype(int)
y1 = (rng.random(m) < 1 / (1 + np.exp(-(X1 @ w)))).astype(int)
a0, a1 = auc(X0 @ w, y0), auc(X1 @ w, y1)
print('AUC before', round(a0, 4), 'after the shift', round(a1, 4))
assert abs(a1 - a0) < 0.005
# 4. Calibrate the effect-size threshold from history: 26 weeks of week-over-week D with natural wobble.
hist = []
base = rng.standard_normal(200_000)
for wk in range(26):
    mu = rng.normal(0, 0.03)                       # seasonal wobble in standard deviations
    hist.append(stats.ks_2samp(base, rng.standard_normal(200_000) + mu).statistic)
q99 = float(np.quantile(hist, 0.99))
print('week-over-week D: median', round(float(np.median(hist)), 4), '99th percentile', round(q99, 4))
thr = 0.10                                          # chosen effect-size threshold, several times the natural wobble
assert thr > 3 * q99 and max(Ds) < thr
# 5. Alert rule (illustrative): D >= thr on at least 2 of the 10 most important features, two weeks running.
def alert(weekly_D, imp_top10, k=2, weeks=2):
    hits = [sum(weekly_D[f] >= thr for f in imp_top10) >= k for weekly_D in weekly_D_history]
    return len(hits) >= weeks and all(hits[-weeks:])
weekly_D_history = [Ds, Ds]
assert not alert(None, range(10))                    # this week's D=0.02 does not alert
weekly_D_history = [[0.12] * 40, [0.15] * 40]
assert alert(None, range(10))
# 6. These are not chance false positives: under NO change, 40 features at p<0.001 give about 0.04 flags a week.
expected_null_flags = 40 * 0.001
print('expected flags per week under no change at p<0.001:', expected_null_flags, '; P(at least one):', round(1 - 0.999 ** 40, 4))
assert expected_null_flags == 0.04 and round(1 - 0.999 ** 40, 3) == 0.039
# 38 flags therefore mean 38 real but tiny differences; the fix is an effect-size rule, not a smaller p-value.
