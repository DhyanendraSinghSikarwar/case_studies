import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

FEATURES = ["tenure_months", "monthly_spend", "support_calls"]


def make_data(n=600, seed=0):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "tenure_months": rng.integers(1, 72, n),
        "monthly_spend": rng.normal(60, 15, n).round(2),
        "support_calls": rng.poisson(1.5, n),
    })
    z = -1.0 - 0.04 * df.tenure_months + 0.02 * df.monthly_spend + 0.5 * df.support_calls
    df["churned"] = (rng.random(n) < 1 / (1 + np.exp(-z))).astype(int)
    return df


def add_ratio(df):                       # tiny feature function: UNIT test target
    out = df.copy()
    out["spend_per_month_tenure"] = out.monthly_spend / out.tenure_months.clip(lower=1)
    return out


def train(df, seed=0):
    model = LogisticRegression(max_iter=1000, random_state=seed)
    model.fit(df[FEATURES], df["churned"])
    return model
