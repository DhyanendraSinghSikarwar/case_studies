import os
os.environ.setdefault("MODEL_PATH", "/tmp/claude-0/b6_q1_12/models/iris_v1.onnx")
from fastapi.testclient import TestClient
from app import app


def test_ok():
    with TestClient(app) as c:                       # `with` runs the lifespan
        r = c.post("/v1/predict", json={"features": [6.7, 3.0, 5.2, 2.3]})
        print(r.status_code, r.json())
        assert r.status_code == 200 and r.json()["name"] == "virginica"


def test_wrong_length_422():
    with TestClient(app) as c:
        r = c.post("/v1/predict", json={"features": [1.0, 2.0, 3.0]})
        print(r.status_code, r.json()["detail"][0]["type"], r.json()["detail"][0]["loc"])
        assert r.status_code == 422


def test_typo_key_and_bad_type_422():
    with TestClient(app) as c:
        r1 = c.post("/v1/predict", json={"feature": [1, 2, 3, 4]})
        r2 = c.post("/v1/predict", json={"features": [1, 2, "abc", 4]})
        print(r1.status_code, [e["type"] for e in r1.json()["detail"]])
        print(r2.status_code, [e["type"] for e in r2.json()["detail"]])
        assert r1.status_code == r2.status_code == 422
