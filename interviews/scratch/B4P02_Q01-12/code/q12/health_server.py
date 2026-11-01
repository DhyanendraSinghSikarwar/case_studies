"""Stdlib model server stub: /live = process alive, /ready = model loaded. Load time is configurable."""
import json, sys, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class State: model = None
def load_model(seconds):
    time.sleep(seconds)               # stands in for reading weights
    State.model = lambda x: x * 2     # "model object"

class H(BaseHTTPRequestHandler):
    def _send(self, code, body):
        b = json.dumps(body).encode(); self.send_response(code)
        self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b)))
        self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        if self.path == "/live": return self._send(200, {"alive": True})
        if self.path == "/ready":
            if State.model is None: return self._send(503, {"ready": False, "reason": "model loading"})
            try: ok = State.model(1) == 2        # real predict on a tiny input, not just 'is not None'
            except Exception as e: return self._send(503, {"ready": False, "reason": str(e)})
            return self._send(200 if ok else 503, {"ready": ok})
        self._send(404, {})
    def log_message(self, *a): pass

def serve(port, load_seconds):
    threading.Thread(target=load_model, args=(load_seconds,), daemon=True).start()
    srv = ThreadingHTTPServer(("127.0.0.1", port), H); srv.serve_forever()

if __name__ == "__main__": serve(int(sys.argv[1]), float(sys.argv[2]))
