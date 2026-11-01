import numpy as np, pandas as pd
from sklearn.datasets import make_classification
X, y = make_classification(n_samples=400, n_features=8, n_informative=4, random_state=0)
pd.DataFrame(X).assign(y=y).to_csv("data.csv", index=False)
