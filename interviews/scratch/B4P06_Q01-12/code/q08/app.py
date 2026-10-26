import os, uuid
from contextlib import asynccontextmanager
from typing import Annotated
import numpy as np, onnxruntime as ort
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator

MAX_BODY = 2_000          # bytes; a 4-number request is far below this
Cm = Annotated[float, Field(allow_inf_nan=False, gt=0, le=20)]     # petal/sepal sizes in cm

class Flower(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sepal_len: Cm
    sepal_wid: Cm
    petal_len: Cm
    petal_wid: Cm
    region: str = Field(pattern="^(north|south|east|west)$")
    age_days: int = Field(ge=0, le=3650)                            # age -5 -> 422

    @field_validator("petal_wid")
    @classmethod
    def petal_not_wider_than_long(cls, v, info):
        if "petal_len" in info.data and v > info.data["petal_len"]:
            raise ValueError("petal_wid cannot exceed petal_len")
        return v

class ModelUnavailable(Exception):
    pass

def err(status, code, message, rid, extra=None):
    body = {"error": {"code": code, "message": message, "request_id": rid}}
    if extra: body["error"]["details"] = extra
    return JSONResponse(body, status_code=status, headers={"x-request-id": rid})

@asynccontextmanager
async def lifespan(app):
    app.state.session = ort.InferenceSession(os.environ["MODEL_PATH"], providers=["CPUExecutionProvider"])
    yield

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def request_id_and_size(request: Request, call_next):
    rid = request.headers.get("x-request-id") or uuid.uuid4().hex[:12]
    request.state.rid = rid
    if int(request.headers.get("content-length", 0)) > MAX_BODY:
        return err(413, "payload_too_large", f"body over {MAX_BODY} bytes", rid)
    try:
        resp = await call_next(request)
    except Exception:                                  # last resort: no stack trace to the client
        return err(500, "internal_error", "unexpected error", rid)
    resp.headers["x-request-id"] = rid
    return resp

@app.exception_handler(RequestValidationError)
async def on_422(request: Request, exc: RequestValidationError):
    details = [{"field": ".".join(str(p) for p in e["loc"][1:]), "problem": e["type"]} for e in exc.errors()]
    return err(422, "invalid_input", "request failed validation", request.state.rid, details)

@app.exception_handler(ModelUnavailable)
async def on_model(request: Request, exc: ModelUnavailable):
    return err(503, "model_unavailable", "model could not score this request, retry later", request.state.rid)

@app.post("/v1/predict")
def predict(f: Flower, request: Request):
    x = np.asarray([[f.sepal_len, f.sepal_wid, f.petal_len, f.petal_wid]], dtype=np.float32)
    try:
        label, _ = request.app.state.session.run(None, {"X": x})
    except Exception as e:
        raise ModelUnavailable() from e                # real cause goes to logs, not to the client
    return {"label": int(label[0]), "request_id": request.state.rid}
