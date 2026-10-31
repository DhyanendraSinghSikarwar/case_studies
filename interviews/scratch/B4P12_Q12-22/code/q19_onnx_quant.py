"""Q19: tiny model -> ONNX -> dynamic int8 quantisation -> size/accuracy check -> HMAC-signed manifest.
Timings are sandbox CPU only, NOT device numbers. Fake signing key."""
import os, sys, json, time, hmac, hashlib, tempfile, warnings
warnings.filterwarnings("ignore")
import numpy as np, torch, onnx, onnxruntime as ort
from onnxruntime.quantization import quantize_dynamic, QuantType
torch.manual_seed(19); np.random.seed(19)
d = tempfile.mkdtemp(prefix="q19_", dir="/tmp/claude-0/b12_q12_22")
# synthetic 3-class "defect" data, 128 features
C = np.random.randn(3, 128) * 0.25
def make(n):
    y = np.random.randint(0, 3, n); c = C
    return (c[y] + np.random.randn(n, 128)).astype("float32"), y
Xtr, ytr = make(6000); Xte, yte = make(2000)
m = torch.nn.Sequential(torch.nn.Linear(128, 512), torch.nn.ReLU(), torch.nn.Linear(512, 512), torch.nn.ReLU(), torch.nn.Linear(512, 3))
opt = torch.optim.Adam(m.parameters(), 1e-3)
for ep in range(15):
    for i in range(0, 6000, 128):
        xb, yb = torch.from_numpy(Xtr[i:i+128]), torch.from_numpy(ytr[i:i+128])
        opt.zero_grad(); torch.nn.functional.cross_entropy(m(xb), yb).backward(); opt.step()
m.eval()
f32 = os.path.join(d, "model_fp32.onnx"); i8 = os.path.join(d, "model_int8.onnx")
torch.onnx.export(m, torch.from_numpy(Xte[:1]), f32, input_names=["x"], output_names=["logits"], dynamic_axes={"x": {0: "batch"}}, dynamo=False)
onnx.checker.check_model(onnx.load(f32))
quantize_dynamic(f32, i8, weight_type=QuantType.QInt8)
def acc_and_time(path):
    s = ort.InferenceSession(path, providers=["CPUExecutionProvider"])
    s.run(None, {"x": Xte[:64]})
    t = time.perf_counter(); out = s.run(None, {"x": Xte})[0]; dt = time.perf_counter() - t
    return (out.argmax(1) == yte).mean(), dt * 1000, out
a32, t32, o32 = acc_and_time(f32); a8, t8, o8 = acc_and_time(i8)
s32, s8 = os.path.getsize(f32), os.path.getsize(i8)
print(f"torch version {torch.__version__}, onnxruntime {ort.__version__}, onnx {onnx.__version__}")
print(f"fp32: {s32/1024:.0f} KiB  acc={a32:.4f}  2000-row run {t32:.1f} ms (sandbox CPU only)")
print(f"int8: {s8/1024:.0f} KiB  acc={a8:.4f}  2000-row run {t8:.1f} ms (sandbox CPU only)")
print(f"size ratio int8/fp32 = {s8/s32:.2f}; accuracy change = {a8-a32:+.4f}; prediction agreement = {(o32.argmax(1)==o8.argmax(1)).mean():.4f}")
GATE_DROP = 0.01
assert a32 - a8 <= GATE_DROP, "quantisation accuracy gate failed"
print(f"gate: accuracy drop <= {GATE_DROP} -> PASS")
# signed manifest (HMAC with a FAKE key; real systems use KMS/HSM-held keys or Ed25519 and a trust root on device)
KEY = b"fake-demo-key-not-secret"
man = {"model": "model_int8.onnx", "sha256": hashlib.sha256(open(i8, "rb").read()).hexdigest(), "version": "2026.10.1", "min_app": "3.2"}
body = json.dumps(man, sort_keys=True).encode(); sig = hmac.new(KEY, body, hashlib.sha256).hexdigest()
def verify(path, man, sig):
    body = json.dumps(man, sort_keys=True).encode()
    return hmac.compare_digest(sig, hmac.new(KEY, body, hashlib.sha256).hexdigest()) and hashlib.sha256(open(path, "rb").read()).hexdigest() == man["sha256"]
print("manifest verifies:", verify(i8, man, sig))
raw = bytearray(open(i8, "rb").read()); raw[100] ^= 1
tam = os.path.join(d, "tampered.onnx"); open(tam, "wb").write(raw)
print("tampered file verifies:", verify(tam, man, sig))
