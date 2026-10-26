import sys, time, statistics
from fastapi.testclient import TestClient
from q24_cache_app import make_app, cache_key
model = sys.argv[1]
app = make_app(model)
with TestClient(app) as c:
    f = [6.7, 3.0, 5.2, 2.3]
    r1 = c.post("/predict", json={"features": f}).json()
    r2 = c.post("/predict", json={"features": f}).json()
    r3 = c.post("/predict", json={"features": [6.7000001, 3.0, 5.2, 2.3]}).json()
    print("1st:", r1); print("2nd:", r2); print("same after rounding to 6dp:", r3["cached"])
    c.post("/admin/model_version/v2")
    r4 = c.post("/predict", json={"features": f}).json()
    print("after bump to v2:", r4)
    assert r1["cached"] is False and r2["cached"] is True and r4["cached"] is False
    print("keys differ across versions:", cache_key("v1", f) != cache_key("v2", f))
    print("bad input:", c.post("/predict", json={"features": [1, 2]}).status_code)
    print("stats after test:", c.get("/cache/stats").json())
    # tiny measurement: 20 distinct inputs, each sent 10 times (200 requests)
    c.post("/admin/model_version/v3")
    import random; random.seed(0)
    inputs = [[round(random.uniform(4,8),1), round(random.uniform(2,4),1), round(random.uniform(1,7),1), round(random.uniform(0.1,2.5),1)] for _ in range(20)]
    miss_t, hit_t = [], []
    for rep in range(10):
        for x in inputs:
            t = time.perf_counter(); j = c.post("/predict", json={"features": x}).json(); dt = (time.perf_counter()-t)*1000
            (hit_t if j["cached"] else miss_t).append(dt)
    s = c.get("/cache/stats").json()
    print("requests 200, misses", len(miss_t), "hits", len(hit_t), "hit rate", len(hit_t)/200)
    print(f"median ms miss {statistics.median(miss_t):.2f}, hit {statistics.median(hit_t):.2f} (this sandbox, TestClient, not a benchmark)")
