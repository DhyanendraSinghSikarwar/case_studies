import os
os.environ.setdefault("MODEL_PATH", "/tmp/claude-0/b6_q1_12/models/iris_v1.onnx")
from fastapi.testclient import TestClient
from app import app

def test_not_ready_before_lifespan():
    c = TestClient(app)                              # NO `with`: lifespan has not run
    assert c.get("/livez").status_code == 200        # alive...
    r = c.get("/readyz")
    print("before lifespan:", r.status_code, r.json())
    assert r.status_code == 503                      # ...but not ready

def test_ready_after_lifespan():
    with TestClient(app) as c:                       # lifespan ran
        r = c.get("/readyz"); d = c.get("/readyz?deep=true"); s = c.get("/startupz")
        print("after lifespan :", r.status_code, r.json(), "| deep:", d.status_code, "| startup:", s.status_code)
        assert r.status_code == d.status_code == s.status_code == 200
