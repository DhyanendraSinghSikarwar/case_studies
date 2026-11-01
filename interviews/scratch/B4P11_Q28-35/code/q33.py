# q33.py - driver (stdlib only): start both emulators on own ports, write the SAME artifact through both adapters, stop them.
import subprocess, time, os, sys, json, socket, tempfile
VENV = "/tmp/claude-0/b11p11"; HERE = os.path.dirname(os.path.abspath(__file__))
W = sys.argv[1]; os.makedirs(W + "/blob", exist_ok=True); os.makedirs(W + "/gcs", exist_ok=True)
AZ_PORT, GCS_PORT = 8631, 8632
art = W + "/model.bin"; open(art, "wb").write(b"fake-model-weights-v1" * 100)
def wait(port):
    for _ in range(60):
        try: socket.create_connection(("127.0.0.1", port), 0.3).close(); return True
        except OSError: time.sleep(0.5)
    return False
procs = []
try:
    procs.append(subprocess.Popen([f"{VENV}/az_npm/node_modules/.bin/azurite-blob", "--blobPort", str(AZ_PORT), "--location", W + "/blob",
        "--skipApiVersionCheck", "--silent"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
    procs.append(subprocess.Popen([f"{VENV}/emu/bin/gcp-storage-emulator", "start", "--port", str(GCS_PORT), "--default-bucket=mlartifacts",
        "--in-memory"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
    print("ports up:", wait(AZ_PORT), wait(GCS_PORT))
    for kind, port, py in (("azure", AZ_PORT, "az"), ("gcs", GCS_PORT, "gcp")):
        r = subprocess.run([f"{VENV}/{py}/bin/python", "-I", HERE + "/q33_adapter.py", kind, str(port), "models/churn/1/model.bin", art],
                           capture_output=True, text=True, timeout=120)
        print(kind, "->", r.stdout.strip() or r.stderr.strip()[-300:])
finally:
    for p in procs: p.terminate()
    for p in procs:
        try: p.wait(10)
        except Exception: p.kill()
    print("stopped; ports free:", all(subprocess.run(["bash","-c",f"! (echo > /dev/tcp/127.0.0.1/{x}) 2>/dev/null"]).returncode == 0 for x in (AZ_PORT, GCS_PORT)))
