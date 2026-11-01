# A tiny FastAPI MOCK of the KServe v2 / Open Inference Protocol HTTP routes for the iris ONNX model. Not Triton.
import os, numpy as np, onnxruntime as ort
from contextlib import asynccontextmanager
import json
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
S = {}
@asynccontextmanager
async def lifespan(app):
    S["s"] = ort.InferenceSession(os.environ["MODEL_PATH"], providers=["CPUExecutionProvider"]); yield
app = FastAPI(lifespan=lifespan)
@app.get("/v2/health/live")
def live(): return Response(status_code=200)
@app.get("/v2/health/ready")
def ready(): return Response(status_code=200 if "s" in S else 503)
@app.get("/v2/models/iris_onnx/ready")
def mready(): return Response(status_code=200)
@app.get("/v2/models/iris_onnx")
def meta():
    return {"name": "iris_onnx", "versions": ["1"], "platform": "mock",
            "inputs": [{"name": "X", "datatype": "FP32", "shape": [-1, 4]}],
            "outputs": [{"name": "label", "datatype": "INT64", "shape": [-1]},
                        {"name": "probabilities", "datatype": "FP32", "shape": [-1, 3]}]}
@app.post("/v2/models/iris_onnx/infer")
async def infer(request: Request):
    body = json.loads(await request.body())          # the client sends no JSON content-type, so parse the raw body
    t = body["inputs"][0]
    if t["datatype"] != "FP32" or len(t["shape"]) != 2 or t["shape"][1] != 4:
        return JSONResponse({"error": f"unexpected input: datatype {t['datatype']} shape {t['shape']}, want FP32 [N,4]"}, 400)
    x = np.array(t["data"], dtype=np.float32).reshape(t["shape"])      # JSON data is a flat row-major list
    label, prob = S["s"].run(None, {"X": x})
    return {"model_name": "iris_onnx", "model_version": "1", "id": body.get("id", ""),
            "outputs": [{"name": "label", "datatype": "INT64", "shape": [len(label)], "data": label.tolist()},
                        {"name": "probabilities", "datatype": "FP32", "shape": list(prob.shape), "data": prob.astype(float).flatten().round(4).tolist()}]}
