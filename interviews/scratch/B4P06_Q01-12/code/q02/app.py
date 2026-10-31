import time
from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool

app = FastAPI()

def heavy():                      # stands in for a blocking model call (0.3 s)
    time.sleep(0.3)
    return {"ok": True}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/slow_async")           # BAD: blocking call on the event loop
async def slow_async():
    return heavy()

@app.get("/slow_def")             # OK: FastAPI runs plain def in a threadpool
def slow_def():
    return heavy()

@app.get("/slow_async_pool")      # OK: async def, but blocking work pushed to a thread
async def slow_async_pool():
    return await run_in_threadpool(heavy)
