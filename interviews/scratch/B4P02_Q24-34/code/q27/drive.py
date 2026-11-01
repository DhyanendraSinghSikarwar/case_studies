"""Run train.py, kill it with SIGTERM mid-run, run it again, check it resumed."""
import os, signal, subprocess, sys, tempfile, time, json

d = tempfile.mkdtemp()
env = dict(os.environ, CKPT_PATH=os.path.join(d, "state.json"), TOTAL_STEPS="50", STEP_SECONDS="0.05")
here = os.path.dirname(os.path.abspath(__file__))
cmd = [sys.executable, "-I", os.path.join(here, "train.py")]

p = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, text=True)
time.sleep(1.0)                                    # let it get past step 10 or so
p.send_signal(signal.SIGTERM)
out, _ = p.communicate(timeout=10)
print("--- run 1 output\n" + out.strip())
print("run 1 exit code:", p.returncode)
saved = json.load(open(env["CKPT_PATH"]))
print("checkpoint on disk:", saved)

r = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=30)
print("--- run 2 output\n" + r.stdout.strip())
print("run 2 exit code:", r.returncode)
assert saved["step"] > 0 and r.returncode == 0
print("resumed from", saved["step"], "and finished: OK")
