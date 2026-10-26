import yaml
docs = list(yaml.safe_load_all(open("pipeline.yaml")))
print("yaml documents:", len(docs), "(0 = pipeline spec, 1 = platform spec)" if len(docs) > 1 else "")
spec = docs[0]
print("pipelineInfo.name:", spec["pipelineInfo"]["name"])
print("input parameters:", {k: (v["parameterType"], v.get("defaultValue")) for k, v in spec["root"]["inputDefinitions"]["parameters"].items()})
print("components:", sorted(spec["components"]))
print("root dag tasks:", sorted(spec["root"]["dag"]["tasks"]))
for name, c in sorted(spec["components"].items()):
    if "dag" in c:
        print(f"  {name}: tasks={sorted(c['dag']['tasks'])}")
for name, t in sorted(spec["root"]["dag"]["tasks"].items()):
    print(f"  root.{name}: dependentTasks={t.get('dependentTasks', [])} trigger={t.get('triggerPolicy', {}).get('strategy')}")
def walk(d, path=""):
    for name, t in d["dag"]["tasks"].items():
        extra = {k: t[k] for k in ("parameterIterator", "triggerPolicy") if k in t}
        if "parameterIterator" in t: print(f"  {path}{name}: parameterIterator items={t['parameterIterator']['items']}")
        if "triggerPolicy" in t: print(f"  {path}{name}: condition={t['triggerPolicy']['condition']}")
        ref = t.get("componentRef", {}).get("name")
        if ref in spec["components"] and "dag" in spec["components"][ref]:
            walk(spec["components"][ref], path + name + "/")
walk(spec["root"])
ex = [e for k, e in spec["deploymentSpec"]["executors"].items() if k.startswith("exec-train")][0]["container"]
print("train executor resources:", ex.get("resources"))
if len(docs) > 1:
    pk = docs[1]["platforms"]["kubernetes"]["deploymentSpec"]["executors"]
    for k, v in pk.items():
        print("platform executor", k, "->", sorted(v))
        print("   nodeSelector:", v.get("nodeSelector"), "| tolerations:", v.get("tolerations"), "| secretAsEnv:", v.get("secretAsEnv"))
