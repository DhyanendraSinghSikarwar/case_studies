# run under the NEW environment (system python, scikit-learn 1.9.1)
import json, pickle, warnings, sklearn
from sklearn.exceptions import InconsistentVersionWarning
print("loading with scikit-learn", sklearn.__version__)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always", InconsistentVersionWarning)
    with open("model_old.pkl", "rb") as f:
        m = pickle.load(f)
for x in w:
    print("warning:", x.category.__name__, "|", str(x.message).split(" This")[0])
print("loaded:", type(m).__name__, "| version warnings:", len(w))

# safer: fail closed using the sidecar, instead of trusting a warning
meta = json.load(open("model_old.meta.json"))
if meta["sklearn"] != sklearn.__version__:
    print(f"GUARD: artifact built with {meta['sklearn']}, runtime has {sklearn.__version__} -> refuse to serve, retrain or re-export")
