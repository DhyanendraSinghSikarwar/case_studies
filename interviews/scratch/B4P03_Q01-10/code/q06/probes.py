"""Model server sketch with a loading flag (/healthz = process alive, /ready = model usable),
plus startup-budget arithmetic, a bad-liveness restart timeline and a real local test."""
import http.server, threading, time

STATE = {"loaded": False}

def load_model(seconds):
    time.sleep(seconds)               # stands in for reading weights from disk or object storage
    STATE["loaded"] = True

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            code = 200                                   # alive even while loading
        elif self.path == "/ready":
            code = 200 if STATE["loaded"] else 503       # not ready until weights are in memory
        else:
            code = 404
        self.send_response(code); self.end_headers(); self.wfile.write(b"ok" if code == 200 else b"no")
    def log_message(self, *a): pass

def make_server(load_seconds, port=0):
    threading.Thread(target=load_model, args=(load_seconds,), daemon=True).start()
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv

import urllib.request, urllib.error

def budget(period_s, failure_threshold, initial_delay=0):
    return initial_delay + period_s * failure_threshold

def min_threshold(worst_case_load_s, period_s, safety=1.5):
    need = worst_case_load_s * safety
    return int(-(-need // period_s))                # ceil

print("budget 5s x 36        =", budget(5, 36), "s")
print("min failureThreshold for worst load 90 s, period 5 s, x1.5 safety =", min_threshold(90, 5))

def liveness_loop(load_s, initial=10, period=10, threshold=3, horizon=200):
    """Liveness checks the MODEL (fails while loading). Returns restart times."""
    t0, restarts, fails, t = 0, [], 0, initial
    while t <= horizon:
        loaded = (t - t0) >= load_s
        fails = 0 if loaded else fails + 1
        if fails >= threshold:
            restarts.append(t); t0, fails, t = t, 0, t + initial   # container restarts, loads again
            continue
        t += period
    return restarts
print("bad liveness (checks model, load 90 s) restarts at t =", liveness_loop(90)[:4], "... never becomes healthy")
print("good: liveness=/healthz always 200 -> restarts: none; startupProbe holds liveness off")

def get(port, path):
    try:
        return urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=1).status
    except urllib.error.HTTPError as e:
        return e.code

srv = make_server(load_seconds=1.0)               # 1 s stands in for 90 s
port = srv.server_address[1]
print("t=0.0  /healthz", get(port, "/healthz"), " /ready", get(port, "/ready"))
time.sleep(1.3)
print("t=1.3  /healthz", get(port, "/healthz"), " /ready", get(port, "/ready"))
srv.shutdown()
