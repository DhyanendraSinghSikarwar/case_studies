# Q30: async job pattern: 202 + job id + polling. In-process queue and worker thread stand in for Celery/Redis.
import queue, threading, time, uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Header, HTTPException, Response
from pydantic import BaseModel

class Job(BaseModel):
    n: int

def make_app(work_seconds=0.3, ttl=3600):
    jobs, idem, q = {}, {}, queue.Queue()
    def worker():
        while True:
            jid = q.get()
            if jid is None: break
            jobs[jid]["state"] = "running"
            try:
                time.sleep(work_seconds)                      # the slow model
                if jobs[jid]["n"] < 0: raise ValueError("negative n")
                jobs[jid].update(state="done", result=jobs[jid]["n"] ** 2)
            except Exception as e:
                jobs[jid].update(state="failed", error=str(e))
            jobs[jid]["finished"] = time.time()
    @asynccontextmanager
    async def lifespan(app):
        t = threading.Thread(target=worker, daemon=True); t.start()
        yield
        q.put(None); t.join(timeout=2)
    app = FastAPI(lifespan=lifespan)
    @app.post("/jobs", status_code=202)
    def submit(j: Job, response: Response, idempotency_key: str | None = Header(default=None)):
        if idempotency_key and idempotency_key in idem:      # retry of the same request: same job
            response.headers["Location"] = f"/jobs/{idem[idempotency_key]}"
            return {"job_id": idem[idempotency_key], "state": jobs[idem[idempotency_key]]["state"], "deduplicated": True}
        jid = uuid.uuid4().hex[:8]
        jobs[jid] = {"state": "queued", "n": j.n, "created": time.time()}
        if idempotency_key: idem[idempotency_key] = jid
        q.put(jid); response.headers["Location"] = f"/jobs/{jid}"
        return {"job_id": jid, "state": "queued", "deduplicated": False}
    @app.get("/jobs/{jid}")
    def status(jid: str):
        j = jobs.get(jid)
        if j is None: raise HTTPException(404, "unknown or expired job")
        if "finished" in j and time.time() - j["finished"] > ttl:
            del jobs[jid]; raise HTTPException(404, "unknown or expired job")
        return {k: v for k, v in j.items() if k in ("state", "result", "error")}
    return app
