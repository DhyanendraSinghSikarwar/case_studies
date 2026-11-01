### Q24 ⭐⭐ 🟡 Caching predictions. When is it safe (deterministic model, repeated inputs, tolerable staleness), cache key design (a hash of the canonicalised features plus the model version, so a new model never serves old answers), in-process LRU versus Redis, TTLs, caching negative results, cache stampede protection, and the risk of caching features that change. Show a FastAPI endpoint with a functools-style LRU or a dict cache keyed by a stable hash of the request and the model version, a test that proves a model version bump misses the cache, and a tiny measurement of hit rate and latency on repeated requests (labelled machine-specific). Redis is not executed.
**Asked at:** Serving interview-prep and glossary pages (nerdleveltech.com MLOps engineer interviews 'model serving infrastructure', techinterview.org MLOps interview and model-serving design posts, wecreateproblems.com MLOps interview questions, insertchat.com model-serving glossary; search snippets only, not opened); editorial guides, not verified candidate reports; MLOps, ML platform and ML engineer roles
**Say this first (1 line):** Cache only when the model is deterministic and a slightly old answer is fine, key the cache on the model version plus a canonical hash of the features, and never let a new model read an old model's answers.

**Then explain:**
- **Safe when:** same input always gives the same output (no sampling, no clock, no random), inputs repeat (popular items, retries, dashboards), and you can live with staleness up to the TTL.
- **Key design:** `sha256(model_version | canonical features)`. Canonical means fixed order, fixed rounding, fixed JSON format. A version bump changes every key, so the old entries simply never match and age out.
- **In-process LRU vs Redis:** in-process is fastest and has no network hop, but every replica has its own copy, so hit rate drops as you add replicas and a restart empties it. Redis is shared and survives restarts, but adds a network call and a new thing to run (not executed here).
- **TTL and negatives:** TTL bounds staleness. Cache only successes. Cache a "no result" only briefly, and never cache a 5xx or a timeout.
- **Stampede:** a hot key expires and 500 requests all compute it at once. Fix with a per-key lock or single-flight, jittered TTLs, or serving the stale value while one request refreshes.
- **Danger:** caching on request features is fine; caching on an ID whose features change behind the scenes (a user's last-hour spend) serves stale scores. Key on the feature values, or put the feature freshness in the TTL.

**Example:** Request `[6.7, 3.0, 5.2, 2.3]` on model `v1`: first call computes (miss), second call returns the stored label (hit). Bump to `v2`: same features, new key, miss again. Also `6.7000001` rounds to `6.7` at 6 decimals, so it hits the same entry. 20 distinct inputs sent 10 times each should give 20 misses and 180 hits, a 90 percent hit rate. You can check that by hand.

**Code:** an in-process LRU (`OrderedDict`) inside a FastAPI app with an ONNX iris model, a pytest file that proves the version bump misses, and a runner that measures hit rate. `make_model.py` (shared by several answers) builds the ONNX file; it is in `code/`. Redis is not run; the swap is `GET key` / `SETEX key ttl value` with the same key function.
```python
# ===== make_model.py =====
# Builds iris ONNX model (LogisticRegression) into the dir given as argv[1]
import sys, os
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from skl2onnx import to_onnx
out = sys.argv[1]
X, y = load_iris(return_X_y=True)
X = X.astype(np.float32)
m = LogisticRegression(max_iter=500).fit(X, y)
onx = to_onnx(m, X[:1], target_opset=17, options={id(m): {"zipmap": False}})
os.makedirs(out, exist_ok=True)
with open(os.path.join(out, "iris.onnx"), "wb") as f:
    f.write(onx.SerializeToString())
print("wrote", os.path.join(out, "iris.onnx"), "bytes", len(onx.SerializeToString()))

# ===== q24_cache_app.py =====
# Q24: prediction cache in FastAPI. Key = sha256(model_version + canonical features).
import hashlib, json, os, time
from collections import OrderedDict
from contextlib import asynccontextmanager
import numpy as np, onnxruntime as ort
from fastapi import FastAPI
from pydantic import BaseModel, Field

class LRU:
    def __init__(self, size): self.size, self.d, self.hits, self.misses = size, OrderedDict(), 0, 0
    def get(self, k):
        if k in self.d:
            self.d.move_to_end(k); self.hits += 1; return self.d[k]
        self.misses += 1; return None
    def put(self, k, v):
        self.d[k] = v; self.d.move_to_end(k)
        if len(self.d) > self.size: self.d.popitem(last=False)

def cache_key(model_version, features):
    canon = json.dumps([round(float(x), 6) for x in features], separators=(",", ":"))
    return hashlib.sha256(f"{model_version}|{canon}".encode()).hexdigest()

class Req(BaseModel):
    features: list[float] = Field(min_length=4, max_length=4)

def make_app(model_path, model_version="v1", cache_size=1000):
    state = {"version": model_version, "cache": LRU(cache_size)}
    @asynccontextmanager
    async def lifespan(app):
        state["sess"] = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
        yield
    app = FastAPI(lifespan=lifespan)
    app.state.s = state
    @app.post("/predict")
    def predict(r: Req):
        k = cache_key(state["version"], r.features)
        hit = state["cache"].get(k)
        if hit is not None:
            return {"label": hit, "cached": True, "model_version": state["version"]}
        x = np.array([r.features], dtype=np.float32)
        label = int(state["sess"].run(["label"], {"X": x})[0][0])
        state["cache"].put(k, label)      # we only cache successes, never errors
        return {"label": label, "cached": False, "model_version": state["version"]}
    @app.post("/admin/model_version/{v}")
    def bump(v: str):
        state["version"] = v; return {"version": v}
    @app.get("/cache/stats")
    def stats():
        c = state["cache"]; return {"hits": c.hits, "misses": c.misses, "size": len(c.d)}
    return app

# ===== q24_run.py =====
import sys, time, statistics
from fastapi.testclient import TestClient
from q24_cache_app import make_app, cache_key
model = sys.argv[1]
app = make_app(model)
with TestClient(app) as c:
    f = [6.7, 3.0, 5.2, 2.3]
    r1 = c.post("/predict", json={"features": f}).json()
    r2 = c.post("/predict", json={"features": f}).json()
    r3 = c.post("/predict", json={"features": [6.7000001, 3.0, 5.2, 2.3]}).json()
    print("1st:", r1); print("2nd:", r2); print("same after rounding to 6dp:", r3["cached"])
    c.post("/admin/model_version/v2")
    r4 = c.post("/predict", json={"features": f}).json()
    print("after bump to v2:", r4)
    assert r1["cached"] is False and r2["cached"] is True and r4["cached"] is False
    print("keys differ across versions:", cache_key("v1", f) != cache_key("v2", f))
    print("bad input:", c.post("/predict", json={"features": [1, 2]}).status_code)
    print("stats after test:", c.get("/cache/stats").json())
    # tiny measurement: 20 distinct inputs, each sent 10 times (200 requests)
    c.post("/admin/model_version/v3")
    import random; random.seed(0)
    inputs = [[round(random.uniform(4,8),1), round(random.uniform(2,4),1), round(random.uniform(1,7),1), round(random.uniform(0.1,2.5),1)] for _ in range(20)]
    miss_t, hit_t = [], []
    for rep in range(10):
        for x in inputs:
            t = time.perf_counter(); j = c.post("/predict", json={"features": x}).json(); dt = (time.perf_counter()-t)*1000
            (hit_t if j["cached"] else miss_t).append(dt)
    s = c.get("/cache/stats").json()
    print("requests 200, misses", len(miss_t), "hits", len(hit_t), "hit rate", len(hit_t)/200)
    print(f"median ms miss {statistics.median(miss_t):.2f}, hit {statistics.median(hit_t):.2f} (this sandbox, TestClient, not a benchmark)")

# ===== test_q24.py =====
import os
from fastapi.testclient import TestClient
from q24_cache_app import make_app
MODEL = os.environ["IRIS_ONNX"]
def test_version_bump_misses_cache():
    with TestClient(make_app(MODEL)) as c:
        f = {"features": [5.1, 3.5, 1.4, 0.2]}
        assert c.post("/predict", json=f).json()["cached"] is False
        assert c.post("/predict", json=f).json()["cached"] is True
        c.post("/admin/model_version/v2")
        assert c.post("/predict", json=f).json()["cached"] is False
def test_lru_evicts_oldest():
    with TestClient(make_app(MODEL, cache_size=2)) as c:
        for v in ([1,1,1,1],[2,2,2,2],[3,3,3,3]):
            c.post("/predict", json={"features": v})
        assert c.post("/predict", json={"features": [1,1,1,1]}).json()["cached"] is False
```
```bash
python make_model.py /tmp/work            # writes /tmp/work/iris.onnx
python q24_run.py /tmp/work/iris.onnx
IRIS_ONNX=/tmp/work/iris.onnx python -m pytest -q test_q24.py
```

**Output (my run):** real run, Python 3.13, fastapi 0.162, onnxruntime 1.31, TestClient. Redis not executed (no Redis here); the cache logic and key function did run. Timings are this sandbox only, not a benchmark.
```text
1st: {'label': 2, 'cached': False, 'model_version': 'v1'}
2nd: {'label': 2, 'cached': True, 'model_version': 'v1'}
same after rounding to 6dp: True
after bump to v2: {'label': 2, 'cached': False, 'model_version': 'v2'}
keys differ across versions: True
bad input: 422
stats after test: {'hits': 2, 'misses': 2, 'size': 2}
requests 200, misses 20 hits 180 hit rate 0.9
median ms miss 3.79, hit 3.32 (this sandbox, TestClient, not a benchmark)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2 passed, 1 warning in 0.93s
```
Reading the timing: the model is tiny and TestClient overhead dominates, so a hit saves almost nothing here. A cache pays when the model call is slow, not when it is a 20-microsecond logistic regression.

**Follow-ups:**
- *How do you stop a stampede?* One lock per key (single-flight), jittered TTLs, or serve stale while one worker refreshes.
- *Why not key on a user id?* The features behind that id change. You would serve a score computed from old data, with no sign it is old.
- *Cache in the model server or the gateway?* Gateway or app cache is simpler and shared across model versions; keep the version in the key either way.

**Common mistakes:**
- Leaving the model version out of the key, so a rollout keeps serving the old model's answers for a TTL.
- Hashing the raw JSON string: `{"a":1,"b":2}` and `{"b":2,"a":1}` become two keys. Canonicalise first.
- Caching non-deterministic models (sampling, dropout left on) or error responses.
- Unbounded dict as a cache: memory grows until the pod is killed. Always set a size.

### Q25 ⭐⭐ 🟡 Autoscaling a model service. Explain scaling signals (CPU, requests in flight per replica, queue depth, GPU utilisation, custom metrics), why CPU alone misleads for batching or GPU services, HPA, KEDA and Knative at concept level (Part 3 owns Kubernetes autoscaling), scale-up lag from image pull and model load, minimum replicas to avoid cold start, scale-down grace and draining, and flapping. Give a worked calculation of the replica count from requests in flight and a target concurrency per replica, as a tested Python function, and a simple simulation of a traffic spike with a 90-second start-up delay that shows how many requests would exceed the latency budget. All numbers are inputs, no cluster is used.
**Asked at:** Autoscaling and cold-start sources (feedly.com engineering 'fast autoscaling on GPUs', designgurus.io 'what to expect in the Baseten system design interview' (not an official Baseten source), uwaterloo.ca GPU cold-start paper listing; search snippets only, not opened); engineering blog and secondary prep page; GPU serving and inference platform roles
**Say this first (1 line):** I scale on requests in flight per replica (or queue depth), not CPU, and I size for start-up time, because a replica that takes 90 seconds to become ready does not help the spike that already happened.

**Then explain:**
- **Signals:** CPU is fine for simple CPU-bound APIs. For batching or GPU services CPU stays low while the queue grows, so it misleads. Better: in-flight requests per replica, queue depth, p95 latency, GPU utilisation or GPU memory (check what your platform can read).
- **Tools at concept level:** HPA scales on CPU, memory or custom metrics; KEDA adds event sources such as queue length; Knative scales on request concurrency and can scale to zero. Details are Part 3. Check current docs for exact behaviour.
- **Maths (Little's law):** in flight = requests per second x seconds per request. Replicas = ceil(in flight / target per replica). Set the target below real capacity to leave headroom.
- **Scale-up lag:** pod scheduling, image pull, model download and load. If that is 90 seconds, the spike is over before the new pods help. Fixes: minimum replicas, smaller images, model baked in or cached on a volume, scale earlier on a leading signal.
- **Scale-down:** use a stabilisation window and drain in-flight requests (terminationGracePeriod, readiness off first). Flapping (up, down, up) wastes start-ups; slow scale-down prevents it.
- **Failure mode:** with no headroom, backlog never drains even after scaling (shown below).

**Example:** 200 req/s at 0.1 s each is 20 in flight. A replica handles 4 at once (capacity), target 3 for headroom: ceil(20/3) = 7 replicas, capacity 7 x 4 / 0.1 = 280 req/s. At target 4 you would get 5 replicas, capacity exactly 200, and the queue built during the lag would never drain.

**Code:** the function and a per-second spike simulation. Traffic is 20 rps for 60 s, then 200 rps. Latency budget 500 ms. A request is late if queue wait plus service time exceeds it. Everything is an input; no cluster.
```python
# ===== q25_autoscale.py =====
# Q25: replica maths and a spike simulation. All numbers are inputs; no cluster.
import math

def replicas_needed(in_flight, target_per_replica, min_r=1, max_r=50):
    """Desired replicas from requests in flight (Little's law: in_flight = rps * latency)."""
    return max(min_r, min(max_r, math.ceil(in_flight / target_per_replica)))

def simulate(rps_at, secs, service_ms, conc_per_replica, start_delay, min_r, budget_ms, target, tick=1):
    """Per-second fluid simulation. Each replica serves conc/service_s req/s.
    Backlog grows when arrivals exceed capacity. A request arriving in a second waits
    backlog/capacity seconds; counts as late if wait + service > budget."""
    replicas, pending, backlog, late, total = min_r, [], 0.0, 0.0, 0.0
    log = []
    for t in range(secs):
        pending_ready = [p for p in pending if p <= t]
        replicas += len(pending_ready); pending = [p for p in pending if p > t]
        arrivals = rps_at(t)
        cap = replicas * conc_per_replica / (service_ms / 1000)
        wait_ms = (backlog / cap) * 1000 if cap else 1e9
        total += arrivals
        if wait_ms + service_ms > budget_ms: late += arrivals
        backlog = max(0.0, backlog + arrivals - cap)
        in_flight = arrivals * service_ms / 1000   # Little: rps x seconds; queued work is not counted here
        want = replicas_needed(in_flight, target, min_r)
        have = replicas + len(pending)
        for _ in range(max(0, want - have)): pending.append(t + start_delay)
        if t % 30 == 0: log.append((t, arrivals, replicas, len(pending), round(wait_ms)))
    return late, total, log

if __name__ == "__main__":
    assert replicas_needed(0, 4) == 1
    assert replicas_needed(40, 4) == 10
    assert replicas_needed(41, 4) == 11
    assert replicas_needed(1000, 4, max_r=20) == 20
    print("replica function tests passed")
    print("worked: 200 rps * 0.100 s = 20 in flight; target 3 per replica (capacity 4, so headroom) ->", replicas_needed(200*0.1, 3), "replicas")
    spike = lambda t: 20 if t < 60 else 200
    for delay in (90, 10):
        late, total, log = simulate(spike, 300, 100, 4, delay, min_r=1, budget_ms=500, target=3)
        print(f"start-up delay {delay}s, min replicas 1: late {late:.0f} of {total:.0f} requests ({100*late/total:.1f}%)")
        if delay == 90:
            for row in log[:6]: print("  t=%3d rps=%3d ready=%2d starting=%2d wait_ms=%d" % row)
    late, total, _ = simulate(spike, 300, 100, 4, 90, min_r=7, budget_ms=500, target=3)
    print(f"start-up delay 90s, min replicas 7 (pre-warmed): late {late:.0f} of {total:.0f} ({100*late/total:.1f}%)")
```

**Output (my run):** real run with `python -I`. The spike result is a model of the inputs above, not a measurement of any system. Kubernetes, HPA, KEDA and Knative are not executed.
```text
replica function tests passed
worked: 200 rps * 0.100 s = 20 in flight; target 3 per replica (capacity 4, so headroom) -> 7 replicas
start-up delay 90s, min replicas 1: late 47800 of 49200 requests (97.2%)
  t=  0 rps= 20 ready= 1 starting= 0 wait_ms=0
  t= 30 rps= 20 ready= 1 starting= 0 wait_ms=0
  t= 60 rps=200 ready= 1 starting= 6 wait_ms=0
  t= 90 rps=200 ready= 1 starting= 6 wait_ms=120000
  t=120 rps=200 ready= 1 starting= 6 wait_ms=240000
  t=150 rps=200 ready= 7 starting= 0 wait_ms=51429
start-up delay 10s, min replicas 1: late 5600 of 49200 requests (11.4%)
start-up delay 90s, min replicas 7 (pre-warmed): late 0 of 49200 (0.0%)
```
Read it: with 90 s start-up and one warm replica, almost every request in the window is late, because the backlog built during the lag drains slowly. With a 10 s start-up it is 11 percent. With 7 warm replicas it is zero, at the price of paying for idle pods.

**Follow-ups:**
- *Why not scale to zero?* Cold start of image plus model hits the first user. Fine for batch or rare internal tools, bad for latency-sensitive APIs.
- *What stops flapping?* Stabilisation window on scale-down, a rate limit on scale-down steps, and a metric that is not noisy.
- *CPU 30 percent but latency high?* Queueing or GPU bound; look at in-flight and queue depth.

**Common mistakes:**
- Autoscaling GPU services on CPU.
- Setting target equal to max capacity, so there is no headroom.
- Ignoring start-up time in the plan.
- Scaling down while requests are in flight, which drops them.

### Q26 ⭐⭐ 🟡 GPU serving for a model API. When a GPU pays off (large models, big batches, heavy convolution or transformer maths) versus CPU (small tree models, tiny inputs, low traffic), why a GPU idles without batching, multiple model instances per GPU, GPU memory limits and out-of-memory failures, mixed precision, MIG and time slicing at concept level, the image and driver compatibility boundary (Part 2 owns GPU Docker), and cost per prediction. Show how you would pick the provider in ONNX Runtime (CUDAExecutionProvider with a CPU fallback) and print the available providers on this machine. No GPU is available here; GPU execution is not executed.
**Asked at:** Autoscaling and cold-start sources (feedly.com engineering 'fast autoscaling on GPUs', designgurus.io 'what to expect in the Baseten system design interview' (not an official Baseten source), uwaterloo.ca GPU cold-start paper listing; search snippets only, not opened); engineering blog and secondary prep page; GPU serving and inference platform roles
**Say this first (1 line):** A GPU pays off when the model is big and I can batch enough work to keep it busy; for small tree models or low traffic a CPU is cheaper and simpler, and I always verify which provider the session really got.

**Then explain:**
- **GPU wins:** large transformers or CNNs, big batches, heavy matrix maths. **CPU wins:** small tree or linear models, tiny inputs, low or bursty traffic.
- **Idle without batching:** one request at a time uses a sliver of the GPU. Dynamic batching and several model instances per GPU raise utilisation.
- **Memory:** weights plus activations plus batch must fit. Too big a batch or too many instances gives out-of-memory errors, so set a batch cap and test with the largest input.
- **Concept only:** mixed precision (FP16 or BF16) cuts memory and time with a small accuracy check needed; MIG splits a supported GPU into isolated slices, time slicing shares it without memory isolation. Check vendor docs for supported cards.
- **Boundary:** the container image, CUDA version and driver must be compatible (Part 2 owns GPU Docker).
- **Cost per prediction:** hourly price divided by predictions per hour at your real utilisation. An idle GPU is the expensive failure.
- **Silent fallback trap:** ONNX Runtime may fall back to CPU if CUDA is not usable. Print `session.get_providers()` and alert if it is not what you expected.

**Example:** Asking for `["CUDAExecutionProvider", "CPUExecutionProvider"]` on a machine with no GPU should end up on CPU. The helper below filters the wish list by what is available, so the list order is the priority and CPU is always last.

**Code:**
```python
# ===== q26_providers.py =====
# Q26: pick an ONNX Runtime provider with a CPU fallback.
import sys, onnxruntime as ort
def pick_providers():
    avail = ort.get_available_providers()
    wanted = ["CUDAExecutionProvider", "CPUExecutionProvider"]   # order = priority
    return [p for p in wanted if p in avail]
print("onnxruntime", ort.__version__)
print("available:", ort.get_available_providers())
print("device:", ort.get_device())
chosen = pick_providers()
print("chosen:", chosen)
sess = ort.InferenceSession(sys.argv[1], providers=chosen)
print("session is using:", sess.get_providers())
try:
    s2 = ort.InferenceSession(sys.argv[1], providers=["CUDAExecutionProvider"])
    print("asked for CUDA only, session loaded anyway; it is really using:", s2.get_providers())
except Exception as e:
    print("CUDA only ->", type(e).__name__, str(e)[:160].replace("\n"," "))
```

**Output (my run):** real run on a CPU-only sandbox, onnxruntime 1.31. GPU execution is not executed (no GPU here); only provider selection ran.
```text
/tmp/claude-0/b6p06/v/lib/python3.13/site-packages/onnxruntime/capi/onnxruntime_inference_collection.py:197: UserWarning: Specified provider 'CUDAExecutionProvider' is not in available provider names.Available providers: 'AzureExecutionProvider, CPUExecutionProvider'
onnxruntime 1.31.0
available: ['AzureExecutionProvider', 'CPUExecutionProvider']
device: CPU
chosen: ['CPUExecutionProvider']
session is using: ['CPUExecutionProvider']
asked for CUDA only, session loaded anyway; it is really using: ['CPUExecutionProvider']
```
Notice the last line: asking for CUDA only did not fail, it warned and ran on CPU. In production that is a latency incident waiting to happen, so check `get_providers()` at startup.

**Follow-ups:**
- *How do you know the GPU is worth it?* Measure cost per 1000 predictions at realistic batch and traffic on both. Not done here.
- *Several instances per GPU?* Good when one instance cannot fill the GPU; bad when memory is tight.
- *OOM at runtime?* Cap batch size and input length, restart the instance, and alert.

**Common mistakes:**
- Assuming a GPU is faster for a small model.
- Not checking the active provider.
- Mismatched CUDA, driver and runtime versions.
- Benchmarking with batch 1 and concluding the GPU is useless, or with huge batches and ignoring latency.

### Q27 ⭐⭐ 🟡 Batch inference job design. Score 50 million rows nightly. Cover reading in chunks or partitions, loading the model once per worker, vectorised prediction, writing partitioned output (a date partition) idempotently with a temp-then-rename step, checkpointing so a failed job resumes, parallelism with multiprocessing or Spark at concept level (Part 9 owns Spark), joining scores back to keys, and validating row counts. Write a Python batch scorer with chunked reading of a CSV, ONNX Runtime prediction, atomic output, and a resume test. Run it on 100,000 generated rows and show real counts; Spark and cloud batch services are not executed.
**Asked at:** Serving interview-prep and glossary pages (nerdleveltech.com MLOps engineer interviews 'model serving infrastructure', techinterview.org MLOps interview and model-serving design posts, wecreateproblems.com MLOps interview questions, insertchat.com model-serving glossary; search snippets only, not opened); editorial guides, not verified candidate reports; MLOps, ML platform and ML engineer roles
**Say this first (1 line):** I read the input in chunks, load the model once, predict in vectorised batches, write each output part to a temp file then rename it, and skip finished parts on restart, so a crash at part 6 costs me parts 6 onward, not the whole night.

**Then explain:**
- **Chunking:** never load 50 million rows into memory. Read fixed-size chunks or partition files.
- **Load once:** one model session per worker, not per chunk or per row.
- **Vectorise:** one `run` call per chunk, not a Python loop over rows.
- **Idempotent output:** write `part-00003.csv.tmp`, then `os.replace` to the final name (atomic on the same filesystem). Output goes in a date partition (`dt=2026-10-26`) so a re-run replaces that day only.
- **Checkpoint:** a part that exists is done. No fancy state file is needed when part names are deterministic. Chunk boundaries must be deterministic too.
- **Parallelism (concept):** multiprocessing per partition file, or Spark/Ray at scale (Part 9 owns Spark). Each worker loads its own model copy.
- **Validate:** output rows equal input rows, ids are unique, no stray `.tmp` files, then publish (flip a pointer or write a `_SUCCESS` marker).
- **Failure modes:** crash between write and rename leaves only a `.tmp`, ignored on resume; a changed chunk size between runs breaks part numbering, so fix it in config.

**Example:** 100,000 rows, chunk 10,000: 10 parts. Crash after 4 parts. Resume scores 60,000 rows and skips 40,000. Run again: skips all 100,000. Output rows must equal 100,000 with 100,000 unique ids.

**Code:** the scorer (input CSV is generated on first run) and the shell steps.
```python
# ===== q27_batch.py =====
# Q27: chunked, resumable, atomic batch scorer (CSV -> parts -> ONNX). Run: q27_batch.py MODEL WORKDIR [--crash-after N]
import csv, os, sys, json, time, argparse
import numpy as np, onnxruntime as ort
ap = argparse.ArgumentParser(); ap.add_argument("model"); ap.add_argument("work")
ap.add_argument("--rows", type=int, default=100_000); ap.add_argument("--chunk", type=int, default=10_000)
ap.add_argument("--crash-after", type=int, default=None); a = ap.parse_args()
inp = os.path.join(a.work, "input.csv"); out_dir = os.path.join(a.work, "scores", "dt=2026-10-26")
os.makedirs(out_dir, exist_ok=True)
if not os.path.exists(inp):                       # generate input once
    rng = np.random.default_rng(7)
    X = np.round(rng.uniform([4,2,1,0.1],[8,4.5,7,2.5], size=(a.rows,4)), 2)
    with open(inp, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["id","f1","f2","f3","f4"])
        for i, r in enumerate(X): w.writerow([i, *r])
sess = ort.InferenceSession(a.model, providers=["CPUExecutionProvider"])   # load ONCE
def read_chunks(path, n):
    with open(path, newline="") as f:
        rd = csv.reader(f); next(rd); buf = []
        for row in rd:
            buf.append(row)
            if len(buf) == n: yield buf; buf = []
        if buf: yield buf
done = skipped = 0; t0 = time.perf_counter()
for k, rows in enumerate(read_chunks(inp, a.chunk)):
    final = os.path.join(out_dir, f"part-{k:05d}.csv")
    if os.path.exists(final): skipped += len(rows); continue          # resume: finished parts are skipped
    ids = [r[0] for r in rows]; x = np.array([r[1:] for r in rows], dtype=np.float32)
    labels = sess.run(["label"], {"X": x})[0]                         # vectorised
    tmp = final + ".tmp"
    with open(tmp, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["id","label"]); w.writerows(zip(ids, labels.tolist()))
    os.replace(tmp, final)                                            # atomic rename
    done += len(rows)
    if a.crash_after is not None and k + 1 == a.crash_after: print("simulated crash after part", k); sys.exit(3)
# validate: counts + unique ids
total = 0; seen = set()
for fn in sorted(os.listdir(out_dir)):
    if fn.endswith(".tmp"): print("stray tmp file", fn); continue
    with open(os.path.join(out_dir, fn)) as f:
        rd = csv.reader(f); next(rd)
        for r in rd: total += 1; seen.add(r[0])
with open(inp) as f: n_in = sum(1 for _ in f) - 1
print(f"scored now {done}, skipped (already done) {skipped}, output rows {total}, unique ids {len(seen)}, input rows {n_in}, match {total==n_in==len(seen)}")
print("parts:", len([f for f in os.listdir(out_dir) if f.endswith('.csv')]), f"elapsed {time.perf_counter()-t0:.1f}s (this sandbox)")
```
```bash
python make_model.py /tmp/work
python q27_batch.py /tmp/work/iris.onnx /tmp/work/q27 --crash-after 4   # exits 3
python q27_batch.py /tmp/work/iris.onnx /tmp/work/q27                   # resumes
python q27_batch.py /tmp/work/iris.onnx /tmp/work/q27                   # nothing to do
```

**Output (my run):** real run on 100,000 generated rows with the iris ONNX model. Elapsed times are this sandbox only. Spark and cloud batch services are not executed.
```text
$ run 1 (crash after 4 parts)
simulated crash after part 3
exit code 3
$ run 2 (resume)
scored now 60000, skipped (already done) 40000, output rows 100000, unique ids 100000, input rows 100000, match True
parts: 10 elapsed 0.2s (this sandbox)
$ run 3 (re-run, nothing to do)
scored now 0, skipped (already done) 100000, output rows 100000, unique ids 100000, input rows 100000, match True
parts: 10 elapsed 0.1s (this sandbox)
```

**Follow-ups:**
- *Why rename instead of writing the final file directly?* A crash mid-write would leave a half file that looks finished.
- *Join scores to keys how?* Write the id with each score (done here), then join on id downstream.
- *Duplicates if two jobs run at once?* Use a lock or a run id; same part names mean the last rename wins with identical content.

**Common mistakes:**
- Loading the model inside the loop.
- Appending to one big output file, so re-runs duplicate rows.
- Not validating counts before publishing.
- Treating `.tmp` files as output.

### Q28 ⭐⭐ 🟡 Streaming and event-driven inference at the serving boundary. A consumer reads events from a queue, scores each, and writes results. Explain at-least-once delivery and duplicate scoring (idempotent writes by event id), ordering and partitioning, micro-batching consumer polls to use the model efficiently, backpressure and lag as the key signal, dead-letter handling for poison events, and when a request-response API is simpler. Part 9 owns Kafka and Flink in depth. Write a runnable simulation with an in-memory queue, a scorer with a deduplication set, and a poison message that goes to a dead-letter list; show the real counts. Kafka itself is not executed.
**Asked at:** Serving interview-prep and glossary pages (nerdleveltech.com MLOps engineer interviews 'model serving infrastructure', techinterview.org MLOps interview and model-serving design posts, wecreateproblems.com MLOps interview questions, insertchat.com model-serving glossary; search snippets only, not opened); editorial guides, not verified candidate reports; MLOps, ML platform and ML engineer roles
**Say this first (1 line):** Streaming inference is at-least-once, so I make the write idempotent by event id, score in micro-batches, watch consumer lag, and send events that keep failing to a dead-letter queue instead of blocking the partition.

**Then explain:**
- **At-least-once:** the broker may redeliver after a crash or rebalance. Duplicates are normal. Dedupe by event id, or make the write an upsert keyed by id.
- **Order and partitions:** order is kept only within a partition. Key by entity id (user, device) if scores depend on order.
- **Micro-batching:** poll up to N events or wait T ms, then one model call. Better throughput than one by one, bounded added latency.
- **Backpressure and lag:** if the consumer is slower than the producer, lag grows. Lag (messages or seconds behind) is the key signal; scale consumers up to the partition count.
- **Poison events:** a bad payload throws on every retry. Retry a limited number of times, then dead-letter it with the error, and carry on.
- **Simpler alternative:** if the caller waits for the answer, a request-response API is simpler than a queue.
- **Failure mode:** marking an id as seen before the result is written loses the event if the write fails. In real code, record "seen" in the same transaction as the output (the simulation keeps it in memory, so it ignores this).

**Example:** 40 events, one poison (id 10), and 5 redeliveries (ids 3, 3, 17, 25, 25). Queue has 45 messages. Expected: 39 scored, 5 duplicates skipped, 1 dead-lettered, 39 + 1 = 40 unique ids.

**Code:**
```python
# ===== q28_stream_sim.py =====
# Q28: queue consumer simulation: at-least-once duplicates, dedupe by event id, micro-batches, poison -> DLQ, lag.
import random
from collections import deque
random.seed(1)
def score_batch(events):                      # stand-in model; raises on a poison event
    for e in events:
        if e["x"] is None: raise ValueError(f"bad payload in event {e['id']}")
    return [int(e["x"] > 0.5) for e in events]

queue = deque()
for i in range(40): queue.append({"id": i, "x": random.random()})
queue[10]["x"] = None                          # poison event
for i in (3, 3, 17, 25, 25):                   # broker redelivers: at-least-once duplicates
    queue.append(dict(queue[i]) if i != 10 else None)
produced = len(queue)
seen, results, dlq, polls, max_lag, scored_calls = set(), {}, [], 0, 0, 0
BATCH = 8
while queue:
    max_lag = max(max_lag, len(queue))
    batch = [queue.popleft() for _ in range(min(BATCH, len(queue)))]; polls += 1
    fresh = []
    for e in batch:
        if e["id"] in seen: continue           # duplicate: skip (idempotent)
        seen.add(e["id"]); fresh.append(e)
    try:
        for e, s in zip(fresh, score_batch(fresh)): results[e["id"]] = s
        scored_calls += 1
    except ValueError:
        for e in fresh:                        # isolate the poison: retry one by one
            try: results[e["id"]] = score_batch([e])[0]
            except ValueError as err: dlq.append((e["id"], str(err)))
print(f"messages on queue {produced}, polls {polls}, max lag {max_lag}")
print(f"scored {len(results)}, duplicates skipped {produced - len(seen)}, dead-lettered {len(dlq)}: {dlq}")
assert len(results) + len(dlq) == len(seen) == 40
print("check: scored + dead-lettered == unique ids (40):", len(results) + len(dlq))
```

**Output (my run):** real run with `python -I`. Kafka is not executed (no broker here); the logic (dedupe, micro-batch, dead letter) ran in memory.
```text
messages on queue 45, polls 6, max lag 45
scored 39, duplicates skipped 5, dead-lettered 1: [(10, 'bad payload in event 10')]
check: scored + dead-lettered == unique ids (40): 40
```

**Follow-ups:**
- *Exactly-once?* Mostly means at-least-once plus idempotent writes; check your platform's transaction support.
- *What do you alert on?* Consumer lag trend, dead-letter rate, and scoring error rate.
- *Why retry one by one after a batch fails?* To isolate the poison event so the other seven still get scored.

**Common mistakes:**
- Dead-lettering a whole batch for one bad event.
- Unbounded retries that block the partition.
- Dedupe set in memory only, lost on restart (use the output store as the source of truth).
- Ignoring lag until users complain.

### Q29 ⭐⭐ 🟡 Optimising a model for serving: ONNX Runtime graph optimisation levels, dynamic quantisation to int8, smaller models and distillation at concept level, operator fusion, batching, and thread settings. Explain the accuracy trade-off and how you check it (compare metrics on a validation set, not just a few rows), plus size, latency and memory measurements. Quantise a small ONNX model (onnxruntime.quantization.quantize_dynamic) and compare file size, accuracy on held-out data and CPU latency for an original and quantised model, showing real output labelled machine-specific. If the quantiser rejects the model, show that error. GPU and TensorRT are not executed.
**Asked at:** Model format and safety sources (scikit-learn model persistence docs, arxiv.org 2410.04490 on Hugging Face model exploits, labs.snyk.io deep-learning file format vulnerabilities, union.ai secure-AI post, ProtectAI ModelScan docs; search snippets only, not opened); docs and security write-ups, not interview reports; ML engineer and MLOps roles, security-aware teams
**Say this first (1 line):** I quantise with ONNX Runtime dynamic int8 to cut size and often CPU time, then I decide by accuracy on a held-out set and by latency at my real batch size, not by a few sample rows.

**Then explain:**
- **Graph optimisation:** ONNX Runtime has optimisation levels (basic, extended, all) that fold constants and fuse operators; they are on by default at a high level, and you can save the optimised model. Check current docs for names.
- **Dynamic int8:** weights are stored as int8, activations are quantised on the fly. Good for matmul-heavy models (MLPs, transformers on CPU). Little help for tiny linear or tree models.
- **Other levers:** smaller or distilled model (concept: a small student learns from a big teacher), batching, thread settings (intra-op threads match the cores you were given).
- **Check the trade-off:** accuracy on a validation set (thousands of rows), how many predictions flip versus fp32, file size, latency at batch 1 and at the real batch, and memory.
- **Failure modes:** accuracy drop on rare classes hidden by overall accuracy; speed-up that disappears at batch 1; quantiser errors on unsupported operators (the tool then raises, so read the message).

**Example:** A 64-feature, two hidden layer (256, 256) MLP, 3 classes, 6,000 synthetic rows. Compare fp32 and int8 on 1,800 held-out rows: size, accuracy, flipped labels, latency.

**Code:**
```python
# ===== q29_quantize.py =====
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
```
```bash
python q29_quantize.py /tmp/work/q29
```

**Output (my run):** real run, onnxruntime 1.31 CPU, a quantiser warning about pre-processing was printed and is harmless here. The quantiser did not reject the model. Latency is machine-specific, not a benchmark. GPU and TensorRT are not executed.
```text
WARNING:root:Please consider to run pre-processing before quantization. Refer to example: https://github.com/microsoft/onnxruntime-inference-examples/blob/main/quantization/image_classification/cpu/ReadMe.md 
size KB fp32 326  int8 87
sklearn acc 0.9444 | onnx fp32 acc 0.9444 | onnx int8 acc 0.9439 (held-out 1800 rows)
rows where int8 label differs from fp32: 10 of 1800
median ms batch   1: fp32 0.019  int8 0.020  (this sandbox, not a benchmark)
median ms batch 256: fp32 0.448  int8 0.234  (this sandbox, not a benchmark)
```
Read it: the file is about a quarter of the size; accuracy moved from 0.9444 to 0.9439 (10 of 1800 labels flipped); at batch 1 there is no speed-up (the call overhead dominates), at batch 256 it was about twice as fast on this machine. Your model and CPU will differ.

**Follow-ups:**
- *Dynamic vs static quantisation?* Static uses a calibration set to fix activation scales ahead of time; usually faster, more work.
- *Why not trust 5 sample rows?* Rare flips would not show.
- *When not to quantise?* When accuracy is tight, or the model is already tiny.

**Common mistakes:**
- Judging by file size only.
- Measuring latency at batch 1 and claiming a general speed-up.
- Skipping the accuracy check per class or slice.
- Forgetting to re-run the golden and parity tests (Q33) on the quantised artifact.

### Q30 ⭐⭐ 🟡 Long-running or slow models behind an API: the asynchronous job pattern. Explain why you do not hold an HTTP connection for 40 seconds, POST returns 202 with a job id, GET /jobs/{id} polls (or a webhook or a message when done), a queue plus workers (Celery, RQ, a cloud queue at concept level), job states, result expiry, idempotency keys for retries, and timeouts at each hop. Write a FastAPI version using an in-process queue and a worker thread (stand-in for a real queue) with job states and a test that follows submit, poll and result. Run it with TestClient. Celery and Redis are not executed.
**Asked at:** Serving interview-prep and glossary pages (nerdleveltech.com MLOps engineer interviews 'model serving infrastructure', techinterview.org MLOps interview and model-serving design posts, wecreateproblems.com MLOps interview questions, insertchat.com model-serving glossary; search snippets only, not opened); editorial guides, not verified candidate reports; MLOps, ML platform and ML engineer roles
**Say this first (1 line):** For a 40-second model I do not hold the connection: POST returns 202 with a job id, a worker does the job from a queue, and the client polls GET /jobs/id or gets a callback.

**Then explain:**
- **Why not wait:** proxies, gateways and browsers time out (often 30 to 60 seconds, check yours), and a held connection pins a worker and breaks on any retry.
- **Flow:** `POST /jobs` returns 202, a `Location` header and a job id; `GET /jobs/{id}` returns `queued`, `running`, `done` or `failed` with the result or error.
- **Queue plus workers:** in production Celery, RQ or a cloud queue with Redis or a broker; here an in-process queue and a thread stand in. A real queue survives an API restart; this does not.
- **Idempotency key:** the client sends `Idempotency-Key`; a retried POST returns the same job instead of running the model twice.
- **Result expiry:** keep results for a TTL, then return 404 or 410. Store big results in object storage and return a link.
- **Timeouts at each hop:** client, gateway, API, queue visibility timeout and worker timeout, with the inner ones shorter than the outer.
- **Alternatives:** webhook or a message when done, to avoid polling.

**Example:** `POST /jobs {"n": 7}` returns 202 `{"job_id": "...", "state": "queued"}`. Polling shows `queued` or `running`, then `{"state": "done", "result": 49}`. The same POST with the same `Idempotency-Key` returns the same job id.

**Code:** app and tests (TestClient).
```python
# ===== q30_async_jobs.py =====
# Q30: async job pattern: 202 + job id + polling. In-process queue and worker thread stand in for Celery/Redis.
import queue, threading, time, uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Header, HTTPException, Response
from pydantic import BaseModel

class Job(BaseModel):
    n: int

def make_app(work_seconds=0.3, ttl=3600):
    jobs, idem, q = {}, {}, queue.Queue()
    def worker():
        while True:
            jid = q.get()
            if jid is None: break
            jobs[jid]["state"] = "running"
            try:
                time.sleep(work_seconds)                      # the slow model
                if jobs[jid]["n"] < 0: raise ValueError("negative n")
                jobs[jid].update(state="done", result=jobs[jid]["n"] ** 2)
            except Exception as e:
                jobs[jid].update(state="failed", error=str(e))
            jobs[jid]["finished"] = time.time()
    @asynccontextmanager
    async def lifespan(app):
        t = threading.Thread(target=worker, daemon=True); t.start()
        yield
        q.put(None); t.join(timeout=2)
    app = FastAPI(lifespan=lifespan)
    @app.post("/jobs", status_code=202)
    def submit(j: Job, response: Response, idempotency_key: str | None = Header(default=None)):
        if idempotency_key and idempotency_key in idem:      # retry of the same request: same job
            response.headers["Location"] = f"/jobs/{idem[idempotency_key]}"
            return {"job_id": idem[idempotency_key], "state": jobs[idem[idempotency_key]]["state"], "deduplicated": True}
        jid = uuid.uuid4().hex[:8]
        jobs[jid] = {"state": "queued", "n": j.n, "created": time.time()}
        if idempotency_key: idem[idempotency_key] = jid
        q.put(jid); response.headers["Location"] = f"/jobs/{jid}"
        return {"job_id": jid, "state": "queued", "deduplicated": False}
    @app.get("/jobs/{jid}")
    def status(jid: str):
        j = jobs.get(jid)
        if j is None: raise HTTPException(404, "unknown or expired job")
        if "finished" in j and time.time() - j["finished"] > ttl:
            del jobs[jid]; raise HTTPException(404, "unknown or expired job")
        return {k: v for k, v in j.items() if k in ("state", "result", "error")}
    return app

# ===== test_q30.py =====
import time
from fastapi.testclient import TestClient
from q30_async_jobs import make_app
def wait(c, jid, timeout=3):
    end = time.time() + timeout
    while time.time() < end:
        s = c.get(f"/jobs/{jid}").json()
        if s["state"] in ("done", "failed"): return s
        time.sleep(0.05)
    raise TimeoutError
def test_submit_poll_result():
    with TestClient(make_app(0.2)) as c:
        r = c.post("/jobs", json={"n": 7}); assert r.status_code == 202
        jid = r.json()["job_id"]; assert r.headers["location"] == f"/jobs/{jid}"
        first = c.get(f"/jobs/{jid}").json(); assert first["state"] in ("queued", "running")
        final = wait(c, jid); assert final == {"state": "done", "result": 49}
def test_idempotency_key_reuses_job():
    with TestClient(make_app(0.1)) as c:
        a = c.post("/jobs", json={"n": 2}, headers={"Idempotency-Key": "k1"}).json()
        b = c.post("/jobs", json={"n": 2}, headers={"Idempotency-Key": "k1"}).json()
        assert a["job_id"] == b["job_id"] and b["deduplicated"] is True
def test_failure_and_unknown():
    with TestClient(make_app(0.05)) as c:
        jid = c.post("/jobs", json={"n": -1}).json()["job_id"]
        assert wait(c, jid)["state"] == "failed"
        assert c.get("/jobs/nope").status_code == 404
def test_expiry():
    with TestClient(make_app(0.05, ttl=0)) as c:
        jid = c.post("/jobs", json={"n": 3}).json()["job_id"]
        time.sleep(0.4); assert c.get(f"/jobs/{jid}").status_code == 404
```

**Output (my run):** real pytest run with TestClient. Celery and Redis are not executed.
```text
test_q30.py::test_submit_poll_result PASSED
test_q30.py::test_idempotency_key_reuses_job PASSED
test_q30.py::test_failure_and_unknown PASSED
test_q30.py::test_expiry PASSED
============================== 4 passed in 1.22s ===============================
```

**Follow-ups:**
- *Poll or push?* Polling is simple and works through any proxy; webhooks cut load but need a reachable receiver and retries.
- *Worker dies mid-job?* A real queue redelivers after a visibility timeout, so jobs must be idempotent.
- *Why 202 not 200?* The work is accepted, not finished.

**Common mistakes:**
- In-memory job state with multiple API replicas (replica A cannot see replica B's jobs): use a shared store.
- No expiry, so results pile up.
- Retrying POST without an idempotency key, running the model twice.
- Polling in a tight loop with no backoff.

### Q31 ⭐⭐ 🟡 Timeouts, retries, backpressure and load shedding for a model service. Explain client timeouts shorter than the server's, retries with exponential backoff and jitter (and only for idempotent calls), retry storms, a concurrency limit per replica with a 429 or 503 when full (shed load early instead of queueing forever), circuit breakers, bulkheads, and degraded modes (a cheaper model or a default score). Write a FastAPI middleware or semaphore-based limiter that returns 503 with Retry-After when more than N requests are in flight, and a test with concurrent httpx calls showing shed and served counts. Run it locally.
**Asked at:** Serving interview-prep and glossary pages (nerdleveltech.com MLOps engineer interviews 'model serving infrastructure', techinterview.org MLOps interview and model-serving design posts, wecreateproblems.com MLOps interview questions, insertchat.com model-serving glossary; search snippets only, not opened); editorial guides, not verified candidate reports; MLOps, ML platform and ML engineer roles
**Say this first (1 line):** I put a hard cap on requests in flight per replica and answer 503 with Retry-After when it is full, because failing fast early is better than a queue that grows until everything times out.

**Then explain:**
- **Timeouts:** the client's timeout is shorter than the server's, so the client gives up first and the server does not keep working for nobody. Set a timeout at every hop.
- **Retries:** only for idempotent calls (a prediction is, a "charge the card" is not). Exponential backoff with jitter, a retry budget, and honour Retry-After.
- **Retry storm:** when a service slows, every client retries, load multiplies, the service dies. Backoff, jitter and a retry budget stop it.
- **Load shedding:** limit concurrency (here N in flight). Over the limit return 503 (or 429 for per-client limits) at once.
- **Circuit breaker:** after many failures, stop calling for a while, then probe. **Bulkhead:** separate pools per dependency or route so one slow part cannot eat all capacity.
- **Degraded modes:** a cheaper model, cached answer or default score, labelled as such.
- **Failure mode:** shedding on liveness probes or counting shed requests as healthy latency hides the problem; export the shed count (Q32).

**Example:** limit 4, a 0.3 s handler, 10 simultaneous requests: 4 are served, 6 are rejected with 503 and `Retry-After: 1`, peak in flight is 4. After the burst, a new request gets 200.

**Code:** middleware, plus a full-jitter backoff helper, plus tests.
```python
# ===== q31_limiter.py =====
# Q31: concurrency limiter that sheds load with 503 + Retry-After instead of queueing forever.
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

def make_app(max_in_flight=4, work_s=0.2):
    app = FastAPI(); st = {"in_flight": 0, "peak": 0, "shed": 0, "served": 0}
    @app.middleware("http")
    async def limiter(request: Request, call_next):
        if request.url.path != "/predict": return await call_next(request)
        if st["in_flight"] >= max_in_flight:          # no await between check and increment: no race
            st["shed"] += 1
            return JSONResponse({"detail": "overloaded"}, status_code=503, headers={"Retry-After": "1"})
        st["in_flight"] += 1; st["peak"] = max(st["peak"], st["in_flight"])
        try: return await call_next(request)
        finally: st["in_flight"] -= 1
    @app.post("/predict")
    async def predict():
        await asyncio.sleep(work_s); st["served"] += 1       # stand-in for model time
        return {"label": 1}
    @app.get("/stats")
    async def stats(): return st
    return app

def backoff_delays(base=0.1, cap=2.0, tries=5, seed=0):
    """Full-jitter exponential backoff schedule for a client (idempotent calls only)."""
    import random; r = random.Random(seed)
    return [round(r.uniform(0, min(cap, base * 2 ** i)), 3) for i in range(tries)]

# ===== test_q31.py =====
import asyncio, httpx
from q31_limiter import make_app, backoff_delays
def test_sheds_when_full():
    async def go():
        app = make_app(max_in_flight=4, work_s=0.3)
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://t") as c:
            rs = await asyncio.gather(*[c.post("/predict") for _ in range(10)])
            codes = [r.status_code for r in rs]
            stats = (await c.get("/stats")).json()
            late = await c.post("/predict")            # after the burst, capacity is free again
        return codes, rs, stats, late.status_code
    codes, rs, stats, late = asyncio.run(go())
    print("codes:", sorted(codes)); print("stats:", stats)
    assert codes.count(200) == 4 and codes.count(503) == 6
    assert stats["peak"] == 4 and stats["shed"] == 6
    assert all(r.headers["retry-after"] == "1" for r in rs if r.status_code == 503)
    assert late == 200
def test_backoff_bounded_and_jittered():
    d = backoff_delays(); print("backoff:", d)
    assert len(d) == 5
    assert all(0 <= x <= min(2.0, 0.1 * 2 ** i) for i, x in enumerate(d))
```

**Output (my run):** real pytest run with httpx and an in-process ASGI transport. Printed lines are from `-s`.
```text
test_q31.py::test_sheds_when_full codes: [200, 200, 200, 200, 503, 503, 503, 503, 503, 503]
stats: {'in_flight': 0, 'peak': 4, 'shed': 6, 'served': 4}
PASSED
test_q31.py::test_backoff_bounded_and_jittered backoff: [0.084, 0.152, 0.168, 0.207, 0.818]
PASSED
============================== 2 passed in 0.91s ===============================
```

**Follow-ups:**
- *503 or 429?* 429 says "you sent too many"; 503 says "I am overloaded". Per-client limits use 429.
- *Why not a bigger queue?* A long queue only converts overload into latency, then timeouts.
- *Where do you set the limit?* From measured capacity per replica (load test), a bit below the knee.

**Common mistakes:**
- Retrying without jitter (all clients retry together).
- Retrying non-idempotent calls.
- Limit counted per process while running several workers (each has its own count).
- Client timeout longer than the server's.

### Q32 ⭐⭐ 🟡 Observability inside the serving layer (Part 8 owns model drift and data-quality monitoring). Cover structured logs with a request id and model version, request count, latency histogram and error counters exposed on a /metrics endpoint in Prometheus text format, what to alert on (error rate, p99, saturation, readiness flapping), logging inputs and predictions safely (sampling, hashing, no PII) for later drift analysis, and trace ids across services. Add a small middleware to a FastAPI app that records latency into a histogram and exposes /metrics; use prometheus_client if it installs (otherwise hand-write the text format), and show the real output. Prometheus and Grafana servers are not executed.
**Asked at:** Serving interview-prep and glossary pages (nerdleveltech.com MLOps engineer interviews 'model serving infrastructure', techinterview.org MLOps interview and model-serving design posts, wecreateproblems.com MLOps interview questions, insertchat.com model-serving glossary; search snippets only, not opened); editorial guides, not verified candidate reports; MLOps, ML platform and ML engineer roles
**Say this first (1 line):** Inside the serving layer I want structured logs with a request id and model version, request, error and latency metrics on /metrics, and alerts on error rate, p99 and saturation; drift and data quality belong to Part 8.

**Then explain:**
- **Logs:** one JSON line per request: request id, route, status, model version, duration. Pass the id back in a header and forward it to downstream calls (trace id).
- **Metrics:** a counter for requests by route and status, a histogram for latency, a gauge for in-flight. Histograms let Prometheus compute p99 across replicas; averages hide tails.
- **Labels:** keep values bounded (route template, not the raw URL with ids). Unbounded labels blow up memory in Prometheus.
- **Alert on:** error rate, p99 versus the budget, saturation (in-flight at the limit, shed count), and readiness flapping. Alert on symptoms users feel.
- **Logging inputs and predictions for later drift analysis:** sample (for example 1 percent), hash or drop identifiers, never log PII, keep a retention limit. Store features and predictions with the model version.
- **Failure mode:** a metric registered twice (two app instances in tests) raises an error; use your own registry per app or create once.

**Example:** Two POST /predict and one unknown URL: the counter shows `/predict` 200 = 2 and `unmatched` 404 = 1; the histogram count for `/predict` is 2; the log line for the first request has the id `abc123` we sent.

**Code:**
```python
# ===== q32_metrics_app.py =====
# Q32: serving-layer observability: request id + structured log, Prometheus histogram, /metrics.
import json, logging, sys, time, uuid
from fastapi import FastAPI, Request, Response
from prometheus_client import CollectorRegistry, Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

MODEL_VERSION = "v1"
def make_app():
    reg = CollectorRegistry()          # own registry: no clashes when tests build the app twice
    REQS = Counter("predict_requests_total", "Requests", ["route", "status"], registry=reg)
    LAT = Histogram("predict_latency_seconds", "Latency", ["route"], buckets=(0.005, 0.01, 0.05, 0.1, 0.5), registry=reg)
    INF = Gauge("predict_in_flight", "In flight", registry=reg)
    log = logging.getLogger("serve"); log.handlers[:] = [logging.StreamHandler(sys.stdout)]
    log.setLevel(logging.INFO); log.propagate = False
    app = FastAPI()
    @app.middleware("http")
    async def observe(request: Request, call_next):
        rid = request.headers.get("x-request-id") or uuid.uuid4().hex[:8]
        t = time.perf_counter(); INF.inc(); status = 500
        try:
            resp = await call_next(request); status = resp.status_code
            resp.headers["x-request-id"] = rid; return resp
        finally:
            INF.dec(); dt = time.perf_counter() - t
            route = request.scope.get("route").path if request.scope.get("route") else "unmatched"   # bounded label values
            REQS.labels(route, str(status)).inc(); LAT.labels(route).observe(dt)
            log.info(json.dumps({"request_id": rid, "route": route, "status": status, "model_version": MODEL_VERSION, "ms": round(dt*1000, 2)}))
    @app.post("/predict")
    async def predict(): return {"label": 1}
    @app.get("/metrics")
    def metrics(): return Response(generate_latest(reg), media_type=CONTENT_TYPE_LATEST)
    return app

# ===== q32_run.py =====
from fastapi.testclient import TestClient
from q32_metrics_app import make_app
with TestClient(make_app()) as c:
    c.post("/predict", headers={"x-request-id": "abc123"}); c.post("/predict"); c.get("/nope")
    print("--- /metrics (selected lines) ---")
    for line in c.get("/metrics").text.splitlines():
        if line.startswith(("predict_requests_total", "predict_latency_seconds_count", "predict_latency_seconds_bucket", "predict_in_flight", "# TYPE predict")) : print(line)
```

**Output (my run):** real run with prometheus_client 0.26 and TestClient. Log lines and /metrics text are the actual output (trimmed to the key lines). Prometheus and Grafana servers are not executed. The in-flight gauge reads 1 because the /metrics request itself was in flight.
```text
{"request_id": "abc123", "route": "/predict", "status": 200, "model_version": "v1", "ms": 0.72}
{"request_id": "d175d904", "route": "/predict", "status": 200, "model_version": "v1", "ms": 0.6}
{"request_id": "4faa3caa", "route": "unmatched", "status": 404, "model_version": "v1", "ms": 0.25}
--- /metrics (selected lines) ---
{"request_id": "21552a31", "route": "/metrics", "status": 200, "model_version": "v1", "ms": 1.91}
# TYPE predict_requests_total counter
predict_requests_total{route="/predict",status="200"} 2.0
predict_requests_total{route="unmatched",status="404"} 1.0
# TYPE predict_requests_created gauge
# TYPE predict_latency_seconds histogram
predict_latency_seconds_bucket{le="0.005",route="/predict"} 2.0
predict_latency_seconds_bucket{le="0.01",route="/predict"} 2.0
predict_latency_seconds_bucket{le="0.05",route="/predict"} 2.0
predict_latency_seconds_bucket{le="0.1",route="/predict"} 2.0
predict_latency_seconds_bucket{le="0.5",route="/predict"} 2.0
predict_latency_seconds_bucket{le="+Inf",route="/predict"} 2.0
predict_latency_seconds_count{route="/predict"} 2.0
predict_latency_seconds_bucket{le="0.005",route="unmatched"} 1.0
predict_latency_seconds_bucket{le="0.01",route="unmatched"} 1.0
predict_latency_seconds_bucket{le="0.05",route="unmatched"} 1.0
predict_latency_seconds_bucket{le="0.1",route="unmatched"} 1.0
predict_latency_seconds_bucket{le="0.5",route="unmatched"} 1.0
predict_latency_seconds_bucket{le="+Inf",route="unmatched"} 1.0
predict_latency_seconds_count{route="unmatched"} 1.0
# TYPE predict_latency_seconds_created gauge
# TYPE predict_in_flight gauge
predict_in_flight 1.0
```

**Follow-ups:**
- *Histogram buckets?* Pick them around your latency budget; check current prometheus_client defaults.
- *Multiple uvicorn workers?* Each process has its own metrics; use prometheus_client's multiprocess mode or scrape per pod (check docs).
- *Health endpoints in metrics?* Count them separately or exclude them, so probes do not hide real error rates.

**Common mistakes:**
- Raw path as a label (`/items/123`).
- Averages instead of percentiles.
- Logging full request bodies with personal data.
- No model version in logs, so you cannot tell which model made a bad call.

### Q33 ⭐⭐ 🟡 Testing a model API beyond unit tests. Cover pytest with TestClient, contract tests on the schema, golden-file prediction tests (fixed inputs, expected outputs with tolerance), parity between the training pipeline and the served artifact (the ONNX output must match the original), a startup test (service becomes ready), a load smoke test in CI, and property tests (batch of N equals N singles). Part 7 owns CI wiring. Write a pytest suite for the iris ONNX FastAPI app with a golden test, a parity test and a batch-equals-singles test, run it, and show the real result.
**Asked at:** FastAPI docs and tutorials (fastapi.tiangolo.com advanced events/lifespan page, reintech.io 'FastAPI ML model serving production REST APIs', docs.truefoundry.com deploy-model-fastapi; search snippets only, not opened); docs and tutorials, not interview reports; ML engineer and MLOps roles that ship model APIs, including IT-services firms, product companies and GCCs
**Say this first (1 line):** I test the API in layers: schema contract, golden predictions, parity with the training pipeline, a startup test, and a batch-equals-singles property, all in pytest with TestClient so CI runs them in seconds.

**Then explain:**
- **TestClient:** use `with TestClient(app)` so the lifespan runs and the model loads; without `with` the model is not loaded (shown: /readyz gives 503).
- **Contract test:** response keys and types, and 422 for bad input. This catches an accidental rename.
- **Golden file:** fixed inputs with expected outputs and a tolerance (`atol`). Generate it once from a reviewed artifact, commit it, and a model change that moves outputs fails the test and forces a human look. Do not regenerate it blindly.
- **Parity:** the served artifact (ONNX) must match the original (sklearn) on labels and, within tolerance, on probabilities. This catches export bugs and dtype mistakes (float64 vs float32).
- **Property:** a batch of N rows gives the same labels as N single calls.
- **Smoke load test:** a few hundred requests in CI checking no errors and a loose latency ceiling (CI wiring is Part 7; not run here).
- **Failure modes:** exact float equality (flaky), goldens regenerated on every change (test proves nothing), testing only the happy path.

**Example:** Iris, three golden rows (setosa, versicolor, virginica), parity on all 150 rows, and 15 rows sent as one batch and as 15 single calls.

**Code:** the app under test, the pytest suite, and the golden file (made once from the reviewed artifact, then committed). A mutation check (editing one golden number) should make the golden test fail, and it did.
```python
# ===== iris_app.py =====
# The iris ONNX FastAPI app under test (Q33).
import os
from contextlib import asynccontextmanager
import numpy as np, onnxruntime as ort
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

class One(BaseModel):
    features: list[float] = Field(min_length=4, max_length=4)
class Many(BaseModel):
    rows: list[list[float]] = Field(min_length=1, max_length=256)

def make_app(path=None):
    path = path or os.environ["IRIS_ONNX"]; st = {}
    @asynccontextmanager
    async def lifespan(app):
        st["s"] = ort.InferenceSession(path, providers=["CPUExecutionProvider"]); yield
    app = FastAPI(lifespan=lifespan)
    @app.get("/readyz")
    def readyz():
        if "s" not in st: raise HTTPException(503, "not ready")
        return {"status": "ready"}
    @app.post("/v1/predict")
    def predict(r: One):
        o = st["s"].run(None, {"X": np.array([r.features], dtype=np.float32)})
        return {"label": int(o[0][0]), "probabilities": [round(float(p), 6) for p in o[1][0]]}
    @app.post("/v1/predict_batch")
    def predict_batch(r: Many):
        if any(len(x) != 4 for x in r.rows): raise HTTPException(422, "each row needs 4 features")
        o = st["s"].run(None, {"X": np.array(r.rows, dtype=np.float32)})
        return {"labels": o[0].tolist()}
    return app

# ===== test_q33.py =====
import json, os, pathlib
import numpy as np, pytest, onnxruntime as ort
from fastapi.testclient import TestClient
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from iris_app import make_app

MODEL = os.environ["IRIS_ONNX"]
GOLDEN = pathlib.Path(__file__).with_name("golden_iris.json")

@pytest.fixture(scope="module")
def client():
    with TestClient(make_app(MODEL)) as c: yield c        # `with` runs lifespan

def test_startup_ready_and_not_ready_without_lifespan():
    assert TestClient(make_app(MODEL)).get("/readyz").status_code == 503   # no `with`: lifespan did not run
    with TestClient(make_app(MODEL)) as c: assert c.get("/readyz").json() == {"status": "ready"}

def test_contract_schema(client):
    r = client.post("/v1/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})
    assert r.status_code == 200 and set(r.json()) == {"label", "probabilities"}
    assert isinstance(r.json()["label"], int) and len(r.json()["probabilities"]) == 3
    assert client.post("/v1/predict", json={"features": [1, 2]}).status_code == 422
    assert client.post("/v1/predict", json={"features": ["a", 2, 3, 4]}).status_code == 422

def test_golden_file(client):
    golden = json.loads(GOLDEN.read_text())
    for g in golden:
        out = client.post("/v1/predict", json={"features": g["x"]}).json()
        assert out["label"] == g["label"]
        np.testing.assert_allclose(out["probabilities"], g["p"], atol=1e-4)

def test_parity_with_training_pipeline(client):
    X, y = load_iris(return_X_y=True); X = X.astype(np.float32)
    sk = LogisticRegression(max_iter=500).fit(X, y)                   # the original model
    r = client.post("/v1/predict_batch", json={"rows": X.tolist()[:150]}).json()
    assert r["labels"] == sk.predict(X).tolist()
    s = ort.InferenceSession(MODEL, providers=["CPUExecutionProvider"])
    np.testing.assert_allclose(s.run(None, {"X": X})[1], sk.predict_proba(X), atol=1e-4)

def test_batch_equals_singles(client):
    X, _ = load_iris(return_X_y=True)
    rows = X[::10].tolist()
    batch = client.post("/v1/predict_batch", json={"rows": rows}).json()["labels"]
    singles = [client.post("/v1/predict", json={"features": r}).json()["label"] for r in rows]
    assert batch == singles and len(batch) == 15
```
```bash
python make_model.py /tmp/work
IRIS_ONNX=/tmp/work/iris.onnx python -m pytest -v test_q33.py
```
```json
[
 {
  "x": [
   5.1,
   3.5,
   1.4,
   0.2
  ],
  "label": 0,
  "p": [
   0.9816,
   0.0184,
   0.0
  ]
 },
 {
  "x": [
   6.0,
   2.9,
   4.5,
   1.5
  ],
  "label": 1,
  "p": [
   0.0055,
   0.8126,
   0.1819
  ]
 },
 {
  "x": [
   6.7,
   3.0,
   5.2,
   2.3
  ],
  "label": 2,
  "p": [
   0.0001,
   0.0807,
   0.9193
  ]
 }
]
```

**Output (my run):** real run, pytest 9.1, fastapi 0.162. The second part is the mutation check (one golden probability changed to 0.5, then restored).
```text
test_q33.py::test_startup_ready_and_not_ready_without_lifespan PASSED
test_q33.py::test_contract_schema PASSED
test_q33.py::test_golden_file PASSED
test_q33.py::test_parity_with_training_pipeline PASSED
test_q33.py::test_batch_equals_singles PASSED
============================== 5 passed in 2.17s ===============================
E           Mismatched elements: 1 / 3 (33.3%)
E           Mismatch at index:
FAILED test_q33.py::test_golden_file - AssertionError: 
1 failed, 4 passed in 2.61s
```

**Follow-ups:**
- *Why tolerance?* Different libraries and CPUs give tiny float differences.
- *When do you update the golden file?* On an intended model change, in the same pull request, with a reviewer comparing old and new.
- *Where does the load test run?* A small smoke in CI, the real one on a staging environment (locust or k6 not executed here).

**Common mistakes:**
- Forgetting `with TestClient(...)`, so the lifespan never runs.
- Comparing floats with `==`.
- Golden file made from the model it tests, never reviewed.
- Testing the Python model but not the exported artifact that really ships.

### Q34 ⭐⭐ 🟡 Serving LLMs at the boundary with Book 2. Do not repeat vLLM, KV cache or RAG internals (Book 2 owns them). Cover what changes for the serving layer: streaming tokens with Server-Sent Events from FastAPI, time to first token versus tokens per second as the latency metrics, request timeouts and cancellation when the client disconnects, an OpenAI-compatible interface as the common contract, putting an API gateway in front of a model server, and why classic fixed-size batching is replaced by continuous batching inside the engine. Write a FastAPI streaming endpoint that streams tokens from a fake generator and a httpx client that measures time to first chunk and total time, run it for real, and say that no real LLM or GPU server is executed.
**Asked at:** Serving interview-prep and glossary pages (nerdleveltech.com MLOps engineer interviews 'model serving infrastructure', techinterview.org MLOps interview and model-serving design posts, wecreateproblems.com MLOps interview questions, insertchat.com model-serving glossary; search snippets only, not opened); editorial guides, not verified candidate reports; MLOps, ML platform and ML engineer roles
**Say this first (1 line):** For LLMs the serving layer streams tokens over Server-Sent Events, I measure time to first token and tokens per second separately, and I cancel generation when the client disconnects, while the engine does the continuous batching.

**Then explain:**
- **Streaming (SSE):** the response is `text/event-stream`, each chunk is `data: ...` and a blank line, ending with a `[DONE]` marker. Turn off proxy buffering, or users see nothing until the end.
- **Metrics:** time to first token (TTFT) is prefill plus queueing, which users feel as "did it start". Tokens per second is decode speed, which sets how fast it reads. Track both, plus total time.
- **Cancellation:** if the client closes the tab, stop generating. Otherwise you pay for tokens nobody reads. Check `request.is_disconnected()` or handle `CancelledError`.
- **Timeouts:** a total request timeout and an idle timeout between chunks, at gateway and server.
- **OpenAI-compatible interface:** many servers and clients speak `/v1/chat/completions`, so clients can swap backends. Check current docs for the exact fields.
- **Gateway in front:** auth, rate limits, quotas, routing between models, logging, retries. Streaming must pass through it unbuffered.
- **Continuous batching:** requests finish at different lengths, so fixed-size batches waste slots waiting for the longest one. The engine adds and removes sequences every step. Internals belong to Book 2.

**Example:** 20 tokens, a fake 0.30 s prefill and 0.05 s per token: first token near 0.3 s, total near 1.3 s, about 20 tokens per second after the first. Disconnect after 3 tokens: the server should record a cancel.

**Code:** a FastAPI endpoint with a fake generator, and an httpx client. Run with `python -m uvicorn q34_stream_app:app --port 8341`, then the client.
```python
# ===== q34_stream_app.py =====
# Q34: SSE token streaming from a fake generator (no real LLM).
import asyncio, json, time
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

app = FastAPI(); stats = {"started": 0, "completed": 0, "cancelled": 0}
class Chat(BaseModel):
    prompt: str
    max_tokens: int = Field(default=20, ge=1, le=200)

async def fake_llm(prompt, n, first_delay=0.30, per_token=0.05):
    await asyncio.sleep(first_delay)                 # "prefill": time to first token
    for i in range(n):
        yield f"tok{i} "; await asyncio.sleep(per_token)   # "decode": one token per step

@app.post("/v1/chat/stream")
async def chat(body: Chat, request: Request):
    async def sse():
        stats["started"] += 1
        try:
            async for tok in fake_llm(body.prompt, body.max_tokens):
                if await request.is_disconnected(): stats["cancelled"] += 1; return   # stop paying for tokens nobody reads
                yield f"data: {json.dumps({'token': tok})}\n\n"
            yield "data: [DONE]\n\n"; stats["completed"] += 1
        except asyncio.CancelledError:
            stats["cancelled"] += 1; raise
    return StreamingResponse(sse(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

@app.get("/stats")
async def get_stats(): return stats

# ===== q34_client.py =====
import sys, time, httpx
base = sys.argv[1]
with httpx.Client(timeout=10) as c:
    t0 = time.perf_counter(); first = None; n = 0
    with c.stream("POST", base + "/v1/chat/stream", json={"prompt": "hi", "max_tokens": 20}) as r:
        print("status", r.status_code, r.headers["content-type"])
        for line in r.iter_lines():
            if line.startswith("data: ") and line != "data: [DONE]":
                n += 1
                if first is None: first = time.perf_counter() - t0
    total = time.perf_counter() - t0
    print(f"tokens {n}; time to first token {first*1000:.0f} ms; total {total*1000:.0f} ms; tokens/s after first {(n-1)/(total-first):.1f} (this sandbox, fake generator)")
    # client disconnects after 3 tokens
    with c.stream("POST", base + "/v1/chat/stream", json={"prompt": "hi", "max_tokens": 100}) as r:
        k = 0
        for line in r.iter_lines():
            if line.startswith("data: "):
                k += 1
                if k == 3: break
    time.sleep(0.6)
    print("stats after one full stream and one early disconnect:", c.get(base + "/stats").json())
```

**Output (my run):** real local uvicorn server on port 8341, stopped afterwards. No real LLM or GPU server is executed; the generator is fake. Timings are this sandbox only.
```text
status 200 text/event-stream; charset=utf-8
tokens 20; time to first token 329 ms; total 1349 ms; tokens/s after first 18.6 (this sandbox, fake generator)
stats after one full stream and one early disconnect: {'started': 2, 'completed': 1, 'cancelled': 1}
```

**Follow-ups:**
- *SSE or WebSocket?* SSE is simpler for one-way token streams and works over normal HTTP; WebSocket for two-way.
- *What breaks streaming?* Proxy or CDN buffering and gzip on the stream.
- *Rate limit by what?* Tokens, not just requests; one request can be 10 or 10,000 tokens.

**Common mistakes:**
- Measuring only total latency.
- Not cancelling on disconnect.
- Buffering proxies.
- Setting a total timeout shorter than a long answer needs.
