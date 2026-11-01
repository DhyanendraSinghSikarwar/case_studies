import time, json, random, zlib, statistics as st
from collections import deque

class CallLogger:
    """Log metadata first: no raw text stored, only length, latency, a hash of the request, feedback."""
    def __init__(self, window=50):
        self.rows = deque(maxlen=window)
    def log(self, request_id, prompt, response, latency_ms, error=None):
        self.rows.append({"id": request_id, "prompt_len": len(prompt), "resp_len": len(response or ""),
                          "latency_ms": latency_ms, "error": error, "thumb": None, "prompt_hash": zlib.crc32(prompt.encode())})
    def feedback(self, request_id, thumb):
        for r in self.rows:
            if r["id"] == request_id: r["thumb"] = thumb
    def summary(self):
        rows = list(self.rows); lat = sorted(r["latency_ms"] for r in rows)
        fb = [r["thumb"] for r in rows if r["thumb"] is not None]
        return {"n": len(rows), "error_rate": round(sum(r["error"] is not None for r in rows) / len(rows), 3),
                "p50_ms": lat[len(lat) // 2], "p95_ms": lat[int(0.95 * (len(lat) - 1))],
                "mean_resp_len": round(st.mean(r["resp_len"] for r in rows), 1),
                "feedback_n": len(fb), "thumbs_up_rate": round(sum(fb) / len(fb), 3) if fb else None}

def stub_model(prompt, rng):                       # stands in for a real provider call (NOT executed here)
    if rng.random() < 0.10: raise TimeoutError("stub timeout")
    return "ok " * rng.randint(3, 30)

rng = random.Random(42); lg = CallLogger(window=50)
for i in range(80):
    p = "question %d " % i + "x" * rng.randint(0, 100)
    t0 = time.perf_counter()
    try: out, err = stub_model(p, rng), None
    except TimeoutError as e: out, err = None, str(e)
    lat = rng.randint(80, 400) if i < 60 else rng.randint(300, 900)   # simulated latency; late slowdown
    lg.log(i, p, out, lat, err)
    if i % 3 == 0 and err is None: lg.feedback(i, rng.random() < 0.7)
    if i in (49, 79): print(f"after {i+1} calls:", json.dumps(lg.summary()))
