# shows what the refactor exposes: the notebook's scaler statistics include the test rows
import numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
df = pd.read_csv("data.csv")
X, y = df[["tenure", "monthly_spend", "support_calls"]], df["churned"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print("mean (all 400 rows, notebook):", X.mean().round(3).tolist())
print("mean (320 train rows, fixed) :", Xtr.mean().round(3).tolist())
print("max abs gap in std units:", float(((X.mean() - Xtr.mean()).abs() / Xtr.std()).max().round(4)))
