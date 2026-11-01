import os
from fastapi.testclient import TestClient
from q24_cache_app import make_app
MODEL = os.environ["IRIS_ONNX"]
def test_version_bump_misses_cache():
    with TestClient(make_app(MODEL)) as c:
        f = {"features": [5.1, 3.5, 1.4, 0.2]}
        assert c.post("/predict", json=f).json()["cached"] is False
        assert c.post("/predict", json=f).json()["cached"] is True
        c.post("/admin/model_version/v2")
        assert c.post("/predict", json=f).json()["cached"] is False
def test_lru_evicts_oldest():
    with TestClient(make_app(MODEL, cache_size=2)) as c:
        for v in ([1,1,1,1],[2,2,2,2],[3,3,3,3]):
            c.post("/predict", json={"features": v})
        assert c.post("/predict", json={"features": [1,1,1,1]}).json()["cached"] is False
