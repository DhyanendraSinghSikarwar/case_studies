import json, os, tempfile, time, warnings, numpy as np, onnxruntime as ort
warnings.filterwarnings("ignore")
from sklearn.neural_network import MLPClassifier
from skl2onnx import to_onnx
rng = np.random.default_rng(0)
X = rng.normal(size=(2000, 64)).astype(np.float32); y = (X[:, :8].sum(1) > 0).astype(int)
m = MLPClassifier(hidden_layer_sizes=(1024, 1024), max_iter=5, random_state=0).fit(X, y)
model = to_onnx(m, X[:1], target_opset=17, options={id(m): {"zipmap": False}}).SerializeToString()
print("onnxruntime", ort.__version__, "| available providers:", ort.get_available_providers())
print("CPU cores visible:", os.cpu_count())
batch = np.tile(X, (1, 1))[:1024]

def make(intra=0, inter=1, level=ort.GraphOptimizationLevel.ORT_ENABLE_ALL, mode=ort.ExecutionMode.ORT_SEQUENTIAL, profile=False):
    so = ort.SessionOptions(); so.intra_op_num_threads = intra; so.inter_op_num_threads = inter
    so.graph_optimization_level = level; so.execution_mode = mode; so.enable_profiling = profile
    return ort.InferenceSession(model, so, providers=["CPUExecutionProvider"])   # providers in fallback order

def bench(s, b, n=60):
    for _ in range(5): s.run(None, {"X": b})            # warm-up
    ts = []
    for _ in range(n):
        t = time.perf_counter(); s.run(None, {"X": b}); ts.append(time.perf_counter() - t)
    return float(np.median(ts) * 1000)

t = time.perf_counter(); s0 = make(); print(f"session creation: {(time.perf_counter()-t)*1000:.1f} ms vs one batch-1024 run: {bench(s0, batch, 10):.2f} ms (create once, reuse)")
print("\nintra-op threads (batch 1024, median ms, this sandbox only):")
for n in (1, 2, 4): print(f"  intra_op_num_threads={n}: {bench(make(intra=n), batch):.2f} ms")
print("\ngraph optimisation level (1 thread, batch 1024):")
for name, lvl in [("DISABLE_ALL", ort.GraphOptimizationLevel.ORT_DISABLE_ALL), ("ENABLE_BASIC", ort.GraphOptimizationLevel.ORT_ENABLE_BASIC), ("ENABLE_EXTENDED", ort.GraphOptimizationLevel.ORT_ENABLE_EXTENDED), ("ENABLE_ALL", ort.GraphOptimizationLevel.ORT_ENABLE_ALL)]:
    print(f"  {name}: {bench(make(intra=1, level=lvl), batch):.2f} ms")
print("\nbatch size 1 with 1 vs 4 threads (measure it, do not assume):")
for n in (1, 4): print(f"  intra_op_num_threads={n}: {bench(make(intra=n), X[:1], 200):.3f} ms")
print("\nsame session from 4 Python threads (sessions are thread safe for run):")
import concurrent.futures as cf
s = make(intra=1); ref = s.run(None, {"X": batch})[0]
with cf.ThreadPoolExecutor(4) as ex: outs = list(ex.map(lambda _: s.run(None, {"X": batch})[0], range(8)))
print("  all 8 results identical to single-thread result:", all(np.array_equal(o, ref) for o in outs))

d = tempfile.mkdtemp(); os.chdir(d)
sp = make(intra=1, profile=True); [sp.run(None, {"X": batch}) for _ in range(3)]
f = sp.end_profiling(); ev = json.load(open(f))
print("\nprofile file:", os.path.basename(f)[:20] + "...json", "| events:", len(ev), "| keys of an event:", sorted(ev[0].keys()))
node = next(e for e in ev if e.get("cat") == "Node")
print("categories seen:", sorted({e["cat"] for e in ev}), "| node event args keys:", sorted(node["args"].keys()))
tot = {}
for e in ev:
    if e.get("cat") == "Node" and e["name"].endswith("_kernel_time"): tot[e["args"].get("op_name", "?")] = tot.get(e["args"].get("op_name", "?"), 0) + e["dur"]
print("kernel time per op type (us, 3 runs):", dict(sorted(tot.items(), key=lambda kv: -kv[1])))
