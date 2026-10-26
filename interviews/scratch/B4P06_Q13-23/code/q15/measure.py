# measure.py URL : closed-loop, a few concurrency levels, 3 s each, one local uvicorn process (sandbox only, not a benchmark)
import asyncio, sys, time, statistics, httpx
URL = sys.argv[1]; BODY = {"features": [6.7, 3.0, 5.2, 2.3]}
async def run(conc, secs=3.0):
    lat, errs, stop = [], 0, time.perf_counter() + secs
    async with httpx.AsyncClient(base_url=URL, limits=httpx.Limits(max_connections=conc)) as c:
        async def worker():
            nonlocal errs
            while time.perf_counter() < stop:
                t = time.perf_counter()
                r = await c.post("/v1/predict", json=BODY)
                lat.append(time.perf_counter() - t); errs += r.status_code != 200
        await asyncio.gather(*[worker() for _ in range(conc)])
    lat.sort(); p99 = lat[int(0.99 * len(lat)) - 1] * 1000
    return len(lat) / secs, p99, errs
async def main():
    async with httpx.AsyncClient(base_url=URL) as c:
        for _ in range(50): await c.post("/v1/predict", json=BODY)       # warm-up, not measured
    for conc in (1, 4, 16, 64):
        rps, p99, e = await run(conc)
        print(f"concurrency {conc:>2}: {rps:7.0f} req/s, p99 {p99:7.1f} ms, errors {e}")
asyncio.run(main())
