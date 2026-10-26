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
