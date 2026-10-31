import asyncio, httpx
from q31_limiter import make_app, backoff_delays
def test_sheds_when_full():
    async def go():
        app = make_app(max_in_flight=4, work_s=0.3)
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://t") as c:
            rs = await asyncio.gather(*[c.post("/predict") for _ in range(10)])
            codes = [r.status_code for r in rs]
            stats = (await c.get("/stats")).json()
            late = await c.post("/predict")            # after the burst, capacity is free again
        return codes, rs, stats, late.status_code
    codes, rs, stats, late = asyncio.run(go())
    print("codes:", sorted(codes)); print("stats:", stats)
    assert codes.count(200) == 4 and codes.count(503) == 6
    assert stats["peak"] == 4 and stats["shed"] == 6
    assert all(r.headers["retry-after"] == "1" for r in rs if r.status_code == 503)
    assert late == 200
def test_backoff_bounded_and_jittered():
    d = backoff_delays(); print("backoff:", d)
    assert len(d) == 5
    assert all(0 <= x <= min(2.0, 0.1 * 2 ** i) for i, x in enumerate(d))
