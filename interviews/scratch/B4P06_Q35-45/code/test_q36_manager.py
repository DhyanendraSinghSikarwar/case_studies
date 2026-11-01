import sys, threading, time, pathlib, tempfile
import numpy as np, pytest
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from sklearn.linear_model import LogisticRegression
from skl2onnx import to_onnx
from q36_manager import ModelManager

@pytest.fixture(scope="module")
def registry(tmp_path_factory):
    d = tmp_path_factory.mktemp("reg")
    rng = np.random.default_rng(1)
    X = rng.normal(size=(60, 4)).astype(np.float32)
    paths = {}
    for i in range(6):
        y = (X[:, 0] * (1 if i % 2 == 0 else -1) > 0).astype(int)     # even tenants and odd tenants disagree
        m = LogisticRegression().fit(X, y)
        p = d / f"t{i}.onnx"
        p.write_bytes(to_onnx(m, X[:1], target_opset=17, options={id(m): {"zipmap": False}}).SerializeToString())
        paths[f"t{i}"] = str(p)
    return paths

def test_lru_eviction(registry):
    mm = ModelManager(registry.__getitem__, max_models=3)
    for t in ["t0", "t1", "t2"]: mm.get(t)
    mm.get("t0")                       # t0 is now most recent, t1 is the oldest
    mm.get("t3")                       # forces one eviction
    assert mm.evictions == ["t1"]
    assert mm.cached() == ["t2", "t0", "t3"]
    mm.get("t1")                       # t1 comes back: a second (cold) load
    assert mm.loads["t1"] == 2 and len(mm.cached()) == 3

def test_no_double_load_under_concurrency(registry):
    mm = ModelManager(registry.__getitem__, max_models=3)
    barrier = threading.Barrier(16)
    got = []
    def worker():
        barrier.wait()
        got.append(mm.get("t4"))
    ts = [threading.Thread(target=worker) for _ in range(16)]
    [t.start() for t in ts]; [t.join() for t in ts]
    assert mm.loads["t4"] == 1                    # 16 threads, one load
    assert len({id(s) for s in got}) == 1         # everybody got the same session

def test_slow_load_does_not_block_other_tenants(registry):
    slow_started, release = threading.Event(), threading.Event()
    def lookup(t):
        if t == "t5": slow_started.set(); release.wait(5)   # simulate a slow download for t5 only
        return registry[t]
    mm = ModelManager(lookup, max_models=3)
    th = threading.Thread(target=lambda: mm.get("t5")); th.start()
    slow_started.wait(5)
    t0 = time.perf_counter(); mm.get("t0"); fast = time.perf_counter() - t0
    release.set(); th.join()
    assert fast < 1.0 and mm.loads["t5"] == 1 and mm.loads["t0"] == 1

def test_unknown_tenant_not_cached(registry):
    mm = ModelManager(registry.__getitem__, max_models=2)
    with pytest.raises(KeyError): mm.get("nope")
    assert mm.cached() == []

def test_predictions_are_per_tenant(registry):
    mm = ModelManager(registry.__getitem__, max_models=2)
    x = np.array([[2.0, 0, 0, 0]], dtype=np.float32)
    a = mm.get("t0").run(["label"], {"X": x})[0][0]; b = mm.get("t1").run(["label"], {"X": x})[0][0]
    assert a != b
