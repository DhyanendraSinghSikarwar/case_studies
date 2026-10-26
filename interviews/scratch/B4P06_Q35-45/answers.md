### Q35 ⭐⭐ 🟡 Training-serving skew and preprocessing in the serving path. Explain how skew appears (different tokenisers, different scaling, a missing category, a feature computed in SQL for training and in Python for serving, float precision), why the preprocessing should live inside the model artifact (a scikit-learn Pipeline exported to ONNX, a shared package imported by both training and serving) and not be re-implemented, and tests that catch it (parity on a held-out sample, a schema contract). Show a bug where serving forgets to scale features, the parity test that catches it, and the fix by exporting the whole Pipeline with skl2onnx. Run it for real and show the output. Part 8 owns drift monitoring and Part 9 feature stores.
**Asked at:** Model format and safety sources (scikit-learn model persistence docs, arxiv.org 2410.04490 on Hugging Face model exploits, labs.snyk.io deep-learning file format vulnerabilities, union.ai secure-AI post, ProtectAI ModelScan docs; search snippets only, not opened); docs and security write-ups, not interview reports; ML engineer and MLOps roles, security-aware teams
**Say this first (1 line):** Skew means training and serving compute the features differently, so the fix is one artifact: export the whole preprocessing plus model Pipeline as one ONNX file, and keep a parity test on held-out rows that fails the build if serving and training disagree.

**Then explain:**
- How skew shows up: a different tokeniser version, scaling done in training but forgotten in serving, a category that never appeared in training, a feature built in SQL for training and in Python for serving (different null handling or time zone), float64 in training and float32 in serving.
- It is silent. The API returns 200 and a plausible number. Accuracy dashboards (Part 8) only notice weeks later.
- Fix 1: preprocessing lives inside the artifact (a scikit-learn Pipeline exported with skl2onnx, or a shared package that both training and serving import). Nobody re-implements it.
- Fix 2: tests. A parity test (same held-out rows through the training object and the served artifact, compare labels exactly and probabilities with a tolerance) and a schema contract (column count, dtype, no NaN) checked at the edge.
- Failure modes of the fix: a custom transformer that skl2onnx cannot convert (then use the shared package route), a parity tolerance set so loose it hides a bug, and a held-out sample that never contains the rare category.
- Not here: drift monitoring is Part 8, feature stores are Part 9.

**Example:** Four features on very different scales (about 0.01 to 1000). Training pipeline = StandardScaler then LogisticRegression. Serving exports only the LogisticRegression and feeds raw values. A value like 5000 hits weights learned for values near 0, so the score saturates and about half the labels are wrong (the run shows 52 percent agreement, close to a coin flip on this balanced data). Exporting the whole pipeline gives 100 percent agreement.

**Code:** one Python file (run with `python3 -I`). Run with Python 3.13.17 in a venv: fastapi 0.162.0, uvicorn 0.54.0, httpx 0.28.1, pytest 9.1.1, scikit-learn 1.9.1, skl2onnx 1.20.0, onnxruntime 1.31.0, torch 2.14.1 (CPU only). Sandbox timings are machine-specific demos, not benchmarks.
```python
# Q35: serving forgets to scale; parity test catches it; fix = export the whole Pipeline.
import numpy as np, onnxruntime as ort
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from skl2onnx import to_onnx

X, y = make_classification(n_samples=600, n_features=4, n_informative=3, n_redundant=0, random_state=0)
X = (X * np.array([1, 50, 1000, 0.01]) + np.array([0, 300, 5000, 2])).astype(np.float32)  # very different scales
Xtr, ytr, Xho = X[:500], y[:500], X[500:]                                                  # held-out parity sample

pipe = Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression(max_iter=1000))]).fit(Xtr, ytr)
opt = lambda m: {id(m): {"zipmap": False}}

# BUG: only the classifier is exported; the scaler stays in the training notebook
bad = to_onnx(pipe.named_steps["clf"], Xtr[:1], target_opset=17, options=opt(pipe.named_steps["clf"]))
# FIX: the whole Pipeline is exported, scaler included
good = to_onnx(pipe, Xtr[:1], target_opset=17, options=opt(pipe.steps[-1][1]))

def serve_labels(onnx_model, X):
    s = ort.InferenceSession(onnx_model.SerializeToString(), providers=["CPUExecutionProvider"])
    return s.run(["label"], {"X": X})[0]

def parity(name, onnx_model):
    ref = pipe.predict(Xho)
    got = serve_labels(onnx_model, Xho)
    agree = float((ref == got).mean())
    print(f"{name}: agreement with training pipeline on {len(Xho)} held-out rows = {agree:.3f}")
    return agree

a_bad = parity("buggy serving (no scaler)", bad)
a_good = parity("fixed serving (whole Pipeline)", good)
assert a_bad < 1.0 and a_good == 1.0

# probability parity with a tolerance (float32 vs float64 maths)
s = ort.InferenceSession(good.SerializeToString(), providers=["CPUExecutionProvider"])
p_onnx = s.run(["probabilities"], {"X": Xho})[0]
print("max |proba diff| fixed vs sklearn < 1e-4:", float(np.abs(p_onnx - pipe.predict_proba(Xho)).max()) < 1e-4)

# schema contract: refuse inputs the model was not trained on
CONTRACT = {"n_features": 4, "dtype": "float32"}
def check_contract(arr):
    if arr.ndim != 2 or arr.shape[1] != CONTRACT["n_features"]: raise ValueError(f"expected (n,4), got {arr.shape}")
    if str(arr.dtype) != CONTRACT["dtype"]: raise ValueError(f"expected float32, got {arr.dtype}")
    if not np.isfinite(arr).all(): raise ValueError("NaN or inf in input")
nan_arr = Xho[:2].copy(); nan_arr[0, 0] = np.nan
for name, arr in [("ok", Xho[:2]), ("3 columns", Xho[:2, :3]), ("float64", Xho[:2].astype(np.float64)), ("NaN", nan_arr)]:
    try: check_contract(arr); print("contract", name, "-> pass")
    except ValueError as e: print("contract", name, "-> reject:", e)
```
```bash
cd /tmp/claude-0/b6_q35_45 && /tmp/claude-0/b6p06/v/bin/python -I q35_skew.py
```

**Output (my run):** real run.
```text
buggy serving (no scaler): agreement with training pipeline on 100 held-out rows = 0.520
fixed serving (whole Pipeline): agreement with training pipeline on 100 held-out rows = 1.000
max |proba diff| fixed vs sklearn < 1e-4: True
contract ok -> pass
contract 3 columns -> reject: expected (n,4), got (2, 3)
contract float64 -> reject: expected float32, got float64
contract NaN -> reject: NaN or inf in input
```

**Follow-ups:**
- Why a tolerance for probabilities but exact match for labels? ONNX runs float32 and sklearn runs float64, so probabilities differ in the last digits. Labels should match exactly except for rows right at the 0.5 boundary; pick the tolerance on purpose and write it down.
- What if the transformer cannot be exported? Put the preprocessing in a small package, pin its version, import it in both the training job and the service, and run the same parity test.
- Where does the schema contract live? At the API edge (pydantic or the check above) and in the model signature in the registry (Part 4).

**Common mistakes:**
- Exporting only the final estimator and "doing the scaling in the service".
- A parity test on training rows only (the scaler saw them, so it hides bugs). Use held-out rows plus a few edge rows (unknown category, missing values).
- Comparing float probabilities with `==`.
- Forgetting that a retrained model needs a retrained scaler: they ship together or not at all.

---

### Q36 ⭐ 🔴 Multi-model serving: hosting dozens or thousands of models (one per customer or region) behind one service. Cover the model registry lookup, a bounded LRU cache of loaded models with eviction, lazy loading with per-model locks, memory accounting, cold-start latency for a rarely used model, routing by tenant id, Triton model control and KServe ModelMesh at concept level (check current docs), and noisy-neighbour isolation. Write a Python model manager with an LRU of ONNX sessions limited by count, thread-safe loading, and tests that show eviction and no double load under concurrency. Run it for real. Triton and ModelMesh are not executed.
**Asked at:** Triton write-ups (apxml.com serving models with Triton, reintech.io Triton deep dive, oneuptime.com Triton posts 2026, softwaremill.com Triton tips and tricks, a 2025 academia.edu FastAPI-versus-Triton benchmark note; search snippets only, not opened); tutorials and one small benchmark note, not interview reports, check NVIDIA docs; GPU serving and ML platform roles
**Say this first (1 line):** Keep a bounded LRU of loaded sessions, load lazily on first request under a per-model lock so two callers never load the same model twice, and look the file up in the registry by tenant id.

**Then explain:**
- Flow: tenant id from the request, registry lookup (tenant to model version to artifact path), cache hit returns the session, cache miss loads under that tenant's lock, then the LRU evicts the oldest if over the limit.
- Two locks: one short global lock for the dict, one lock per model for the slow load. A single global lock would make one slow download block every tenant. The code re-checks the cache after getting the per-model lock (double-checked locking), which is what stops the double load.
- Memory: a count limit is the simple version. Real services also track bytes per model (file size is a rough guide, measure resident memory) and evict until under budget. Count limits fail when one model is 100 times bigger than the rest.
- Cold start: the first request for a rarely used tenant pays download plus session creation. Mitigate with a warm list for top tenants, a pre-fetch to local disk, and a timeout so the caller gets a clear 503 or a fallback instead of hanging.
- Noisy neighbour: one tenant with a huge request rate can evict everyone else (cache thrash) and eat CPU. Use per-tenant rate limits and a concurrency cap, or give big tenants dedicated replicas. Route by tenant id with consistent hashing so the same tenant lands on the same replica and the cache stays warm.
- Concept only, not executed: Triton has model control (explicit load and unload through its repository API, check current docs) and KServe ModelMesh packs many models into shared pods and loads/evicts them on demand (check current docs for status and setup).

**Example:** Capacity 3. Calls: t0, t1, t2 (cache = t0 t1 t2), t0 again (t0 becomes newest, t1 is now oldest), t3. Cache would hold 4, so t1 is evicted: cache = t2 t0 t3. Asking for t1 again is a fresh, slow load and evicts t2. The test asserts exactly this order.

**Code:** the manager, five pytest tests (eviction order, 16 threads and one load, a slow load for one tenant not blocking another, unknown tenant, per-tenant predictions) and a small cold-versus-warm timing. Run with Python 3.13.17 in a venv: fastapi 0.162.0, uvicorn 0.54.0, httpx 0.28.1, pytest 9.1.1, scikit-learn 1.9.1, skl2onnx 1.20.0, onnxruntime 1.31.0, torch 2.14.1 (CPU only). Sandbox timings are machine-specific demos, not benchmarks.
```python
# ===== q36_manager.py =====
# Q36: bounded LRU of ONNX sessions, lazy load, per-model locks, no double load.
import threading, time
from collections import OrderedDict
import onnxruntime as ort

class ModelManager:
    def __init__(self, registry_lookup, max_models=3):
        self.lookup = registry_lookup            # tenant -> path of .onnx (the "registry")
        self.max_models = max_models
        self._cache = OrderedDict()              # tenant -> session, oldest first
        self._lock = threading.Lock()            # protects _cache and _locks only (short holds)
        self._locks = {}                         # tenant -> lock held during that tenant's load
        self.loads = {}                          # tenant -> times loaded (for tests)
        self.evictions = []

    def get(self, tenant):
        with self._lock:
            if tenant in self._cache:
                self._cache.move_to_end(tenant)  # mark most recently used
                return self._cache[tenant]
            tlock = self._locks.setdefault(tenant, threading.Lock())
        with tlock:                              # only callers for THIS tenant wait here
            with self._lock:                     # someone may have loaded it while we waited
                if tenant in self._cache:
                    self._cache.move_to_end(tenant)
                    return self._cache[tenant]
            path = self.lookup(tenant)           # KeyError -> unknown tenant, nothing cached
            sess = ort.InferenceSession(path, providers=["CPUExecutionProvider"])  # slow part, outside the global lock
            with self._lock:
                self.loads[tenant] = self.loads.get(tenant, 0) + 1
                self._cache[tenant] = sess
                while len(self._cache) > self.max_models:
                    old, _ = self._cache.popitem(last=False)   # evict least recently used
                    self.evictions.append(old)
            return sess

    def cached(self):
        with self._lock:
            return list(self._cache)

# ===== test_q36_manager.py =====
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

# ===== q36_cold.py =====
import sys,time,tempfile,pathlib; sys.path.insert(0,"/home/user/case_studies/interviews/scratch/B4P06_Q35-45/code")
import numpy as np
from sklearn.linear_model import LogisticRegression
from skl2onnx import to_onnx
from q36_manager import ModelManager
X=np.random.default_rng(0).normal(size=(50,4)).astype(np.float32); m=LogisticRegression().fit(X,(X[:,0]>0).astype(int))
d=pathlib.Path(tempfile.mkdtemp()); p=d/"m.onnx"; p.write_bytes(to_onnx(m,X[:1],target_opset=17,options={id(m):{"zipmap":False}}).SerializeToString())
mm=ModelManager(lambda t:str(p),2)
t=time.perf_counter(); s=mm.get("a"); cold=time.perf_counter()-t
t=time.perf_counter(); mm.get("a"); warm=time.perf_counter()-t
t=time.perf_counter(); s.run(None,{"X":X[:1]}); inf=time.perf_counter()-t
print(f"cold get {cold*1000:.2f} ms, cached get {warm*1000:.4f} ms, one inference {inf*1000:.3f} ms (this sandbox only)")
```
```bash
cd /tmp/claude-0/b6_q35_45 && /tmp/claude-0/b6p06/v/bin/python -m pytest -q -p no:cacheprovider test_q36_manager.py
/tmp/claude-0/b6p06/v/bin/python -I q36_cold.py
```

**Output (my run):** real run for the manager and tests. Triton model control and ModelMesh are not executed (no Triton server, no Kubernetes here).
```text
.....                                                                    [100%]
5 passed in 1.85s
cold get 4.05 ms, cached get 0.0066 ms, one inference 0.502 ms (this sandbox only)
```

**Follow-ups:**
- How do you stop a thundering herd after a restart? Warm the top tenants at startup before readiness turns green, and keep the per-model lock so a burst still loads once.
- Evict a model that is serving a request right now? The session object stays alive while a request holds a reference, so eviction only removes it from the dict. Memory frees when the last request finishes.
- Thousands of models: is ONNX Runtime per model still fine? Each session costs memory, so load on demand, keep the cache small, and consider tools built for this (Triton, ModelMesh) after checking current docs.

**Common mistakes:**
- One global lock held during the load (all tenants wait on one slow download).
- No re-check after getting the per-model lock (16 threads, 16 loads).
- Caching a failed load, or letting an unknown tenant fill the cache.
- Unbounded dict "because models are small" (it works until the 500th tenant).
- Evicting by age only, not by use.

---

### Q37 ⭐ 🔴 Implement weighted traffic splitting and a mirror (shadow) path in your own gateway. Explain deterministic assignment by hashing a user id so a user does not flip between versions, sticky ramp-ups (5 to 25 to 100 percent) that only move users in one direction, sending a copy of the request to the shadow model without waiting for it (fire and forget with a timeout, so shadow latency never touches the caller), comparing outputs, and automatic rollback on error or p99 breach. Write the router in FastAPI with httpx.AsyncClient calling two local model apps, run the three apps on localhost, and show the observed split, shadow agreement and caller latency. Service meshes and KServe canary are not executed.
**Asked at:** Deployment-strategy guides (techinterview.org 'ML model serving system low-level design: versioned deployment, A/B testing, shadow mode', seldon.io 'Essential guide to ML model serving strategies', qwak.com A/B testing ML models; search snippets only, not opened); vendor and editorial pages, thresholds are examples; MLOps and ML platform roles
**Say this first (1 line):** Hash the user id into a stable bucket 0 to 99, send buckets below the canary percent to the new version, copy each request to the shadow model as a background task with a timeout, and roll back automatically on error rate or p99.

**Then explain:**
- Deterministic assignment: `sha256(user_id) % 100` gives each user a fixed bucket. Python's built-in `hash()` is randomised per process, so never use it. Same user, same bucket, same version.
- Sticky ramp: the rule is `bucket < percent`. Going 5 to 25 to 100 only adds users to the canary, nobody moves back. The gateway ignores a lower percent unless a rollback sets the flag (the run shows 0 users moved).
- Shadow (mirror): after the main answer is ready, start `asyncio.create_task` for the shadow call with its own short timeout. The caller never awaits it, so shadow latency cannot touch the caller. Keep task references so they are not garbage collected, and count timeouts. Shadow output is only compared and logged, never returned.
- Rollback: keep a sliding window of recent canary calls. If the error rate or p99 passes a limit (after a minimum sample count), set `rolled_back` and everyone goes to stable. Callers also get a fallback to stable for the failed call.
- Failure modes: the shadow model has side effects (writes, emails) so it must be side-effect free; mirror load doubles traffic to the shadow; a hash on a field with few values gives uneven splits (observed share is 3.9 percent for a 5 percent target on 1,000 users, which is normal sampling noise); the p99 limit on a tiny window is noisy.
- Not executed: Istio or Envoy traffic splitting and KServe canary (check current docs).

**Example:** User `user17` has bucket 42, say. At 5 percent: stable. At 25 percent: stable (42 is not below 25). At 100 percent: canary. Once on canary, the user stays on canary for every later step. A user with bucket 3 is on canary at 5, 25 and 100 percent.

**Code:** three files: a stand-in model app (v1, v2, shadow), the gateway, and a driver that starts everything on ports 8401 to 8404, runs the demo and stops all servers. Run with Python 3.13.17 in a venv: fastapi 0.162.0, uvicorn 0.54.0, httpx 0.28.1, pytest 9.1.1, scikit-learn 1.9.1, skl2onnx 1.20.0, onnxruntime 1.31.0, torch 2.14.1 (CPU only). Sandbox timings are machine-specific demos, not benchmarks.
```python
# ===== q37_model_app.py =====
# Tiny stand-in model server. VERSION, DELAY_MS and the /admin/break toggle come from the environment/requests.
import os, asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
VERSION = os.environ.get("VERSION", "v1"); DELAY = float(os.environ.get("DELAY_MS", "2")) / 1000
state = {"broken": False}
app = FastAPI()
class Req(BaseModel): x: float
@app.post("/predict")
async def predict(r: Req):
    await asyncio.sleep(DELAY)
    if os.environ.get("SLOW_TAIL") and r.x >= 0.95: await asyncio.sleep(0.4)   # about 5 percent of calls are very slow
    if state["broken"]: raise HTTPException(500, "model crashed")
    # v2 differs from v1 for inputs in [0.9, 1.0): about 10 percent of uniform inputs
    label = int(r.x > 0.5) if not (VERSION == "v2" and r.x >= 0.9) else 0
    return {"version": VERSION, "label": label}
@app.post("/admin/break")
async def brk(): state["broken"] = True; return {"broken": True}

# ===== q37_gateway.py =====
# Gateway: deterministic hash split, sticky ramp, fire-and-forget shadow, automatic rollback.
import asyncio, hashlib, os, time
from collections import deque
import httpx
from fastapi import FastAPI

STABLE, CANARY, SHADOW = os.environ["STABLE_URL"], os.environ["CANARY_URL"], os.environ["SHADOW_URL"]
SHADOW_TIMEOUT = 0.15
state = {"percent": 5, "rolled_back": False, "mirror_sent": 0, "mirror_done": 0, "mirror_agree": 0, "mirror_timeout": 0, "mirror_err": 0}
canary_lat, canary_err = deque(maxlen=50), deque(maxlen=50)     # recent canary calls
P99_LIMIT, ERR_LIMIT, MIN_SAMPLES = 0.200, 0.2, 20
tasks = set()                                                    # keep refs so tasks are not garbage collected

def bucket(user_id: str) -> int:                                  # stable 0..99 per user; does not depend on PYTHONHASHSEED
    return int.from_bytes(hashlib.sha256(user_id.encode()).digest()[:8], "big") % 100

def use_canary(user_id: str) -> bool:
    return (not state["rolled_back"]) and bucket(user_id) < state["percent"]   # same bucket, bigger percent: users only move stable -> canary

async def mirror(client, body, primary_label):
    state["mirror_sent"] += 1
    try:
        r = await client.post(SHADOW + "/predict", json=body, timeout=SHADOW_TIMEOUT)
        state["mirror_done"] += 1
        state["mirror_agree"] += int(r.json()["label"] == primary_label)
    except httpx.TimeoutException: state["mirror_timeout"] += 1
    except Exception: state["mirror_err"] += 1

def check_rollback():
    if len(canary_err) < MIN_SAMPLES: return
    err_rate = sum(canary_err) / len(canary_err)
    p99 = sorted(canary_lat)[int(0.99 * (len(canary_lat) - 1))]
    if err_rate > ERR_LIMIT or p99 > P99_LIMIT: state["rolled_back"] = True

app = FastAPI()
@app.on_event("startup")
async def _s(): app.state.client = httpx.AsyncClient()
@app.post("/predict")
async def predict(body: dict):
    c = app.state.client; uid = str(body["user_id"])
    to_canary = use_canary(uid); url = CANARY if to_canary else STABLE
    t = time.perf_counter()
    try:
        r = await c.post(url + "/predict", json={"x": body["x"]}, timeout=2.0); ok = r.status_code == 200
    except Exception: ok = False
    dt = time.perf_counter() - t
    if to_canary:
        canary_lat.append(dt); canary_err.append(0 if ok else 1); check_rollback()
        if not ok:                                               # caller still gets an answer: fall back to stable
            r = await c.post(STABLE + "/predict", json={"x": body["x"]}, timeout=2.0)
    if not ok and not to_canary: return {"error": "stable failed"}
    out = r.json()
    if SHADOW:                                                   # fire and forget: caller never awaits this
        t_ = asyncio.create_task(mirror(c, {"x": body["x"]}, out["label"])); tasks.add(t_); t_.add_done_callback(tasks.discard)
    return {**out, "routed": "canary" if to_canary else "stable"}
@app.post("/admin/percent/{p}")
async def set_percent(p: int): state["percent"] = max(state["percent"], p) if p >= state["percent"] else state["percent"]; return state   # ramp only goes up
@app.get("/admin/state")
async def get_state(): return {**state, "canary_p99_recent": (sorted(canary_lat)[int(0.99*(len(canary_lat)-1))] if canary_lat else None)}

# ===== q37_run.py =====
# Starts 3 apps (stable 8401, canary 8402, shadow 8403) + gateway 8404, runs the demo, stops everything.
import os, subprocess, sys, time, random, statistics, pathlib
import httpx
HERE = str(pathlib.Path(__file__).parent); PY = sys.executable; procs = []
def start(mod, port, **env):
    p = subprocess.Popen([PY, "-m", "uvicorn", f"{mod}:app", "--port", str(port), "--log-level", "warning", "--app-dir", HERE],
                         env={**os.environ, **env}); procs.append(p)
def wait(port):
    for _ in range(100):
        try: httpx.get(f"http://127.0.0.1:{port}/openapi.json", timeout=1); return
        except Exception: time.sleep(0.1)
    raise RuntimeError(port)
try:
    start("q37_model_app", 8401, VERSION="v1", DELAY_MS="2")
    start("q37_model_app", 8402, VERSION="v2", DELAY_MS="2")
    start("q37_model_app", 8403, VERSION="v2", DELAY_MS="20", SLOW_TAIL="1")   # shadow: 20 ms, but 5% of calls take 400 ms+
    start("q37_gateway", 8404, STABLE_URL="http://127.0.0.1:8401", CANARY_URL="http://127.0.0.1:8402", SHADOW_URL="http://127.0.0.1:8403")
    for p in (8401, 8402, 8403, 8404): wait(p)
    G = "http://127.0.0.1:8404"; c = httpx.Client(timeout=10); rng = random.Random(7)
    users = [f"user{i}" for i in range(1000)]
    def sweep(label):
        routed = {}; lat = []
        for u in users:
            t = time.perf_counter(); r = c.post(G + "/predict", json={"user_id": u, "x": rng.random()}).json(); lat.append(time.perf_counter() - t)
            routed[u] = r["routed"]
        n = sum(v == "canary" for v in routed.values()); print(f"{label}: canary share = {n/len(users):.1%} of 1000 users, caller p50 {statistics.median(lat)*1000:.1f} ms, p99 {sorted(lat)[989]*1000:.1f} ms")
        return routed
    r5 = sweep("5% step"); r5b = sweep("5% again (same users)")
    print("users who flipped between two sweeps at 5%:", sum(r5[u] != r5b[u] for u in users))
    c.post(G + "/admin/percent/25"); r25 = sweep("25% step")
    print("users on canary at 5% who left canary at 25%:", sum(r5[u] == "canary" and r25[u] != "canary" for u in users))
    c.post(G + "/admin/percent/100"); r100 = sweep("100% step")
    print("users on canary at 25% who left canary at 100%:", sum(r25[u] == "canary" and r100[u] != "canary" for u in users))
    c.post(G + "/admin/percent/10"); print("ramp-down request ignored, percent still:", c.get(G + "/admin/state").json()["percent"])
    time.sleep(1.0)
    s = c.get(G + "/admin/state").json()
    print(f"shadow: sent {s['mirror_sent']}, completed {s['mirror_done']}, timed out (150 ms cap) {s['mirror_timeout']}, agree {s['mirror_agree']}")
    # rollback: break the canary, then keep sending traffic
    httpx.post("http://127.0.0.1:8402/admin/break")
    codes = []
    for i in range(60):
        r = c.post(G + "/predict", json={"user_id": f"user{i}", "x": 0.3}); codes.append((r.status_code, r.json().get("routed")))
    s = c.get(G + "/admin/state").json()
    print("after breaking canary: rolled_back =", s["rolled_back"], "| HTTP statuses seen by callers:", sorted({c_[0] for c_ in codes}),
          "| last 10 routed to:", sorted({c_[1] for c_ in codes[-10:]}))
finally:
    for p in procs: p.terminate()
    for p in procs: p.wait(timeout=10)
    print("servers stopped:", all(p.poll() is not None for p in procs))
```
```bash
cd /tmp/claude-0/b6_q35_45 && /tmp/claude-0/b6p06/v/bin/python -I q37_run.py
```

**Output (my run):** real run (stable 8401, canary 8402, shadow 8403, gateway 8404; all stopped at the end). The p99 branch of the rollback rule is in the code but this run only exercised the error-rate branch. Latencies are machine-specific.
```text
5% step: canary share = 3.9% of 1000 users, caller p50 6.4 ms, p99 13.7 ms
5% again (same users): canary share = 3.9% of 1000 users, caller p50 6.7 ms, p99 13.5 ms
users who flipped between two sweeps at 5%: 0
25% step: canary share = 23.8% of 1000 users, caller p50 7.0 ms, p99 15.0 ms
users on canary at 5% who left canary at 25%: 0
100% step: canary share = 100.0% of 1000 users, caller p50 7.3 ms, p99 16.2 ms
users on canary at 25% who left canary at 100%: 0
ramp-down request ignored, percent still: 100
shadow: sent 4000, completed 3808, timed out (150 ms cap) 192, agree 3677
after breaking canary: rolled_back = True | HTTP statuses seen by callers: [200] | last 10 routed to: ['stable']
servers stopped: True
```

**Follow-ups:**
- A/B test versus canary? A/B measures a business metric over time with a fixed split. Canary guards against breakage with a ramp and rollback. The mechanism (hash buckets) is the same.
- How would you compare shadow outputs for a regression model? Log both values and compare with a tolerance and a rank or error metric, not equality.
- Why not split in the load balancer? You can (service mesh), but per-user stickiness and shadow comparison are easier to control in the gateway. Check current docs for what your platform supports.

**Common mistakes:**
- Random per-request routing (a user flips between versions).
- `hash()` for bucketing (changes on restart).
- Awaiting the shadow call (shadow slowness becomes caller slowness).
- Shadow model with side effects.
- Rolling back on 3 failures out of 3 requests (no minimum sample).
- Ramp-down by lowering the percent, which moves users back and forth.

---

### Q38 ⭐ 🔴 Zero-downtime deploys and graceful shutdown of a model service. Explain rolling updates, readiness gating so traffic only reaches pods that have loaded the model, SIGTERM handling (stop accepting, finish in-flight requests, then exit), uvicorn's graceful shutdown timeout, a preStop sleep and terminationGracePeriodSeconds at concept level (Part 3 owns Kubernetes), connection draining at the load balancer, and in-flight batches during shutdown. Run a real uvicorn on localhost, start a slow request, send SIGTERM, and show that the in-flight request still completes and the process then exits. Kubernetes rolling updates are not executed.
**Asked at:** FastAPI docs and tutorials (fastapi.tiangolo.com advanced events/lifespan page, reintech.io 'FastAPI ML model serving production REST APIs', docs.truefoundry.com deploy-model-fastapi; search snippets only, not opened); docs and tutorials, not interview reports; ML engineer and MLOps roles that ship model APIs, including IT-services firms, product companies and GCCs
**Say this first (1 line):** On SIGTERM, uvicorn stops accepting new connections, lets in-flight requests finish up to a graceful timeout, runs lifespan shutdown and exits; Kubernetes adds readiness gating, a preStop sleep and a grace period that is longer than all of that.

**Then explain:**
- Rolling update: new pods start, old pods are removed only when new ones are Ready. Readiness must mean "model loaded". uvicorn only starts listening after the lifespan startup finishes, so while the model loads the port refuses connections and the probe fails (in the run, the first successful answer was already 200).
- SIGTERM sequence in uvicorn: close the listening socket (new connections are refused, as the run shows), wait for open connections, then run lifespan shutdown. `--timeout-graceful-shutdown N` caps the wait. After N seconds the remaining tasks are cancelled and the caller gets an error (second trial).
- Kubernetes (concept, not executed, Part 3 owns it): the pod is marked terminating and removed from Service endpoints at about the same time SIGTERM is sent, but load balancers lag. A `preStop` sleep (a few seconds) gives them time to stop sending traffic. `terminationGracePeriodSeconds` must be larger than preStop plus the uvicorn timeout, otherwise SIGKILL arrives mid-request.
- In-flight batches: a dynamic batcher must flush or finish its current batch on shutdown, and refuse to start new ones. Long jobs need a timeout shorter than the grace period or they get killed.
- Exit code: the run shows -15 (uvicorn re-raises the signal), which is normal here.

**Example:** Request needs 2 s. SIGTERM at t=0.5 s. With a 10 s window: new connections are refused immediately, the old request finishes at about t=2 s, the process exits about 1.6 s after SIGTERM. With a 1 s window and a 4 s request: the request is cancelled at about 1 s and the caller gets a 500 style failure.

**Code:** a tiny app with a slow endpoint, a driver that starts real uvicorn on port 8405, sends a slow request, sends SIGTERM and records what happens, and a Kubernetes pod-spec fragment checked with pyyaml (the fragment is not applied anywhere). Run with Python 3.13.17 in a venv: fastapi 0.162.0, uvicorn 0.54.0, httpx 0.28.1, pytest 9.1.1, scikit-learn 1.9.1, skl2onnx 1.20.0, onnxruntime 1.31.0, torch 2.14.1 (CPU only). Sandbox timings are machine-specific demos, not benchmarks.
```python
# ===== q38_app.py =====
import asyncio, os, time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
ready = {"ok": False}
@asynccontextmanager
async def lifespan(app):
    await asyncio.sleep(0.5)                 # pretend to load the model
    ready["ok"] = True
    yield
    print("lifespan shutdown: closing resources", flush=True)   # runs after in-flight requests finished
app = FastAPI(lifespan=lifespan)
@app.get("/readyz")
async def readyz(r: Response):
    if not ready["ok"]: r.status_code = 503
    return {"ready": ready["ok"]}
@app.post("/slow")
async def slow(seconds: float = 3.0):
    await asyncio.sleep(seconds)             # stands in for a long inference or a batch in flight
    return {"done": True, "finished_at": time.time()}

# ===== q38_run.py =====
import os, signal, subprocess, sys, threading, time, pathlib, httpx
HERE = str(pathlib.Path(__file__).parent); PORT = 8405
def launch(extra):
    return subprocess.Popen([sys.executable, "-m", "uvicorn", "q38_app:app", "--port", str(PORT), "--app-dir", HERE, "--log-level", "info", *extra],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
def wait_ready(p):
    for _ in range(100):
        try:
            if httpx.get(f"http://127.0.0.1:{PORT}/readyz", timeout=1).status_code == 200: return
        except Exception: pass
        time.sleep(0.1)
    raise RuntimeError("not ready")
def trial(name, extra, slow_seconds):
    p = launch(extra)
    try:
        # readiness: 503 while loading, then 200
        t0 = time.time(); first = None
        while True:
            try: first = httpx.get(f"http://127.0.0.1:{PORT}/readyz", timeout=1).status_code; break
            except Exception: time.sleep(0.02)
        print(f"[{name}] first /readyz answer right after start: {first}")
        wait_ready(p)
        res = {}
        def call():
            try: res["r"] = httpx.post(f"http://127.0.0.1:{PORT}/slow", params={"seconds": slow_seconds}, timeout=30).json()
            except Exception as e: res["err"] = type(e).__name__
        th = threading.Thread(target=call); th.start(); time.sleep(0.5)
        t_term = time.time(); p.send_signal(signal.SIGTERM)
        time.sleep(0.3)
        try: httpx.get(f"http://127.0.0.1:{PORT}/readyz", timeout=1); new = "accepted"
        except Exception as e: new = "refused (" + type(e).__name__ + ")"
        th.join(); rc = p.wait(timeout=20); t_exit = time.time()
        out = p.stdout.read()
        print(f"[{name}] new request after SIGTERM: {new}")
        print(f"[{name}] in-flight request: {res}  (slow request asked for {slow_seconds}s)")
        print(f"[{name}] exit code {rc}, exited {t_exit - t_term:.2f}s after SIGTERM")
        print(f"[{name}] relevant log lines:", [l.strip() for l in out.splitlines() if any(k in l for k in ("Shutting", "Waiting", "lifespan", "Finished", "Cancel", "cancel"))])
    finally:
        if p.poll() is None: p.kill()
trial("graceful 10s window", ["--timeout-graceful-shutdown", "10"], 2.0)
trial("window too short (1s)", ["--timeout-graceful-shutdown", "1"], 4.0)

# ===== q38_check_yaml.py =====
import yaml, pathlib
d = yaml.safe_load(open(pathlib.Path(__file__).with_name("q38_k8s_fragment.yaml")))["spec"]
c = d["containers"][0]; grace = d["terminationGracePeriodSeconds"]
pre = int(c["lifecycle"]["preStop"]["exec"]["command"][1]); uv = int(c["command"][c["command"].index("--timeout-graceful-shutdown") + 1])
print("YAML parses; grace", grace, "| preStop sleep", pre, "| uvicorn graceful timeout", uv, "| budget ok (pre + uvicorn < grace):", pre + uv < grace)
assert pre + uv < grace and "readinessProbe" in c
```
```yaml
# Pod spec fragment (concept; NOT applied to any cluster). Part 3 owns Kubernetes.
spec:
  terminationGracePeriodSeconds: 45        # must be > preStop sleep + uvicorn graceful timeout
  containers:
    - name: model
      image: registry.example/model:1.4.0
      command: ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-graceful-shutdown", "25"]
      readinessProbe: {httpGet: {path: /readyz, port: 8000}, periodSeconds: 5, failureThreshold: 2}
      livenessProbe:  {httpGet: {path: /livez,  port: 8000}, periodSeconds: 10, failureThreshold: 3}
      lifecycle:
        preStop: {exec: {command: ["sleep", "10"]}}   # let endpoints/load balancer stop sending traffic first
```
```bash
cd /tmp/claude-0/b6_q35_45 && /tmp/claude-0/b6p06/v/bin/python -I q38_run.py
/tmp/claude-0/b6p06/v/bin/python -I q38_check_yaml.py
```

**Output (my run):** real run of uvicorn on localhost (second trial shows the window being too short). Kubernetes rolling update, preStop and load-balancer draining are not executed; the validation that did run is the YAML parse and the time-budget check at the end.
```text
[graceful 10s window] first /readyz answer right after start: 200
[graceful 10s window] new request after SIGTERM: refused (ConnectError)
[graceful 10s window] in-flight request: {'r': {'done': True, 'finished_at': 1793032677.6631048}}  (slow request asked for 2.0s)
[graceful 10s window] exit code -15, exited 1.61s after SIGTERM
[graceful 10s window] relevant log lines: ['INFO:     Waiting for application startup.', 'INFO:     Shutting down', 'INFO:     Waiting for connections to close. (CTRL+C to force quit)', 'INFO:     Waiting for application shutdown.', 'lifespan shutdown: closing resources', 'INFO:     Finished server process [2891]']
[window too short (1s)] first /readyz answer right after start: 200
[window too short (1s)] new request after SIGTERM: refused (ConnectError)
[window too short (1s)] in-flight request: {'err': 'JSONDecodeError'}  (slow request asked for 4.0s)
[window too short (1s)] exit code -15, exited 1.15s after SIGTERM
[window too short (1s)] relevant log lines: ['INFO:     Waiting for application startup.', 'INFO:     Shutting down', 'INFO:     Waiting for connections to close. (CTRL+C to force quit)', 'ERROR:    Cancel 1 running task(s), timeout graceful shutdown exceeded', 'INFO:     Waiting for application shutdown.', 'asyncio.exceptions.CancelledError: Task cancelled, timeout graceful shutdown exceeded', 'lifespan shutdown: closing resources', 'INFO:     Finished server process [2897]']
YAML parses; grace 45 | preStop sleep 10 | uvicorn graceful timeout 25 | budget ok (pre + uvicorn < grace): True
```

**Follow-ups:**
- Why a preStop sleep if the app handles SIGTERM? Because endpoint removal and SIGTERM race. Without the sleep, some traffic still arrives after the app stopped listening.
- What about --workers? The parent process forwards the signal and workers drain; test it with your real settings.
- WebSockets or streaming? Those connections can outlive the timeout, so close them with a message and let the client reconnect.

**Common mistakes:**
- Grace period shorter than the longest request.
- Readiness that returns 200 before the model is loaded.
- Using SIGKILL (`docker kill`) in tests, then thinking shutdown works.
- A preStop sleep with no matching increase of terminationGracePeriodSeconds.
- Ignoring in-flight batches.

---

### Q39 ⭐ 🔴 Security of a model API. Cover authentication (API keys, JWT or mutual TLS at the gateway), authorisation per model, rate limiting per key, input size and shape limits against denial of service (a huge JSON array, a pathological image), never accepting a pickle or joblib upload, model supply-chain checks (hash and signature of artifacts, scanning with a model scanner), secrets handling, logging without PII, and model extraction through unlimited queries at concept level. Show a FastAPI dependency that checks an API key with constant-time compare, a body-size limit, a per-key token-bucket rate limiter, and tests that exercise 401, 413 and 429. Run it with TestClient. Penetration testing and a WAF are not executed.
**Asked at:** Model format and safety sources (scikit-learn model persistence docs, arxiv.org 2410.04490 on Hugging Face model exploits, labs.snyk.io deep-learning file format vulnerabilities, union.ai secure-AI post, ProtectAI ModelScan docs; search snippets only, not opened); docs and security write-ups, not interview reports; ML engineer and MLOps roles, security-aware teams
**Say this first (1 line):** Put the checks in dependencies: hash and constant-time compare the API key, cap the body size while streaming, charge a per-key token bucket, check the key may use this model, and never accept pickle or joblib from outside.

**Then explain:**
- Authentication at the gateway: API keys for services, JWT for user identity, mutual TLS inside a mesh. Store only hashes of keys, compare with `hmac.compare_digest` so timing does not leak the key. Real keys come from a secret manager, never from code or logs.
- Authorisation per model: a valid key is not enough. The key carries the models it can call (the test shows 403).
- Rate limit per key: a token bucket (capacity and refill rate) gives a burst allowance and a steady rate. Return 429 with Retry-After. In production the counter lives in a shared store (Redis; not executed here) so all replicas agree; in-process is per replica only.
- Input limits: a huge JSON array or a decompression bomb costs CPU and memory. Limit body bytes (also for chunked uploads with no Content-Length, which the test covers), array length and image dimensions, and validate before inference. A WAF or reverse proxy should also cap sizes.
- Supply chain: never load a pickle or joblib file from a user or an unverified place (loading can run arbitrary code). Prefer ONNX or safetensors, check a SHA-256 and a signature of every artifact, and scan model files with a model scanner (check current tools). Log request ids and hashes, not raw inputs, so logs hold no PII.
- Model extraction: unlimited queries let someone copy your model. Per-key quotas, no probability vectors if labels are enough, and anomaly alerts. Concept only.

**Example:** Bucket capacity 3, refill 1 token per second. Five fast calls: 200, 200, 200, 429, 429. After 2 seconds of fake clock time two tokens are back: 200, 200, 429. A 5,000-number body is over the 2,000-byte cap: 413. Missing or wrong key: 401. alice calling bob's model: 403.

**Code:** the secured app (note the body limit is a dependency that also reads chunked bodies) and eight tests using FastAPI TestClient with an injectable fake clock. Run with Python 3.13.17 in a venv: fastapi 0.162.0, uvicorn 0.54.0, httpx 0.28.1, pytest 9.1.1, scikit-learn 1.9.1, skl2onnx 1.20.0, onnxruntime 1.31.0, torch 2.14.1 (CPU only). Sandbox timings are machine-specific demos, not benchmarks.
```python
# ===== q39_secure_api.py =====
import hmac, time, hashlib
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, Field

# Keys are stored as sha256 hashes (never plain). Demo values only; real keys come from a secret manager.
KEYS = {hashlib.sha256(b"key-alice").hexdigest(): {"name": "alice", "models": {"iris"}},
        hashlib.sha256(b"key-bob").hexdigest(): {"name": "bob", "models": {"fraud"}}}
MAX_BODY = 2_000          # bytes
MAX_FEATURES = 4

class Bucket:
    """Token bucket: `capacity` tokens, refilled at `rate` per second. clock is injectable for tests."""
    def __init__(self, capacity, rate, clock=time.monotonic):
        self.capacity, self.rate, self.clock = capacity, rate, clock; self.tokens, self.last = capacity, clock()
    def allow(self):
        now = self.clock(); self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate); self.last = now
        if self.tokens >= 1: self.tokens -= 1; return True
        return False

def make_app(clock=time.monotonic, capacity=3, rate=1.0):
    app = FastAPI(); buckets = {}

    async def limit_body(request: Request):
        cl = request.headers.get("content-length")
        if cl is not None and int(cl) > MAX_BODY: raise HTTPException(413, "body too large")
        body = b""
        async for chunk in request.stream():          # also covers chunked uploads with no Content-Length
            body += chunk
            if len(body) > MAX_BODY: raise HTTPException(413, "body too large")
        request.state.body = body

    def auth(x_api_key: str = Header(default="")):
        h = hashlib.sha256(x_api_key.encode()).hexdigest()
        for stored, info in KEYS.items():              # compare against every key, constant time per compare
            if hmac.compare_digest(h, stored): return info
        raise HTTPException(401, "invalid api key", headers={"WWW-Authenticate": "ApiKey"})

    def rate_limit(user=Depends(auth)):
        b = buckets.setdefault(user["name"], Bucket(capacity, rate, clock))
        if not b.allow(): raise HTTPException(429, "rate limit", headers={"Retry-After": "1"})
        return user

    class Features(BaseModel): features: list[float] = Field(min_length=MAX_FEATURES, max_length=MAX_FEATURES)

    @app.post("/v1/models/{model}/predict", dependencies=[Depends(limit_body)])
    async def predict(model: str, request: Request, user=Depends(rate_limit)):
        if model not in user["models"]: raise HTTPException(403, "key not allowed for this model")   # per-model authorisation
        try: f = Features.model_validate_json(request.state.body)
        except Exception: raise HTTPException(422, "bad payload")
        return {"model": model, "score": sum(f.features) / 4}      # stand-in for the model
    return app

# ===== test_q39_secure_api.py =====
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent))
import warnings; warnings.filterwarnings("ignore")
from fastapi.testclient import TestClient
from q39_secure_api import make_app
GOOD = {"features": [1, 2, 3, 4]}
class Clock:
    t = 0.0
    def __call__(self): return self.t

def client(clock=None, **kw): return TestClient(make_app(clock or Clock(), **kw))
H = lambda k: {"x-api-key": k}

def test_401_missing_and_wrong_key():
    c = client()
    assert c.post("/v1/models/iris/predict", json=GOOD).status_code == 401
    assert c.post("/v1/models/iris/predict", json=GOOD, headers=H("nope")).status_code == 401

def test_200_with_valid_key():
    assert client().post("/v1/models/iris/predict", json=GOOD, headers=H("key-alice")).json()["score"] == 2.5

def test_403_other_models_key():
    assert client().post("/v1/models/fraud/predict", json=GOOD, headers=H("key-alice")).status_code == 403

def test_413_big_body_with_content_length():
    r = client().post("/v1/models/iris/predict", json={"features": [1.0] * 5000}, headers=H("key-alice"))
    assert r.status_code == 413

def test_413_chunked_body_without_content_length():
    def gen():
        for _ in range(100): yield b" " * 100                # 10 KB streamed, no Content-Length
    r = client().post("/v1/models/iris/predict", content=gen(), headers=H("key-alice"))
    assert r.status_code == 413

def test_422_wrong_shape():
    assert client().post("/v1/models/iris/predict", json={"features": [1, 2]}, headers=H("key-alice")).status_code == 422

def test_429_then_refill():
    clk = Clock(); c = client(clk, capacity=3, rate=1.0)
    codes = [c.post("/v1/models/iris/predict", json=GOOD, headers=H("key-alice")).status_code for _ in range(5)]
    assert codes == [200, 200, 200, 429, 429]
    assert c.post("/v1/models/fraud/predict", json=GOOD, headers=H("key-bob")).status_code == 200   # bob has his own bucket
    clk.t += 2.0                                                  # two tokens refilled
    codes = [c.post("/v1/models/iris/predict", json=GOOD, headers=H("key-alice")).status_code for _ in range(3)]
    assert codes == [200, 200, 429]

def test_bad_key_does_not_spend_tokens():
    c = client(capacity=1)
    for _ in range(5): assert c.post("/v1/models/iris/predict", json=GOOD, headers=H("bad")).status_code == 401
    assert c.post("/v1/models/iris/predict", json=GOOD, headers=H("key-alice")).status_code == 200
```
```bash
cd /tmp/claude-0/b6_q35_45 && /tmp/claude-0/b6p06/v/bin/python -m pytest -v -p no:cacheprovider -W ignore test_q39_secure_api.py
```

**Output (my run):** real run with TestClient (no network port). Penetration testing, a WAF, mTLS, JWT validation and Redis-backed limits are not executed.
```text
collecting ... collected 8 items
../../..test_q39_secure_api.py::test_401_missing_and_wrong_key PASSED [ 12%]
../../..test_q39_secure_api.py::test_200_with_valid_key PASSED [ 25%]
../../..test_q39_secure_api.py::test_403_other_models_key PASSED [ 37%]
../../..test_q39_secure_api.py::test_413_big_body_with_content_length PASSED [ 50%]
../../..test_q39_secure_api.py::test_413_chunked_body_without_content_length PASSED [ 62%]
../../..test_q39_secure_api.py::test_422_wrong_shape PASSED [ 75%]
../../..test_q39_secure_api.py::test_429_then_refill PASSED [ 87%]
../../..test_q39_secure_api.py::test_bad_key_does_not_spend_tokens PASSED [100%]
============================== 8 passed in 0.45s ===============================
```

**Follow-ups:**
- Why hash stored keys? A database leak should not leak working keys. Use a slow hash or HMAC with a server secret if keys are low-entropy; random long keys are fine with SHA-256.
- Where is the rate limit best placed? At the gateway or ingress first (cheap), and a per-key limit in the app for fairness.
- How do you limit a pathological image? Cap bytes, cap width and height from the header before decoding, and decode in a worker with a timeout.

**Common mistakes:**
- Comparing keys with `==` (timing leak) or logging the key.
- Trusting Content-Length only (chunked bodies skip it).
- A rate limiter that counts failed-auth requests against the real key's bucket (the test checks it does not).
- `pickle.load` or `joblib.load` on an uploaded file.
- Logging full request bodies with personal data.

---

### Q40 ⭐ 🔴 Where does p99 latency come from, and how do you cut it? Cover queueing near saturation, dynamic-batching wait, garbage collection pauses, cold caches and lazy imports on first request, slow outliers from a noisy neighbour or CPU throttling (container CPU limits), large payload serialisation, connection setup without keep-alive, and slow dependencies. Remedies: warm-up requests, fixed concurrency limits, hedged requests at concept level, pre-allocation, keep-alive, profiling a trace. Write an experiment that injects a 2 percent slow-path into a local endpoint, shows p50 versus p99, and shows how a concurrency cap or a timeout-and-fallback changes the tail. Report numbers as machine-specific.
**Asked at:** Load-testing and latency sources (docs.databricks.com 'what is a load test' for model serving, tianpan.co 'Load testing LLM applications', loadforge.com guides, mintlify ml-in-production-practice module 6; search snippets only, not opened); docs and blogs, some promotional; serving and SRE-leaning ML roles
**Say this first (1 line):** p99 is mostly waiting, not computing: queues near saturation, slow outliers, pauses and cold paths; you cut it with warm-up, bounded queues, timeouts with a fallback, and by keeping load below saturation.

**Then explain:**
- Sources: queueing when utilisation is high (the biggest one), dynamic-batching wait, GC pauses, cold caches and lazy imports on the first call, CPU throttling from container CPU limits, a noisy neighbour, big payload serialisation, new TCP/TLS connections without keep-alive, and slow dependencies (feature store, database).
- Why p50 hides it: a 2 percent slow path never moves the median but sets p99 almost by itself.
- Remedies: warm-up requests before readiness, fixed concurrency limits with load shedding (503 fast beats waiting 800 ms), client timeout plus a cheap fallback, keep-alive, pre-allocated buffers, and profile a trace of the slow requests to find the cause. Hedged requests (send a second copy after a delay, take the first reply) cut tails but add load, so use only with idempotent calls and spare capacity (concept only).
- Trap: a client timeout does not free the server. The abandoned request still occupies a slot, so under overload you also need the server-side cap.
- The experiment below: 4 "slots", mean work about 9 ms, 2 percent of calls take 200 ms. Open-loop arrivals at 150 and 330 requests per second. All numbers are this sandbox only.

**Example:** Hand check at 150 rps: 2 percent of calls are slow, so about 3 of every 150 per second. p99 is the 99th of 100 calls, so it lands in the slow group and shows about 200 ms while p50 stays near the 5 to 8 ms of the fast path. At 330 rps the slots are busy enough that requests wait in line, and even p50 rises.

**Code:** an app with a 4-slot semaphore, an unprotected route and a capped route, and an open-loop load driver on port 8406. Run with Python 3.13.17 in a venv: fastapi 0.162.0, uvicorn 0.54.0, httpx 0.28.1, pytest 9.1.1, scikit-learn 1.9.1, skl2onnx 1.20.0, onnxruntime 1.31.0, torch 2.14.1 (CPU only). Sandbox timings are machine-specific demos, not benchmarks.
```python
# ===== q40_app.py =====
# 4 "workers" (a semaphore) stand in for CPU capacity. 2 percent of calls take the slow path (200 ms).
import asyncio, random
from fastapi import FastAPI, Response
SLOTS = asyncio.Semaphore(4); waiting = 0; rng = random.Random(1)
MAX_WAITING = 8
app = FastAPI()
async def work():
    await asyncio.sleep(0.200 if rng.random() < 0.02 else 0.005)
@app.post("/predict")                      # no protection: unbounded queue in front of the 4 slots
async def predict():
    async with SLOTS: await work()
    return {"label": 1}
@app.post("/predict_capped")               # concurrency cap: too many waiting -> shed with 503 straight away
async def predict_capped(resp: Response):
    global waiting
    if waiting >= MAX_WAITING: resp.status_code = 503; return {"shed": True}
    waiting += 1
    try:
        async with SLOTS: await work()
    finally: waiting -= 1
    return {"label": 1}

# ===== q40_run.py =====
import asyncio, os, subprocess, sys, time, pathlib, statistics, httpx
HERE = str(pathlib.Path(__file__).parent); PORT = 8406; URL = f"http://127.0.0.1:{PORT}"
SECONDS = 5; RATE = 150     # open loop: requests arrive at RATE per second no matter how slow the server is
def pct(v, q): v = sorted(v); return v[min(len(v) - 1, int(q * len(v)))] * 1000
async def run(path, timeout=None, fallback=False, RATE=None):
    RATE = RATE or globals()['RATE']
    lat, shed, fell = [], 0, 0
    async with httpx.AsyncClient(limits=httpx.Limits(max_connections=2000), timeout=30) as c:
        async def one():
            nonlocal shed, fell
            t = time.perf_counter()
            try:
                r = await asyncio.wait_for(c.post(URL + path), timeout) if timeout else await c.post(URL + path)
                if r.status_code == 503: shed += 1
            except asyncio.TimeoutError:
                fell += 1                                   # fallback: a cheap default answer, computed locally
                if not fallback: raise
            lat.append(time.perf_counter() - t)
        tasks = []; start = time.perf_counter()
        for i in range(RATE * SECONDS):
            await asyncio.sleep(max(0, start + i / RATE - time.perf_counter())); tasks.append(asyncio.create_task(one()))
        await asyncio.gather(*tasks)
    ok = [x for x in lat]
    return len(lat), pct(ok, .5), pct(ok, .99), shed, fell
def show(name, r): print(f"{name:42s} n={r[0]:5d}  p50={r[1]:7.1f} ms  p99={r[2]:7.1f} ms  shed(503)={r[3]:4d}  timeout->fallback={r[4]:4d}")
p = subprocess.Popen([sys.executable, "-m", "uvicorn", "q40_app:app", "--port", str(PORT), "--app-dir", HERE, "--log-level", "warning"])
try:
    for _ in range(100):
        try: httpx.get(URL + "/openapi.json", timeout=1); break
        except Exception: time.sleep(0.1)
    asyncio.run(run("/predict", RATE=50))   # warm-up pass (not reported)
    print("4 slots; mean work about 8.9 ms => roughly 450 requests/s max on paper. Open-loop arrivals.")
    for rate in (150, 330):
        print(f"--- offered load {rate} requests/s for {SECONDS}s ---")
        show("A. baseline, 2% slow path, unbounded queue", asyncio.run(run("/predict", RATE=rate)))
        show("B. client timeout 60 ms + fallback", asyncio.run(run("/predict", timeout=0.060, fallback=True, RATE=rate)))
        show("C. server cap (shed above 8 waiting)", asyncio.run(run("/predict_capped", RATE=rate)))
finally:
    p.terminate(); p.wait(timeout=10); print("server stopped:", p.poll() is not None)
```
```bash
cd /tmp/claude-0/b6_q35_45 && /tmp/claude-0/b6p06/v/bin/python -I q40_run.py
```

**Output (my run):** real run (server started and stopped by the script). Numbers are machine-specific demos, not benchmarks; a rerun will differ.
```text
4 slots; mean work about 8.9 ms => roughly 450 requests/s max on paper. Open-loop arrivals.
--- offered load 150 requests/s for 5s ---
A. baseline, 2% slow path, unbounded queue n=  750  p50=    8.0 ms  p99=  202.9 ms  shed(503)=   0  timeout->fallback=   0
B. client timeout 60 ms + fallback         n=  750  p50=    8.0 ms  p99=   61.7 ms  shed(503)=   0  timeout->fallback=  44
C. server cap (shed above 8 waiting)       n=  750  p50=    8.1 ms  p99=  203.5 ms  shed(503)=   2  timeout->fallback=   0
--- offered load 330 requests/s for 5s ---
A. baseline, 2% slow path, unbounded queue n= 1650  p50=  126.4 ms  p99=  800.2 ms  shed(503)=   0  timeout->fallback=   0
B. client timeout 60 ms + fallback         n= 1650  p50=    9.1 ms  p99=   62.6 ms  shed(503)=   0  timeout->fallback= 324
C. server cap (shed above 8 waiting)       n= 1650  p50=    8.1 ms  p99=  205.1 ms  shed(503)= 107  timeout->fallback=   0
server stopped: True
```

**Follow-ups:**
- Would more replicas fix it? At 330 rps yes (less queueing), at 150 rps no (the tail is the slow path itself). Find which one you have before scaling.
- Timeout value? Slightly above the p99 of the healthy path, and shorter than the caller's own deadline.
- What does the fallback return? A cached or default prediction, flagged so Part 8 monitoring can count it.

**Common mistakes:**
- Quoting averages or only p50.
- Load-testing closed loop (the client slows down when the server does, hiding queueing). Use open loop.
- Retrying on timeout with no cap (retry storm).
- Timeouts with no server-side limit.
- Treating these numbers as benchmarks.

---

### Q41 ⭐ 🔴 ONNX Runtime tuning. Explain session options (graph_optimization_level, intra_op_num_threads and inter_op_num_threads, execution_mode), execution providers and fallback order, IO binding to avoid host-device copies on GPU, dynamic versus fixed input shapes, why session creation is expensive and a session is reused across threads, and profiling (enable_profiling). On CPU, run a small model with 1, 2 and 4 intra-op threads and different optimisation levels, show timings labelled machine-specific, and show the profile file keys. GPU, TensorRT and OpenVINO providers are not executed; print the providers that are available here.
**Asked at:** Model format and safety sources (scikit-learn model persistence docs, arxiv.org 2410.04490 on Hugging Face model exploits, labs.snyk.io deep-learning file format vulnerabilities, union.ai secure-AI post, ProtectAI ModelScan docs; search snippets only, not opened); docs and security write-ups, not interview reports; ML engineer and MLOps roles, security-aware teams
**Say this first (1 line):** Create one InferenceSession per model and reuse it across threads, set threads and graph optimisation on purpose, list providers in fallback order, measure instead of assuming, and use the profiler to see which operators cost time.

**Then explain:**
- Session options: `graph_optimization_level` (disable, basic, extended, all) controls fusions and constant folding; `intra_op_num_threads` splits one operator across threads, `inter_op_num_threads` runs independent operators in parallel and only matters with `execution_mode = ORT_PARALLEL`.
- Providers: pass a list in priority order, for example CUDA then CPU. If the first cannot take a node, ONNX Runtime falls back to the next, which can hide a silent CPU fallback. Check `session.get_providers()`.
- IO binding (GPU): bind inputs and outputs in device memory so tensors do not copy host to device on every call. Concept here, not executed.
- Shapes: dynamic dimensions give flexibility; fixed shapes let the runtime plan memory and sometimes fuse better. Dynamic batch is usual for serving.
- Session creation parses and optimises the graph, which costs far more than a small run. Create at startup, reuse, `run` is thread-safe (the test shows eight parallel runs identical).
- Threads: do not set intra-op threads times worker processes above the cores you have (oversubscription makes the tail worse).
- Profiling: `enable_profiling=True` then `end_profiling()` writes a Chrome-trace style JSON.

**Example:** Machine has 4 cores and you run 4 uvicorn workers. Give each session 1 intra-op thread: 4 x 1 = 4. Giving each 4 threads means 16 threads fighting for 4 cores. In the run below, 1, 2 and 4 threads on a big batch of 1024 rows speed up; for a batch of 1 the work is tiny, so measure before adding threads.

**Code:** one script: builds an MLP (two 1024-wide hidden layers) with scikit-learn, exports it with skl2onnx, times it, and dumps the profile keys. Run with Python 3.13.17 in a venv: fastapi 0.162.0, uvicorn 0.54.0, httpx 0.28.1, pytest 9.1.1, scikit-learn 1.9.1, skl2onnx 1.20.0, onnxruntime 1.31.0, torch 2.14.1 (CPU only). Sandbox timings are machine-specific demos, not benchmarks.
```python
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
```
```bash
cd /tmp/claude-0/b6_q35_45 && /tmp/claude-0/b6p06/v/bin/python -I q41_ort.py
```

**Output (my run):** real run on CPU, 4 visible cores. Times are medians in this sandbox only and are noisy (the optimisation levels differ by less than the noise here, so do not read a ranking into them). GPU, TensorRT and OpenVINO providers are not executed; the available providers are printed below.
```text
onnxruntime 1.31.0 | available providers: ['AzureExecutionProvider', 'CPUExecutionProvider']
CPU cores visible: 4
session creation: 17.2 ms vs one batch-1024 run: 19.67 ms (create once, reuse)

intra-op threads (batch 1024, median ms, this sandbox only):
  intra_op_num_threads=1: 24.82 ms
  intra_op_num_threads=2: 13.62 ms
  intra_op_num_threads=4: 10.35 ms

graph optimisation level (1 thread, batch 1024):
  DISABLE_ALL: 22.01 ms
  ENABLE_BASIC: 28.12 ms
  ENABLE_EXTENDED: 22.08 ms
  ENABLE_ALL: 20.22 ms

batch size 1 with 1 vs 4 threads (measure it, do not assume):
  intra_op_num_threads=1: 0.228 ms
  intra_op_num_threads=4: 0.115 ms

same session from 4 Python threads (sessions are thread safe for run):
  all 8 results identical to single-thread result: True

profile file: onnxruntime_profile_...json | events: 35 | keys of an event: ['args', 'cat', 'dur', 'name', 'ph', 'pid', 'tid', 'ts']
categories seen: ['Node', 'Session'] | node event args keys: ['activation_size', 'input_type_shape', 'mem_arena_held', 'mem_arena_held_delta', 'mem_bytes_in_use', 'mem_bytes_requested_in_use', 'mem_in_use_delta', 'mem_in_use_peak', 'mem_requested_in_use_delta', 'node_index', 'op_name', 'output_size', 'output_type_shape', 'parameter_size', 'provider', 'thread_scheduling_stats']
kernel time per op type (us, 3 runs): {'FusedGemm': 167739, 'Sub': 127, 'Concat': 88, 'ArgMax': 61, 'ArrayFeatureExtractor': 31, 'Cast': 29, 'Reshape': 25}
```

**Follow-ups:**
- Why FusedGemm in the profile? Graph optimisation fused a matrix multiply with its bias and activation. With optimisation disabled you would see separate nodes.
- Is bigger batch always better? It raises throughput but adds latency per request; Q30-style dynamic batching is the trade.
- Quantisation? `onnxruntime.quantization.quantize_dynamic` exists; always re-check accuracy afterwards (not run here).

**Common mistakes:**
- Creating a session per request.
- Leaving default threads in every one of many worker processes.
- Assuming CUDA is used because it is listed first (check `get_providers()` after creation).
- Benchmarking with no warm-up or with one run.
- Trusting a laptop timing as a production number.

---

### Q42 ⭐ 🔴 Export failures and portability. Show and fix the common ones: a PyTorch export that fails on an unsupported operator or data-dependent control flow (tracing versus scripting versus the newer torch.export-based exporter; check current docs), a missing dynamic axis so a batch of 7 fails on a model exported with batch 1, opset mismatch between exporter and runtime, float64 inputs to a float32 graph, and a custom preprocessing step that is not in the graph. Write the failing cases and the fixes with PyTorch CPU and ONNX Runtime, run them for real, and show the exact error messages. TorchScript save and load are also shown.
**Asked at:** Model format and safety sources (scikit-learn model persistence docs, arxiv.org 2410.04490 on Hugging Face model exploits, labs.snyk.io deep-learning file format vulnerabilities, union.ai secure-AI post, ProtectAI ModelScan docs; search snippets only, not opened); docs and security write-ups, not interview reports; ML engineer and MLOps roles, security-aware teams
**Say this first (1 line):** Most export failures are one of five things: tracing freezes a Python branch, an operator has no ONNX mapping, a batch dimension was not marked dynamic, the dtype is wrong, or preprocessing never made it into the graph; each has a clear error or a one-line fix.

**Then explain:**
- Tracing records the ops run for one example input, so a Python `if` on a tensor value is frozen to the branch taken. It does not error, it gives wrong answers later (shown). Fixes: write the branch with `torch.where`, use `torch.jit.script` for TorchScript, or use the newer `torch.export`-based exporter (the default in recent torch; check current docs for its limits and what it needs installed).
- Unsupported operator: the exporter raises `UnsupportedOperatorError` naming the op (here `aten::fft_rfft`). Options: rewrite with supported ops (a DFT matrix in the run), register a custom symbolic or op, or keep that step outside the model (then it is a skew risk, Q35).
- Missing dynamic axis: a model exported with batch 1 fails for batch 7 with an `INVALID_ARGUMENT ... Expected: 1` error. Declare `dynamic_axes` for inputs and outputs.
- Opset mismatch: the exporter's opset must be one the runtime supports. A model newer than the runtime fails at load (simulated here by editing the opset number). Pin the export opset and the runtime version together.
- dtype: ONNX graphs are strict, float64 into a float32 graph errors. Cast at the edge.
- Preprocessing outside the graph: no error, just wrong numbers. Put it inside the module before export.
- TorchScript save/load is shown at the end. Note `torch.load` and TorchScript files should still come from trusted sources only.

**Example:** Branchy model: `if x.sum() > 0: return x * 2 else x - 100`. Exported with an all-ones example, the trace keeps `x * 2`. For input -1,-1,-1,-1 eager gives -101, the trace gives -2 (hand check: -1 times 2 is -2). The fixed version with `torch.where` gives -101.

**Code:** one script with eight numbered cases. It uses the legacy TorchScript-based exporter (`dynamo=False`) for the failing cases because its messages are the classic ones, and calls the default exporter once in case 7. Run with Python 3.13.17 in a venv: fastapi 0.162.0, uvicorn 0.54.0, httpx 0.28.1, pytest 9.1.1, scikit-learn 1.9.1, skl2onnx 1.20.0, onnxruntime 1.31.0, torch 2.14.1 (CPU only). Sandbox timings are machine-specific demos, not benchmarks.
```python
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
```
```bash
cd /tmp/claude-0/b6_q35_45 && /tmp/claude-0/b6p06/v/bin/python -I q42_export.py 2>/dev/null
```

**Output (my run):** real run, exact messages (long lines cut at about 230 characters by my script; the progress lines of the default exporter were filtered out). Exporter messages change between torch versions, check current docs.
```text
torch 2.14.1+cu130 | onnx 1.23.2 | onnxruntime 1.31.0

== 1. data-dependent control flow: trace bakes in one branch ==
eager on negative input: [-101.0, -101.0, -101.0, -101.0] | traced on negative input: [-2.0, -2.0, -2.0, -2.0]   <- silently wrong (branch frozen)
fixed with torch.where, ONNX on negative input: [-101.0, -101.0, -101.0, -101.0]
torch.jit.script keeps the branch, negative input: [-101.0, -101.0, -101.0, -101.0]

== 2. unsupported operator (no ONNX mapping) ==
fft: UnsupportedOperatorError: Exporting the operator 'aten::fft_rfft' to ONNX opset version 17 is not supported
DFT-matrix rewrite exports; max diff vs torch.fft: True

== 3. missing dynamic axis: exported with batch 1, serve batch 7 ==
batch 7: InvalidArgument: [ONNXRuntimeError] : 2 : INVALID_ARGUMENT : Got invalid dimensions for input: x for the following indices  index: 0 Got: 7 Expected: 1  Please fix either the inputs/outputs or the model.
with dynamic_axes, batch 7 output shape: (7, 2) | matches torch: True

== 4. opset mismatch between exporter and runtime ==
exported opset: 17
runtime too old for opset 99: Fail: [ONNXRuntimeError] : 1 : FAIL : /onnxruntime_src/onnxr ... before next ONNX release and in this case ONNX Runtime will not guarantee backward compatibility. Current official support for domain ai.onnx is till opset 26. 

== 5. float64 input to a float32 graph ==
float64: InvalidArgument: [ONNXRuntimeError] : 2 : INVALID_ARGUMENT : Unexpected input data type. Actual: (tensor(double)) , expected: (tensor(float))
fix: x.astype(np.float32) -> shape (7, 2)

== 6. preprocessing outside the graph ==
expected (normalised first): [[0.8385999798774719]] | graph without preprocessing on raw input: [[6.509099960327148]] | graph with preprocessing: [[0.8385999798774719]]

== 7. newer torch.export-based exporter (default dynamo=True in recent torch) ==
default exporter wrote 1860 bytes

== 8. TorchScript save and load ==
loaded matches eager on batch 7: True | file size > 0: True
(torch then prints its internal IR graph for the failing op; trimmed here)
```

**Follow-ups:**
- Which exporter should a new project use? The torch.export-based one is the direction of travel (the legacy one warns it is superseded), but check current docs for operator coverage and try both on your model.
- How do you test an exported model? Run the same inputs through torch and ONNX Runtime and compare outputs with a tolerance, including a batch size different from the example (Q35 parity test).
- Custom ops? Keep them out of the graph or ship a custom ONNX Runtime op library; both add risk.

**Common mistakes:**
- Exporting with batch 1 and no dynamic axes.
- Trusting a trace of a model with data-dependent `if` or loops.
- Exporting a model in train mode (dropout, batch norm behave differently); call `.eval()`.
- Testing only the example shape.
- Leaving normalisation in the notebook.

---

### Q43 ⭐ 🔴 Cost model for serving: cost per 1,000 predictions for batch, real-time on CPU and real-time on GPU. Explain utilisation (idle capacity is the biggest cost), batching raising throughput per dollar, spot or preemptible capacity for batch only, reserved baseline plus autoscaled burst, scale to zero versus warm replicas, and the trade between cost and p99. Write a Python calculator with explicit invented inputs (hourly price, throughput per replica, utilisation, peak-to-average ratio) and tests; run it and show the break-even point between always-on real-time and nightly batch. No real prices or vendor numbers are used; Part 12 owns cost in depth.
**Asked at:** Autoscaling and cold-start sources (feedly.com engineering 'fast autoscaling on GPUs', designgurus.io 'what to expect in the Baseten system design interview' (not an official Baseten source), uwaterloo.ca GPU cold-start paper listing; search snippets only, not opened); engineering blog and secondary prep page; GPU serving and inference platform roles
**Say this first (1 line):** Cost per 1,000 predictions is hourly price divided by useful predictions per hour, so utilisation decides it: an idle replica is the biggest cost, and batching and autoscaling work by raising utilisation.

**Then explain:**
- Formula: cost per 1,000 = 1000 x (replicas x hourly price x hours) / predictions served. Replicas come from peak requests per second divided by (throughput per replica x target utilisation). Target utilisation stays below 100 percent because near saturation p99 explodes (Q40).
- Sized for the peak all day, a service with peak-to-average 4 sits at low average utilisation. Autoscaling follows the load but needs headroom for scale-up lag. Reserved or committed capacity for the steady baseline plus autoscaled burst is the usual mix (check current provider options).
- Batch scoring runs at high throughput on big batches, can use spot or preemptible capacity because a failed job can restart, and shuts down when done. Spot is not for real-time serving (interruptions hit user requests).
- Scale to zero removes idle cost but adds cold starts, so it trades cost against p99 (Q44).
- GPU: much higher hourly price, much higher throughput. It only wins at high utilisation or for models that need it; at low traffic it just idles expensively.
- All inputs in the code are invented (units are made-up). Part 12 owns real cost work.

**Example:** Hand check (invented): avg 20 rps, peak 80 rps. One CPU replica does 50 rps at 100 percent busy, target 60 percent, so 30 usable. Peak needs ceil(80 / 30) = 3 replicas, cost 3 x 1.0 x 24 = 72 per day for 1,728,000 predictions: 72 x 1000 / 1,728,000 = 0.0417 per 1,000. Autoscaled to 1 replica: 24 per day, 0.0139 per 1,000. Nightly batch: 1.2 h of work plus 0.25 h overhead, times price 1.0 and spot factor 0.4 = 0.58 per run.

**Code:** the calculator, nine tests that check the hand numbers above, and a break-even: how many batch runs per day cost the same as one always-on replica. Run with Python 3.13.17 in a venv: fastapi 0.162.0, uvicorn 0.54.0, httpx 0.28.1, pytest 9.1.1, scikit-learn 1.9.1, skl2onnx 1.20.0, onnxruntime 1.31.0, torch 2.14.1 (CPU only). Sandbox timings are machine-specific demos, not benchmarks.
```python
# ===== q43_cost.py =====
"""Serving cost calculator. EVERY number below is INVENTED for the demo (units: 'cu' = made-up currency units)."""
import math
from dataclasses import dataclass

@dataclass(frozen=True)
class Realtime:
    price_per_hour: float      # cost of one replica for one hour
    rps_per_replica: float     # sustainable requests/s at 100% busy (measured by you in real life)
    target_util: float         # keep below 1.0 so p99 does not blow up (queueing)
    min_replicas: int = 1

@dataclass(frozen=True)
class Batch:
    price_per_hour: float
    preds_per_sec: float       # batch throughput of one worker (big batches, so higher than online)
    spot_factor: float = 1.0   # 0.4 means spot costs 40% of on-demand (invented); batch only
    overhead_hours: float = 0.25   # startup + load + write results, billed

def replicas_needed(rps, rt):
    return max(rt.min_replicas, math.ceil(rps / (rt.rps_per_replica * rt.target_util)))

def realtime_static_cost_per_day(avg_rps, peak_to_avg, rt):
    """Provision for the peak all day (no autoscaling)."""
    n = replicas_needed(avg_rps * peak_to_avg, rt)
    return n * rt.price_per_hour * 24, n

def realtime_autoscaled_cost_per_day(avg_rps, rt, scale_headroom=1.3):
    """Replicas follow the average load plus headroom for scale-up lag; floor at min_replicas."""
    n = max(rt.min_replicas, math.ceil(avg_rps * scale_headroom / (rt.rps_per_replica * rt.target_util)))
    return n * rt.price_per_hour * 24, n

def batch_cost_per_day(preds_per_day, b, workers=1):
    hours = preds_per_day / (b.preds_per_sec * 3600 * workers) + b.overhead_hours
    return hours * workers * b.price_per_hour * b.spot_factor

def per_1000(cost_per_day, preds_per_day):
    return 1000 * cost_per_day / preds_per_day

def utilisation(avg_rps, replicas, rt):
    return avg_rps / (replicas * rt.rps_per_replica)

def breakeven_runs_per_day(always_on_cost_per_day, preds_per_run, b, workers=1):
    """How many batch runs per day (each scoring preds_per_run rows) cost the same as keeping the real-time service on.
    Fewer runs than this: batch is cheaper. More runs (fresher scores): always-on is cheaper."""
    one_run = batch_cost_per_day(preds_per_run, b, workers)      # cost of one run, overhead included
    return always_on_cost_per_day / one_run

if __name__ == "__main__":
    cpu = Realtime(price_per_hour=1.0, rps_per_replica=50, target_util=0.6)
    gpu = Realtime(price_per_hour=6.0, rps_per_replica=600, target_util=0.6)
    bcpu = Batch(price_per_hour=1.0, preds_per_sec=400, spot_factor=0.4)
    avg_rps, ratio = 20, 4                                          # average 20 req/s, peak 80 req/s
    day = avg_rps * 86400
    print(f"traffic: avg {avg_rps} rps, peak/avg {ratio}, {day:,} predictions/day (all numbers invented)")
    print(f"{'option':34s}{'replicas':>9s}{'cost/day':>10s}{'cu per 1000':>13s}{'avg util':>10s}")
    for name, cost, n, rt in [("CPU real-time, sized for peak", *realtime_static_cost_per_day(avg_rps, ratio, cpu), cpu),
                              ("CPU real-time, autoscaled", *realtime_autoscaled_cost_per_day(avg_rps, cpu), cpu),
                              ("GPU real-time, sized for peak", *realtime_static_cost_per_day(avg_rps, ratio, gpu), gpu)]:
        print(f"{name:34s}{n:9d}{cost:10.1f}{per_1000(cost, day):13.4f}{utilisation(avg_rps, n, rt):10.1%}")
    bc = batch_cost_per_day(day, bcpu); print(f"{'CPU nightly batch on spot':34s}{'1 job':>9s}{bc:10.1f}{per_1000(bc, day):13.4f}{'n/a':>10s}")
    one_always_on = cpu.price_per_hour * 24
    for rows in (1_728_000, 50_000_000):
        r = breakeven_runs_per_day(one_always_on, rows, bcpu, workers=math.ceil(rows / (bcpu.preds_per_sec * 3600 * 6)))
        print(f"scoring {rows:>10,} rows per run (workers sized to finish in ~6h): batch = always-on CPU replica ({one_always_on:.0f} cu/day) at {r:.1f} runs/day")
    print("  nightly = 1 run/day, hourly = 24 runs/day. Real-time is the only choice when a user waits for the answer.")

# ===== test_q43_cost.py =====
import sys, pathlib, math; sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q43_cost import *
CPU = Realtime(1.0, 50, 0.6); B = Batch(1.0, 400, 0.4)

def test_replicas_hand_check():             # 80 rps / (50*0.6=30 per replica) = 2.67 -> 3
    assert replicas_needed(80, CPU) == 3
def test_min_replicas_floor():
    assert replicas_needed(1, Realtime(1, 50, 0.6, min_replicas=2)) == 2
def test_static_cost():                     # 3 replicas * 1.0 * 24
    assert realtime_static_cost_per_day(20, 4, CPU) == (72.0, 3)
def test_autoscaled_cheaper_than_static():
    assert realtime_autoscaled_cost_per_day(20, CPU)[0] < realtime_static_cost_per_day(20, 4, CPU)[0]
def test_batch_hand_check():                # 1,728,000 preds / (400*3600=1.44M per h) = 1.2 h + 0.25 = 1.45 h * 0.4
    assert math.isclose(batch_cost_per_day(1_728_000, B), 1.45 * 0.4)
def test_per_1000():
    assert per_1000(72.0, 1_728_000) == 72.0 * 1000 / 1_728_000
def test_breakeven_runs_hand_check():       # one run = 1.45 h * 0.4 = 0.58 cu; 24 / 0.58 = 41.38 runs
    assert math.isclose(breakeven_runs_per_day(24.0, 1_728_000, B), 24.0 / 0.58)
def test_breakeven_is_where_costs_cross():
    r = breakeven_runs_per_day(24.0, 1_728_000, B)
    assert math.isclose(r * batch_cost_per_day(1_728_000, B), 24.0)
    assert 24 * batch_cost_per_day(1_728_000, B) < 24.0       # hourly batch is still cheaper here
def test_low_utilisation_costs_more_per_prediction():
    c1 = per_1000(24.0, 100_000); c2 = per_1000(24.0, 1_000_000); assert c1 == 10 * c2
```
```bash
cd /tmp/claude-0/b6_q35_45 && /tmp/claude-0/b6p06/v/bin/python -I q43_cost.py
/tmp/claude-0/b6p06/v/bin/python -m pytest -q -p no:cacheprovider test_q43_cost.py
```

**Output (my run):** real run. All inputs are invented; no real prices or vendor numbers.
```text
traffic: avg 20 rps, peak/avg 4, 1,728,000 predictions/day (all numbers invented)
option                             replicas  cost/day  cu per 1000  avg util
CPU real-time, sized for peak             3      72.0       0.0417     13.3%
CPU real-time, autoscaled                 1      24.0       0.0139     40.0%
GPU real-time, sized for peak             1     144.0       0.0833      3.3%
CPU nightly batch on spot             1 job       0.6       0.0003       n/a
scoring  1,728,000 rows per run (workers sized to finish in ~6h): batch = always-on CPU replica (24 cu/day) at 41.4 runs/day
scoring 50,000,000 rows per run (workers sized to finish in ~6h): batch = always-on CPU replica (24 cu/day) at 1.7 runs/day
  nightly = 1 run/day, hourly = 24 runs/day. Real-time is the only choice when a user waits for the answer.
.........                                                                [100%]
9 passed in 0.02s
```

**Follow-ups:**
- When is always-on real-time cheaper than batch? When you would have to run the batch very often to keep scores fresh: above the break-even runs per day the always-on replica wins. If users wait for the answer, batch is not an option anyway.
- Why not size at 100 percent utilisation? Queueing: the tail grows fast near saturation, and a failed node has no spare.
- How do you get the throughput number? Load-test your own model with a realistic payload (Part 6 Q40 style) and use p99-safe throughput, not the max.

**Common mistakes:**
- Dividing price by peak throughput instead of real average traffic.
- Ignoring idle time and overheads (startup, model load, data read).
- Using spot for the real-time path.
- Comparing GPU and CPU at different utilisation levels.
- Quoting invented numbers as real prices.

---

### Q44 ⭐ 🔴 Serverless and managed endpoints for models at concept level: AWS Lambda, Cloud Run, Azure Container Apps and the managed endpoints in SageMaker, Vertex AI and Azure ML. Cover cold starts and package or image size limits (check current limits), no GPU or limited GPU on some options, scale to zero, per-request pricing versus always-on, concurrency per instance, and when serverless fits (spiky, small models) versus when it does not (large models, steady heavy traffic, strict p99). Give a comparison table with hedged claims and a decision function with tests. Nothing is deployed; Parts 10 and 11 own the cloud services.
**Asked at:** Autoscaling and cold-start sources (feedly.com engineering 'fast autoscaling on GPUs', designgurus.io 'what to expect in the Baseten system design interview' (not an official Baseten source), uwaterloo.ca GPU cold-start paper listing; search snippets only, not opened); engineering blog and secondary prep page; GPU serving and inference platform roles
**Say this first (1 line):** Serverless fits small models with spiky or low traffic and relaxed p99; it does not fit big models, steady heavy traffic, strict tail latency or GPU needs, so measure cold start and decide from traffic shape, not from fashion.

**Then explain:**
- The options at concept level: AWS Lambda (functions, also container images), Cloud Run (serverless containers, concurrency per instance), Azure Container Apps (serverless containers), and the managed endpoints in SageMaker, Vertex AI and Azure ML (model-focused, some can scale to zero or have serverless modes; check each one's current docs).
- Cold start: the first request after idle pays image pull, runtime start and model load. A bigger package or image means a longer one. Keep the model small, load at startup not per request, or keep minimum instances above zero (which costs idle money).
- Limits: package or image size, memory, timeout, payload size and GPU support differ per service and change; check current limits before designing around any of them.
- Pricing shape: per request or per busy second is cheap when traffic is rare, expensive when traffic is steady. Always-on is the reverse.
- Concurrency per instance: some services (Cloud Run style) serve many requests per container, some (function style) one at a time. This changes how many instances a burst creates.
- Hedged comparison (check current docs for every row):

| Option | Scale to zero | Typical fit | Watch out for |
|---|---|---|---|
| Function service (Lambda style) | yes | small models, event or spiky calls | package or image size cap, cold start, no or limited GPU |
| Serverless container (Cloud Run, Container Apps style) | usually yes | medium image, HTTP model API, spiky | cold start with big images, GPU availability varies |
| Managed model endpoint (SageMaker, Vertex AI, Azure ML) | varies by mode | team wants registry, scaling, monitoring built in | price of always-on instances, mode limits |
| Always-on cluster (Part 3) | no (unless added) | steady heavy traffic, GPU, strict p99 | you run it |

**Example:** Small tabular scorer, 0.5 rps average, bursts 10x, relaxed 2 s budget, 600 ms cold start: function. Fraud scorer with a 150 ms p99 and 600 ms cold start: the cold start alone breaks the budget, so keep minimum instances above zero. Transformer needing GPU: not serverless.

**Code:** a rule-based decision function with invented thresholds (clearly labelled, not cloud limits), a demo and seven tests. Run with Python 3.13.17 in a venv: fastapi 0.162.0, uvicorn 0.54.0, httpx 0.28.1, pytest 9.1.1, scikit-learn 1.9.1, skl2onnx 1.20.0, onnxruntime 1.31.0, torch 2.14.1 (CPU only). Sandbox timings are machine-specific demos, not benchmarks.
```python
# ===== q44_serverless.py =====
"""Rule-based picker: serverless function / serverless container / managed endpoint / always-on cluster.
Thresholds are INVENTED teaching defaults, not cloud limits. Check current provider docs for real limits."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Workload:
    model_mb: float            # size of model plus runtime image
    needs_gpu: bool
    avg_rps: float
    peak_to_avg: float         # burstiness
    p99_budget_ms: float       # strict latency need
    cold_start_ms: float       # your measured cold start for this image (measure it)
    idle_fraction: float       # share of the day with no traffic, 0..1
    team_runs_k8s: bool = False

FUNCTION_MAX_MB = 250          # invented stand-in for a function package/image ceiling; real ceilings differ per provider, check docs
CONTAINER_MAX_MB = 4000        # invented stand-in for a comfortable serverless-container image size
STEADY_RPS = 5                 # above this average, always-on capacity is usually cheaper than per-request billing (invented)

def choose(w: Workload) -> tuple[str, list[str]]:
    why = []
    if w.needs_gpu:
        why.append("GPU needed: many serverless options have no GPU or a limited one (check current docs)")
        return ("managed endpoint (GPU) or cluster", why)
    cold_ok = w.cold_start_ms <= w.p99_budget_ms * 0.5
    if not cold_ok and w.idle_fraction > 0:
        why.append(f"cold start {w.cold_start_ms:.0f} ms is over half the p99 budget: scale-to-zero would breach it; keep min instances warm")
    if w.avg_rps >= STEADY_RPS:
        why.append(f"avg {w.avg_rps} rps is steady and heavy: always-on capacity usually beats per-request billing")
        return ("managed endpoint or cluster (always-on)", why)
    if w.model_mb > CONTAINER_MAX_MB:
        why.append("large model: image pull and load make cold starts long; prefer warm replicas")
        return ("managed endpoint or cluster (always-on)", why)
    if w.model_mb <= FUNCTION_MAX_MB and cold_ok:
        why.append("small model, low traffic, cold start fits the budget: a function fits")
        return ("serverless function", why)
    if not cold_ok:
        why.append("serverless container with minimum instances > 0 (pays for idle, kills cold start)")
        return ("serverless container (min instances > 0)", why)
    why.append("model too big for a function package but fine for a container image; low traffic favours scale to zero")
    return ("serverless container (scale to zero)", why)

# ===== test_q44_serverless.py =====
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent))
from dataclasses import replace
from q44_serverless import Workload, choose
BASE = Workload(model_mb=50, needs_gpu=False, avg_rps=0.5, peak_to_avg=10, p99_budget_ms=2000, cold_start_ms=600, idle_fraction=0.7)

def test_small_spiky_model_fits_function(): assert choose(BASE)[0] == "serverless function"
def test_gpu_never_serverless(): assert choose(replace(BASE, needs_gpu=True))[0].startswith("managed endpoint (GPU)")
def test_steady_heavy_traffic_goes_always_on(): assert "always-on" in choose(replace(BASE, avg_rps=50))[0]
def test_strict_p99_with_slow_cold_start_keeps_warm(): assert "min instances" in choose(replace(BASE, p99_budget_ms=500, cold_start_ms=600))[0]
def test_medium_model_container_scale_to_zero(): assert choose(replace(BASE, model_mb=900))[0] == "serverless container (scale to zero)"
def test_huge_model_always_on(): assert "always-on" in choose(replace(BASE, model_mb=8000))[0]
def test_reasons_are_returned(): assert all(len(choose(w)[1]) >= 1 for w in [BASE, replace(BASE, needs_gpu=True), replace(BASE, avg_rps=50)])

# ===== q44_demo.py =====
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q44_serverless import Workload, choose
cases = {"small tabular model, spiky, lax latency": Workload(50, False, 0.5, 10, 2000, 600, 0.7),
         "image model 900 MB, low traffic": Workload(900, False, 1, 8, 3000, 1500, 0.5),
         "fraud scorer, strict p99, bursty": Workload(80, False, 2, 6, 150, 600, 0.2),
         "ranking model, steady 50 rps": Workload(200, False, 50, 2, 100, 400, 0.0),
         "large transformer needing GPU": Workload(4000, True, 3, 5, 800, 20000, 0.3)}
for n, w in cases.items():
    c, why = choose(w); print(f"{n:42s} -> {c}\n    {why[0]}")
```
```bash
cd /tmp/claude-0/b6_q35_45 && /tmp/claude-0/b6p06/v/bin/python -I q44_demo.py
/tmp/claude-0/b6p06/v/bin/python -m pytest -q -p no:cacheprovider test_q44_serverless.py
```

**Output (my run):** real run of the decision function and tests. Nothing was deployed to Lambda, Cloud Run, Azure or any managed endpoint, and no cloud limit was checked (not executed).
```text
small tabular model, spiky, lax latency    -> serverless function
    small model, low traffic, cold start fits the budget: a function fits
image model 900 MB, low traffic            -> serverless container (scale to zero)
    model too big for a function package but fine for a container image; low traffic favours scale to zero
fraud scorer, strict p99, bursty           -> serverless container (min instances > 0)
    cold start 600 ms is over half the p99 budget: scale-to-zero would breach it; keep min instances warm
ranking model, steady 50 rps               -> managed endpoint or cluster (always-on)
    avg 50 rps is steady and heavy: always-on capacity usually beats per-request billing
large transformer needing GPU              -> managed endpoint (GPU) or cluster
    GPU needed: many serverless options have no GPU or a limited one (check current docs)
.......                                                                  [100%]
7 passed in 0.01s
```

**Follow-ups:**
- Cold start fix without paying for idle? Smaller image, lazy-load only what you need, load the model from a local layer, and warm with a scheduled ping (which still costs a little).
- Batch inference serverless? Often fine for event-driven scoring, but long jobs hit time limits; check current docs.
- Why a function and not rules in a notebook? The point is to make the trade explicit and testable; the real answer comes from your own cold-start and load measurements.

**Common mistakes:**
- Picking serverless for steady 24/7 traffic.
- Ignoring cold start in the p99 budget.
- Designing around a size limit from memory (limits change).
- Forgetting concurrency per instance when sizing for bursts.
- Assuming GPU is available everywhere.

---

### Q45 ⭐ 🔴 Scenario: after a new model version rolls out, p99 latency doubles and the 5xx rate rises to 2 percent, but accuracy dashboards look fine. Walk through triage: confirm the change with the deploy timeline, compare resource saturation and queueing, check readiness flapping and OOM kills, compare model size and input pre-processing cost between versions, look at batch wait settings, then roll back first and debug after. Include the communication steps and a short blameless post-incident list. Write a Python script that takes two latency and error logs (before and after) and produces a comparison report with percentile deltas and a rollback recommendation; run it on generated logs. Real incident tooling is not executed.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** Roll back first, debug after: confirm the change lines up with the deploy time, protect users by restoring the old version, then compare saturation, restarts and per-version differences on the evidence you kept.

**Then explain:**
- Step 1, confirm: line up the deploy timeline with the latency and 5xx graphs. Did the change start at the rollout, per pod as it rolled? If it started before the deploy, it is something else.
- Step 2, stabilise: if the user impact is real and the cause is not obvious in minutes, roll back. A routing or image-tag revert is fast. Say so in the incident channel.
- Step 3, find the cause with the saved evidence: CPU and memory saturation, request queue depth, readiness flapping, OOM kills and restart counts (errors concentrated on one pod is a clue, as in the run), model file size and load time (a bigger model means more memory and slower start), input pre-processing cost, and batch wait settings (a longer max wait lifts p99).
- Accuracy dashboards look fine because they measure correctness of answered requests, not failed ones or slow ones. Add latency and error SLOs to the release gate (Part 7).
- Communication: one incident owner, a status note every 15 to 30 minutes (impact, what we know, next step, next update time), a clear "rolled back at HH:MM, watching" and a customer-facing note if needed. No blame.
- Blameless post-incident list: timeline, what detected it and how long it took, why the gate did not catch it, what we change (canary with p99 and 5xx rollback from Q37, load test on the new model size, memory limit review, readiness check that loads the model), owners and dates.

**Example:** Before: p99 45 ms, 5xx 0.08 percent. After (generated logs): p99 about 85 ms (x1.9), 5xx 2.15 percent, and 7.5 percent of requests on pod-2 fail. Rule: p99 ratio at least 1.5 or error rate up 0.5 points or above 1 percent absolute means ROLLBACK. All three triggers fire.

**Code:** a log generator (seeded, makes before, a bad after and a healthy after), the comparison report script and five tests. Thresholds are invented team examples, agree yours with your SLO. Run with Python 3.13.17 in a venv: fastapi 0.162.0, uvicorn 0.54.0, httpx 0.28.1, pytest 9.1.1, scikit-learn 1.9.1, skl2onnx 1.20.0, onnxruntime 1.31.0, torch 2.14.1 (CPU only). Sandbox timings are machine-specific demos, not benchmarks.
```python
# ===== q45_gen_logs.py =====
"""Generate fake request logs: ts_seconds,status,latency_ms,replica. Usage: q45_gen_logs.py OUTDIR"""
import csv, random, sys, pathlib
def gen(path, n, seed, p50, tail_p, tail_mult, err_rate, bad_replica=None, bad_err=0.0):
    r = random.Random(seed); rows = []
    for i in range(n):
        rep = f"pod-{r.randrange(4)}"
        lat = r.lognormvariate(0, 0.25) * p50
        if r.random() < tail_p: lat *= tail_mult
        e = bad_err if rep == bad_replica else err_rate
        status = 503 if r.random() < e else 200
        if status == 503: lat = min(lat, 30.0)                  # failures return fast (readiness/OOM restarts)
        rows.append((round(i * 0.05, 2), status, round(lat, 2), rep))
    with open(path, "w", newline="") as f: w = csv.writer(f); w.writerow(["ts", "status", "latency_ms", "replica"]); w.writerows(rows)
if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    gen(out / "before.csv", 6000, 1, p50=20, tail_p=0.01, tail_mult=3, err_rate=0.001)
    gen(out / "after_bad.csv", 6000, 2, p50=24, tail_p=0.03, tail_mult=3.3, err_rate=0.004, bad_replica="pod-2", bad_err=0.07)
    gen(out / "after_ok.csv", 6000, 3, p50=20.5, tail_p=0.01, tail_mult=3, err_rate=0.001)
    print("wrote", sorted(p.name for p in out.iterdir()))

# ===== q45_compare.py =====
"""Compare before/after request logs and recommend keep or rollback. Usage: q45_compare.py BEFORE.csv AFTER.csv"""
import csv, sys, math
from collections import defaultdict
P99_RATIO_LIMIT, ERR_DELTA_LIMIT, ERR_ABS_LIMIT = 1.5, 0.005, 0.01     # team thresholds: invented; agree yours with the SLO

def percentile(sorted_vals, q):                    # nearest-rank percentile, easy to hand-check
    return sorted_vals[max(0, math.ceil(q / 100 * len(sorted_vals)) - 1)]

def load(path):
    with open(path) as f: return [(float(r["ts"]), int(r["status"]), float(r["latency_ms"]), r["replica"]) for r in csv.DictReader(f)]

def summarise(rows):
    ok = sorted(l for _, s, l, _ in rows if s < 500); errs = [r for r in rows if r[1] >= 500]
    by = defaultdict(lambda: [0, 0])
    for _, s, _, rep in rows: by[rep][0] += 1; by[rep][1] += s >= 500
    return {"n": len(rows), "err_rate": len(errs) / len(rows), "p50": percentile(ok, 50), "p95": percentile(ok, 95), "p99": percentile(ok, 99),
            "replica_err": {k: v[1] / v[0] for k, v in sorted(by.items())}}

def recommend(b, a):
    reasons = []
    if a["p99"] / b["p99"] >= P99_RATIO_LIMIT: reasons.append(f"p99 x{a['p99']/b['p99']:.2f} (limit x{P99_RATIO_LIMIT})")
    if a["err_rate"] - b["err_rate"] >= ERR_DELTA_LIMIT: reasons.append(f"error rate +{(a['err_rate']-b['err_rate'])*100:.2f} pp (limit {ERR_DELTA_LIMIT*100:.1f} pp)")
    if a["err_rate"] >= ERR_ABS_LIMIT: reasons.append(f"error rate {a['err_rate']*100:.2f}% over {ERR_ABS_LIMIT*100:.0f}% absolute limit")
    return ("ROLLBACK", reasons) if reasons else ("KEEP", ["all deltas inside thresholds"])

def report(bp, ap):
    b, a = summarise(load(bp)), summarise(load(ap))
    print(f"{'metric':10s}{'before':>10s}{'after':>10s}{'delta':>10s}")
    for k in ("p50", "p95", "p99"): print(f"{k + ' ms':10s}{b[k]:10.1f}{a[k]:10.1f}{a[k]-b[k]:+10.1f}  (x{a[k]/b[k]:.2f})")
    print(f"{'5xx rate':10s}{b['err_rate']*100:9.2f}%{a['err_rate']*100:9.2f}%{(a['err_rate']-b['err_rate'])*100:+9.2f}pp")
    worst = max(a["replica_err"].items(), key=lambda kv: kv[1])
    print("5xx rate by replica after:", {k: f"{v*100:.1f}%" for k, v in a["replica_err"].items()})
    if worst[1] > 0.01 and worst[1] > 3 * a["err_rate"]: print(f"note: errors concentrated on {worst[0]}: check OOM kills, restarts and readiness on that pod")
    verdict, why = recommend(b, a); print("RECOMMENDATION:", verdict, "|", "; ".join(why)); return verdict

if __name__ == "__main__": report(sys.argv[1], sys.argv[2])

# ===== test_q45_compare.py =====
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q45_compare import percentile, recommend, summarise
def test_percentile_hand_check():
    v = list(range(1, 101)); assert percentile(v, 50) == 50 and percentile(v, 99) == 99 and percentile(v, 100) == 100
def test_rollback_on_p99():
    b = {"p99": 50, "err_rate": 0.001}; a = {"p99": 100, "err_rate": 0.001}; assert recommend(b, a)[0] == "ROLLBACK"
def test_rollback_on_errors_only():
    b = {"p99": 50, "err_rate": 0.001}; a = {"p99": 52, "err_rate": 0.02}; v, why = recommend(b, a); assert v == "ROLLBACK" and len(why) == 2
def test_keep_inside_thresholds():
    b = {"p99": 50, "err_rate": 0.001}; a = {"p99": 55, "err_rate": 0.002}; assert recommend(b, a)[0] == "KEEP"
def test_summarise_counts_5xx_and_excludes_them_from_latency():
    rows = [(0, 200, 10.0, "a"), (1, 200, 20.0, "a"), (2, 503, 900.0, "b"), (3, 200, 30.0, "b")]
    s = summarise(rows); assert s["err_rate"] == 0.25 and s["p99"] == 30.0 and s["replica_err"]["b"] == 0.5
```
```bash
cd /tmp/claude-0/b6_q35_45 && mkdir -p logs45
/tmp/claude-0/b6p06/v/bin/python -I q45_gen_logs.py logs45
/tmp/claude-0/b6p06/v/bin/python -I q45_compare.py logs45/before.csv logs45/after_bad.csv
/tmp/claude-0/b6p06/v/bin/python -I q45_compare.py logs45/before.csv logs45/after_ok.csv
/tmp/claude-0/b6p06/v/bin/python -m pytest -q -p no:cacheprovider test_q45_compare.py
```

**Output (my run):** real run on generated (fake) logs. Real incident tooling (paging, dashboards, deploy system) is not executed.
```text
wrote ['after_bad.csv', 'after_ok.csv', 'before.csv']
--- before vs after_bad
metric        before     after     delta
p50 ms          19.9      24.0      +4.1  (x1.20)
p95 ms          30.4      40.2      +9.8  (x1.32)
p99 ms          45.3      85.1     +39.9  (x1.88)
5xx rate       0.08%     2.15%    +2.07pp
5xx rate by replica after: {'pod-0': '0.5%', 'pod-1': '0.3%', 'pod-2': '7.5%', 'pod-3': '0.5%'}
note: errors concentrated on pod-2: check OOM kills, restarts and readiness on that pod
RECOMMENDATION: ROLLBACK | p99 x1.88 (limit x1.5); error rate +2.07 pp (limit 0.5 pp); error rate 2.15% over 1% absolute limit
--- before vs after_ok
metric        before     after     delta
p50 ms          19.9      20.5      +0.5  (x1.03)
p95 ms          30.4      31.9      +1.5  (x1.05)
p99 ms          45.3      46.2      +1.0  (x1.02)
5xx rate       0.08%     0.03%    -0.05pp
5xx rate by replica after: {'pod-0': '0.1%', 'pod-1': '0.0%', 'pod-2': '0.0%', 'pod-3': '0.0%'}
RECOMMENDATION: KEEP | all deltas inside thresholds
.....                                                                    [100%]
5 passed in 0.01s
```

**Follow-ups:**
- Roll back or fix forward? Roll back when the cause is unknown or the fix is not tiny and tested. Fix forward only with a one-line known cause and a fast pipeline.
- What if rollback is not possible (schema change)? Make model and schema changes backward compatible, which is why the deploy plan should always keep the old version runnable.
- Which signal first? User-facing 5xx and p99, then saturation. Do not wait for accuracy.

**Common mistakes:**
- Debugging in production while users suffer.
- Comparing averages (the tail moved, not the mean).
- Deleting the old version right after rollout (no way back).
- Blaming a person in the post-incident note.
- No saved logs from before the change, so no baseline.

---
