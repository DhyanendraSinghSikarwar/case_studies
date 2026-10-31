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
