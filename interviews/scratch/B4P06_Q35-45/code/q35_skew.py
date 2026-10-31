# Q35: serving forgets to scale; parity test catches it; fix = export the whole Pipeline.
import numpy as np, onnxruntime as ort
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from skl2onnx import to_onnx

X, y = make_classification(n_samples=600, n_features=4, n_informative=3, n_redundant=0, random_state=0)
X = (X * np.array([1, 50, 1000, 0.01]) + np.array([0, 300, 5000, 2])).astype(np.float32)  # very different scales
Xtr, ytr, Xho = X[:500], y[:500], X[500:]                                                  # held-out parity sample

pipe = Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression(max_iter=1000))]).fit(Xtr, ytr)
opt = lambda m: {id(m): {"zipmap": False}}

# BUG: only the classifier is exported; the scaler stays in the training notebook
bad = to_onnx(pipe.named_steps["clf"], Xtr[:1], target_opset=17, options=opt(pipe.named_steps["clf"]))
# FIX: the whole Pipeline is exported, scaler included
good = to_onnx(pipe, Xtr[:1], target_opset=17, options=opt(pipe.steps[-1][1]))

def serve_labels(onnx_model, X):
    s = ort.InferenceSession(onnx_model.SerializeToString(), providers=["CPUExecutionProvider"])
    return s.run(["label"], {"X": X})[0]

def parity(name, onnx_model):
    ref = pipe.predict(Xho)
    got = serve_labels(onnx_model, Xho)
    agree = float((ref == got).mean())
    print(f"{name}: agreement with training pipeline on {len(Xho)} held-out rows = {agree:.3f}")
    return agree

a_bad = parity("buggy serving (no scaler)", bad)
a_good = parity("fixed serving (whole Pipeline)", good)
assert a_bad < 1.0 and a_good == 1.0

# probability parity with a tolerance (float32 vs float64 maths)
s = ort.InferenceSession(good.SerializeToString(), providers=["CPUExecutionProvider"])
p_onnx = s.run(["probabilities"], {"X": Xho})[0]
print("max |proba diff| fixed vs sklearn < 1e-4:", float(np.abs(p_onnx - pipe.predict_proba(Xho)).max()) < 1e-4)

# schema contract: refuse inputs the model was not trained on
CONTRACT = {"n_features": 4, "dtype": "float32"}
def check_contract(arr):
    if arr.ndim != 2 or arr.shape[1] != CONTRACT["n_features"]: raise ValueError(f"expected (n,4), got {arr.shape}")
    if str(arr.dtype) != CONTRACT["dtype"]: raise ValueError(f"expected float32, got {arr.dtype}")
    if not np.isfinite(arr).all(): raise ValueError("NaN or inf in input")
nan_arr = Xho[:2].copy(); nan_arr[0, 0] = np.nan
for name, arr in [("ok", Xho[:2]), ("3 columns", Xho[:2, :3]), ("float64", Xho[:2].astype(np.float64)), ("NaN", nan_arr)]:
    try: check_contract(arr); print("contract", name, "-> pass")
    except ValueError as e: print("contract", name, "-> reject:", e)
