import os, pickle, tempfile, pathlib, io
import numpy as np, joblib, torch
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from skl2onnx import to_onnx
import onnxruntime as ort
import skops.io as sio
from safetensors.torch import save_file, load_file

_td = tempfile.TemporaryDirectory(prefix="q09_", dir="/tmp/claude-0/b6_q1_12"); tmp = pathlib.Path(_td.name)

# 1. Harmless "attack": unpickling runs a function chosen by whoever made the file.
class Evil:
    def __reduce__(self):
        return (print, ("!! code ran during pickle.loads (a real attacker would run os.system here)",))
blob = pickle.dumps(Evil())
print("1. before loads: nothing printed yet")
pickle.loads(blob)

# 2. joblib round trip of a real model (same pickle machinery underneath)
X, y = load_iris(return_X_y=True); X = X.astype(np.float32)
m = LogisticRegression(max_iter=500).fit(X, y)
joblib.dump(m, tmp / "m.joblib")
m2 = joblib.load(tmp / "m.joblib")
print("2. joblib round trip same predictions:", bool((m.predict(X) == m2.predict(X)).all()), "| bytes:", (tmp / "m.joblib").stat().st_size)

# 3. skops: loading checks which types are in the file; unknown types need explicit trust
sio.dump(m, tmp / "m.skops")
print("3. skops untrusted types for our model:", sio.get_untrusted_types(file=tmp / "m.skops"))
m3 = sio.load(tmp / "m.skops", trusted=sio.get_untrusted_types(file=tmp / "m.skops"))   # only after YOU reviewed that list
print("   skops load ok:", bool((m.predict(X) == m3.predict(X)).all()))
sio.dump(Evil(), tmp / "evil.skops")
try:
    sio.load(tmp / "evil.skops")
except Exception as e:
    print("   skops refuses unknown/untrusted object:", type(e).__name__)

# 4. ONNX: graph + weights, no Python objects
onx = to_onnx(m, X[:1], target_opset=17, options={id(m): {"zipmap": False}})
(tmp / "m.onnx").write_bytes(onx.SerializeToString())
s = ort.InferenceSession(str(tmp / "m.onnx"), providers=["CPUExecutionProvider"])
lab = s.run(None, {"X": X})[0]
print("4. ONNX labels equal sklearn:", bool((lab == m.predict(X)).all()), "| bytes:", (tmp / "m.onnx").stat().st_size)

# 5. torch: pickled checkpoint vs weights_only vs safetensors
torch.save({"w": Evil()}, tmp / "evil.pt")
try:
    torch.load(tmp / "evil.pt", weights_only=True)
except Exception as e:
    print("5. torch.load(weights_only=True) blocked the pickle:", type(e).__name__)
sd = {"w": torch.arange(6, dtype=torch.float32).reshape(2, 3)}
save_file(sd, str(tmp / "w.safetensors"))
print("   safetensors round trip:", bool(torch.equal(load_file(str(tmp / "w.safetensors"))["w"], sd["w"])))
