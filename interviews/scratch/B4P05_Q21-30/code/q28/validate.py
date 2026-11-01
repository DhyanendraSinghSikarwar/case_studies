import re, sys, yaml

def check_workflow(spec, label):
    errs = []
    templates = {t["name"]: t for t in spec["templates"]}
    if spec["entrypoint"] not in templates:
        errs.append(f"entrypoint {spec['entrypoint']!r} is not a template")
    wf_params = {p["name"] for p in spec.get("arguments", {}).get("parameters", [])}
    for t in spec["templates"]:
        body = t.get("dag", {}).get("tasks", [])
        names = {x["name"] for x in body}
        for x in body:
            if x["template"] not in templates:
                errs.append(f"task {x['name']}: unknown template {x['template']!r}")
            for d in x.get("dependencies", []):
                if d not in names:
                    errs.append(f"task {x['name']}: unknown dependency {d!r}")
        declared = {p["name"] for p in t.get("inputs", {}).get("parameters", [])}
        for ref in re.findall(r"{{inputs\.parameters\.([\w-]+)}}", yaml.dump(t.get("container", {}))):
            if ref not in declared:
                errs.append(f"template {t['name']}: uses inputs.parameters.{ref} but does not declare it")
        for ref in re.findall(r"{{workflow\.parameters\.([\w-]+)}}", yaml.dump(t)):
            if ref not in wf_params:
                errs.append(f"template {t['name']}: workflow.parameters.{ref} not in spec.arguments")
    print(f"{label}: templates={sorted(templates)} errors={errs or 'none'}")
    return not errs

docs = list(yaml.safe_load_all(open(sys.argv[1])))
for d in docs:
    assert d["apiVersion"].startswith("argoproj.io/"), d["apiVersion"]
    print("kind:", d["kind"])
    if d["kind"] == "Workflow":
        check_workflow(d["spec"], "good workflow")
    else:
        print("cron schedule:", d["spec"]["schedule"], "| concurrencyPolicy:", d["spec"]["concurrencyPolicy"])
        check_workflow(d["spec"]["workflowSpec"], "cron workflowSpec")
# negative test: break it on purpose
bad = yaml.safe_load(open(sys.argv[1]).read().split("---")[0])
bad["spec"]["templates"][0]["dag"]["tasks"][1]["dependencies"] = ["trian"]
bad["spec"]["templates"][1]["container"]["args"][0] += " {{inputs.parameters.epochs}}"
check_workflow(bad["spec"], "broken workflow")
