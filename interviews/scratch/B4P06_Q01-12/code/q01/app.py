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
