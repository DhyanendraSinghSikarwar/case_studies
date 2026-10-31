# Starts 3 apps (stable 8401, canary 8402, shadow 8403) + gateway 8404, runs the demo, stops everything.
import os, subprocess, sys, time, random, statistics, pathlib
import httpx
HERE = str(pathlib.Path(__file__).parent); PY = sys.executable; procs = []
def start(mod, port, **env):
    p = subprocess.Popen([PY, "-m", "uvicorn", f"{mod}:app", "--port", str(port), "--log-level", "warning", "--app-dir", HERE],
                         env={**os.environ, **env}); procs.append(p)
def wait(port):
    for _ in range(100):
        try: httpx.get(f"http://127.0.0.1:{port}/openapi.json", timeout=1); return
        except Exception: time.sleep(0.1)
    raise RuntimeError(port)
try:
    start("q37_model_app", 8401, VERSION="v1", DELAY_MS="2")
    start("q37_model_app", 8402, VERSION="v2", DELAY_MS="2")
    start("q37_model_app", 8403, VERSION="v2", DELAY_MS="20", SLOW_TAIL="1")   # shadow: 20 ms, but 5% of calls take 400 ms+
    start("q37_gateway", 8404, STABLE_URL="http://127.0.0.1:8401", CANARY_URL="http://127.0.0.1:8402", SHADOW_URL="http://127.0.0.1:8403")
    for p in (8401, 8402, 8403, 8404): wait(p)
    G = "http://127.0.0.1:8404"; c = httpx.Client(timeout=10); rng = random.Random(7)
    users = [f"user{i}" for i in range(1000)]
    def sweep(label):
        routed = {}; lat = []
        for u in users:
            t = time.perf_counter(); r = c.post(G + "/predict", json={"user_id": u, "x": rng.random()}).json(); lat.append(time.perf_counter() - t)
            routed[u] = r["routed"]
        n = sum(v == "canary" for v in routed.values()); print(f"{label}: canary share = {n/len(users):.1%} of 1000 users, caller p50 {statistics.median(lat)*1000:.1f} ms, p99 {sorted(lat)[989]*1000:.1f} ms")
        return routed
    r5 = sweep("5% step"); r5b = sweep("5% again (same users)")
    print("users who flipped between two sweeps at 5%:", sum(r5[u] != r5b[u] for u in users))
    c.post(G + "/admin/percent/25"); r25 = sweep("25% step")
    print("users on canary at 5% who left canary at 25%:", sum(r5[u] == "canary" and r25[u] != "canary" for u in users))
    c.post(G + "/admin/percent/100"); r100 = sweep("100% step")
    print("users on canary at 25% who left canary at 100%:", sum(r25[u] == "canary" and r100[u] != "canary" for u in users))
    c.post(G + "/admin/percent/10"); print("ramp-down request ignored, percent still:", c.get(G + "/admin/state").json()["percent"])
    time.sleep(1.0)
    s = c.get(G + "/admin/state").json()
    print(f"shadow: sent {s['mirror_sent']}, completed {s['mirror_done']}, timed out (150 ms cap) {s['mirror_timeout']}, agree {s['mirror_agree']}")
    # rollback: break the canary, then keep sending traffic
    httpx.post("http://127.0.0.1:8402/admin/break")
    codes = []
    for i in range(60):
        r = c.post(G + "/predict", json={"user_id": f"user{i}", "x": 0.3}); codes.append((r.status_code, r.json().get("routed")))
    s = c.get(G + "/admin/state").json()
    print("after breaking canary: rolled_back =", s["rolled_back"], "| HTTP statuses seen by callers:", sorted({c_[0] for c_ in codes}),
          "| last 10 routed to:", sorted({c_[1] for c_ in codes[-10:]}))
finally:
    for p in procs: p.terminate()
    for p in procs: p.wait(timeout=10)
    print("servers stopped:", all(p.poll() is not None for p in procs))
