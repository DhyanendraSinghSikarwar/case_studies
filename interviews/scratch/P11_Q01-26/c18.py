import numpy as np, pandas as pd
rng = np.random.default_rng(0)
n = 1000
df = pd.DataFrame({"user": rng.integers(0, 50, n),
                   "ts": pd.Timestamp("2026-01-01") + pd.to_timedelta(np.sort(rng.integers(0, 90*24*3600, n)), unit="s"),
                   "y": rng.integers(0, 2, n)})
# point-in-time feature: user's past positives count, STRICTLY before this row
df = df.sort_values("ts").reset_index(drop=True)
df["past_pos"] = df.groupby("user")["y"].cumsum() - df["y"]
# time-based split with a gap equal to label window (7 days)
cut = pd.Timestamp("2026-03-01"); gap = pd.Timedelta("7D")
train = df[df.ts < cut - gap]; test = df[df.ts >= cut]
print(len(train), len(test), train.ts.max() < test.ts.min())
print(df[["user","y","past_pos"]].head(3).to_string())
