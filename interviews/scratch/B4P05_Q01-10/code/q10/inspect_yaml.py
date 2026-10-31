import yaml
spec = list(yaml.safe_load_all(open("two_step.yaml")))
doc = spec[0]
print("documents in file     :", len(spec))
print("top-level keys        :", sorted(doc))
print("pipelineInfo          :", doc["pipelineInfo"])
print("components            :", sorted(doc["components"]))
print("executors             :", sorted(doc["deploymentSpec"]["executors"]))
dag = doc["root"]["dag"]["tasks"]
for name, t in dag.items():
    print("task", name, "-> component", t["componentRef"]["name"], "| depends on", t.get("dependentTasks", []))
print("train inputs          :", {k: list(v) for k, v in doc["components"]["comp-train"]["inputDefinitions"].items()})
print("train outputs         :", {k: list(v) for k, v in doc["components"]["comp-train"]["outputDefinitions"].items()})
print("root params           :", doc["root"]["inputDefinitions"]["parameters"])
print("train image           :", doc["deploymentSpec"]["executors"]["exec-train"]["container"]["image"])
