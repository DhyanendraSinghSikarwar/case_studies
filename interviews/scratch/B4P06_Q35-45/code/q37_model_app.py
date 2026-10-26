# Tiny stand-in model server. VERSION, DELAY_MS and the /admin/break toggle come from the environment/requests.
import os, asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
VERSION = os.environ.get("VERSION", "v1"); DELAY = float(os.environ.get("DELAY_MS", "2")) / 1000
state = {"broken": False}
app = FastAPI()
class Req(BaseModel): x: float
@app.post("/predict")
async def predict(r: Req):
    await asyncio.sleep(DELAY)
    if os.environ.get("SLOW_TAIL") and r.x >= 0.95: await asyncio.sleep(0.4)   # about 5 percent of calls are very slow
    if state["broken"]: raise HTTPException(500, "model crashed")
    # v2 differs from v1 for inputs in [0.9, 1.0): about 10 percent of uniform inputs
    label = int(r.x > 0.5) if not (VERSION == "v2" and r.x >= 0.9) else 0
    return {"version": VERSION, "label": label}
@app.post("/admin/break")
async def brk(): state["broken"] = True; return {"broken": True}
