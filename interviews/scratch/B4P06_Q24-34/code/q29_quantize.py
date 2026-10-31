# Q29: dynamic int8 quantisation: size, accuracy on held-out data, CPU latency.
import os, sys, time, tempfile, statistics
import numpy as np, onnxruntime as ort
from onnxruntime.quantization import quantize_dynamic, QuantType
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from skl2onnx import to_onnx
d = sys.argv[1]
X, y = make_classification(n_samples=6000, n_features=64, n_informative=30, n_classes=3, random_state=0)
X = X.astype(np.float32)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
m = MLPClassifier(hidden_layer_sizes=(256, 256), max_iter=60, random_state=0).fit(Xtr, ytr)
onx = to_onnx(m, Xtr[:1], target_opset=17, options={id(m): {"zipmap": False}})
fp = os.path.join(d, "mlp_fp32.onnx"); q = os.path.join(d, "mlp_int8.onnx")
open(fp, "wb").write(onx.SerializeToString())
try:
    quantize_dynamic(fp, q, weight_type=QuantType.QInt8)
except Exception as e:
    print("quantiser rejected model:", type(e).__name__, e); raise SystemExit
print("size KB fp32 %.0f  int8 %.0f" % (os.path.getsize(fp)/1024, os.path.getsize(q)/1024))
def acc(path):
    s = ort.InferenceSession(path, providers=["CPUExecutionProvider"])
    return (s.run(["label"], {s.get_inputs()[0].name: Xte})[0] == yte).mean(), s
a32, s32 = acc(fp); a8, s8 = acc(q)
print("sklearn acc %.4f | onnx fp32 acc %.4f | onnx int8 acc %.4f (held-out %d rows)" % (m.score(Xte, yte), a32, a8, len(yte)))
l32 = s32.run(["label"], {"X": Xte})[0]; l8 = s8.run(["label"], {"X": Xte})[0]
print("rows where int8 label differs from fp32: %d of %d" % ((l32 != l8).sum(), len(yte)))
def lat(s, batch):
    x = Xte[:batch]; ts = []
    for _ in range(5): s.run(["label"], {"X": x})
    for _ in range(60):
        t = time.perf_counter(); s.run(["label"], {"X": x}); ts.append((time.perf_counter()-t)*1000)
    return statistics.median(ts)
for b in (1, 256):
    print("median ms batch %3d: fp32 %.3f  int8 %.3f  (this sandbox, not a benchmark)" % (b, lat(s32, b), lat(s8, b)))
