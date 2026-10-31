"""Real SIGTERM test: a worker that drains in-flight work vs one that ignores SIGTERM handling."""
import os, signal, subprocess, sys, tempfile, textwrap, time

WORKER = textwrap.dedent('''
    import signal, sys, time
    handle = sys.argv[1] == "graceful"
    stopping = False
    def on_term(signum, frame):
        global stopping
        stopping = True                      # stop taking new work, finish what we have
    if handle:
        signal.signal(signal.SIGTERM, on_term)
    inflight = ["req-1", "req-2", "req-3"]   # pretend these are in-flight requests (0.2 s each)
    print("ready", flush=True)
    done = []
    while True:
        if stopping and not inflight:
            break
        if inflight:
            time.sleep(0.2); done.append(inflight.pop(0))
            print("finished", done[-1], flush=True)
        else:
            time.sleep(0.05)                 # idle loop, waiting for new work
    print("drained", len(done), "requests; exiting 0", flush=True)
    sys.exit(0)
''')

def trial(mode):
    path = os.path.join(tempfile.mkdtemp(), "worker.py")
    open(path, "w").write(WORKER)
    p = subprocess.Popen([sys.executable, "-I", path, mode], stdout=subprocess.PIPE, text=True)
    assert p.stdout.readline().strip() == "ready"
    time.sleep(0.1)                          # first request is in progress
    p.send_signal(signal.SIGTERM)            # what the kubelet sends first
    out, _ = p.communicate(timeout=10)
    return p.returncode, out.strip().splitlines()

for mode in ("graceful", "ignore-handler"):
    rc, lines = trial(mode)
    print(f"--- {mode}: exit code {rc}")
    for l in lines: print("   ", l)
