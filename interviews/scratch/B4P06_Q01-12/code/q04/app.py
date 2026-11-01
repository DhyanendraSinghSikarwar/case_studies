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
