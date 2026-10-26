import json, re, sys

def to_bytes(s):
    m = re.fullmatch(r"(\d+)([kmg]?)", s)
    return int(m.group(1)) * {"": 1, "k": 1024, "m": 1024**2, "g": 1024**3}[m.group(2)]

def check(path):
    try:
        cfg = json.load(open(path))
    except json.JSONDecodeError as e:
        return [f"invalid JSON: {e}"]
    probs = []
    opts = cfg.get("log-opts", {})
    if cfg.get("log-driver", "json-file") == "json-file":
        if "max-size" not in opts: probs.append("json-file without max-size: logs grow without limit")
        for k in ("max-size", "max-file"):
            if k in opts and not isinstance(opts[k], str): probs.append(f"{k} must be a string like '50m', got {type(opts[k]).__name__}")
    if not probs:
        worst = to_bytes(opts["max-size"]) * int(opts.get("max-file", "1"))
        print(f"{path}: OK. Upper bound per container = {opts['max-size']} x {opts.get('max-file','1')} = {worst/1024**2:.0f} MiB")
    return probs

rc = 0
for p in sys.argv[1:]:
    probs = check(p)
    for x in probs: print(f"{p}: PROBLEM: {x}")
    rc |= bool(probs)
sys.exit(rc)
