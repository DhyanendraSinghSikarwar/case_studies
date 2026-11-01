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
