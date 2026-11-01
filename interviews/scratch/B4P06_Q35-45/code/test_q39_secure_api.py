import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent))
import warnings; warnings.filterwarnings("ignore")
from fastapi.testclient import TestClient
from q39_secure_api import make_app
GOOD = {"features": [1, 2, 3, 4]}
class Clock:
    t = 0.0
    def __call__(self): return self.t

def client(clock=None, **kw): return TestClient(make_app(clock or Clock(), **kw))
H = lambda k: {"x-api-key": k}

def test_401_missing_and_wrong_key():
    c = client()
    assert c.post("/v1/models/iris/predict", json=GOOD).status_code == 401
    assert c.post("/v1/models/iris/predict", json=GOOD, headers=H("nope")).status_code == 401

def test_200_with_valid_key():
    assert client().post("/v1/models/iris/predict", json=GOOD, headers=H("key-alice")).json()["score"] == 2.5

def test_403_other_models_key():
    assert client().post("/v1/models/fraud/predict", json=GOOD, headers=H("key-alice")).status_code == 403

def test_413_big_body_with_content_length():
    r = client().post("/v1/models/iris/predict", json={"features": [1.0] * 5000}, headers=H("key-alice"))
    assert r.status_code == 413

def test_413_chunked_body_without_content_length():
    def gen():
        for _ in range(100): yield b" " * 100                # 10 KB streamed, no Content-Length
    r = client().post("/v1/models/iris/predict", content=gen(), headers=H("key-alice"))
    assert r.status_code == 413

def test_422_wrong_shape():
    assert client().post("/v1/models/iris/predict", json={"features": [1, 2]}, headers=H("key-alice")).status_code == 422

def test_429_then_refill():
    clk = Clock(); c = client(clk, capacity=3, rate=1.0)
    codes = [c.post("/v1/models/iris/predict", json=GOOD, headers=H("key-alice")).status_code for _ in range(5)]
    assert codes == [200, 200, 200, 429, 429]
    assert c.post("/v1/models/fraud/predict", json=GOOD, headers=H("key-bob")).status_code == 200   # bob has his own bucket
    clk.t += 2.0                                                  # two tokens refilled
    codes = [c.post("/v1/models/iris/predict", json=GOOD, headers=H("key-alice")).status_code for _ in range(3)]
    assert codes == [200, 200, 429]

def test_bad_key_does_not_spend_tokens():
    c = client(capacity=1)
    for _ in range(5): assert c.post("/v1/models/iris/predict", json=GOOD, headers=H("bad")).status_code == 401
    assert c.post("/v1/models/iris/predict", json=GOOD, headers=H("key-alice")).status_code == 200
