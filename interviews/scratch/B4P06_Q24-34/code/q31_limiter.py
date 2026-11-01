# Q31: concurrency limiter that sheds load with 503 + Retry-After instead of queueing forever.
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

def make_app(max_in_flight=4, work_s=0.2):
    app = FastAPI(); st = {"in_flight": 0, "peak": 0, "shed": 0, "served": 0}
    @app.middleware("http")
    async def limiter(request: Request, call_next):
        if request.url.path != "/predict": return await call_next(request)
        if st["in_flight"] >= max_in_flight:          # no await between check and increment: no race
            st["shed"] += 1
            return JSONResponse({"detail": "overloaded"}, status_code=503, headers={"Retry-After": "1"})
        st["in_flight"] += 1; st["peak"] = max(st["peak"], st["in_flight"])
        try: return await call_next(request)
        finally: st["in_flight"] -= 1
    @app.post("/predict")
    async def predict():
        await asyncio.sleep(work_s); st["served"] += 1       # stand-in for model time
        return {"label": 1}
    @app.get("/stats")
    async def stats(): return st
    return app

def backoff_delays(base=0.1, cap=2.0, tries=5, seed=0):
    """Full-jitter exponential backoff schedule for a client (idempotent calls only)."""
    import random; r = random.Random(seed)
    return [round(r.uniform(0, min(cap, base * 2 ** i)), 3) for i in range(tries)]
