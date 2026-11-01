import threading, time
from fastapi.testclient import TestClient
from holder import app, holder

def test_not_ready_before_lifespan():
    holder._m = None
    c = TestClient(app)                           # no "with": lifespan not run
    assert c.get("/readyz").status_code == 503

def test_reload_never_shows_half_loaded_model():
    with TestClient(app) as c:
        assert c.get("/readyz").json() == {"ready": True, "version": "v1"}
        seen, errors, stop = set(), [], threading.Event()
        def reader():
            while not stop.is_set():
                r = c.post("/predict", params={"x": 1.0})
                if r.status_code != 200: errors.append(r.text); continue
                seen.add(r.json()["version"])
        ts = [threading.Thread(target=reader) for _ in range(4)]
        [t.start() for t in ts]
        time.sleep(0.1)
        assert c.post("/admin/reload", params={"version": "v2", "load_secs": 0.3}).status_code == 200   # slow load beside v1
        time.sleep(0.1); stop.set(); [t.join() for t in ts]
        assert errors == [], errors               # no 500 from the half-loaded assertion, no 503
        assert seen == {"v1", "v2"}, seen         # old served during the load, new after the swap
        assert c.post("/predict", params={"x": 2.0}).json() == {"version": "v2", "y": 6.0}

def test_naive_in_place_reload_is_caught():
    """control: mutate the LIVE object in steps. The same reader check must catch it."""
    import holder as h
    m = h.Model("v1"); stop = threading.Event(); bad = []
    def reader():
        while not stop.is_set():
            try: m.predict(1.0)
            except AssertionError as e: bad.append(str(e))
    t = threading.Thread(target=reader); t.start()
    m.version = "v2"; time.sleep(0.2); m.weights = "weights-of-v2"       # half-loaded window
    stop.set(); t.join()
    assert bad and "half-loaded" in bad[0]
