"""Make two small iris ONNX models (v1 logistic regression, v2 random forest) in a temp dir."""
import sys, pathlib
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from skl2onnx import to_onnx

out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
X, y = load_iris(return_X_y=True)
X = X.astype(np.float32)
for name, m in [("iris_v1", LogisticRegression(max_iter=500)),
                ("iris_v2", RandomForestClassifier(n_estimators=20, random_state=0))]:
    m.fit(X, y)
    onx = to_onnx(m, X[:1], target_opset=17, options={id(m): {"zipmap": False}})
    (out / f"{name}.onnx").write_bytes(onx.SerializeToString())
    print(name, "train accuracy", round(float((m.predict(X) == y).mean()), 3))
