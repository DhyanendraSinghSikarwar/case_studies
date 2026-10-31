# validate_ensemble.py REPO : every tensor a step consumes is produced earlier; every model exists; python files compile.
import sys, pathlib, ast
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from pbtxt import parse
def load(repo):
    return {p.name: parse((p / "config.pbtxt").read_text()) for p in pathlib.Path(repo).iterdir() if (p / "config.pbtxt").exists()}
def check(cfgs, name="pipeline"):
    errs, ens = [], cfgs[name]
    known = {t["name"][0] for t in ens["input"]}                 # tensors available: ensemble inputs
    for n, s in enumerate(ens["ensemble_scheduling"][0]["step"], 1):
        m = s["model_name"][0]
        if m not in cfgs: errs.append(f"step {n}: model {m} not in repository"); continue
        inner_in = {t["name"][0] for t in cfgs[m]["input"]}; inner_out = {t["name"][0] for t in cfgs[m]["output"]}
        for kv in s.get("input_map", []):
            k, v = kv["key"][0], kv["value"][0]
            if k not in inner_in: errs.append(f"step {n}: {m} has no input {k}")
            if v not in known: errs.append(f"step {n}: tensor {v} is consumed before anything produces it")
        for kv in s.get("output_map", []):
            k, v = kv["key"][0], kv["value"][0]
            if k not in inner_out: errs.append(f"step {n}: {m} has no output {k}")
            known.add(v)
    for t in ens["output"]:
        if t["name"][0] not in known: errs.append(f"ensemble output {t['name'][0]} is never produced")
    return errs
repo = sys.argv[1]; cfgs = load(repo)
print("models found:", sorted(cfgs))
print("wiring problems:", check(cfgs) or "none")
for f in pathlib.Path(repo).rglob("model.py"):
    tree = ast.parse(f.read_text()); cls = [n for n in tree.body if isinstance(n, ast.ClassDef)][0]
    print(f"{f.relative_to(repo)}: class {cls.name}, methods {[n.name for n in cls.body if isinstance(n, ast.FunctionDef)]}")
# broken copy: classifier reads a tensor nobody produces
cfgs["pipeline"]["ensemble_scheduling"][0]["step"][1]["input_map"][0]["value"] = ["features_typo"]
print("after introducing a typo:", check(cfgs))
