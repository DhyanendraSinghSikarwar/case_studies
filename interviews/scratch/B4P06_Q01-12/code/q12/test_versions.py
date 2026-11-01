import os
M = "/tmp/claude-0/b6_q1_12/models/"
os.environ.setdefault("MODEL_V1", M + "iris_v1.onnx"); os.environ.setdefault("MODEL_V2", M + "iris_v2.onnx")
os.environ.setdefault("GIT_SHA", "abc1234")
import pytest
from fastapi.testclient import TestClient
from app import app

X = {"features": [6.7, 3.0, 5.2, 2.3]}

@pytest.fixture(scope="module")
def c():
    with TestClient(app) as client:
        yield client

def test_v1_schema_frozen(c):
    r = c.post("/v1/predict", json=X)
    print("v1:", r.status_code, r.json(), {k: v for k, v in r.headers.items() if k in ("deprecation", "sunset")})
    assert set(r.json()) == {"label", "model_version", "request_id"}        # the contract: exactly these keys
    assert r.headers["deprecation"] == "true" and "sunset" in r.headers

def test_v1_openapi_fields_frozen(c):
    props = c.get("/openapi.json").json()["components"]["schemas"]["PredictResponseV1"]["properties"]
    assert sorted(props) == ["label", "model_version", "request_id"]

def test_v2_is_additive_superset_of_v1(c):
    r1, r2 = c.post("/v1/predict", json=X).json(), c.post("/v2/predict", json=X).json()
    print("v2:", r2)
    assert set(r1) <= set(r2) and {"name", "probabilities"} <= set(r2)
    assert r1["model_version"] != r2["model_version"] and r2["model_version"].endswith("abc1234")

def test_request_schema_same_on_both(c):
    assert c.post("/v1/predict", json={"features": [1, 2, 3]}).status_code == 422
    assert c.post("/v2/predict", json={"features": [1, 2, 3]}).status_code == 422

def test_versions_endpoint(c):
    print("/versions:", c.get("/versions").json())
    assert set(c.get("/versions").json()) == {"v1", "v2"}
