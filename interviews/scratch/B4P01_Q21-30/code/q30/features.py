import numpy as np
import numpy.typing as npt
import pandas as pd

FloatArray = npt.NDArray[np.float64]

def log_income(income: FloatArray, floor: float = 1.0) -> FloatArray:
    """log of income with a floor, so zeros do not give -inf."""
    return np.log(np.maximum(income, floor))

def add_features(df: pd.DataFrame, floor: float = 1.0) -> pd.DataFrame:
    out = df.copy()
    out["log_income"] = log_income(out["income"].to_numpy(dtype=np.float64), floor)
    return out

def mean_log_income(df: pd.DataFrame) -> float:
    return float(add_features(df)["log_income"].mean())
