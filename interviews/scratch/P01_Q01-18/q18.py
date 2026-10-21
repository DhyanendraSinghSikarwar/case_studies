import numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
rng = np.random.default_rng(0)
df = pd.DataFrame({"y": (rng.random(10000) < .02).astype(int)})
a, b = train_test_split(df, test_size=.2, random_state=0)
c, d = train_test_split(df, test_size=.2, random_state=0, stratify=df.y)
print("random  test pos rate:", b.y.mean().round(4), " stratified:", d.y.mean().round(4), " overall:", df.y.mean().round(4))
# small sample variability
rates = [train_test_split(df.iloc[:500], test_size=.2, random_state=s)[1].y.mean() for s in range(200)]
print("500-row sample, random split test-rate spread: min %.3f max %.3f" % (min(rates), max(rates)))
rates = [train_test_split(df.iloc[:500], test_size=.2, random_state=s, stratify=df.y.iloc[:500])[1].y.mean() for s in range(200)]
print("stratified spread: min %.3f max %.3f" % (min(rates), max(rates)))
