# make_model.py OUTDIR : train iris LogisticRegression, export ONNX (zipmap off), check it, save to OUTDIR/iris.onnx
import sys, pathlib, numpy as np, onnx, onnxruntime as ort
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from skl2onnx import to_onnx
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
X, y = load_iris(return_X_y=True); X = X.astype(np.float32)
m = LogisticRegression(max_iter=500).fit(X, y)
onx = to_onnx(m, X[:1], target_opset=17, options={id(m): {"zipmap": False}})
onnx.checker.check_model(onx)
(out / "iris.onnx").write_bytes(onx.SerializeToString())
s = ort.InferenceSession(str(out / "iris.onnx"), providers=["CPUExecutionProvider"])
print("inputs ", [(i.name, i.shape, i.type) for i in s.get_inputs()])
print("outputs", [(o.name, o.shape, o.type) for o in s.get_outputs()])
print("agree with sklearn on 150 rows:", bool((s.run(None, {"X": X})[0] == m.predict(X)).all()))
