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
