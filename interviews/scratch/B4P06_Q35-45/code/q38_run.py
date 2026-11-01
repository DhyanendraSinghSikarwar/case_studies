import os, signal, subprocess, sys, threading, time, pathlib, httpx
HERE = str(pathlib.Path(__file__).parent); PORT = 8405
def launch(extra):
    return subprocess.Popen([sys.executable, "-m", "uvicorn", "q38_app:app", "--port", str(PORT), "--app-dir", HERE, "--log-level", "info", *extra],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
def wait_ready(p):
    for _ in range(100):
        try:
            if httpx.get(f"http://127.0.0.1:{PORT}/readyz", timeout=1).status_code == 200: return
        except Exception: pass
        time.sleep(0.1)
    raise RuntimeError("not ready")
def trial(name, extra, slow_seconds):
    p = launch(extra)
    try:
        # readiness: 503 while loading, then 200
        t0 = time.time(); first = None
        while True:
            try: first = httpx.get(f"http://127.0.0.1:{PORT}/readyz", timeout=1).status_code; break
            except Exception: time.sleep(0.02)
        print(f"[{name}] first /readyz answer right after start: {first}")
        wait_ready(p)
        res = {}
        def call():
            try: res["r"] = httpx.post(f"http://127.0.0.1:{PORT}/slow", params={"seconds": slow_seconds}, timeout=30).json()
            except Exception as e: res["err"] = type(e).__name__
        th = threading.Thread(target=call); th.start(); time.sleep(0.5)
        t_term = time.time(); p.send_signal(signal.SIGTERM)
        time.sleep(0.3)
        try: httpx.get(f"http://127.0.0.1:{PORT}/readyz", timeout=1); new = "accepted"
        except Exception as e: new = "refused (" + type(e).__name__ + ")"
        th.join(); rc = p.wait(timeout=20); t_exit = time.time()
        out = p.stdout.read()
        print(f"[{name}] new request after SIGTERM: {new}")
        print(f"[{name}] in-flight request: {res}  (slow request asked for {slow_seconds}s)")
        print(f"[{name}] exit code {rc}, exited {t_exit - t_term:.2f}s after SIGTERM")
        print(f"[{name}] relevant log lines:", [l.strip() for l in out.splitlines() if any(k in l for k in ("Shutting", "Waiting", "lifespan", "Finished", "Cancel", "cancel"))])
    finally:
        if p.poll() is None: p.kill()
trial("graceful 10s window", ["--timeout-graceful-shutdown", "10"], 2.0)
trial("window too short (1s)", ["--timeout-graceful-shutdown", "1"], 4.0)
