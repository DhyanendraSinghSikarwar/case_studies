import asyncio, os, subprocess, sys, time, pathlib, statistics, httpx
HERE = str(pathlib.Path(__file__).parent); PORT = 8406; URL = f"http://127.0.0.1:{PORT}"
SECONDS = 5; RATE = 150     # open loop: requests arrive at RATE per second no matter how slow the server is
def pct(v, q): v = sorted(v); return v[min(len(v) - 1, int(q * len(v)))] * 1000
async def run(path, timeout=None, fallback=False, RATE=None):
    RATE = RATE or globals()['RATE']
    lat, shed, fell = [], 0, 0
    async with httpx.AsyncClient(limits=httpx.Limits(max_connections=2000), timeout=30) as c:
        async def one():
            nonlocal shed, fell
            t = time.perf_counter()
            try:
                r = await asyncio.wait_for(c.post(URL + path), timeout) if timeout else await c.post(URL + path)
                if r.status_code == 503: shed += 1
            except asyncio.TimeoutError:
                fell += 1                                   # fallback: a cheap default answer, computed locally
                if not fallback: raise
            lat.append(time.perf_counter() - t)
        tasks = []; start = time.perf_counter()
        for i in range(RATE * SECONDS):
            await asyncio.sleep(max(0, start + i / RATE - time.perf_counter())); tasks.append(asyncio.create_task(one()))
        await asyncio.gather(*tasks)
    ok = [x for x in lat]
    return len(lat), pct(ok, .5), pct(ok, .99), shed, fell
def show(name, r): print(f"{name:42s} n={r[0]:5d}  p50={r[1]:7.1f} ms  p99={r[2]:7.1f} ms  shed(503)={r[3]:4d}  timeout->fallback={r[4]:4d}")
p = subprocess.Popen([sys.executable, "-m", "uvicorn", "q40_app:app", "--port", str(PORT), "--app-dir", HERE, "--log-level", "warning"])
try:
    for _ in range(100):
        try: httpx.get(URL + "/openapi.json", timeout=1); break
        except Exception: time.sleep(0.1)
    asyncio.run(run("/predict", RATE=50))   # warm-up pass (not reported)
    print("4 slots; mean work about 8.9 ms => roughly 450 requests/s max on paper. Open-loop arrivals.")
    for rate in (150, 330):
        print(f"--- offered load {rate} requests/s for {SECONDS}s ---")
        show("A. baseline, 2% slow path, unbounded queue", asyncio.run(run("/predict", RATE=rate)))
        show("B. client timeout 60 ms + fallback", asyncio.run(run("/predict", timeout=0.060, fallback=True, RATE=rate)))
        show("C. server cap (shed above 8 waiting)", asyncio.run(run("/predict_capped", RATE=rate)))
finally:
    p.terminate(); p.wait(timeout=10); print("server stopped:", p.poll() is not None)
