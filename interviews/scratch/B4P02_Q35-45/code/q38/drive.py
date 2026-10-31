"""Q38 driver. Run: python3 -I drive.py   (needs bash). Runs entrypoint.sh against a fake dependency."""
import os, shutil, signal, subprocess, sys, tempfile, time

here = os.path.dirname(os.path.abspath(__file__))
tmp = tempfile.mkdtemp()
env = dict(os.environ, MODEL_DIR=os.path.join(tmp, "models"), DEP_PORT="5999", DEP_TIMEOUT="10")

def run(script, label, dep_delay="1.5", port="5999"):
    print(f"--- {label}")
    dep = subprocess.Popen([sys.executable, os.path.join(here, "fake_dep.py"), port, dep_delay])
    e = dict(env, DEP_PORT=port)
    p = subprocess.Popen([os.path.join(here, script), sys.executable, os.path.join(here, "server.py"), "q38_server_marker"],
                         env=e, stdout=subprocess.PIPE, text=True)
    time.sleep(3.5)
    print(f"[driver] sending SIGTERM to entrypoint pid {p.pid}", flush=True)
    p.send_signal(signal.SIGTERM)
    try:
        out, _ = p.communicate(timeout=5)
        print(out.rstrip())
        print("[driver] container-like process exited with", p.returncode)
    except subprocess.TimeoutExpired:
        p.kill()
        subprocess.run(["pkill", "-9", "-f", "q38_server_marker"])   # orphan keeps the pipe open
        out, _ = p.communicate(); print(out.rstrip())
        print("[driver] no clean shutdown within 5s: server never saw SIGTERM; killed it by hand")
    dep.kill()

run("entrypoint.sh", "WITH exec", port="5999")
run("entrypoint_noexec.sh", "WITHOUT exec (server is a child of bash)", port="5998")
# timeout path
print("--- dependency never comes up (timeout 2s)")
r = subprocess.run([os.path.join(here, "entrypoint.sh"), "true"], env=dict(env, DEP_PORT="5997", DEP_TIMEOUT="2"),
                   capture_output=True, text=True)
print(r.stdout.rstrip()); print(r.stderr.rstrip()); print("exit code:", r.returncode)
# cleanup stray servers from the no-exec case
subprocess.run(["pkill", "-9", "-f", "q38_server_marker"])
shutil.rmtree(tmp)
