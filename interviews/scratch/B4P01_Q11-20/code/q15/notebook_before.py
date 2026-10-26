# What the notebook looked like, flattened into one script (cells in order). DO NOT ship this.
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle

df = pd.read_csv("C:/Users/me/Downloads/churn_final_v3.csv")     # hard-coded path
X = df[["tenure", "monthly_spend", "support_calls"]]
y = df["churned"]
X = StandardScaler().fit_transform(X)                            # fitted on ALL rows: test statistics leak in
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2)       # no seed
m = LogisticRegression().fit(Xtr, ytr)
print("accuracy", m.score(Xte, yte))                             # metric only printed
pickle.dump(m, open("model.pkl", "wb"))                          # scaler not saved: serving cannot reproduce inputs
