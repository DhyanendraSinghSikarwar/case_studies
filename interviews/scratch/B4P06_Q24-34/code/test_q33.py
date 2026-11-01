import json, os, pathlib
import numpy as np, pytest, onnxruntime as ort
from fastapi.testclient import TestClient
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from iris_app import make_app

MODEL = os.environ["IRIS_ONNX"]
GOLDEN = pathlib.Path(__file__).with_name("golden_iris.json")

@pytest.fixture(scope="module")
def client():
    with TestClient(make_app(MODEL)) as c: yield c        # `with` runs lifespan

def test_startup_ready_and_not_ready_without_lifespan():
    assert TestClient(make_app(MODEL)).get("/readyz").status_code == 503   # no `with`: lifespan did not run
    with TestClient(make_app(MODEL)) as c: assert c.get("/readyz").json() == {"status": "ready"}

def test_contract_schema(client):
    r = client.post("/v1/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})
    assert r.status_code == 200 and set(r.json()) == {"label", "probabilities"}
    assert isinstance(r.json()["label"], int) and len(r.json()["probabilities"]) == 3
    assert client.post("/v1/predict", json={"features": [1, 2]}).status_code == 422
    assert client.post("/v1/predict", json={"features": ["a", 2, 3, 4]}).status_code == 422

def test_golden_file(client):
    golden = json.loads(GOLDEN.read_text())
    for g in golden:
        out = client.post("/v1/predict", json={"features": g["x"]}).json()
        assert out["label"] == g["label"]
        np.testing.assert_allclose(out["probabilities"], g["p"], atol=1e-4)

def test_parity_with_training_pipeline(client):
    X, y = load_iris(return_X_y=True); X = X.astype(np.float32)
    sk = LogisticRegression(max_iter=500).fit(X, y)                   # the original model
    r = client.post("/v1/predict_batch", json={"rows": X.tolist()[:150]}).json()
    assert r["labels"] == sk.predict(X).tolist()
    s = ort.InferenceSession(MODEL, providers=["CPUExecutionProvider"])
    np.testing.assert_allclose(s.run(None, {"X": X})[1], sk.predict_proba(X), atol=1e-4)

def test_batch_equals_singles(client):
    X, _ = load_iris(return_X_y=True)
    rows = X[::10].tolist()
    batch = client.post("/v1/predict_batch", json={"rows": rows}).json()["labels"]
    singles = [client.post("/v1/predict", json={"features": r}).json()["label"] for r in rows]
    assert batch == singles and len(batch) == 15
