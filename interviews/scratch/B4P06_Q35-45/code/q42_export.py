import io, os, tempfile, warnings, traceback
import numpy as np, torch, onnx, onnxruntime as ort
warnings.filterwarnings("ignore")
print("torch", torch.__version__, "| onnx", onnx.__version__, "| onnxruntime", ort.__version__)
os.chdir(tempfile.mkdtemp())
def sess(b): return ort.InferenceSession(b, providers=["CPUExecutionProvider"])
def err(e, n=230): return (type(e).__name__ + ": " + str(e).replace("\n", " "))[:n]
def export(model, args, **kw):
    f = io.BytesIO(); torch.onnx.export(model, args, f, dynamo=False, **kw); return f.getvalue()

class Net(torch.nn.Module):
    def __init__(s): super().__init__(); s.l = torch.nn.Linear(4, 2)
    def forward(s, x): return s.l(x)
net = Net().eval()

print("\n== 1. data-dependent control flow: trace bakes in one branch ==")
class Branchy(torch.nn.Module):
    def forward(s, x):
        if x.sum() > 0: return x * 2          # python if on a tensor value
        return x - 100
b = Branchy().eval()
traced = torch.jit.trace(b, torch.ones(1, 4), check_trace=False)
neg = -torch.ones(1, 4)
print("eager on negative input:", b(neg).tolist()[0], "| traced on negative input:", traced(neg).tolist()[0], "  <- silently wrong (branch frozen)")
class Fixed(torch.nn.Module):
    def forward(s, x): return torch.where(x.sum() > 0, x * 2, x - 100)   # branch inside the graph
fx = Fixed().eval(); o = sess(export(fx, torch.ones(1, 4), input_names=["x"], opset_version=17))
print("fixed with torch.where, ONNX on negative input:", o.run(None, {"x": neg.numpy()})[0].tolist()[0])
scripted = torch.jit.script(b); print("torch.jit.script keeps the branch, negative input:", scripted(neg).tolist()[0])

print("\n== 2. unsupported operator (no ONNX mapping) ==")
class Fft(torch.nn.Module):
    def forward(s, x): return torch.fft.rfft(x).abs()
try: export(Fft().eval(), torch.ones(1, 8), opset_version=17)
except Exception as e: print("fft:", err(e))
class DftMag(torch.nn.Module):                      # fix: express the transform with ops the exporter knows (a DFT matrix)
    def __init__(s, n=8):
        super().__init__(); k = torch.arange(n // 2 + 1)[:, None] * torch.arange(n)[None, :] * 2 * torch.pi / n
        s.register_buffer("c", torch.cos(k)); s.register_buffer("s", torch.sin(k))
    def forward(s, x): return torch.sqrt((x @ s.c.T) ** 2 + (x @ s.s.T) ** 2)
xx = torch.arange(8.).reshape(1, 8); o = sess(export(DftMag().eval(), xx, input_names=["x"], opset_version=17))
print("DFT-matrix rewrite exports; max diff vs torch.fft:", float(np.abs(o.run(None, {"x": xx.numpy()})[0] - Fft()(xx).numpy()).max()) < 1e-4)

print("\n== 3. missing dynamic axis: exported with batch 1, serve batch 7 ==")
fixed_b = sess(export(net, torch.ones(1, 4), input_names=["x"], output_names=["y"], opset_version=17))
x7 = np.random.default_rng(0).normal(size=(7, 4)).astype(np.float32)
try: fixed_b.run(None, {"x": x7})
except Exception as e: print("batch 7:", err(e))
dyn = sess(export(net, torch.ones(1, 4), input_names=["x"], output_names=["y"], opset_version=17, dynamic_axes={"x": {0: "batch"}, "y": {0: "batch"}}))
print("with dynamic_axes, batch 7 output shape:", dyn.run(None, {"x": x7})[0].shape, "| matches torch:", np.allclose(dyn.run(None, {"x": x7})[0], net(torch.from_numpy(x7)).detach().numpy(), atol=1e-5))

print("\n== 4. opset mismatch between exporter and runtime ==")
m = onnx.load_from_string(export(net, torch.ones(1, 4), input_names=["x"], opset_version=17, dynamic_axes={"x": {0: "b"}}))
print("exported opset:", m.opset_import[0].version)
m.opset_import[0].version = 99                       # pretend a newer exporter produced it
try: sess(m.SerializeToString())
except Exception as e: print("runtime too old for opset 99:", err(e, 600)[:60], "...", str(e)[-160:].replace("\n"," "))

print("\n== 5. float64 input to a float32 graph ==")
try: dyn.run(None, {"x": x7.astype(np.float64)})
except Exception as e: print("float64:", err(e))
print("fix: x.astype(np.float32) -> shape", dyn.run(None, {"x": x7.astype(np.float64).astype(np.float32)})[0].shape)

print("\n== 6. preprocessing outside the graph ==")
mean, std = torch.tensor([10., 20., 30., 40.]), torch.tensor([2., 2., 2., 2.])
raw = np.array([[12., 24., 34., 44.]], np.float32)
class Core(torch.nn.Module):
    def __init__(s): super().__init__(); s.l = torch.nn.Linear(4, 1)
    def forward(s, x): return s.l(x)
core = Core().eval()
class WithPre(torch.nn.Module):
    def __init__(s, core): super().__init__(); s.core = core; s.register_buffer("mean", mean); s.register_buffer("std", std)
    def forward(s, x): return s.core((x - s.mean) / s.std)          # normalisation lives in the graph
core_only = sess(export(core, torch.ones(1, 4), input_names=["x"], opset_version=17))
full = sess(export(WithPre(core).eval(), torch.ones(1, 4), input_names=["x"], opset_version=17))
want = core(torch.from_numpy((raw - mean.numpy()) / std.numpy())).detach().numpy()
print("expected (normalised first):", want.round(4).tolist(), "| graph without preprocessing on raw input:", core_only.run(None, {"x": raw})[0].round(4).tolist(), "| graph with preprocessing:", full.run(None, {"x": raw})[0].round(4).tolist())

print("\n== 7. newer torch.export-based exporter (default dynamo=True in recent torch) ==")
try:
    f = io.BytesIO(); torch.onnx.export(net, (torch.ones(1, 4),), f); print("default exporter wrote", len(f.getvalue()), "bytes")
except Exception as e: print("default exporter:", err(e, 300))

print("\n== 8. TorchScript save and load ==")
ts = torch.jit.trace(net, torch.ones(1, 4)); ts.save("net.pt"); back = torch.jit.load("net.pt")
print("loaded matches eager on batch 7:", bool(torch.allclose(back(torch.from_numpy(x7)), net(torch.from_numpy(x7)))), "| file size > 0:", os.path.getsize("net.pt") > 0)
