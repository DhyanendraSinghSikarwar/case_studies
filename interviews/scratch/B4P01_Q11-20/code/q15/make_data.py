import sys, numpy as np, pandas as pd
rng = np.random.default_rng(7)
n = 400
df = pd.DataFrame({"tenure": rng.integers(1, 72, n), "monthly_spend": rng.normal(60, 20, n).round(2), "support_calls": rng.poisson(2, n)})
z = -0.04 * df.tenure + 0.02 * df.monthly_spend + 0.4 * df.support_calls - 0.3 + rng.normal(0, 0.8, n)
df["churned"] = (z > 0).astype(int)
df.to_csv(sys.argv[1], index=False)
print("rows", n, "churn rate", round(df.churned.mean(), 3))
