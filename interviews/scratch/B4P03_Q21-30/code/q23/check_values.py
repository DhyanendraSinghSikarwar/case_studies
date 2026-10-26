"""Compare values-*.yaml files: same key paths, flag drift. Values may differ; keys should not."""
import sys, yaml

def paths(d, prefix=""):
    out = set()
    for k, v in d.items():
        p = f"{prefix}{k}"
        if isinstance(v, dict) and v:
            out |= paths(v, p + ".")
        else:
            out.add(p)
    return out

files = sys.argv[1:]
keys = {f: paths(yaml.safe_load(open(f))) for f in files}
union = set().union(*keys.values())
bad = False
for f in files:
    missing = sorted(union - keys[f])
    print(f"{f}: {len(keys[f])} keys; missing: {missing or 'none'}")
    bad |= bool(missing)
print("RESULT:", "DRIFT (fix or add to the base values.yaml)" if bad else "same key set")
sys.exit(1 if bad else 0)
