import time
from fastapi.testclient import TestClient
from q30_async_jobs import make_app
def wait(c, jid, timeout=3):
    end = time.time() + timeout
    while time.time() < end:
        s = c.get(f"/jobs/{jid}").json()
        if s["state"] in ("done", "failed"): return s
        time.sleep(0.05)
    raise TimeoutError
def test_submit_poll_result():
    with TestClient(make_app(0.2)) as c:
        r = c.post("/jobs", json={"n": 7}); assert r.status_code == 202
        jid = r.json()["job_id"]; assert r.headers["location"] == f"/jobs/{jid}"
        first = c.get(f"/jobs/{jid}").json(); assert first["state"] in ("queued", "running")
        final = wait(c, jid); assert final == {"state": "done", "result": 49}
def test_idempotency_key_reuses_job():
    with TestClient(make_app(0.1)) as c:
        a = c.post("/jobs", json={"n": 2}, headers={"Idempotency-Key": "k1"}).json()
        b = c.post("/jobs", json={"n": 2}, headers={"Idempotency-Key": "k1"}).json()
        assert a["job_id"] == b["job_id"] and b["deduplicated"] is True
def test_failure_and_unknown():
    with TestClient(make_app(0.05)) as c:
        jid = c.post("/jobs", json={"n": -1}).json()["job_id"]
        assert wait(c, jid)["state"] == "failed"
        assert c.get("/jobs/nope").status_code == 404
def test_expiry():
    with TestClient(make_app(0.05, ttl=0)) as c:
        jid = c.post("/jobs", json={"n": 3}).json()["job_id"]
        time.sleep(0.4); assert c.get(f"/jobs/{jid}").status_code == 404
