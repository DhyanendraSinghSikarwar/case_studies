"""Start the stub with a 3 s 'model load' and run healthcheck.py every 0.5 s: shows start-period idea."""
import subprocess, sys, time, os
HERE = os.path.dirname(os.path.abspath(__file__))
srv = subprocess.Popen([sys.executable, "-I", os.path.join(HERE, "health_server.py"), "8765", "3"])
t0 = time.time(); first_ok = None
try:
    while time.time() - t0 < 5:
        live = subprocess.run([sys.executable, "-I", os.path.join(HERE, "healthcheck.py"), "http://127.0.0.1:8765/live"]).returncode
        ready = subprocess.run([sys.executable, "-I", os.path.join(HERE, "healthcheck.py"), "http://127.0.0.1:8765/ready"]).returncode
        t = time.time() - t0
        print(f"t={t:3.1f}s live_rc={live} ready_rc={ready}")
        if ready == 0 and first_ok is None: first_ok = t
        time.sleep(0.5)
finally:
    srv.terminate(); srv.wait()
print("ready first seen at about", round(first_ok, 1), "s (load takes 3 s)")
