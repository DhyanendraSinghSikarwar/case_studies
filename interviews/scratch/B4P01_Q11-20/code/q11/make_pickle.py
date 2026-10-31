# run under the OLD environment (scikit-learn 1.6.1)
import json, pickle, sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
X, y = make_classification(n_samples=100, random_state=0)
m = LogisticRegression().fit(X, y)
with open("model_old.pkl", "wb") as f:
    pickle.dump(m, f)
with open("model_old.meta.json", "w") as f:        # sidecar: what built this artifact
    json.dump({"sklearn": sklearn.__version__, "python": "3.13"}, f)
print("wrote model_old.pkl with scikit-learn", sklearn.__version__)
