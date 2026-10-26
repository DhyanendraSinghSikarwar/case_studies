"""Spot-safe training loop in pure Python: checkpoint everything, resume, compare with uninterrupted run."""
import json, os, random, sys, tempfile, hashlib

class Interrupted(Exception):
    pass

def make_data(n=64, seed=7):
    r = random.Random(seed)
    return [(x, 3.0 * x + 1.0 + r.gauss(0, 0.1)) for x in (r.uniform(-1, 1) for _ in range(n))]

def save_ckpt(path, state):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f)
    os.replace(tmp, path)  # atomic: a reclaim mid-write must not leave a half file

def train(ckpt, total_steps=200, every=25, interrupt_at=None, batch=8, seed=123):
    data = make_data()
    st = {"step": 0, "w": 0.0, "b": 0.0, "mw": 0.0, "mb": 0.0, "rng": None}
    rng = random.Random(seed)
    if os.path.exists(ckpt):
        st = json.load(open(ckpt))
        rng.setstate((st["rng"][0], tuple(st["rng"][1]), st["rng"][2]))
        print(f"  resumed at step {st['step']}")
    while st["step"] < total_steps:
        if interrupt_at is not None and st["step"] == interrupt_at:
            raise Interrupted(f"reclaimed at step {st['step']}")
        lr = 0.1 * (0.99 ** st["step"])              # scheduler state is a function of step
        b_ = rng.sample(data, batch)                  # data position = RNG state
        gw = sum(2 * (st["w"] * x + st["b"] - y) * x for x, y in b_) / batch
        gb = sum(2 * (st["w"] * x + st["b"] - y) for x, y in b_) / batch
        st["mw"] = 0.9 * st["mw"] + gw               # optimizer state (momentum)
        st["mb"] = 0.9 * st["mb"] + gb
        st["w"] -= lr * st["mw"]; st["b"] -= lr * st["mb"]
        st["step"] += 1
        if st["step"] % every == 0:
            s = rng.getstate()
            save_ckpt(ckpt, {**st, "rng": [s[0], list(s[1]), s[2]]})
    return st

def train_sloppy(ckpt, total_steps=200, batch=8):
    data = make_data()
    st = json.load(open(ckpt))
    rng = random.Random(999)  # wrong: fresh RNG instead of the saved state
    while st["step"] < total_steps:
        lr = 0.1 * (0.99 ** st["step"])
        b_ = rng.sample(data, batch)
        gw = sum(2 * (st["w"] * x + st["b"] - y) * x for x, y in b_) / batch
        gb = sum(2 * (st["w"] * x + st["b"] - y) for x, y in b_) / batch
        st["mw"] = 0.9 * st["mw"] + gw; st["mb"] = 0.9 * st["mb"] + gb
        st["w"] -= lr * st["mw"]; st["b"] -= lr * st["mb"]; st["step"] += 1
    return st

def digest(st):
    return hashlib.sha256(json.dumps([st["w"], st["b"]]).encode()).hexdigest()[:12]

with tempfile.TemporaryDirectory() as d:
    print("A) uninterrupted run")
    a = train(os.path.join(d, "a.json"), every=10**9)
    print(f"  w={a['w']:.6f} b={a['b']:.6f} digest={digest(a)}")
    print("B) interrupted at step 130, last checkpoint at 125, then resume")
    p = os.path.join(d, "b.json")
    try:
        train(p, interrupt_at=130)
    except Interrupted as e:
        print(" ", e)
    b = train(p)
    print(f"  w={b['w']:.6f} b={b['b']:.6f} digest={digest(b)}")
    print("identical to uninterrupted:", a["w"] == b["w"] and a["b"] == b["b"])
    print("C) sloppy resume: weights and step only (no momentum, no RNG state)")
    full = json.load(open(p))
    # re-create the step-125 checkpoint by re-running to 125, then load it sloppily
    q = os.path.join(d, "c.json")
    try:
        train(q, total_steps=125, every=25)
    except Interrupted:
        pass
    ck = json.load(open(q))
    json.dump({"step": ck["step"], "w": ck["w"], "b": ck["b"], "mw": 0.0, "mb": 0.0, "rng": None}, open(q, "w"))
    c = train_sloppy(q)
    print(f"  w={c['w']:.6f} b={c['b']:.6f} digest={digest(c)}")
    print("sloppy equals uninterrupted:", a["w"] == c["w"] and a["b"] == c["b"])
