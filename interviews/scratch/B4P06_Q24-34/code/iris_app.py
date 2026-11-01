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
