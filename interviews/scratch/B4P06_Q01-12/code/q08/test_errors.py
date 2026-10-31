import os
os.environ.setdefault("MODEL_PATH", "/tmp/claude-0/b6_q1_12/models/iris_v1.onnx")
import pytest
from fastapi.testclient import TestClient
from app import app

GOOD = {"sepal_len": 6.7, "sepal_wid": 3.0, "petal_len": 5.2, "petal_wid": 2.3, "region": "north", "age_days": 10}

@pytest.fixture(scope="module")
def c():
    with TestClient(app, raise_server_exceptions=False) as client:
        yield client

def test_ok(c):
    r = c.post("/v1/predict", json=GOOD)
    print(r.status_code, r.json()); assert r.status_code == 200 and r.json()["label"] == 2

def test_negative_age(c):
    r = c.post("/v1/predict", json={**GOOD, "age_days": -5})
    print(r.status_code, r.json()); assert r.status_code == 422 and r.json()["error"]["details"][0]["field"] == "age_days"

def test_nan_literal_rejected(c):
    r = c.post("/v1/predict", content=b'{"sepal_len": NaN, "sepal_wid": 3, "petal_len": 5, "petal_wid": 2, "region": "north", "age_days": 1}',
               headers={"content-type": "application/json"})
    print(r.status_code, r.json()["error"]["details"]); assert r.status_code == 422

def test_infinity_rejected(c):
    r = c.post("/v1/predict", content=b'{"sepal_len": 1, "sepal_wid": 3, "petal_len": Infinity, "petal_wid": 2, "region": "north", "age_days": 1}',
               headers={"content-type": "application/json"})
    assert r.status_code == 422

def test_business_rule_validator(c):
    r = c.post("/v1/predict", json={**GOOD, "petal_wid": 9.0})
    print(r.status_code, r.json()["error"]["details"]); assert r.status_code == 422

def test_bad_enum_and_extra_field(c):
    assert c.post("/v1/predict", json={**GOOD, "region": "mars"}).status_code == 422
    assert c.post("/v1/predict", json={**GOOD, "colour": "red"}).status_code == 422

def test_too_large_413(c):
    r = c.post("/v1/predict", content=b"x" * 5000, headers={"content-type": "application/json"})
    print(r.status_code, r.json()); assert r.status_code == 413

def test_model_failure_503_with_request_id(c):
    class Boom:
        def run(self, *a, **k): raise RuntimeError("secret internal path /models/x.onnx corrupted")
    real = app.state.session; app.state.session = Boom()
    try:
        r = c.post("/v1/predict", json=GOOD, headers={"x-request-id": "req-abc-123"})
    finally:
        app.state.session = real
    print(r.status_code, r.json(), r.headers["x-request-id"])
    assert r.status_code == 503 and r.json()["error"]["request_id"] == "req-abc-123"
    assert "secret" not in r.text and "Traceback" not in r.text

def test_unknown_route_404(c):
    assert c.get("/v1/nope").status_code == 404
