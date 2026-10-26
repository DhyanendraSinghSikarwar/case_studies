import asyncio, time, sys, httpx, numpy as np
BASE = "http://127.0.0.1:8107"; CONC, EACH = 32, 25
rng = np.random.default_rng(1)
async def worker(c, lat):
    for _ in range(EACH):
        body = {"x": rng.standard_normal(512).tolist()}
        t = time.perf_counter(); r = await c.post("/predict", json=body); lat.append((time.perf_counter() - t) * 1000)
        assert r.status_code == 200
async def main():
    async with httpx.AsyncClient(base_url=BASE, timeout=30, limits=httpx.Limits(max_connections=CONC)) as c:
        for _ in range(10): await c.post("/predict", json={"x": [0.0] * 512})
        await c.get("/stats"); lat = []; t0 = time.perf_counter()
        await asyncio.gather(*[worker(c, lat) for _ in range(CONC)])
        wall = time.perf_counter() - t0; st = (await c.get("/stats")).json()
        p = np.percentile(lat, [50, 99])
        print(f"{CONC*EACH} reqs, {CONC} concurrent: {CONC*EACH/wall:6.0f} req/s  p50 {p[0]:6.1f} ms  p99 {p[1]:6.1f} ms | server stats incl. warm-up: {st}")
asyncio.run(main())
