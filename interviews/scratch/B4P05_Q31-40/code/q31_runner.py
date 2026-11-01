"""Tiny pipeline runner: checkpoints, validation gate, eval gate, atomic publish, run lock."""
import json, os, sys, tempfile, shutil

class Crash(Exception): pass

def atomic_write(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f: json.dump(obj, f)
    os.replace(tmp, path)            # atomic on the same filesystem

def validate(rows):
    bad = [r for r in rows if r["label"] not in (0, 1)]
    if len(rows) < 4 or bad:
        raise ValueError(f"validation failed: rows={len(rows)} bad_labels={len(bad)}")

def train(work, rows, crash_at=None):
    ck = os.path.join(work, "ckpt.json")
    state = json.load(open(ck)) if os.path.exists(ck) else {"epoch": 0, "w": 0.0}
    print(f"  train: start at epoch {state['epoch']}")
    while state["epoch"] < 4:
        state["epoch"] += 1
        state["w"] = round(state["w"] + 0.25, 2)
        atomic_write(ck, state)      # checkpoint after every epoch
        if crash_at == state["epoch"]:
            raise Crash(f"spot instance gone after epoch {state['epoch']}")
    return state["w"]

def run(root, run_id, rows, crash_at=None, gate=0.9):
    work = os.path.join(root, "work", run_id); os.makedirs(work, exist_ok=True)
    lock = os.path.join(work, "LOCK")
    try: fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)   # duplicate-run guard
    except FileExistsError: print("  skip: another run holds the lock"); return "locked"
    try:
        validate(rows)
        w = train(work, rows, crash_at)
        score = w * 0.9 if gate > 0.9 else w          # pretend score; low-quality case below
        score = round(score, 2)
        if score < gate:
            print(f"  eval gate FAILED: score {score} < {gate}; production untouched"); return "gate_failed"
        stage = os.path.join(root, "staging_model.json")
        atomic_write(stage, {"run_id": run_id, "w": w, "score": score})
        os.replace(stage, os.path.join(root, "prod_model.json"))   # promote = one rename
        print(f"  published model from {run_id}, score {score}"); return "ok"
    except ValueError as e:
        os.makedirs(os.path.join(root, "dead_letter"), exist_ok=True)
        atomic_write(os.path.join(root, "dead_letter", run_id + ".json"), {"error": str(e), "rows": len(rows)})
        print(f"  {e} -> sent to dead_letter, no training"); return "poisoned"
    except Crash as e:
        print(f"  CRASH: {e}"); return "crashed"
    finally:
        os.close(fd); os.remove(lock)

def prod(root):
    p = os.path.join(root, "prod_model.json")
    return open(p).read() if os.path.exists(p) else "none"

good = [{"x": i, "label": i % 2} for i in range(8)]
poison = good + [{"x": 99, "label": 7}]
root = tempfile.mkdtemp()
print("A. crash mid-training, then rerun same run_id"); print(" attempt 1:", run(root, "r1", good, crash_at=2))
print(" attempt 2:", run(root, "r1", good)); print(" prod:", prod(root))
print("B. poisoned upstream table"); print(" result:", run(root, "r2", poison)); print(" prod unchanged:", prod(root))
print(" dead_letter:", os.listdir(os.path.join(root, "dead_letter")))
print("C. model fails evaluation gate (gate 0.95)"); print(" result:", run(root, "r3", good, gate=0.95)); print(" prod unchanged:", prod(root))
print("D. duplicate run while one is active")
os.makedirs(os.path.join(root, "work", "r4")); open(os.path.join(root, "work", "r4", "LOCK"), "w").close()
print(" result:", run(root, "r4", good))
shutil.rmtree(root)
