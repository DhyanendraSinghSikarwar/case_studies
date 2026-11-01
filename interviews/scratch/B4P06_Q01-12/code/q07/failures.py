import asyncio, httpx
async def main():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8107", timeout=10) as c:
        good = {"x": [0.1] * 512}; bad = {"x": [-999.0] + [0.1] * 511}
        rs = await asyncio.gather(c.post("/predict", json=good), c.post("/predict", json=bad), c.post("/predict", json=good))
        print("good/bad/good in one batch ->", [r.status_code for r in rs])
        # cancelled request: client gives up after 1 ms; server keeps working
        try: await c.post("/predict", json=good, timeout=0.0001)
        except httpx.TimeoutException: print("client timed out (cancelled) ok")
        print("still serving ->", (await c.post("/predict", json=good)).status_code)
asyncio.run(main())
