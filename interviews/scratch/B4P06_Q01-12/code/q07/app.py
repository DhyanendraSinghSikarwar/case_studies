import asyncio, os
from contextlib import asynccontextmanager
import numpy as np, onnxruntime as ort
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

MAX_BATCH = int(os.environ.get("MAX_BATCH", "32"))
MAX_WAIT = float(os.environ.get("MAX_WAIT_MS", "5")) / 1000

class Req(BaseModel):
    x: list[float] = Field(min_length=512, max_length=512)

class MicroBatcher:
    def __init__(self, session, max_batch, max_wait):
        self.s, self.max_batch, self.max_wait = session, max_batch, max_wait
        self.q: asyncio.Queue = asyncio.Queue()
        self.sizes: list[int] = []
        self.task = None

    def start(self):
        self.task = asyncio.create_task(self._loop())

    async def submit(self, row: np.ndarray):
        fut = asyncio.get_running_loop().create_future()
        await self.q.put((row, fut))
        return await fut                              # cancelled client -> fut is cancelled

    def _run(self, rows):                             # blocking; runs in a worker thread
        if any(r[0] == -999.0 for r in rows):         # demo "poison" row that makes the model raise
            raise ValueError("bad row")
        return self.s.run(None, {"x": np.stack(rows)})[0]

    async def _loop(self):
        loop = asyncio.get_running_loop()
        while True:
            row, fut = await self.q.get()
            items = [(row, fut)]
            deadline = loop.time() + self.max_wait
            while len(items) < self.max_batch:
                left = deadline - loop.time()
                if left <= 0:
                    break
                try:
                    items.append(await asyncio.wait_for(self.q.get(), left))
                except asyncio.TimeoutError:
                    break
            items = [(r, f) for r, f in items if not f.done()]     # drop cancelled requests
            if not items:
                continue
            self.sizes.append(len(items))
            try:
                out = await asyncio.to_thread(self._run, [r for r, _ in items])
                for (_, f), o in zip(items, out):                  # same order in, same order out
                    if not f.done(): f.set_result(o)
            except Exception:
                for r, f in items:                                  # isolate the bad row: retry one by one
                    try:
                        o = (await asyncio.to_thread(self._run, [r]))[0]
                        if not f.done(): f.set_result(o)
                    except Exception as e:
                        if not f.done(): f.set_exception(e)

    async def stop(self):
        self.task.cancel()
        while not self.q.empty():                                   # fail whatever is still queued
            _, f = self.q.get_nowait()
            if not f.done(): f.set_exception(RuntimeError("shutting down"))

@asynccontextmanager
async def lifespan(app):
    so = ort.SessionOptions(); so.intra_op_num_threads = 1
    app.state.b = MicroBatcher(ort.InferenceSession(os.environ["MLP_PATH"], so, providers=["CPUExecutionProvider"]),
                               MAX_BATCH, MAX_WAIT)
    app.state.b.start()
    yield
    await app.state.b.stop()

app = FastAPI(lifespan=lifespan)

@app.post("/predict")
async def predict(req: Req, request: Request):
    try:
        y = await request.app.state.b.submit(np.asarray(req.x, dtype=np.float32))
    except ValueError:
        raise HTTPException(422, "model rejected this row")
    except RuntimeError:
        raise HTTPException(503, "shutting down")
    return {"argmax": int(np.argmax(y))}

@app.get("/stats")
def stats(request: Request):
    s = request.app.state.b.sizes
    return {"batches": len(s), "mean_batch": round(sum(s) / max(1, len(s)), 2), "max_batch": max(s, default=0)}
