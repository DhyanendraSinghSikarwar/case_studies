"""Launch each style as PID 1 of a new PID namespace (unshare --pid --fork), send SIGTERM from outside
like `docker stop` does, wait a short grace period, then SIGKILL. Needs root + unshare (works in this sandbox)."""
import subprocess, signal, time, os
HERE = os.path.dirname(os.path.abspath(__file__))
GRACE = 1.5
def run(name, argv):
    p = subprocess.Popen(["unshare", "--pid", "--fork", "--mount-proc"] + argv, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, cwd=HERE, start_new_session=True)
    time.sleep(1.0)
    # unshare --fork makes the command PID 1 in the namespace; signal the namespace's init (child of unshare)
    kids = subprocess.run(["pgrep", "-P", str(p.pid)], capture_output=True, text=True).stdout.split()
    init = int(kids[0]); os.kill(init, signal.SIGTERM)
    deadline = time.time() + GRACE
    while time.time() < deadline and p.poll() is None: time.sleep(0.05)
    if p.poll() is None:
        os.kill(init, signal.SIGKILL); verdict = f"still alive after {GRACE}s grace -> SIGKILL (like docker stop after timeout)"
    else: verdict = f"stopped by SIGTERM, rc={p.returncode}"
    out, _ = p.communicate()
    got = "got SIGTERM" in out
    print(f"--- {name}\n    {verdict}\n    app handler ran: {got}")
run("exec form: CMD [python3, server.py]", ["python3", "server.py"])
run("shell form: sh -c 'python3 server.py; true'", ["sh", "-c", "python3 server.py; true"])
run("entrypoint script WITHOUT exec", ["./entrypoint_noexec.sh", "server.py"])
run("entrypoint script WITH exec", ["./entrypoint.sh", "server.py"])
run("exec form but app has NO SIGTERM handler (PID 1 gets no default action)", ["python3", "server_nohandler.py"])
