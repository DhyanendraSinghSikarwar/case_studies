"""Run once at training time: 20 seeded sample rows + the features the training path produced."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np, pandas as pd
from features import build_features

rng = np.random.default_rng(42)
df = pd.DataFrame({
    "age": rng.integers(18, 80, 20),
    "income": rng.integers(20, 200, 20) * 1000.0,
    "household": rng.integers(1, 6, 20),
})
df.loc[[3, 11, 17], "income"] = np.nan          # missing incomes on purpose
df.to_csv("golden_raw.csv", index=False)
build_features(df).to_csv("golden_features.csv", index=False)
print("golden rows:", len(df), "| NaN incomes:", int(df.income.isna().sum()))
