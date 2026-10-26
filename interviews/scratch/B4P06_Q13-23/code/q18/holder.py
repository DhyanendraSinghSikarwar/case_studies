import threading, time
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

class Model:
    """Loading is slow and happens in steps. A reader must never see it half done."""
    def __init__(self, version: str, load_secs: float = 0.0):
        self.version = None; self.weights = None
        self.version = version
        time.sleep(load_secs)                     # a window where the object is half built
        self.weights = f"weights-of-{version}"
    def predict(self, x: float):
        assert self.version is not None and self.weights == f"weights-of-{self.version}", "half-loaded model seen!"
        return {"version": self.version, "y": x * (2 if self.version == "v1" else 3)}

class Holder:
    def __init__(self): self._m = None; self._reload_lock = threading.Lock()
    def get(self): return self._m                 # a plain attribute read: atomic in CPython
    def reload(self, version, load_secs=0.0):
        with self._reload_lock:                   # one reload at a time
            new = Model(version, load_secs)       # build fully BESIDE the old one
            self._m = new                         # then swap one reference

holder = Holder()
@asynccontextmanager
async def lifespan(app):
    holder.reload("v1"); yield
app = FastAPI(lifespan=lifespan)

@app.get("/readyz")
def readyz():
    if holder.get() is None: raise HTTPException(503, "loading")
    return {"ready": True, "version": holder.get().version}
@app.post("/predict")
def predict(x: float):
    m = holder.get()                              # take ONE reference, use it for the whole request
    if m is None: raise HTTPException(503, "loading")
    return m.predict(x)
@app.post("/admin/reload")
def admin_reload(version: str, load_secs: float = 0.0):
    holder.reload(version, load_secs); return {"now": version}
