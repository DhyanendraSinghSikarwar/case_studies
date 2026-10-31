# Q16: safe startup download: retries with backoff, sha256 check, atomic rename, readiness gate. Local HTTP server stands in for the model store.
import hashlib, http.server, os, tempfile, threading, time, urllib.request, urllib.error

MODEL = os.urandom(200_000)                       # stand-in "weights"
GOOD = hashlib.sha256(MODEL).hexdigest()
calls = {"n": 0}

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        calls["n"] += 1
        if self.path == "/flaky.bin" and calls["n"] <= 2:      # first two tries fail
            self.send_error(503); return
        body = MODEL[:1000] + b"X" if self.path == "/corrupt.bin" else MODEL
        self.send_response(200); self.send_header("Content-Length", str(len(body))); self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a): pass

srv = http.server.HTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{srv.server_port}"

def fetch(url, dest, sha256, tries=4, delay=0.05):
    for i in range(1, tries + 1):
        tmp = dest + ".part"
        try:
            with urllib.request.urlopen(url, timeout=5) as r, open(tmp, "wb") as f: f.write(r.read())
            h = hashlib.sha256(open(tmp, "rb").read()).hexdigest()
            if h != sha256: raise ValueError(f"checksum mismatch {h[:8]} != {sha256[:8]}")
            os.replace(tmp, dest)                  # atomic: readers never see half a file
            return i
        except (urllib.error.URLError, ValueError) as e:
            print(f"  attempt {i}: {e}")
            if os.path.exists(tmp): os.remove(tmp)
            time.sleep(delay * 2 ** i)             # exponential backoff
    raise SystemExit("giving up: container exits non-zero, orchestrator restarts it, NOT ready")

d = tempfile.mkdtemp(); ready = os.path.join(d, "READY")
print("flaky store, good checksum:")
n = fetch(base + "/flaky.bin", os.path.join(d, "model.bin"), GOOD); print(f"  ok after {n} attempt(s)")
open(ready, "w").write(GOOD)                       # readiness gate: /ready handler would check this file or the loaded model
print("ready file present:", os.path.exists(ready), "| leftover .part files:", [f for f in os.listdir(d) if f.endswith('.part')])
print("corrupt file:")
try: fetch(base + "/corrupt.bin", os.path.join(d, "bad.bin"), GOOD, tries=2)
except SystemExit as e: print(" ", e)
print("bad.bin exists:", os.path.exists(os.path.join(d, "bad.bin")))
