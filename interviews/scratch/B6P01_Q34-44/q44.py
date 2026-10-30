# Q44 DAU baseline with weekly cycle, moving festival dates and growth (illustrative simulation)
import numpy as np
rng = np.random.default_rng(44)
D = 365 * 3
t = np.arange(D)
dow = np.array([1.0, 1.0, 1.0, 1.0, 1.02, 1.08, 1.06])
fest_days = {0: [300, 301, 302], 1: [330, 331, 332], 2: [320, 321, 322]}   # moves each year (day offsets within the year)
fest = np.zeros(D)
for yr, ds in fest_days.items():
    for d in ds:
        fest[yr*365 + d] = 1
# festival lift 12% on the day, 6% in the two days before
lift = np.zeros(D)
for i in np.where(fest == 1)[0]:
    lift[i] = 0.12
    lift[max(0, i-2):i] += 0.06
true = 1_000_000 * np.exp(0.0006*t) * dow[t % 7] * (1 + lift)
y = true * np.exp(rng.normal(0, 0.012, D))

# model: log y = a + b t + dow dummies + festival indicators; fit on first two years, test on year three
def design(idx, use_fest=True):
    cols = [np.ones(len(idx)), idx.astype(float)]
    for k in range(1, 7):
        cols.append(((idx % 7) == k).astype(float))
    if use_fest:
        cols.append((lift[idx] > 0).astype(float))
    return np.column_stack(cols)
tr = np.arange(0, 730); te = np.arange(730, D)
res = {}
for flag in (False, True):
    X = design(tr, flag)
    # festival dates of the next year are known in advance from the calendar, so the flag is available at test time
    beta, *_ = np.linalg.lstsq(X, np.log(y[tr]), rcond=None)
    r = np.log(y[tr]) - X @ beta
    # robust sigma from MAD on non-festival days
    sd = 1.4826*np.median(np.abs(r - np.median(r)))
    pred = design(te, flag) @ beta
    z = (np.log(y[te]) - pred)/sd
    res[flag] = (z, sd)
    print(f"festival flag {flag}: robust sigma {sd:.4f}; share of test days with z<-3: {(z<-3).mean():.3%}; z>3: {(z>3).mean():.3%}")
# one-sided alerts; inject an 8% drop on 10 random normal days
z_f, sd_f = res[True]
normal_days = np.array([i for i in range(len(te)) if lift[te[i]] == 0])
inj = rng.choice(normal_days, 10, replace=False)
y2 = y[te].copy(); y2[inj] *= 0.92
Xte = design(te, True)
beta, *_ = np.linalg.lstsq(design(tr, True), np.log(y[tr]), rcond=None)
z2 = (np.log(y2) - Xte @ beta)/sd_f
caught = (z2[inj] < -3).sum()
print(f"threshold z<-3 (about {3*sd_f*100:.1f}% below expected): caught {caught}/10 injected 8% drops; false alerts in 365 clean days: {(z_f<-3).sum()}")
assert (res[False][0] < -3).sum() + (res[False][0] > 3).sum() > (z_f < -3).sum() + (z_f > 3).sum()
assert caught >= 8
# naive same-day-last-week rule around festival days
naive = y[te][7:]/y[te][:-7]-1                      # naive[j]: day j+7 versus day j
fday = np.array([i for i in range(len(te)) if lift[te[i]] > 0])
up = naive[fday[fday >= 7] - 7]                     # festival-affected day vs the same weekday a week earlier
down = naive[fday[fday < len(naive)]]               # one week LATER vs the festival-affected day
print(f"naive week-over-week on festival-affected days: {up.min():+.1%} to {up.max():+.1%}")
print(f"naive week-over-week one week later (comparing with the festival day): {down.min():+.1%} to {down.max():+.1%}")
assert down.min() < -0.05
