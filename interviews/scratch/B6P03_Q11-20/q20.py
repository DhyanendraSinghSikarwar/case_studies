# Q20: -999 sentinels and text-typed income (illustrative simulation)
import numpy as np, pandas as pd
rng = np.random.default_rng(20)
from scipy.stats import rankdata
def sig(z): return 1 / (1 + np.exp(-z))
def auc(s, y):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def fit(X, y, it=30):
    w = np.zeros(X.shape[1])
    for _ in range(it):
        p = sig(X @ w); H = (X * (p * (1 - p))[:, None]).T @ X + 1e-6 * np.eye(len(w))
        w += np.linalg.solve(H, X.T @ (y - p))
    return w
N = 300_000
age = np.clip(rng.normal(40, 12, N), 18, 90).round()
inc = rng.lognormal(np.log(50_000), 0.5, N).round()
age_missing = np.zeros(N, bool); age_missing[rng.choice(N, 12_000, replace=False)] = True   # 4%
logit = -2.5 - 0.03 * (age - 40) - 0.6 * (inc / 50_000 - 1) + 1.2 * age_missing
y = (rng.random(N) < sig(logit)).astype(float)
df = pd.DataFrame({"age": np.where(age_missing, -999, age), "income": inc.astype(int).astype(str)})
bad = rng.random(N)
df.loc[bad < 0.03, "income"] = "N/A"; df.loc[(bad >= 0.03) & (bad < 0.05), "income"] = "null"
df.loc[(bad >= 0.05) & (bad < 0.06), "income"] = ""
# 1. find them: look at extreme values and at what refuses to parse
print("age sentinel rows:", int((df.age == -999).sum()), f"= {(df.age == -999).mean():.1%}")
assert (df.age == -999).sum() == 12_000
print("age min / mean with sentinel:", df.age.min(), round(df.age.mean(), 2), " mean without:", round(df.age[df.age != -999].mean(), 2))
parsed = pd.to_numeric(df.income, errors="coerce")
tokens = df.income[parsed.isna()].replace("", "<empty>").value_counts()
print("income tokens that failed to parse:\n" + tokens.to_string())
assert set(tokens.index) == {"N/A", "null", "<empty>"} and tokens.sum() == parsed.isna().sum()
print(f"income unparsable: {parsed.isna().mean():.2%}")
# 2. handle: explicit NaN + missing flags + median fill (fit on training rows only)
tr = rng.random(N) < 0.7; te = ~tr
age_c = df.age.where(df.age != -999)
inc_c = parsed
def design(clean):
    if clean:
        a_med, i_med = age_c[tr].median(), inc_c[tr].median()
        return np.c_[np.ones(N), age_c.fillna(a_med), inc_c.fillna(i_med) / 1e4, age_c.isna(), inc_c.isna()]
    i_fill = inc_c.fillna(0)                          # the 'quick model': text coerced, blanks to 0, -999 left in
    return np.c_[np.ones(N), df.age, i_fill / 1e4]
res = {}
for name, flag in (("quick (-999 left in)", False), ("cleaned + flags", True)):
    X = design(flag); w = fit(X[tr], y[tr]); res[name] = auc(X[te] @ w, y[te])
    print(f"{name:22} test AUC {res[name]:.3f}")
assert res["cleaned + flags"] > res["quick (-999 left in)"]
# 3. does it matter?  Compare coefficients on age
Xq = design(False); Xc = design(True)
print("age coefficient quick:", round(fit(Xq[tr], y[tr])[1], 4), " cleaned:", round(fit(Xc[tr], y[tr])[1], 4), " (truth -0.03)")
print(f"event rate: age missing {y[age_missing].mean():.1%} vs present {y[~age_missing].mean():.1%}")
assert abs(fit(Xc[tr], y[tr])[1] + 0.03) < 0.005
