# 4 "workers" (a semaphore) stand in for CPU capacity. 2 percent of calls take the slow path (200 ms).
import asyncio, random
from fastapi import FastAPI, Response
SLOTS = asyncio.Semaphore(4); waiting = 0; rng = random.Random(1)
MAX_WAITING = 8
app = FastAPI()
async def work():
    await asyncio.sleep(0.200 if rng.random() < 0.02 else 0.005)
@app.post("/predict")                      # no protection: unbounded queue in front of the 4 slots
async def predict():
    async with SLOTS: await work()
    return {"label": 1}
@app.post("/predict_capped")               # concurrency cap: too many waiting -> shed with 503 straight away
async def predict_capped(resp: Response):
    global waiting
    if waiting >= MAX_WAITING: resp.status_code = 503; return {"shed": True}
    waiting += 1
    try:
        async with SLOTS: await work()
    finally: waiting -= 1
    return {"label": 1}
