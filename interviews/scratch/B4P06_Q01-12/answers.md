### Q1 ⭐⭐⭐ 🟢 Build a model prediction API with FastAPI. Explain the request and response models with pydantic (types, Field constraints, why a typo or a wrong-length feature list returns 422 before your model sees it), loading the model once at startup with the lifespan function instead of per request, a predict endpoint, a health endpoint, and keeping the model in app state. Use a small scikit-learn model exported to ONNX and served with onnxruntime. Test it with pytest and TestClient, and show the real 200 and 422 responses. Also run it once under a real uvicorn on localhost and call it with curl.
**Asked at:** FastAPI docs and tutorials (fastapi.tiangolo.com advanced events/lifespan page, reintech.io 'FastAPI ML model serving production REST APIs', docs.truefoundry.com deploy-model-fastapi; search snippets only, not opened); docs and tutorials, not interview reports; ML engineer and MLOps roles that ship model APIs, including IT-services firms, product companies and GCCs
**Say this first (1 line):** I load the ONNX model once in the lifespan function, keep it in `app.state`, and let pydantic reject bad input with a 422 before my model code runs.

**Then explain:**
- Pydantic models are the contract. `features: list[float]` with `min_length=4, max_length=4` means a wrong-length list, a string in the list, or a missing key never reaches the model. `extra="forbid"` turns a typo like `feature` into a 422 instead of a silent ignore.
- Lifespan runs once before the first request. Loading per request would cost milliseconds to seconds on every call and would make memory spike under load. The session lives in `app.state.session` and is shared by all requests.
- Failure modes: the model file is missing, so startup fails and the pod never becomes ready (good, loud). The model is loaded but the input is float64, which ONNX Runtime rejects (cast to float32 yourself). Do not use a module-level global that is loaded at import time, because tests and tooling then load the model just by importing the file.
- `def` endpoint on purpose: ONNX Runtime releases the GIL, so FastAPI's threadpool handles concurrency (Q2 explains why).
- A health route is separate from predict. Here `/readyz` returns 503 until the session exists (Q4 goes deep).

**Example:** the iris row `[6.7, 3.0, 5.2, 2.3]` is class 2 (virginica). Send 3 numbers instead of 4 and you get 422 `too_short` at `body.features`. Hand check: a 4-feature request must have exactly 4 numbers, so 3 fails.

**Code:** (one python block with the app and its test; one bash block for the real uvicorn run)
```python
# ===== q01/app.py =====
import os
from contextlib import asynccontextmanager
import numpy as np
import onnxruntime as ort
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel, Field, ConfigDict

MODEL_PATH = os.environ.get("MODEL_PATH", "iris_v1.onnx")
LABELS = ["setosa", "versicolor", "virginica"]


class PredictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")          # a typo'd key -> 422
    features: list[float] = Field(min_length=4, max_length=4,
                                  description="sepal_len, sepal_wid, petal_len, petal_wid (cm)")


class PredictResponse(BaseModel):
    label: int
    name: str
    probabilities: list[float]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # runs ONCE at startup, before the first request
    app.state.session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
    app.state.input_name = app.state.session.get_inputs()[0].name
    yield
    app.state.session = None                           # shutdown: release


app = FastAPI(lifespan=lifespan)


@app.get("/readyz")
def readyz(request: Request, response: Response):
    if getattr(request.app.state, "session", None) is None:
        response.status_code = 503
        return {"status": "loading"}
    return {"status": "ready"}


@app.post("/v1/predict", response_model=PredictResponse)
def predict(req: PredictRequest, request: Request):
    x = np.asarray([req.features], dtype=np.float32)
    label, probs = request.app.state.session.run(None, {request.app.state.input_name: x})
    return PredictResponse(label=int(label[0]), name=LABELS[int(label[0])],
                           probabilities=[round(float(p), 4) for p in probs[0]])

# ===== q01/test_app.py =====
import os
os.environ.setdefault("MODEL_PATH", "/tmp/claude-0/b6_q1_12/models/iris_v1.onnx")
from fastapi.testclient import TestClient
from app import app


def test_ok():
    with TestClient(app) as c:                       # `with` runs the lifespan
        r = c.post("/v1/predict", json={"features": [6.7, 3.0, 5.2, 2.3]})
        print(r.status_code, r.json())
        assert r.status_code == 200 and r.json()["name"] == "virginica"


def test_wrong_length_422():
    with TestClient(app) as c:
        r = c.post("/v1/predict", json={"features": [1.0, 2.0, 3.0]})
        print(r.status_code, r.json()["detail"][0]["type"], r.json()["detail"][0]["loc"])
        assert r.status_code == 422


def test_typo_key_and_bad_type_422():
    with TestClient(app) as c:
        r1 = c.post("/v1/predict", json={"feature": [1, 2, 3, 4]})
        r2 = c.post("/v1/predict", json={"features": [1, 2, "abc", 4]})
        print(r1.status_code, [e["type"] for e in r1.json()["detail"]])
        print(r2.status_code, [e["type"] for e in r2.json()["detail"]])
        assert r1.status_code == r2.status_code == 422
```
```bash
# make the model once (see code/mkmodel.py), then:
cd code && python -m pytest q01 -q -s
cd q01 && MODEL_PATH=/tmp/claude-0/b6_q1_12/models/iris_v1.onnx python -m uvicorn app:app --port 8101 --log-level warning &
curl -s -i localhost:8101/readyz | sed -n '1p;$p'
curl -s -X POST localhost:8101/v1/predict -H 'content-type: application/json' -d '{"features":[6.7,3.0,5.2,2.3]}'
curl -s -w ' [HTTP %{http_code}]\n' -X POST localhost:8101/v1/predict -H 'content-type: application/json' -d '{"features":[1,2,3]}'
kill %1
```

**Output (my run):** fastapi 0.162.0, pydantic 2.14.1, onnxruntime 1.31.0, uvicorn 0.54.0, Python 3.13 (one sandbox, check current docs for your versions). Pytest with `-s`:
```
200 {'label': 2, 'name': 'virginica', 'probabilities': [0.0001, 0.0807, 0.9193]}
422 too_short ['body', 'features']
422 ['missing', 'extra_forbidden']
422 ['float_parsing']
3 passed, 1 warning in 0.46s
```
Real uvicorn on localhost:8101 plus curl:
```
HTTP/1.1 200 OK
{"status":"ready"}
{"label":2,"name":"virginica","probabilities":[0.0001,0.0807,0.9193]}
{"detail":[{"type":"too_short","loc":["body","features"],"msg":"List should have at least 4 items after validation, not 3","input":[1,2,3],"ctx":{"field_type":"List","min_length":4,"actual_length":3}}]} [HTTP 422]
```
The server was stopped afterwards. The one warning is a Starlette notice about the TestClient and httpx; it still works.

**Follow-ups:**
- *Why not load the model at import time?* Tests and tools that import the module would pay the load cost, and failures hit before the app can report them. Lifespan gives one clear place.
- *What does `with TestClient(app)` do?* It runs lifespan. Without `with`, the model is not loaded (Q4 proves this).
- *How do I return 400 instead of 422?* You can register a handler, but 422 is the FastAPI default and clients usually cope; pick one and keep it consistent (Q8).

**Common mistakes:**
- Loading the model inside the endpoint.
- Using `list` with no length limit, so a 3-feature request crashes inside the model as a 500.
- Forgetting `extra="forbid"` and silently ignoring a misspelled field.
- Testing without `with TestClient(app)` and wondering why `app.state.session` is missing.

---

### Q2 ⭐⭐⭐ 🟡 async def versus def for a FastAPI model endpoint. Explain the event loop, why a CPU-bound or blocking model call inside async def freezes every other request (including the health check), how plain def endpoints run in a threadpool, when async def is right (awaiting an HTTP call, a database or a queue), and the fixes for heavy inference (def endpoint, run_in_threadpool, a process pool, or a separate model server). Include the GIL point: threads help only when the model call releases the GIL, as ONNX Runtime and NumPy mostly do. Show a small experiment where a 0.3 s blocking call in async def delays a concurrent /health call and the def version does not. Run it with httpx on localhost and show the timings as labelled machine-specific.
**Asked at:** FastAPI docs and tutorials (fastapi.tiangolo.com advanced events/lifespan page, reintech.io 'FastAPI ML model serving production REST APIs', docs.truefoundry.com deploy-model-fastapi; search snippets only, not opened); docs and tutorials, not interview reports; ML engineer and MLOps roles that ship model APIs, including IT-services firms, product companies and GCCs
**Say this first (1 line):** `async def` runs on the single event loop thread, so a blocking model call inside it freezes everything, including `/health`; a plain `def` endpoint runs in a threadpool and does not.

**Then explain:**
- One event loop thread handles all `async def` code. It only switches tasks at an `await`. A `time.sleep(0.3)` or a 300 ms `session.run()` has no await, so nothing else runs for 300 ms. Health probes time out and the orchestrator may kill a healthy pod.
- FastAPI runs a plain `def` endpoint in a worker thread (anyio threadpool, 40 threads by default; check current docs). The loop stays free.
- Use `async def` only when the body awaits something: an HTTP call, a database driver with async support, a queue. Use `def` for CPU-bound or blocking work like model inference.
- GIL point: threads only help if the call releases the GIL. ONNX Runtime and NumPy mostly do, so threads give real parallelism. Pure Python loops and many Python pre-processing steps do not, so threads will not speed them up.
- Fixes for heavy inference: `def` endpoint, `await run_in_threadpool(fn)` from an async endpoint, a process pool for pure-Python CPU work, or a separate model server (Triton, BentoML) when you need batching or GPUs.
- Failure mode: the threadpool is finite. Too many slow `def` requests queue up behind it; limit concurrency and set timeouts.

**Example:** four requests of 0.3 s each. On the event loop they run one after another, about 4 x 0.3 = 1.2 s total. In threads (and a work call that really does sleep and not compute) they overlap, about 0.3 s total. A `/health` call that arrives 50 ms into a 300 ms blocking call waits about 300 - 50 = 250 ms.

**Code:**
```python
# ===== q02/app.py =====
import time
from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool

app = FastAPI()

def heavy():                      # stands in for a blocking model call (0.3 s)
    time.sleep(0.3)
    return {"ok": True}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/slow_async")           # BAD: blocking call on the event loop
async def slow_async():
    return heavy()

@app.get("/slow_def")             # OK: FastAPI runs plain def in a threadpool
def slow_def():
    return heavy()

@app.get("/slow_async_pool")      # OK: async def, but blocking work pushed to a thread
async def slow_async_pool():
    return await run_in_threadpool(heavy)

# ===== q02/experiment.py =====
import asyncio, time, httpx

BASE = "http://127.0.0.1:8102"

async def trial(client, path):
    slow = asyncio.create_task(client.get(path))
    await asyncio.sleep(0.05)                      # slow request is now running
    t = time.perf_counter()
    h = await client.get("/health")
    health_ms = (time.perf_counter() - t) * 1000
    await slow
    return health_ms

async def main():
    async with httpx.AsyncClient(base_url=BASE, timeout=10) as c:
        await c.get("/health")                     # warm up
        t = time.perf_counter(); await c.get("/health")
        print(f"idle /health            : {(time.perf_counter()-t)*1000:7.1f} ms")
        for path in ["/slow_async", "/slow_def", "/slow_async_pool"]:
            ms = await trial(c, path)
            print(f"/health during {path:17s}: {ms:7.1f} ms")
        # 4 concurrent slow requests, total wall time
        for path in ["/slow_async", "/slow_def"]:
            t = time.perf_counter()
            await asyncio.gather(*[c.get(path) for _ in range(4)])
            print(f"4 concurrent {path:12s} wall: {(time.perf_counter()-t)*1000:7.1f} ms")

asyncio.run(main())
```
```bash
cd code/q02
python -m uvicorn app:app --port 8102 --log-level warning &
python -I experiment.py
kill %1
```

**Output (my run):** machine-specific, a 4-core sandbox, not a benchmark. `time.sleep` stands in for a model call that releases the GIL.
```
idle /health            :     2.6 ms
/health during /slow_async      :   253.3 ms
/health during /slow_def        :     3.1 ms
/health during /slow_async_pool :     2.7 ms
4 concurrent /slow_async  wall:  1208.2 ms
4 concurrent /slow_def    wall:   308.1 ms
```
The 253 ms matches the hand estimate (300 minus the 50 ms head start). The server was stopped afterwards.

**Follow-ups:**
- *Is `async def` faster?* Not for CPU work. It only helps when you wait on I/O.
- *Can I call a sync library from async def?* Only through `run_in_threadpool` or `asyncio.to_thread`.
- *What about a heavy pure-Python model?* The GIL blocks thread parallelism, so use processes (Q3) or a model server.

**Common mistakes:**
- Marking everything `async def` out of habit.
- Calling `requests` or `session.run` inside `async def`.
- Putting the health check behind the same blocked loop and not noticing until pods restart.
- Assuming the 40-thread default is infinite.

---

### Q3 ⭐⭐⭐ 🟡 Workers and process model for a model API: uvicorn --workers, gunicorn with uvicorn workers, one process per CPU core, why each worker loads its own copy of the model (memory multiplies), preloading and copy-on-write, threads inside a worker, the number of intra-op threads in the inference library versus the number of workers (oversubscription), and when to scale with more replicas instead of more workers. Give a sizing rule of thumb with arithmetic for a 500 MB model on a 4-core, 8 GB pod, and show how you would check which worker answered a request (a pid in the response). Run a two-worker uvicorn on localhost and show the pids; load tests are not claims about production.
**Asked at:** FastAPI docs and tutorials (fastapi.tiangolo.com advanced events/lifespan page, reintech.io 'FastAPI ML model serving production REST APIs', docs.truefoundry.com deploy-model-fastapi; search snippets only, not opened); docs and tutorials, not interview reports; ML engineer and MLOps roles that ship model APIs, including IT-services firms, product companies and GCCs
**Say this first (1 line):** One worker is one process with its own copy of the model, so I size workers by cores and by memory (copies multiply), keep intra-op threads times workers at or below cores, and add replicas when one pod is full.

**Then explain:**
- `uvicorn --workers N` starts N processes. Each runs the lifespan and loads the model: 500 MB model times 4 workers is about 2 GB, not 500 MB. `gunicorn -k uvicorn.workers.UvicornWorker` (a worker class from the uvicorn project; check current docs, it has moved packages over time) adds a mature process manager that restarts crashed workers.
- Preloading (`--preload` in gunicorn) loads the model once in the parent, and forked children share pages copy-on-write. It saves memory only if the weights are not touched or rewritten; Python reference counting can still dirty pages for Python objects, but large NumPy or ONNX buffers usually stay shared. Measure RSS, do not assume.
- Oversubscription: ONNX Runtime uses `intra_op_num_threads` threads per call. 4 workers x 4 threads on 4 cores means 16 busy threads fighting for 4 cores, so latency gets worse. Rule: workers x intra_op_threads <= cores.
- Threads inside a worker (the `def` threadpool) share one model copy, which is memory-cheap; processes give isolation and GIL-free parallelism for Python code.
- Replicas vs workers: when one pod is out of cores or memory, add replicas. Replicas also give failure isolation and rolling updates. Workers inside one pod cannot exceed the pod's limits.
- Failure modes: OOM kill from forgetting that memory multiplies; a worker crash during a request; uneven distribution, because the kernel hands new connections to workers, so one long-lived connection pins one worker.

**Example (500 MB model, 4-core, 8 GB pod):** reserve about 1.5 GB for OS and runtime, leaving 6.5 GB (6,656 MB). Assume about 1.3 x 500 = 650 MB per worker (weights plus buffers; measure yours). Memory allows 6,656 / 650 = 10 copies, cores allow 4, so start with 4 workers and 1 intra-op thread each. If the model is bigger, say 3 GB, memory allows only 2 copies; then use 2 workers with 2 threads each, or use threads inside one worker.

**Code:**
```python
# ===== q03/app.py =====
import os
from contextlib import asynccontextmanager
import numpy as np, onnxruntime as ort
from fastapi import FastAPI, Request

@asynccontextmanager
async def lifespan(app):
    so = ort.SessionOptions()
    # threads INSIDE one inference call. workers x intra_op threads should be <= cores
    so.intra_op_num_threads = int(os.environ.get("INTRA_OP", "1"))
    app.state.s = ort.InferenceSession(os.environ["MODEL_PATH"], so, providers=["CPUExecutionProvider"])
    app.state.pid = os.getpid()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/predict")
def predict(request: Request, features: list[float]):
    x = np.asarray([features], dtype=np.float32)
    label, _ = request.app.state.s.run(None, {"X": x})
    return {"label": int(label[0]), "pid": request.app.state.pid}

# ===== q03/who.py =====
import collections, httpx
c = collections.Counter()
for _ in range(40):
    with httpx.Client() as cl:                       # new connection each time
        c[cl.post("http://127.0.0.1:8103/predict", json=[6.7, 3.0, 5.2, 2.3]).json()["pid"]] += 1
print("distinct worker pids:", len(c), "| answers per pid:", sorted(c.values(), reverse=True))

# ===== q03/sizing.py =====
model_mb, cores, pod_gb, reserve_gb = 500, 4, 8, 1.5      # reserve: OS + runtime + headroom
usable_mb = (pod_gb - reserve_gb) * 1024
by_mem = int(usable_mb // (model_mb * 1.3))               # 1.3 = weights + activations/buffers per copy
workers = min(cores, by_mem)
print(f"usable {usable_mb:.0f} MB; each worker ~{model_mb*1.3:.0f} MB -> memory allows {by_mem}")
print(f"cores allow {cores} -> start with {workers} workers, intra_op_threads = {max(1, cores // workers)}")
```
```bash
cd code/q03
MODEL_PATH=/tmp/claude-0/b6_q1_12/models/iris_v1.onnx python -m uvicorn app:app --port 8103 --workers 2 --log-level warning &
python -I who.py      # 40 requests, a new connection each time
python -I sizing.py
kill %1               # stops the parent, which stops its workers
```

**Output (my run):** two workers on localhost:8103, machine-specific:
```
distinct worker pids: 2 | answers per pid: [21, 19]
usable 6656 MB; each worker ~650 MB -> memory allows 10
cores allow 4 -> start with 4 workers, intra_op_threads = 1
```
Two different pids answered, roughly evenly. This is a distribution demo, not a load test. I stopped the server afterwards and checked no process of mine was left.

**Follow-ups:**
- *Why not just 16 workers on 4 cores?* Context switching and memory, with no extra throughput.
- *In Kubernetes, workers or replicas?* Often 1 to a few workers per pod and scale with replicas, so the autoscaler and failures work at pod level (Part 3 owns this).
- *How do you check memory?* Look at RSS per worker, and compare with and without preload.

**Common mistakes:**
- Setting workers = cores x 2 by web-server habit, then OOM.
- Ignoring `intra_op_num_threads`.
- Assuming preload always saves memory.
- Reading a pid demo as proof of scaling.

---

### Q4 ⭐⭐⭐ 🟡 Health, liveness, readiness and startup checks for a model service. Explain what each probe answers, why the model-loaded flag belongs in readiness and not liveness (a restart loop while a big model downloads), a startup probe for slow loads, why a health route that always returns 200 hides a dead worker, a deep check that runs one tiny prediction (and its cost), and what the load balancer does on 503. Show FastAPI /livez, /readyz and /startupz routes and a pytest that proves /readyz is 503 before lifespan runs and 200 after. Kubernetes probe YAML is shown and validated with pyyaml only; Part 3 owns Kubernetes itself.
**Asked at:** FastAPI docs and tutorials (fastapi.tiangolo.com advanced events/lifespan page, reintech.io 'FastAPI ML model serving production REST APIs', docs.truefoundry.com deploy-model-fastapi; search snippets only, not opened); docs and tutorials, not interview reports; ML engineer and MLOps roles that ship model APIs, including IT-services firms, product companies and GCCs
**Say this first (1 line):** Liveness asks "is the process stuck, restart it?", readiness asks "send me traffic now?", startup asks "has the slow boot finished?", and "model loaded" belongs in readiness, never liveness.

**Then explain:**
- Liveness (`/livez`): cheap, no model, no dependencies. If it fails, the orchestrator restarts the container. Putting "model loaded" here causes a restart loop: the model takes 3 minutes to download, liveness fails, pod restarts, download starts again, forever.
- Readiness (`/readyz`): 503 until the model is loaded; the load balancer takes the pod out of rotation on 503 and puts it back on 200. Nothing is restarted.
- Startup (`/startupz`): gives slow loads a long window (period x failureThreshold) before liveness starts to count. Without it you set a huge liveness delay for everyone.
- A route that always returns 200 hides a dead worker or a half-loaded model, and the pod gets traffic it cannot serve.
- Deep check: run one tiny prediction (`/readyz?deep=true`). It proves the graph runs, but it costs CPU every probe and can fail on a transient glitch; use a slow period or run it only at startup, never on a tight loop.
- Catch from my run: if you load the model inside `lifespan` and it blocks, uvicorn does not accept connections until it finishes. The probe then sees connection refused, not 503. That is also "not ready", but if you want a visible 503 and a live `/livez` during loading, start the load in a background task.

**Example:** a 300 MB model that takes 3 s to load. Blocking load: at t = 1.5 s every probe is refused (no listener). Background load: `/livez` 200 and `/readyz` 503 at 1.5 s, then `/readyz` 200 at 4.5 s. YAML window: 5 s x 60 = 300 s startup budget.

**Code:**
```python
# ===== q04/app.py =====
import os, asyncio
from contextlib import asynccontextmanager
import numpy as np, onnxruntime as ort
from fastapi import FastAPI, Request, Response

def _load(app):
    app.state.session = ort.InferenceSession(os.environ["MODEL_PATH"], providers=["CPUExecutionProvider"])
    app.state.loaded = True

@asynccontextmanager
async def lifespan(app):
    app.state.session = None
    app.state.loaded = False
    delay = float(os.environ.get("LOAD_DELAY", "0"))
    if os.environ.get("LOAD_MODE") == "bg":
        # port opens at once; /readyz says 503 until the background load finishes
        async def bg():
            await asyncio.sleep(delay)          # pretend: slow download
            await asyncio.to_thread(_load, app)
        app.state.task = asyncio.create_task(bg())
    else:
        # blocking load: uvicorn does not accept connections until this returns
        await asyncio.sleep(delay)
        _load(app)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/livez")                       # "is the process alive and the loop responsive?" Nothing about the model.
def livez():
    return {"status": "alive"}

@app.get("/startupz")                    # "has the slow start finished?" Used only while booting.
def startupz(request: Request, response: Response):
    if not getattr(request.app.state, "loaded", False):
        response.status_code = 503
        return {"status": "starting"}
    return {"status": "started"}

@app.get("/readyz")                      # "should I get traffic?" Model loaded (+ optional deep check).
def readyz(request: Request, response: Response, deep: bool = False):
    s = getattr(request.app.state, "session", None)
    if s is None:
        response.status_code = 503
        return {"status": "loading"}
    if deep:                             # costs one tiny inference: keep it off the hot probe path
        try:
            s.run(None, {"X": np.zeros((1, 4), dtype=np.float32)})
        except Exception:
            response.status_code = 503
            return {"status": "model_error"}
    return {"status": "ready"}

# ===== q04/test_probes.py =====
import os
os.environ.setdefault("MODEL_PATH", "/tmp/claude-0/b6_q1_12/models/iris_v1.onnx")
from fastapi.testclient import TestClient
from app import app

def test_not_ready_before_lifespan():
    c = TestClient(app)                              # NO `with`: lifespan has not run
    assert c.get("/livez").status_code == 200        # alive...
    r = c.get("/readyz")
    print("before lifespan:", r.status_code, r.json())
    assert r.status_code == 503                      # ...but not ready

def test_ready_after_lifespan():
    with TestClient(app) as c:                       # lifespan ran
        r = c.get("/readyz"); d = c.get("/readyz?deep=true"); s = c.get("/startupz")
        print("after lifespan :", r.status_code, r.json(), "| deep:", d.status_code, "| startup:", s.status_code)
        assert r.status_code == d.status_code == s.status_code == 200

# ===== q04/check_yaml.py =====
import yaml
d = yaml.safe_load(open("probes.yaml"))
for k, v in d.items():
    print(k, v["httpGet"]["path"], "period", v["periodSeconds"], "fail", v["failureThreshold"])
assert d["livenessProbe"]["httpGet"]["path"] != d["readinessProbe"]["httpGet"]["path"]
print("max startup window:", d["startupProbe"]["periodSeconds"] * d["startupProbe"]["failureThreshold"], "s")
```
```yaml
# ===== q04/probes.yaml =====
# Container probe block (Kubernetes pod spec fragment). Not applied to a cluster here.
startupProbe:
  httpGet: {path: /startupz, port: 8000}
  periodSeconds: 5
  failureThreshold: 60        # up to 5 min to download and load the model
livenessProbe:
  httpGet: {path: /livez, port: 8000}
  periodSeconds: 10
  failureThreshold: 3
readinessProbe:
  httpGet: {path: /readyz, port: 8000}
  periodSeconds: 5
  failureThreshold: 2
```
```bash
cd code
python -m pytest q04 -q -s
cd q04 && python -I check_yaml.py
for mode in blocking bg; do
  MODEL_PATH=/tmp/claude-0/b6_q1_12/models/iris_v1.onnx LOAD_DELAY=3 LOAD_MODE=$mode python -m uvicorn app:app --port 8104 --log-level warning &
  sleep 1.5; for p in livez readyz; do curl -s -o /dev/null -w "t=1.5s /$p %{http_code}\n" localhost:8104/$p; done
  sleep 3; curl -s -o /dev/null -w "t=4.5s /readyz %{http_code}\n" localhost:8104/readyz
  kill %1; wait
done
```

**Output (my run):** pytest and pyyaml, TestClient plus real uvicorn on localhost:8104 (timings are demo values, 3 s was an artificial delay).
```
before lifespan: 503 {'status': 'loading'}
after lifespan : 200 {'status': 'ready'} | deep: 200 | startup: 200
2 passed, 1 warning in 0.50s
startupProbe /startupz period 5 fail 60
livenessProbe /livez period 10 fail 3
readinessProbe /readyz period 5 fail 2
max startup window: 300 s
== LOAD_MODE=blocking
t=1.5s /livez 000
t=1.5s /readyz 000
t=4.5s /readyz 200
== LOAD_MODE=bg
t=1.5s /livez 200
t=1.5s /readyz 503
t=4.5s /readyz 200
```
(`000` is curl's code for connection refused.) The YAML is not applied to a cluster: Kubernetes was not executed, and only pyyaml parsed the file and asserted that liveness and readiness use different paths. Check current Kubernetes docs for probe fields.

**Follow-ups:**
- *What does the load balancer do on 503?* Stops routing to that instance until the probe passes again; in-flight requests finish.
- *Should readiness check downstream dependencies like a feature store?* Carefully. If a shared dependency is down, every pod goes unready at once and you serve nothing; often better to degrade or fail per request.
- *Why a startup probe and not a long initial delay?* The delay is paid on every restart even when boot is fast; the startup probe ends as soon as it passes.

**Common mistakes:**
- Same endpoint for liveness and readiness.
- Liveness that calls the model or the database.
- Deep check on a one-second probe loop.
- Testing without `with TestClient(app)` and forgetting that lifespan did not run (which, deliberately, is the 503 proof here).

---

### Q5 ⭐⭐⭐ 🟢 Batch versus real-time (online) versus streaming inference. Define each, give the deciding factors (who waits, freshness of features, volume, cost per prediction, failure impact, whether predictions can be precomputed), and one example each (nightly churn scores, fraud check at checkout, per-event anomaly scoring). Explain the hybrid pattern of precomputing scores in batch and serving them from a key-value store, and when near-real-time micro-batching is the compromise. Give a decision table and a small function that picks a mode from stated requirements, with tests. Runs locally; nothing is deployed.
**Asked at:** Serving interview-prep and glossary pages (nerdleveltech.com MLOps engineer interviews 'model serving infrastructure', techinterview.org MLOps interview and model-serving design posts, wecreateproblems.com MLOps interview questions, insertchat.com model-serving glossary; search snippets only, not opened); editorial guides, not verified candidate reports; MLOps, ML platform and ML engineer roles
**Say this first (1 line):** Batch scores many rows on a schedule, online scores one request while someone waits, streaming scores each event as it arrives, and I pick by who is waiting, how fresh the inputs must be, and whether I can precompute.

**Then explain:**
- Batch: nightly job, high throughput, cheap per prediction, results stored. Failure impact is low and retryable. Example: nightly churn scores.
- Online (real-time): request in, answer in tens to hundreds of milliseconds, a human or a blocking system waits. Needs always-on capacity and p99 care. Example: fraud check at checkout.
- Streaming: a consumer scores each event from a log as it arrives; nobody blocks on it, but freshness is seconds. Example: per-event anomaly scoring. Kafka itself is Part 9.
- Hybrid: precompute scores in batch, write to a key-value store, serve a lookup online. Fast and cheap, but stale up to the batch interval and only works when the input space is known (all customers, all products).
- Micro-batch: collect events for seconds to minutes and score together. The compromise when 5-minute freshness is fine but per-event infrastructure is not worth it.
- Failure modes: online with heavy features hits the p99 budget; batch with a missed run serves stale or no scores (monitor job freshness); hybrid serves a score for a user who changed behaviour an hour ago.

**Example:**
| Need | Who waits | Freshness | Precompute? | Mode |
|---|---|---|---|---|
| Churn score per customer | nobody | 1 day | yes | batch |
| Card fraud check | cashier | live inputs | no | online |
| Sensor anomaly per event | nobody | seconds | no | streaming |
| "Recommended for you" page | user | 1 day ok | yes | batch + key-value |
| Dashboard refreshed every 5 min | nobody | minutes | no | micro-batch |

**Code:**
```python
# ===== q05/pick_mode.py =====
from dataclasses import dataclass

@dataclass
class Req:
    human_waiting: bool            # is a person or a blocking system waiting for the answer?
    max_staleness_s: float         # how old may the score be? (0 = must use fresh inputs)
    can_precompute: bool           # is the input space small/known (e.g. all customers)?
    events_per_s: float = 0.0      # continuous event stream volume (0 = none)
    latency_budget_ms: float = 0.0 # only meaningful for human_waiting

def pick_mode(r: Req) -> str:
    if r.max_staleness_s < 0 or r.events_per_s < 0:
        raise ValueError("negative input")
    if r.human_waiting:
        if r.max_staleness_s >= 3600 and r.can_precompute:
            return "batch+kv"                     # precompute, serve lookup (hybrid)
        return "online"
    if r.events_per_s > 0:
        return "streaming" if r.max_staleness_s < 60 else "micro-batch"
    return "batch"

# ===== q05/test_pick_mode.py =====
import pytest
from pick_mode import Req, pick_mode

@pytest.mark.parametrize("req,expected", [
    (Req(False, 86400, True),                 "batch"),        # nightly churn scores
    (Req(True, 0, False, latency_budget_ms=100), "online"),    # fraud check at checkout
    (Req(False, 5, False, events_per_s=2000), "streaming"),    # per-event anomaly scoring
    (Req(False, 300, False, events_per_s=2000), "micro-batch"),# 5-minute freshness is enough
    (Req(True, 86400, True),                  "batch+kv"),     # "recommended for you" page
    (Req(True, 86400, False),                 "online"),       # cannot precompute -> must compute live
])
def test_modes(req, expected):
    assert pick_mode(req) == expected

def test_bad_input():
    with pytest.raises(ValueError):
        pick_mode(Req(True, -1, False))
```
```bash
cd code/q05 && python -m pytest -q -p no:cacheprovider
```

**Output (my run):** local only; nothing was deployed, no queue or key-value store was run.
```
7 passed in 0.02s
```
The tests encode the table above, including the error case for negative input.

**Follow-ups:**
- *When is batch a better answer than online even when the user waits?* When the answer can be precomputed and a lookup is enough.
- *What breaks the hybrid?* New entities (a new user has no precomputed score), so keep an online fallback or a default.
- *Streaming vs micro-batch?* If staleness under a minute matters, stream; otherwise micro-batch is simpler.

**Common mistakes:**
- Building online serving for a report nobody reads before morning.
- Calling something real-time when the features are a day old.
- Forgetting the cold-start entity in the hybrid pattern.
- Treating the function in this answer as a rule: it is a talking aid, the real choice includes cost and team skills.

---

### Q6 ⭐⭐⭐ 🟡 Latency, throughput and percentiles for a model API. Define p50, p95, p99, throughput (QPS) and utilisation; explain why averages hide tail latency, why p99 matters when one page makes many calls (tail amplification), Little's law (concurrency = throughput x latency), the knee of the latency-versus-load curve, and how queueing makes p99 explode near saturation. Show a script that computes percentiles from a list of timings with numpy and checks them by hand on a tiny list, then measures a real local FastAPI endpoint for 200 sequential calls. Label every number as this sandbox only, not a benchmark.
**Asked at:** Serving interview-prep and glossary pages (nerdleveltech.com MLOps engineer interviews 'model serving infrastructure', techinterview.org MLOps interview and model-serving design posts, wecreateproblems.com MLOps interview questions, insertchat.com model-serving glossary; search snippets only, not opened); editorial guides, not verified candidate reports; MLOps, ML platform and ML engineer roles
**Say this first (1 line):** I report p50, p95 and p99 plus throughput, never the average, because the tail is what users and downstream callers feel, and the tail explodes as utilisation nears 100 percent.

**Then explain:**
- Percentile p99 = 99 percent of requests were at least this fast. Throughput (QPS) = completed requests per second. Utilisation = busy time over capacity.
- Averages hide tails: ten timings `1..9, 100 ms` have mean 14.5 ms but p99 near 92 ms.
- Tail amplification: if a page makes k calls and each is slower than its p99 once per 100, then the chance at least one is slow is 1 - 0.99^k. For k = 50 that is 39.5 percent of pages.
- Little's law: concurrency in flight = throughput x latency. 200 req/s at 50 ms means 10 requests in flight, which sizes thread pools and connection limits.
- The knee: latency is flat at low load, then curves up. Queueing makes waiting time grow roughly like 1 / (1 - utilisation). Plan capacity at 50 to 70 percent, not 95.
- Failure modes: measuring with a coordinated client (waits for each response, so it hides the queue it caused); measuring warm-up calls; one-machine client being the bottleneck; fixed inputs that hit a cache.

**Example (hand check):** timings `[1,2,3,4,5,6,7,8,9,100]`. NumPy's linear rule: p50 rank = 0.5 x 9 = 4.5, between 5 and 6, so 5.5. p99 rank = 0.99 x 9 = 8.91, so 9 + 0.91 x (100 - 9) = 91.81. The script asserts these.

**Code:**
```python
# ===== q06/pct.py =====
import numpy as np
# hand check: 10 timings in ms, sorted: 1..9 and 100
t = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]
print("mean", np.mean(t), "p50", np.percentile(t, 50), "p90", np.percentile(t, 90), "p99", np.percentile(t, 99))
# numpy's default 'linear' rule: rank = p/100*(n-1) = 0.5*9 = 4.5 -> between 5 and 6 -> 5.5
# p90: rank 8.1 -> 9 + 0.1*(100-9) = 18.1 ; p99: rank 8.91 -> 9 + 0.91*91 = 91.81
assert np.percentile(t, 50) == 5.5 and abs(np.percentile(t, 90) - 18.1) < 1e-9 and abs(np.percentile(t, 99) - 91.81) < 1e-9
# tail amplification: a page makes k calls; P(at least one call is slower than its own p99) = 1 - 0.99**k
for k in (1, 10, 50, 100):
    print(f"page with {k:3d} calls: {100*(1-0.99**k):5.1f}% of pages see at least one call beyond p99")
# Little's law: concurrency = throughput x latency
print("Little: 200 req/s x 0.050 s =", 200 * 0.050, "requests in flight")

# ===== q06/queue_sim.py =====
"""Single server, Poisson arrivals, exponential service (mean 10 ms). Shows p99 vs utilisation."""
import numpy as np
rng = np.random.default_rng(0)
n, service_mean = 200_000, 0.010
S = rng.exponential(service_mean, n)
for rho in (0.3, 0.5, 0.7, 0.8, 0.9, 0.95):
    A = rng.exponential(service_mean / rho, n)          # inter-arrival gaps
    w = np.zeros(n)                                      # waiting time (Lindley recursion)
    for i in range(1, n):
        w[i] = max(0.0, w[i-1] + S[i-1] - A[i])
    lat = (w + S) * 1000
    print(f"utilisation {rho:4.2f}: p50 {np.percentile(lat,50):6.1f} ms  p99 {np.percentile(lat,99):7.1f} ms")

# ===== q06/measure.py =====
import time, sys, httpx, numpy as np
url = sys.argv[1]; body = {"features": [6.7, 3.0, 5.2, 2.3]}
with httpx.Client() as c:
    for _ in range(20): c.post(url, json=body)            # warm-up, not measured
    t = []
    for _ in range(200):
        s = time.perf_counter(); r = c.post(url, json=body); t.append((time.perf_counter() - s) * 1000)
        assert r.status_code == 200
p = np.percentile(t, [50, 95, 99])
print(f"200 sequential calls: mean {np.mean(t):.2f} ms  p50 {p[0]:.2f}  p95 {p[1]:.2f}  p99 {p[2]:.2f}  max {max(t):.2f} (this sandbox only)")
```
```bash
cd code/q06
python -I pct.py
python -I queue_sim.py
# serve the Q1 app, then measure 200 sequential calls (twice)
cd ../q01 && MODEL_PATH=/tmp/claude-0/b6_q1_12/models/iris_v1.onnx python -m uvicorn app:app --port 8106 --log-level warning &
sleep 3; python -I ../q06/measure.py http://127.0.0.1:8106/v1/predict; python -I ../q06/measure.py http://127.0.0.1:8106/v1/predict; kill %1
```

**Output (my run):** every latency number below is this sandbox only (4 cores, localhost, one client), a demo, not a benchmark.
```
mean 14.5 p50 5.5 p90 18.099999999999966 p99 91.81000000000002
page with   1 calls:   1.0% of pages see at least one call beyond p99
page with  10 calls:   9.6% of pages see at least one call beyond p99
page with  50 calls:  39.5% of pages see at least one call beyond p99
page with 100 calls:  63.4% of pages see at least one call beyond p99
Little: 200 req/s x 0.050 s = 10.0 requests in flight
utilisation 0.30: p50    9.9 ms  p99   66.2 ms
utilisation 0.50: p50   13.9 ms  p99   92.6 ms
utilisation 0.70: p50   23.1 ms  p99  158.6 ms
utilisation 0.80: p50   34.0 ms  p99  233.3 ms
utilisation 0.90: p50   67.3 ms  p99  448.5 ms
utilisation 0.95: p50  139.3 ms  p99  758.3 ms
200 sequential calls: mean 2.20 ms  p50 1.97  p95 3.56  p99 5.37  max 7.19 (this sandbox only)
200 sequential calls: mean 2.33 ms  p50 2.15  p95 3.33  p99 6.21  max 8.48 (this sandbox only)
```
The queue table is a simulation (single server, random arrivals, mean service 10 ms), not a real service. The two live runs differ, which is the point: report ranges and repeat. The server was stopped afterwards.

**Follow-ups:**
- *Why do percentiles not add up across services?* You cannot sum p99s; measure end to end or combine distributions.
- *What is a good p99 target?* Whatever the product's SLA says; derive the target from the user flow, not from a number you read somewhere.
- *Sequential vs concurrent test?* Sequential shows service time; concurrent shows queueing. You need both.

**Common mistakes:**
- Quoting the average.
- Load testing the load generator.
- Including warm-up and cold-start calls in the percentiles.
- Setting capacity for 95 percent utilisation.

---

### Q7 ⭐⭐⭐ 🟡 Dynamic (micro) batching for model serving. Explain why batching raises throughput (one matrix multiply for many rows, GPU utilisation), the trade-off (a request waits up to max_wait_ms to fill a batch, so p50 rises while throughput rises), the two knobs (max_batch_size and max_wait), and where it lives (Triton dynamic batcher, BentoML adaptive batching, your own code). Write a small asyncio micro-batcher for a FastAPI endpoint: requests put a future in a queue, a background task flushes on size or timeout, and results are returned per request in order. Run it with ONNX Runtime on localhost with concurrent httpx calls and show batch sizes seen and the effect on latency, labelled machine-specific. Cover the failure modes: one bad row failing the batch, cancelled requests, and shutdown.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** Dynamic batching holds each request for a few milliseconds so many can share one model call; throughput goes up, but p50 goes up by up to the wait time, so I tune `max_batch_size` and `max_wait` against my latency target.

**Then explain:**
- Why it works: a model call has fixed cost (weight reads, kernel launch, Python overhead). 32 rows in one matrix multiply cost far less than 32 separate calls. On a GPU the effect is bigger.
- The trade-off: a request may wait up to `max_wait_ms` for company. Light traffic means batches of 1 and you only pay the wait; heavy traffic fills batches fast and the wait shrinks.
- The knobs: `max_batch_size` (cap per call) and `max_wait` (deadline for the first request in a batch). Triton calls them `max_batch_size` and `max_queue_delay_microseconds` in its dynamic batcher; BentoML has adaptive batching (`batchable=True`); check each tool's current docs. Or write your own, as below.
- Design: each request puts `(row, future)` in an `asyncio.Queue` and awaits the future. One background task collects until size or timeout, runs the model in a thread, and sets each future by position, so order is preserved.
- Failure modes covered in the code: one bad row fails the whole batch (fix: retry rows one by one and fail only the bad one; better still, validate input before it enters the queue); a cancelled client (skip futures that are already done); shutdown (cancel the loop and fail queued futures with 503). Not covered: the batch loop crashing (supervise it), unbounded queue growth (bound it and return 429), and input shapes that differ between rows.

**Example:** `max_batch=32`, `max_wait=5 ms`. 3 requests arrive within 5 ms, so the batch is 3 and runs after at most 5 ms. 40 arrive at once, so a batch of 32 runs immediately and the other 8 start the next batch.

**Code:**
```python
# ===== q07/make_mlp.py =====
import sys, torch
torch.manual_seed(0)
m = torch.nn.Sequential(torch.nn.Linear(512, 2048), torch.nn.ReLU(), torch.nn.Linear(2048, 2048),
                        torch.nn.ReLU(), torch.nn.Linear(2048, 10)).eval()
torch.onnx.export(m, torch.zeros(1, 512), sys.argv[1], input_names=["x"], output_names=["y"],
                  dynamic_axes={"x": {0: "b"}, "y": {0: "b"}}, dynamo=False)
print("wrote", sys.argv[1])

# ===== q07/app.py =====
import asyncio, os
from contextlib import asynccontextmanager
import numpy as np, onnxruntime as ort
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

MAX_BATCH = int(os.environ.get("MAX_BATCH", "32"))
MAX_WAIT = float(os.environ.get("MAX_WAIT_MS", "5")) / 1000

class Req(BaseModel):
    x: list[float] = Field(min_length=512, max_length=512)

class MicroBatcher:
    def __init__(self, session, max_batch, max_wait):
        self.s, self.max_batch, self.max_wait = session, max_batch, max_wait
        self.q: asyncio.Queue = asyncio.Queue()
        self.sizes: list[int] = []
        self.task = None

    def start(self):
        self.task = asyncio.create_task(self._loop())

    async def submit(self, row: np.ndarray):
        fut = asyncio.get_running_loop().create_future()
        await self.q.put((row, fut))
        return await fut                              # cancelled client -> fut is cancelled

    def _run(self, rows):                             # blocking; runs in a worker thread
        if any(r[0] == -999.0 for r in rows):         # demo "poison" row that makes the model raise
            raise ValueError("bad row")
        return self.s.run(None, {"x": np.stack(rows)})[0]

    async def _loop(self):
        loop = asyncio.get_running_loop()
        while True:
            row, fut = await self.q.get()
            items = [(row, fut)]
            deadline = loop.time() + self.max_wait
            while len(items) < self.max_batch:
                left = deadline - loop.time()
                if left <= 0:
                    break
                try:
                    items.append(await asyncio.wait_for(self.q.get(), left))
                except asyncio.TimeoutError:
                    break
            items = [(r, f) for r, f in items if not f.done()]     # drop cancelled requests
            if not items:
                continue
            self.sizes.append(len(items))
            try:
                out = await asyncio.to_thread(self._run, [r for r, _ in items])
                for (_, f), o in zip(items, out):                  # same order in, same order out
                    if not f.done(): f.set_result(o)
            except Exception:
                for r, f in items:                                  # isolate the bad row: retry one by one
                    try:
                        o = (await asyncio.to_thread(self._run, [r]))[0]
                        if not f.done(): f.set_result(o)
                    except Exception as e:
                        if not f.done(): f.set_exception(e)

    async def stop(self):
        self.task.cancel()
        while not self.q.empty():                                   # fail whatever is still queued
            _, f = self.q.get_nowait()
            if not f.done(): f.set_exception(RuntimeError("shutting down"))

@asynccontextmanager
async def lifespan(app):
    so = ort.SessionOptions(); so.intra_op_num_threads = 1
    app.state.b = MicroBatcher(ort.InferenceSession(os.environ["MLP_PATH"], so, providers=["CPUExecutionProvider"]),
                               MAX_BATCH, MAX_WAIT)
    app.state.b.start()
    yield
    await app.state.b.stop()

app = FastAPI(lifespan=lifespan)

@app.post("/predict")
async def predict(req: Req, request: Request):
    try:
        y = await request.app.state.b.submit(np.asarray(req.x, dtype=np.float32))
    except ValueError:
        raise HTTPException(422, "model rejected this row")
    except RuntimeError:
        raise HTTPException(503, "shutting down")
    return {"argmax": int(np.argmax(y))}

@app.get("/stats")
def stats(request: Request):
    s = request.app.state.b.sizes
    return {"batches": len(s), "mean_batch": round(sum(s) / max(1, len(s)), 2), "max_batch": max(s, default=0)}

# ===== q07/load.py =====
import asyncio, time, sys, httpx, numpy as np
BASE = "http://127.0.0.1:8107"; CONC, EACH = 32, 25
rng = np.random.default_rng(1)
async def worker(c, lat):
    for _ in range(EACH):
        body = {"x": rng.standard_normal(512).tolist()}
        t = time.perf_counter(); r = await c.post("/predict", json=body); lat.append((time.perf_counter() - t) * 1000)
        assert r.status_code == 200
async def main():
    async with httpx.AsyncClient(base_url=BASE, timeout=30, limits=httpx.Limits(max_connections=CONC)) as c:
        for _ in range(10): await c.post("/predict", json={"x": [0.0] * 512})
        await c.get("/stats"); lat = []; t0 = time.perf_counter()
        await asyncio.gather(*[worker(c, lat) for _ in range(CONC)])
        wall = time.perf_counter() - t0; st = (await c.get("/stats")).json()
        p = np.percentile(lat, [50, 99])
        print(f"{CONC*EACH} reqs, {CONC} concurrent: {CONC*EACH/wall:6.0f} req/s  p50 {p[0]:6.1f} ms  p99 {p[1]:6.1f} ms | server stats incl. warm-up: {st}")
asyncio.run(main())

# ===== q07/failures.py =====
import asyncio, httpx
async def main():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8107", timeout=10) as c:
        good = {"x": [0.1] * 512}; bad = {"x": [-999.0] + [0.1] * 511}
        rs = await asyncio.gather(c.post("/predict", json=good), c.post("/predict", json=bad), c.post("/predict", json=good))
        print("good/bad/good in one batch ->", [r.status_code for r in rs])
        # cancelled request: client gives up after 1 ms; server keeps working
        try: await c.post("/predict", json=good, timeout=0.0001)
        except httpx.TimeoutException: print("client timed out (cancelled) ok")
        print("still serving ->", (await c.post("/predict", json=good)).status_code)
asyncio.run(main())

# ===== q07/bench_direct.py =====
import sys, time, numpy as np, onnxruntime as ort
so = ort.SessionOptions(); so.intra_op_num_threads = 1
s = ort.InferenceSession(sys.argv[1], so, providers=["CPUExecutionProvider"])
x = np.random.default_rng(0).standard_normal((32, 512)).astype(np.float32)
def best(f, n=20):
    f(); ts = []
    for _ in range(n):
        t = time.perf_counter(); f(); ts.append(time.perf_counter() - t)
    return min(ts) * 1000
one = best(lambda: [s.run(None, {"x": x[i:i+1]}) for i in range(32)])
bat = best(lambda: s.run(None, {"x": x}))
print(f"32 rows as 32 calls of batch 1: {one:6.1f} ms | one call of batch 32: {bat:6.1f} ms | ratio {one/bat:.1f}x (this sandbox only)")
```
```bash
cd code/q07
python -I make_mlp.py /tmp/claude-0/b6_q1_12/models/mlp.onnx      # 512-2048-2048-10 MLP, random weights, dynamic batch axis
python -I bench_direct.py /tmp/claude-0/b6_q1_12/models/mlp.onnx
for cfg in "1 0" "32 5" "32 20"; do set -- $cfg
  MLP_PATH=/tmp/claude-0/b6_q1_12/models/mlp.onnx MAX_BATCH=$1 MAX_WAIT_MS=$2 python -m uvicorn app:app --port 8107 --log-level warning &
  sleep 3; python -I load.py; python -I load.py; kill %1; wait
done
MLP_PATH=/tmp/claude-0/b6_q1_12/models/mlp.onnx MAX_BATCH=32 MAX_WAIT_MS=20 python -m uvicorn app:app --port 8107 --log-level warning &
sleep 3; python -I failures.py; kill %1
```

**Output (my run):** onnxruntime 1.31.0, CPU, 1 intra-op thread, a 4-core sandbox; everything is machine-specific and not a benchmark. Direct model calls (no HTTP):
```
32 rows as 32 calls of batch 1:   28.2 ms | one call of batch 32:    3.0 ms | ratio 9.6x (this sandbox only)
```
Through the micro-batcher, 32 concurrent clients, 800 requests per run, each config run twice (the "server stats" are cumulative and include warm-up):
```
== MAX_BATCH=1 MAX_WAIT_MS=0
800 reqs, 32 concurrent:    244 req/s  p50   64.2 ms  p99  648.5 ms | server stats incl. warm-up: {'batches': 810, 'mean_batch': 1.0, 'max_batch': 1}
800 reqs, 32 concurrent:    226 req/s  p50   86.8 ms  p99  619.4 ms | server stats incl. warm-up: {'batches': 1620, 'mean_batch': 1.0, 'max_batch': 1}
== MAX_BATCH=32 MAX_WAIT_MS=5
800 reqs, 32 concurrent:    281 req/s  p50   48.8 ms  p99  522.4 ms | server stats incl. warm-up: {'batches': 275, 'mean_batch': 2.95, 'max_batch': 19}
800 reqs, 32 concurrent:    272 req/s  p50   52.0 ms  p99  504.6 ms | server stats incl. warm-up: {'batches': 561, 'mean_batch': 2.89, 'max_batch': 19}
== MAX_BATCH=32 MAX_WAIT_MS=20
800 reqs, 32 concurrent:    235 req/s  p50   68.3 ms  p99  500.9 ms | server stats incl. warm-up: {'batches': 133, 'mean_batch': 6.09, 'max_batch': 18}
800 reqs, 32 concurrent:    239 req/s  p50   67.7 ms  p99  579.7 ms | server stats incl. warm-up: {'batches': 267, 'mean_batch': 6.07, 'max_batch': 28}
== failures
good/bad/good in one batch -> [200, 422, 200]
client timed out (cancelled) ok
still serving -> 200
```
How to read it honestly: the model itself gains about 9.6x from batching, but end to end the gain is small (about 240 to 280 req/s), most likely because JSON parsing of 512 floats in one Python process and the single-process load client dominate (I did not profile it). Waiting 20 ms made batches bigger (mean about 6) and p50 worse here than waiting 5 ms. The runs are noisy; I would not draw a conclusion about the best setting from them. The servers were stopped afterwards. Triton and BentoML adaptive batching were not run.

**Follow-ups:**
- *How do I choose max_wait?* Start from the latency budget: wait should be a small slice of it (a fraction of p99 target), then measure with realistic traffic.
- *Does batching help on CPU?* Yes for dense models, as the direct benchmark shows, but check that your bottleneck is the model and not serialization.
- *Variable-length inputs (text)?* Pad to the longest in the batch, or bucket by length; padding wastes compute.

**Common mistakes:**
- Setting a large wait on a low-traffic service and adding latency for nothing.
- Running the model on the event loop inside the batcher.
- Not bounding the queue.
- Letting one bad row take down the batch.
- Forgetting that results must go back to the right caller.

---

### Q8 ⭐⭐⭐ 🟡 Input validation and error handling in a model API. Explain what pydantic can enforce (types, ranges, lengths, enums, custom validators for impossible values such as age -5 or NaN), 422 versus 400 versus 404 versus 429 versus 500 versus 503, why NaN and infinity must be rejected explicitly, consistent error bodies with an error code and a request id, custom exception handlers, never returning stack traces, a fallback prediction versus failing loudly, and request size limits. Show a FastAPI app with a validator that rejects NaN and out-of-range values, a handler for a model exception that returns 503 with a request id, and pytest cases for each. Run them for real with TestClient.
**Asked at:** FastAPI docs and tutorials (fastapi.tiangolo.com advanced events/lifespan page, reintech.io 'FastAPI ML model serving production REST APIs', docs.truefoundry.com deploy-model-fastapi; search snippets only, not opened); docs and tutorials, not interview reports; ML engineer and MLOps roles that ship model APIs, including IT-services firms, product companies and GCCs
**Say this first (1 line):** I make the schema strict with pydantic (types, ranges, enums, finite numbers), return one consistent error body with a request id, map model failures to 503, and never leak a stack trace.

**Then explain:**
- What pydantic can enforce: types, `gt/ge/le`, lengths, regex or enums, `extra="forbid"`, and custom validators for business rules (here: petal width cannot exceed petal length, age cannot be negative).
- NaN and infinity: JSON from Python can carry the tokens `NaN` and `Infinity`, and a float field accepts them by default. A model will happily score NaN and return garbage, so set `allow_inf_nan=False` (pydantic reports `finite_number`).
- Status codes: 422 schema or value invalid (FastAPI default); 400 for a request the server cannot parse or a semantic rule you want to call 400; 404 unknown route or model; 413 payload too large; 429 rate limited; 500 your bug; 503 model or dependency temporarily unavailable, retry. Pick one convention and document it.
- One error shape: `{"error": {"code", "message", "request_id", "details"}}`. The request id also goes in a response header and your logs, so support can find the trace. The real exception is logged server side only.
- Fallback vs fail loudly: a fallback (default score, cached score) is fine for low-risk ranking if you label it in the response and count it in metrics; for credit or safety decisions fail loudly with 503.
- Size limit: reject by `Content-Length` early (done here) and also set the limit at the proxy or server, because a chunked body has no length header.

**Example:** age_days = -5 gives 422 with `field: age_days, problem: greater_than_equal`. A body with `"sepal_len": NaN` gives 422 `finite_number`. A model that raises "secret internal path ... corrupted" gives 503 with the caller's `x-request-id` echoed and none of the internal text.

**Code:**
```python
# ===== q08/app.py =====
import os, uuid
from contextlib import asynccontextmanager
from typing import Annotated
import numpy as np, onnxruntime as ort
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator

MAX_BODY = 2_000          # bytes; a 4-number request is far below this
Cm = Annotated[float, Field(allow_inf_nan=False, gt=0, le=20)]     # petal/sepal sizes in cm

class Flower(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sepal_len: Cm
    sepal_wid: Cm
    petal_len: Cm
    petal_wid: Cm
    region: str = Field(pattern="^(north|south|east|west)$")
    age_days: int = Field(ge=0, le=3650)                            # age -5 -> 422

    @field_validator("petal_wid")
    @classmethod
    def petal_not_wider_than_long(cls, v, info):
        if "petal_len" in info.data and v > info.data["petal_len"]:
            raise ValueError("petal_wid cannot exceed petal_len")
        return v

class ModelUnavailable(Exception):
    pass

def err(status, code, message, rid, extra=None):
    body = {"error": {"code": code, "message": message, "request_id": rid}}
    if extra: body["error"]["details"] = extra
    return JSONResponse(body, status_code=status, headers={"x-request-id": rid})

@asynccontextmanager
async def lifespan(app):
    app.state.session = ort.InferenceSession(os.environ["MODEL_PATH"], providers=["CPUExecutionProvider"])
    yield

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def request_id_and_size(request: Request, call_next):
    rid = request.headers.get("x-request-id") or uuid.uuid4().hex[:12]
    request.state.rid = rid
    if int(request.headers.get("content-length", 0)) > MAX_BODY:
        return err(413, "payload_too_large", f"body over {MAX_BODY} bytes", rid)
    try:
        resp = await call_next(request)
    except Exception:                                  # last resort: no stack trace to the client
        return err(500, "internal_error", "unexpected error", rid)
    resp.headers["x-request-id"] = rid
    return resp

@app.exception_handler(RequestValidationError)
async def on_422(request: Request, exc: RequestValidationError):
    details = [{"field": ".".join(str(p) for p in e["loc"][1:]), "problem": e["type"]} for e in exc.errors()]
    return err(422, "invalid_input", "request failed validation", request.state.rid, details)

@app.exception_handler(ModelUnavailable)
async def on_model(request: Request, exc: ModelUnavailable):
    return err(503, "model_unavailable", "model could not score this request, retry later", request.state.rid)

@app.post("/v1/predict")
def predict(f: Flower, request: Request):
    x = np.asarray([[f.sepal_len, f.sepal_wid, f.petal_len, f.petal_wid]], dtype=np.float32)
    try:
        label, _ = request.app.state.session.run(None, {"X": x})
    except Exception as e:
        raise ModelUnavailable() from e                # real cause goes to logs, not to the client
    return {"label": int(label[0]), "request_id": request.state.rid}

# ===== q08/test_errors.py =====
import os
os.environ.setdefault("MODEL_PATH", "/tmp/claude-0/b6_q1_12/models/iris_v1.onnx")
import pytest
from fastapi.testclient import TestClient
from app import app

GOOD = {"sepal_len": 6.7, "sepal_wid": 3.0, "petal_len": 5.2, "petal_wid": 2.3, "region": "north", "age_days": 10}

@pytest.fixture(scope="module")
def c():
    with TestClient(app, raise_server_exceptions=False) as client:
        yield client

def test_ok(c):
    r = c.post("/v1/predict", json=GOOD)
    print(r.status_code, r.json()); assert r.status_code == 200 and r.json()["label"] == 2

def test_negative_age(c):
    r = c.post("/v1/predict", json={**GOOD, "age_days": -5})
    print(r.status_code, r.json()); assert r.status_code == 422 and r.json()["error"]["details"][0]["field"] == "age_days"

def test_nan_literal_rejected(c):
    r = c.post("/v1/predict", content=b'{"sepal_len": NaN, "sepal_wid": 3, "petal_len": 5, "petal_wid": 2, "region": "north", "age_days": 1}',
               headers={"content-type": "application/json"})
    print(r.status_code, r.json()["error"]["details"]); assert r.status_code == 422

def test_infinity_rejected(c):
    r = c.post("/v1/predict", content=b'{"sepal_len": 1, "sepal_wid": 3, "petal_len": Infinity, "petal_wid": 2, "region": "north", "age_days": 1}',
               headers={"content-type": "application/json"})
    assert r.status_code == 422

def test_business_rule_validator(c):
    r = c.post("/v1/predict", json={**GOOD, "petal_wid": 9.0})
    print(r.status_code, r.json()["error"]["details"]); assert r.status_code == 422

def test_bad_enum_and_extra_field(c):
    assert c.post("/v1/predict", json={**GOOD, "region": "mars"}).status_code == 422
    assert c.post("/v1/predict", json={**GOOD, "colour": "red"}).status_code == 422

def test_too_large_413(c):
    r = c.post("/v1/predict", content=b"x" * 5000, headers={"content-type": "application/json"})
    print(r.status_code, r.json()); assert r.status_code == 413

def test_model_failure_503_with_request_id(c):
    class Boom:
        def run(self, *a, **k): raise RuntimeError("secret internal path /models/x.onnx corrupted")
    real = app.state.session; app.state.session = Boom()
    try:
        r = c.post("/v1/predict", json=GOOD, headers={"x-request-id": "req-abc-123"})
    finally:
        app.state.session = real
    print(r.status_code, r.json(), r.headers["x-request-id"])
    assert r.status_code == 503 and r.json()["error"]["request_id"] == "req-abc-123"
    assert "secret" not in r.text and "Traceback" not in r.text

def test_unknown_route_404(c):
    assert c.get("/v1/nope").status_code == 404
```
```bash
cd code && python -m pytest q08 -q -s
```

**Output (my run):** TestClient, fastapi 0.162.0, pydantic 2.14.1, nine tests (the 200 and 422 lines come from `-s` prints):
```
200 {'label': 2, 'request_id': '26b0907db5f4'}
422 {'error': {'code': 'invalid_input', 'message': 'request failed validation', 'request_id': 'e7c3d90ae9fb', 'details': [{'field': 'age_days', 'problem': 'greater_than_equal'}]}}
422 [{'field': 'sepal_len', 'problem': 'finite_number'}]
422 [{'field': 'petal_wid', 'problem': 'value_error'}]
413 {'error': {'code': 'payload_too_large', 'message': 'body over 2000 bytes', 'request_id': '9567b9be5ddf'}}
503 {'error': {'code': 'model_unavailable', 'message': 'model could not score this request, retry later', 'request_id': 'req-abc-123'}} req-abc-123
9 passed, 1 warning in 0.63s
```
Request ids that were generated differ on every run. No real server or rate limiter was run here (429 is only described).

**Follow-ups:**
- *Should I clip out-of-range values instead of rejecting?* Only if the business agrees, and log it; silent clipping hides upstream bugs.
- *Where does 429 come from?* Usually a gateway or middleware rate limiter; the API should return `Retry-After`.
- *Is the 413 check enough?* No, it is a first filter; enforce the real limit at the proxy as well.

**Common mistakes:**
- Letting NaN through.
- Returning `str(exception)` to the client.
- Using 200 with an error field.
- Using 500 for a bad input and paging someone at night.
- A silent fallback with no metric.

---

### Q9 ⭐⭐⭐ 🟡 Model formats for serving: pickle, joblib, ONNX, TorchScript, SavedModel and safetensors (weights only). For each give what is stored (Python object graph, a computation graph, weights only), portability across Python and library versions, speed, language support, and the security point that loading pickle or joblib (and torch.load of a pickled checkpoint) can run arbitrary code, so never load one from an untrusted source; compare skops, ONNX and safetensors as safer routes (check current docs for the exact scikit-learn and PyTorch guidance). Show a harmless demo where unpickling an object with a __reduce__ method runs a function (prints a line only), a joblib save and load round trip, and the ONNX alternative. Run it for real and show the output.
**Asked at:** Model format and safety sources (scikit-learn model persistence docs, arxiv.org 2410.04490 on Hugging Face model exploits, labs.snyk.io deep-learning file format vulnerabilities, union.ai secure-AI post, ProtectAI ModelScan docs; search snippets only, not opened); docs and security write-ups, not interview reports; ML engineer and MLOps roles, security-aware teams
**Say this first (1 line):** Pickle and joblib store Python objects and run code on load, so I never load them from an untrusted source; for serving I prefer ONNX (a graph), safetensors (weights only) or skops (checked loading), and I verify parity.

**Then explain:**
| Format | What is stored | Portable? | Safe to load untrusted? |
|---|---|---|---|
| pickle / joblib | Python object graph (class paths plus state) | Fragile: same Python and library versions | No, can run code |
| ONNX | Computation graph plus weights, operator set | Yes: many languages and runtimes | Mostly yes (a model file, not code), but custom ops and parser bugs exist; validate and scan |
| TorchScript | Serialized PyTorch graph/code | PyTorch runtime needed | Treat like pickle-family, check current docs |
| TF SavedModel | Graph, weights, signatures | TF ecosystem | Can contain ops with side effects; check current docs |
| safetensors | Tensors only (weights), no code | Yes, fast load | Yes, by design; but you still need the architecture code |
| skops | Scikit-learn objects with a type allow-list | Python only | Safer: unknown types need explicit trust |
- The attack: `pickle.loads` calls whatever `__reduce__` returns. A file from a model hub can run a shell command at load time. `torch.load` on a pickled checkpoint is the same risk; `weights_only=True` blocks arbitrary objects (check current PyTorch docs for defaults in your version).
- Speed and size: ONNX Runtime is usually fast to start and has no Python class dependency; joblib is quick for NumPy-heavy sklearn models but breaks across scikit-learn versions. Do not trust a number from me for your model; measure.
- Failure modes: pickle files that load on your laptop and fail in the container (version skew); trusting a "safe" format and skipping a hash check; ONNX models with custom operators that the serving runtime lacks.
- Defences: verify the source and a hash, load in a sandbox, scan (for example ModelScan), prefer weights-only formats, pin library versions.

**Example:** the demo's "attack" calls `print`, so it is harmless. A real payload would put `os.system` there. The tell: you can see the effect (a line printed) before you get a model object back.

**Code:**
```python
# ===== q09/formats_demo.py =====
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
```
```bash
cd code/q09 && python -I formats_demo.py
```

**Output (my run):** scikit-learn 1.9.1, skops 0.16.0, safetensors 0.8.0, torch 2.14.1, onnxruntime 1.31.0 (I installed skops and safetensors into the shared test venv for this). Warnings omitted.
```
1. before loads: nothing printed yet
!! code ran during pickle.loads (a real attacker would run os.system here)
2. joblib round trip same predictions: True | bytes: 931
3. skops untrusted types for our model: []
   skops load ok: True
   skops refuses unknown/untrusted object: UntrustedTypesFoundException
4. ONNX labels equal sklearn: True | bytes: 518
5. torch.load(weights_only=True) blocked the pickle: UnpicklingError
   safetensors round trip: True
```
Byte sizes are for this tiny iris model only. Temporary files were deleted by the script.

**Follow-ups:**
- *Is ONNX 100 percent safe?* No. It carries no Python, so the code-execution-on-load class is gone, but parsers have bugs and custom operator libraries can be native code; treat unknown models with care.
- *How do I ship an sklearn model safely inside my own pipeline?* Same-team, pinned versions, hash checked, loaded from your registry; that is a trusted source. For third parties use skops or ONNX.
- *What do Hugging Face models use?* Many use safetensors now, but pickled `.bin` files still exist; check the file type before loading.

**Common mistakes:**
- `pickle.load` on a file from a download link.
- Assuming "it is just a model, not code".
- Skipping version pins, then getting silent behaviour change across scikit-learn versions.
- Skipping the parity check after converting.

---

### Q10 ⭐⭐⭐ 🟡 Export a model to ONNX and run it with ONNX Runtime. Explain what ONNX is (a graph format plus operator sets, opset version), converting a scikit-learn pipeline with skl2onnx and a PyTorch module with torch.onnx.export (dynamic axes for the batch dimension), ONNX Runtime sessions and execution providers (CPU, CUDA, TensorRT at concept), and why you always check parity between the original and ONNX outputs on real rows. Include what breaks: unsupported operators, opset mismatches, custom Python preprocessing that is not in the graph, and float32 versus float64. Run a scikit-learn export with a parity check and a small PyTorch module export with a dynamic batch axis, and show the real results.
**Asked at:** Model format and safety sources (scikit-learn model persistence docs, arxiv.org 2410.04490 on Hugging Face model exploits, labs.snyk.io deep-learning file format vulnerabilities, union.ai secure-AI post, ProtectAI ModelScan docs; search snippets only, not opened); docs and security write-ups, not interview reports; ML engineer and MLOps roles, security-aware teams
**Say this first (1 line):** I export to ONNX so serving does not need the training stack, then I always compare ONNX Runtime outputs against the original on real rows before I ship.

**Then explain:**
- ONNX is a graph of operators plus weights. The opset version (here 17) decides which operator definitions you get; the runtime must support the opset you export.
- scikit-learn: `skl2onnx.to_onnx(model, X[:1], target_opset=17, options={id(model): {"zipmap": False}})`. `zipmap=False` returns probabilities as an array, not a list of dicts. Pipelines convert as a unit (the scaler is inside the graph).
- PyTorch: `torch.onnx.export` with `dynamic_axes` (legacy exporter) or `dynamic_shapes` (the newer default exporter, which needs the `onnxscript` package in my test) so the batch size is not frozen to the example input.
- ONNX Runtime session: pick execution providers in order, for example `["CUDAExecutionProvider", "CPUExecutionProvider"]` on a GPU box, or TensorRT at concept level. Here only CPU (and an Azure provider entry) was available. Check current docs for the provider names and builds.
- What breaks: an unsupported operator or custom Python in preprocessing (a `FunctionTransformer(lambda ...)` does not convert); opset mismatch between exporter and runtime; float64 data fed to a float32 graph; dynamic control flow baked in by tracing; tokenisation or feature code that lives outside the graph and drifts from training.
- Parity: compare labels exactly and probabilities within a tolerance (1e-5 is typical for float32; choose yours), on real rows plus edge cases, and also test batch sizes 1 and more than 1.

**Example:** a StandardScaler + LogisticRegression pipeline on the 150 iris rows: all 150 labels equal sklearn, and the biggest probability difference is about 1.5e-07. A float64 array fed to the graph fails with a clear data type error.

**Code:**
```python
# ===== q10/export_demo.py =====
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
```
```bash
cd code/q10 && python -I export_demo.py
```

**Output (my run):** warnings removed; the tracebacks are shortened to their message.
```
onnx 1.23.2 | onnxruntime 1.31.0 | providers: ['AzureExecutionProvider', 'CPUExecutionProvider']
A. opset: [('ai.onnx.ml', 1), ('ai.onnx', 17), ('ai.onnx', 17)]
A. labels equal: True | max |proba diff|: 1.4901161193847656e-07
B. float64 into float32 graph: InvalidArgument - ror] : 2 : INVALID_ARGUMENT : Unexpected input data type. Actual: (tensor(double)) , expected: (tensor(float))
C. FunctionTransformer(lambda): RuntimeError - FunctionTransformer is not supported unless the transform function is None (= identity). You may rai
D. legacy exporter (dynamo=False): batch 1 -> out shape (1, 3), max diff vs torch 7.5e-09
D. legacy exporter (dynamo=False): batch 7 -> out shape (7, 3), max diff vs torch 1.5e-08
D. legacy exporter (dynamo=False): declared input shape ['batch', 4]
D. default exporter: batch 1 -> out shape (1, 3), max diff vs torch 3.0e-08
D. default exporter: batch 7 -> out shape (7, 3), max diff vs torch 3.0e-08
D. default exporter: declared input shape ['batch', 4]
```
Torch 2.14.1, onnxscript 0.7.2, scikit-learn 1.9.1, skl2onnx 1.20.0 (the legacy exporter prints a deprecation warning, which I removed). CUDA and TensorRT providers were not executed (no GPU). The first attempt with the default exporter failed because I used the wrong argument name in `dynamic_shapes`; the code shown is the fixed version.

**Follow-ups:**
- *Why not just ship pickle?* Version skew and the security risk (Q9), plus ONNX can run without Python.
- *Does ONNX make it faster?* Often, but not always; measure on your model and hardware.
- *What about quantisation?* `onnxruntime.quantization` can shrink and speed up some models, but you must re-check accuracy; not run here.

**Common mistakes:**
- Exporting with a fixed batch size of 1.
- Checking parity on one row.
- Leaving preprocessing in Python and forgetting to ship it.
- Mixing float32 and float64.

---

### Q11 ⭐⭐⭐ 🟡 REST versus gRPC for model inference. Compare payload encoding (JSON text versus protobuf binary), HTTP/1.1 versus HTTP/2 multiplexing and streaming, schema and code generation, browser and curl friendliness, load balancer and gateway support, debugging, and how much the protocol matters next to model time and payload size (a 2 ms model behind a 20 ms network hop). Explain that Triton, TorchServe and TensorFlow Serving expose both, the KServe v2 / Open Inference Protocol shape at concept level, and the common pattern of REST at the edge and gRPC between internal services. Show a JSON request and the equivalent proto message definition, measure JSON size versus a packed float32 buffer for a 224x224x3 image tensor with Python, and say what was not run (no gRPC server). Do not quote vendor benchmark numbers.
**Asked at:** Protocol and framework comparisons (aws.amazon.com ML blog on gRPC with TensorFlow Serving on SageMaker, itea4.org inference scaling summary, aiwiki.ai serving page, smartdev.com REST versus gRPC page whose numbers are placeholders; search snippets only, not opened); weak-to-medium sources, treat numbers as unverified; serving and platform roles
**Say this first (1 line):** REST with JSON is easy to debug and works everywhere; gRPC with protobuf is compact, typed and streams over HTTP/2; the protocol matters mainly for big tensors and chatty internal calls, and I measure before I switch.

**Then explain:**
| Point | REST + JSON | gRPC + protobuf |
|---|---|---|
| Encoding | Text; floats become decimal strings | Binary; packed float32 is 4 bytes per value |
| Transport | HTTP/1.1 or 2 | HTTP/2 only: multiplexing, streaming |
| Schema | Optional (OpenAPI) | Mandatory `.proto`, generated clients |
| Debugging | curl, browser, easy logs | Needs grpcurl or tooling |
| Gateways / browsers | Universal | Needs gRPC-aware proxy; browsers need gRPC-web |
- Triton, TorchServe and TensorFlow Serving expose both REST and gRPC (check each tool's current docs for ports and details). KServe v2 / Open Inference Protocol defines the same inference shape over both: a request with named `inputs`, each with `name`, `shape`, `datatype` and `data`, and matching `outputs`.
- Common pattern: REST at the edge (clients, partners, browsers), gRPC between internal services, or REST everywhere until a measurement says otherwise.
- Perspective: a 2 ms model behind a 20 ms network hop is dominated by the network; switching protocol will not fix that, but cutting a 3 MB JSON body might. Payload size and serialization CPU matter most for images and large embeddings.
- Failure modes: long-lived gRPC connections pin to one pod behind an L4 load balancer (balance per request with an L7 proxy or client-side balancing); proxies that drop HTTP/2; schema changes that reuse field numbers.

**Example:** a 224x224x3 float image has 150,528 values. As packed float32 that is 150,528 x 4 = 602,112 bytes. As a JSON list of Python floats it is about 3 MB (about 20 bytes per value). So JSON is about 5 times bigger. A cheaper REST option is base64 of the raw buffer, about 1.33 times the packed size.

**Code:**
```python
# ===== q11/sizes.py =====
import base64, json
import numpy as np
rng = np.random.default_rng(0)
img = rng.random((1, 3, 224, 224), dtype=np.float32)            # normalised pixels in [0, 1)
n = img.size
raw = img.tobytes()
json_nested = json.dumps({"inputs": [{"name": "x", "shape": list(img.shape), "datatype": "FP32",
                                       "data": img.reshape(-1).tolist()}]})   # KServe v2 REST style (shape of the idea)
json_b64 = json.dumps({"shape": list(img.shape), "datatype": "FP32", "b64": base64.b64encode(raw).decode()})
print(f"elements: {n}")
print(f"packed float32 buffer (what a protobuf bytes field carries): {len(raw):>9,} bytes  ({len(raw)/n:.1f} B/element)")
print(f"JSON list of floats (python repr, float64 text)           : {len(json_nested):>9,} bytes  ({len(json_nested)/n:.1f} B/element)")
print(f"JSON with base64 of the float32 buffer                    : {len(json_b64):>9,} bytes  ({len(json_b64)/n:.1f} B/element)")
print(f"ratio JSON-list / packed: {len(json_nested)/len(raw):.2f}x ; base64 / packed: {len(json_b64)/len(raw):.2f}x")
small = np.float32([0.5, 0.25]).tobytes(); print("2 floats packed:", len(small), "bytes -> JSON '[0.5, 0.25]':", len(json.dumps([0.5, 0.25])), "bytes")
print("sample of the JSON body:", json_nested[:110], "...")

# ===== q11/check_proto.py =====
# usage: python -m grpc_tools.protoc -I. --python_out=OUT infer.proto ; python -I check_proto.py OUT
import sys; sys.path.insert(0, sys.argv[1])
import numpy as np, infer_pb2
x = np.zeros((1, 3, 224, 224), np.float32)
m = infer_pb2.InferRequest(model_name="resnet", model_version="3", shape=list(x.shape), datatype="FP32", raw_data=x.tobytes())
b = m.SerializeToString()
print("serialized InferRequest bytes:", len(b), "= raw", len(x.tobytes()), "+ overhead", len(b) - len(x.tobytes()))
print("round trip shape:", list(infer_pb2.InferRequest.FromString(b).shape))
```
```protobuf
// ===== q11/infer.proto =====
syntax = "proto3";
package demo.v1;

message InferRequest {
  string model_name = 1;
  string model_version = 2;
  repeated int64 shape = 3;          // [1, 3, 224, 224]
  string datatype = 4;               // "FP32"
  bytes raw_data = 5;                // packed little-endian float32, no text
}
message InferResponse {
  string model_name = 1;
  string model_version = 2;
  repeated float scores = 3 [packed = true];
}
service Inference {
  rpc Infer (InferRequest) returns (InferResponse);
}
```
```json
{"inputs": [{"name": "x", "shape": [1, 3, 224, 224], "datatype": "FP32", "data": [0.85, 0.63, "..."]}]}
```
```bash
cd code/q11
python -I sizes.py
OUT=/tmp/claude-0/b6_q1_12/proto && mkdir -p $OUT
python -m grpc_tools.protoc -I. --python_out=$OUT infer.proto     # pip install grpcio-tools
python -I check_proto.py $OUT
```

**Output (my run):** the size numbers are exact byte counts for this random float32 tensor (no timing involved).
```
elements: 150528
packed float32 buffer (what a protobuf bytes field carries):   602,112 bytes  (4.0 B/element)
JSON list of floats (python repr, float64 text)           :  3,050,958 bytes  (20.3 B/element)
JSON with base64 of the float32 buffer                    :   802,874 bytes  (5.3 B/element)
ratio JSON-list / packed: 5.07x ; base64 / packed: 1.33x
2 floats packed: 8 bytes -> JSON '[0.5, 0.25]': 11 bytes
sample of the JSON body: {"inputs": [{"name": "x", "shape": [1, 3, 224, 224], "datatype": "FP32", "data": [0.8506242036819458, 0.636961 ...
serialized InferRequest bytes: 602141 = raw 602112 + overhead 29
round trip shape: [1, 3, 224, 224]
```
`protoc` compiled the `.proto` (compile check passed), and the protobuf message round trip ran. NOT executed: any gRPC server or client, so no gRPC-versus-REST timing is claimed.

**Follow-ups:**
- *Is gRPC always lower latency?* Often yes for large payloads and many calls, but it depends on payload and network; I would measure with my own model rather than quote a vendor number.
- *Can I stream?* gRPC supports server and bidirectional streaming; REST can use server-sent events or chunked responses.
- *Which for a public API?* REST, for tooling and browser support.

**Common mistakes:**
- Switching protocol before profiling.
- Sending images as JSON float lists.
- Ignoring load balancing behaviour of long-lived gRPC connections.
- Reusing or renumbering protobuf field numbers.

---

### Q12 ⭐⭐⭐ 🟡 Model versioning and versioned APIs. Explain URL versions (/v1/predict) versus a header, the difference between the API contract version and the model version, returning model_version and a request id in every response, serving two model versions side by side, backward-compatible changes (add optional fields) versus breaking ones, deprecation with a sunset period, and tying the served version to the registry entry and the git SHA (Part 4 owns the registry; Part 7 owns promotion). Show a FastAPI app with /v1 and /v2 routers that load different ONNX models, a response that carries model_version, and a pytest that checks the v1 schema did not change. Run it with TestClient.
**Asked at:** FastAPI docs and tutorials (fastapi.tiangolo.com advanced events/lifespan page, reintech.io 'FastAPI ML model serving production REST APIs', docs.truefoundry.com deploy-model-fastapi; search snippets only, not opened); docs and tutorials, not interview reports; ML engineer and MLOps roles that ship model APIs, including IT-services firms, product companies and GCCs
**Say this first (1 line):** I version the API contract in the URL (`/v1`, `/v2`) and report the model version separately in every response, so I can swap models without breaking clients and break the contract only on purpose.

**Then explain:**
- Two versions, two meanings: the API contract version (fields, types, status codes) changes rarely; the model version (weights, features) changes often. A new model behind `/v1` is fine as long as the response shape and meaning hold.
- URL vs header: a path version is visible, cacheable, easy to route and log. A header version keeps URLs clean but hides the version from logs and curl. Either works; be consistent.
- Every response carries `model_version` and `request_id`. The model version string should tie to the registry entry (name and version, Part 4) and the git SHA of the serving build; promotion rules are Part 7.
- Two versions side by side: separate routers, separate sessions in `app.state`, or separate deployments behind a gateway. Side by side doubles memory, so watch the pod size.
- Backward compatible: add optional response fields, add optional request fields with defaults. Breaking: remove or rename a field, change a type or unit, tighten validation, change what a label means.
- Deprecation: announce, add `Deprecation` and `Sunset` response headers (the Sunset date is a policy decision; the date here is an example), watch traffic on the old version, remove after the sunset.
- Failure modes: a "small" model upgrade that changes the score range under the same `/v1`; clients that parse by position; losing the mapping from a prediction in a log to the model that made it.

**Example:** `/v1/predict` returns `{label, model_version, request_id}`. `/v2/predict` returns the same three plus `name` and `probabilities`, so a v1 client could read v2 responses too. The test fails the build if anyone removes or renames a v1 field.

**Code:**
```python
# ===== q12/app.py =====
import os, uuid
from contextlib import asynccontextmanager
import numpy as np, onnxruntime as ort
from fastapi import APIRouter, FastAPI, Request, Response
from pydantic import BaseModel, ConfigDict, Field

LABELS = ["setosa", "versicolor", "virginica"]
GIT_SHA = os.environ.get("GIT_SHA", "dev")

class PredictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    features: list[float] = Field(min_length=4, max_length=4)

# ---- v1 contract: FROZEN. Never remove or rename these fields.
class PredictResponseV1(BaseModel):
    label: int
    model_version: str
    request_id: str

# ---- v2 contract: v1 fields + a new field (additive), and the v2 model behind it
class PredictResponseV2(PredictResponseV1):
    name: str
    probabilities: list[float]

def run(session, features):
    x = np.asarray([features], dtype=np.float32)
    label, probs = session.run(None, {"X": x})
    return int(label[0]), [round(float(p), 4) for p in probs[0]]

v1, v2 = APIRouter(prefix="/v1"), APIRouter(prefix="/v2")

@v1.post("/predict", response_model=PredictResponseV1)
def predict_v1(req: PredictRequest, request: Request, response: Response):
    response.headers["Deprecation"] = "true"                       # tell clients early
    response.headers["Sunset"] = "Wed, 31 Dec 2026 23:59:59 GMT"   # example date, set by your policy
    label, _ = run(request.app.state.models["v1"], req.features)
    return PredictResponseV1(label=label, model_version=request.app.state.versions["v1"], request_id=uuid.uuid4().hex[:12])

@v2.post("/predict", response_model=PredictResponseV2)
def predict_v2(req: PredictRequest, request: Request):
    label, probs = run(request.app.state.models["v2"], req.features)
    return PredictResponseV2(label=label, name=LABELS[label], probabilities=probs,
                             model_version=request.app.state.versions["v2"], request_id=uuid.uuid4().hex[:12])

@asynccontextmanager
async def lifespan(app):
    cpu = ["CPUExecutionProvider"]
    app.state.models = {"v1": ort.InferenceSession(os.environ["MODEL_V1"], providers=cpu),
                        "v2": ort.InferenceSession(os.environ["MODEL_V2"], providers=cpu)}
    # in real life these come from the registry entry (name + version) and the build's git SHA
    app.state.versions = {"v1": f"iris-logreg:1+{GIT_SHA}", "v2": f"iris-rf:3+{GIT_SHA}"}
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(v1)
app.include_router(v2)

@app.get("/versions")
def versions(request: Request):
    return request.app.state.versions

# ===== q12/test_versions.py =====
import os
M = "/tmp/claude-0/b6_q1_12/models/"
os.environ.setdefault("MODEL_V1", M + "iris_v1.onnx"); os.environ.setdefault("MODEL_V2", M + "iris_v2.onnx")
os.environ.setdefault("GIT_SHA", "abc1234")
import pytest
from fastapi.testclient import TestClient
from app import app

X = {"features": [6.7, 3.0, 5.2, 2.3]}

@pytest.fixture(scope="module")
def c():
    with TestClient(app) as client:
        yield client

def test_v1_schema_frozen(c):
    r = c.post("/v1/predict", json=X)
    print("v1:", r.status_code, r.json(), {k: v for k, v in r.headers.items() if k in ("deprecation", "sunset")})
    assert set(r.json()) == {"label", "model_version", "request_id"}        # the contract: exactly these keys
    assert r.headers["deprecation"] == "true" and "sunset" in r.headers

def test_v1_openapi_fields_frozen(c):
    props = c.get("/openapi.json").json()["components"]["schemas"]["PredictResponseV1"]["properties"]
    assert sorted(props) == ["label", "model_version", "request_id"]

def test_v2_is_additive_superset_of_v1(c):
    r1, r2 = c.post("/v1/predict", json=X).json(), c.post("/v2/predict", json=X).json()
    print("v2:", r2)
    assert set(r1) <= set(r2) and {"name", "probabilities"} <= set(r2)
    assert r1["model_version"] != r2["model_version"] and r2["model_version"].endswith("abc1234")

def test_request_schema_same_on_both(c):
    assert c.post("/v1/predict", json={"features": [1, 2, 3]}).status_code == 422
    assert c.post("/v2/predict", json={"features": [1, 2, 3]}).status_code == 422

def test_versions_endpoint(c):
    print("/versions:", c.get("/versions").json())
    assert set(c.get("/versions").json()) == {"v1", "v2"}
```
```bash
cd code && python -m pytest q12 -q -s
```

**Output (my run):** TestClient with two ONNX models (logistic regression as v1, random forest as v2) and `GIT_SHA=abc1234` set by the test; request ids vary per run.
```
v1: 200 {'label': 2, 'model_version': 'iris-logreg:1+abc1234', 'request_id': '53740c0f527e'} {'deprecation': 'true', 'sunset': 'Wed, 31 Dec 2026 23:59:59 GMT'}
v2: {'label': 2, 'model_version': 'iris-rf:3+abc1234', 'request_id': '72b0c153e6c8', 'name': 'virginica', 'probabilities': [0.0, 0.05, 0.95]}
/versions: {'v1': 'iris-logreg:1+abc1234', 'v2': 'iris-rf:3+abc1234'}
5 passed, 1 warning in 0.46s
```
The registry names `iris-logreg:1` and `iris-rf:3` are made up for the demo; no registry was used.

**Follow-ups:**
- *How do I roll out a new model without a new URL version?* Keep the contract, change `model_version`, and use shadow or canary routing (Part 7 and later parts).
- *When must I bump to v2?* When the contract breaks, not when the model changes.
- *How long to support v1?* As long as your policy and the traffic say; measure remaining callers per version.

**Common mistakes:**
- Putting the model version in the URL and forcing every client to migrate on each retrain.
- No `model_version` in responses, so incidents cannot be traced.
- "Improving" a v1 response in place.
- Having no test that locks the v1 schema.

---
