import tempfile, pathlib, warnings
import numpy as np, onnx, onnxruntime as ort, torch
from sklearn.datasets import load_iris
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.linear_model import LogisticRegression
from skl2onnx import to_onnx

_td = tempfile.TemporaryDirectory(prefix="q10_", dir="/tmp/claude-0/b6_q1_12"); tmp = pathlib.Path(_td.name)
print("onnx", onnx.__version__, "| onnxruntime", ort.__version__, "| providers:", ort.get_available_providers())

# ---- A. scikit-learn pipeline -> ONNX, parity on all 150 real rows
X, y = load_iris(return_X_y=True)
X32 = X.astype(np.float32)
pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=500)).fit(X32, y)
onx = to_onnx(pipe, X32[:1], target_opset=17, options={id(pipe): {"zipmap": False}})
onnx.checker.check_model(onx)
print("A. opset:", [(o.domain or "ai.onnx", o.version) for o in onx.opset_import])
s = ort.InferenceSession(onx.SerializeToString(), providers=["CPUExecutionProvider"])
lab, prob = s.run(None, {"X": X32})
print("A. labels equal:", bool((lab == pipe.predict(X32)).all()),
      "| max |proba diff|:", float(np.abs(prob - pipe.predict_proba(X32)).max()))

# ---- B. float64 input to a float32 graph
try:
    s.run(None, {"X": X})                       # X is float64
except Exception as e:
    print("B. float64 into float32 graph:", type(e).__name__, "-", str(e).replace("\n"," ")[-110:])

# ---- C. preprocessing that is arbitrary Python does not convert
bad = make_pipeline(FunctionTransformer(lambda a: np.log1p(a)), LogisticRegression(max_iter=500)).fit(X32, y)
try:
    to_onnx(bad, X32[:1], target_opset=17)
except Exception as e:
    print("C. FunctionTransformer(lambda):", type(e).__name__, "-", str(e).splitlines()[0][:100])

# ---- D. PyTorch module, dynamic batch axis (legacy exporter) and default exporter
torch.manual_seed(0)
net = torch.nn.Sequential(torch.nn.Linear(4, 8), torch.nn.ReLU(), torch.nn.Linear(8, 3)).eval()
def check(path, tag):
    sess = ort.InferenceSession(str(path), providers=["CPUExecutionProvider"])
    name = sess.get_inputs()[0].name
    for n in (1, 7):
        xb = torch.randn(n, 4)
        out = sess.run(None, {name: xb.numpy()})[0]
        d = float(np.abs(out - net(xb).detach().numpy()).max())
        print(f"D. {tag}: batch {n} -> out shape {out.shape}, max diff vs torch {d:.1e}")
    print(f"D. {tag}: declared input shape {sess.get_inputs()[0].shape}")

p1 = tmp / "legacy.onnx"
torch.onnx.export(net, torch.zeros(1, 4), str(p1), input_names=["x"], output_names=["y"],
                  dynamic_axes={"x": {0: "batch"}, "y": {0: "batch"}}, dynamo=False)
check(p1, "legacy exporter (dynamo=False)")
try:
    p2 = tmp / "default.onnx"
    torch.onnx.export(net, (torch.zeros(2, 4),), str(p2), input_names=["x"], output_names=["y"],
                      dynamic_shapes=({0: torch.export.Dim("batch")},))
    check(p2, "default exporter")
except Exception as e:
    print("D. default exporter failed here:", type(e).__name__, str(e).splitlines()[0][:120])
