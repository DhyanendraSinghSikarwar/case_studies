import numpy as np, pandas as pd
rng = np.random.default_rng(2)
df = pd.DataFrame({'seg': rng.choice(['A', 'B', 'C'], 100000, p=[.7, .2, .1])})
df['y'] = df.seg.map({'A': 10, 'B': 30, 'C': 80}) + rng.normal(0, 5, len(df))
srs = [df.y.sample(300, random_state=i).mean() for i in range(500)]
strat = [df.groupby('seg').sample(frac=300/len(df), random_state=i).y.mean() for i in range(500)]
print(np.std(srs).round(3), np.std(strat).round(3), df.y.mean().round(2))   # 1.279 vs 0.279; truth 21.04
