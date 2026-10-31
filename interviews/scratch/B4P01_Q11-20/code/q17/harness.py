import sys, pathlib, tempfile, numpy as np, pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import review_target, fixed

rng = np.random.default_rng(0)                       # PURE NOISE: 120 rows, 400 features, random labels -> honest accuracy is about 0.5
df = pd.DataFrame(rng.normal(size=(120, 400)), columns=[f"f{i}" for i in range(400)])
df["y"] = rng.integers(0, 2, 120)
p = pathlib.Path(tempfile.mkdtemp()) / "data.csv"; df.to_csv(p, index=False)

print("== buggy, run 3 times (note: prints TRAIN accuracy, and it changes each run)")
for _ in range(3):
    review_target.train_and_report(str(p))
print("== buggy but score on its own test split (what bug 3 hides)")
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
X = SelectKBest(f_classif, k=20).fit_transform(df.drop(columns="y"), df["y"])
Xtr, Xte, ytr, yte = train_test_split(X, df["y"], test_size=0.3, random_state=0)
print("leaky test accuracy:", round(LogisticRegression(max_iter=200).fit(Xtr, ytr).score(Xte, yte), 3), "(labels are random, so this should be about 0.5)")
print("== fixed")
fixed.train_and_report(str(p)); fixed.train_and_report(str(p))
