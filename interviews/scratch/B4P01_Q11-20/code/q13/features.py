"""Single source of truth for features. Training and serving both import this."""
import numpy as np
import pandas as pd
from pydantic import BaseModel

INCOME_FILL = 50_000.0   # constant learned at training time, stored in code/config, not retyped elsewhere
COLUMNS = ["age", "income", "household", "income_per_head", "log_income", "is_senior"]


class RawRow(BaseModel):          # schema contract at the service boundary
    age: int
    income: float | None = None
    household: int


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)
    out["age"] = df["age"]
    out["income"] = df["income"].fillna(INCOME_FILL)
    out["household"] = df["household"]
    out["income_per_head"] = (out["income"] / out["household"]).round(2)
    out["log_income"] = np.log1p(out["income"]).round(4)
    out["is_senior"] = (out["age"] >= 60).astype(int)
    return out[COLUMNS]
