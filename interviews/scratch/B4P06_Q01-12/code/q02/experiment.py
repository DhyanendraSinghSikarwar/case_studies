import asyncio, time, httpx

BASE = "http://127.0.0.1:8102"

async def trial(client, path):
    slow = asyncio.create_task(client.get(path))
    await asyncio.sleep(0.05)                      # slow request is now running
    t = time.perf_counter()
    h = await client.get("/health")
    health_ms = (time.perf_counter() - t) * 1000
    await slow
    return health_ms

async def main():
    async with httpx.AsyncClient(base_url=BASE, timeout=10) as c:
        await c.get("/health")                     # warm up
        t = time.perf_counter(); await c.get("/health")
        print(f"idle /health            : {(time.perf_counter()-t)*1000:7.1f} ms")
        for path in ["/slow_async", "/slow_def", "/slow_async_pool"]:
            ms = await trial(c, path)
            print(f"/health during {path:17s}: {ms:7.1f} ms")
        # 4 concurrent slow requests, total wall time
        for path in ["/slow_async", "/slow_def"]:
            t = time.perf_counter()
            await asyncio.gather(*[c.get(path) for _ in range(4)])
            print(f"4 concurrent {path:12s} wall: {(time.perf_counter()-t)*1000:7.1f} ms")

asyncio.run(main())
