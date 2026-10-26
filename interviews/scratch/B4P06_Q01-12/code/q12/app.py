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
