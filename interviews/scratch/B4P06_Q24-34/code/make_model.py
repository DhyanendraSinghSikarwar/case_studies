# Builds iris ONNX model (LogisticRegression) into the dir given as argv[1]
import sys, os
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from skl2onnx import to_onnx
out = sys.argv[1]
X, y = load_iris(return_X_y=True)
X = X.astype(np.float32)
m = LogisticRegression(max_iter=500).fit(X, y)
onx = to_onnx(m, X[:1], target_opset=17, options={id(m): {"zipmap": False}})
os.makedirs(out, exist_ok=True)
with open(os.path.join(out, "iris.onnx"), "wb") as f:
    f.write(onx.SerializeToString())
print("wrote", os.path.join(out, "iris.onnx"), "bytes", len(onx.SerializeToString()))
