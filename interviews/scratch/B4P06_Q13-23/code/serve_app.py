# serve_app.py : small FastAPI service around the iris ONNX model (used by Q15 and Q16). MODEL_PATH env var.
import os
from contextlib import asynccontextmanager
import numpy as np, onnxruntime as ort
from fastapi import FastAPI, Response
from pydantic import BaseModel, Field

state = {}
@asynccontextmanager
async def lifespan(app):
    state["s"] = ort.InferenceSession(os.environ["MODEL_PATH"], providers=["CPUExecutionProvider"])
    yield
    state.clear()
app = FastAPI(lifespan=lifespan)

class Req(BaseModel):
    features: list[float] = Field(min_length=4, max_length=4)

@app.get("/readyz")
def readyz(r: Response):
    if "s" not in state:
        r.status_code = 503; return {"status": "loading"}
    return {"status": "ready"}

@app.post("/v1/predict")
def predict(req: Req):
    x = np.array([req.features], dtype=np.float32)
    return {"label": int(state["s"].run(["label"], {"X": x})[0][0])}
