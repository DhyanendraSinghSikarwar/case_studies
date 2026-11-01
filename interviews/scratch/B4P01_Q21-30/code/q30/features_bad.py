import numpy as np
import numpy.typing as npt
import pandas as pd
from features import add_features

FloatArray = npt.NDArray[np.float64]

def log_income(income: FloatArray, floor: float = 1.0) -> FloatArray:
    return np.log(np.maximum(income, floor))

def run(df: pd.DataFrame) -> None:
    add_features(df, floor="1")             # ERROR: str where float expected
    log_income([1.0, 2.0])                  # ERROR: list is not an ndarray
    log_income(np.array([1.0]), floor="1")  # ERROR: str where float expected
    x: int = log_income(np.array([1.0]))    # ERROR: array assigned to int
