# Q32: serving-layer observability: request id + structured log, Prometheus histogram, /metrics.
import json, logging, sys, time, uuid
from fastapi import FastAPI, Request, Response
from prometheus_client import CollectorRegistry, Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

MODEL_VERSION = "v1"
def make_app():
    reg = CollectorRegistry()          # own registry: no clashes when tests build the app twice
    REQS = Counter("predict_requests_total", "Requests", ["route", "status"], registry=reg)
    LAT = Histogram("predict_latency_seconds", "Latency", ["route"], buckets=(0.005, 0.01, 0.05, 0.1, 0.5), registry=reg)
    INF = Gauge("predict_in_flight", "In flight", registry=reg)
    log = logging.getLogger("serve"); log.handlers[:] = [logging.StreamHandler(sys.stdout)]
    log.setLevel(logging.INFO); log.propagate = False
    app = FastAPI()
    @app.middleware("http")
    async def observe(request: Request, call_next):
        rid = request.headers.get("x-request-id") or uuid.uuid4().hex[:8]
        t = time.perf_counter(); INF.inc(); status = 500
        try:
            resp = await call_next(request); status = resp.status_code
            resp.headers["x-request-id"] = rid; return resp
        finally:
            INF.dec(); dt = time.perf_counter() - t
            route = request.scope.get("route").path if request.scope.get("route") else "unmatched"   # bounded label values
            REQS.labels(route, str(status)).inc(); LAT.labels(route).observe(dt)
            log.info(json.dumps({"request_id": rid, "route": route, "status": status, "model_version": MODEL_VERSION, "ms": round(dt*1000, 2)}))
    @app.post("/predict")
    async def predict(): return {"label": 1}
    @app.get("/metrics")
    def metrics(): return Response(generate_latest(reg), media_type=CONTENT_TYPE_LATEST)
    return app
