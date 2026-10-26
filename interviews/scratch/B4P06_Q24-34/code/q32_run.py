from fastapi.testclient import TestClient
from q32_metrics_app import make_app
with TestClient(make_app()) as c:
    c.post("/predict", headers={"x-request-id": "abc123"}); c.post("/predict"); c.get("/nope")
    print("--- /metrics (selected lines) ---")
    for line in c.get("/metrics").text.splitlines():
        if line.startswith(("predict_requests_total", "predict_latency_seconds_count", "predict_latency_seconds_bucket", "predict_in_flight", "# TYPE predict")) : print(line)
