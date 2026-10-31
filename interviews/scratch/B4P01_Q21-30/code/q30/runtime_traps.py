# things the type checker cannot see: both lines type-check, both fail or mislead at runtime
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # -I removes the script dir from sys.path
import numpy as np
import pandas as pd
from features import add_features, log_income

df = pd.DataFrame({"salary": [10.0, 20.0]})        # wrong column name: mypy is happy
try:
    add_features(df)
except KeyError as e:
    print("KeyError at runtime (mypy cannot see DataFrame columns):", e)
a = np.ones((3, 2))                               # wrong shape / dtype is also invisible to NDArray[float64]
print("2-D array accepted by a function meant for 1-D income:", log_income(a).shape)
