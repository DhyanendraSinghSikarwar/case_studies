# loadgen.py URL : closed-loop (fixed concurrency) and open-loop (fixed rate) generators, one 0.3 s stall injected at t=1 s.
import asyncio, sys, time, httpx
STALL = len(sys.argv) < 3; URL = sys.argv[1]; BODY = {"features": [6.7, 3.0, 5.2, 2.3]}; SECS = 4.0
def pct(xs, p):
    xs = sorted(xs); return xs[min(len(xs) - 1, int(p / 100 * len(xs)))] * 1000
def show(name, lat, extra=""):
    print(f"{name:<34} n={len(lat):>4}  p50 {pct(lat,50):7.1f}  p95 {pct(lat,95):7.1f}  p99 {pct(lat,99):7.1f}  max {max(lat)*1000:7.1f} ms {extra}")
async def stall_once(c):
    await asyncio.sleep(1.0); await c.get("/stall", params={"secs": 0.3}, timeout=10)

async def closed_loop(conc):
    lat = []; end = time.perf_counter() + SECS
    async with httpx.AsyncClient(base_url=URL) as c:
        async def w():
            while time.perf_counter() < end:
                t = time.perf_counter(); await c.post("/v1/predict", json=BODY); lat.append(time.perf_counter() - t)
        await asyncio.gather(stall_once(c), *[w() for _ in range(conc)])
    return lat

async def open_loop(rate):
    sent_lat, true_lat = [], []; n = int(rate * SECS); t0 = time.perf_counter() + 0.1
    async with httpx.AsyncClient(base_url=URL, limits=httpx.Limits(max_connections=1000)) as c:
        async def one(i):
            intended = t0 + i / rate                               # when the request SHOULD have been sent
            await asyncio.sleep(max(0, intended - time.perf_counter()))
            s = time.perf_counter(); await c.post("/v1/predict", json=BODY); e = time.perf_counter()
            sent_lat.append(e - s); true_lat.append(e - intended)
        await asyncio.gather(*( [stall_once(c)] if STALL else [] ), *[one(i) for i in range(n)])
    return sent_lat, true_lat

async def main():
    async with httpx.AsyncClient(base_url=URL) as c:
        for _ in range(100): await c.post("/v1/predict", json=BODY)      # warm-up, discarded
    show("closed loop, concurrency 1", await closed_loop(1))
    s, t = await open_loop(80)
    show("open loop 80 rps, from send time", s)
    show("open loop 80 rps, from intended time", t, "<- the honest one")
asyncio.run(main())
