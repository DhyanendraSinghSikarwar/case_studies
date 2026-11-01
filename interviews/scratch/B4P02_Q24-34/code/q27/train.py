"""Training skeleton for spot instances: atomic checkpoints, resume, SIGTERM -> save -> exit 143."""
import json, os, signal, sys, time

CKPT = os.environ.get("CKPT_PATH", "/ckpt/state.json")
TOTAL = int(os.environ.get("TOTAL_STEPS", "50"))
STEP_SECONDS = float(os.environ.get("STEP_SECONDS", "0.05"))
SAVE_EVERY = int(os.environ.get("SAVE_EVERY", "10"))
stop = False

def on_term(signum, frame):
    global stop
    stop = True                                    # only set a flag; do the save in the main loop
    print(f"got signal {signum}, will checkpoint and exit", flush=True)

def save(state):
    tmp = CKPT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, CKPT)                          # atomic: a reader sees the old or the new file, never half

def load():
    try:
        with open(CKPT) as f: return json.load(f)
    except FileNotFoundError:
        return {"step": 0, "loss": 1.0}

signal.signal(signal.SIGTERM, on_term)
state = load()
print(f"start at step {state['step']}", flush=True)
while state["step"] < TOTAL:
    time.sleep(STEP_SECONDS)                       # stands in for one training step
    state["step"] += 1
    state["loss"] = round(1.0 / (1 + state["step"]), 4)
    if state["step"] % SAVE_EVERY == 0: save(state)
    if stop:
        save(state)
        print(f"saved step {state['step']}, exiting 143", flush=True)
        sys.exit(143)                              # 128 + 15: 'stopped by SIGTERM', orchestrator can retry
save(state)
print(f"done at step {state['step']}, loss {state['loss']}", flush=True)
